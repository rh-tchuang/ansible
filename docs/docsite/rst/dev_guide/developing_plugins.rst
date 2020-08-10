.. _developing_plugins:
.. _plugin_guidelines:

******************
プラグインの開発
******************

.. contents::
   :local:

プラグインは、すべてのモジュールがアクセスできるロジックおよび機能を使用して Ansible のコア機能を拡張します。Ansible には、便利なプラグインが多数同梱されています。また、簡単に独自のプラグインを作成することもできます。すべてのプラグインは、以下の条件を満たす必要があります。

* Python で書かれている。
* エラーを発生させる。
* Unicode で文字列を返す。
* Ansible の設定およびドキュメントの標準仕様に準拠する。

これらの一般的なガイドラインを確認したら、開発する特定のタイプのプラグインを参照してください。

Python でのプラグインの作成
=========================

``PluginLoader`` により読み込まれ、モジュールが使用できる Python オブジェクトとして返すには、Python でプラグインを作成する必要があります。プラグインはコントローラーで実行するため、:ref:`互換性のある Python バージョン <control_node_requirements>` で作成する必要があります。

エラーの発生
==============

プラグインの実行中に発生したエラーは、``AnsibleError()`` または同様のクラスでエラーを記述したメッセージを発生させて返す必要があります。他の例外をエラーメッセージにラップする場合は、Python のバージョン間で適切な文字列の互換性を確保するために、常に Ansible 関数の ``to_native`` を使用する必要があります。

.. code-block:: python

    from ansible.module_utils._text import to_native

    try:
        cause_an_exception()
    except Exception as e:
        raise AnsibleError('Something happened, this was original exception: %s' % to_native(e))

様々な `AnsibleError オブジェクト <https://github.com/ansible/ansible/blob/devel/lib/ansible/errors/__init__.py>`_ を確認して、お使いの状況に最適なものを確認します。

文字列エンコーディング
===============

プラグインによって返される文字列は、Python の Unicode タイプに変換する必要があります。Unicode に変換すると、これらの文字列が Jinja2 を介して実行できるようになります。文字列を変換するには、次を実行します。

.. code-block:: python

    from ansible.module_utils._text import to_text
    result_string = to_text(result_string)

プラグインの設定およびドキュメントの標準仕様
==============================================

プラグインの設定可能なオプションを定義するには、python ファイルの ``DOCUMENTATION`` セクションで説明します。Ansible バージョン 2.4 以降、コールバックおよび接続プラグインはこの方法で設定要件を宣言しました。ほとんどのプラグインが同じように動作するようになりました。この方法により、プラグインのオプションのドキュメントを常に正しく最新の状態に保つことができます。設定可能なオプションをプラグインに追加するには、以下の形式で定義します。

.. code-block:: yaml

    options:
      option_name:
        description: describe this config option
        default: default value for this config option
        env:
          - name: NAME_OF_ENV_VAR
        ini:
          - section: section_of_ansible.cfg_where_this_config_option_is_defined
            key: key_used_in_ansible.cfg
        required: True/False
        type: boolean/float/integer/list/none/path/pathlist/pathspec/string/tmppath
        version_added: X.x

プラグインの構成設定にアクセスするには、``self.get_option(<option_name>)`` を使用します。ほとんどのプラグインタイプでは、コントローラーは設定を事前入力します。設定を明示的に入力する必要がある場合は、``self.set_options()`` 呼び出しを使用します。


組み込みドキュメンテーションをサポートするプラグイン (そのリストの「:ref:`ansible-doc`」参照) には、Ansible リポジトリーへのマージ用に考慮される適切な形式のドキュメント文字列が必要になります。プラグインを継承する場合は、そのプラグインが取るオプションを、ドキュメントフラグメントから、またはコピーとして文書化しなければなりません。正しいドキュメントの詳細は「:ref:`module_documenting`」を参照してください。詳細なドキュメントは、ローカルで使用するプラグインを開発する場合でも推奨されます。

特定のプラグインタイプの開発
==================================

.. _developing_actions:

Action プラグイン
--------------

Action プラグインを使用すると、ローカル処理とローカルデータをモジュール機能に統合できます。

Action プラグインを作成するには、Base(ActionBase) クラスを親として新しいクラスを作成します。

.. code-block:: python

    from ansible.plugins.action import ActionBase

    class ActionModule(ActionBase):
        pass

そこから、``_execute_module`` メソッドを使用して元のモジュールを呼び出します。
モジュールの実行に成功すると、モジュールの戻り値データを変更できます。

