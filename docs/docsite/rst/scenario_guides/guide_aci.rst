.. _aci_guide:

Cisco ACI ガイド
===============


.. _aci_guide_intro:

Cisco ACI とは
-------------------

Application Centric Infrastructure (ACI)
........................................
ACI (Cisco Application Centric Infrastructure) を使用すると、アプリケーション要件でネットワークを定義できます。このアーキテクチャーは、アプリケーションのデプロイメントライフサイクル全体を単純化し、最適化し、加速化します。


Application Policy Infrastructure Controller (APIC)
...................................................
APIC は、スケーラブルな ACI マルチテナントファブリックを管理します。APIC は、ファブリックの自動化と管理、ポリシープログラミング、アプリケーションのデプロイメント、ヘルスモニタリングの統合ポイントを提供します。複製された同期クラスターコントローラーとして実装される APIC は、パフォーマンスを最適化し、任意のアプリケーションをどこでもサポートし、物理インフラストラクチャーおよび仮想インフラストラクチャーの統一された操作を提供します。

APIC により、ネットワーク管理者はアプリケーションに最適なネットワークを簡単に定義できます。データセンターオペレーターは、アプリケーションがネットワークリソースをどのように消費するか、アプリケーションとインフラストラクチャーの問題を簡単に分離してトラブルシューティングし、リソース使用状況パターンを監視およびプロファイルできます。

APIC (Cisco Application Policy Infrastructure Controller) API を使用すると、アプリケーションと、ネットワーク、コンピュート、およびストレージの機能を含む、安全で共有されている高性能リソースプールを直接接続できます。


ACI Fabric
..........
ACI (Cisco Application Centric Infrastructure) Fabric には、Cisco Nexus 9000 シリーズスイッチと、リーフ/スパインの ACI fabric モードで実行する APIC が含まれます。これらのスイッチは、各リーフノードを各スパインノードに接続し、その他のデバイスはリーフノードに接続することで「fat-tree」ネットワークを形成します。APIC は ACI ファブリックを管理します。

ACI ファブリックは、高帯域幅のリンクで一貫した低レイテンシー転送を提供します (40 Gbps、100-Gbps の将来の能力)。送信元および宛先が同じリーフスイッチにあるトラフィックはローカルで処理され、他のすべてのトラフィックはスパインスイッチを介して 入力リーフから出力リーフに送信されます。このアーキテクチャーは、物理的には 2 つのホップとして表示されますが、このファブリックが単一のレイヤー 3 スイッチとして機能するため、実際には単一のレイヤー 3 ホップとなります。

ACI ファブリックオブジェクト指向のオペレーティングシステム (OS) は、それぞれの Cisco Nexus 9000 シリーズノードで実行されます。システムの設定可能な各要素のオブジェクトのプログラミングを有効にします。ACI ファブリック OS は、APIC からのポリシーを物理インフラストラクチャーで実行される具体的なモデルにレンダリングします。具体的なモデルは、コンパイルされたソフトウェアに似ています。これは、スイッチオペレーティングシステムを実行できるモデルの形式です。

すべてのスイッチノードには、具体的なモデルの完全なコピーが含まれます。管理者が設定を表す APIC にポリシーを作成すると、APIC は論理モデルを更新します。その後、APIC は、具体的なモデルが更新されるすべてのスイッチノードにプッシュされる完全に改良されたポリシーを作成する中間ステップを実行します。

APIC は、ファブリックのアクティブ化、ファームウェア管理の切り替え、ネットワークポリシーの設定、およびインスタンス化を行います。APIC はそのファブリックの集中管理ポリシーおよびネットワーク管理エンジンとして機能しますが、転送トポロジーを含むデータパスから完全に削除されます。したがって、ファブリックは APIC との通信が失われてもトラフィックを転送できます。


詳細情報
................
ACI の学習を開始するためのさまざまなリソースが存在します。ここでは、コミュニティーからの興味のある記事の一覧を記載しています。

