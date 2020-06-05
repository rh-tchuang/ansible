.. _intro_dynamic_inventory:
.. _dynamic_inventory:

******************************
動的インベントリーの使用
******************************

.. contents::
   :local:

ビジネスニーズに応じてホストを起動またはャットダウンすることで Ansible インベントリーが時間の経過と共に変動する場合は、:ref:`インベントリー` で説明されている静的なインベントリーソリューションではユーザーのニーズに応えることができません。クラウドプロバイダー、LDAP、`Cobbler <https://cobbler.github.io>`_、エンタープライズ CMDB システムなどの複数のソースからホストを追跡することが必要になる場合があります。

Ansible は、動的な外部インベントリーシステムでこのオプションをすべて統合します。Ansible は、:ref:`inventory_plugins` および `インベントリースクリプト <https://github.com/ansible/ansible/tree/devel/contrib/inventory>`_ の 2 つの方法で外部インベントリーに接続します。

インベントリープラグインは、Ansible コアコードへの最新の更新を利用します。動的インベントリーのスクリプトには、プラグインを使用することが推奨されます。追加の動的インベントリーソースに接続する :ref:`独自のプラグインを記述<developing_inventory>` できます

選択した場合には、インベントリースクリプトを使用できます。インベントリープラグインを実装すると、スクリプトインベントリープラグインを介して後方互換性が確保されます。以下の例は、インベントリースクリプトの使用方法を示しています。

動的インベントリーの対応に GUI が必要な場合は、:ref:`ansible_tower` インベントリーデータベースがすべての動的インベントリーソースと同期し、その結果への Web および REST アクセスを提供し、グラフィカルインベントリーエディターを提供します。すべてのホストのデータベースレコードを使用して、過去のイベント履歴を関連付け、最後の Playbook の実行でどのホストに障害が発生したかを確認できます。

.. _cobbler_example:

インベントリースクリプトの例:Cobbler
=================================

Ansible は、Linux インストールサーバー `Cobbler <https://cobbler.github.io>`_ (最初に Michael DeHaan が作成し、現在は Ansible に所属する James Cammarata が率いています) とシームレスに統合されます。

Cobbler は主に OS のインストールを開始し、DHCP と DNS を管理するために使用されますが、
複数の構成管理システムのデータを (同時にでも) 表現し、「軽量CMDB」として機能する汎用レイヤーがあります。

Ansible インベントリーを Cobbler に関連付けるには、`このスクリプト<https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/cobbler.py>`_ を ``/etc/ansible`` および ``chmod +x`` ファイルにコピーします。Ansible を使用する場合はいつでも ``cobblerd`` を実行し、``-i`` コマンドラインオプション (``-i /etc/ansible/cobbler.py`` など) を使用して、Cobbler の XMLRPC API を使用して Cobbler と通信します。

Ansible が Cobbler サーバーの場所を認識し、キャッシュが改善されるように ``/etc/ansible`` に ``cobbler.ini`` ファイルを追加します。以下に例を示します。

.. code-block:: text

    [cobbler]

    # Set Cobbler's hostname or IP address
    host = http://127.0.0.1/cobbler_api

    # API calls to Cobbler can be slow. For this reason, we cache the results of an API
    # call. Set this to the path you want cache files to be written to. Two files
    # will be written to this directory:
    #   - ansible-cobbler.cache
    #   - ansible-cobbler.index

    cache_path = /tmp

    # The number of seconds a cache file is considered valid. After this many
    # seconds, a new API call will be made, and the cache file will be updated.

    cache_max_age = 900


まず ``/etc/ansible/cobbler.py`` を直接実行して、このスクリプトをテストします。  JSON データの出力が表示されますが、まだ何も含まれていない場合もあります。

これが何をするのか見てみましょう。 Cobbler では、以下のようなシナリオを想定しています。

.. code-block:: bash

    cobbler profile add --name=webserver --distro=CentOS6-x86_64
    cobbler profile edit --name=webserver --mgmt-classes="webserver" --ksmeta="a=2 b=3"
    cobbler system edit --name=foo --dns-name="foo.example.com" --mgmt-classes="atlanta" --ksmeta="c=4"
    cobbler system edit --name=bar --dns-name="bar.example.com" --mgmt-classes="atlanta" --ksmeta="c=5"

