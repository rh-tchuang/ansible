Rackspace Cloud ガイド
=====================

.. _rax_introduction:

はじめに
````````````

.. note:: 本ガイドの本セクションは作成中です。Rackspace モジュールと、そのモジュールがどのように連携するかについて、サンプルをさらに追加している最中です。 完了したら、`ansible-examples <https://github.com/ansible/ansible-examples/>`_ に Rackspace Cloud のサンプルが含まれます。

Ansible には、Rackspace Cloud と対話するためのコアモジュールが多数含まれています。  

このセクションは、Ansibleモジュールを組み合わせ (およびインベントリースクリプトを使用し) て、
Rackspace Cloud コンテキストで Ansible を使用する方法を説明することを目的としています。

rax モジュールを使用する前提条件は最小限です。 Ansible 自体に加えて、
すべてのモジュールは pyrax 1.5 以上を必要とし、テストされています。
この Python モジュールは、実行ホストにインストールする必要があります。  

``pyrax`` は、現在、多くのオペレーティングシステムパッケージリポジトリーで利用できないため、
pip を使用してインストールする必要がある可能性があります。

.. code-block:: bash

    $ pip install pyrax

Ansible は、``ansible-playbook`` およびその他の CLI ツールと同じコンテキストで実行される暗黙的なローカルホストを作成します。
なんらかの理由で、またはインベントリーに保存する必要があるまたは保存したい場合には、以下のような作業を行う必要があります。

.. code-block:: ini

    [localhost]
    localhost ansible_connection=local ansible_python_interpreter=/usr/local/bin/python2

詳細は「:ref:`暗黙的なローカルホスト<implicit_localhost>`」を参照してください。

Playbook ステップでは、通常、以下のパターンを使用します。

.. code-block:: yaml

    - hosts: localhost
      gather_facts:False
      tasks:

.. _credentials_file:

認証情報ファイル
````````````````

`rax.py` インベントリースクリプトと、すべての `rax` モジュールは、以下のような標準の `pyrax` 認証情報ファイルに対応します。

.. code-block:: ini

    [rackspace_cloud]
    username = myraxusername
    api_key = d41d8cd98f00b204e9800998ecf8427e

環境パラメーター ``RAX_CREDS_FILE`` をこのファイルのパスに設定すると、
Ansible は、この情報を読み込む方法を見つけるのに役に立ちます。

この認証情報ファイルに関する詳細情報: 
https://github.com/pycontribs/pyrax/blob/master/docs/getting_started.md#authenticating


.. _virtual_environment:

Python 仮想環境からの実行 (オプション)
++++++++++++++++++++++++++++++++++++++++++++++++++++

ほとんどのユーザーは virtualenv を使用しませんが、一部のユーザー、特に Python の開発者はそれを使用する場合があります。

Ansible が Python virtualenv にインストールされる場合には、デフォルトのグローバルスコープでのインストールではなく、特別な考慮事項があります。Ansible は、特に指示がない限り、python バイナリーが /usr/bin/python にあることを前提としています。 これは、モジュールのインタープリターの行を使用して行われますが、インベントリー変数「ansible_python_interpreter」を設定して指示すると、Ansible は Python の検索の代わりに、この指定されたパスを使用します。 これは、「localhost」で実行しているモジュール、または「local_action」で実行されるモジュールが virtualenv Python インタープリターを使用していると仮定するため、混乱が生じる可能性があります。 この行をインベントリーに設定すると、モジュールは virtualenv インタープリターで実行され、virtualenv パッケージ (具体的には pyrax) が利用できるようになります。virtualenv を使用している場合は、以下のように、この場所が検出されるように、localhost インベントリー定義を変更します。

.. code-block:: ini

    [localhost]
    localhost ansible_connection=local ansible_python_interpreter=/path/to/ansible_venv/bin/python

.. note::

    pyrax は、グローバルの Python パッケージスコープまたは仮想環境にインストールできます。 pyrax をインストールする際には、特別な留意事項はありません。

.. _provisioning:

プロビジョニング
````````````



