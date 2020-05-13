Google Cloud Platform ガイド
===========================

.. gce_intro:

はじめに
--------------------------

Ansible および Google 社は、
Google Cloud Platform (GCP) 全体を一貫して包括的に対応するように設計された、
自動生成された一連の Ansible モジュールに共同で取り組んできました。

Ansible には、インスタンスの作成、ネットワークアクセスの制御、永続ディスクの操作、
ロードバランサーの管理など、
Google Cloud Platform リソースを管理するモジュールが含まれています。

この新しいモジュールは、一貫した新しい名前スキーム「gcp_*"」にあります。
(注記: 「gcp_*」名であっても、
gcp_target_proxy および gcp_url_map はレガシーモジュールです。代わりに gcp_compute_target_proxy および gcp_compute_url_map を使用してください。)

さらに、gcp_compute インベントリープラグインは、
すべての Google Compute Engine (GCE) インスタンスを検出し、
それらを Ansible インベントリーで自動的に利用できるようにします。

この命名規則に準拠していないその他の GCP モジュールのコレクションが
表示される場合があります。これは、
主に Ansible コミュニティーで開発されたオリジナルモジュールです。「gce」モジュール、
新しい「gcp_compute_instance」モジュールなど、重複する機能があります。どちらも使用できますが、
一緒に使用しようとすると問題が発生する場合があります。

コミュニティーの GCP モジュールは廃止されませんが、
Google 社は、新しい「gcp_*」モジュールに取り組んでいます。Google 社は、
Ansible コミュニティーが GCP で素晴らしい体験をすることを約束しているため、
可能であればこの新しいモジュールを採用することが推奨されます。


要件
---------------
GCP モジュールでは、``requests`` ライブラリーと
``google-auth`` ライブラリーの両方をインストールする必要があります。

.. code-block:: bash

    $ pip install requests google-auth

RHEL/CentOS では、
``requests`` ライブラリーの代わりに ``python-requests`` パッケージも利用できます。

.. code-block:: bash

    $ yum install python-requests

認証情報
-----------
Ansible の認証情報を使用して GCP アカウントを作成するのは簡単です。認証情報を取得するオプションは複数ありますが、
最も一般的なオプションは次の 2 つです。

* サービスアカウント (推奨) - 特定のパーミッションを持つ JSON サービスアカウントを使用します。
* マシンアカウント - Ansible を使用する GCP インスタンスに関連付けられたパーミッションを使用します。

以下の例では、サービスアカウントの認証情報を使用します。

GCP モジュールを使用するには、
最初に JSON 形式の認証情報を取得する必要があります。

1. `サービスアカウント作成する <https://developers.google.com/identity/protocols/OAuth2ServiceAccount#creatinganaccount>`_
2. `JSON 認証情報をダウンロードする <https://support.google.com/cloud/answer/6158849?hl=en&ref_topic=6262490#serviceaccounts>`_

認証情報を取得したあと、Ansible に提供する方法は 2 つあります。

* モジュールパラメーターとして直接指定する
* 追加の環境変数を設定する

認証情報をモジュールパラメーターとして指定
``````````````````````````````````````````

GCE モジュールでは、認証情報を引数として指定できます。

* ``auth_kind`` - 使用される認証のタイプ (選択肢は machineaccount、serviceaccount、application です)
* ``service_account_email`` - プロジェクトに関連付けられたメール
* ``service_account_file`` - JSON 認証情報ファイルへのパス
* ``project`` - プロジェクトの id
* ``scopes`` - アクションで使用する特定のスコープ

たとえば、``gcp_compute_address`` モジュールを使用して新規 IP アドレスを作成するには、以下を実行します。
以下の設定を使用できます。

.. code-block:: yaml

   - name: Create IP address
     hosts: localhost
     gather_facts: no

     vars:
       service_account_file: /home/my_account.json
       project: my-project
       auth_kind: serviceaccount
       scopes:
         - https://www.googleapis.com/auth/compute

     tasks:

      - name: Allocate an IP Address
        gcp_compute_address:
            state: present
            name: 'test-address1'
            region: 'us-west1'
            project: "{{ project }}"
            auth_kind: "{{ auth_kind }}"
            service_account_file: "{{ service_account_file }}"
            scopes: "{{ scopes }}"

