Alibaba Cloud コンピュートサービスガイド
====================================

.. _alicloud_intro:

はじめに
````````````

Ansible には、Alibaba Cloud Compute Services (Alicloud) を制御および管理するためのモジュールが複数含まれています。 本ガイドでは、
Alicloud Ansible モジュールを一緒に使用する方法を説明します。

すべての Alicloud モジュールには ``footmark`` - が必要です。これは、``pip install footmark`` で、コントロールマシンにインストールします。

Alicloud モジュールを含むクラウドモジュールは、ホストに定義されたリモートマシンではなく、ローカルマシン (コントロールマシン) で、``connection: local`` を使用して実行します。

通常、Alicloud リソースをプロビジョニングするプレイには次のパターンを使用します::

    - hosts: localhost
      connection: local
      vars:
        - ...
      tasks:
        - ...

.. _alicloud_authentication:

認証
``````````````

Alicloud の認証情報 (アクセスキーおよびシークレットキー) を指定するには、その認証情報を環境変数として渡すか、
vars ファイルに保存します。

環境変数として認証情報を渡すには、以下を実行します::

    export ALICLOUD_ACCESS_KEY='Alicloud123'
    export ALICLOUD_SECRET_KEY='AlicloudSecret123'

認証情報を vars_file に保存するには、:ref:`Ansible Vault<vault>` で認証情報を暗号化してセキュアに維持してから、その認証情報の一覧を表示します::

    ---
    alicloud_access_key: "--REMOVED--"
    alicloud_secret_key: "--REMOVED--"

認証情報を vars_file に保存する場合は、各 Alicloud モジュールで認証情報を参照する必要があることに注意してください。例::

    - ali_instance:
        alicloud_access_key: "{{alicloud_access_key}}"
        alicloud_secret_key: "{{alicloud_secret_key}}"
        image_id: "..."
    
.. _alicloud_provisioning:

プロビジョニング
````````````

Alicloud モジュールは、Alicloud ECS インスタンス、ディスク、仮想プライベートクラウド、仮想スイッチ、セキュリティーグループ、およびその他のリソースを作成します。

``count`` パラメーターを使用して、作成または終了するリソースの数を制御できます。たとえば、``NewECS`` のタグが付けられた 5 つのインスタンスが必要な場合は、
以下のサンプル Playbook の 最後のタスクで説明されているように、インスタンスの ``count`` を 5 に設定し、``count_tag`` を ``NewECS`` に設定します。
タグ ``NewECS`` を持つインスタンスがない場合、タスクは新規インスタンスを 5 つ作成します。そのタグを持つインスタンスが 2 個ある場合、
タスクはさらに 3 個作成します。このタグを持つインスタンスが 8 個ある場合、タスクはそのうちの 3 つのインスタンスを終了します。

``count_tag`` を指定しないと、システムは、指定した ``instance_name`` で ``count`` に指定したインスタンスの数を作成します。

::

    # alicloud_setup.yml

    - hosts: localhost
      connection: local

      tasks:

        - name: Create VPC
          ali_vpc:
            cidr_block: '{{ cidr_block }}'
            vpc_name: new_vpc
          register: created_vpc

        - name: Create VSwitch
          ali_vswitch:
            alicloud_zone: '{{ alicloud_zone }}'
            cidr_block: '{{ vsw_cidr }}'
            vswitch_name: new_vswitch
            vpc_id: '{{ created_vpc.vpc.id }}'
          register: created_vsw

        - name: Create security group
          ali_security_group:
            name: new_group
            vpc_id: '{{ created_vpc.vpc.id }}'
            rules:
              - proto: tcp
                port_range: 22/22
                cidr_ip: 0.0.0.0/0
                priority: 1
            rules_egress:
              - proto: tcp
                port_range: 80/80
                cidr_ip: 192.168.0.54/32
                priority: 1
          register: created_group

        - name: Create a set of instances
          ali_instance:
             security_groups: '{{ created_group.group_id }}'
             instance_type: ecs.n4.small
             image_id: "{{ ami_id }}"
             instance_name: "My-new-instance"
             instance_tags:
                 Name: NewECS
                 Version: 0.0.1
             count: 5
             count_tag:
                 Name: NewECS
             allocate_public_ip: true
             max_bandwidth_out: 50
             vswitch_id: '{{ created_vsw.vswitch.id}}'
          register: create_instance

上記のサンプル Playbook では、この Playbook で作成される vpc、vswitch、group、およびインスタンスに関するデータは、
各タスクの「register」キーワードで定義される変数に保存されます。

各 Alicloud モジュールは、さまざまなパラメーターオプションを提供します。上記の例で、すべてのオプションが示されているわけではありません。
詳細およびサンプルは、各モジュールを参照してください。
