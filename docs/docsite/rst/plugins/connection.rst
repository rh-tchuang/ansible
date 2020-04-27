.. _connection_plugins:

Connection プラグイン
==================

.. contents::
   :local:
   :depth: 2

Connection プラグインは、Ansibleがターゲットホストに接続して、そのホストでタスクを実行できるようにします。Ansible には多くの connection プラグインが含まれていますが、1 台のホストで一度に使用できるプラグインは 1 つのみです。

デフォルトでは、Ansible には複数のプラグインが含まれます。最もよく使用されるのは、:ref:`paramiko SSH<paramiko_ssh_connection>`、ネイティブ (:ref:`ssh<ssh_connection>` と呼ばれる) および :ref:`ローカル<local_connection>` 接続タイプです。 上記はすべて、Playbook や :command:`/usr/bin/ansible` で使用して、リモートマシンと対話する方法を決定できます。

このような接続タイプの基本情報は、:ref:`getting started<intro_getting_started>` のセクションで説明しています。

.. _ssh_plugins:

``ssh`` プラグイン
---------------

ssh は、システム管理でデフォルトで使用されるプロトコルであり、Ansible で最も使用されるプロトコルでもあるため、コマンドラインツールに ssh オプションが含まれています。詳細は :ref:`ansible-playbook` を参照してください。

.. _enabling_connection:

Connection プラグインの追加
-------------------------

カスタムのプラグインを ``connection_plugins`` ディレクトリーに配置して、
Ansible を拡張して他のトランスポート (SNMP またはメッセージバス) をサポートできます。

.. _using_connection:

Connection プラグインの使用
------------------------

接続プラグインは、Play で :ref:`設定<ansible_configuration_settings>`、コマンドライン (``-c``、``--connection``) を :ref:`キーワード<playbook_keywords>` として設定できます。または、インベントリーで最もよく使われる :ref:`変数<behavioral_parameters>` をグローバルに設定できます。
たとえば、Windows マシンでは :ref:`winrm <winrm_connection>` プラグインをインベントリー変数として設定できます。

多くの Connection プラグインは最小限の構成で動作します。デフォルトでは、:ref:`inventory hostname<inventory_hostnames_lookup>` を使用し、ターゲットホストを検索するようにデフォルト設定されています。

プラグインは、自己文書化されており、プラグインごとに、設定オプションについて文書化する必要があります。以下は、多くの connection プラグインに共通する接続変数です。

:ref:`ansible_host<magic_variables_and_hostvars>`
    接続するホストの名前 (:ref:`インベントリー<intro_inventory>` のホスト名と異なる場合)。
:ref:`ansible_port<faq_setting_users_and_ports>`
    :ref:`ssh <ssh_connection>` および :ref:`paramiko_ssh <paramiko_ssh_connection>` の ssh ポート番号は、デフォルトでは 22 に設定されます。
:ref:`ansible_user<faq_setting_users_and_ports>`
    ログインに使用するデフォルトのユーザー名。多くのプラグインは、「Ansible を実行する現在のユーザー」にデフォルトで設定されます。

プラグインごとに、一般的なバージョンをオーバーライドする特定の変数バージョンがある場合もあります。たとえば、:ref:`ssh <ssh_connection>` プラグインの場合は ``ansible_ssh_host`` です。

.. _connection_plugin_list:

プラグイン一覧
-----------

``ansible-doc -t connection -l`` を使用すると、利用可能なプラグインの一覧を表示できます。
詳細にわたるドキュメントや例を参照するには、``ansible-doc -t connection <plugin name>`` を使用します。


.. toctree:: :maxdepth: 1
    :glob:

    connection/*


.. seealso::

   :ref:`Playbook の使用<working_with_playbooks>`
       Playbook の概要
   :ref:`callback_plugins`
       Ansible callback プラグイン
   :ref:`Filters<playbooks_filters>`
       Jinja2 filter プラグイン
   :ref:`Tests<playbooks_tests>`
       Jinja2 test プラグイン
   :ref:`Lookups<playbooks_lookups>`
       Jinja2 lookup プラグイン
   :ref:`vars_plugins`
       Ansible vars プラグイン
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
