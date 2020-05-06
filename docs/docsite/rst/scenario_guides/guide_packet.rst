**********************************
Packet.net ガイド
**********************************

はじめに
============

`Packet.net <https://packet.net>`_ は、動的インベントリースクリプトと 2 つのクラウドモジュールを介して Ansible (>=2.3) が対応するベアメタルインフラストラクチャーホストです。2 つのモジュールは、以下の通りです。

- packet_sshkey - ファイルまたは値から Packet インフラストラクチャーに公開 SSH キーを追加します。今後作成されるすべてのデバイスには、この公開鍵が .ssh/authorized_keys にインストールされています。
- packet_device - Packet 上のサーバーを管理します。このモジュールを使用して、デバイスの作成、再起動、および削除を行うことができます。

本ガイドは、Ansible とその仕組みに精通していることを前提とします。そうでない場合は、作業を開始する前に :ref:`ドキュメント <ansible_documentation>` を確認してください。

要件
============

Packet モジュールおよびインベントリースクリプトは、packet-python パッケージを使用して Packet API に接続します。pip を使用してインストールできます。

.. code-block:: bash

    $ pip install packet-python

Packet で Ansible が作成したデバイスの状態を確認するには、`Packet CLI クライアント <https://www.packet.net/developers/integrations/>`_ のいずれかをインストールすることが推奨されます。そうでない場合は、`Packet ポータル <https://app.packet.net/portal>`_ で確認できます。

モジュールおよびインベントリースクリプトを使用するには、Packet API トークンが必要です。`こちら <https://app.packet.net/portal#/api-keys>`_ で Packet ポータルから API トークンを生成できます。自身を認証する最も簡単な方法は、環境変数に Packet API トークンを設定することです。

.. code-block:: bash

    $ export PACKET_API_TOKEN=Bfse9F24SFtfs423Gsd3ifGsd43sSdfs

API トークンのエクスポートが不明な場合は、これをパラメーターとしてモジュールに渡すことができます。

Packet では、デバイスと予約された IP アドレスは `プロジェクト <https://www.packet.net/developers/api/projects/>`_ に属します。Packet_device モジュールを使用するには、デバイスを作成または管理するプロジェクトの UUID を指定する必要があります。Packet ポータル (`こちら <https://app.packet.net/portal#/projects/list/table/>`_) (これはプロジェクトテーブルのすぐ下にあります) または利用可能な `CLI <https://www.packet.net/developers/integrations/>`_ のいずれを使用して、プロジェクトの UUID を確認できます。


このチュートリアルでは、新しい SSH キーペアを使用する場合は、以下のように ``./id_rsa`` および ``./id_rsa.pub`` に生成できます。

.. code-block:: bash

    $ ssh-keygen -t rsa -f ./id_rsa

既存のキーペアを使用する場合は、秘密鍵と公開鍵を Playbook ディレクトリーにコピーします。


デバイスの作成
===============

以下のコードブロックは、`Type 0 <https://www.packet.net/bare-metal/servers/type-0/>`_ サーバー (「plan」パラメーター) を作成する簡単な Playbook です。「plan」および「operating_system」を定義する必要があります。「location」は、「EWR1」 (Parsippany、NJ) に設定されます。`CLI クライアント` <https://www.packet.net/developers/integrations/>_ を使用して、パラメーターに使用できるすべての値を見つけることができます。

.. code-block:: yaml

    # playbook_create.yml

- name: create ubuntu device
  hosts: localhost
  tasks:

  - packet_sshkey:
      key_file: ./id_rsa.pub
      label: tutorial key

  - packet_device:
      project_id: <your_project_id>
      hostnames: myserver
      operating_system: ubuntu_16_04
      plan: baremetal_0
      facility: sjc1

``ansible-playbook playbook_create.yml`` の実行後に、サーバーが Packet でプロビジョニングされている必要があります。CLI または`Packet ポータル <https://app.packet.net/portal#/projects/list/table>`_ で検証できます。

エラーが発生し、"failed to set machine state present, error:Error 404:Not Found" メッセージが表示されたら、プロジェクト UUID を確認します。


デバイスの更新
================

Packet デバイスを一意に識別するために使用される 2 つのパラメーターは、「device_ids」および「hostnames」です。どちらのパラメーターも、1 つの文字 (後で単一の要素の一覧に変換) または文字列の一覧を受け入れます。

「device_ids」パラメーターおよび「hostnames」パラメーターは相互排他的です。以下の値はすべて受け入れ可能です。

- device_ids: a27b7a83-fc93-435b-a128-47a5b04f2dcf

- hostnames: mydev1

- device_ids: [a27b7a83-fc93-435b-a128-47a5b04f2dcf, 4887130f-0ccd-49a0-99b0-323c1ceb527b]

- hostnames: [mydev1, mydev2]