認証情報を環境変数として指定
``````````````````````````````````````````````

認証情報を設定するために Ansible を実行する前に、以下の環境変数を設定します。

.. code-block:: bash

    GCP_AUTH_KIND
    GCP_SERVICE_ACCOUNT_EMAIL
    GCP_SERVICE_ACCOUNT_FILE
    GCP_SCOPES

GCE 動的インベントリー
---------------------

ホストと対話する最適な方法は、gcp_compute インベントリープラグインを使用することです。このプラグインは、GCE に動的にクエリーを送信し、管理できるノードを Ansible に通知します。

この GCE 動的インベントリープラグインを使用するには、最初に ``ansible.cfg`` ファイルに以下を指定して有効にする必要があります。

.. code-block:: ini

  [inventory]
  enable_plugins = gcp_compute

次に、root ディレクトリーに ``.gcp.yml`` で終わるファイルを作成します。

gcp_compute スクリプトは、モジュールと同じ認証情報を取得します。

以下は、有効なインベントリーファイルの例です。

.. code-block:: yaml

    plugin: gcp_compute
    projects:
      - graphite-playground
    auth_kind: serviceaccount
    service_account_file: /home/alexstephen/my_account.json


``ansible-inventory --list -i <filename>.gcp.yml`` を実行すると、Ansible を使用して設定する準備ができている GCP インスタンスの一覧が作成されます。

インスタンスグループの作成
``````````````````

すべての GCP モジュールは、GCP API 全体に完全に対応することで、
さまざまな GCP リソースを作成する機能を提供します。

以下の Playbook は GCE インスタンスを作成します。このインスタンスは、
GCP ネットワークとディスクに依存しています。ディスクとネットワークを別々に作成することにより、
ディスクとネットワークをどのようにフォーマットするかについて、詳細を必要なだけ提供できます。ディスク/ネットワークを
変数に登録することで、
変数をインスタンスタスクに簡単に挿入できます。gcp_compute_instance モジュールが、
残りの部分を理解します。

.. code-block:: yaml

   - name: Create an instance
     hosts: localhost
     gather_facts: no
     vars:
         gcp_project: my-project
         gcp_cred_kind: serviceaccount
         gcp_cred_file: /home/my_account.json
         zone: "us-central1-a"
         region: "us-central1"

     tasks:
      - name: create a disk
        gcp_compute_disk:
            name: 'disk-instance'
            size_gb: 50
            source_image: 'projects/ubuntu-os-cloud/global/images/family/ubuntu-1604-lts'
            zone: "{{ zone }}"
            project: "{{ gcp_project }}"
            auth_kind: "{{ gcp_cred_kind }}"
            service_account_file: "{{ gcp_cred_file }}"
            scopes:
              - https://www.googleapis.com/auth/compute
            state: present
        register: disk
      - name: create a network
        gcp_compute_network:
            name: 'network-instance'
            project: "{{ gcp_project }}"
            auth_kind: "{{ gcp_cred_kind }}"
            service_account_file: "{{ gcp_cred_file }}"
            scopes:
              - https://www.googleapis.com/auth/compute
            state: present
        register: network
      - name: create a address
        gcp_compute_address:
            name: 'address-instance'
            region: "{{ region }}"
            project: "{{ gcp_project }}"
            auth_kind: "{{ gcp_cred_kind }}"
            service_account_file: "{{ gcp_cred_file }}"
            scopes:
              - https://www.googleapis.com/auth/compute
            state: present
        register: address
      - name: create a instance
        gcp_compute_instance:
            state: present
            name: test-vm
            machine_type: n1-standard-1
            disks:
              - auto_delete: true
                boot: true
                source: "{{ disk }}"
            network_interfaces:
                - network: "{{ network }}"
                  access_configs:
                    - name: 'External NAT'
                      nat_ip: "{{ address }}"
                      type: 'ONE_TO_ONE_NAT'
            zone: "{{ zone }}"
            project: "{{ gcp_project }}"
            auth_kind: "{{ gcp_cred_kind }}"
            service_account_file: "{{ gcp_cred_file }}"
            scopes:
              - https://www.googleapis.com/auth/compute
        register: instance

       - name: Wait for SSH to come up
         wait_for: host={{ address.address }} port=22 delay=10 timeout=60

       - name: Add host to groupname
         add_host: hostname={{ address.address }} groupname=new_instances


   - name: Manage new instances
     hosts: new_instances
     connection: ssh
     sudo: True
     roles:
       - base_configuration
       - production_server