.. code-block:: python

    module_return = self._execute_module(module_name='<NAME_OF_MODULE>',
                                         module_args=module_args,
                                         task_vars=task_vars, tmp=tmp)


たとえば、Ansible コントローラーとターゲットマシン間の時間差を確認する場合は、Action プラグインを作成してローカルタイムを確認し、それを Ansible の ``setup`` モジュールから返されるデータと比較できます。

.. code-block:: python

    #!/usr/bin/python
    # Make coding more python3-ish, this is required for contributions to Ansible
    from __future__ import (absolute_import, division, print_function)
    __metaclass__ = type

    from ansible.plugins.action import ActionBase
    from datetime import datetime


    class ActionModule(ActionBase):
        def run(self, tmp=None, task_vars=None):
            super(ActionModule, self).run(tmp, task_vars)
            module_args = self._task.args.copy()
            module_return = self._execute_module(module_name='setup',
                                                 module_args=module_args,
                                                 task_vars=task_vars, tmp=tmp)
            ret = dict()
            remote_date = None
            if not module_return.get('failed'):
                for key, value in module_return['ansible_facts'].items():
                    if key == 'ansible_date_time':
                        remote_date = value['iso8601']

            if remote_date:
                remote_date_obj = datetime.strptime(remote_date, '%Y-%m-%dT%H:%M:%SZ')
                time_delta = datetime.now() - remote_date_obj
                ret['delta_seconds'] = time_delta.seconds
                ret['delta_days'] = time_delta.days
                ret['delta_microseconds'] = time_delta.microseconds

            return dict(ansible_facts=dict(ret))
    

このコードはコントローラーの時間を確認し、``setup`` モジュールを使用してリモートマシンの日時を取得し、取得した時間とローカル時間の差異を算出し、
その時間差を日数、秒、マイクロ秒で返します。

Action プラグインの実用的な例
「`Ansible Core に含まれる Action プラグイン<https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/action>`_」のソースコードを参照してください。

.. _developing_cache_plugins:

Cache プラグイン
-------------

Cache プラグインは、Inventory プラグインによって取得されるファクトおよびデータを収集したデータを格納します。現在、ファクトキャッシュのみがコレクションの Cache プラグインでサポートされています。

cache_loader を使用して Cache プラグインをインポートし、``self.set_options()`` および ``self.get_option(<option_name>)`` を使用できるようにします。コードベースで Cache プラグインを直接インポートする場合は、``ansible.constants`` からのみアクセスでき、Inventory プラグインによって使用される Cache プラグインの機能が壊れます。

.. code-block:: python

    from ansible.plugins.loader import cache_loader
    [...]
    plugin = cache_loader.get('custom_cache', **cache_kwargs)

Cache プラグインには、2 つのベースクラス (データベースベースのバックアップ用のキャッシュの場合は ``BaseCacheModule``、ファイルのバックアップ用のキャッシュの場合は ``BaseCacheFileModule``) があります。

Cache プラグインを作成するには、最初に適切なベースクラスで新しい ``CacheModule`` クラスを作成します。``__init__`` メソッドを使用してプラグインを作成する場合は、指定した args および kwargs でベースクラスを初期化して、Inventory プラグインのキャッシュオプションと互換性を持たせるようにする必要があります。ベースクラスは ``self.set_options(direct=kwargs)`` を呼び出します。ベースクラスの ``__init__`` メソッドが呼ばれたあと、キャッシュオプションにアクセスするために ``self.get_option(<option_name>)`` を使用しなければなりません。

新しい Cache プラグインは、既存の Cache プラグインとの整合性を保つために、``_uri`` オプション、``_prefix`` オプション、および ``_timeout`` オプションを使用する必要があります。

.. code-block:: python

    from ansible.plugins.cache import BaseCacheModule

    class CacheModule(BaseCacheModule):
        def __init__(self, *args, **kwargs):
            super(CacheModule, self).__init__(*args, **kwargs)
            self._connection = self.get_option('_uri')
            self._prefix = self.get_option('_prefix')
            self._timeout = self.get_option('_timeout')

``BaseCacheModule`` を使用する場合は、メソッドの ``get``、``contains``、``keys``、``set``、``delete``、``flush``、および ``copy`` を実装する必要があります。``contains`` メソッドは、キーが存在し、期限切れではないことを示すブール値を返す必要があります。ファイルベースのキャッシュとは異なり、キャッシュの有効期限が切れている場合、``get`` メソッドは KeyError を発生させません。

``BaseFileCacheModule`` を使用する場合は、ベースクラスメソッド ``get`` および ``set`` から呼び出される ``_load`` メソッドおよび ``_dump`` メソッドを実装する必要があります。