上記の例では、「foo.example.com」システムは Ansible で直接アドレスを指定できますが、グループ名「webserver」または「Atlanta」を使用する場合にもアドレスを指定できます。 Ansible は SSH を使用するため、「foo.example.com」(foo ではなく) を介してシステム foo と通信します。 同様に、システムの DNS 名が「foo」で始まるため、「ansible foo」を試してもシステムは見つかりませんが、「ansible 'foo*」にすると見つかります。

このスクリプトは、ホストおよびグループの情報よりも多くの情報を提供します。 さらに、(Playbook を使用する際に自動的に実行される)「setup」モジュールが実行すると、変数「a」、「b」、および「c」 はすべてテンプレートに自動入力されるようになります。

.. code-block:: text

    # file: /srv/motd.j2
    Welcome, I am templated with a value of a={{ a }}, b={{ b }}, and c={{ c }}

これは以下のように実行できます。

.. code-block:: bash

    ansible webserver -m setup
    ansible webserver -m template -a "src=/tmp/motd.j2 dest=/etc/motd"

.. note::
   設定ファイルの変数と同様に、
   「webserver」は Cobbler のものです。 Ansible では、通常どおりに独自の変数を渡すことはできますが、
   外部インベントリースクリプトの変数が、
   同じ名前の変数を上書きします。

そのため、上記のテンプレート (``motd.j2``) を使用すると、システムの「foo」用に、以下のデータが ``/etc/motd`` に書き込まれます。

.. code-block:: text

    Welcome, I am templated with a value of a=2, b=3, and c=4

システム「bar」 (bar.example.com) は、以下のようになります。

.. code-block:: text

    Welcome, I am templated with a value of a=2, b=3, and c=5

技術的には、これを行う大きな正当な理由はありませんが、これも機能します。

.. code-block:: bash

    ansible webserver -m shell -a "echo {{ a }}"

つまり、引数やアクションでこの変数を使用することもできます。

.. _aws_example:

インベントリースクリプトの例:AWS EC2
=================================

Amazon Web Services EC2 を使用している場合は、時間とともにホストが起動またはシャットダウンして外部アプリケーションにより管理されたり、AWS 自動スケーリングを使用している場合もあるため、インベントリーファイルを維持することが最良の方法ではない可能性があります。このため、`EC2 の外部インベントリー<https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.py>`_ スクリプトを使用できます。

このスクリプトは、以下のいずれかの方法で使用できます。最も簡単な方法は、Ansible の ``-i`` コマンドラインオプションを使用し、スクリプトを実行ファイルとした後、スクリプトへのパスを指定することです。

.. code-block:: bash

    ansible -i ec2.py -u ubuntu us-east-1d -m ping

次のオプションとして、スクリプトを `/etc/ansible/hosts` にコピーし `chmod +x` を設定します。`ec2.ini <https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/ec2.ini>`_ ファイルを `/etc/ansible/ec2.ini` にコピーする必要もあります。通常どおりに Ansible を実行できます。

AWS への API 呼び出しを正常に行うには、Boto (AWS への Python インターフェース) を設定する必要があります。この `方法いくつか<http://docs.pythonboto.org/en/latest/boto_config_tut.html>`_ ありますが、最も簡単なのは 2 つの環境変数をエクスポートすることです。

.. code-block:: bash

    export AWS_ACCESS_KEY_ID='AK123'
    export AWS_SECRET_ACCESS_KEY='abc123'

スクリプトを単独でテストして、設定が正しいことを確認できます。

.. code-block:: bash

    cd contrib/inventory
    ./ec2.py --list

しばらくすると、JSON のすべてのリージョンに EC2 インベントリー全体が表示されます。

Boto プロファイルを使用して複数の AWS アカウントを管理する場合は、``--profile PROFILE`` 名を ``ec2.py`` スクリプトに渡すことができます。プロファイルの例は以下のようになります。

.. code-block:: text

    [profile dev]
    aws_access_key_id = <dev access key>
    aws_secret_access_key = <dev secret key>

    [profile prod]
    aws_access_key_id = <prod access key>
    aws_secret_access_key = <prod secret key>

