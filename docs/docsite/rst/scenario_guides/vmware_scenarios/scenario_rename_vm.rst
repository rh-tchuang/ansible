.. \_vmware\_guest\_rename\_virtual\_machine:

**********************************
既存の仮想マシンの名前変更
**********************************

.. contents:: トピック

はじめに
============

本ガイドでは、Ansible を使用して既存の仮想マシンの名前を変更する方法を説明します。

シナリオの要件
=====================

* ソフトウェア

    * Ansible 2.5 以降がインストールされています。

    * Ansible コントロールノード (またはローカルホストで実行していない場合はターゲットホスト) に、Python モジュール ``Pyvmomi`` をインストールしている必要があります。

    * pip で最新バージョンをインストールすることが推奨されます。インストールするには ``pip install Pyvmomi`` を実行してください (通常は OS パッケージが古く、互換性がないため)。

* ハードウェア

    * 少なくともスタンドアロンの ESXi サーバー 1 台、または

    * ESXi サーバーが 1 台以上搭載されている vCenter Server

* アクセス/認証情報

    * Ansible (またはターゲットサーバー) には、vCenter サーバーまたは ESXi サーバーへのネットワークアクセスが必要です。

    * vCenter サーバーまたは ESXi サーバーのユーザー名およびパスワード

    * ESXi クラスター内のホストが、テンプレートが存在するデータストアにアクセスできる必要があります。

注意事項
=======

- 変数名および VMware オブジェクト名はすべて大文字と小文字を区別します。
- ``validate_certs`` オプションを使用するには、Python 2.7.9 バージョンを使用する必要があります。このバージョンは、SSL 検証の動作を変更できるためです。


例の説明
===================

以下の Ansible Playbook を使用して、UUID を変更して既存の仮想マシンの名前を変更できます。

.. code-block:: yaml

    ---
    - name:Rename virtual machine from old name to new name using UUID
      gather_facts: no
      vars_files:
        - vcenter_vars.yml
      vars:
        ansible_python_interpreter: "/usr/bin/env python3"
      hosts: localhost
      tasks:
        - set_fact:
            vm_name: "old_vm_name"
            new_vm_name: "new_vm_name"
            datacenter:"DC1"
            cluster_name:"DC1_C1"

        - name:Get VM "{{ vm_name }}" uuid
      vmware_guest_facts:
        hostname: "{{ vcenter_server }}"
        username: "{{ vcenter_user }}"
        password: "{{ vcenter_pass }}"
        validate_certs: False
        datacenter: "{{ datacenter }}"
        folder: "/{{datacenter}}/vm"
        name: "{{ vm_name }}"
      register: vm_facts

    - name: Rename "{{ vm_name }}" to "{{ new_vm_name }}"
      vmware_guest:
        hostname: "{{ vcenter_server }}"
        username: "{{ vcenter_user }}"
        password: "{{ vcenter_pass }}"
        validate_certs: False
        cluster: "{{ cluster_name }}"
        uuid: "{{ vm_facts.instance.hw_product_uuid }}"
        name: "{{ new_vm_name }}"
    
Ansible は VMware API を使用してアクションを実行するため、このユースケースではローカルホストから API に直接接続されます。

つまり、Playbook は vCenter サーバーまたは ESXi サーバーから実行されないことを示しています。

ローカルホストに関するファクトは収集しないため、このプレイは ``gather_facts`` パラメーターを無効にすることに注意してください。

ローカルホストが vCenter サーバーにアクセスできない場合は、API に接続する別のサーバーに対してこのモジュールを実行できます。その場合は、必要な Python モジュールをターゲットサーバーにインストールする必要があります。pip で最新バージョンをインストールすることが推奨されます。インストールするには ``pip install Pyvmomi`` を実行してください (通常は OS パッケージが古く、互換性がないため)。

開始する前に、以下の点を確認してください。

