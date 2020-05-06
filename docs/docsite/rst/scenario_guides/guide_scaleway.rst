.. _guide_scaleway:

**************
Scaleway ガイド
**************

.. _scaleway_introduction:

はじめに
============

`Scaleway <https://scaleway.com>`_ は、動的インベントリープラグインおよびモジュールを介して Ansible (バージョン 2.6 以降) が対応するクラウドプロバイダーです。
このモジュールは次のような特長があります。

- :ref:`scaleway_sshkey_module`: ファイルまたは値から Packet インフラストラクチャーに公開 SSH キーを追加します。今後作成されるすべてのデバイスには、この公開鍵が .ssh/authorized_keys にインストールされています。
- :ref:`scaleway_compute_module`: は、Scaleway でサーバーを管理します。このモジュールを使用して、サーバーの作成、再起動、および削除を行うことができます。
- :ref:`scaleway_volume_module`: Scaleway でボリュームを管理します。

.. note::
   本ガイドは、Ansible とその仕組みに精通していることを前提とします。
   そうでない場合は、開始する前に :ref:`ansible_documentation` を確認してください。

.. _scaleway_requirements:

要件
============

Scaleway モジュールおよびインベントリースクリプトは、`Scaleway REST API <https://developer.scaleway.com>`_を使用して Scaleway API に接続します。
モジュールおよびインベントリースクリプトを使用するには、Scaleway API トークンが必要です。
API トークンは、`こちら <https://cloud.scaleway.com/#/credentials>`_ にある Scaleway コンソールを使用して生成できます。
自身を認証する最も簡単な方法は、環境変数に Scaleway API トークンを設定することです。

.. code-block:: bash

    $ export SCW_TOKEN=00000000-1111-2222-3333-444444444444

API トークンのエクスポートが不明な場合は、``api_token`` 引数を使用してこれをパラメーターとしてモジュールに渡すことができます。

このチュートリアルでは、新しい SSH キーペアを使用する場合は、以下のように ``./id_rsa`` および ``./id_rsa.pub`` に生成できます。

.. code-block:: bash

    $ ssh-keygen -t rsa -f ./id_rsa

既存のキーペアを使用する場合は、秘密鍵と公開鍵を Playbook ディレクトリーにコピーします。

.. _scaleway_add_sshkey:

SSH キーの追加方法
======================

Scaleway コンピュートノードへの接続は、Secure Shell を使用します。
SSH キーはアカウントレベルに保存されるため、同じ SSH キーを複数のノードで再利用できます。
Scaleway コンピュートリソースを設定する最初の手順は、少なくとも SSH キーを設定することです。

:ref:`scaleway_sshkey_module` は、Scaleway アカウントで SSH キーを管理するモジュールです。
以下のタスクを Playbook に追加することで、SSH キーをアカウントに追加できます。

.. code-block:: yaml

    - name:"Add SSH key"
      scaleway_sshkey:
        ssh_pub_key: "ssh-rsa AAAA..."
        state: "present"

``ssh_pub_key`` パラメーターには、ssh 公開鍵が文字列として含まれています。以下は、Playbook の例になります。


.. code-block:: yaml

    # SCW_API_KEY='XXX' ansible-playbook ./test/legacy/scaleway_ssh_playbook.yml

- name: Test SSH key lifecycle on a Scaleway account
  hosts: localhost
  gather_facts: no
  environment:
    SCW_API_KEY: ""

  tasks:

    - scaleway_sshkey:
        ssh_pub_key: "ssh-rsa AAAAB...424242 developer@example.com"
        state: present
      register: result

    - assert:
        that:
          - result is success and result is changed

.. _scaleway_create_instance:

コンピュートインスタンスの作成方法
=================================

これで SSH キーが設定されたので、次のステップとしてサーバーを起動します。
:ref:`scaleway_compute_module` は、Scaleway コンピュートインスタンスを作成、更新、および削除できるモジュールです。

.. code-block:: yaml

    - name:Create a server
      scaleway_compute:
        name: foobar
        state: present
        image:00000000-1111-2222-3333-444444444444
        organization:00000000-1111-2222-3333-444444444444
        region: ams1
        commercial_type:START1-S

以下は、上述のパラメーターの詳細です。

- ``name`` は、インスタンスの名前です (Web コンソールに表示される名前)。
- ``image`` は、使用するシステムイメージの UUID です。
  各アベイラビリティーゾーンには、利用可能なイメージの一覧があります。
- ``organization`` とは、自分のアカウントがアタッチされている組織を表します。
- ``region`` は、インスタンスが置かれているアベイラビリティーゾーンを表します (例: par1 および ams1)。
- ``commercial_type`` は販売サービスの名前を表します。
  Scaleway 価格ページでは、どのインスタンスが正しいかを確認できます。

次の短い Playbook で、``scaleway_compute`` を使用した作業例を確認します。

.. code-block:: yaml

    # SCW_TOKEN='XXX' ansible-playbook ./test/legacy/scaleway_compute.yml

