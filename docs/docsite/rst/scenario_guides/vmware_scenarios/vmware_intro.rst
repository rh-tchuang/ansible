.. _vmware_ansible_intro:

**********************************
VMware 向け Ansible の概要
**********************************

.. contents:: トピック

はじめに
============

Ansible は、
データセンター、クラスター、ホストシステム、仮想マシンなどの VMware インフラストラクチャーを管理するさまざまなモジュールを提供します。

要件
============

Ansible VMware モジュールは、`pyVmomi <https://github.com/vmware/pyvmomi>`_ に記述されます。
pyVmomi は、
ユーザーが ESX、ESXi、vCenter インフラストラクチャーを管理できるようにする VMware vSphere API の Python SDK です。pip を使用して pyVmomi をインストールできます。

.. code-block:: bash

    $ pip install pyvmomi

最新の vSphere(6.0 以降の) 機能を使用する Ansible VMware モジュールは、`vSphere Automation Python SDK` <https://github.com/vmware/vsphere-automation-sdk-python>_ を使用します。VSphere Automation Python SDK には、AWS Console API 向け VMware Cloud、AWS 統合 API 向け NSX VMware Cloud、AWS サイトリカバリー API 向け VMware Cloud、NSX-T API に対するクライアントライブラリー、ドキュメント、サンプルコードもあります。

VSphere Automation Python SDK は、pip を使用してインストールできます。

.. code-block:: bash

     $ pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git

注記:
   VSphere Automation Python SDK をインストールすると、``pyvmomi`` もインストールされます。``pyvmomi`` の個別インストールは必要ありません。
   
vmware_guest モジュール
===================

:ref:`vmware_guest<vmware_guest_module>` モジュールは、特定の ESXi サーバーまたは vCenter サーバーで仮想マシンに関連するさまざまな操作を管理します。


.. seealso::

    `pyVmomi <https://github.com/vmware/pyvmomi>`_
        pyVmomi の GitHub ページ
    `pyVmomi Issue Tracker <https://github.com/vmware/pyvmomi/issues>`_
        pyVmomi プロジェクトの問題トラッカー
    `govc <https://github.com/vmware/govmomi/tree/master/govc>`_
        govc は、govmomi に構築された vSphere CLI です。
    :ref:`working_with_playbooks`
        Playbook の概要