「rax」モジュールは、Rackspace Cloud 内でインスタンスをプロビジョニングする機能を提供します。 通常、プロビジョニングタスクは、Rackspace cloud API に対して Ansible コントロールサーバー (この例ではローカルホスト) から実行されます。 これにはいくつかの理由があります。

    - リモートノードに pyrax ライブラリーをインストールしないようにする
    - 認証情報を暗号化してリモートノードに配布する必要はない
    - スピードと単純化

.. note::

   Rackspace 関連のモジュールを使用した認証は、
   ユーザー名と API キーを環境変数として指定するか、
   モジュールの引数として渡すか、
   認証情報ファイルの場所を指定することで処理されます。

以下は、アドホックモードでのインスタンスをプロビジョニングする基本的な例です。

.. code-block:: bash

    $ ansible localhost -m rax -a "name=awx flavor=4 image=ubuntu-1204-lts-precise-pangolin wait=yes"

以下は、パラメーターが変数に定義されていると仮定した場合の、Playbook で表示される内容です。

.. code-block:: yaml

    tasks:
      - name:Provision a set of instances
        rax:
            name: "{{ rax_name }}"
        flavor: "{{ rax_flavor }}"
        image: "{{ rax_image }}"
        count: "{{ rax_count }}"
        group: "{{ group }}"
            wait: yes
        register: rax
        delegate_to: localhost
    
rax モジュールは、IP アドレス、ホスト名、ログインパスワードなど、作成するノードのデータを返します。 ステップの戻り値を登録すると、このデータを使用して、作成されるホストをインベントリー (通常はメモリー内) に動的に追加できます。これにより、後続のタスクによるホストでの設定アクションの実行が容易になります。 以下の例では、上記のタスクを使用して正常に作成されたサーバーは「raxhosts」というグループに動的に追加され、各ノードのホスト名、IP アドレス、および root パスワードがインベントリーに追加されます。

.. code-block:: yaml

    - name:Add the instances we created (by public IP) to the group 'raxhosts'
      add_host:
          hostname: "{{ item.name }}"
      ansible_host: "{{ item.rax_accessipv4 }}"
      ansible_password: "{{ item.rax_adminpass }}"
      groups: raxhosts
  loop: "{{ rax.success }}"
      when: rax.action == 'create'
    
これでホストグループが作成され、この Playbook の次のプレイで raxhosts グループに属するサーバーを設定できるようになりました。

.. code-block:: yaml

    - name:Configuration play
      hosts: raxhosts
      user: root
      roles:
        - ntp
        - webserver

上記の方法は、ホストの設定と、プロビジョニング手順を関連付けます。 これは常に必要なことではなく、
次のセクションに進みます。

.. _host_inventory:

ホストインベントリー
``````````````

ノードが起動したら、おそらく再度通信するようにしたいでしょう。 これを処理する最善の方法は、「rax」インベントリープラグインを使用することです。これは、Rackspace Cloud に動的にクエリーを実行し、管理する必要があるノードを Ansible に通知します。 これは、別のツール (Rackspace Cloud ユーザーインターフェースなど) を介してクラウドインスタンスを起動している場合であっても使用することができます。インベントリープラグインは、リソースをメタデータ、リージョン、OS などでまとめるのに使用できます。 メタデータの使用は「rax」で強く推奨され、ホストグループとロールとの間で簡単に並べ替えることができます。動的インベントリースクリプト ``rax.py`` を使用しない場合は、INI インベントリーファイルを手動で管理することもできますが、これは推奨されていません。

Ansible では、INI ファイルデータとともに複数の動的インベントリープラグインを使用できます。 単にそれらを共通のディレクトリーに配置し、スクリプトが chmod +x で、INI ベースのディレクトリーではないことを確認します。

.. _raxpy:

rax.py
++++++

Rackspace 動的インベントリースクリプトを使用するには、``rax.py`` をインベントリーディレクトリーにコピーして、実行可能にします。``RAX_CREDS_FILE`` 環境変数を使用して、``rax.py`` の認証情報ファイルを指定できます。