- ESXi サーバーまたは vCenter サーバーのホスト名
- ESXi サーバーまたは vCenter サーバーのユーザー名およびパスワード
- 名前を変更する既存の仮想マシンの UUID

現時点では直接入力しますが、より高度な Playbook では、:ref:`ansible-vault` または `Ansible Tower 認証情報<https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html>`_ を使用して、より安全な方法でこれを抽象化し、保存できます。

vCenter サーバーまたは ESXi サーバーが Ansible サーバーから検証できる適切な CA 証明書で設定されていない場合は、``validate_certs`` パラメーターを使用してこの証明書の検証を無効にする必要があります。これを実行するには、Playbook に ``validate_certs=False`` を設定する必要があります。

次に、名前を変更する既存の仮想マシンに関する情報を指定する必要があります。仮想マシンの名前変更のために、``vmware_guest`` モジュールは VMware UUID を使用します。これは、vCenter 環境全体で一意です。この値は自動生成され、変更できません。``vmware_guest_facts`` モジュールを使用して仮想マシンを検索し、仮想マシンの VMware UUID に関する情報を取得します。

この値は、``vmware_guest`` モジュールの入力に使用されます。``name`` パラメーターとして命名規則のすべての VMware 要件に準拠する仮想マシンに新しい名前を指定します。また、``uuid`` を VMware UUID の値として提供します。

予想されること
--------------

環境やネットワーク接続によっては、この Playbook の実行に時間がかかる場合があります。実行が完了すると、以下が表示されます。

.. code-block:: yaml

    {
        "changed": true,
        "instance": {
            "annotation": "",
            "current_snapshot": null,
            "customvalues": {},
            "guest_consolidation_needed": false,
            "guest_question": null,
            "guest_tools_status": "guestToolsNotRunning",
            "guest_tools_version":"10247",
            "hw_cores_per_socket":1,
            "hw_datastores": ["ds_204_2"],
            "hw_esxi_host":"10.x.x.x",
            "hw_eth0": {
                "addresstype": "assigned",
                "ipaddresses": [],
                "label":"Network adapter 1",
                "macaddress":"00:50:56:8c:b8:42",
                "macaddress_dash":"00-50-56-8c-b8-42",
                "portgroup_key": "dvportgroup-31",
                "portgroup_portkey":"15",
                "summary":"DVSwitch:50 0c 3a 69 df 78 2c 7b-6e 08 0a 89 e3 a6 31 17"
            },
            "hw_files": ["[ds_204_2] old_vm_name/old_vm_name.vmx", "[ds_204_2] old_vm_name/old_vm_name.nvram", "[ds_204_2] old_vm_name/old_vm_name.vmsd", "[ds_204_2] old_vm_name/vmware.log", "[ds_204_2] old_vm_name/old_vm_name.vmdk"],
            "hw_folder": "/DC1/vm",
            "hw_guest_full_name": null,
            "hw_guest_ha_state": null,
            "hw_guest_id": null,
            "hw_interfaces": ["eth0"],
            "hw_is_template": false,
            "hw_memtotal_mb":1024,
            "hw_name": "new_vm_name",
            "hw_power_status": "poweredOff",
            "hw_processor_count":1,
            "hw_product_uuid":"420cbebb-835b-980b-7050-8aea9b7b0a6d",
            "hw_version": "vmx-13",
            "instance_uuid":"500c60a6-b7b4-8ae5-970f-054905246a6f",
            "ipv4": null,
            "ipv6": null,
            "module_hw": true,
            "snapshots": []
        }
    }

仮想マシンの名前が変更されたことを確認します。


トラブルシューティング
---------------

Playbook が失敗した場合は、以下を行います。

- ユーザー名およびパスワードの値が正しいことを確認します。
- 指定したデータセンターが利用可能かどうかを確認します。
- 指定した仮想マシンが存在しているかどうか、およびデータストアにアクセスするパーミッションがあるかどうかを確認します。
- 指定したディレクトリーの完全パスが存在していることを確認します。
