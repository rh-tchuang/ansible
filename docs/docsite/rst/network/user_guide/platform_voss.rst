.. \_voss\_platform\_options:

***************************************
VOSS プラットフォームのオプション
***************************************

現在、Extreme VOSS の Ansible モジュールは、CLI 接続にのみ対応します。このページには、
Ansible の Voss で ``network_cli`` を使用します。

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

    |enable_mode|         サポート対象: ``ansible_become: yes`` を
                          ``ansible_become_method: enable`` とともに使用します。

    返されるデータ形式 ``stdout[0]``
    ====================  ==========================================

.. |enable\_mode| replace::Enable モード |br| (権限昇格)


VOSS は ``ansible_connection: local`` に対応していません。``ansible_connection: network_cli`` を使用する必要があります。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/voss.yml``
-----------------------------------

.. code-block:: yaml

   ansible\_connection: network\_cli
   ansible\_network\_os: voss
   ansible\_user: myuser
   ansible\_become: yes
   ansible\_become\_method: enable
   ansible\_password: !vault...
   ansible\_ssh\_common\_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Retrieve VOSS info
     voss\_command:
       commands: show sys-info
     when: ansible\_network\_os == 'voss'

.. include:: shared\_snippets/SSH\_warning.txt