.. note:: 動的インベントリースクリプト (``rax.py`` など) は、Ansible がグローバルにインストールされている場合は、``/usr/share/ansible/inventory`` に保存されます。 virtualenv にインストールされている場合、インベントリースクリプトは ``$VIRTUALENV/share/inventory`` にインストールされます。

.. note:: :ref:`ansible_tower` のユーザーは、Tower が動的インベントリーをネイティブにサポートしており、グループを Rackspace Cloud 認証情報に関連付けるだけで、このステップを実行せずに簡単に同期できます。

    $ RAX_CREDS_FILE=~/.raxpub ansible all -i rax.py -m setup

``rax.py`` は、個別のリージョンまたはコンマ区切りのリージョン一覧を指定できる ``RAX_REGION`` 環境変数も受け入れます。

``rax.py`` を使用する場合は、インベントリーに「localhost」を定義しません。  

前述のように、ほとんどのモジュールはホストループの外部で実行されることが多く、「localhost」を定義する必要があります。 これを行うには、``inventory`` ディレクトリーを作成し、``rax.py`` スクリプトと、``localhost`` を含むファイルの両方をそのディレクトリーに置くことが推奨されます。

``ansible`` または ``ansible-playbook`` を実行し、個々のファイルの代わりに、``inventory`` ディレクトリーを指定すると、
Ansible がそのディレクトリー内の各ファイルをインベントリー用に評価します。

インベントリースクリプトをテストし、Rackspace Cloud と通信できるかどうかを確認します。

.. code-block:: bash

    $ RAX_CREDS_FILE=~/.raxpub ansible all -i inventory/ -m setup

適切に設定されていると仮定すると、``rax.py`` インベントリースクリプトは、以下のような情報を出力します。
これは、インベントリーおよび変数に使用されます。 

.. code-block:: json

    {
        "ORD": [
        "test"
    ],
        "_meta": {
            "hostvars": {
                "test": {
                    "ansible_host":"198.51.100.1",
                    "rax_accessipv4":"198.51.100.1",
                    "rax_accessipv6":"2001:DB8::2342",
                    "rax_addresses": {
                        "private": [
                        {
                            "addr": "192.0.2.2",
                            "version": 4
                        }
                    ],
                        "public": [
                        {
                            "addr": "198.51.100.1",
                            "version": 4
                        },
                        {
                            "addr": "2001:DB8::2342",
                            "version": 6
                        }
                    ]
                    },
                    "rax_config_drive": "",
                    "rax_created":"2013-11-14T20:48:22Z",
                    "rax_flavor": {
                        "id": "performance1-1",
                        "links": [
                        {
                            "href": "https://ord.servers.api.rackspacecloud.com/111111/flavors/performance1-1",
                            "rel": "bookmark"
                        }
                    ]
                    },
                    "rax_hostid": "e7b6961a9bd943ee82b13816426f1563bfda6846aad84d52af45a4904660cde0",
                    "rax_human_id": "test",
                    "rax_id":"099a447b-a644-471f-87b9-a7f580eb0c2a",
                    "rax_image": {
                        "id": "b211c7bf-b5b4-4ede-a8de-a4368750c653",
                        "links": [
                        {
                            "href": "https://ord.servers.api.rackspacecloud.com/111111/images/b211c7bf-b5b4-4ede-a8de-a4368750c653",
                            "rel": "bookmark"
                        }
                    ]
                    },
                    "rax_key_name": null,
                    "rax_links": [
                    {
                        "href": "https://ord.servers.api.rackspacecloud.com/v2/111111/servers/099a447b-a644-471f-87b9-a7f580eb0c2a",
                        "rel": "self"
                    },
                    {
                        "href": "https://ord.servers.api.rackspacecloud.com/111111/servers/099a447b-a644-471f-87b9-a7f580eb0c2a",
                        "rel": "bookmark"
                    }
                ],
                    "rax_metadata": {
                        "foo": "bar"
                    },
                    "rax_name": "test",
                    "rax_name_attr": "name",
                    "rax_networks": {
                        "private": [
                        "192.0.2.2"
                    ],
                        "public": [
                        "198.51.100.1",
                        "2001:DB8::2342"
                    ]
                    },
                    "rax_os-dcf_diskconfig":"AUTO",
                    "rax_os-ext-sts_power_state":1,
                    "rax_os-ext-sts_task_state": null,
                    "rax_os-ext-sts_vm_state": "active",
                    "rax_progress":100,
                    "rax_status":"ACTIVE",
                    "rax_tenant_id":"111111",
                    "rax_updated":"2013-11-14T20:49:27Z",
                    "rax_user_id":"22222"
                }
            }
        }
    }
    
