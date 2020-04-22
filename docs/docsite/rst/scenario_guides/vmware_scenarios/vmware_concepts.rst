.. \_vmware\_concepts:

***************************
Ansible for VMware の概念
***************************

この概念の一部は、VMware の自動化を含む Ansible のすべての用途に共通します。VMware に固有の概念もあります。VMWare の自動化に Ansible を活用するには、この概念を理解しておく必要があります。この概要では、本ガイドの :ref:`シナリオ<vmware_scenarios>` に従う必要がある背景を説明します。

.. contents::
   :local:

コントロールノード
============

Ansible がインストールされているマシン。``/usr/bin/ansible`` または ``/usr/bin/ansible-playbook`` を任意のコントロールノードから起動して、コマンドと Playbook を実行できます。Python がインストールされたコンピューターは、コントロールノード (ノートパソコン、共有デスクトップ、およびサーバーがすべて Ansible を実行) として使用できます。ただし、Windows マシンをコントロールノードとして使用することはできません。複数のコントロールノードを使用できます。

委譲
==========

委譲では、特定タスクを実行するシステムを選択できます。コントロールノードに ``pyVmomi`` がインストールされていない場合は、VMware 固有のタスクで ``delegate_to`` キーワードを使用して、``pyVmomi`` がインストールされているホストで特定タスクを実行します。

モジュール
=======

Ansible が実行するコード単位。各モジュールには、vCenter での仮想マシン作成から、vCenter 環境で分散型仮想スイッチの管理まで、特定の用途があります。タスクを使用して 1 つのモジュールを起動することも、Playbook で複数の異なるモジュールを呼び出すこともできます。Ansible に含まれるモジュール数を理解するには、VMware モジュールを含む :ref:`クラウドモジュールの一覧<cloud_modules>` を確認してください。

Playbook
=========

順序付けされたタスク一覧を保存し、このタスクを順番に繰り返し実行できるようにします。Playbook には、変数やタスクを追加できます。Playbook は YAML で記述され、読み取り、書き込み、共有、および理解が簡単にできます。

pyVmomi
=======

Ansible VMware モジュールは `pyVmomi <https://github.com/vmware/pyvmomi>`_ に記述されます。``pyVmomi`` は、ユーザーが ESX、ESXi、および vCenter インフラストラクチャーを管理できるようにする VMware vSphere API の公式の Python SDK です。

この Python SDK を、VMware 自動化を起動するホストからホストにインストールする必要があります。たとえば、コントロールノードを使用している場合は、``pyVmomi`` をコントロールノードにインストールする必要があります。

お使いのコントロールノードとは異なる ``delegate_to`` ホストを使用している場合は、その ``delegate_to`` ノードに ``pyVmomi`` をインストールする必要があります。

pip を使用して pyVmomi をインストールできます。

.. code-block:: bash

    $ pip install pyvmomi