その後、``ec2.py --profile prod`` を実行して、prod アカウントのインベントリーを取得できますが、このオプションは ``ansible-playbook`` ではサポートされません。
``AWS_PROFILE`` 変数を使用することもできます。以下に例を示します。``AWS_PROFILE=prod ansible-playbook -i ec2.py myplaybook.yml``

各リージョンには独自の API 呼び出しが必要であるため、小規模なリージョンセットのみを使用している場合は、``ec2.ini`` ファイルを編集して、使用していないリージョンをコメントアウトできます。

キャッシュ制御や宛先変数など、``ec2.ini`` にはその他の設定オプションがあります。デフォルトでは、``ec2.ini`` ファイルは **すべての Amazon クラウドサービス** に対して設定されますが、適用できない機能はコメントアウトできます。たとえば、``RDS`` または ``elasticache`` がない場合は、その機能を ``False`` に設定できます。

.. code-block:: text

    [ec2]
    ...

    # To exclude RDS instances from the inventory, uncomment and set to False.
    rds = False

    # To exclude ElastiCache instances from the inventory, uncomment and set to False.
    elasticache = False
    ...

基本的に、インベントリーファイルは単に名前から宛先アドレスへのマッピングです。デフォルトの ``ec2.ini`` 設定は、EC2 以外 (ノートパソコンなど) で Ansible を実行するように構成されています。これは EC2 を管理する最も効率的な方法ではありません。

EC2 内から Ansible を実行している場合には、内部 DNS 名および IP アドレスの方がパブリック DNS 名よりも推奨されます。この場合は、``ec2.ini`` の ``destination_variable`` をインスタンスのプライベート DNS 名に変更できます。これは、VPC 内のプライベートサブネット内で Ansible を実行する場合に特に重要になります。インスタンスにアクセスする唯一の方法は、プライベート IP アドレスを使用する方法です。VPC インスタンスの場合、``ec2.ini`` の `vpc_destination_variable` は、`boto.ec2.instance variable <http://docs.pythonboto.org/en/latest/ref/ec2.html#module-boto.ec2.instance>`_ を使用してお客様の環境に最も適した方法を提供します。

EC2 外部インベントリーは、複数のグループからインスタンスへのマッピングを提供します。

グローバル
  すべてのインスタンスは、グループ ``ec2`` にあります。

インスタンス ID
  インスタンス ID は一意であるため、これはインスタンス ID のグループです。
  (例: 
  ``i-00112233``
  ``i-a1b1c1d1``)

リージョン
  AWS リージョンのすべてのインスタンスのグループです。
  (例: 
  ``us-east-1``
  ``us-west-2``)

アベイラビリティーゾーン
  アベイラビリティーゾーン内のすべてのインスタンスのグループです。
  (例: 
  ``us-east-1a``
  ``us-east-1b``)

セキュリティーグループ
  インスタンスは複数のセキュリティーグループに属します。セキュリティーグループごとにグループが作成され、英数字以外のすべての文字がアンダースコア (_) に変換されます。各グループの先頭には ``security_group_`` が付けられます。現在、ダッシュ (-) もアンダースコア (_) に変換されます。ec2.ini の replace_dash_in_groups 設定を使用して変更できます (これはいくつかのバージョンで変更されているため、詳細は ec2.ini を確認してください)。
  (例: 
  ``security_group_default``
  ``security_group_webservers``
  ``security_group_Pete_s_Fancy_Group``)