Cache プラグインが JSON を格納している場合は、``_dump`` メソッドまたは ``set`` メソッドで ``AnsibleJSONEncoder`` を使用するか、``_load`` メソッドまたは ``get`` メソッドで ``AnsibleJSONDecoder`` を設定します。

たとえば、Cache プラグインは、「`Ansible Core に含まれる Cache プラグイン <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/cache>`_」のソースコードを参照してください。

.. _developing_callbacks:

Callback プラグイン
----------------

Callback プラグインは、イベントに応答する際に新しい動作を Ansible に追加します。デフォルトでは、Callback プラグインは、コマンドラインプログラムの実行時に表示されるほとんどの出力を制御します。

Callback プラグインを作成するには、Base(Callbacks) クラスを親として使用して新規クラスを作成します。

.. code-block:: python

  from ansible.plugins.callback import CallbackBase

  class CallbackModule(CallbackBase):
      pass

そこから、コールバックを提供する CallbackBase から特定のメソッドを上書きします。
Ansible バージョン 2.0 以降で使用するプラグインでは、``v2`` で始まる方法のみを上書きする必要があります。
上書き可能なメソッドの完全リストは、
`lib/ansible/plugins/callback <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/callback>`_ ディレクトリーの「``__init__.py``」を参照してください。

以下は、Ansible の Timer プラグインの実装方法の変更例です。
ただし、追加のオプションを使用すると、Ansible バージョン 2.4 以降で構成がどのように機能するかを確認できます。

