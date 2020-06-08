.. _VMware_module_development:

****************************************
VMware モジュール開発のガイドライン
****************************************

VMware モジュールおよびこれらのガイドラインは、VMware Working Group が管理しています。たとえば、
`チームのコミュニティーページ <https://github.com/ansible/community/wiki/VMware>`_ を参照してください。

.. contents::
   :local:

govcsim を使用したテスト
====================

既存のモジュールのほとんどは、機能テストで対応しています。テストは :file:`test/integration/targets/` にあります。

デフォルトでは、テストは `govcsim <https://github.com/vmware/govmomi/tree/master/vcsim>`_ という名前の vCenter API シミュレーターに対して実行されます。``ansible-test`` は、`govcsim コンテナー <https://quay.io/repository/ansible/vcenter-test-container>` を自動的にプルし、これを使用してテスト環境を設定します。

``ansible-test`` コマンドを使用して、モジュールのテストを手動でトリガーできます。たとえば、``vcenter_folder`` テストをトリガーするには、以下を使用します。

.. code-block:: shell

    source hacking/env-setup
    ansible-test integration --python 3.7 vcenter_folder

``govcsim`` は、通常のテスト環境よりも高速なため便利です。ただし、
ESXi または vCenter のすべての機能に対応しているわけではありません。

.. note::

   ``govcsim`` と ``vcsim`` を混同しないようにしてください。vcsim は古いバージョンの vCenterシミュレーターですが、govcsim は新しく、Go 言語で書かれています

独自のインフラストラクチャーでのテスト
====================================

通常の VMware 環境を対象とすることもできます。この段落では、テストスイートを自分で実行する方法について順を追って説明します。

要件
------------

- 2 台の ESXi ホスト (6.5 または 6.7)
   - 2 つの NIC (テスト用に 2 番目の NIC が利用可能)
- VCSA ホスト
- NFS サーバー
- Python の依存関係:
    - `pyvmomi <https://github.com/vmware/pyvmomi/tree/master/pyVmomi>`
    - `requests <https://2.python-requests.org/en/master/>`

