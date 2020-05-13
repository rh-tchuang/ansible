CloudStack Cloud ガイド
======================

.. _cloudstack_introduction:

はじめに
````````````
本セクションの目的は、Ansible モジュールを 1 つにまとめて CloudStack コンテキストで Ansible を使用する方法を説明します。その他の使用例は、各モジュールの詳細セクションに記載されています。

Ansible には、CloudStack ベースのクラウドと対話するための追加モジュールが多数含まれています。すべてのモジュールは、チェックモードに対応しており、冪等であるように設計されています。これらは作成およびテストされており、コミュニティーによって維持されます。

.. note:: 一部のモジュールには、ドメイン管理または root 管理者権限が必要です。

要件
`````````````
CloudStack モジュールを使用する前提条件は最小限です。Ansible 自体に加えて、すべてのモジュールには python ライブラリー ``cs`` https://pypi.org/project/cs/ が必要です。

この Python モジュールは、実行ホスト (通常はワークステーション) にインストールする必要があります。

.. code-block:: bash

    $ pip install cs

もしくは、Debian 9 および Ubuntu 16.04 から始まります。

.. code-block:: bash

    $ sudo apt install python-cs

.. note:: cs には、CloudStack API などの、アドホックの対話用のコマンドラインインターフェースも含まれています (``$ cs listVirtualMachines state=Running``)。

制限および既知の問題
````````````````````````````
VPC のサポートは Ansible 2.3 以降で改善されましたが、まだ完全に実装されていません。コミュニティーは VPC 統合で機能しています。

認証情報ファイル
````````````````
認証情報とクラウドのエンドポイントをモジュール引数として渡すことができますが、ほとんどの場合、認証情報を cloudstack.ini ファイルに保存する作業ははるかに少なくなります。

Python ライブラリー cs は、以下の順番で認証情報ファイルを検索します (最後のコピーが優先されます)。

* ホームディレクトリーの ``.cloudstack.ini`` (ドットは必須)。
* .ini ファイルを参照する ``CLOUDSTACK_CONFIG`` 環境変数。
* 現在の作業ディレクトリーにある ``cloudstack.ini`` (ドットなし) ファイル (Playbook と同じディレクトリー)。

ini ファイルの構造は以下のようになります。

.. code-block:: bash

    $ cat $HOME/.cloudstack.ini
    [cloudstack]
    endpoint = https://cloud.example.com/client/api
    key = api key
    secret = api secret
    timeout = 30
    
.. Note:: セクション ``[cloudstack]`` はデフォルトのセクションです。``CLOUDSTACK_REGION`` 環境変数を使用してデフォルトのセクションを定義できます。

バージョン 2.4 における新機能

ENV 変数は、ライブラリー ``cs`` のドキュメントに記載されている ``CLOUDSTACK_*`` に対応します。たとえば、``CLOUDSTACK_TIMEOUT``、``CLOUDSTACK_METHOD`` などが Ansible に実装されています。cloudstack.ini に不完全な設定を設定することも可能です。

.. code-block:: bash

    $ cat $HOME/.cloudstack.ini
    [cloudstack]
    endpoint = https://cloud.example.com/client/api
    timeout = 30
    
ENV 変数または task パラメーターを設定して、不足しているデータに対応します。

.. code-block:: yaml

    ---
    - name: provision our VMs
      hosts: cloud-vm
      tasks:
        - name: ensure VMs are created and running
          delegate_to: localhost
          cs_instance:
            api_key: your api key
            api_secret: your api secret
            ...

リージョン
```````
複数の CloudStack リージョンを使用する場合は、必要な数だけセクションを定義し、任意の名前を付けることができます。以下に例を示します。

.. code-block:: bash

    $ cat $HOME/.cloudstack.ini
    [exoscale]
    endpoint = https://api.exoscale.ch/compute
    key = api key
    secret = api secret

    [example_cloud_one]
    endpoint = https://cloud-one.example.com/client/api
    key = api key
    secret = api secret

    [example_cloud_two]
    endpoint = https://cloud-two.example.com/client/api
    key = api key
    secret = api secret
    
.. Hint:: セクションは、異なるアカウントを使用して同じリージョンにログインするためにも使用できます。

引数 ``api_region`` を CloudStack モジュールに渡すと、必要なリージョンが選択されます。

.. code-block:: yaml

    - name: ensure my ssh public key exists on Exoscale
      cs_sshkeypair:
        name: my-ssh-key
        public_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
        api_region: exoscale
      delegate_to: localhost

または、すべてのリージョンでタスクを実行する場合は、リージョンリストをループします。

.. code-block:: yaml

    - name: ensure my ssh public key exists in all CloudStack regions
      local_action: cs_sshkeypair
        name: my-ssh-key
        public_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
        api_region: "{{ item }}"
        loop:
          - exoscale
          - example_cloud_one
          - example_cloud_two
    
