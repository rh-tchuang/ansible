# coding: utf-8
# Copyright: (c) 2019, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import asyncio
import os
import os.path
import pathlib
import sys
import tarfile
from collections import defaultdict
from distutils.version import LooseVersion
from functools import partial
from tempfile import TemporaryDirectory

import yaml
from jinja2 import Environment, FileSystemLoader
from ansible.galaxy.api import GalaxyAPI
from ansible.module_utils._text import to_bytes, to_native
from ansible.module_utils.urls import Request

# Pylint doesn't understand Python3 namespace modules.
# pylint: disable=relative-beyond-top-level
from ..change_detection import update_file_if_different
from ..commands import Command
from ..jinja2.environment import doc_environment
from ..jinja2.filters import documented_type, html_ify
from ..document_plugins import (get_plugin_info, init_plugin_doc_arg_parser,
                                normalize_plugin_info, plugin_filename_format,
                                plugin_output_directory)
# pylint: enable=relative-beyond-top-level


PLUGIN_TYPES = frozenset(('become', 'cache', 'callback', 'cliconf', 'connection', 'httpapi',
                          'inventory', 'lookup', 'shell', 'strategy', 'vars', 'module',
                          'module_utils'))
DOCUMENTED_PLUGIN_TYPES = frozenset(('module',))
DEFAULT_PLUGIN_TO_COLLECTION_FILE = (pathlib.Path(__file__).parents[4]
                                     / 'docs/docsite/collection-plugins.yml')

DOCS_SITE = 'https://docs.ansible.com/ansible/collections/plugins/'
GALAXY_SERVER = 'galaxy.ansible.com'
MAX_PAGE_SIZE = 1000  # The galaxy server has a max page size

# Testing config
GALAXY_SERVER = 'galaxy-dev.ansible.com'

DEFAULT_TEMPLATE_DIR = pathlib.Path(__file__).parents[4] / 'docs/templates'
DEFAULT_STUB_TEMPLATE_FILE = 'moved_to_collections.rst.j2'
DEFAULT_PLUGIN_TEMPLATE_FILE = 'collectionized_plugin.rst.j2'
DEFAULT_OUTPUT_DIR = pathlib.Path(__file__).parents[4] / 'docs/docsite/rst'


#
# Exceptions
#

class UnreleasedCollectionError(Exception):
    """Raised when a collection has no releases available"""
    pass


class UnknownCollectionNameFormat(Exception):
    """A collection's tarball name was in an unanticipated format"""
    pass


#
# Common utility functions
#

def plugin_to_collection_mapping(mapping_filename):
    """
    Return the data that maps all plugins inside of ansible to their collection location.

    :arg mapping_filename: The filename in which the data lives
    :return: The returned data is structured as a set of dicts::

        plugin_type:
            plugin_name:
                source: "Service that this lives on.  For example https://galaxy.ansible.com/"
                fqcn: "Full qualified collection name.  For example purestorage.flasharray"
            plugin_name2:
            [..]
        plugin_type2:
        [..]

    """
    with open(mapping_filename, 'rb') as f:
        plugin_to_collection_mapping = yaml.safe_load(f.read())
    return plugin_to_collection_mapping


def get_running_loop():
    """
    Do our best to get the running loop

    Python-3.7 has a special function for this but older Pythons have a different function which is
    not robust in some cornercases which we hopefully will not encounter.
    """
    if sys.version_info >= (3, 7):
        return asyncio.get_running_loop()
    return asyncio.get_event_loop()


