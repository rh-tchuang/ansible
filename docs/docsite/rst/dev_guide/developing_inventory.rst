.. _developing_inventory:

****************************
動的インベントリーの開発
****************************

.. contents:: トピック
   :local:

「:ref:`dynamic_inventory`」で説明されているように、Ansible は、
付属の「:ref:`Inventory プラグイン <inventory_plugins>`」を使用して、クラウドソースを含む動的ソースからインベントリー情報を引き出すことができます。
現在、必要なソースが既存のプラグインで対応していない場合は、他のプラグインの種類と同様、自身で作成できます。

以前のバージョンでは、適切な引数で呼び出す際に、JSON を正しい形式で出力できるスクリプトまたはプログラムを作成する必要があります。
:ref:`スクリプトインベントリープラグイン <script_inventory>` により後方互換性を確保しており、使用するプログラミング言語に制限はないため、
インベントリースクリプトを使用して作成できます。
スクリプトを作成する場合は、いくつかの機能を実装する必要があります。
つまり、キャッシュ、設定管理、動的変数、グループ構成などです。
「:ref:`インベントリープラグイン <inventory_plugins>`」では、Ansible コードベースを活用して、これらの一般的な機能を追加できます。


.. _inventory_sources:

インベントリーソース
=================

インベントリーソースは文字列 (コマンドラインで ``-i`` に渡すもの) です。
これらはファイル/スクリプトへのパスを表すか、またはプラグインが使用する生データになります。
プラグインとそれらが使用するソースのタイプを以下に示します。

+--------------------------------------------+---------------------------------------+
|  Plugin                                    | Source                                |
+--------------------------------------------+---------------------------------------+
| :ref:`host list <host_list_inventory>`     | ホストのコンマ区切りリスト       |
+--------------------------------------------+---------------------------------------+
| :ref:`yaml <yaml_inventory>`               | YAML 形式のデータファイルへのパス       |
+--------------------------------------------+---------------------------------------+
| :ref:`constructed <constructed_inventory>` | YAML設定ファイルへのパス     |
+--------------------------------------------+---------------------------------------+
| :ref:`ini <ini_inventory>`                 | INI 形式のデータファイルへのパス    |
+--------------------------------------------+---------------------------------------+
| :ref:`virtualbox <virtualbox_inventory>`   | YAML 設定ファイルへのパス     |
+--------------------------------------------+---------------------------------------+
| :ref:`script plugin <script_inventory>`    |  JSON を出力する実行ファイルへのパス |
+--------------------------------------------+---------------------------------------+


.. _developing_inventory_inventory_plugins:

Inventory プラグイン
=================

ほとんどのプラグインタイプ (モジュールを除く) と同様に、それらは Python で開発されなければなりません。コントローラー上で実行するため、「:ref:`control_node_requirements`」と同じ要件に一致させなければなりません。

:ref:`developing_plugins` に関するドキュメントの多くはここでも適用されています。したがって、反復しないように、本ガイドを先に読み、次に Inventory プラグインの詳細を参照してください。

通常、Inventory プラグインは、Playbook/プレイ、およびロールが読み込まれる前に、実行の開始時にのみ実行されます。
ただし、``meta: refresh_inventory`` タスク経由で「再実行」することができます。これにより、既存のインベントリーを削除し、再ビルドします。

「永続」キャッシュを使用する場合、Inventory プラグインは設定済みのキャッシュプラグインを使用してデータを保存および取得し、コストのかかる外部呼び出しを回避することもできます。

.. _developing_an_inventory_plugin:

Inventory プラグインの開発
------------------------------

最初に行うのは、ベースクラスを使用することです。

.. code-block:: python

    from ansible.plugins.inventory import BaseInventoryPlugin

    class InventoryModule(BaseInventoryPlugin):

        NAME = 'myplugin'  # used internally by Ansible, it should match the file name but not required

Inventory プラグインがコレクションにある場合、NAME は「namespace.collection_name.myplugin」形式である必要があります。

このクラスは、各プラグインが実装する必要のあるいくつかのメソッドと、インベントリーソースを解析してインベントリーを更新するためのヘルパーがいくつかあります。

基本的なプラグインが動作するようになったら、より多くの基本クラスを追加することで他の機能を組み込むことができます。

.. code-block:: python

    from ansible.plugins.inventory import BaseInventoryPlugin, Constructable, Cacheable

    class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

        NAME = 'myplugin'

プラグインでの作業の大部分では、主に 2 つのメソッド ``verify_file`` と ``parse`` を扱います。

.. _inventory_plugin_verify_file:

verify_file
^^^^^^^^^^^