.. _standard_inventory:

標準インベントリー
++++++++++++++++++

(インベントリープラグインではなく) 標準の ini 形式のインベントリーファイルを使用する場合でも、検出可能な hostvar 情報を Rackspace API から取得すると有効な場合があります。

これは、``rax_facts`` モジュールと、以下のようなインベントリーファイルを使用して実行できます。

.. code-block:: ini

    [test_servers]
    hostname1 rax_region=ORD
    hostname2 rax_region=ORD

.. code-block:: yaml

    - name:Gather info about servers
      hosts: test_servers
      gather_facts:False
      tasks:
        - name:Get facts about servers
          rax_facts:
            credentials: ~/.raxpub
            name: "{{ inventory_hostname }}"
        region: "{{ rax_region }}"
      delegate_to: localhost
    - name: Map some facts
      set_fact:
        ansible_host: "{{ rax_accessipv4 }}"
    
どのように機能するかを知る必要はありませんが、返される変数の種類を把握しておくといいでしょう、

``rax_facts`` モジュールは、以下のようにファクトを提供します。これは ``rax.py`` インベントリースクリプトに一致します。

.. code-block:: json

    {
        "ansible_facts": {
            "rax_accessipv4":"198.51.100.1",
            "rax_accessipv6":"2001:DB8::2342",
            "rax_addresses": {
                "private": [
                {
                    "addr": "192.0.2.2",
                    "version": 4
                }
            ],
                "public": [
                {
                    "addr": "198.51.100.1",
                    "version": 4
                },
                {
                    "addr": "2001:DB8::2342",
                    "version": 6
                }
            ]
            },
            "rax_config_drive": "",
            "rax_created":"2013-11-14T20:48:22Z",
            "rax_flavor": {
                "id": "performance1-1",
                "links": [
                {
                    "href": "https://ord.servers.api.rackspacecloud.com/111111/flavors/performance1-1",
                    "rel": "bookmark"
                }
            ]
            },
            "rax_hostid": "e7b6961a9bd943ee82b13816426f1563bfda6846aad84d52af45a4904660cde0",
            "rax_human_id": "test",
            "rax_id":"099a447b-a644-471f-87b9-a7f580eb0c2a",
            "rax_image": {
                "id": "b211c7bf-b5b4-4ede-a8de-a4368750c653",
                "links": [
                {
                    "href": "https://ord.servers.api.rackspacecloud.com/111111/images/b211c7bf-b5b4-4ede-a8de-a4368750c653",
                    "rel": "bookmark"
                }
            ]
            },
            "rax_key_name": null,
            "rax_links": [
            {
                "href": "https://ord.servers.api.rackspacecloud.com/v2/111111/servers/099a447b-a644-471f-87b9-a7f580eb0c2a",
                "rel": "self"
            },
            {
                "href": "https://ord.servers.api.rackspacecloud.com/111111/servers/099a447b-a644-471f-87b9-a7f580eb0c2a",
                "rel": "bookmark"
            }
        ],
            "rax_metadata": {
                "foo": "bar"
            },
            "rax_name": "test",
            "rax_name_attr": "name",
            "rax_networks": {
                "private": [
                "192.0.2.2"
            ],
                "public": [
                "198.51.100.1",
                "2001:DB8::2342"
            ]
            },
            "rax_os-dcf_diskconfig":"AUTO",
            "rax_os-ext-sts_power_state":1,
            "rax_os-ext-sts_task_state": null,
            "rax_os-ext-sts_vm_state": "active",
            "rax_progress":100,
            "rax_status":"ACTIVE",
            "rax_tenant_id":"111111",
            "rax_updated":"2013-11-14T20:49:27Z",
            "rax_user_id":"22222"
        },
        "changed": false
    }
    