class CollectionFetcher:
    """
    Fetches collections from a galaxy server to a directory.

    .. warn:: This class is used in multithreaded code.  It is designed to be initialized and then
        none of the attributes it contains are changed by any of the methods.  This makes the
        methods safe for use inside of multithreaded code.  If you need to use different attributes,
        you need to use a new instance of this object.  If you are writing new methods, be sure your
        methods do not write to any of the attributes.
    """
    CHUNK_SIZE = 4096

    def __init__(self, server, destdir):
        """
        :server: The galaxy server to fetch from
        :destdir: The destination directory to fetch to
        """
        self.api = GalaxyAPI(None, None, server)
        self.destdir = destdir

    def _construct_filename(self, download_url):
        """Construct a filename for the collection inside of the destdir"""
        base_filename = os.path.basename(download_url)
        return os.path.join(self.destdir, base_filename)

    def fetch_collection(self, namespace, name, newer_than=None):
        """
        Retrieves the latest version of the collection to the CollectionFetcher's destdir

        :arg namespace: Namespace of the collection
        :arg name: Name of the collection
        :arg newer_then: If this is set, it must be a version string understood by
            :py3:`distutils.versioning.LooseVersion` we only download a collection if it is newer
            than this version string.  If this is not set, then we always download the latest
            version of the collection.
        :returns: filename of the fetched collection or None if no collection was retrieved
        :raises UnreleasedCollectionError: if the specified collection has no releases to download
        """
        # Find the latest version of a collection.
        # Requires one round trip
        versions = self.api.get_collection_versions(namespace, name)
        if len(versions) <= 0:
            raise UnreleasedCollectionError('Collection {namespace}.{name} does not yet have any'
                                            ' releases'.format(namespace=namespace, name=name))
        latest = sorted(versions, key=LooseVersion)[0]

        if newer_than and LooseVersion(newer_than) > LooseVersion(latest):
            return None

        # Get the download url for the latest version of the collection
        # Roundtrip #2
        collection_info = self.api.get_collection_version_metadata(namespace, name, latest)
        filename = self._construct_filename(collection_info.download_url)

        requestor = Request()
        response_handle = requestor.get(collection_info.download_url)
        with open(filename, 'wb') as f:
            # Replace with walrus operator when we can require python-3.8
            # while chunk := response_handle.read(self.CHUNK_SIZE):
            #   f.write(chunk)
            chunk = response_handle.read(self.CHUNK_SIZE)
            while chunk:
                f.write(chunk)
                chunk = response_handle.read(self.CHUNK_SIZE)

        return filename


#
# Subcommand validate
#

def validate(args):
    """
    Validate the structure of the yaml file

    :args args: The parsed command line arguments

    Schema example:
    .. code-block:: yaml

        modules:
          ec2:
            fqcn: "ansible_aws_sig.amazon"
            source: "https://galaxy.ansible.com"
          ec2_remove_host:
            fqcn: "ansible_aws_sig.ec2"
            source: "https://dev.ansible.redhat.com/api/automation-hub"
        filters:
          ipaddress:
            fqcn: "ansible_ipadress.ipaddress"
            source: "https://galaxy.ansible.com"
    """
    # Import voluptuous here so that it is only a dependency of the validation, not of the rest of
    # the script
    import voluptuous as v

    collection_mapping_schema = v.Schema({v.Any(*PLUGIN_TYPES): {
        str: {'fqcn': str,
              'source': str}
    }})

    plugin_mapping = plugin_to_collection_mapping(args.plugin_to_collection_file)
    return collection_mapping_schema(plugin_mapping)


#
# Subcommand full
#

async def fetch_collections(destdir, fqcns):
    """
    Fetch all of the collections to the destdir
    """
    loop = get_running_loop()

    requestors = []
    for server in fqcns:
        fetcher = CollectionFetcher(server, destdir)
        for fqcn in fqcns[server]:
            requestors.append(loop.run_in_executor(None, fetcher.fetch_collection,
                                                   *fqcn.split('.', 1)))

    await asyncio.gather(*requestors)


def expand_collection(tar_file, expand_dir):
    # TODO: Is the filename normalized by galaxy or could we get a filename that was arbitrarily
    # determined by the uploading user?
    # According to rich, the filename is validated by galaxy so if it doesn't match
    # namespace.collection-version.tar.gz, then it is rejected.

    # Derive the fqcn from the tar_file name
    tar_name_parts = os.path.basename(tar_file).split('-')
    if len(tar_name_parts) != 3:
        raise UnknownCollectionNameFormat('The name of the tarball for a collection did not meet'
                                          ' our assumptions.  This code has to be recoded to allow'
                                          ' for this name: {0}'.format(tar_file))
    fqcn = '.'.join(tar_name_parts[0:2])

    dir_name = os.path.join(expand_dir, fqcn)

    with tarfile.open(tar_file, 'r') as collection_tar:
        return collection_tar.extractall(path=dir_name)


async def expand_collections(tar_dir, expand_dir):
    """
    Expand all collections in the tar_dir into expand_dir

    :tar_dir: Directory where the collections have been placed
    :expand_dir: Directory where the expanded collections will live
    """
    loop = get_running_loop()

    expanders = []
    for filename in os.listdir(tar_dir):
        tar_file = os.path.join(tar_dir, filename)
        expanders.append(loop.run_in_executor(None, expand_collection, tar_file, expand_dir))

    await asyncio.gather(*expanders)


