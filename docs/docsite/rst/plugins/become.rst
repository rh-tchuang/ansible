.. \_become\_plugins:

become プラグイン
==============

.. contents::
   :local:
   :depth: 2

.. versionadded:: 2.8

bocome プラグインは、基本的なコマンドの実行時に、
Ansible が特定の特権昇格システムを使用して、
Play で指定されたタスクを実行するのに必要なモジュールやターゲットマシンと連携できるようにします。

通常、``sudo``、``su``、``doas`` などのユーティリティーを使用すると、別のユーザーになり (become)、
そのユーザーのパーミッションでコマンドを実行できるようになります。


.. \_enabling\_become:

Become プラグインの有効化
-----------------------

Ansible に同梱の become プラグインはすでに有効化されています。カスタムのプラグインを追加するには、
ロール内の Play の隣りにある ``become_plugins`` ディレクトリーに配置するか
:ref:`ansible.cfg <ansible_configuration_settings>` で設定した become プラグインのディレクトリーソースの 1 つに配置します。


.. \_using\_become:

Become プラグインの使用
--------------------

:ref:`ansible_configuration_settings` や 
``--become-method`` コマンドラインオプションでのデフォルト設定に加え、Play で ``become_method`` キーワードを使用できます。
「ホスト固有」にする必要がある場合には、接続変数の ``ansible_become_method`` で、使用するプラグインを選択します。

プラグイン自体 (以下にリンク) に詳述されているその他の設定オプションを使用して、
各プラグインの設定をさらに制御できます。

.. \_become\_plugin\_list:

プラグイン一覧
-----------

``ansible-doc -t become -l`` を使用して、利用可能なプラグインの一覧を表示できます。
特定のドキュメントと例を参照する場合は、``ansible-doc -t become <plugin name>`` を使用してください。

.. toctree:: :maxdepth: 1
    :glob:

    become/*

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
       \#ansible IRC chat channel
