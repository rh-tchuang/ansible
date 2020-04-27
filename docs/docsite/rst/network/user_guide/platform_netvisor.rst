.. _netvisor_platform_options:

**********************************
Pluribus NETVISOR プラットフォームのオプション
**********************************

Pluribus NETVISOR Ansible モジュールは現時点では CLI 接続のみに対応します。``httpapi`` モジュールは今後追加される可能性があります。
このページには、Ansible で NETVISOR の ``network_cli`` を使用する詳細な方法が記載されています。

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

    |enable_mode|         NETVISOR では対応していません。

    返されるデータ形式 ``stdout[0]``
    ====================  ==========================================

.. |enable_mode| replace::Enable モード |br| (権限昇格)

Pluribus NETVISOR は ``ansible_connection: local`` に対応していません。``ansible_connection: network_cli`` を使用する必要があります。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/netvisor.yml``
---------------------------------------

.. code-block:: yaml

   ansible_connection: network_cli
   ansible_network_os: netvisor
   ansible_user: myuser
   ansible_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Create access list
     pn_access_list:
       pn_name: "foo"
       pn_scope: "local"
       state: "present"
     register: acc_list
     when: ansible_network_os == 'netvisor'


.. include:: shared_snippets/SSH_warning.txt
