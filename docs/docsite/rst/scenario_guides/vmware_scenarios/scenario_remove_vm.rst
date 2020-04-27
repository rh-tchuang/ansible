.. _vmware_guest_remove_virtual_machine:

*****************************************
既存の VMware 仮想マシンの削除
*****************************************

.. contents:: トピック

はじめに
============

本ガイドでは、Ansible を使用して既存の VMware 仮想マシンを削除する方法を説明します。

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
- ``vmware_guest`` モジュールは、VMware Web UI およびワークフローを模倣するため、VMware インベントリーから仮想マシンを削除するには、電源がオフになっている必要があります。

.. warning::

   ``vmware_guest`` モジュールを使用して VMware 仮想マシンを削除することは破壊的な操作であり、元に戻すことができないため、先に進む前に仮想マシンと関連ファイル (vmx ファイルおよび vmdk ファイル) のバックアップを作成することが強く推奨されます。

例の説明
===================

このユースケース/例では、名前を使用して仮想マシンを削除します。以下の Ansible Playbook は、これに必要な基本的なパラメーターを示しています。

.. code-block:: yaml

    ---
    - name:Remove virtual machine
      gather_facts: no
      vars_files:
        - vcenter_vars.yml
      vars:
        ansible_python_interpreter: "/usr/bin/env python3"
      hosts: localhost
      tasks:
        - set_fact:
            vm_name:"VM_0003"
            datacenter:"DC1"

        - name:Remove "{{ vm_name }}"
      vmware_guest:
        hostname: "{{ vcenter_server }}"
        username: "{{ vcenter_user }}"
        password: "{{ vcenter_pass }}"
        validate_certs: no
        cluster: "DC1_C1"
        name: "{{ vm_name }}"
            state: absent
          delegate_to: localhost
          register: facts
    

Ansible は VMware API を使用してアクションを実行するため、このユースケースではローカルホストから API に直接接続されます。

つまり、Playbook は vCenter サーバーまたは ESXi サーバーから実行されないことを示しています。

ローカルホストに関するファクトは収集しないため、このプレイは ``gather_facts`` パラメーターを無効にすることに注意してください。

ローカルホストが vCenter サーバーにアクセスできない場合は、API に接続する別のサーバーに対してこのモジュールを実行できます。その場合は、必要な Python モジュールをターゲットサーバーにインストールする必要があります。pip で最新バージョンをインストールすることが推奨されます。インストールするには ``pip install Pyvmomi`` を実行してください (通常は OS パッケージが古く、互換性がないため)。

開始する前に、以下の点を確認してください。

- ESXi サーバーまたは vCenter サーバーのホスト名
- ESXi サーバーまたは vCenter サーバーのユーザー名およびパスワード
- 削除する既存の仮想マシンの名前

現時点では直接入力しますが、より高度な Playbook では、:ref:`ansible-vault` または `Ansible Tower 認証情報 <https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html>`_ を使用して、より安全な方法でこれを抽象化し、保存できます。

vCenter サーバーまたは ESXi サーバーが Ansible サーバーから検証できる適切な CA 証明書で設定されていない場合は、``validate_certs`` パラメーターを使用してこの証明書の検証を無効にする必要があります。これを実行するには、Playbook に ``validate_certs=False`` を設定する必要があります。

既存の仮想マシンの名前は、``name`` パラメーターで ``vmware_guest`` モジュールの入力として使用されます。


予想されること
--------------

- この Playbook の完了後に、``vmware_guest`` モジュールを使用して実行した他の操作と比較した JSON 出力は表示されません。

.. code-block:: yaml

    {
        "changed": true
    }

- 状態が ``True`` に変更になり、仮想マシンが VMware インベントリーから削除されることを通知します。環境やネットワーク接続によっては、時間がかかる場合があります。


トラブルシューティング
---------------

Playbook が失敗した場合は、以下を行います。

- ユーザー名およびパスワードの値が正しいことを確認します。
- 指定したデータセンターが利用可能かどうかを確認します。
- 指定した仮想マシンが存在しているかどうか、およびデータストアにアクセスするパーミッションがあるかどうかを確認します。
- 指定したディレクトリーの完全パスが存在していることを確認します。ディレクトリーが自動的に作成されることはありません。