- `Adam Raffe:Learning ACI <https://adamraffe.com/learning-aci/>`_
- `Luca Relandini:ACI for dummies <https://lucarelandini.blogspot.be/2015/03/aci-for-dummies.html>`_
- `Cisco DevNet Learning Labs about ACI <https://learninglabs.cisco.com/labs/tags/ACI>`_


.. _aci_guide_modules:

ACI モジュールの使用
---------------------
Ansible ACI モジュールは、Ansible Playbook を使用して ACI 環境を管理するユーザーフレンドリーなインターフェースを提供します。

たとえば、特定のテナントが存在することを確認するには、モジュール :ref:`aci_tenant <aci_tenant_module>` を使用して以下の Ansible タスクを使用します。

.. code-block:: yaml

    - name:Ensure tenant customer-xyz exists
      aci_tenant:
        host: my-apic-1
        username: admin
        password: my-password
    
        tenant: customer-xyz
        description:Customer XYZ
        state: present

既存の ACI モジュールの完全な一覧は、:ref:`ネットワークモジュール一覧<network_modules>` にある最新の安定したリリースで利用できます。`現在の開発バージョン <https://docs.ansible.com/ansible/devel/modules/list_of_network_modules.html#aci>`_ を表示することもできます。

独自の ACI モジュールを作成して貢献する方法を学ぶ場合は、「:ref:`Cisco ACI モジュールの開発 <aci_dev_guide>`」セクションを参照してください。

ACI 設定のクエリー
..........................

モジュールは、特定のオブジェクトのクエリーにも使用できます。

.. code-block:: yaml

    - name: Query tenant customer-xyz
      aci_tenant:
        host: my-apic-1
        username: admin
        password: my-password
    
        tenant: customer-xyz
        state: query
      register: my_tenant

または、すべてのオブジェクトをクエリーします。

.. code-block:: yaml

    - name: Query all tenants
      aci_tenant:
        host: my-apic-1
        username: admin
        password: my-password
    
        state: query
      register: all_tenants

上記のように :ref:`aci_tenant <aci_tenant_module>` タスクの戻り値を登録した後、変数 ``all_tenants`` からすべてのテナント情報にアクセスできます。


コントローラーでローカルに実行
.................................
最初に設計されたように、Ansible モジュールはリモートターゲットに同梱され、実行されますが、ACI モジュール (ほとんどのネットワーク関連モジュールなど) はネットワークデバイスやコントローラー (この場合は APIC) では動作しませんが、APIC の REST インターフェースと直接対話します。

このため、モジュールはローカルの Ansible コントローラーで実行する必要があります (または、APIC に *接続できる* 別のシステムに委譲されます)。


ファクトの収集
```````````````
Ansible コントローラーでモジュールを実行するため、収集ファクトは機能しません。そのため、これらの ACI モジュールを使用する場合はファクトの収集を無効にする必要があります。これは、``ansible.cfg`` でグローバルに行うことも、すべてのプレイに ``gather_facts: no`` を追加して実行することもできます。

.. code-block:: yaml
   :emphasize-lines: 3

    - name: Another play in my playbook
      hosts: my-apic-1
      gather_facts: no
      tasks:
      - name: Create a tenant
        aci_tenant:
          ...

ローカルホストへの委譲
```````````````````````
そのため、以下に示すように、FQDN 名を ``ansible_host`` 値として使用し、ターゲットをインベントリーに設定したと仮定します。

.. code-block:: yaml
   :emphasize-lines: 3

    apics:
      my-apic-1:
        ansible_host: apic01.fqdn.intra
        ansible_user: admin
        ansible_password: my-password

これを設定する方法は、ディレクティブのすべてのタスク (``delegate_to: localhost``) に追加することです。

.. code-block:: yaml
   :emphasize-lines: 8

    - name: Query all tenants
      aci_tenant:
        host: '{{ ansible_host }}'
        username: '{{ ansible_user }}'
        password: '{{ ansible_password }}'
    
        state: query
      delegate_to: localhost
      register: all_tenants
    