このメソッドは、Inventory ソースがプラグインで使用可能かどうかをすばやく判断するために、Ansible によって使用されます。プラグインが処理できるものに重複がある可能性があり、Ansible はデフォルトで有効なプラグインを (順番に) 試行するため、100％ 正確である必要はありません。

.. code-block:: python

    def verify_file(self, path):
        ''' return true/false if this is possibly a valid file for this plugin to consume '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            # base class verifies that file exists and is readable by current user
            if path.endswith(('virtualbox.yaml', 'virtualbox.yml', 'vbox.yaml', 'vbox.yml')):
                valid = True
        return valid

この場合、:ref:`virtualbox Inventory プラグイン <virtualbox_inventory>` から有効な yaml ファイルを使用しないように、特定のファイル名のパターンを選定します。ここには任意のタイプの条件を追加できますが、最も一般的な条件は「拡張子一致」です。YAML 設定ファイルの拡張子マッチングを実装している場合は、パスの接尾辞 <plugin_name>.<yml|yaml> を使用する必要があります。有効な拡張機能はすべて、プラグインの説明で文書化されている必要があります。

別の例では、実際には「file」を使わず、
:ref:`ホストリスト <host_list_inventory>` プラグインの、インベントリのソース文字列そのものを使用します。

.. code-block:: python

    def verify_file(self, path):
        ''' don't call base class as we don't expect a path, but a host list '''
        host_list = path
        valid = False
        b_path = to_bytes(host_list, errors='surrogate_or_strict')
        if not os.path.exists(b_path) and ',' in host_list:
            # the path does NOT exist and there is a comma to indicate this is a 'host list'
            valid = True
        return valid

この方法は、Inventory プロセスを迅速化し、解析エラーの原因になる前に簡単に除外できるソースの不要な解析を回避するためのものです。

.. _inventory_plugin_parse:

parse
^^^^^

この方法は、プラグインの作業の大部分を行います。

このメソッドは、以下のパラメーターを取ります。

 * inventory: 既存のデータと、ホスト/グループ/変数をインベントリーに追加するメソッドがある Inventory オブジェクト。
 * loader: Ansible の DataLoader です。DataLoader は、ファイルの読み取り、JSON/YAML の自動読み込み、vault を使用したデータの復号化、および読み取りファイルのキャッシュを行うことができます。
 * path: インベントリーソースを持つ文字列 (通常、これはパスですが、必須ではありません)。
 * cache: プラグインがキャッシュを使用するかどうかを示します (キャッシュプラグインまたはローダー、もしくはその両方)。


ベースクラスは他のメソッドで再利用するための割り当てを最小限に抑えます。

.. code-block:: python

       def parse(self, inventory, loader, path, cache=True):

        self.loader = loader
        self.inventory = inventory
        self.templar = Templar(loader=loader)

プラグインは提供されるインベントリーソースに対応し、これを Ansible インベントリーに変換します。
これを容易にするため、以下の例ではいくつかのヘルパー関数を使用します。

.. code-block:: python

       NAME = 'myplugin'

       def parse(self, inventory, loader, path, cache=True):

            # call base method to ensure properties are available for use with other helper methods
            super(InventoryModule, self).parse(inventory, loader, path, cache)

            # this method will parse 'common format' inventory sources and
            # update any options declared in DOCUMENTATION as needed
            config = self._read_config_data(path)

            # if NOT using _read_config_data you should call set_options directly,
            # to process any defined configuration for this plugin,
            # if you don't define any options you can skip
            #self.set_options()

            # example consuming options from inventory source
            mysession = apilib.session(user=self.get_option('api_user'),
                                       password=self.get_option('api_pass'),
                                       server=self.get_option('api_server')
            )


            # make requests to get data to feed into inventory
            mydata = mysession.getitall()

            #parse data and create inventory objects:
            for colo in mydata:
                for server in mydata[colo]['servers']:
                    self.inventory.add_host(server['name'])
                    self.inventory.set_variable(server['name'], 'ansible_host', server['external_ip'])
    
具体的な内容は、返される API や構造体によって異なります。ただし、注意すべき点の 1 つは、インベントリーソースやその他の問題が発生した場合は ``raise AnsibleParserError を発生`` させて、ソースが無効であったことやプロセスが失敗したことを Ansible に知らせる必要があるということです。

インベントリープラグインの実装方法の例は、
ソースコード `lib/ansible/plugins/inventory` <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/inventory>_ を参照してください。

.. _inventory_plugin_caching:

インベントリーキャッシュ
^^^^^^^^^^^^^^^

インベントリープラグインのドキュメントを inventory_cache ドキュメントフラグメントで拡張し、Cacheable ベースクラスを使用して、キャッシュシステムを自由に使用できます。

.. code-block:: yaml

    extends_documentation_fragment:
      - inventory_cache

.. code-block:: python

    class InventoryModule(BaseInventoryPlugin, Constructable, Cacheable):

        NAME = 'myplugin'

次に、ユーザーが指定したキャッシュプラグインを読み込み、キャッシュからの読み込みと更新を行います。Inventory プラグインが YAML ベースの設定ファイルおよび ``_read_config_data`` メソッドを使用している場合は、キャッシュプラグインがそのメソッドに読み込まれます。インベントリープラグインが ``_read_config_data`` を使用しない場合は、``load_cache_plugin`` でキャッシュを明示的に読み込む必要があります。

.. code-block:: python

    NAME = 'myplugin'

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self.load_cache_plugin()

キャッシュを使用する前に、``get_cache_key`` メソッドを使用して一意のキャッシュキーを取得します。これはキャッシュを使用するすべてのインベントリーモジュールによって実行される必要があるため、キャッシュの他の部分を使用したり上書きしたりしないでください。

.. code-block:: python

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self.load_cache_plugin()
        cache_key = self.get_cache_key(path)

キャッシュを有効にし、正しいプラグインを読み込み、ユニークなキャッシュキーを取得したため、キャッシュとインベントリーとの間のデータの流れを、``parse`` メソッドの ``cache`` パラメーターを使用して設定できます。この値はインベントリーマネージャーから取得され、インベントリーを更新するかどうかを示します (``--flush-cache`` またはメタタスク ``refresh_inventory`` など)。キャッシュの更新時にインベントリーを設定するために使用される訳ではありませんが、ユーザーがキャッシュを有効にしている場合は、キャッシュを新しいインベントリーで更新する必要があります。``self._cache`` はディクショナリーのように使用できます。以下のパターンでは、インベントリーの更新がキャッシュと連動して動作するようになっています。

.. code-block:: python

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path)

        self.load_cache_plugin()
        cache_key = self.get_cache_key(path)

        # cache may be True or False at this point to indicate if the inventory is being refreshed
        # get the user's cache option too to see if we should save the cache if it is changing
        user_cache_setting = self.get_option('cache')

        # read if the user has caching enabled and the cache isn't being refreshed
        attempt_to_read_cache = user_cache_setting and cache
        # update if the user has caching enabled and the cache is being refreshed; update this value to True if the cache has expired below
        cache_needs_update = user_cache_setting and not cache

        # attempt to read the cache if inventory isn't being refreshed and the user has caching enabled
        if attempt_to_read_cache:
            try:
                results = self._cache[cache_key]
            except KeyError:
                # This occurs if the cache_key is not in the cache or if the cache_key expired, so the cache needs to be updated
                cache_needs_update = True

        if cache_needs_updates:
            results = self.get_inventory()

            # set the cache
            self._cache[cache_key] = results

        self.populate(results)
    
``parse`` メソッドが完了すると、``self._cache`` の内容は、キャッシュの内容が変更された場合にキャッシュプラグインを設定するために使用されます。

利用できるキャッシュメソッドは 3 つあります。
  - ``set_cache_plugin`` は、``parse`` メソッドの完了前にキャッシュプラグインを ``self._cache`` の内容で強制的に設定します。
  - ``update_cache_if_changed`` は、``parse`` メソッドが完了する前に ``self._cache`` が変更された場合のみキャッシュプラグインを設定します。
  - ``clear_cache`` は、キャッシュプラグインから ``self._cache`` のキーを削除します。

.. _inventory_source_common_format:

インベントリーソース共通形式
------------------------------

開発を簡単にするために、ほとんどのプラグインにはインベントリーのソースとして標準的な設定ファイルを使用し、YAML ベースで、ファイルを使用するプラグインの名前を含む 1 つの必須フィールド ``plugin`` があります。
使用されるその他の一般的な機能に応じて、他のフィールドが必要になるかもしれませんが、各プラグインは必要に応じて独自のカスタムオプションを追加することもできます。
たとえば、統合されたキャッシュを使用している場合は、``cache_plugin``、``cache_timeout`` やその他のキャッシュ関連のフィールドが必要になるかもしれません。

.. _inventory_development_auto:

「auto」プラグイン
-----------------

Ansible 2.5 以降、デフォルトで有効になっている :ref:`自動インベントリープラグイン <auto_inventory>` が含まれます。これは、インベントリープラグイン名と一致する ``plugin`` フィールドを指定する共通の YAML 設定形式を使用する場合のみ、他のプラグインを読み込みます。これにより、設定を更新する必要がないプラグインを簡単に使用できます。


.. _inventory_scripts:
.. _developing_inventory_scripts:

インベントリースクリプト
=================

インベントリープラグインはそのままですが、後方互換性だけでなく、ユーザーが他のプログラミング言語を使用できるように、引き続きインベントリースクリプトをサポートします。


.. _inventory_script_conventions:

インベントリースクリプトの規則
----------------------------

インベントリースクリプトでは ``--list`` および ``--host <hostname>`` の引数が使用できるようにする必要があります。他の引数も受け取りますが、Ansible はこれらを使用しません。
これらの引数は、スクリプトを直接実行する際に便利な場合があります。

単一の引数 ``--list`` を指定してスクリプトを呼び出した場合、
スクリプトは、管理対象のすべてのグループを含む JSON エンコードされたハッシュまたはディクショナリーを標準出力に出力する必要があります。
各グループの値は、各ホスト、子グループ、可能なグループ変数、
または単にホストのリストを含むハッシュまたはディクショナリーにする必要があります。


    {
        "group001": {
            "hosts": ["host001", "host002"],
            "vars": {
                "var1": true
            },
            "children": ["group002"]
        },
        "group002": {
            "hosts": ["host003","host004"],
            "vars": {
                "var2": 500
            },
            "children":[]
        }

    }

グループのいずれかの要素が空の場合は、出力から省略される可能性があります。

引数 ``--host <hostname>`` (<hostname> は上述のホストです) で呼び出されると、スクリプトは空の JSON ハッシュ/ディクショナリーか、テンプレートや Playbook で利用できるようにするための変数のハッシュ/ディクショナリーを出力しなければなりません。例::


    {
        "VAR001": "VALUE",
        "VAR002": "VALUE",
    }

変数の出力は任意です。スクリプトがこれを実行しない場合は、空のハッシュまたはディクショナリーを出力する必要があります。

.. _inventory_script_tuning:

外部インベントリースクリプトのチューニング
------------------------------------

バージョン 1.3 における新機能

上述したストックインベントリースクリプトシステムは Ansible のすべてのバージョンで動作しますが、
すべてのホストに対して ``--host`` を呼び出すことは、特にリモートサブシステムへの API 呼び出しを伴う場合には、
かなり非効率的になる可能性があります。

この非効率さを回避するために、インベントリースクリプトが「_meta」と呼ばれるトップレベルの要素を返す場合に、
1 回のスクリプト実行ですべてのホスト変数を返すことができます。
このメタ要素に「hostvars」の値が含まれる場合、
インベントリースクリプトは各ホストに対して ``--host`` で呼び出されません。
これにより、大量のホストに対してパフォーマンスが大幅に向上します。

トップレベルの JSON ディクショナリーに追加するデータは次のようになります。

    {

        # results of inventory script as above go here
        # ...

        "_meta": {
            "hostvars": {
                "host001": {
                    "var001" : "value"
                },
                "host002": {
                    "var002": "value"
                }
            }
        }
    }

Ansible が ``--host`` でインベントリーを呼び出すのを防ぐために ``_meta`` を使用する要件を満たすには、少なくとも空の ``hostvars`` ディクショナリーで ``_meta`` を埋めなければなりません。
例::

    {

        # results of inventory script as above go here
        # ...

        "_meta": {
            "hostvars": {}
        }
    }


.. _replacing_inventory_ini_with_dynamic_provider:

既存の静的インベントリーファイルをインベントリースクリプトで置き換える場合は、
インベントリー内のすべてのホストをメンバーとして、
インベントリー内のすべてのグループを子として含む「all」グループを含む JSON オブジェクトを返さなければなりません。
また、他のグループのメンバーではないすべてのホストを含む「ungrouped」グループも含まなければなりません。
この JSON オブジェクトのスケルトンの例は以下のとおりです。

.. code-block:: json

   {
       "_meta": {
         "hostvars": {}
       },
       "all": {
         "children": [
           "ungrouped"
         ]
       },
       "ungrouped": {
         "children": [
         ]
       }
   }

これがどのように見えるかを確認する簡単な方法は、:ref:`ansible-inventory` を使用することです。これにより、インベントリースクリプトのように ``--list`` パラメーターおよび ``--host`` パラメーターがサポートされます。

.. seealso::

   :ref:`developing_api`
       Playbook およびアドホックタスク実行のための Python API
   :ref:`developing_modules_general`
       モジュールの開発を始める
   :ref:`developing_plugins`
       プラグインの開発方法
   `Ansible Tower <https://www.ansible.com/products/tower>`_
       Ansible の REST API エンドポイントおよび GUI (動的インベントリーと同期)
   `開発メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発トピックのメーリングリスト
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
