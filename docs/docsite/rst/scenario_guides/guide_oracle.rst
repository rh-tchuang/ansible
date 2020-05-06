===================================
Oracle Cloud Infrastructure ガイド
===================================

************
はじめに
************

Oracle 社は、Oracle Cloud Infrastructure (OCI) と対話するための Ansible モジュールを多数提供しています。本ガイドでは、そのモジュールを使用して、OCI でインフラストラクチャーをオーケストレーションし、プロビジョニングし、設定する方法を説明します。 

************
要件
************
OCI Ansible モジュールを使用するには、Ansible Playbook を実行するコンピューターのコントロールノードに、以下の前提条件を設定する必要があります。

1. `Oracle Cloud Infrastructure アカウント <https://cloud.oracle.com/en_US/tryit>`_

2. それらのコンパートメント内のリソースを操作するために必要なパーミッションを付与するポリシーを持つセキュリティグループで、そのアカウントで作成されたユーザー。詳細は「`ポリシーの仕組み <https://docs.cloud.oracle.com/iaas/Content/Identity/Concepts/policies.htm>`_」を参照してください。

3. 必要な認証情報と OCID 情報。

************
インストール
************ 
1. Oracle Cloud Infrastructure Python SDK をインストールします (`詳細なインストール手順 <https://oracle-cloud-infrastructure-python-sdk.readthedocs.io/en/latest/installation.html>`_)。

.. code-block:: bash

        pip install oci

2.  以下のいずれかの方法で Ansible OCI モジュールをインストールします。

a. 	Galaxy の場合: 

.. code-block:: bash

 ansible-galaxy install oracle.oci_ansible_modules

b. 	GitHub の場合:

.. code-block:: bash

     $ git clone https://github.com/oracle/oci-ansible-modules.git

.. code-block:: bash

    $ cd oci-ansible-modules


以下のコマンドのいずれかを実行します。

- Ansible をお使いのユーザーにのみインストールする場合は、以下を実行します。 

.. code-block:: bash

    $ ./install.py

- Ansible を root でインストールする場合は、以下を実行します。 

.. code-block:: bash

    $ sudo ./install.py

*************
構成
*************

Oracle Cloud Infrastructure リソースを作成して設定する際に、Ansible モジュールは `こちら <https://docs.cloud.oracle.com/iaas/Content/API/Concepts/sdkconfig.htm>`_ で説明されている認証情報を使用します。

 
********
例
********
コンピュートインスタンスの起動
=========================
この `sample launch playbook <https://github.com/oracle/oci-ansible-modules/tree/master/samples/compute/launch_compute_instance>`_ は、
パブリックのコンピュートインスタンスを起動し、SSH 接続を経由して Ansible モジュールからインスタンスにアクセスします。このサンプルは、以下を実行する方法を示しています。

- 一時的なホスト固有の SSH キーペアを生成します。
- インスタンスへの接続に使用するキーペアの公開鍵を指定し、インスタンスを起動します。
- SSH を使用して、新たに起動したインスタンスに接続します。

Autonomous Data Warehouse の作成および管理
============================================
この `sample warehouse playbook <https://github.com/oracle/oci-ansible-modules/tree/master/samples/database/autonomous_data_warehouse>`_ は、Autonomous Data Warehouse (自立型データウェアハウス) を作成して、そのライフサイクルを管理します。このサンプルは、以下を実行する方法を示しています。

- Autonomous Data Warehouse. を設定します。
- 表示名で対象を絞った、コンパートメントで利用可能な Autonomous Data Warehouse を一覧表示します。
- 指定された Autonomous Data Warehouse の「ファクト」を取得します。
- Autonomous Data Warehouse インスタンスを停止して開始します。
- Autonomous Data Warehouse インスタンスを削除します。

Autonomous Transaction Processing の作成と管理
===================================================
この `sample playbook <https://github.com/oracle/oci-ansible-modules/tree/master/samples/database/autonomous_database>`_ は、
Autonomous Transaction Processing (自律型トランザクション処理) データベースを作成し、そのライフサイクルを管理します。このサンプルは、以下を実行する方法を示しています。

- Autonomous Transaction Processing データベースインスタンスを設定します。
- 表示名で対象を絞った、コンパートメントで利用可能な Autonomous Transaction Processing を一覧表示します。
- 指定された Autonomous Transaction Processing インスタンスの「ファクト」を取得します。
- Autonomous Transaction Processing データベースインスタンスを削除します。

詳細: `Ansible Playbook のサンプル <https://docs.cloud.oracle.com/iaas/Content/API/SDKDocs/ansiblesamples.htm>`_.
