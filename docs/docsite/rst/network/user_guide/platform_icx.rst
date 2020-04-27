.. _icx_platform_options:

***************************************
ICX プラットフォームのオプション
***************************************

ICX は、Enable モード (権限昇格) に対応します。ここでは、Ansible の ICX で Enalbe モードを使用する方法を説明します。

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

    |enable_mode|         supported: use ``ansible_become: yes`` with
                          ``ansible_become_method: enable`` and ``ansible_become_password:``

    返されるデータ形式 ``stdout[0]``
    ====================  ==========================================

.. |enable_mode| replace::Enable モード |br| (権限昇格)


Ansible での CLI の使用
====================

CLI の例: ``group_vars/icx.yml``
----------------------------------

.. code-block:: yaml

   ansible_connection: network_cli
   ansible_network_os: icx
   ansible_user: myuser
   ansible_password: !vault...
   ansible_become: yes
   ansible_become_method: enable
   ansible_become_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Backup current switch config (icx)
     icx_config:
       backup: yes
     register: backup_icx_location
     when: ansible_network_os == 'icx'

.. include:: shared_snippets/SSH_warning.txt