def write_stubs(plugin_type, plugin_name, collection, jinja_env, stub_dir):
    """
    Output an html page at the old location that says the plugin has moved to a collection

    :arg plugin_type: Is the plugin a module, module_util, callback, connection, etc
    :arg plugin_name: The name of the plugin
    :arg collection: FQCN for the collection which contains the plugin
    :arg jinja_env: The jinja2 environment in which te template for the stub pages resides
    :arg stub_dir: The directory to output the stub file to.
    """
    stub_template = jinja_env.get_template('moved_to_collections.rst.j2')
    stub_file = stub_template.render({'plugin_type': plugin_type,
                                      'module': plugin_name,
                                      'collection': collection['fqcn'],
                                      })

    output_file = plugin_filename_format(plugin_type) % plugin_name
    filename = os.path.join(stub_dir, output_file)
    with open(filename, 'w') as f:
        f.write(stub_file)


def write_collection_doc(plugin_type, plugin_name, collection, jinja_env, input_dir,
                         collection_doc_dir):
    # Determine which file in the collection has the plugin's docs
    if plugin_type in ('module', 'module_util'):
        plugin_dir = '{0}s'.format(plugin_type)
    else:
        plugin_dir = plugin_type

    plugin_file = os.path.join(input_dir, collection['fqcn'], 'plugins', plugin_dir,
                               '%s.py' % plugin_name)

    # Get the documentation data from the plugin
    try:
        plugin_data = get_plugin_info(plugin_name, plugin_file, input_dir)
    except Exception as e:
        print("*** ERROR: Malformed documentation in %s: %s ***" % (plugin_file, to_native(e)))

    # Format the data into the form the templates expect
    aliases = set()  # Current collections implementation does not have aliases
    normalize_plugin_info(plugin_data['doc'], plugin_name, collection['fqcn'],
                          collection['source'], plugin_data['source'], plugin_type,
                          plugin_data['deprecated'], aliases, plugin_data['metadata'],
                          plugin_data['examples'], plugin_data['returndocs'])
    plugin_data = plugin_data['doc']

    # Pass the documentation into the jinja2 render function
    plugin_template = jinja_env.get_template('plugin.rst.j2')
    plugin_file = plugin_template.render(**plugin_data)

    # Write the docs to the plugin_name.rst file
    filename = os.path.join(collection_doc_dir, '%s.rst' % plugin_name)
    with open(filename, 'w') as f:
        f.write(plugin_file)


async def write_docs(plugin_mapping_for_type, plugin_type, template_dir, input_dir, output_dir):
    loop = get_running_loop()

    # Setup output directory for this plugin type
    stub_dir = plugin_output_directory(plugin_type, output_dir)

    if not os.path.exists(stub_dir):
        os.mkdir(stub_dir)

    collection_doc_dir = os.path.join(output_dir, 'collections')
    if not os.path.exists(collection_doc_dir):
        os.mkdir(collection_doc_dir)

    collection_doc_dir = os.path.join(collection_doc_dir, plugin_type)
    if not os.path.exists(collection_doc_dir):
        os.mkdir(collection_doc_dir)

    jinja_env = doc_environment(template_dir)

    writers = []
    for plugin_name, collection in plugin_mapping_for_type.items():
        writers.append(loop.run_in_executor(None, write_stubs, plugin_type, plugin_name, collection,
                                            jinja_env, stub_dir))
        writers.append(loop.run_in_executor(None, write_collection_doc, plugin_type, plugin_name,
                                            collection, jinja_env, input_dir, collection_doc_dir))

    await asyncio.gather(*writers)


def generate_full_docs(args):
    """Regenerate the documentation for all plugins listed in the plugin_to_collection_file"""
    loop = None
    if sys.version_info < (3, 7):
        # Event loop hasn't started yet, so don't use get_running_loop()
        loop = asyncio.get_event_loop()
        asyncio_run = loop.run_until_complete
    else:
        asyncio_run = asyncio.run

    fqcns_by_server = defaultdict(set)
    plugin_mapping = plugin_to_collection_mapping(args.plugin_to_collection_file)
    for plugins in plugin_mapping.values():
        for collection in plugins.values():
            fqcns_by_server[collection['source']].add(collection['fqcn'])

    with TemporaryDirectory() as tmpdir:
        download_dir = os.path.join(tmpdir, 'download')
        os.mkdir(download_dir)
        asyncio_run(fetch_collections(download_dir, fqcns_by_server))

        expanded_dir = os.path.join(tmpdir, 'expanded')
        os.mkdir(expanded_dir)
        asyncio_run(expand_collections(download_dir, expanded_dir))

        # We only provide backwards compatible documentation for a subset of the plugin types
        for plugin_type in DOCUMENTED_PLUGIN_TYPES:
            asyncio_run(write_docs(plugin_mapping[plugin_type], plugin_type, args.template_dir,
                                   expanded_dir, args.output_dir))