このディレクティブの追加を忘れると、Ansible は SSH を使用して APIC への接続を試み、モジュールのコピーとリモート実行を試行します。これはクリアエラーで失敗しますが、一部の混乱が生じる可能性があります。


ローカル接続方法の使用
`````````````````````````````````
よく使用される別のオプションは、``ローカル`` 接続方法をこのターゲットに結び付けることです。これにより、このターゲットの後続のすべてのタスクでローカル接続方法が使用されます (したがって、SSH を使用するのではなくローカルで実行します)。

この場合、インベントリーは以下のようになります。

.. code-block:: yaml
   :emphasize-lines:6

    apics:
      my-apic-1:
        ansible_host: apic01.fqdn.intra
        ansible_user: admin
        ansible_password: my-password
        ansible_connection: local

ただし、使用したタスクには特別な追加は必要ありません。

.. code-block:: yaml

    - name: Query all tenants
      aci_tenant:
        host: '{{ ansible_host }}'
        username: '{{ ansible_user }}'
        password: '{{ ansible_password }}'
    
        state: query
      register: all_tenants
    
.. hint:: 分かりやすくするために、モジュールドキュメントのすべての例に ``delegate_to: localhost`` を追加しました。これにより、初回のユーザーが簡単に一部をコピーして、最低限の努力で作業できるようになります。


一般的なパラメーター
.................
すべての Ansible ACI モジュールは、APIC REST API を使用したモジュールの通信に影響を与える以下のパラメーターを受け入れます。

    host
        APIC のホスト名または IP アドレス。

    port
        通信に使用するポート。(デフォルトは、HTTPS の場合は ``443`、HTTP の場合は ``80``)

    username
        APIC にログインするのに使用されるユーザー名。(デフォルトは ``admin``)

    password
        パスワードベースの認証を使用して APIC にログインする ``username`` のパスワード。

    private_key
        署名ベースの認証を使用して APIC にログインする ``username`` の秘密鍵。
        これは、(ヘッダー/フットプリントを含む) 生の秘密鍵コンテンツ、または鍵コンテンツを格納するファイルのいずれかになります。
        *バージョン 2.5 の新機能* です。

    certificate_name
        ACI Web GUI での証明書の名前。
        デフォルトは ``username`` の値または ``private_key`` ファイルベース名のいずれかになります。
        *バージョン 2.5 の新機能* です。

    timeout
        ソケットレベルの通信のタイムアウト値。

    use_proxy
        システムプロキシー設定を使用します。(``yes`` にデフォルト設定)

    use_ssl
        APIC REST 通信には HTTPS または HTTP を使用します。(``yes`` にデフォルト設定)

    validate_certs
        HTTPS 通信を使用する場合に証明書を検証します。(``yes`` にデフォルト設定)

    output_level
        詳細な ACI モジュールがユーザーに返るレベルに影響します。( ``normal``、``info``、``debug`` のいずれか) *バージョン 2.5 での新機能* です。


プロキシーのサポート
.............
デフォルトでは、環境変数 ``<protocol>_proxy`` がターゲットホストに設定されていると、要求はそのプロキシー経由で送信されます。この動作は、このタスクに変数を設定して上書きするか (:ref:`playbooks_environment` を参照)、``use_proxy`` モジュールパラメーターを使用して上書きできます。

HTTP リダイレクトは HTTP から HTTPS へリダイレクトできるため、両方のプロトコルのプロキシー環境が正しく設定されていることを確認します。

プロキシーサポートが必要なくても、システムがそれを設定する可能性がある場合は、``use_proxy: no`` パラメーターを使用して、誤ったシステムプロキシーの使用を回避します。

.. hint:: ``no_proxy`` 環境変数を使用した選択的プロキシーサポートにも対応しています。


戻り値
.............

バージョン 2.5 における新機能

以下の値が常に返されます。

    current
        管理オブジェクトの結果の状態、またはクエリーの結果。