環境変数
`````````````````````
バージョン 2.3 における新機能

Ansible 2.3 以降、ドメイン (``CLOUDSTACK_DOMAIN``)、アカウント (``CLOUDSTACK_ACCOUNT``)、プロジェクト (``CLOUDSTACK_PROJECT``)、VPC (``CLOUDSTACK_VPC``)、およびゾーン (``CLOUDSTACK_ZONE``) に環境変数を使用できます。これにより、すべてのタスクの引数が繰り返し実行されず、タスクが簡素化されます。

以下は、Ansible のブロック機能と組み合わせて使用する例を示しています。

.. code-block:: yaml

    - hosts: cloud-vm
      tasks:
        - block:
            - name: ensure my ssh public key
              cs_sshkeypair:
                name: my-ssh-key
                public_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

            - name: ensure my ssh public key
              cs_instance:
                  display_name: "{{ inventory_hostname_short }}"
                  template: Linux Debian 7 64-bit 20GB Disk
                  service_offering: "{{ cs_offering }}"
                  ssh_key: my-ssh-key
                  state: running

          delegate_to: localhost
          environment:
            CLOUDSTACK_DOMAIN: root/customers
            CLOUDSTACK_PROJECT: web-app
            CLOUDSTACK_ZONE: sf-1

.. Note:: モジュール引数 (例: ``zone: sf-2``) を使用して環境変数を上書きすることは可能です。

.. Note:: ``CLOUDSTACK_REGION`` とは異なり、この追加の環境変数は CLI ``cs`` では無視されます。

ユースケース
`````````
以下は、モジュールを使用して仮想マシンをクラウドにプロビジョニングする方法を示すものです。通常と同様に、これを行う方法は 1 つだけではありません。しかし、いつものように、最初はシンプルに保つことは、常に良いスタートです。

ユースケース: Advanced Networking CloudStack 設定のプロビジョニング
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
CloudStack クラウドには高度なネットワーク設定があり、静的な NAT を取得し、ファイアウォールポート 80 および 443 を開く Web サーバーをプロビジョニングを行います。さらに、アクセスを提供しないデータベースサーバーをプロビジョニングします。SSH で仮想マシンにアクセスするには、SSH ジャンプホストを使用します。

インベントリーは以下のようになります。

.. code-block:: none

    [cloud-vm:children]
    webserver
    db-server
    jumphost

    [webserver]
    web-01.example.com  public_ip=198.51.100.20
    web-02.example.com  public_ip=198.51.100.21

    [db-server]
    db-01.example.com
    db-02.example.com

    [jumphost]
    jump.example.com  public_ip=198.51.100.22

ご覧のとおり、Web サーバーおよびジャンプホストのパブリック IP は、インベントリーで直接変数 ``public_ip`` として割り当てられます。

ジャンプホスト、Web サーバー、およびデータベースサーバーを設定し、``group_vars`` を使用します。``group_vars`` ディレクトリーには、cloud-vm、jumphost、webserver、db-server の 4 つのファイルが含まれています。クラウドインフラストラクチャーのデフォルトを指定する cloud-vm があります。

.. code-block:: yaml

    # file: group_vars/cloud-vm
    ---
    cs_offering: Small
    cs_firewall: []
    
データベースサーバーはより多くの CPU および RAM を取得する必要があるため、``Large`` オファリングを使用するように定義します。

.. code-block:: yaml

    # file: group_vars/db-server
    ---
    cs_offering: Large

Web サーバーは、水平的にスケーリングするのと同様に、``Small`` オファリングを取得します。これはデフォルトのオファリングです。また、既知の Web ポートがグローバルに開いていることを確認します。

.. code-block:: yaml

    # file: group_vars/webserver
    ---
    cs_firewall:
      - { port: 80 }
      - { port: 443 }

さらに、オフィス IPv4 ネットワークから仮想マシンにアクセスするためにポート 22 のみを開くジャンプホストをプロビジョニングします。

.. code-block:: yaml

    # file: group_vars/jumphost
    ---
    cs_firewall:
      - { port: 22, cidr: "17.17.17.0/24" }

ここからが重要です。Playbook を作成して、``infra.yml`` を呼び出すインフラストラクチャーを作成します。

