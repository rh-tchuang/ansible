.. _cache_plugins:

Cache プラグイン
=============

.. contents::
   :local:
   :depth: 2

chache プラグインによりバックエンドキャッシングメカニズムが実装され、Ansible は収集したファクトまたはインベントリーソースデータを保存できます。
ソースからの取得でパフォーマンスが低下することはありません。

デフォルトの cache プラグインは :ref:`メモリー<memory_cache>` プラグインで、Ansible が現在実行するデータのみをキャッシュします。永続ストレージのあるプラグインは他にもあり、実行時にデータをキャッシュできるようにします。

インベントリーおよびファクトに個別のキャッシュプラグインを使用できます。インベントリー固有のキャッシュプラグインが提供されておらず、インベントリーキャッシュが有効になっている場合は、ファクトキャッシュプラグインがインベントリーに使用されます。

.. _enabling_cache:

ファクトの cache プラグインの有効化
---------------------------

一度に有効にできるファクトの cache プラグインは 1 つだけです。

Ansible 設定でキャッシュプラグインを有効にするには、環境変数を使用するか、

.. code-block:: shell

    export ANSIBLE_CACHE_PLUGIN=jsonfile

または、``ansible.cfg`` ファイルで以下を設定します。

.. code-block:: ini

    [defaults]
    fact_caching=redis

Cache プラグインをコレクションで使用する場合には、完全修飾名を使用してください。

.. code-block:: ini

    [defaults]
    fact_caching = namespace.collection_name.cache_plugin_name

また、各プラグインに固有の他のオプションを設定する必要があります。詳細は、各プラグインのドキュメント、
または Ansible :ref:`の設定 <ansible_configuration_settings>` を参照してください。

カスタムの cache プラグインを有効にするには、ロール内の Play の隣りにある ``cache_plugins`` ディレクトリーに保存するか、:ref:`ansible.cfg <ansible_configuration_settings>` で設定したディレクトリーソースの 1 つに保存します。


インベントリーの cache プラグインの有効化
--------------------------------

インベントリーは、ファイルベースの cache プラグイン (jsonfile など) を使用してキャッシュできます。特定のインベントリープラグインをチェックして、キャッシュに対応しているかどうかを確認します。コレクション内の cache プラグインは cache インベントリーではサポートされません。
インベントリー固有の cache プラグインが指定されていない場合、Ansible はファクト cache プラグインオプションがある cache インベントリーにフォールバックします。

インベントリーキャッシュは、デフォルトで無効になっています。環境変数でこれを有効にできます。

.. code-block:: shell

    export ANSIBLE_INVENTORY_CACHE=True

または、``ansible.cfg`` ファイルで以下を設定します。

.. code-block:: ini

    [inventory]
    cache=True

または、inventory プラグインが YAML 設定ソースに対応している場合には、設定ファイルで以下を指定します。

.. code-block:: yaml

    # dev.aws_ec2.yaml
    plugin: aws_ec2
    cache: True

ファクトキャッシュプラグインと同様に、一度に 1 つのインベントリーの cache プラグインのみをアクティブにでき、環境変数で設定できます。

.. code-block:: shell

    export ANSIBLE_INVENTORY_CACHE_PLUGIN=jsonfile

または、ansible.cfg ファイルで以下を設定します。

.. code-block:: ini

    [inventory]
    cache_plugin=jsonfile

または、inventory プラグインが YAML 設定ソースに対応している場合には、設定ファイルで以下を指定します。

.. code-block:: yaml

    # dev.aws_ec2.yaml
    plugin: aws_ec2
    cache_plugin: jsonfile

詳細は、各 inventory プラグインのドキュメント、または Ansible :ref:`設定<ansible_configuration_settings>` を参照してください。

.. _using_cache:

Cache プラグインの使用
-------------------

Cache プラグインは、有効になると自動的に使用されます。


.. _cache_plugin_list:

プラグイン一覧
-----------

``ansible-doc -t cache -l`` を使用して、利用可能なプラグインの一覧を表示できます。
特定のドキュメントと例を参照する場合は、``ansible-doc -t cache <plugin name>`` を使用してください。

.. toctree:: :maxdepth: 1
    :glob:

    cache/*

.. seealso::

   :ref:`action_plugins`
       Ansible Action プラグイン
   :ref:`callback_plugins`
       Ansible callback プラグイン
   :ref:`connection_plugins`
       Ansible connection プラグイン
   :ref:`inventory_plugins`
       Ansible inventory プラグインの使用
   :ref:`shell_plugins`
       Ansible Shell プラグイン
   :ref:`strategy_plugins`
       Ansible Strategy プラグイン
   :ref:`vars_plugins`
       Ansible Vars プラグイン
   `ユーザーのメーリングリスト <https://groups.google.com/forum/#!forum/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `webchat.freenode.net <https://webchat.freenode.net>`_
       #ansible IRC chat channel
