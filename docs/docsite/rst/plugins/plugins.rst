.. _plugins_lookup:

********************
プラグインの使用
********************

プラグインは、Ansible のコア機能を拡張するコードの一部です。Ansible は、プラグインアーキテクチャーを使用して、柔軟で拡張可能な機能セットを数多く活用できるようになります。

Ansible には、便利なプラグインが多数同梱されていますし、簡単に独自のプラグインを記述することもできます。

本セクションでは、Ansible に含まれるさまざまなプラグインについて説明します。

.. toctree::
   :maxdepth: 1

   action
   become
   cache
   callback
   cliconf
   connection
   httpapi
   inventory
   lookup
   netconf
   shell
   strategy
   vars
   ../user_guide/playbooks_filters
   ../user_guide/playbooks_tests
   ../user_guide/plugin_filtering_config

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`ansible_configuration_settings`
       Ansible 設定ドキュメントおよび設定
   :ref:`command_line_tools`
       Ansible ツール、説明、およびオプション
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