さらに、ホスト名には、簡単な名前と数字のパターンに従うホスト名を簡単に拡張できる「count」パラメーターとともに特別な「%d」フォーマッターを含めることができます。つまり、``hostnames: "mydev%d", count:2`` が [mydev1, mydev2] に展開します。

Playbook が既存の Packet デバイスで動作する場合は、「hostname」パラメーターおよび「device_ids」パラメーターのみを渡すことができます。以下の Playbook は、「hostname」パラメーターを設定して特定の Packet デバイスを再起動する方法を示しています。

.. code-block:: yaml

    # playbook_reboot.yml

- name: reboot myserver
  hosts: localhost
  tasks:

  - packet_device:
      project_id: <your_project_id>
      hostnames: myserver
      state: rebooted

「device_ids」パラメーターで特定の Packet デバイスを識別することもできます。デバイスの UUID は、`Packet ポータル <https://app.packet.net/portal>`_ または `CLI <https://www.packet.net/developers/integrations/>`_ を使用して確認できます。以下の Playbook は、「device_ids」フィールドを使用して Packet デバイスを削除します。

.. code-block:: yaml

    # playbook_remove.yml

- name: remove a device
  hosts: localhost
  tasks:

  - packet_device:
      project_id: <your_project_id>
      device_ids: <myserver_device_id>
      state: absent


より複雑な Playbook
======================

この例では、`ユーザーデータ<https://support.packet.com/kb/articles/user-data>`_ で CoreOS クラスターを作成します。


CoreOS クラスターは、クラスター内の他のサーバーの検出に `etcd <https://coreos.com/etcd/>`_ を使用します。サーバーをプロビジョニングする前に、クラスターの検出トークンを生成する必要があります。

.. code-block:: bash

    $ curl -w "\n" 'https://discovery.etcd.io/new?size=3'

以下の Playbook は、SSH キー、3 台の Packet サーバーを作成し、SSH の準備ができるまで (または 5 分経過するまで) 待ちます。``ansible-playbook`` を実行する前に、「user_data」の検出トークン URL と「project_id」を置き換えてください。また、「plan」および「facility」は自由に変更してください。

.. code-block:: yaml

    # playbook_coreos.yml

- name: Start 3 CoreOS nodes in Packet and wait until SSH is ready
  hosts: localhost
  tasks:

  - packet_sshkey:
      key_file: ./id_rsa.pub
      label: new

  - packet_device:
      hostnames: [coreos-one, coreos-two, coreos-three]
      operating_system: coreos_beta
          plan: baremetal_0
          facility: ewr1
          project_id: <your_project_id>
      wait_for_public_IPv:4
          user_data: |
            #cloud-config
        coreos:
          etcd2:
            discovery: https://discovery.etcd.io/<token>
            advertise-client-urls: http://$private_ipv4:2379,http://$private_ipv4:4001
            initial-advertise-peer-urls: http://$private_ipv4:2380
            listen-client-urls: http://0.0.0.0:2379,http://0.0.0.0:4001
            listen-peer-urls: http://$private_ipv4:2380
          fleet:
            public-ip: $private_ipv4
          units:
            - name: etcd2.service
              command: start
            - name: fleet.service
              command: start
    register: newhosts

  - name: wait for ssh
    wait_for:
      delay: 1
      host: "{{ item.public_ipv4 }}"
      port: 22
      state: started
      timeout: 500
    loop: "{{ newhosts.results[0].devices }}"
    

ほとんどの Ansible モジュールと同様に、Packet モジュールのデフォルト状態は冪等です。つまり、プロジェクトのリソースは Playbook の再実行後も同じになります。したがって、Playbook で ``packet_sshkey`` モジュール呼び出しを保持できます。公開鍵がすでに Packet アカウントにある場合、呼び出しは機能しません。

次のモジュール呼び出しは、「project_id」パラメーターで識別されるプロジェクトの 3 Packet タイプ 0 (「plan」パラメーターで指定) サーバーをプロビジョニングします。サーバーはすべて CoreOS ベータでプロビジョニングされ (「operating_system」パラメーター)、「user_data」パラメーターに渡される cloud-config ユーザーデータでカスタマイズされます。

``packet_device`` モジュールには、待機する IP アドレスのバージョンを指定するために使用される ``wait_for_public_IPv`` があります (有効な値は、IPv4 または IPv6 である ``4`` または ``6``)。これが指定されている場合、Ansible はデバイスの GET API 呼び出しに指定バージョンのインターネットルーティング可能な IP アドレスが含まれるまで待機します。後続のモジュール呼び出しで作成されたデバイスの IP アドレスを参照する場合は、packet_device モジュール呼び出しで ``wait_for_public_IPv`` パラメーターまたは ``state: active`` を使用することが推奨されます。

Playbook を実行します。

.. code-block:: bash

    $ ansible-playbook playbook_coreos.yml

Playbook が終了すると、SSH 経由で新しいデバイスに到達できるようになります。接続して、etcd が正常に起動したかどうかを確認します。