ハイパーバイザーにテスト環境をデプロイする場合は、VMware と Libvirt (<https://github.com/goneri/vmware-on-libvirt>) の両方が正常に機能します。

NFS サーバーの設定
~~~~~~~~~~~~~~~~~~~~~~~~

NFS サーバーでは、以下のディレクトリー構造を公開する必要があります。

.. code-block:: shell

    $ tree /srv/share/
    /srv/share/
    ├── isos
    │   ├── base.iso
    │   ├── centos.iso
    │   └── fedora.iso
    └── vms
    2 directories, 3 files

Linux システムでは、次のエクスポートファイルを使用して、NFS 経由でディレクトリーを公開できます。

.. code-block:: shell

    $ cat /etc/exports
    /srv/share  192.168.122.0/255.255.255.0(rw,anonuid=1000,anongid=1000)

.. note::

    この設定では、UID 1000 および GID 1000 のユーザーが、新しいファイルをすべてが所有します。
    ユーザーの UID および GID に合わせて設定を調整してください。

このサービスは以下で有効にできます。

.. code-block:: shell

   $ sudo systemctl enable --now nfs-server


インストールの設定
---------------------------

セットアップを記述する設定ファイルを準備します。ファイルの名前は、
:file:`test/lib/ansible_test/config/cloud-config-vcenter.ini.template` で、
:file:`test/integration/cloud-config-vcenter.ini` を呼び出してからベースにする必要があります。たとえば、`VMware-on-libvirt` <https://github.com/goneri/vmware-on-libvirt> を使用してラボをデプロイしている場合は、
次を使用します。

.. code-block:: ini

    [DEFAULT]
    vcenter_username: administrator@vsphere.local
    vcenter_password: !234AaAa56
    vcenter_hostname: vcenter.test
    vmware_validate_certs: false
    esxi1_username: root
    esxi1_hostname: esxi1.test
    esxi1_password: root
    esxi2_username: root
    esxi2_hostname: test2.test
    esxi2_password: root

HTTP プロキシーを使用する場合
-------------------------
HTTP プロキシーの背後でテストインフラストラクチャーをホストするためのサポートは現在開発中です。詳細は、以下のプル要求を参照してください。

- ansible-test: HTTP プロキシーの背後にある vcenter (<https://github.com/ansible/ansible/pull/58208>)
- pyvmkko: proxy サポート (<https://github.com/vmware/pyvmomi/pull/799>)
- VMware: 接続 API に HTTP プロキシーのサポートを追加 (<https://github.com/ansible/ansible/pull/52936>)

これらの PR からコードを組み込んだら、別の 2 つのキーでプロキシーサーバーの場所を指定します。

.. code-block:: ini

    vmware_proxy_host: esxi1-gw.ws.testing.ansible.com
    vmware_proxy_port: 11153

さらに、以下のファイルの変数をラボの設定に合わせて調整しないといけない場合があります。
:file:`test/integration/targets/prepare_vmware_tests/vars/real_lab.yml`.`vmware-on-libvirt <https://github.com/goneri/vmware-on-libvirt>` を使用してラボを準備する場合は、変更することができません。

テストスイートの実行
------------------

設定の準備ができたら、以下のコマンドで実行をトリガーできます。

.. code-block:: shell

    source hacking/env-setup
    VMWARE_TEST_PLATFORM=static ansible-test integration --python 3.7 vmware_host_firewall_manager

``vmware_host_firewall_manager`` は、テストするモジュールの名前です。

``vmware_guest`` は、他のテストロールよりもはるかに大きく、速度もかなり遅くなります。一部のテスト Playbook を、
:file:`test/integration/targets/vmware_guest/defaults/main.yml` で有効または無効にできます。


ユニットテスト
=========

VMware モジュールでは、ユニットテストの対象範囲が限られています。テストスイートは、
次のコマンドで実行できます。

.. code-block:: shell

    source hacking/env-setup
    ansible-test units --tox --python 3.7 '.*vmware.*'

コードスタイルおよびベストプラクティス
============================

ESXi での datacenter 引数
-----------------------------

``datacenter`` パラメーターでは、デフォルトで ``ha-datacenter`` を使用していないはずです。これは、Ansible が誤って間違ったデータセンターを対象としていることに、
ユーザーが気付かない可能性があるためです。

esxi_hostname は必須ではない
-------------------------------------

ESXi または vCenter が提供する機能に応じて、一部のモジュールは両方でシームレスに動作します。この場合、
``ESXi_hostname`` パラメーターは任意である必要があります。

.. code-block:: python

    if self.is_vcenter():
        esxi_hostname = module.params.get('esxi_hostname')
        if not esxi_hostname:
            self.module.fail_json("esxi_hostname parameter is mandatory")
        self.host = self.get_all_host_objs(cluster_name=cluster_name, esxi_host_name=esxi_hostname)[0]
    else:
        self.host = find_obj(self.content, [vim.HostSystem], None)
    if self.host is None:
        self.module.fail_json(msg="Failed to find host system.")

機能テスト
----------------

新規テストの作成
~~~~~~~~~~~~~~~~~

統合テストの新しいコレクションを作成する場合は、
標準の Ansible :ref:`統合テスト<testing_integration>` プロセス以外に、VMware 固有の注意点がいくつかあります。

テストスイートは、:file:`test/integration/targets/prepare_vmware_tests/` ロールにある一般的な事前定義済みの変数のセットを使用します。
ここに定義されたリソースは、テストの開始時にそのロールをインポートして自動的に作成されます。

.. code-block:: yaml

  - import_role:
      name: prepare_vmware_tests
    vars:
      setup_datacenter: true

これにより、クラスター、データセンター、データストア、ディレクトリー、スイッチ、dvSwitch、ESXi ホスト、および仮想マシンを使用する準備が整います。

リソースを過剰に作成する必要なし
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ほとんどの場合、複数のリソースを作成するために ``with_items`` を使用する必要はありません。これを回避することで、
テストの実行を迅速化し、その後のクリーンアップを簡素化します。

仮想マシン名は、名前で内容が予測できるものにする必要があります。
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

テスト中に新しい仮想マシンを作成する必要がある場合は、``test_vm1``、``test_vm2``、または ``test_vm3`` を使用できます。これにより、
自動的にクリーンアップされます。


表記規則
======================

命名法
------------

Ansible のドキュメントでは、次のルールを適用しています。

- VMware (VMWare または vmware ではありません)
- ESXi (esxi または ESXI ではありません)
- vCenter (vcenter または VCenter ではない)

また、``govcsim`` を使用した vcsim の Go 実装も参照します。これは、古い実装との混乱を回避するためのものです。
