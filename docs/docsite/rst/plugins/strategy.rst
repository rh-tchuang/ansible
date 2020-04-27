.. _strategy_plugins:

Strategy プラグイン
================

.. contents::
   :local:
   :depth: 2

Strategy プラグインは、タスクおよびホストスケジューリングを処理し、Play 実行のフローを制御します。

.. _enable_strategy:

Strategy プラグインの有効化
-------------------------

Ansible に同梱される Strategy プラグインはすべて、デフォルトで有効となっています。カスタムストラテジープラグインは、
:ref:`ansible.cfg <ansible_configuration_settings>` で設定した lookup ディレクトリーソースのいずれかにこれを配置することで有効にできます。

.. _using_strategy:

Strategy プラグインの使用
----------------------

1 つの Play で使用できる Strategy プラグインは 1 つだけですが、Playbook の Play または Ansible の実行ごとに異なる Strategy プラグインを使用できます。
デフォルトは、:ref:`linear <linear_strategy>` プラグインです。Ansible :ref:`設定<ansible_configuration_settings>` でこのデフォルトを変更するには、環境変数を使用します。

.. code-block:: shell

    export ANSIBLE_STRATEGY=free

または、`ansible.cfg` ファイルで以下を設定します。

.. code-block:: ini

    [defaults]
    strategy=linear

Play で :ref:`strategy keyword <playbook_keywords>` を使用して、Play の Strategy プラグインを指定できます。

  - hosts: all
    strategy: debug
    tasks:
      - copy: src=myhosts dest=/etc/hosts
        notify: restart_tomcat

      - package: name=tomcat state=present

    handlers:
      - name: restart_tomcat
        service: name=tomcat state=restarted

.. _strategy_plugin_list:

プラグイン一覧
-----------

``ansible-doc -t strategy -l`` を使用して、利用可能なプラグインの一覧を確認できます。
プラグイン固有のドキュメントや例を参照するには、``ansible-doc -t strategy <plugin name>`` を使用します。


.. toctree:: :maxdepth: 1
    :glob:

    strategy/*

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`inventory_plugins`
       Ansible inventory プラグインの使用
   :ref:`callback_plugins`
       Ansible callback プラグイン
   :ref:`playbooks_filters`
       Jinja2 filter プラグイン
   :ref:`playbooks_tests`
       Jinja2 test プラグイン
   :ref:`playbooks_lookups`
       Jinja2 lookup プラグイン
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
