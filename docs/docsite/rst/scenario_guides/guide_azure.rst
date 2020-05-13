Microsoft Azure ガイド
=====================

Ansible には、Azure Resource Manager と対話するためのモジュールのスイートが含まれており、簡単に作成し、
Microsoft Azure Cloud 上のインフラストラクチャーを調整するツールを提供します。

要件
------------

Azure Resource Manager モジュールを使用するには、
Ansible を実行しているホストに特定の Azure SDK モジュールをインストールする必要があります。

.. code-block:: bash

    $ pip install 'ansible[azure]'

ソースから Ansible を実行している場合は、
Ansible リポジトリーの root ディレクトリーから依存関係をインストールできます。

.. code-block:: bash

    $ pip install .[azure]

また、Ansible が事前にインストールされている `Azure Cloud Shell <https://shell.azure.com>`_ で Ansible を直接実行することもできます。

API での認証
-------------------------

Azure Resource Manager モジュールを使用するには、Azure API で認証する必要があります。以下の認証ストラテジーを選択できます。

* Active Directory ユーザー名/パスワード
* サービスプリンシパルの認証情報

使用する戦略の指示に従い、実際にモジュールを使用して Azure API で認証する方法について、「`Azure モジュールへの認証情報の提供`_」
に進んでください。


サービスプリンシパルの使用
.......................

「`サービスプリンシパルの作成方法 <https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-group-create-service-principal-portal>`_」を説明する詳細な公式チュートリアルがあります。

チュートリアルを実行すると、以下が可能になります。

* Azure ポータルのアプリケーションの「設定」ページの「クライアント ID」ボックスにあるクライアント ID。
* シークレットキーは、アプリケーションの作成時に生成されます。作成後にキーを表示することはできません。
  キーが失われた場合は、アプリケーションの「設定」ページで新しいキーを作成する必要があります。
* 最後にテナント ID。これは、
  アプリケーションを含む AD を指す UUID (例: ABCDEFGH-1234-ABCD-1234-ABCDEFGHIJKL) です。これは、Azure ポータルまたは指定の URL の「エンドポイントの表示」にある URL にあります。


Active Directory のユーザー名/パスワードの使用
........................................

Active Directory のユーザー名/パスワードを作成するには、以下を実行します。

* 管理者アカウントを使用して Azure Classic Portal に接続します。
* デフォルトの AAD でユーザーを作成します。マルチファクター認証をアクティブにしないでください。
* Settings、Administrator に移動します。
* Add をクリックして、新規ユーザーの電子メールを入力します。
* このユーザーでテストするサブスクリプションのチェックボックスにチェックを付けます。
* この新規ユーザーで Azure Portal にログインし、一時パスワードを新規パスワードに変更します。OAuth ログインに、
  一時パスワードを使用することはできません。

Azure モジュールへの認証情報の提供
......................................

モジュールは、認証情報を提供する複数の方法を提供します。Ansible Tower、Jenkins などの CI/CD ツールでは、
ほとんどの場合は、環境変数を使用してください。ローカル開発の場合は、
認証情報をホームディレクトリー内のファイルに保存できます。当然ながら、認証情報をパラメーターとして Playbook 内のタスクに渡すことができます。優先順位は、
パラメーター、環境変数、最後にホームディレクトリーにあるファイルの順になります。

追加の環境変数
```````````````````````````

環境経由でサービスプリンシパルの認証情報を渡すには、以下の変数を定義します。

* AZURE_CLIENT_ID
* AZURE_SECRET
* AZURE_SUBSCRIPTION_ID
* AZURE_TENANT

環境経由で Active Directory のユーザー名/パスワードのペアを渡すには、以下の変数を定義します。

* AZURE_AD_USER
* AZURE_PASSWORD

環境経由で Active Directory のユーザー名/パスワードを渡すには、以下の変数を定義します。

* AZURE_AD_USER
* AZURE_PASSWORD
* AZURE_CLIENT_ID
* AZURE_TENANT
* AZURE_ADFS_AUTHORITY_URL

「AZURE_ADFS_AUTHORITY_URL」は任意です。これは、https://yourdomain.com/adfs といった独自の認証機関がある場合にのみ必要です。

ファイルへの保存
`````````````````

開発環境で作業する場合は、ファイルに認証情報を保存することが望ましい場合があります。モジュールは、
``$HOME/.azure/credentials`` を認証情報を探します。このファイルは ini 形式のファイルです。以下のようになります。