``output_level: info`` の場合に以下の値が返されます。

    previous
        管理オブジェクトの元の状態 (変更を行う前)。

    proposed
        ユーザーが指定した値に基づく、提案された設定ペイロード。

    sent
        ユーザーが指定した値、および既存の設定に基づく、送信された設定ペイロード。

``output_level: debug`` または ``ANSIBLE_DEBUG=1`` の場合に、以下の値が返されます。

    filter_string
        特定の APIC クエリーに使用されるフィルター。

    method
        送信されたペイロードに使用される HTTP メソッド。(クエリーの場合は ``GET``、変更の場合は ``DELETE`` または ``POST``)

    response
        APIC からの HTTP 応答。

    status
        要求の HTTP ステータスコード。

    url
        要求に使用される URL。

.. note:: モジュールの戻り値は、各モジュールのドキュメントで詳細に説明されています。


詳細情報
................
ACI プログラミングの詳細を学ぶために、さまざまなリソースがあります。以下のリンクが推奨されます。

- :ref:`Cisco ACI モジュールの開発 <aci_dev_guide>`
- `Jacob McGill:Automating Cisco ACI with Ansible <https://blogs.cisco.com/developer/automating-cisco-aci-with-ansible-eliminates-repetitive-day-to-day-tasks>`_
- `Cisco DevNet Learning Labs about ACI and Ansible <https://learninglabs.cisco.com/labs/tags/ACI,Ansible>`_


.. _aci_guide_auth:

ACI 認証
------------------

パスワードベースの認証
.............................
ユーザー名とパスワードを使用してログインする場合は、ACI モジュールで以下のパラメーターを使用できます。

.. code-block:: yaml

    username: admin
    password: my-password

パスワードベースの認証は非常に簡単に機能しますが、別のログイン要求とオープンセッションが機能する必要があるため、ACI の観点から最も効率的な認証形式ではありません。セッションのタイムアウトや別のログインを必要としないように、より効率的な署名ベースの認証を使用できます。

.. note:: パスワードベースの認証では、ACI v3.1 以降の DoS 対策がトリガーとなり、セッションスロットルが発生し、HTTP 503 エラーとなり、ログインが失敗する可能性があります。

.. warning:: プレーンテキストにパスワードを保存しないでください。

Ansible の「Vault」機能を使用すると、パスワードやキーなどの機密データを、Playbook やロールのプレーンテキストとしてではなく、暗号化されたファイルに保存できます。この vault ファイルは、ソース制御に配布または配置することができます。詳細は「:ref:`playbooks_vault`」を参照してください。


証明書を使用した署名ベースの認証
.................................................

バージョン 2.5 における新機能

署名ベースの認証の使用は、パスワードベースの認証よりも効率的で、信頼性が高くなります。

証明書と秘密鍵の生成
````````````````````````````````````
署名ベースの認証では、秘密鍵を持つ (自己署名) X.509 証明書と、ACI の AAA ユーザーの設定手順が必要になります。稼働中の X.509 証明書と秘密鍵を生成するには、以下の手順に従います。

.. code-block:: bash

    $ openssl req -new -newkey rsa:1024 -days 36500 -nodes -x509 -keyout admin.key -out admin.crt -subj '/CN=Admin/O=Your Company/C=US'