タグ
  各インスタンスには、タグと呼ばれるさまざまなキーと値のペアを関連付けることができます。最も一般的なタグキーは「Name」ですが、他のタグも使用できます。キーと値の各ペアはインスタンスの独自のグループで、``tag_KEY_VALUE`` の形式でアンダースコアに変換される特殊文字が再度使用されます。
  (例: 
  ``tag_Name_redis-master-001`` が ``tag_Name_redis_master_001`` になり、
  ``tag_aws_cloudformation_logical-id_WebServerGroup`` が ``tag_aws_cloudformation_logical_id_WebServerGroup`` となるように、
  tag_Name_Web を使用できます。

Ansible が特定のサーバーと対話する場合、EC2 インベントリースクリプトは ``--host HOST`` オプションを使用して再度呼び出されます。これは、インデックスキャッシュで HOST を検索してインスタンス ID を取得し、AWS への API 呼び出しを行い、その特定のインスタンスに関する情報を取得します。次に、そのインスタンスに関する情報を変数として Playbook で利用できるようにします。各変数の先頭には ``ec2_`` が付けられます。利用可能な変数の一部は次のとおりです。

- ec2_architecture
- ec2_description
- ec2_dns_name
- ec2_id
- ec2_image_id
- ec2_instance_type
- ec2_ip_address
- ec2_kernel
- ec2_key_name
- ec2_launch_time
- ec2_monitored
- ec2_ownerId
- ec2_placement
- ec2_platform
- ec2_previous_state
- ec2_private_dns_name
- ec2_private_ip_address
- ec2_public_dns_name
- ec2_ramdisk
- ec2_region
- ec2_root_device_name
- ec2_root_device_type
- ec2_security_group_ids
- ec2_security_group_names
- ec2_spot_instance_request_id
- ec2_state
- ec2_state_code
- ec2_state_reason
- ec2_status
- ec2_subnet_id
- ec2_tag_Name
- ec2_tenancy
- ec2_virtualization_type
- ec2_vpc_id

``ec2_security_group_ids`` と ``ec2_security_group_names`` は両方とも、すべてのセキュリティーグループをコンマ区切った一覧になります。各 EC2 タグは ``ec2_tag_KEY`` 形式の変数です。

インスタンスで使用可能な変数の完全一覧を表示するには、スクリプトを単独で実行します。

.. code-block:: bash

    cd contrib/inventory
    ./ec2.py --host ec2-12-12-12-12.compute-1.amazonaws.com

AWS インベントリースクリプトは、API 呼び出しの繰り返しを回避するために結果をキャッシュし、このキャッシュ設定は ec2.ini で構成できることに注意してください。 キャッシュを明示的に消去するには、
``--refresh-cache`` パラメーターを使用して ec2.py スクリプトを実行します。

.. code-block:: bash

    ./ec2.py --refresh-cache

.. _openstack_example:

インベントリースクリプトの例:OpenStack
===================================

独自のインベントリーファイルを手動で管理する代わりに、OpenStack ベースのクラウドを使用する場合は、動的インベントリー ``openstack_inventory.py`` を使用して、OpenStack から直接コンピュートインスタンスに関する情報を取得できます。

最新バージョンの OpenStack インベントリースクリプトは、`こちら <https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/openstack_inventory.py>`_ からダウンロードできます。

(`-i openstack_inventory.py` 引数を Ansible に渡すことで) インベントリースクリプトを明示的に使用するか、(スクリプトを `/etc/ansible/hosts` において) 暗黙的に使用できます。

OpenStack インベントリースクリプトの明示的な使用
------------------------------------------

最新バージョンの OpenStack の動的インベントリースクリプトをダウンロードし、実行可能にします。

    wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/openstack_inventory.py
    chmod +x openstack_inventory.py

.. note::
    `openstack.py` という名前は付けないでください。この名前は、openstacksdk からのインポートと競合します。

OpenStack RC ファイルを読み込みます。

.. code-block:: bash

    source openstack.rc

.. note::

    OpenStack RC ファイルには、認証 URL、ユーザー名、パスワード、リージョン名など、クラウドプロバイダーとの接続を確立するためにクライアントツールが必要とする環境変数が含まれています。OpenStack RC ファイルのダウンロード、作成、または読み込み (source) の方法は、`OpenStack RC ファイルを使用して環境変数の設定<https://docs.openstack.org/user-guide/common/cli_set_environment_variables_using_openstack_rc.html>`_.を参照してください。

`nova list` などの単純なコマンドを実行してエラーを返さないようにすることで、ファイルが正常に読み込まれたことを確認できます。

.. note::

    OpenStack コマンドラインのクライアントは、`nova list` コマンドを実行する必要があります。これらのインストール方法の詳細は、`OpenStack コマンドラインクライアントのインストール <https://docs.openstack.org/user-guide/common/cli_install_openstack_command_line_clients.html>`_ を参照してください。

OpenStack の動的インベントリースクリプトを手動でテストして、想定どおりに機能していることを確認します。

    ./openstack_inventory.py --list

しばらくすると、コンピュートインスタンスに関する情報が含まれる JSON 出力が表示されます。

動的インベントリースクリプトが想定どおりに機能していることを確認したら、以下のように Ansible が `openstack_inventory.py` スクリプトをインベントリーファイルとして使用するように指定します。

.. code-block:: bash

    ansible -i openstack_inventory.py all -m ping

OpenStack インベントリースクリプトの暗黙的な使用
------------------------------------------

最新バージョンの OpenStack 動的インベントリースクリプトをダウンロードし、実行可能にし、これを `/etc/ansible/hosts` にコピーします。

.. code-block:: bash

    wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/openstack_inventory.py
    chmod +x openstack_inventory.py
    sudo cp openstack_inventory.py /etc/ansible/hosts

サンプル設定ファイルをダウンロードし、必要に応じて変更し、これを `/etc/ansible/openstack.yml` にコピーします。

.. code-block:: bash

    wget https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/openstack.yml
    vi openstack.yml
    sudo cp openstack.yml /etc/ansible/

OpenStack 動的インベントリースクリプトを手動でテストして、想定どおりに機能していることを確認します。

.. code-block:: bash

    /etc/ansible/hosts --list

しばらくすると、コンピュートインスタンスに関する情報が含まれる JSON 出力が表示されます。

キャッシュの更新
--------------------

OpenStack 動的インベントリースクリプトは、API 呼び出しが繰り返し行われるのを防ぐために、結果をキャッシュすることに注意してください。キャッシュを明示的に消去するには、``--refresh`` パラメーターを使用して openstack_inventory.py (または hosts) スクリプトを実行します。

.. code-block:: bash

    ./openstack_inventory.py --refresh --list

.. _other_inventory_scripts:

その他のインベントリースクリプト
=======================

含まれるインベントリースクリプトはすべて `contrib/inventory ディレクトリー <https://github.com/ansible/ansible/tree/devel/contrib/inventory>`_ にあります。一般的な使用法は、すべてのインベントリースクリプトで類似しています。:ref:`独自のインベントリースクリプトを作成<developing_inventory>` することもできます。

.. _using_multiple_sources:

インベントリーディレクトリーおよび複数のインベントリーソースの使用
==========================================================

Ansible で ``-i`` に指定される場所がディレクトリー (または ``ansible.cfg`` で設定される場所) の場合、
Ansible は複数のインベントリーソースを同時に使用できます。 これを実行する場合は、同じ Ansible 実行で動的および静的に管理されているインベントリーソースの両方を混在させることができます。インスタント
ハイブリッドクラウドです。

インベントリーディレクトリーでは、実行ファイルは動的インベントリーソースとして扱われ、その他のほとんどのファイルは静的ソースとして処理されます。以下のいずれかが続いたファイルは無視されます。

.. code-block:: text

    ~, .orig, .bak, .ini, .cfg, .retry, .pyc, .pyo

この一覧を、自分で選択したものに置き換えるには、ansible.cfg に ``inventory_ignore_extensions`` の一覧を設定するか、:envvar:`ANSIBLE_INVENTORY_IGNORE` 環境変数を設定します。いずれの場合でも、値は、上記のように、パターンをコンマで区切った一覧である必要があります。

インベントリーディレクトリーの ``group_vars`` サブディレクトリーおよび ``host_vars`` サブディレクトリーは想定どおりに解釈されるため、インベントリーディレクトリーはさまざまな構成セットを整理するための強力な方法になります。詳細は :ref:`using_multiple_inventory_sources` を参照してください。

.. _static_groups_of_dynamic:

動的グループの静的グループ
===============================

静的インベントリーファイルでグループのグループを定義する場合は、
子グループも静的インベントリーファイルで定義する必要があります。
そうでない場合には、Ansible はエラーを返します。動的な子グループの静的グループを定義する場合は、
静的インベントリーファイルで動的グループを空として定義します。例:

.. code-block:: text

    [tag_Name_staging_foo]

    [tag_Name_staging_bar]

    [staging:children]
    tag_Name_staging_foo
    tag_Name_staging_bar


.. seealso::

   :ref:`intro_inventory`
       静的インベントリーファイルの詳細
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
