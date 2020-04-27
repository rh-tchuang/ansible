.. _vmware_guest_from_template:

****************************************
テンプレートからの仮想マシンのデプロイメント
****************************************

.. contents:: トピック

はじめに
============

本ガイドでは、Ansible を使用して、既存の VMware テンプレートまたは既存の VMware ゲストから仮想マシンのクローンを作成する方法を説明します。

シナリオの要件
=====================

* ソフトウェア

    * Ansible 2.5 以降がインストールされています。

    * Ansible (ローカルホストで実行していない場合はターゲットホスト) に、Python モジュール ``Pyvmomi`` をインストールしている必要があります。

    * [通常は、OS が提供するパッケージが古くなり、互換性がないため]、``pip`` から最新の ``Pyvmomi`` をインストールすることが推奨されます。

* ハードウェア

    * ESXi サーバーが 1 台以上搭載されている vCenter Server

* アクセス/認証情報

    * Ansible (またはターゲットサーバー) には、デプロイする vCenter サーバーまたは ESXi サーバーへのネットワークアクセスが必要です。

    * ユーザー名とパスワード

    * 以下の権限を持つユーザー

        - 宛先データストアまたはデータストアディレクトリーの ``Datastore.AllocateSpace``
        - 仮想マシンを割り当てるネットワークの ``Network.Assign``
        - 移行先ホスト、クラスター、またはリソースプールの ``Resource.AssignVMToPool``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.AddNewDisk``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.AddRemoveDevice``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Interact.PowerOn``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Inventory.CreateFromExisting``
        - クローンを作成している仮想マシンの ``VirtualMachine.Provisioning.Clone``
        - ゲストオペレーティングシステムをカスタマイズする場合、仮想マシンまたは仮想マシンディレクトリーの ``VirtualMachine.Provisioning.Customize``
        - 使用しているテンプレートの ``VirtualMachine.Provisioning.DeployTemplate``
        - ゲストオペレーティングシステムをカスタマイズする場合、ルート vCenter Server の ``VirtualMachine.Provisioning.ReadCustSpecs``
        
        要件によっては、以下の権限が 1 つ以上必要になる場合があります。 

        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.CPUCount``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.Memory``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.DiskExtend``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.Annotation``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.AdvancedConfig``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.EditDevice``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.Resource``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.Settings``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Config.UpgradeVirtualHardware``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Interact.SetCDMedia``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Interact.SetFloppyMedia``
        - データセンターまたは仮想マシンディレクトリーの ``VirtualMachine.Interact.DeviceConnection``

前提条件
===========

- 変数名および VMware オブジェクト名はすべて大文字と小文字を区別します。
- VMware では、データセンター間およびデータセンター内で、同じ名前の仮想マシンとテンプレートを作成できます。
- ``validate_certs`` オプションを使用するには、Python 2.7.9 バージョンを使用する必要があります。このバージョンは、SSL 検証の動作を変更できるためです。

注意事項
=======

- ESXi クラスター内のホストが、テンプレートが存在するデータストアにアクセスできる必要があります。
- 同じ名前のテンプレートが複数存在する場合、モジュールは失敗します。
- ゲストのカスタマイズを使用するには、テンプレートに VMware ツールをインストールする必要があります。Linux の場合は ``open-vm-tools`` パッケージが推奨されます。``Perl`` がインストールされている必要があります。


例の説明
===================

このユースケース/例では、仮想マシンテンプレートを選択して、データセンター/クラスターの特定のフォルダーにクローンを作成します。 以下の Ansible Playbook は、これに必要な基本的なパラメーターを示しています。

.. code-block:: yaml

    ---
    - name:Create a VM from a template
      hosts: localhost
      gather_facts: no
      tasks:
      - name:Clone the template
        vmware_guest:
          hostname: "{{ vcenter_ip }}"
      username: "{{ vcenter_username }}"
      password: "{{ vcenter_password }}"
      validate_certs: False
      name: testvm_2
      template: template_el7
      datacenter: "{{ datacenter_name }}"
      folder: /DC1/vm
      state: poweredon
      cluster: "{{ cluster_name }}"
          wait_for_ip_address: yes
    

Ansible は VMware API を使用してアクションを実行するため、このユースケースではローカルホストから API に直接接続されます。つまり、Playbook は vCenter サーバーまたは ESXi サーバーから実行しないことを意味します。必ずしもローカルホストに関するファクトを収集する必要がないため、``gather_facts`` パラメーターが無効になります。ローカルホストが vCenter サーバーにアクセスできない場合は、API に接続する別のサーバーに対してこのモジュールを実行できます。その場合は、必要な Python モジュールをターゲットサーバーにインストールする必要があります。

