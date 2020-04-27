.. _exos_platform_options:

***************************************
EXOS プラットフォームのオプション
***************************************

Extreme EXOS Ansible モジュールは、複数の接続に対応しています。このページには、各接続が Ansible でどのように機能するか、およびその使用方法に関する詳細が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================


.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                   CLI                                         EXOS-API
    ====================  ==========================================  =========================
    プロトコル              SSH                                         HTTP(S)

    認証情報           (存在する場合は) SSH キー / SSH-agent を使用します。        (存在する場合は) HTTPS 証明書を使用します。

                          パスワードを使用する場合は ``-u myuser -k`` を許可します。

    間接アクセス       bastion (ジャンプホスト) を経由                   Web プロキシーを経由

    接続設定   ``ansible_connection: network_cli``         ``ansible_connection: httpapi``

    |enable_mode|         EXOS では対応していません。                       EXOS では対応していません。

    返されるデータ形式  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================

.. |enable_mode| replace::Enable モード |br| (権限昇格)

EXOS は ``ansible_connection: local`` に対応していません。``ansible_connection: network_cli`` または ``ansible_connection: httpapi`` を使用する必要があります。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/exos.yml``
-----------------------------------

.. code-block:: yaml

   ansible_connection: network_cli
   ansible_network_os: exos
   ansible_user: myuser
   ansible_password: !vault...
   ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Retrieve EXOS OS version
     exos_command:
       commands: show version
     when: ansible_network_os == 'exos'



Ansible での EXOS-API の使用
=========================

EXOS-API の例: ``group_vars/exos.yml``
----------------------------------------

.. code-block:: yaml

   ansible_connection: httpapi
   ansible_network_os: exos
   ansible_user: myuser
   ansible_password: !vault...
   proxy_env:
     http_proxy: http://proxy.example.com:8080

- (Web プロキシーを経由せず) ホストに直接アクセスしている場合は、``proxy_env`` 設定を削除できます。
- ``https`` を使用して Web プロキシー経由でホストにアクセスする場合は、``http_proxy`` を ``https_proxy`` に変更します。


EXOS-API タスクの例
---------------------

.. code-block:: yaml

   - name:Retrieve EXOS OS version
     exos_command:
       commands: show version
     when: ansible_network_os == 'exos'

この例では、``group_vars`` で定義された ``proxy_env`` 変数は、タスクのモジュールで使用される ``environment`` オプションに渡されます。

.. include:: shared_snippets/SSH_warning.txt
