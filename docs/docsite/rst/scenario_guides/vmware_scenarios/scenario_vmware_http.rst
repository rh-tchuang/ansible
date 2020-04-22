.. \_vmware\_http\_api\_usage:

***********************************
Ansible を使用した VMware HTTP API の使用
***********************************

.. contents:: トピック

はじめに
============

本書では、Ansible で VMware HTTP API を使用してさまざまなタスクを自動化する方法を説明します。

シナリオの要件
=====================

* ソフトウェア

    * Ansible 2.5 以降がインストールされています。

    * pip で最新バージョンをインストールすることが推奨されます。(通常は OS パッケージが古く、互換性がないため) 既存の VMware モジュールを使用する予定がある場合は、Ansible コントロールノードで ``pip install Pyvmomi`` を
      実行してください。

* ハードウェア

    * 少なくとも 1 台の ESXi サーバーを備えた vCenter Server 6.5 以降

* アクセス/認証情報

    * Ansible (またはターゲットサーバー) には、vCenter サーバーまたは ESXi サーバーへのネットワークアクセスが必要です。

    * vCenter のユーザー名およびパスワード

注意事項
=======

- 変数名および VMware オブジェクト名はすべて大文字と小文字を区別します。
- ``validate_certs`` オプションを使用するには、Python 2.7.9 バージョンを使用する必要があります。このバージョンは、SSL 検証の動作を変更できるためです。
- VMware HTTP API は、vSphere 6.5 以降で導入され、6.5 で必要となる最低レベルが必要です。
- 公開される API の数は非常に限られているため、XMLRPC ベースの VMware モジュールに依存する必要がある場合があります。


例の説明
===================

以下の Ansible Playbook を使用すると、VMware ESXi ホストシステムを見つけ、ホストシステムの一覧に応じてさまざまなタスクを実行できます。
これは、Ansible を使用して VMware HTTP API を使用する方法を実証する一般的な例です。

.. code-block:: yaml

    ---
    - name:Example showing VMware HTTP API utilization
      hosts: localhost
      gather_facts: no
      vars_files:
        - vcenter_vars.yml
      vars:
        ansible_python_interpreter: "/usr/bin/env python3"
      tasks:
        - name:Login into vCenter and get cookies
          uri:
            url: https://{{ vcenter_server }}/rest/com/vmware/cis/session
        force_basic_auth: yes
        validate_certs: no
        method: POST
        user: "{{ vcenter_user }}"
        password: "{{ vcenter_pass }}"
      register: login

    - name: Get all hosts from vCenter using cookies from last task
      uri:
        url: https://{{ vcenter_server }}/rest/vcenter/host
        force_basic_auth: yes
        validate_certs: no
        headers:
          Cookie: "{{ login.set_cookie }}"
      register: vchosts

    - name: Change Log level configuration of the given hostsystem
      vmware_host_config_manager:
        hostname: "{{ vcenter_server }}"
        username: "{{ vcenter_user }}"
        password: "{{ vcenter_pass }}"
        esxi_hostname: "{{ item.name }}"
        options:
          'Config.HostAgent.log.level': 'error'
        validate_certs: no
      loop: "{{ vchosts.json.value }}"
          register: host_config_results
    

Ansible は ``uri`` モジュールを使用してアクションを実行するために VMware HTTP API を利用して、このユースケースでは、ローカルホストから VMware HTTP API に直接接続されます。

つまり、Playbook は vCenter サーバーまたは ESXi サーバーから実行されないことを示しています。

ローカルホストに関するファクトは収集しないため、このプレイは ``gather_facts`` パラメーターを無効にすることに注意してください。

開始する前に、以下の点を確認してください。

- vCenter サーバーのホスト名
- vCenter サーバーのユーザー名およびパスワード
- vCenter のバージョンは 6.5 以上

現時点では直接入力しますが、より高度な Playbook では、:ref:`ansible-vault` または `Ansible Tower 認証情報<https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html>`_ を使用して、より安全な方法でこれを抽象化し、保存できます。

vCenter サーバーが Ansible サーバーから検証できる適切な CA 証明書で設定されていない場合は、``validate_certs`` パラメーターを使用してこの証明書の検証を無効にする必要があります。これを実行するには、Playbook に ``validate_certs=False`` を設定する必要があります。

ここに示されるとおり、最初のタスクで ``uri`` モジュールを使用して vCenter サーバーにログインし、登録を使用して ``login`` 変数に結果を保存します。次のタスクでは、最初のタスクの cookie を使用して ESXi ホストシステムに関する情報を収集します。

この情報を使用して、ESXi ホストシステムの事前設定を変更します。

予想されること
--------------

環境やネットワーク接続によっては、この Playbook の実行に時間がかかる場合があります。実行が完了すると、以下が表示されます。

.. code-block:: yaml

    "results": [
    {
        ...
        "invocation": {
            "module_args": {
                "cluster_name": null,
                "esxi_hostname": "10.76.33.226",
                "hostname": "10.65.223.114",
                "options": {
                    "Config.HostAgent.log.level": "error"
                },
                "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                "port": 443,
                "username": "administrator@vsphere.local",
                "validate_certs": false
            }
        },
        "item": {
            "connection_state": "CONNECTED",
            "host": "host-21",
            "name": "10.76.33.226",
            "power_state": "POWERED_ON"
        },
        "msg": "Config.HostAgent.log.level changed."
        ...
    }
]
    

トラブルシューティング
---------------

Playbook が失敗した場合は、以下を行います。

- ユーザー名およびパスワードの値が正しいことを確認します。
- vCenter 6.5 以降を使用してこの HTTP API を使用しているかどうかを確認します。

.. seealso::

    `VMware vSphere and Ansible From Zero to Useful by @arielsanchezmor <https://www.youtube.com/watch?v=0_qwOKlBlo8>`_
        VMware HTTP API に関連する vBrownBag セッションビデオ
    `Sample Playbooks for using VMware HTTP APIs <https://github.com/Akasurde/ansible-vmware-http>`_
        HTTP API を使用して VMware を管理する Ansible Playbook サンプルの GitHub リポジトリー
