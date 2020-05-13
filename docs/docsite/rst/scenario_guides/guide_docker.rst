Docker ガイド
============

Ansible は、Docker コンテナーのオーケストレーションを行う以下のモジュールを提供します。

    docker_compose
        既存の Docker compose ファイルを使用して、
        1 つの Docker デーモンまたは Swarm でコンテナーのオーケストレーションを行います。Compose のバージョン 1 および 2 をサポートします。

    docker_container
        コンテナーを作成、更新、停止、開始、および破棄する機能を提供することにより、
        コンテナーのライフサイクルを管理します。

    docker_image
        構築、プル、プッシュ、タグ付け、削除など、イメージへの完全な制御を提供します。

    docker_image_info
        Docker ホストのイメージキャッシュ内の 1 つまたは複数のイメージを検査し、
        Playbook で決定またはアサーションを行うための情報を提供します。

    docker_login
        Docker Hub または Docker レジストリーで認証し、Docker Engine 設定ファイルを更新します。
        次に、レジストリーとの間でイメージをパスワードなしでプッシュおよびプルします。

    Docker (動的インベントリー)
        1 つ以上の Docker ホストセットから利用可能なすべてのコンテナーのインベントリーを動的に構築します。


Ansible 2.1.0 には Docker モジュールへのメジャーアップデートが含まれており、プロジェクトの開始をマークして、
コンテナーをオーケストレーションするための完全で統合されたツールセットを作成します。上記のモジュールに加えて、
次の作業も行っています。

イメージの構築に Dockerfile を使用していますか。`ansible-bender <https://github.com/ansible-community/ansible-bender>`_ を確認し、
Ansible Playbook からイメージのビルドを開始します。

`Ansible Operator <https://learn.openshift.com/ansibleop/ansible-operator-overview/>`_ を使用して、
`OpenShift <https://www.okd.io/>`_ で docker-compose ファイルを起動します。Kubernetes を使用すれば、ノートパソコンのアプリから、クラウドの完全にスケーラブルなアプリに、
ほんの数秒で移動できます。

計画は他にもあります。最新のアイディアや考え方は、「`Ansible の提案リポジトリー <https://github.com/ansible/proposals/tree/master/docker>`_」を参照してください。

要件
------------

Docker モジュールを使用するには、`Python 用の Docker SDK <https://docker-py.readthedocs.io/en/stable/>`_ を、
Ansible を実行しているホストにインストールする必要があります。1.7.0 以降がインストールされている必要があります。Python 2.7 または Python 3 では、
以下の方法でインストールできます。

.. code-block:: bash

    $ pip install docker

Python 2.6 では、2.0 より前のバージョンが必要です。SDK は、このバージョンでは ``docker-py`` と呼ばれていて、
以下のようにインストールする必要があります。

.. code-block:: bash

    $ pip install 'docker-py>=1.7.0'

``docker`` または ``docker-py`` のいずれか 1 つのみがインストールされている必要があることに注意してください。両方をインストールすると、
インストールは破損します。これが発生すると、Ansible はこれを検出し、これについて通知します::

    docker-py モジュールと docker python モジュールは、同じ名前空間を使用するため、
    両方インストールすると、インストールが破損します。両方のパッケージをアンインストールし、
    docker-py または docker python モジュールのいずれかを再インストールしてください。Python 2.6 のサポートが必要でない場合は、
    docker モジュールをインストールすることが推奨されます。いずれかのモジュールをアンインストールするだけでは、
    もう一方のモジュールが壊れた状態になる可能性があることに注意してください。

docker_compose モジュールには `docker-compose <https://github.com/docker/compose>`_も必要になります。

.. code-block:: bash

   $ pip install 'docker-compose>=1.7.0'


Docker API への接続
----------------------------

各タスクに渡されるパラメーターを使用するか、または環境変数を設定して、ローカルまたはリモートの API に接続できます。
優先順位は、コマンドラインパラメーター、次に環境変数です。コマンドラインオプションも環境変数も見つからない場合は、
デフォルト値が使用されます。デフォルト値は、
`Parameters`_ にあります。


Parameters
..........