.. code-block:: ini

    [default]
    subscription_id=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    client_id=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    secret=xxxxxxxxxxxxxxxxx
    tenant=xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

.. note:: シークレット値に ASCII 以外の文字が含まれる場合は、ログインエラーを防ぐために `URL Encode <https://www.w3schools.com/tags/ref_urlencode.asp>`_ を行う必要があります。

複数のセクションを作成すると、認証情報ファイルに複数の認証情報セットを保存できます。それぞれのセクションは、
プロファイルとみなされます。モジュールが自動的に [default] プロファイルを検索します。環境で AZURE_PROFILE を定義するか、
プロファイルパラメーターを渡して特定のプロファイルを指定します。

パラメーターとして渡す
`````````````````````

認証情報をパラメーターとしてタスクに渡すには、サービスプリンシパルについて以下のパラメーターを使用します。

* client_id
* secret
* subscription_id
* tenant

または、Active Directory のユーザー名/パスワードについて以下のパラメーターを渡します。

* ad_user
* password

または、以下のパラメーターを ADFS username/pasword に渡します。

* ad_user
* password
* client_id
* tenant
* adfs_authority_url

「adfs_authority_url」は任意です。これは、https://yourdomain.com/adfs といった独自の認証機関がある場合にのみ必要です。


その他のクラウド環境
------------------------

デフォルトのパブリッククラウド (Azure China Cloud、Azure US Government Cloud、Azure Stack など) 以外の Azure Cloud を使用するには、
「cloud_environment」引数をモジュールに渡すか、認証情報プロファイルで構成するか、
「AZURE_CLOUD_ENVIRONMENT」環境を設定します。値は、Azure Python SDK で定義されたクラウド名 (「AzureChinaCloud」、「AzureUSGovernment」など。
デフォルトは「AzureCloud」) または Azure メタデータ検出 URL (Azure Stack の場合) のいずれかです。

仮想マシンの作成
-------------------------

仮想マシンを作成する 2 つの方法は、azure_rm_virtualmachine モジュールに関連する方法があります。ストレージアカウント、ネットワークインターフェース、セキュリティグループ、パブリック IP アドレスを作成して、
これらのオブジェクトの名前をパラメーターとしてモジュールに渡すか、
その作業をモジュールに任せて、選択したデフォルトを受け入れることができます。

個別コンポーネントの作成
..............................

Azure モジュールは、ストレージアカウント、仮想ネットワーク、サブネット、ネットワークインターフェース、
セキュリティーグループ、およびパブリック IP の作成に役立ちます。これをそれぞれを作成し、
最後に azure_rm_virtualmachine モジュールに名前を渡す完全な例を次に示します。

.. code-block:: yaml

    - name:Create storage account
      azure_rm_storageaccount:
        resource_group:Testing
        name: testaccount001
        account_type:Standard_LRS

    - name:Create virtual network
      azure_rm_virtualnetwork:
        resource_group:Testing
        name: testvn001
        address_prefixes:"10.10.0.0/16"

    - name:Add subnet
      azure_rm_subnet:
        resource_group:Testing
        name: subnet001
        address_prefix:"10.10.0.0/24"
        virtual_network: testvn001

    - name:Create public ip
      azure_rm_publicipaddress:
        resource_group:Testing
        allocation_method:Static
        name: publicip001

    - name:Create security group that allows SSH
      azure_rm_securitygroup:
        resource_group:Testing
        name: secgroup001
        rules:
          - name:SSH
            protocol:Tcp
            destination_port_range:22
            access:Allow
            priority:101
            direction:Inbound

    - name:Create NIC
      azure_rm_networkinterface:
        resource_group:Testing
        name: testnic001
        virtual_network: testvn001
        subnet: subnet001
        public_ip_name: publicip001
        security_group: secgroup001

    - name:Create virtual machine
      azure_rm_virtualmachine:
        resource_group:Testing
        name: testvm001
        vm_size:Standard_D1
        storage_account: testaccount001
        storage_container: testvm001
        storage_blob: testvm001.vhd
        admin_username: admin
        admin_password:Password!
        network_interfaces: testnic001
        image:
          offer:CentOS
          publisher:OpenLogic
          sku:'7.1'
          version: latest

各 Azure モジュールは、さまざまなパラメーターオプションを提供します。上記の例で、すべてのオプションが示されているわけではありません。
詳細およびサンプルは、各モジュールを参照してください。


デフォルトオプションを使用した仮想マシンの作成
...............................................

すべての詳細を指定せずに仮想マシンを作成する場合は、これも実行できます。唯一の注意点は、
リソースグループに既に 1 つのサブネットがある仮想ネットワークが必要になることです。既存のサブネットを持つ仮想ネットワークがすでにあると想定すると、
次のコマンドを実行して仮想マシンを作成できます。

.. code-block:: yaml

    azure_rm_virtualmachine:
      resource_group: Testing
      name: testvm10
      vm_size: Standard_D1
      admin_username: chouseknecht
      ssh_password_enabled: false
      ssh_public_keys: "{{ ssh_keys }}"
      image:
        offer: CentOS
        publisher: OpenLogic
        sku: '7.1'
        version: latest


動的インベントリースクリプト
------------------------

Ansible の動的インベントリースクリプトに精通していない場合は、「:ref:`ダイナミックインベントリーの概要 <intro_dynamic_inventory>`」を参照してください。

Azure Resource Manager インベントリースクリプトは、`azure_rm.py  <https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/azure_rm.py>`_ と呼ばれます。これは、Azure API で Azure モジュールとまったく同じように認証されます。
つまり、上記の「`環境変数の使用`_」で説明したのと同じ環境変数を定義することになります。
または、``$HOME/.azure/credentials`` ファイル (上記の「`ファイルへの保存`_」で説明) 作成するか、またはコマンドラインパラメーターを渡します。利用可能なコマンドラインオプションを表示するには、
以下のコマンドを実行します。

.. code-block:: bash

    $ ./ansible/contrib/inventory/azure_rm.py --help

すべての動的インベントリースクリプトと同様に、スクリプトを直接実行でき、パラメーターとして ansible コマンドに渡すか、
-i オプションを使用して ansible-playbook に直接渡します。どのように実行されても、
スクリプトは Azure サブスクリプションで見つかったすべてのホストを表す JSON を生成します。これを、特定の Azure リソースグループのセットにあるホストだけに絞り込むことも、
特定のホストに絞り込むこともできます。

インベントリースクリプトは、指定のホストに対して以下のホスト変数を提供します。

.. code-block:: JSON

    {
      "ansible_host": "XXX.XXX.XXX.XXX",
      "computer_name": "computer_name2",
      "fqdn": null,
      "id": "/subscriptions/subscription-id/resourceGroups/galaxy-production/providers/Microsoft.Compute/virtualMachines/object-name",
      "image": {
        "offer": "CentOS",
        "publisher": "OpenLogic",
        "sku": "7.1",
        "version": "latest"
      },
      "location": "westus",
      "mac_address": "00-00-5E-00-53-FE",
      "name": "object-name",
      "network_interface": "interface-name",
      "network_interface_id": "/subscriptions/subscription-id/resourceGroups/galaxy-production/providers/Microsoft.Network/networkInterfaces/object-name1",
      "network_security_group": null,
      "network_security_group_id": null,
      "os_disk": {
        "name": "object-name",
        "operating_system_type": "Linux"
      },
      "plan": null,
      "powerstate": "running",
      "private_ip": "172.26.3.6",
      "private_ip_alloc_method": "Static",
      "provisioning_state": "Succeeded",
      "public_ip": "XXX.XXX.XXX.XXX",
      "public_ip_alloc_method": "Static",
      "public_ip_id": "/subscriptions/subscription-id/resourceGroups/galaxy-production/providers/Microsoft.Network/publicIPAddresses/object-name",
      "public_ip_name": "object-name",
      "resource_group": "galaxy-production",
      "security_group": "object-name",
      "security_group_id": "/subscriptions/subscription-id/resourceGroups/galaxy-production/providers/Microsoft.Network/networkSecurityGroups/object-name",
      "tags": {
        "db": "mysql"
      },
      "type": "Microsoft.Compute/virtualMachines",
      "virtual_machine_size": "Standard_DS4"
    }

ホストグループ
...........

デフォルトでは、ホストは以下のようにグループ化されます。

* azure (全ホスト)
* location name
* resource group name
* security group name
* tag key
* tag key_value
* os_disk operating_system_type (Windows/Linux)

環境変数を定義するか、現在の作業ディレクトリーに azure_rm.ini ファイルを作成することにより、
ホストのグループ化とホストの選択を制御できます。

注記: .ini ファイルは環境変数よりも優先されます。

注記: .ini ファイルの名前は、インベントリースクリプトのベース名 (つまり「azure_rm」) で、
これには「.ini」拡張子が含まれます。これにより、インベントリースクリプトをコピーし、名前を変更して、
同じディレクトリーで .ini ファイルをすべて一致させることができます。

環境で定義された以下の変数を使用してグループ化を制御します。

* AZURE_GROUP_BY_RESOURCE_GROUP=yes
* AZURE_GROUP_BY_LOCATION=yes
* AZURE_GROUP_BY_SECURITY_GROUP=yes
* AZURE_GROUP_BY_TAG=yes
* AZURE_GROUP_BY_OS_FAMILY=yes

コンマ区切りリストを以下に割り当てて、特定のリソースグループ内のホストを選択します。

* AZURE_RESOURCE_GROUPS=resource_group_a,resource_group_b

タグキーのコンマ区切りリストを以下に割り当てて、特定のタグキーのホストを選択します。

* AZURE_TAGS=key1,key2,key3

場所のコンマ区切りリストを割り当てて、特定の場所のホストを選択します。

* AZURE_LOCATIONS=eastus,eastus2,westus

または、コンマ区切りリストの key:value ペアを以下に割り当てることで、特定のタグ key:value ペアのホストを選択します。

* AZURE_TAGS=key1:value1,key2:value2

電力状態が必要ない場合は、powerstate 取得をオフにすることでパフォーマンスを向上させることができます。

* AZURE_INCLUDE_POWERSTATE=no

zure_rm.ini ファイルのサンプルは、contrib/inventory のインベントリースクリプトに含まれています。.ini ファイルは、
以下が含まれます。

.. code-block:: ini

    [azure]
    # Control which resource groups are included. By default all resources groups are included.
    # Set resource_groups to a comma separated list of resource groups names.
    #resource_groups=

    # Control which tags are included. Set tags to a comma separated list of keys or key:value pairs
    #tags=

    # Control which locations are included. Set locations to a comma separated list of locations.
    #locations=

    # Include powerstate. If you don't need powerstate information, turning it off improves runtime performance.
    # Valid values: yes, no, true, false, True, False, 0, 1.
    include_powerstate=yes

    # Control grouping with the following boolean flags. Valid values: yes, no, true, false, True, False, 0, 1.
    group_by_resource_group=yes
    group_by_location=yes
    group_by_security_group=yes
    group_by_tag=yes
    group_by_os_family=yes

例
........

以下は、インベントリースクリプトの使用例です。

.. code-block:: bash

    # Execute /bin/uname on all instances in the Testing resource group
    $ ansible -i azure_rm.py Testing -m shell -a "/bin/uname -a"

    # Execute win_ping on all Windows instances
    $ ansible -i azure_rm.py windows -m win_ping

    # Execute win_ping on all Windows instances
    $ ansible -i azure_rm.py winux -m ping

    # Use the inventory script to print instance specific information
    $ ./ansible/contrib/inventory/azure_rm.py --host my_instance_host_name --resource-groups=Testing --pretty

    # Use the inventory script with ansible-playbook
    $ ansible-playbook -i ./ansible/contrib/inventory/azure_rm.py test_playbook.yml

以下は、Azure インベントリースクリプトを実行するための単純な Playbook です。

.. code-block:: yaml

    - name: Test the inventory script
      hosts: azure
      connection: local
      gather_facts: no
      tasks:
        - debug: msg="{{ inventory_hostname }} has powerstate {{ powerstate }}"

Playbook は以下のような方法で実行できます。

.. code-block:: bash

    $ ansible-playbook -i ./ansible/contrib/inventory/azure_rm.py test_azure_inventory.yml


Azure エンドポイントでの証明書検証の無効化
...................................................

HTTPS プロキシープロキシが存在する場合、または Azure Stack を使用する場合は、
Azure モジュールで Azure エンドポイントの証明書検証を無効にすることが必要になる場合があります。これは推奨されるセキュリティー対策ではありませんが、
必要な CA 証明書を含めるようにシステムの CA ストアを変更できない場合に必要になることがあります。証明書の検証は、
認証情報プロファイルの「cert_validation_mode」値を設定するか、「AZURE_CERT_VALIDATION_MODE」環境変数を使用するか、
「cert_validation_mode」引数を Azure モジュールに渡すことで制御できます。デフォルト値は「validate」です。
値を「ignore」に設定すると、すべての証明書の検証が回避されます。module 引数は、認証情報プロファイルの値よりも優先されます。
これは、環境値よりも優先されます。