.. code-block:: python

  # Make coding more python3-ish, this is required for contributions to Ansible
  from __future__ import (absolute_import, division, print_function)
  __metaclass__ = type

  # not only visible to ansible-doc, it also 'declares' the options the plugin requires and how to configure them.
  DOCUMENTATION = '''
    callback: timer
    callback_type: aggregate
    requirements:
      - whitelist in configuration
    short_description: Adds time to play stats
    version_added: "2.0"
    description:
        - This callback just adds total play duration to the play stats.
    options:
      format_string:
        description: format of the string shown to user at play end
        ini:
          - section: callback_timer
            key: format_string
        env:
          - name: ANSIBLE_CALLBACK_TIMER_FORMAT
        default: "Playbook run took %s days, %s hours, %s minutes, %s seconds"
  '''
  from datetime import datetime

  from ansible.plugins.callback import CallbackBase


  class CallbackModule(CallbackBase):
      """
      This callback module tells you how long your plays ran for.
      """
      CALLBACK_VERSION = 2.0
      CALLBACK_TYPE = 'aggregate'
      CALLBACK_NAME = 'namespace.collection_name.timer'

      # only needed if you ship it and don't want to enable by default
      CALLBACK_NEEDS_WHITELIST = True

      def __init__(self):

          # make sure the expected objects are present, calling the base's __init__
          super(CallbackModule, self).__init__()

          # start the timer when the plugin is loaded, the first play should start a few milliseconds after.
          self.start_time = datetime.now()

      def _days_hours_minutes_seconds(self, runtime):
          ''' internal helper method for this callback '''
          minutes = (runtime.seconds // 60) % 60
          r_seconds = runtime.seconds - (minutes * 60)
          return runtime.days, runtime.seconds // 3600, minutes, r_seconds

      # this is only event we care about for display, when the play shows its summary stats; the rest are ignored by the base class
      def v2_playbook_on_stats(self, stats):
          end_time = datetime.now()
          runtime = end_time - self.start_time

          # Shows the usage of a config option declared in the DOCUMENTATION variable. Ansible will have set it when it loads the plugin.
          # Also note the use of the display object to print to screen. This is available to all callbacks, and you should use this over printing yourself
          self._display.display(self._plugin_options['format_string'] % (self._days_hours_minutes_seconds(runtime)))
    
``CALLBACK_VERSION`` および ``CALLBACK_NAME`` の定義は、Ansible バージョン 2.0 以降のプラグインが正しく機能するために必要であることに注意してください。``CALLBACK_TYPE`` は、標準出力 (stdout) に書き込むプラグインを 1 つだけ読み込むことができるため、ほとんどの「stdout」プラグインをその他のものと区別するために必要です。

Callback プラグインの例は、`Ansible Core に含まれる Callback プラグイン <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/callback>`_ のソースコードを参照してください。

.. _developing_connection_plugins:

Connection プラグイン
------------------

Connection プラグインは、Ansible をターゲットホストに接続して、そのホストでタスクを実行できるようにします。Ansible には多くの Connection プラグインが含まれていますが、1 台のホストで一度に使用できるプラグインは 1 つのみです。最も一般的に使用される Connection プラグインは、``paramiko`` SSH、ネイティブ ssh (``ssh`` と呼ばれます)、および ``local`` の接続タイプです。 これらはすべて Playbook と ``/usr/bin/ansible`` で使用して、リモートマシンに接続できます。

Ansible バージョン 2.1 では、``smart`` 接続プラグインが導入されました。``スマート`` 接続タイプにより、Ansible はシステム機能に基づいて、Connection プラグインの ``paramiko`` または ``openssh`` を自動的に選択するか、OpenSSH が ControlPersist に対応している場合は ``ssh`` の Connetion プラグインを選択します。

新しい Connetion プラグイン (SNMP、メッセージバス、またはその他のトランスポートをサポートする場合など) を作成するには、既存の Connetion プラグインのいずれかの形式をコピーして、:ref:`ローカルプラグインパス <local_plugins>` にある ``connection`` ディレクトリーに置きます。

Connection プラグインの例は、「`Ansible Core に含まれる Connection プラグイン<https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/connection>`_」のソースコードを参照してください。

.. _developing_filter_plugins:

Filter プラグイン
--------------

Filter プラグインはデータを操作します。これらは Jinja2 の機能であり``template`` モジュールにより使用される Jinja2 テンプレートでも利用できます。すべてのプラグインと同様に簡単に拡張できますが、プラグインごとにファイルを作成する代わりに、ファイルごとに複数のプラグインを作成できます。Ansible に同梱される Filter プラグインのほとんどは ``core.py`` にあります。

Filter プラグインは、上記の標準設定およびドキュメントシステムを使用しません。

Filter プラグインの例は、「`Ansible Core に含まれる Filter プラグイン <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/filter>`_」のソースコードを参照してください。

.. _developing_inventory_plugins:

Inventory プラグイン
-----------------

Inventory プラグインはインベントリーソースを解析し、インベントリーのインメモリー表示を形成します。Inventory プラグインは Ansible バージョン 2.4 で追加されました。

Inventory プラグインの詳細は、「:ref:`developing_inventory`」ページを参照してください。

.. _developing_lookup_plugins:

Lookup プラグイン
--------------

Lookup プラグインは、外部データストアからデータをプルします。Lookup プラグインは Playbook 内でループするため (``with_fileglob`` や ``with_items`` などの Playbook 言語の構造は Lookup プラグインを介して実装されています)、また変数やパラメーターに値を返すために使用することができます。

Lookup プラグインは非常に柔軟性があるため、あらゆるタイプのデータを取得し、返すことができます。Lookup プラグインを記述する際には、Playbook で簡単に使用できる一貫性のあるタイプのデータを常に返します。返されたデータ型を変更するパラメーターは使用しないでください。単一の値を返さなければならないときもあれば、複雑なディクショナリーを返さなければない場合もあります。Lookup プラグインを 2 つ記述してください。

Ansible には、Lookup プラグインによって返されるデータを操作するのに使用できる「:ref:`filters <playbooks_filters>`」が多数含まれています。Lookup プラグイン内でフィルターを実行することが適切な場合もありますが、Playbook でフィルター処理できる結果を返す方が適切な場合もあります。Lookup プラグイン内で実行するフィルターの適切なレベルを決定する際に、データがどのように参照されるかに留意してください。

以下は簡単な Lookup プラグインの実装です。この Lookup は、テキストファイルの内容を変数として返します。

.. code-block:: python

  # python 3 headers, required if submitting to Ansible
  from __future__ import (absolute_import, division, print_function)
  __metaclass__ = type

  DOCUMENTATION = """
          lookup: file
          author: Daniel Hokka Zakrisson <daniel@hozac.com>
          version_added: "0.9"
          short_description: read file contents
          description:
              - This lookup returns the contents from a file on the Ansible controller's file system.
          options:
            _terms:
              description: path(s) of files to read
              required: True
          notes:
            - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
            - this lookup does not understand globing --- use the fileglob lookup instead.
  """
  from ansible.errors import AnsibleError, AnsibleParserError
  from ansible.plugins.lookup import LookupBase
  from ansible.utils.display import Display

  display = Display()


  class LookupModule(LookupBase):

      def run(self, terms, variables=None, **kwargs):


          # lookups in general are expected to both take a list as input and output a list
          # this is done so they work with the looping construct 'with_'.
          ret = []
          for term in terms:
              display.debug("File lookup term: %s" % term)

              # Find the file in the expected search path, using a class method
              # that implements the 'expected' search path for Ansible plugins.
              lookupfile = self.find_file_in_search_path(variables, 'files', term)

              # Don't use print or your own logging, the display class
              # takes care of it in a unified way.
              display.vvvv(u"File lookup using %s as file" % lookupfile)
              try:
                  if lookupfile:
                      contents, show_data = self._loader._get_file_contents(lookupfile)
                      ret.append(contents.rstrip())
                  else:
                      # Always use ansible error classes to throw 'final' exceptions,
                      # so the Ansible engine will know how to deal with them.
                      # The Parser error indicates invalid options passed
                      raise AnsibleParserError()
              except AnsibleParserError:
                  raise AnsibleError("could not locate file in lookup: %s" % term)

          return ret

以下は、このルックアップがどのように呼び出されるかの例になります。

  ---
  - hosts: all
    vars:
       contents: "{{ lookup('namespace.collection_name.file', '/etc/foo.txt') }}"

    tasks:

       - debug:
           msg: the value of foo.txt is {{ contents }} as seen today {{ lookup('pipe', 'date +"%Y-%m-%d"') }}

Lookup プラグインの例は、「`Ansible Core に含まれる Lookup プラグイン <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/lookup>`_」のソースコードを参照してください。

Lookup プラグインの使用方法の例は、「:ref:`Lookup の使用<playbooks_lookups>`」を参照してください。

.. _developing_test_plugins:

Test プラグイン
------------

Test プラグインはデータを検証します。これらは Jinja2 の機能であり``template`` モジュールにより使用される Jinja2 テンプレートでも利用できます。すべてのプラグインと同様に簡単に拡張できますが、プラグインごとにファイルを作成する代わりに、ファイルごとに複数のプラグインを作成できます。Ansible に同梱される Test プラグインのほとんどは ``core.py`` にあります。これらは、``map`` や ``select`` などの Filter プラグインと併用する場合に特に役立ちます。また、``when:`` のような条件ディレクティブでも利用できます。

Test プラグインは、上記の標準設定およびドキュメントシステムを使用しません。

たとえば、Test プラグインは、「`Ansible Core に含まれる Test プラグイン <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/test>`_」のソースコードを参照してください。

.. _developing_vars_plugins:

Vars プラグイン
------------

Vars プラグインは、インベントリーソース、Playbook、またはコマンドラインに組み込まれていない Ansible の実行に、変数データを追加します。Playbook は、Vars プラグインを使用して「host_vars」と「group_vars」の作業のように構築します。

Vars プラグインは Ansible 2.0 に部分的に実装され、Ansible 2.4 以降は、完全実装になるように書き直されました。Vars プラグインはコレクションによってサポートされません。

古いプラグインでは、``run`` メソッドを主要な本文/作業として使用していました。

.. code-block:: python

    def run(self, name, vault_password=None):
        pass # your code goes here


Ansible 2.0 は古いプラグインにパスワードを渡さなかったため、vault は利用できません。
ほとんどの作業は、必要に応じて VariableManager から呼び出される ``get_vars`` メソッドで実行されるようになりました。

.. code-block:: python

    def get_vars(self, loader, path, entities):
        pass # your code goes here

パラメーターは以下のとおりです。

 * loader: Ansible の DataLoader です。DataLoader は、ファイルの読み取り、JSON/YAML の自動読み込み、vault を使用したデータの復号化、および読み取りファイルのキャッシュを行うことができます。
 * path: これはすべてのインベントリーソースと現在のプレイの Playbook ディレクトリーの「ディレクトリーデータ」であるため、それを参照するデータを検索することができます。``get_vars`` は、利用可能なパスごとに最低 1 回呼び出されます。
 * entities: 必要な変数に関連付けられるホスト名またはグループ名です。プラグインはホストについて 1 回呼び出され、グループについて再度呼び出されます。

この ``get vars`` メソッドは変数を含むディクショナリー構造を返す必要があります。

Ansible バージョン 2.4 以降、変数プラグインはタスク実行を準備する際に、必要に応じて実行されます。これにより、古いバージョンの Ansible のインベントリー構築中に発生した「常に実行」動作が回避されます。

たとえば、変数プラグインは「`Ansible Core に含まれる Vars プラグイン
<https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/vars>`_」のソースコードを参照してください。

.. seealso::

   :ref:`all_modules`
       モジュール一覧
   :ref:`developing_api`
       タスク実行用の Python API について
   :ref:`developing_inventory`
       動的インベントリーソースの開発方法について
   :ref:`developing_modules_general`
       Ansible モジュールの作成方法について
   `メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発メーリングリスト
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC チャットチャンネル