#
# Subcommand incremental
#
def retrieve_collection_changes():
    """Retrieve changed collections from the galaxy server"""
    collection_map = {}
    page = '/api/v2/collections/?page_size={0}'.format(MAX_PAGE_SIZE)
    while page is not None:
        requestor = Request()
        response = requestor.get('https://{0}{1}'.format(GALAXY_SERVER, page))
        response_data = response.json()
        # Key by (namespace, collection name)
        collection_map.update({(rec['namespace']['name'], rec['name']):
                               rec['latest_version']['version']
                               for rec in response_data['results']})
        page = response_data["next"]

    return collection_map


def generate_incremental_docs(args):
    """Regenerate documentation for plugins whose collections have updated since the last build"""
    plugin_mapping = plugin_to_collection_mapping(args.plugin_to_collection_file)
    for plugins in plugin_mapping.values():
        pass
    # update_file_if_different(output_name, data)

    # Get the list of collections that we care about
    # Get the last generation time from the website
    # Get the changes since the last generation time
    # Get the files for the updated collections
    # Build docs for the plugins in the updated collections
    # Copy the new plugins into the tree
    # Update the last generation timestamp
    # Copy the new plugins into the tree

# How does this differ from the standard PluginDocs?
# Needs to be able to target per-directory
# Need to assemble from a combination of current collection plugin docs and the new thing that we
# create
#
# Also need to modify the current plugin docs generation so that it can point to these docs if these
# docs are going to exist


class CollectionPluginDocs(Command):
    name = 'document-collection-plugins'
    _ACTION_HELP = """Action to perform.
        validate: verifies the structure of the yaml file with the list of plugins.
        full: regenerate the documentation for all the plugins in the yaml file.
        incremental: regenerate the documentation for the plugins which have changed since the
            website was last updated (Not yet implemented)
    """

    @classmethod
    def init_parser(cls, add_parser):
        parser = add_parser(cls.name,
                            description='Generate documentation for plugins in collections.'
                            ' Plugins in collections will have a stub file in the normal plugin'
                            ' documentation location that says the module is in a collection and'
                            ' point to generated plugin documentation under the collections/'
                            ' hierarchy.')
        init_plugin_doc_arg_parser(parser)
        parser.add_argument('action', action='store', choices=('incremental', 'full', 'validate'),
                            default='full', help=cls._ACTION_HELP)
        parser.add_argument('--plugin-to-collection-file', action='store',
                            default=str(DEFAULT_PLUGIN_TO_COLLECTION_FILE),
                            help='Path to the file which lists the plugins to document which now'
                                 ' live in collections')
        parser.add_argument("-t", "--template-file", action="store", dest="template_file",
                            default=DEFAULT_PLUGIN_TEMPLATE_FILE,
                            help="Jinja2 template to use for the collectionized-plugins")
        parser.add_argument("--stub-template-file", action="store", dest="template_file",
                            default=DEFAULT_STUB_TEMPLATE_FILE,
                            help="Jinja2 template to point at the collectionized-plugin docs")

    @staticmethod
    def main(args):
        if not args.template_dir:
            args.template_dir = [os.path.abspath(str(DEFAULT_TEMPLATE_DIR))]
        if not args.output_dir:
            args.output_dir = os.path.abspath(str(DEFAULT_OUTPUT_DIR))

        if args.action == 'validate':
            try:
                validate(args)
            except Exception:
                print('{0} was *invalid*'.format(args.plugin_to_collection_file))
                raise
            else:
                print('{0} was *valid*'.format(args.plugin_to_collection_file))

        elif args.action == 'full':
            generate_full_docs(args)

        else:
            # args.action == 'incremental' (Invalid actions are caught by argparse)
            generate_incremental_docs(args)

        return 0