ローカルユーザーの設定
`````````````````````````
以下の手順を実行します。

- :guilabel:`ADMIN` » :guilabel:`AAA` で ACI AAA ローカルユーザーに X.509 証明書を追加します。
- :guilabel:`AAA Authentication` をクリックします。
- :guilabel:`Authentication` フィールドの :guilabel:`Realm` フィールドに :guilabel:`Local` が表示されることを確認します。
- :guilabel:`Security Management`、:guilabel:`Local Users` の順に展開します。
- :guilabel:`User Certificates` エリアで、証明書を追加するユーザー名をクリックします。
- :guilabel:`+` 記号をクリックし、:guilabel:`Create X509 Certificate` の :guilabel:`Name` フィールドに証明書名を入力します。

  * ここで秘密鍵の basename を使用する場合は、Ansible で ``certificate_name`` を入力する必要はありません。

- :guilabel:`Data` フィールドに X.509 証明書をコピーして貼り付けます。

これは、以下の Ansible タスクを使用して自動化できます。

.. code-block:: yaml

    - name: Ensure we have a certificate installed
      aci_aaa_user_certificate:
        host: my-apic-1
        username: admin
        password: my-password
    
        aaa_user: admin
        certificate_name: admin
        certificate: "{{ lookup('file', 'pki/admin.crt') }}"  # This will read the certificate data from a local file

.. note:: 署名ベースの認証は、ローカルユーザーでのみ機能します。


Ansible での署名ベースの認証の使用
```````````````````````````````````````````````
これを有効にするには、ACI モジュールで以下のパラメーターが必要です。

.. code-block:: yaml
   :emphasize-lines:2,3

    username: admin
    private_key: pki/admin.key
    certificate_name: admin  # This could be left out !

または、秘密鍵のコンテンツを使用できます。

.. code-block:: yaml
   :emphasize-lines: 2,3

    username: admin
    private_key: |
        -----BEGIN PRIVATE KEY-----
        <<your private key content>>
        -----END PRIVATE KEY-----
    certificate_name: admin  # This could be left out !


.. hint:: 秘密鍵の basename に一致する ACI で証明書名を使用する場合は、上記の例のような ``certificate_name`` パラメーターを省略できます。


Ansible Vault を使用した秘密鍵の暗号化
``````````````````````````````````````````````
バージョン 2.8 における新機能

まず、秘密鍵を暗号化して強固なパスワードを付与します。

.. code-block:: bash

    ansible-vault encrypt admin.key

テキストエディターを使用して、private-key を開きます。これで、暗号化された証明書が存在するはずです。

.. code-block:: bash

    $ANSIBLE_VAULT;1.1;AES256
    56484318584354658465121889743213151843149454864654151618131547984132165489484654
    45641818198456456489479874513215489484843614848456466655432455488484654848489498
    ....

新しい暗号化された証明書を新規の変数として Playbook にコピーアンドペーストします。 

.. code-block:: yaml

    private_key: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          56484318584354658465121889743213151843149454864654151618131547984132165489484654
          45641818198456456489479874513215489484843614848456466655432455488484654848489498
          ....

private_key の新しい変数を使用します。

.. code-block:: yaml

    username: admin
    private_key: "{{ private_key }}"
    certificate_name: admin  # This could be left out !

Playbook の実行時に、「--ask-vault-pass」を使用して秘密鍵を復号します。

.. code-block:: bash

    ansible-playbook site.yaml --ask-vault-pass


詳細情報
````````````````
- 署名ベースの認証に関する詳細情報は、「`Cisco APIC Signature-Based Transactions` <https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/kb/b_KB_Signature_Based_Transactions.html>_」を参照してください。
- Ansible Vault の詳細は、「:ref:`Ansible Vault <vault>`」ページを参照してください。


.. _aci_guide_rest:

Ansible での ACI REST の使用
---------------------------
すでに多くの ACI モジュールが Ansible ディストリビューションに存在し、最も一般的なアクションはこれらの既存のモジュールで実行できますが、既製のモジュールでは不可能なことは常にあります。

:ref:`aci_rest <aci_rest_module>` モジュールを使用すると、APIC REST API に直接アクセスでき、既存のモジュールで対応していないタスクを実行できます。これは複雑な作業のように思えるかもしれませんが、ACI Web インターフェースで実行されるアクションに必要な REST ペイロードを簡単に生成できます。


