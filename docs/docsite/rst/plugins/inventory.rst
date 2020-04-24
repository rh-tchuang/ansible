.. \_inventory\_plugins:

inventory プラグイン
=================

.. contents::
   :local:
   :depth: 2

Inventory プラグインを使用すると、``-i /path/to/file`` や ``-i 'host1, host2'`` のコマンドラインパラメーターや、他の設定ソースを使用して、Ansible が使用するホストのインベントリーをコンパイルするためのデータソースを参照してタスクのターゲットを指定できます。


.. \_enabling\_inventory:

inventory プラグインの有効化
--------------------------

Ansible に同梱されるほとんどの inventory プラグインはデフォルトで無効にされており、
このプラグインを機能させるには、:ref:`ansible.cfg <ansible_configuration_settings>` ファイルでホワイトリスト化する必要があります。 Ansible に同梱される設定ファイルのデフォルトのホワイトリストは、
以下のようになります。

.. code-block:: ini

   \[inventory]
   enable\_plugins = host\_list, script, auto, yaml, ini, toml

上記のリストで、各プラグインがインベントリーソースの解析を試行する順番が確立されます。一覧に含まれていないプラグインは考慮されないので、実際に使用するものだけに最小限に抑えて、インベントリーの読み込みを「最適化」します。以下に例を示します。

.. code-block:: ini

   \[inventory]
   enable\_plugins = advanced\_host\_list, constructed, yaml

``auto`` inventory プラグインは、YAML 設定ファイルに使用する Inventory プラグインを自動的に決定します。auto は、コレクションの Inventory プラグインに使用することもできます。

コレクション内で特定の inventory プラグインをホワイトリスト化するには、完全修飾名を使用する必要があります。

.. code-block:: ini

   \[inventory]
   enable\_plugins = namespace.collection\_name.inventory\_plugin\_name


.. \_using\_inventory:

Inventory プラグインの使用
-----------------------

inventory プラグインを有効化して使用する時の唯一の要件は、解析するインベントリーソースを指定することです。
Ansible は、指定のインベントリーソースごとに、順番に有効化された Inventory プラグインの一覧を使用していきます。
Inventory プラグインがソースの解析に成功すると、残りのインベントリープラグインによるこのソースの解析は省略されます。

YAML 設定ソースで inventory プラグインの使用を開始するには、対応のファイル名スキーマで、対象のプラグインのファイルを作成して、(そのファイルに) ``plugin: plugin_name`` を追加します。プラグインごとに、命名に関する制約をすべて説明します。たとえば、aws\_ec2 inventory プラグインの文末は ``aws_ec2.(yml|yaml)`` に指定します。

.. code-block:: yaml

    # demo.aws_ec2.yml
plugin: aws_ec2

また、openstack プラグインの場合には、ファイルの名前を ``clouds.yml`` または ``openstack.(yml|yaml)`` に指定する必要があります。

.. code-block:: yaml

    # clouds.yml or openstack.(yml|yaml)
plugin: openstack

コレクションでプラグインを使用するには、完全修飾名を指定します。

.. code-block:: yaml

    plugin: namespace.collection_name.inventory_plugin_name

``auto`` inventory プラグインはデフォルトで有効になっており、``plugin`` フィールドを使用して、解析を試行するプラグインを指定する必要があります。`ansible.cfg` \['inventory'] ``enable_plugins`` リストで、ソースの解析に使用する inventory プラグインのホワイトリスト化/優先順位を設定できます。プラグインを有効にして必要なオプションを指定したら、``ansible-inventory -i demo.aws_ec2.yml --graph`` で生成したイベントリーを確認できます。

.. code-block:: text

    @all:
      |--@aws_ec2:
      |  |--ec2-12-345-678-901.compute-1.amazonaws.com
      |  |--ec2-98-765-432-10.compute-1.amazonaws.com
      |--@ungrouped:

Playbook に隣接するコレクションでインベントリーを使用して、``ansible-inventory`` で設定をテストするには、``--playbook-dir`` フラグを使用する必要があります。

(`ansible.cfg` \[defaults] セクションの ``inventory``、または :envvar:`ANSIBLE_INVENTORY` 環境変数を介して) インベントリーソースに対して、デフォルトのインベントリーパスを設定できます。``ansible-inventory --graph`` を実行すると、YAML 設定ソースを直接指定する時と同じ出力が生成されるようになっているはずです。同じ方法で使用するには、カスタムの inventory プラグインをプラグインパスに追加してください。