以下のパラメーターを渡すことで、モジュールが Docker API に接続する方法を制御します。

    docker_host
        Docker API への接続に使用される URL または Unix ソケットパス。デフォルトは ``unix://var/run/docker.sock`` です。
        リモートホストに接続するには、TCP 接続文字列を指定します。たとえば、``tcp://192.0.2.23:2376`` です。API への接続を暗号化するために TLS を使用すると、
        モジュールは、
        「https」を使用した接続 URL の「tcp」を自動的に置き換えます。

    api_version
        Docker ホストで実行している Docker API のバージョン。デフォルトは、
        docker-py にサポートされる最新バージョンの API です。

    timeout
        API からの応答で待機する最大時間 (秒単位)。デフォルトは 60 秒です。

    tls
        Docker ホストサーバーの信頼性を検証せずに TLS を使用して API への接続を保護します。
        デフォルトは False です。

    tls_verify
        TLS を使用し、Docker ホストサーバーの信頼性を検証して、API への接続を保護します。
        デフォルトは False です。

    cacert_path
        CA 証明書ファイルへのパスを指定してサーバーの検証を実行する際に CA 証明書を使用します。

    cert_path
        クライアントの TLS 証明書ファイルへのパスです。

    key_path
        クライアントの TLS キーファイルへのパスです。

    tls_hostname
        Docker ホストサーバーの信頼性を検証する際に、予想されるサーバー名を指定します。デフォルトは、
        「localhost」です。

    ssl_version
        有効な SSL バージョン番号を指定します。本ガイドの作成時、docker-py により指定されるデフォルト値は、
        1.0 です。


環境変数
.....................

Ansible を実行しているホストの環境に以下の変数を設定して、
モジュールが Docker API に接続する方法を制御します。

    DOCKER_HOST
        Docker API への接続に使用される URL または Unix ソケットパス。

    DOCKER_API_VERSION
        Docker ホストで実行している Docker API のバージョン。デフォルトは、
        docker-py で対応している最新バージョンの API です。

    DOCKER_TIMEOUT
        API からの応答で待機する最大時間 (秒単位)。

    DOCKER_CERT_PATH
        クライアント証明書、クライアントキー、および CA 証明書を含むディレクトリーへのパス。

    DOCKER_SSL_VERSION
        有効な SSL バージョン番号を指定します。

    DOCKER_TLS
        Docker ホストの信頼性を検証せずに TLS を使用して API への接続のセキュリティーを保護します。

    DOCKER_TLS_VERIFY
        TLS を使用して API への接続のセキュリティーを確保し、Docker ホストの信頼性を確認します。


動的インベントリースクリプト
------------------------
インベントリースクリプトは、API 要求を複数の Docker API に指定して動的インベントリーを生成します。これは、
インベントリーを静的ファイルから読み取るのではなく、ランタイム時に生成されるため動的になります。このスクリプトでは、
1 つまたは多数の Docker API に接続し、各 API で見つかったコンテナーを検査することで、インベントリーが作成されます。スクリプトがどの API を接続するかは、
環境変数または設定ファイルを使用して定義できます。

グループ
......
このスクリプトは、以下のホストグループを作成します。

 - container id
 - container name
 - container short id
 - image_name (image_<image name>)
 - docker_host
 - running
 - stopped

例
........

コマンドラインからスクリプトをインタラクティブに実行したり、これをインベントリーとして Playbook に渡すことができます。以下に、
開始するための例をいくつか示します。

.. code-block:: bash

    # Connect to the Docker API on localhost port 4243 and format the JSON output
    DOCKER_HOST=tcp://localhost:4243 ./docker.py --pretty

    # Any container's ssh port exposed on 0.0.0.0 will be mapped to
    # another IP address (where Ansible will attempt to connect via SSH)
    DOCKER_DEFAULT_IP=192.0.2.5 ./docker.py --pretty

    # Run as input to a playbook:
    ansible-playbook -i ~/projects/ansible/contrib/inventory/docker.py docker_inventory_test.yml

    # Simple playbook to invoke with the above example:

        - name: Test docker_inventory, this will not connect to any hosts
          hosts: all
          gather_facts: no
          tasks:
            - debug: msg="Container - {{ inventory_hostname }}"