.. code-block:: yaml

    # file: infra.yaml
    ---
    - name: provision our VMs
      hosts: cloud-vm
      tasks:
        - name: run all enclosed tasks from localhost
          delegate_to: localhost
          block:
            - name: ensure VMs are created and running
              cs_instance:
                name: "{{ inventory_hostname_short }}"
                template: Linux Debian 7 64-bit 20GB Disk
                service_offering: "{{ cs_offering }}"
                state: running

            - name: ensure firewall ports opened
              cs_firewall:
                ip_address: "{{ public_ip }}"
                port: "{{ item.port }}"
                cidr: "{{ item.cidr | default('0.0.0.0/0') }}"
              loop: "{{ cs_firewall }}"
              when: public_ip is defined

            - name: ensure static NATs
              cs_staticnat: vm="{{ inventory_hostname_short }}" ip_address="{{ public_ip }}"
              when: public_ip is defined

上記のプレイでは、3 つのタスクを定義し、グループの ``cloud-vm`` をターゲットとして使用し、クラウド内の仮想マシンをすべて処理しますが、代わりにこれらの仮想マシンに SSH を使用するため、``delegate_to: localhost`` を使用してワークステーションからローカルに API 呼び出しを実行します。

最初のタスクでは、実行中の仮想マシンが Debian テンプレートを使用して作成されていることを確認します。仮想マシンがすでに作成されており、停止している場合は、これを起動します。既存の仮想マシンでオファリングを変更する場合は、タスクに ``force: yes`` を追加する必要があります。これにより、仮想マシンが停止し、オファリングを変更して仮想マシンを再度起動します。

次のタスクでは、仮想マシンにパブリック IP を付与した場合にポートを開くようにします。

3 番目のタスクでは、パブリック IP が定義されている仮想マシンに静的 NAT を追加します。


.. Note:: パブリック IP アドレスは事前に取得している必要があります。``cs_ip_address`` も参照してください。

.. Note:: 一部のモジュール (``cs_sshkeypair`` など）の場合、これはすべての仮想マシンに対してではなく、通常 1 回のみ実行するようにします。そのため、ローカルホストをターゲットとする別のプレイを作成します。以下のユースケースの例があります。

ユースケース: Basic Networking CloudStack 設定へのプロビジョニング
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

基本的なネットワーク CloudStack 設定は若干異なります。すべての仮想マシンにはパブリック IP が直接割り当てられ、セキュリティーグループはアクセス制限ポリシーに使用されます。

インベントリーは以下のようになります。

.. code-block:: none

    [cloud-vm:children]
    webserver

    [webserver]
    web-01.example.com
    web-02.example.com

仮想マシンのデフォルトは以下のようになります。

.. code-block:: yaml

    # file: group_vars/cloud-vm
    ---
    cs_offering: Small
    cs_securitygroups: [ 'default']
    
また、Web サーバーはセキュリティーグループ ``Web`` にも存在します。

.. code-block:: yaml

    # file: group_vars/webserver
    ---
    cs_securitygroups: [ 'default', 'web' ]
    
Playbook は以下のようになります。

.. code-block:: yaml

    # file: infra.yaml
    ---
    - name: cloud base setup
      hosts: localhost
      tasks:
      - name: upload ssh public key
        cs_sshkeypair:
          name: defaultkey
          public_key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

      - name: ensure security groups exist
        cs_securitygroup:
          name: "{{ item }}"
        loop:
          - default
          - web

      - name: add inbound SSH to security group default
        cs_securitygroup_rule:
          security_group: default
          start_port: "{{ item }}"
          end_port: "{{ item }}"
        loop:
          - 22

      - name: add inbound TCP rules to security group web
        cs_securitygroup_rule:
          security_group: web
          start_port: "{{ item }}"
          end_port: "{{ item }}"
        loop:
          - 80
          - 443

    - name: install VMs in the cloud
      hosts: cloud-vm
      tasks:
      - delegate_to: localhost
        block:
        - name: create and run VMs on CloudStack
          cs_instance:
            name: "{{ inventory_hostname_short }}"
            template: Linux Debian 7 64-bit 20GB Disk
            service_offering: "{{ cs_offering }}"
            security_groups: "{{ cs_securitygroups }}"
            ssh_key: defaultkey
            state: Running
          register: vm

        - name: show VM IP
          debug: msg="VM {{ inventory_hostname }} {{ vm.default_ip }}"

        - name: assign IP to the inventory
          set_fact: ansible_ssh_host={{ vm.default_ip }}

        - name: waiting for SSH to come up
          wait_for: port=22 host={{ vm.default_ip }} delay=5

最初のプレイでは、セキュリティーグループを設定し、次のプレイで、作成される仮想マシンがこれらのグループに割り当てられます。さらに、モジュールから返されたパブリック IP をホストインベントリーに割り当てることが確認できます。これは、事前に取得している IP が分からないため必要になります。次の手順では、この IP を使用して DNS サーバーを設定し、DNS 名を使用して仮想マシンにアクセスします。

最後のタスクでは、SSH がアクセス可能になるのを待ちます。したがって、後でプレイしても、SSH で仮想マシンにアクセスする際に失敗せずに実行できます。
