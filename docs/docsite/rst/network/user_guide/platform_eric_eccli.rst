.. \_eic\_eccli\_platform\_options:

***************************************
ERIC\_ECCLI プラットフォームのオプション
***************************************

現在、Extreme ERIC\_ECCLI の Ansible モジュールは、CLI 接続にのみ対応します。このページには、Ansible で ERIC\_ECCLI の ``network_cli`` を使用する詳細な方法が記載されています。

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

.. |enable\_mode| replace::Enable モード |br| (権限昇格)

Eric\_ECCLI は、``ansible_connection: local`` に対応していません。``ansible_connection: network_cli`` を使用する必要があります。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/eric_eccli.yml``
-----------------------------------------

.. code-block:: yaml

   ansible\_connection: network\_cli
   ansible\_network\_os: eric\_eccli
   ansible\_user: myuser
   ansible\_password: !vault...
   ansible\_ssh\_common\_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name: run show version on remote devices (eric\_eccli)
     eric\_eccli\_command:
        commands: show version
     when: ansible\_network\_os == 'eric\_eccli'

.. include:: shared\_snippets/SSH\_warning.txt
