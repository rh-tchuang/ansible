.. _developing_modules_in_groups:

*********************************************
Information for submitting a group of modules
*********************************************

Submitting a group of modules
=============================

In Ansible 2.8 and earlier, developers had to submit groups of related modules to the ansible/ansible repository. Beginning with Ansible 2.9, we introduced collections, which allow developers to release and distribute groups of related modules on their own timelines. This page offers tips and tricks about naming modules, testing code, and other topics that will help you create clean, usable collections for your products or your use cases.

.. include:: shared_snippets/licensing.txt

.. contents::
   :local:

Before you start coding
=======================

These prerequisites will help you develop high-quality modules and a coherent collection that users can easily adopt and you can easily maintain.

* Read though all the pages linked off :ref:`developing_modules_general`; paying particular focus to the :ref:`developing_modules_checklist`.
* Create modules that comply with PEP 8. See :ref:`testing_pep8` for more information.
* Create modules that :ref:`support Python 2.6+ and Python 3.5+ <developing_python_3>`.
* Establish a naming convention for the modules in your collection. You may want to review other collections in the same functional area (such as cloud, networking, databases).
* ``TODO: find correct location within a collection!`` Place shared code in ``lib/ansible/module_utils/``
* ``TODO: find correct location within a collection!`` Place shared documentation (for example describing common arguments) n ``lib/ansible/plugins/doc_fragments/``.
* Plan for collection maintenance. Ansible collection maintainers have a duty to help keep modules up to date. As with all successful community projects, collection maintainers should keep a watchful eye for reported issues and contributions.
* Add unit and/or integration tests whenever possible. Unit tests are especially valuable when external resources (such as cloud or network devices) are required. For more information see :ref:`developing_testing` and the `Testing Working Group <https://github.com/ansible/community/blob/master/meetings/README.md>`_.


Naming convention
=================

You collection name should represent the *product* or *OS* name, not the company name. Each module should have the same (or similar) prefix.

**Note:**

* File and directory names are always in lower case
* Words are separated with an underscore (``_``) character
* Module names should be in the singular, rather than plural, eg ``command`` not ``commands``


Leveraging community knowledge
==============================

Ansible has a thriving and knowledgeable community of module developers, including Ansible employees, partner employees, and volunteers. These developers can answer questions, offer advice, and help you avoid common mistakes. If you are creating a new collection, circulating your ideas before coding can help. Write a list of your proposed module names and a short description of what they will achieve, then submit that information on IRC or to a mailing list for interactive dialogue. Community feedback will ensure the modules fit the way people have used Ansible Modules before, and therefore make them easier to use.

The :ref:`communication` page includes details on subscribing to mailing lists, joining IRC channels, and participating in IRC meetings. For developers, we recommend:

* the Ansible Development and Ansible Announce mailing lists
* the ``#ansible-devel`` channel on FreeNode's IRC network
* various weekly IRC meetings, see the `meeting schedule and agenda page <https://github.com/ansible/community/blob/master/meetings/README.md>`_


Creating your collection
========================

Now that you've reviewed this document, you should be ready to create your collection.

* defines the namespace
* provides a basis for detailed review that will help shape your future PRs
* may include shared documentation (`doc_fragments`) that multiple modules require
* may include shared code (`module_utils`) that multiple modules require


The first PR should include the following files:

* ``lib/ansible/modules/$category/$topic/__init__.py`` - An empty file to initialize namespace and allow Python to import the files. *Required new file*
* ``lib/ansible/modules/$category/$topic/$yourfirstmodule.py`` - A single module. *Required new file*
* ``lib/ansible/plugins/doc_fragments/$topic.py`` - Code documentation, such as details regarding common arguments. *Optional new file*
* ``lib/ansible/module_utils/$topic.py`` - Code shared between more than one module, such as common arguments. *Optional new file*

And that's it.

Before pushing your PR to GitHub it's a good idea to review the :ref:`developing_modules_checklist` again.

Subsequent PRs
==============

By this point you first PR that defined the module namespace should have been merged. You can take the lessons learned from the first PR and apply it to the rest of the modules.

Raise exactly one PR per module for the remaining modules.

Over the years we've experimented with different sized module PRs, ranging from one module to many tens of modules, and during that time we've found the following:

* A PR with a single file gets a higher quality review
* PRs with multiple modules are harder for the creator to ensure all feedback has been applied
* PRs with many modules take a lot more work to review, and tend to get passed over for easier-to-review PRs.

You can raise up to five PRs at once (5 PRs = 5 new modules) **after** your first PR has been merged. We've found this is a good batch size to keep the review process flowing.

Maintaining your modules
========================

Now that your modules are integrated there are a few bits of housekeeping to be done.

**Bot Meta**
Update `Ansibullbot` so it knows who to notify if/when bugs or PRs are raised against your modules
`BOTMETA.yml <https://github.com/ansible/ansible/blob/devel/.github/BOTMETA.yml>`_.

If there are multiple people that can be notified, please list them. That avoids waiting on a single person who may be unavailable for any reason. Note that in `BOTMETA.yml` you can take ownership of an entire directory.


**Review Module web docs**
Review the autogenerated module documentation for each of your modules, found in :ref:`Module Docs <modules_by_category>` to ensure they are correctly formatted. If there are any issues please fix by raising a single PR.

If the module documentation hasn't been published live yet, please let a member of the Ansible Core Team know in the ``#ansible-devel`` IRC channel.

.. note:: Consider adding a scenario guide to cover how to use your set of modules. Use the :ref:`sample scenario guide rst file <scenario_template>` to help you get started. For network modules, see :ref:`documenting_modules_network` for further documentation requirements.

New to git or GitHub
====================

We realize this may be your first use of Git or GitHub. The following guides may be of use:

* `How to create a fork of ansible/ansible <https://help.github.com/articles/fork-a-repo/>`_
* `How to sync (update) your fork <https://help.github.com/articles/syncing-a-fork/>`_
* `How to create a Pull Request (PR) <https://help.github.com/articles/about-pull-requests/>`_

Please note that in the Ansible Git Repo the main branch is called ``devel`` rather than ``master``, which is used in the official GitHub documentation.

After your first PR has been merged, you must "sync your fork" with ``ansible/ansible`` to ensure you've pulled in the directory structure and and shared code or documentation previously created.

As stated in the GitHub documentation, always use feature branches for your PRs, never commit directly into ``devel``.