組み込みの冪等性
....................
APIC REST API は冪等であり、変更されたかどうかを報告することができるため、:ref:`aci_rest <aci_rest_module>` モジュールは両方の機能を自動的に継承し、ACI インフラストラクチャーを自動化するファーストクラスソリューションとなります。その結果、ACI インフラストラクチャーへのより強力な低レベルアクセスを必要とするユーザーは、冪等性をあきらめる必要がなく、:ref:`aci_rest <aci_rest_module>` モジュールの使用時に変更が行われたかどうかを推測する必要もありません。


aci_rest モジュールの使用
.........................
:ref:`aci_rest <aci_rest_module>` モジュールはネイティブの XML ペイロードおよび JSON ペイロードを受け入れますが、(JSON などの) インライン YAML ペイロードも追加で受け入れます。XML ペイロードでは、``.xml`` で終わるパスを使用する必要がありますが、JSON または YAML には ``.json`` で終わるパスが必要です。

変更を行う場合は、POST メソッドまたは DELETE メソッドを使用できますが、クエリーのみを実行するには GET メソッドが必要です。

たとえば、特定のテナントが ACI に存在することを確認する場合は、以下の 4 つの例が機能的に同じです。

**XML** (ネイティブの ACI REST)

.. code-block:: yaml

    - aci_rest:
        host: my-apic-1
        private_key: pki/admin.key
    
        method: post
        path: /api/mo/uni.xml
        content: |
          <fvTenant name="customer-xyz" descr="Customer XYZ"/>

**JSON** (ネイティブの ACI REST)

.. code-block:: yaml

    - aci_rest:
        host: my-apic-1
        private_key: pki/admin.key
    
        method: post
        path: /api/mo/uni.json
        content:
          {
            "fvTenant": {
              "attributes": {
                "name": "customer-xyz",
                "descr": "Customer XYZ"
              }
            }
          }

**YAML** (Ansible スタイルの REST)

.. code-block:: yaml

    - aci_rest:
        host: my-apic-1
        private_key: pki/admin.key
    
        method: post
        path: /api/mo/uni.json
        content:
          fvTenant:
            attributes:
              name: customer-xyz
              descr:Customer XYZ

**Ansible タスク** (専用モジュール)

.. code-block:: yaml

    - aci_tenant:
        host: my-apic-1
        private_key: pki/admin.key
    
        tenant: customer-xyz
        description:Customer XYZ
        state: present


.. hint:: XML 形式は、REST ペイロード (インライン) のテンプレートが必要な場合にはより実用的なものですが、YAML 形式は infrastructure-as-code を維持し、Ansible Playbook とより正確に統合されます。専用モジュールは、よりシンプルで抽象化されたモジュールを提供しますが、より限定的なエクスペリエンスも提供します。ユースケースに最適なものを使用してください。


詳細情報
................
ACI の APIC REST インターフェースを学ぶためのリソースは多数あります。以下のリンクが推奨されます。

- :ref:`aci_rest モジュールのドキュメント <aci_rest_module>`
- `APIC REST API Configuration Guide <https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/2-x/rest_cfg/2_1_x/b_Cisco_APIC_REST_API_Configuration_Guide.html>`_ - APIC REST API の設計方法と使用方法に関する詳細ガイド (多数のサンプルを含む)
- `APIC Management Information Model reference <https://developer.cisco.com/docs/apic-mim-ref/>`_ - APIC オブジェクトモデルの完全リファレンス
- `ACI および REST の Cisco DevNet ラーニングラボ <https://learninglabs.cisco.com/labs/tags/ACI,REST>`_


.. _aci_guide_ops:

運用例
--------------------
以下は、Playbook で再利用するのに役立つ運用タスクの概要です。

より有用なスニペットを自由に投稿してください。


すべてのコントローラーの準備が整うまで待機
.......................................
APIC の構築を開始し、すべての APIC がオンラインになるまで待機するようにクラスターを設定したら、以下のタスクを使用できます。これは、コントローラーの数が ``apic`` インベントリーに挙げられている数と等しくなるまで待機します。

