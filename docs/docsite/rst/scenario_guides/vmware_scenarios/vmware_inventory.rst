.. \_vmware\_ansible\_inventory:

*************************************
VMware 動的インベントリープラグインの使用
*************************************

.. contents:: トピック

VMware 動的インベントリープラグイン
===============================


ホストと対話する最善の方法は、VMware 動的インベントリープラグインを使用することです。これは、VMware API を動的にクエリーし、
管理できるノードを Ansible に指示します。

要件
------------

VMware 動的インベントリープラグインを使用するには、
コントロールノード (Ansible を実行するホスト) に `pyVmomi <https://github.com/vmware/pyvmomi>`_ をインストールする必要があります。

仮想マシンのタグ関連の情報を動的インベントリーに含めるには、コントロールノードでタグ付けやコンテンツライブラリーなどの REST API 機能に対応する `vSphere Automation SDK <https://code.vmware.com/web/sdk/65/vsphere-automation-python>`_ も必要になります。
手順 `<https://github.com/vmware/vsphere-automation-sdk-python#installing-required-python-packages>`_ の指示に従って、``vSphere Automation SDK`` をインストールできます。

.. code-block:: bash

    $ pip install pyvmomi

この VMware 動的インベントリープラグインを使用するには、最初に ``ansible.cfg`` ファイルに以下を指定して有効にする必要があります。

.. code-block:: ini

  \[inventory]
  enable\_plugins = vmware\_vm\_inventory

次に、作業ディレクトリーに ``.vmware.yml`` または ``.vmware.yaml`` で終わるファイルを作成します。

``vmware_vm_inventory`` スクリプトは、VMware モジュールと同じ認証情報を取得します。

以下は、有効なインベントリーファイルの例です。

.. code-block:: yaml

    plugin: vmware_vm_inventory
    strict:False
    hostname:10.65.223.31
    username: administrator@vsphere.local
    password:Esxi@123$%
    validate_certs:False
    with_tags:True


``ansible-inventory --list -i <filename>.vmware.yml`` を実行すると、Ansible を使用して設定する準備ができている VMware インスタンスの一覧が作成されます。

vault が設定された設定ファイルの使用
=================================

インベントリー設定ファイルには、プレーンテキストでセキュリティーリスクがある vCenter パスワードが含まれるため、
インベントリー設定ファイル全体を暗号化します。

有効なインベントリー設定ファイルは以下のように暗号化できます。

.. code-block:: bash

    $ ansible-vault encrypt <filename>.vmware.yml
  New Vault password:
  Confirm New Vault password:
  Encryption successful

また、以下を使用して、vault が設定されたこのインベントリー設定ファイルを使用できます。

.. code-block:: bash

    $ ansible-inventory -i filename.vmware.yml --list --vault-password-file=/path/to/vault_password_file


.. seealso::

    `pyVmomi <https://github.com/vmware/pyvmomi>`_
        pyVmomi の GitHub ページ
    `pyVmomi Issue Tracker <https://github.com/vmware/pyvmomi/issues>`_
        pyVmomi プロジェクトの問題トラッカー
    `vSphere Automation SDK GitHub Page <https://github.com/vmware/vsphere-automation-sdk-python>`_
        Python 向けの vSphere Automation SDK の GitHub ページ
    `vSphere Automation SDK Issue Tracker <https://github.com/vmware/vsphere-automation-sdk-python/issues>`_
        Python 向けの vSphere Automation SDK の問題トラッカー
    :ref:`working_with_playbooks`
        Playbook の概要
    :ref:`playbooks_vault`
        Playbook での Vault の使用