インベントリーソースは、インベントリー設定ファイルのディレクトリーである場合があります。構築した inventory プラグインは、インベントリーにすでに存在するホストでのみ動作するので、特定のタイミング (最後など) で構築したインベントリー設定を解析してください。Ansible は、ディレクトリーを再帰的にアルファベットで解析します。解析アプローチは設定できないので、想定通りに機能するように、ファイルの名前を指定します。構築した機能を直接し拡張したインベントリープラグインは、inventory プラグインのプションに構築したオプションを追加し、制約を回避して機能させることができます。それ以外の場合は、複数ソースに ``-i`` を使用して特定の順番を指定します (例: ``-i demo.aws_ec2.yml -i clouds.yml -i constructed.yml``)。

構築した ``keyed_groups`` オプションとホスト変数を使用して、動的なグループを作成できます。``groups`` オプションを使用して、グループを作成し、``compose`` でホスト変数を作成して変更できます。以下は、構築した機能を使用する aws\_ec2 のサンプルです。

.. code-block:: yaml

    # demo.aws_ec2.yml
plugin: aws_ec2
regions:
  - us-east-1
  - us-east-2
keyed_groups:
  # add hosts to tag_Name_value groups for each aws_ec2 host's tags.Name variable
  - key: tags.Name
    prefix: tag_Name_
    separator: ""
groups:
  # add hosts to the group development if any of the dictionary's keys or values is the word 'devel'
  development: "'devel' in (tags|list)"
compose:
  # set the ansible_host variable to connect with the private IP address without changing the hostname
  ansible_host: private_ip_address

``ansible-inventory -i demo.aws_ec2.yml --graph`` の出力は以下のようになります。

.. code-block:: text

    @all:
      |--@aws_ec2:
      |  |--ec2-12-345-678-901.compute-1.amazonaws.com
      |  |--ec2-98-765-432-10.compute-1.amazonaws.com
      |  |--...
      |--@development:
      |  |--ec2-12-345-678-901.compute-1.amazonaws.com
      |  |--ec2-98-765-432-10.compute-1.amazonaws.com
      |--@tag_Name_ECS_Instance:
      |  |--ec2-98-765-432-10.compute-1.amazonaws.com
      |--@tag_Name_Test_Server:
      |  |--ec2-12-345-678-901.compute-1.amazonaws.com
      |--@ungrouped

上記の設定でホストに変数がない場合には (``tags.Name``, ``tags``、``private_ip_address``)、ホストは inventory プラグインが作成したグループ以外には追加されず、また ``ansible_host`` のホスト変数も変更されません。

inventory プラグインがキャッシュをサポートする場合には、環境変数や Ansible 設定ファイルを使用して、個別の YAML 設定ソースまたは複数のインベントリーソースにキャッシュオプションを有効化して設定できます。インベントリー固有のキャッシュオプションを指定せずに inventory プラグインのキャッシュを有効にする場合は、inventory プラグインはファクトキャッシュオプションを使用します。以下は、個別の YAML 設定ファイルのキャッシュ化を有効にする例です。

.. code-block:: yaml

    # demo.aws_ec2.yml
plugin: aws_ec2
cache: yes
cache_plugin: jsonfile
cache_timeout: 7200
cache_connection: /tmp/aws_inventory
cache_prefix: aws_ec2

以下は、``ansible.cfg`` ファイルに、使用する chache プラグインにデフォルト設定されているファクトキャッシュの一部を使用してインベントリーキャッシュと、タイムアウトを設定する例です。

.. code-block:: ini

   \[defaults]
   fact\_caching = jsonfile
   fact\_caching\_connection = /tmp/ansible\_facts
   cache\_timeout = 3600

   \[inventory]
   cache = yes
   cache\_connection = /tmp/ansible\_inventory

Ansible に同梱されている cache プラグインのほかに、インベントリーをキャッシュ可能な cache プラグインもカスタムの cache プラグインパスに配置できます。コレクションで、インベントリー用に cache プラグインを使用することはサポートされていません。

.. \_inventory\_plugin\_list:

プラグイン一覧
-----------

``ansible-doc -t inventory -l`` を使用して、利用可能なプラグインの一覧を確認できます。
プラグイン固有のドキュメントや例を参照するには、``ansible-doc -t inventory <plugin name>`` を使用します。

.. toctree:: :maxdepth: 1
    :glob:

    inventory/*

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`callback_plugins`
       Ansible callback プラグイン
   :ref:`connection_plugins`
       Ansible connection プラグイン
   :ref:`playbooks_filters`
       Jinja2 filter プラグイン
   :ref:`playbooks_tests`
       Jinja2 test プラグイン
   :ref:`playbooks_lookups`
       Jinja2 lookup プラグイン
   :ref:`vars_plugins`
       Ansible vars プラグイン
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       \#ansible IRC chat channel