.. code-block:: bash

    tomk@work $ ssh -i id_rsa core@$one_of_the_servers_ip
core@coreos-one ~ $ etcdctl cluster-health

いくつかのデバイスを作成したら、動的インベントリースクリプトを利用できます。


動的インベントリースクリプト
========================

動的インベントリースクリプトは、ホストの一覧に Packet API をクエリーし、これを Ansible に公開して、Packet デバイスを簡単に識別し、操作できるようにします。これは、`contrib/inventory/packet_net.py <https://github.com/ansible/ansible/blob/devel/contrib/inventory/packet_net.py>`_ の Ansible の git リポジトリーにあります。

インベントリースクリプトは `ini ファイル <https://github.com/ansible/ansible/blob/devel/contrib/inventory/packet_net.ini>`_ で設定可能です。

インベントリースクリプトを使用する場合には、最初に Packet API トークンを PACKET_API_TOKEN 環境変数にエクスポートする必要があります。

インベントリーおよび ini 設定をクローンされた git リポジトリーからコピーするか、以下のように作業ディレクトリーにダウンロードできます。

.. code-block:: bash

    $ wget https://github.com/ansible/ansible/raw/devel/contrib/inventory/packet_net.py
$ chmod +x packet_net.py
$ wget https://github.com/ansible/ansible/raw/devel/contrib/inventory/packet_net.ini

インベントリースクリプトが Ansible に与える影響を理解するために、次を実行できます。

.. code-block:: bash

    $ ./packet_net.py --list

以下のトリムされたディクショナリーのような JSON ドキュメントを出力する必要があります。

.. code-block:: json

    {
      "_meta": {
        "hostvars": {
          "147.75.64.169": {
            "packet_billing_cycle": "hourly",
            "packet_created_at":"2017-02-09T17:11:26Z",
            "packet_facility": "ewr1",
            "packet_hostname": "coreos-two",
            "packet_href": "/devices/d0ab8972-54a8-4bff-832b-28549d1bec96",
            "packet_id": "d0ab8972-54a8-4bff-832b-28549d1bec96",
            "packet_locked": false,
            "packet_operating_system": "coreos_beta",
            "packet_plan": "baremetal_0",
            "packet_state": "active",
            "packet_updated_at":"2017-02-09T17:16:35Z",
            "packet_user": "core",
            "packet_userdata": "#cloud-config\ncoreos:\n  etcd2:\n    discovery: https://discovery.etcd.io/e0c8a4a9b8fe61acd51ec599e2a4f68e\n    advertise-client-urls: http://$private_ipv4:2379,http://$private_ipv4:4001\n    initial-advertise-peer-urls: http://$private_ipv4:2380\n    listen-client-urls: http://0.0.0.0:2379,http://0.0.0.0:4001\n    listen-peer-urls: http://$private_ipv4:2380\n  fleet:\n    public-ip: $private_ipv4\n  units:\n    - name: etcd2.service\n      command: start\n    - name: fleet.service\n      command: start"
      }
    }
  },
  "baremetal_0": [
    "147.75.202.255",
    "147.75.202.251",
    "147.75.202.249",
    "147.75.64.129",
    "147.75.192.51",
    "147.75.64.169"
  ],
      "coreos_beta": [
    "147.75.202.255",
    "147.75.202.251",
    "147.75.202.249",
    "147.75.64.129",
    "147.75.192.51",
    "147.75.64.169"
  ],
      "ewr1": [
    "147.75.64.129",
    "147.75.192.51",
    "147.75.64.169"
  ],
      "sjc1": [
    "147.75.202.255",
    "147.75.202.251",
    "147.75.202.249"
  ],
      "coreos-two": [
    "147.75.64.169"
  ],
      "d0ab8972-54a8-4bff-832b-28549d1bec96": [
    "147.75.64.169"
  ]
    }
    
``['_meta']['hostvars']`` キーには、デバイスの一覧 (特にパブリック IPv4 アドレスで識別されるもの) とそのパラメーターがあります。``['_meta']`` 以下のその他のキーは、一部のパラメーターでグループ分けされたデバイスの一覧です。これはタイプ (すべてのデバイスの種類は baremetal_0)、オペレーティングシステム、およびファシリティー (ewr1 および sjc1) です。

パラメーターグループの他に、デバイスの UUID またはホスト名を持つ 1 項目グループもあります。

Playbook でグループを対象にすることができるようになりました。以下の Playbook は、Ansible ターゲットのリソースを「coreos_beta」グループのすべてのデバイスに提供するロールをインストールします。

.. code-block:: yaml

    # playbook_bootstrap.yml

- hosts: coreos_beta
  gather_facts: false
  roles:
    - defunctzombie.coreos-boostrap

``-i`` 引数に動的インベントリーを指定することを忘れないでください。

.. code-block:: bash

    $ ansible-playbook -u core -i packet_net.py playbook_bootstrap.yml


ご質問やご感想は、help@packet.net までご連絡ください。