- name: Test compute instance lifecycle on a Scaleway account
  hosts: localhost
  gather_facts: no
  environment:
    SCW_API_KEY: ""

  tasks:

    - name: Create a server
      register: server_creation_task
      scaleway_compute:
        name: foobar
        state: present
        image: 00000000-1111-2222-3333-444444444444
        organization: 00000000-1111-2222-3333-444444444444
        region: ams1
        commercial_type: START1-S
        wait: true

    - debug: var=server_creation_task

    - assert:
        that:
          - server_creation_task is success
          - server_creation_task is changed

    - name: Run it
      scaleway_compute:
        name: foobar
        state: running
        image: 00000000-1111-2222-3333-444444444444
        organization: 00000000-1111-2222-3333-444444444444
        region: ams1
        commercial_type: START1-S
        wait: true
        tags:
          - web_server
      register: server_run_task

    - debug: var=server_run_task

    - assert:
        that:
          - server_run_task is success
          - server_run_task is changed

.. _scaleway_dynamic_inventory_tutorial:

動的インベントリースクリプト
========================

Ansible には :ref:`scaleway_inventory` が同梱されています。
これで、このプラグインを介して Scaleway リソースの完全なインベントリーを取得し、各パラメーターで対象を絞ることができます (現在、``regions`` および ``tags`` に対応しています)。


例を作成してみましょう。
たとえば、タグ web_server のあるホストをすべて取得します。
以下の内容を含む ``scaleway_inventory.yml`` という名前のファイルを作成します。

.. code-block:: yaml

    plugin: scaleway
    regions:
      - ams1
      - par1
    tags:
      - web_server

このインベントリーは、ゾーン ``ams1`` および ``par1`` にタグ ``web_server`` のあるホストをすべて必要とすることを意味します。
このファイルを設定したら、以下のコマンドを使用して情報を取得できます。

.. code-block:: bash

    $ ansible-inventory --list -i scaleway_inventory.yml

出力は以下のようになります。

.. code-block:: yaml

    {
        "_meta": {
            "hostvars": {
                "dd8e3ae9-0c7c-459e-bc7b-aba8bfa1bb8d": {
                    "ansible_verbosity":6,
                    "arch": "x86_64",
                    "commercial_type":"START1-S",
                    "hostname": "foobar",
                    "ipv4":"192.0.2.1",
                    "organization":"00000000-1111-2222-3333-444444444444",
                    "state": "running",
                    "tags": [
                    "web_server"
                ]
                }
            }
        },
        "all": {
            "children": [
            "ams1",
            "par1",
            "ungrouped",
            "web_server"
        ]
        },
        "ams1": {},
        "par1": {
            "hosts": [
            "dd8e3ae9-0c7c-459e-bc7b-aba8bfa1bb8d"
        ]
        },
        "ungrouped": {},
        "web_server": {
            "hosts": [
            "dd8e3ae9-0c7c-459e-bc7b-aba8bfa1bb8d"
        ]
        }
    }
    
ここで示すとおり、ホストの異なるグループを取得します。
``par1`` および ``ams1`` は、場所に基づいてグループ化されます。
``web_server`` は、タグに基づくグループです。

フィルターパラメーターが定義されていないと、プラグインは可能な値をすべて必要であると想定します。
これは、Scaleway コンピュートノードに存在する各タグに対して、各タグに基づくグループが作成されることを意味します。

Scaleway S3 オブジェクトストレージ
==========================

`オブジェクトストレージ <https://www.scaleway.com/object-storage>`_ では、あらゆる種類のオブジェクト (ドキュメント、イメージ、ビデオなど) を保存できます。
Scaleway API は S3 と互換性があるため、Ansible は、:ref:`s3_bucket_module` モジュールと :ref:`aws_s3_module` モジュールを使用してネイティブに対応します。

``./test/legacy/roles/scaleway_s3`` にはサンプルが多数あります。

.. code-block:: yaml+jinja

    - hosts: myserver
      vars:
        scaleway_region: nl-ams
        s3_url: https://s3.nl-ams.scw.cloud
      environment:
        # AWS_ACCESS_KEY matches your scaleway organization id available at https://cloud.scaleway.com/#/account
    AWS_ACCESS_KEY: 00000000-1111-2222-3333-444444444444
    # AWS_SECRET_KEY matches a secret token that you can retrieve at https://cloud.scaleway.com/#/credentials
    AWS_SECRET_KEY: aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
  module_defaults:
    group/aws:
      s3_url: '{{ s3_url }}'
      region: '{{ scaleway_region }}'
  tasks:
   # use a fact instead of a variable, otherwise template is evaluate each time variable is used
    - set_fact:
        bucket_name: "{{ 99999999 | random | to_uuid }}"

    # "requester_pays:" is mandatory because Scaleway doesn't implement related API
    # another way is to use aws_s3 and "mode: create" !
    - s3_bucket:
        name: '{{ bucket_name }}'
        requester_pays:

    - name: Another way to create the bucket
      aws_s3:
        bucket: '{{ bucket_name }}'
        mode: create
        encrypt: false
      register: bucket_creation_check

    - name: add something in the bucket
      aws_s3:
        mode: put
        bucket: '{{ bucket_name }}'
        src: /tmp/test.txt  #  needs to be created before
        object: test.txt
        encrypt: false  # server side encryption must be disabled
