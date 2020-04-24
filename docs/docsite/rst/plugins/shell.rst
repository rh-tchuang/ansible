.. \_shell\_plugins:

Shell プラグイン
=============

.. contents::
   :local:
   :depth: 2

Shell プラグインが機能し、Ansible が実行する基本的なコマンドが適切にフォーマットされ、かつターゲットマシンと連携することを確認します。
これにより、ユーザーが Ansible によるタスクの実行方法に関連する特定の動作を設定できるようになります。

.. \_enabling\_shell:

Shell プラグインの有効化
----------------------

カスタムの Shell プラグインを追加にするには、カスタムのプラグインを、ロール内の Play の隣りにある ``vars_plugins`` ディレクトリーに配置するか、
:ref:`ansible.cfg <ansible_configuration_settings>` で設定した shell プラグインディレクトリーソースの 1 つに配置します。

.. warning:: デフォルトの ``/bin/sh`` が POSIX に準拠していないシェルで、実行に利用できない場合は、
 使用するプラグインを変更するべきではありません。

.. \_using\_shell:

Shell プラグインの使用
-------------------

:ref:`ansible_configuration_settings` のデフォルト設定に加えて、
使用するプラグインを選択するための接続変数 :ref:`ansible_shell_type <ansible_shell_type>` を選択できます。
このような場合には、:ref:`ansible_shell_executable <ansible_shell_executable>` を一致するように更新することもできます。

プラグイン自体で詳しく説明されている (以下に記載) その他の設定オプションを使用して、
各プラグインの設定をさらに制御できます。

.. toctree:: :maxdepth: 1
    :glob:

    shell/*

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