ユースケース
`````````

本セクションでは、特定のユースケースを中心とした、その他の使用例を説明します。

.. _network_and_server:

ネットワークおよびサーバー
++++++++++++++++++

分離したクラウドネットワークを作成し、サーバーを構築します。

.. code-block:: yaml

    - name:Build Servers on an Isolated Network
      hosts: localhost
      gather_facts:False
      tasks:
        - name:Network create request
          rax_network:
            credentials: ~/.raxpub
            label: my-net
            cidr:192.168.3.0/24
            region:IAD
            state: present
          delegate_to: localhost

        - name:Server create request
          rax:
            credentials: ~/.raxpub
            name: web%04d.example.org
            flavor:2
            image: ubuntu-1204-lts-precise-pangolin
            disk_config: manual
            networks:
              - public
              - my-net
            region:IAD
            state: present
            count:5
            exact_count: yes
            group: web
            wait: yes
            wait_timeout:360
          register: rax
          delegate_to: localhost

.. _complete_environment:

完全な環境
++++++++++++++++++++

サーバー、カスタムネットワーク、およびロードバランサーで完全な Web サーバー環境を構築し、nginx をインストールしてカスタムの index.html を作成します。

.. code-block:: yaml

    ---
    - name:Build environment
      hosts: localhost
      gather_facts:False
      tasks:
        - name:Load Balancer create request
          rax_clb:
            credentials: ~/.raxpub
            name: my-lb
            port:80
            protocol:HTTP
            algorithm:ROUND_ROBIN
            type:PUBLIC
            timeout:30
            region:IAD
            wait: yes
            state: present
            meta:
              app: my-cool-app
          register: clb

        - name:Network create request
          rax_network:
            credentials: ~/.raxpub
            label: my-net
            cidr:192.168.3.0/24
            state: present
            region:IAD
          register: network

        - name:Server create request
          rax:
            credentials: ~/.raxpub
            name: web%04d.example.org
            flavor: performance1-1
            image: ubuntu-1204-lts-precise-pangolin
            disk_config: manual
            networks:
              - public
              - private
              - my-net
            region:IAD
            state: present
            count:5
            exact_count: yes
            group: web
            wait: yes
          register: rax

        - name:Add servers to web host group
          add_host:
            hostname: "{{ item.name }}"
        ansible_host: "{{ item.rax_accessipv4 }}"
        ansible_password: "{{ item.rax_adminpass }}"
        ansible_user: root
        groups: web
      loop: "{{ rax.success }}"
      when: rax.action == 'create'

    - name: Add servers to Load balancer
      rax_clb_nodes:
        credentials: ~/.raxpub
        load_balancer_id: "{{ clb.balancer.id }}"
        address: "{{ item.rax_networks.private|first }}"
        port: 80
        condition: enabled
        type: primary
        wait: yes
        region: IAD
      loop: "{{ rax.success }}"
      when: rax.action == 'create'

- name: Configure servers
  hosts: web
  handlers:
    - name: restart nginx
      service: name=nginx state=restarted

  tasks:
    - name: Install nginx
      apt: pkg=nginx state=latest update_cache=yes cache_valid_time=86400
      notify:
        - restart nginx

    - name: Ensure nginx starts on boot
      service: name=nginx state=started enabled=yes

    - name: Create custom index.html
      copy: content="{{ inventory_hostname }}" dest=/usr/share/nginx/www/index.html
                owner=root group=root mode=0644
    
.. _rackconnect_and_manged_cloud:

RackConnect および Managed Cloud
+++++++++++++++++++++++++++++

RackConnect バージョン 2 または Rackspace Managed Cloud を使用する場合は、正常に構築された後に作成するサーバーで実行される Rackspace の自動化タスクがあります。その自動化が「RackConnect」または「Managed Cloud」の自動化前に実行される場合は、障害が発生し、サーバーが利用できなくなる場合があります。

これらの例は、サーバーを作成し、Ansible が続行する前に、Rackspace 自動化が完了したことを確認します。

分かりやすくするために、この例は結合されていますが、どちらも RackConnect を使用する場合に限り必要です。 Managed Cloud のみを使用する場合、RackConnect の部分は無視されます。

RackConnect の部分は、RackConnect バージョン 2 にのみ適用されます。

.. _using_a_control_machine:

コントロールマシンの使用
***********************

.. code-block:: yaml

    - name:Create an exact count of servers
      hosts: localhost
      gather_facts:False
      tasks:
        - name:Server build requests
          rax:
            credentials: ~/.raxpub
            name: web%03d.example.org
            flavor: performance1-1
            image: ubuntu-1204-lts-precise-pangolin
            disk_config: manual
            region:DFW
            state: present
            count:1
            exact_count: yes
            group: web
            wait: yes
          register: rax

        - name:Add servers to in memory groups
          add_host:
            hostname: "{{ item.name }}"
        ansible_host: "{{ item.rax_accessipv4 }}"
        ansible_password: "{{ item.rax_adminpass }}"
        ansible_user: root
        rax_id: "{{ item.rax_id }}"
        groups: web,new_web
      loop: "{{ rax.success }}"
      when: rax.action == 'create'

- name: Wait for rackconnect and managed cloud automation to complete
  hosts: new_web
  gather_facts: false
  tasks:
    - name: ensure we run all tasks from localhost
      delegate_to: localhost
      block:
        - name: Wait for rackconnnect automation to complete
          rax_facts:
            credentials: ~/.raxpub
            id: "{{ rax_id }}"
                region:DFW
              register: rax_facts
              until: rax_facts.ansible_facts['rax_metadata']['rackconnect_automation_status']|default('') == 'DEPLOYED'
              retries:30
              delay:10
    
            - name:Wait for managed cloud automation to complete
          rax_facts:
                credentials: ~/.raxpub
                id: "{{ rax_id }}"
                region:DFW
              register: rax_facts
              until: rax_facts.ansible_facts['rax_metadata']['rax_service_level_automation']|default('') == 'Complete'
              retries:30
              delay:10
    
    - name:Update new_web hosts with IP that RackConnect assigns
      hosts: new_web
      gather_facts: false
      tasks:
        - name:Get facts about servers
          rax_facts:
            name: "{{ inventory_hostname }}"
        region: DFW
      delegate_to: localhost
    - name: Map some facts
      set_fact:
        ansible_host: "{{ rax_accessipv4 }}"
    
- name:Base Configure Servers
      hosts: web
      roles:
        - role: users
    
        - role: openssh
          opensshd_PermitRootLogin: "no"
    
        - role: ntp
    
.. _using_ansible_pull:

Ansible Pull の使用
******************

.. code-block:: yaml

    ---
    - name:Ensure Rackconnect and Managed Cloud Automation is complete
      hosts: all
      tasks:
        - name: ensure we run all tasks from localhost
          delegate_to: localhost
          block:
            - name:Check for completed bootstrap
              stat:
                path: /etc/bootstrap_complete
              register: bootstrap

            - name:Get region
              command: xenstore-read vm-data/provider_data/region
              register: rax_region
              when: bootstrap.stat.exists != True

            - name:Wait for rackconnect automation to complete
              uri:
                url: "https://{{ rax_region.stdout|trim }}.api.rackconnect.rackspace.com/v1/automation_status?format=json"
                return_content: yes
              register: automation_status
              when: bootstrap.stat.exists != True
              until: automation_status['automation_status']|default('') == 'DEPLOYED'
              retries:30
              delay:10

            - name:Wait for managed cloud automation to complete
              wait_for:
                path: /tmp/rs_managed_cloud_automation_complete
                delay:10
              when: bootstrap.stat.exists != True

            - name:Set bootstrap completed
              file:
                path: /etc/bootstrap_complete
                state: touch
                owner: root
                group: root
                mode:0400

    - name:Base Configure Servers
      hosts: all
      roles:
        - role: users

        - role: openssh
          opensshd_PermitRootLogin: "no"

        - role: ntp

.. _using_ansible_pull_with_xenstore:

XenStore での Ansible Pull の使用
********************************

.. code-block:: yaml

    ---
    - name:Ensure Rackconnect and Managed Cloud Automation is complete
      hosts: all
      tasks:
        - name:Check for completed bootstrap
          stat:
            path: /etc/bootstrap_complete
          register: bootstrap

        - name:Wait for rackconnect_automation_status xenstore key to exist
          command: xenstore-exists vm-data/user-metadata/rackconnect_automation_status
          register: rcas_exists
          when: bootstrap.stat.exists != True
          failed_when: rcas_exists.rc|int > 1
          until: rcas_exists.rc|int == 0
          retries:30
          delay:10

        - name:Wait for rackconnect automation to complete
          command: xenstore-read vm-data/user-metadata/rackconnect_automation_status
          register: rcas
          when: bootstrap.stat.exists != True
          until: rcas.stdout|replace('"', '') == 'DEPLOYED'
          retries:30
          delay:10

        - name:Wait for rax_service_level_automation xenstore key to exist
          command: xenstore-exists vm-data/user-metadata/rax_service_level_automation
          register: rsla_exists
          when: bootstrap.stat.exists != True
          failed_when: rsla_exists.rc|int > 1
          until: rsla_exists.rc|int == 0
          retries:30
          delay:10

        - name:Wait for managed cloud automation to complete
          command: xenstore-read vm-data/user-metadata/rackconnect_automation_status
          register: rsla
          when: bootstrap.stat.exists != True
          until: rsla.stdout|replace('"', '') == 'DEPLOYED'
          retries:30
          delay:10

        - name:Set bootstrap completed
          file:
            path: /etc/bootstrap_complete
            state: touch
            owner: root
            group: root
            mode:0400

    - name:Base Configure Servers
      hosts: all
      roles:
        - role: users

        - role: openssh
          opensshd_PermitRootLogin: "no"

        - role: ntp

.. _advanced_usage:

高度な使用方法
``````````````

.. _awx_autoscale:

Tower を使用した自動スケーリング
++++++++++++++++++++++

:ref:`ansible_tower` には、自動スケーリングのユースケースに使用する非常に優れた機能も含まれています。  
このモードでは、簡単な curl スクリプトは定義された URL を呼び出すことができ、サーバーはリクエスターに「ダイヤルアウト」し、
起動しているインスタンスを構成します。 これは、一時ノードを再設定する優れた方法です。
詳細は Tower のドキュメントを参照してください。  

プルモードの Tower でコールバックを使用する利点は、ジョブの結果が依然として中央に記録されることです。
また、リモートホストと共有する情報も少なくなります。

.. _pending_information:

Rackspace Cloud のオーケストレーション
++++++++++++++++++++++++++++++++++++

Ansible は強力なオーケストレーションツールであり、rax モジュールを使用すると複雑なタスク、デプロイメント、および設定のオーケストレーションが可能になります。 ここでは、環境内にあるソフトウェアの他の部分と同様に、インフラストラクチャーのプロビジョニングを自動化することが重要になります。 複雑なデプロイメントでは、以前ロードバランサーの手動操作またはサーバーの手動プロビジョニングが必要になる場合があります。 Ansible に含まれる rax モジュールを利用することで、現在実行中のノードの数に応じてノードを追加したり、共通のメタデータを持つノードの数に応じてクラスターアプリケーションを構成できます。 たとえば、以下のようなシナリオを自動化できます。

* Cloud Load Balancer から 1 つずつ削除され、更新され、検証され、ロードバランサープールに返されるサーバー
* ノードのプロビジョニング、ブートストラップ、設定、およびソフトウェアがインストールされている、すでにオンライン環境の拡張
* ノードが非推奨になる前に、アプリケーションログファイルが中央の場所 (Cloud Files など) にアップロードされる手順
* DNS レコードが作成時に作成され、廃止時に破棄されるサーバーとロードバランサー