上記の「add_host」モジュールを使用すると、一時的なインメモリーグループが作成されることに注意してください。 つまり、必要に応じて、
同じ Playbook のプレイで「new_instances」グループのマシンを管理できます。 この時点では、任意の設定が可能です。

Google Cloud の詳細は、「`Google Cloud の Web サイト <https://cloud.google.com>`_」を参照してください。

移行ガイド
----------------

gce.py -> gcp_compute_instance.py
`````````````````````````````````
Ansible 2.8 からは、すべてのユーザーに、``gce`` モジュールから
``gcp_compute_instance`` モジュールに移行することを推奨しています。``gcp_compute_instance`` モジュールは、GCP のすべての機能への対応がより適切で、
依存関係を減らし、柔軟性を高め、
GCP の認証システムへの対応がより適切になります。

``gcp_compute_instance`` モジュールは、``gce`` モジュール (およびその他) 
のすべての機能に対応します、以下は、``gce`` フィールドから、
``gcp_compute_instance`` フィールドへのマッピングとなります。

============================  ==========================================  ======================
 gce.py                        gcp_compute_instance.py                     注記
============================  ==========================================  ======================
 state                        state/status                                gce の state には複数の値 (「present」、「absent」、「stopped」、「started」、「terminated」) が含まれます。gcp_compute_instance の state を使用して、インスタンスが存在する (present) か、存在しない (absent) かを記述します。Status は、インスタンスが「起動」、「停止」、または「終了」であるかを説明するのに使用されます。
 image                        disks[].initialize_params.source_image      disks[] パラメーターを使用してディスクを 1 つ作成し、それをブートディスクに設定する必要があります (disks[].boot = true)。
 image_family                 disks[].initialize_params.source_image      上記を参照。
 external_projects            disks[].initialize_params.source_image      source_image の名前には、プロジェクトの名前が含まれます。
 instance_names               ループまたは複数のタスクを使用します。              ループの使用は、複数のインスタンスを作成するよりも Ansible に適した方法で、柔軟性が最も高くなります。
 service_account_email        service_accounts[].email                    これは、インスタンスを関連付ける service_account メールアドレスです。これは、インスタンスの作成に必要な認証情報に使用される service_account メールアドレスではありません。
 service_account_permissions  service_accounts[].scopes                   インスタンスに付与するパーミッションです。
 pem_file                     対応していません。                             PEM ファイルの代わりに JSON サービスアカウントの認証情報を使用することが推奨されます。
 credentials_file             service_account_file
 project_id                   project
 name                         name                                        このフィールドでは名前の配列を使用できません。ループを使用して複数のインスタンスを作成します。
 num_instances                ループを使用します。                                  柔軟性を最大にするために、モジュールではなく、Ansible の機能を使用して複数のインスタンスを作成することが推奨されます。
 network                      network_interfaces[].network
 subnetwork                   network_interfaces[].subnetwork
 persistent_boot_disk         disks[].type = 'PERSISTENT'
 disks                        disks[]
 ip_forward                   can_ip_forward
 external_ip                  network_interfaces[].access_configs.nat_ip  このフィールドは、複数のタイプの値を取ります。``gcp_compute_address`` で IP アドレスを作成し、ここにアドレスの名前/出力を指定できます。IP アドレスの GCP 名または実際の IP アドレスの文字列値を指定することもできます。
 disks_auto_delete            disks[].auto_delete
 preemptible                  scheduling.preemptible
 disk_size                    disks[].initialize_params.disk_size_gb
============================  ==========================================  ======================

Playbook の例を以下に示します。

.. code:: yaml

  gcp_compute_instance:
      name: "{{ item }}"
      machine_type: n1-standard-1
      ... # any other settings
      zone: us-central1-a
      project: "my-project"
      auth_kind: "service_account_file"
      service_account_file: "~/my_account.json"
      state: present
  with_items:
    - instance-1
    - instance-2