.. code-block:: yaml

    - name:Waiting for all controllers to be ready
      aci_rest:
        host: my-apic-1
        private_key: pki/admin.key
        method: get
        path: /api/node/class/topSystem.json?query-target-filter=eq(topSystem.role,"controller")
      register: topsystem
      until: topsystem|success and topsystem.totalCount|int >= groups['apic']|count >= 3
      retries:20
      delay:30


クラスターが完全に適合するまで待機
...................................
以下の例では、クラスターが完全に調整されるまで待機します。この例では、クラスター内の APIC の数を把握し、各 APIC が「完全に適切な」ステータスを報告することを確認します。

.. code-block:: yaml

    - name:Waiting for cluster to be fully-fit
      aci_rest:
        host: my-apic-1
        private_key: pki/admin.key
        method: get
        path: /api/node/class/infraWiNode.json?query-target-filter=wcard(infraWiNode.dn,"topology/pod-1/node-1/av")
      register: infrawinode
      until: >
        infrawinode|success and
        infrawinode.totalCount|int >= groups['apic']|count >= 3 and
        infrawinode.imdata[0].infraWiNode.attributes.health == 'fully-fit' and
        infrawinode.imdata[1].infraWiNode.attributes.health == 'fully-fit' and
        infrawinode.imdata[2].infraWiNode.attributes.health == 'fully-fit'
      retries:30
      delay:30


.. _aci_guide_errors:

APIC エラーメッセージ
-------------------
以下のエラーメッセージが発生する場合があります。本セクションは、正確な状況と、その修正方法や回避方法を理解するのに役立ちます。

    APIC Error 122: unknown managed object class 'polUni'
        :ref:`aci_rest <aci_rest_module>` ペイロードとオブジェクトクラスが一見正しそうに見える場合にこのエラーが発生する場合は、ペイロードの JSON に誤りがあり (たとえば、送信されたペイロードが二重引用符ではなく一重引用符を使用している) 、その結果 APIC がペイロードからオブジェクトクラスを正しく解析していない可能性があります。これを回避する 1 つの方法は、YAML 形式または XML 形式のペイロードを使用することです。これにより、正しく構築して後で変更するのが簡単になります。


    APIC Error 400: invalid data at line '1'.Attributes are missing, tag 'attributes' must be specified first, before any other tag
        JSON 仕様は順序付けされていない要素を許可しますが、APIC REST API では、JSON の ``attributes`` 要素が ``children`` アレイまたは他の要素の前になければなりません。したがって、ペイロードがこの要件に準拠していることを確認する必要があります。辞書キーを並び替えれば、問題なく終了します。属性がない場合は、``attributes: {}`` を追加する必要があります。APIC がそのエントリーを ``children`` の前に付ける必要があるためです。


    APIC Error 801: property descr of uni/tn-TENANT/ap-AP failed validation for value 'A "legacy" network'
        APIC 内の一部の値には準拠が必要な厳格な format-rules があり、提供される値に対する内部 APIC 検証チェックに失敗しました。上記の例では、``description`` パラメーター (内部では ``descr`` と呼ばれる) は、`Regex: [a-zA-Z0-9!#$%()*,-./:;@ _{|}~?&+]+ <https://pubhub-prod.s3.amazonaws.com/media/apic-mim-ref/docs/MO-fvAp.html」に準拠する値のみを受け付けます。#descr>`_ に準拠した値のみを受け取ります。一般的に、これには引用符または角括弧は含みません。

.. _aci_guide_known_issues:

既知の問題
------------
:ref:`aci_rest <aci_rest_module>` モジュールは、APIC REST API のラッパーです。これにより、APIC に関連する問題がこのモジュールの使用に反映されます。

