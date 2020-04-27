.. _vars_plugins:

vars プラグイン
============

.. contents::
   :local:
   :depth: 2

Vars プラグインは、インベントリーソース、Playbook、またはコマンドラインに組み込まれていない Ansible 実行に、追加で変数データを挿入します。Playbook は、Vars プラグインを使用して 'host_vars' と 'group_vars' の作業のように構築します。

vars プラグインは Ansible 2.0 に部分的に実装され、Ansible 2.4 以降は、完全実装になるように書き直されました。

Ansible に同梱される :ref:`host_group_vars <host_group_vars_vars>` プラグインは、:ref:`host_variables` および :ref:`group_variables` から変数を読み込むことができます。


.. _enable_vars:

vars プラグインの有効化
---------------------

カスタムの Vars プラグインを有効にするには、カスタムのプラグインを、ロール内の Play の隣りにある ``vars_plugins`` ディレクトリーに配置するか、:ref:`ansible.cfg <ansible_configuration_settings>` で設定したディレクトリーソースの 1 つに配置します。


.. _using_vars:

vars プラグインの使用
------------------

Vars プラグインは、有効になると自動的に使用されます。


.. _vars_plugin_list:

プラグイン一覧
------------

``ansible-doc -t vars -l`` を使用して、利用可能なプラグインの一覧を表示できます。
特定のプラグインのドキュメントや例を参照するには、``ansible-doc -t vars <plugin name>`` を使用します。


.. toctree:: :maxdepth: 1
    :glob:

    vars/*

.. seealso::

   :ref:`action_plugins`
       Ansible Action プラグイン
   :ref:`cache_plugins`
       Ansible Cache プラグイン
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
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