まず、必要な情報がいくつかあります。第一に、ESXi サーバーまたは vCenter サーバーのホスト名です。その後、このサーバーのユーザー名とパスワードが必要になります。現時点では直接入力しますが、より高度な Playbook では、:ref:`ansible-vault` または `Ansible Tower 認証情報<https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html>`_ を使用して、より安全な方法でこれを抽象化し、保存できます。vCenter サーバーまたは ESXi サーバーが Ansible サーバーから検証できる適切な CA 証明書で設定されていない場合は、``validate_certs`` パラメーターを使用してこの証明書の検証を無効にする必要があります。これを実行するには、Playbook に ``validate_certs=False`` を設定する必要があります。

次に、作成する仮想マシンに関する情報を指定する必要があります。仮想マシンに名前を付けます。命名規則のすべての VMware 要件に準拠する名前を付けます。 次に、新しい仮想マシンのクローンを作成するテンプレートの表示名を選択します。これは、VMware Web UI で表示されるものと完全に一致している必要があります。次に、この新しい仮想マシンを配置するディレクトリーを指定できます。このパスは、相対パスまたはデータセンターを含むディレクトリーへの完全パスのいずれかになります。仮想マシン状態の指定が必要になる場合があります。 これにより、実行するアクションがモジュールに指示されます。この場合は、仮想マシンが存在し、電源が入っていることを確認します。 任意のパラメーターは ``wait_for_ip_address`` です。これにより、これは仮想マシンが完全に起動し、VMware ツールが実行してからこのタスクが完了するのを待機するように Ansible に指示します。


予想されること
--------------

- この Playbook が完了すると、JSON の出力が表示されます。この出力は、新たに作成された仮想マシンについてモジュールおよび vCenter から返されるさまざまなパラメーターを表示します。

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
            "guest_tools_version":"0",
            "hw_cores_per_socket":1,
            "hw_datastores": [
            "ds_215"
        ],
            "hw_esxi_host":"192.0.2.44",
            "hw_eth0": {
                "addresstype": "assigned",
                "ipaddresses": null,
                "label":"Network adapter 1",
                "macaddress":"00:50:56:8c:19:f4",
                "macaddress_dash":"00-50-56-8c-19-f4",
                "portgroup_key": "dvportgroup-17",
                "portgroup_portkey":"0",
                "summary":"DVSwitch:50 0c 5b 22 b6 68 ab 89-fc 0b 59 a4 08 6e 80 fa"
            },
            "hw_files": [
            "[ds_215] testvm_2/testvm_2.vmx",
                "[ds_215] testvm_2/testvm_2.vmsd",
                "[ds_215] testvm_2/testvm_2.vmdk"
            ],
            "hw_folder": "/DC1/vm",
            "hw_guest_full_name": null,
            "hw_guest_ha_state": null,
            "hw_guest_id": null,
            "hw_interfaces": [
            "eth0"
        ],
            "hw_is_template": false,
            "hw_memtotal_mb":512,
            "hw_name": "testvm_2",
            "hw_power_status": "poweredOff",
            "hw_processor_count":2,
            "hw_product_uuid":"420cb25b-81e8-8d3b-dd2d-a439ee54fcc5",
            "hw_version": "vmx-13",
            "instance_uuid":"500cd53b-ed57-d74e-2da8-0dc0eddf54d5",
            "ipv4": null,
            "ipv6": null,
            "module_hw": true,
            "snapshots": []
        },
        "invocation": {
            "module_args": {
                "annotation": null,
                "cdrom": {},
                "cluster":"DC1_C1",
                "customization": {},
                "customization_spec": null,
                "customvalues": [],
                "datacenter":"DC1",
                "disk": [],
                "esxi_hostname": null,
                "folder": "/DC1/vm",
                "force": false,
                "guest_id": null,
                "hardware": {},
                "hostname":"192.0.2.44",
                "is_template": false,
                "linked_clone": false,
                "name": "testvm_2",
                "name_match": "first",
                "networks": [],
                "password":"VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                "port":443,
                "resource_pool": null,
                "snapshot_src": null,
                "state": "present",
                "state_change_timeout":0,
                "template": "template_el7",
                "username": "administrator@vsphere.local",
                "uuid": null,
                "validate_certs": false,
                "vapp_properties": [],
                "wait_for_ip_address": true
            }
        }
    }
    
- 状態が ``True`` に変更になり、仮想マシンが指定したテンプレートを使用して仮想マシンが構築されたことを通知します。モジュールは、VMware のクローンタスクが終了するまで完了しません。これは、環境に応じて多少時間がかかる場合があります。

- ``wait_for_ip_address`` パラメーターを使用すると、仮想マシンが OS で起動し、指定の NIC に IP アドレスが割り当てられているまで待機するため、クローン時間も増加します。



トラブルシューティング
---------------

調べること

- ユーザー名およびパスワードの値が正しいかどうかを確認します。
- 指定したデータセンターが利用可能かどうかを確認します。
- 指定したテンプレートが存在しているかどうか、およびデータストアにアクセスするパーミッションがあるかどうかを確認します。
- 指定したディレクトリーの完全パスが存在していることを確認します。ディレクトリーが自動的に作成されることはありません。