以下の問題はすべてベンダー企業に報告されており、ほとんどの場合は回避できます。

    連続する API 呼び出しが多くなりすぎると、接続のスロットルが発生する可能性があります。
        ACI v3.1 以降、APIC は特定のしきい値で、パスワードベースの認証接続のレートをアクティブにスロットルします。これは、DDoS 対策の一部として実行されますが、パスワードベースの認証を使用して ACI で Ansible を使用するときに機能する可能性があります。現在、これは nginx 設定内でこのしきい値を増やすことですが、署名ベースの認証の使用が推奨されます。

        **注記:** 接続スロットルを回避するだけでなく、ACI モジュールを使用する場合の全般的なパフォーマンスを向上させるため、ACI で署名ベースの認証を使用することが推奨されます。


    特定の要求には、変更が正しく反映されない場合があります (`#35401 <https://github.com/ansible/ansible/issues/35041>`_)。
        APIC への特定のリクエストが、APIC から明示的に変更をリクエストした場合でも、結果の出力に変更が正しく反映されないという既知の問題があります。ある例では、``api/node/mo/uni/infra.xml`` のパスの使用は失敗しますが、``api/node/mo/uni/infra/.xml`` は正しく動作します。

        **注記:** 回避策としては、タスクの戻り値を登録 (例: ``register: this``) し、``changed_when: this.imdata != []`` を追加することで、タスクが変更を報告するタイミングに影響を与えることができます。
    

    特定のリクエストは冪等でないことが知られています (`#35050 <https://github.com/ansible/ansible/issues/35050>`_)。
        APIC の挙動は、``status="created"`` と ``status="deleted"`` の使用に矛盾しています。したがって、``status="created`` をペイロードに使用した場合は、オブジェクトが既に作成されている場合に結果として生じるタスクは冪等ではなく、作成に失敗します。ただし、``status="deleted"`` の場合は異なり、存在しないオブジェクトを呼び出しても何の問題もありません。

        **注記:** 回避策としては、冪等がワークフローに必要な場合は、``status="created"`` を使用せずに、代わりに ``status="modified"`` を使うことです。


    ユーザーパスワードの設定は冪等ではありません (`#35544 <https://github.com/ansible/ansible/issues/35544>`_)。
        APIC REST API の不整合により、ローカルで認証されたユーザのパスワードを設定するタスクが冪等ではありません。APIC は ``Password history check: user dag should not use previous 5 passwords`` というメッセージを出力します。

        **注記:** この問題の回避策はありません。


.. _aci_guide_community:

ACI Ansible コミュニティー
---------------------
ACI モジュールまたは機能要求に特定の問題が発生した場合や、変更やドキュメントの更新を提案して ACI プロジェクトに貢献する場合は、https://github.com/ansible/community/wiki/Network:-ACI の Ansible Community wiki ACI ページを参照してください。

ロードマップ、オープンな ACI の問題およびプル要求の概要、およびこのコミュニティーに関する詳細情報を確認できます。ACI を Ansible で使用することを検討している場合は、お気軽にご参加ください。進捗状況を追跡し、新しい Ansible リリースの準備をするために、オンラインミーティングを行う場合もがあります。


.. seealso::

   :ref:`ACI モジュールの一覧 <aci_network_modules>`
       対応している ACI モジュールの完全リスト
   :ref:`Cisco ACI モジュールの開発 <aci_dev_guide>`
       新しい Cisco ACI モジュールを開発して貢献する方法に関するウォークスルー
   `ACI コミュニティー <https://github.com/ansible/community/wiki/Network:-ACI>`_
       Ansible ACI コミュニティーの wiki ページ。ロードマップ、概念、および開発ドキュメントが含まれます。
   :ref:`network_guide`
       ネットワークインフラストラクチャーの自動化に Ansible を使用する方法に関する詳細なガイドです。
   `ネットワークワーキンググループ <https://github.com/ansible/community/tree/master/group-network>`_
       Ansible Network コミュニティーページ。連絡先情報およびミーティング情報が含まれます。
   `#ansible-network <https://webchat.freenode.net/?channels=ansible-network>`_
       #ansible-network IRC chat channel on Freenode.net.
`ユーザーメーリングリスト <https://groups.google.com/group/ansible-project>`_
   ご質問はございますか。 Google Group をご覧ください。
