.. _action_plugins:

Action プラグイン
==============

.. contents::
   :local:
   :depth: 2

Action プラグインは、:ref:`modules <working_with_modules>` と連携して、Playbook のタスクに必要なアクションを実行します。
通常、Action プラグインは、モジュールの実行前にバックグラウンドで自動的に実行されて、前提条件となっている作業を行います。

action プラグインが指定されていないモジュールには、「一般的な」action プラグインが使用されます。

.. _enabling_action:

action プラグインの有効化
-----------------------

カスタムの action プラグインを有効にするには、カスタムのプラグインを、ロール内の Play の隣りにある ``action_plugins`` ディレクトリーに配置するか、:ref:`ansible.cfg <ansible_configuration_settings>` に設定した action プラグインのディレクトリーソースの 1 つに配置します。

.. _using_action:

action プラグインの使用
--------------------

Action プラグインは、関連のモジュールを使用する場合には、デフォルトで実行され、特に作業は必要ありません。

プラグイン一覧
-----------

action プラグインを直接一覧表示できませんが、対応のモジュールとして表示されます。

``ansible-doc -l`` を使用して、利用可能なプラグインの一覧を表示できます。
特定のドキュメント例を参照するには、``ansible-doc <name>`` を使用してください。モジュールに対応の action プラグインがある場合は、この点に注意してください。

.. seealso::

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
   :ref:`vars_plugins`
       Ansible Vars プラグイン
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
