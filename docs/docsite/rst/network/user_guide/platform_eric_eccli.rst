.. _eic_eccli_platform_options:

***************************************
ERIC_ECCLI プラットフォームのオプション
***************************************

現在、Extreme ERIC_ECCLI の Ansible モジュールは、CLI 接続にのみ対応します。このページには、Ansible で ERIC_ECCLI の ``network_cli`` を使用する詳細な方法が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                   CLI
    ====================  ==========================================
    プロトコル              SSH

    認証情報           SSH キー / SSH-agent (存在する場合) を使用します。

                          パスワードを使用する場合は ``-u myuser -k`` を許可します。

    間接アクセス       bastion (ジャンプホスト) を経由

    接続設定   ``ansible_connection: network_cli``

    |enable_mode|         ERIC_ECCLI では対応していません。

    返されるデータ形式 ``stdout[0]``
    ====================  ==========================================

.. |enable_mode| replace::Enable モード |br| (権限昇格)

Eric_ECCLI は、``ansible_connection: local`` に対応していません。``ansible_connection: network_cli`` を使用する必要があります。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/eric_eccli.yml``
-----------------------------------------

.. code-block:: yaml

   ansible_connection: network_cli
   ansible_network_os: eric_eccli
   ansible_user: myuser
   ansible_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name: run show version on remote devices (eric_eccli)
     eric_eccli_command:
        commands: show version
     when: ansible_network_os == 'eric_eccli'

.. include:: shared_snippets/SSH_warning.txt