構成
.............
環境変数を定義するか、docker.yml ファイル (ansible/contrib/inventory で提供されるサンプル) を作成して、
インベントリースクリプトの動作を制御できます。優先順位は、docker.yml ファイル、
次に環境変数 です。


環境変数
;;;;;;;;;;;;;;;;;;;;;;

1 つの Docker API に接続するには、以下の変数を環境内で定義して、
接続オプションを制御できます。これは、Docker モジュールが使用するのと同じ環境変数です。

    DOCKER_HOST
        Docker API への接続に使用される URL または Unix ソケットパス。デフォルトは、unix://var/run/docker.sock です。

    DOCKER_API_VERSION:
        Docker ホストで実行している Docker API のバージョン。デフォルトは、
        docker-py で対応している最新バージョンの API です。

    DOCKER_TIMEOUT:
        API からの応答で待機する最大時間 (秒単位)。デフォルトは 60 秒です。

    DOCKER_TLS:
        Docker ホストサーバーの信頼性を検証せずに TLS を使用して API への接続を保護します。
        デフォルトは False です。

    DOCKER_TLS_VERIFY:
        TLS を使用し、Docker ホストサーバーの信頼性を検証して、API への接続を保護します。
        デフォルトは False です。

    DOCKER_TLS_HOSTNAME:
        Docker ホストサーバーの信頼性を検証する際に、予想されるサーバー名を指定します。デフォルトは、
        localhost です。

    DOCKER_CERT_PATH:
        クライアント証明書、クライアントキー、および CA 証明書を含むディレクトリーへのパス。

    DOCKER_SSL_VERSION:
        有効な SSL バージョン番号を指定します。本ガイドの作成時、docker-py により指定されるデフォルト値は、
        1.0 です。

接続変数に加えて、
スクリプトの実行と出力を制御するために使用される変数がいくつかあります。

    DOCKER_CONFIG_FILE
        設定ファイルへのパス。デフォルトは ./docker.yml です。

    DOCKER_PRIVATE_SSH_PORT:
        SSH が接続をリッスンしているプライベートポート (コンテナーポート)。デフォルトは 22 です。

    DOCKER_DEFAULT_IP:
        コンテナーの SSH ポートがインターフェース「0.0.0.0」にマッピングされる場合に ansible_host に割り当てる IP アドレス。


設定ファイル
;;;;;;;;;;;;;;;;;;

設定ファイルを使用すると、インベントリーを構築する Docker API のセットを定義する手段が提供されます。

ファイルのデフォルト名は、インベントリースクリプトの名前から取得します。デフォルトでは、
スクリプトは拡張子が「.yml」のスクリプト (つまり、docker) のベース名を検索します。

環境に DOCKER_CONFIG_FILE を定義することで、スクリプトのデフォルト名を上書きすることもできます。

docker_inventory.yml で定義できるものは、以下のとおりです。

    defaults
        デフォルト接続を定義します。デフォルトはこれから取得して、
        hosts リストで定義されたホストに提供されていない値に適用されます。

    hosts
        複数の Docker ホストからインベントリーを取得する必要がある場合は、hosts 一覧を定義します。

デフォルトのホスト、および hosts リストの各ホストに以下の属性を定義します。

.. code-block:: yaml

  host:
      description:The URL or Unix socket path used to connect to the Docker API.
      required: yes

  tls:
     description:Connect using TLS without verifying the authenticity of the Docker host server.
     default: false
     required: false

  tls_verify:
     description:Connect using TLS without verifying the authenticity of the Docker host server.
     default: false
     required: false

  cert_path:
     description:Path to the client's TLS certificate file.
     default: null
     required: false

  cacert_path:
     description:Use a CA certificate when performing server verification by providing the path to a CA certificate file.
     default: null
     required: false

  key_path:
     description:Path to the client's TLS key file.
     default: null
     required: false

  version:
     description:The Docker API version.
     required: false
     default: will be supplied by the docker-py module.

  timeout:
     description:The amount of time in seconds to wait on an API response.
     required: false
     default:60

  default_ip:
     description:The IP address to assign to ansible_host when the container's SSH port is mapped to interface
     '0.0.0.0'.
     required: false
     default:127.0.0.1

  private_ssh_port:
     description:The port containers use for SSH
     required: false
     default:22
