Desired State Configuration
===========================

.. contents:: トピック
   :local:

Desired State Configuration とは
````````````````````````````````````
Desired State Configuration (DSC) は、PowerShell に同梱されているツールで、
コードを使用して Windows ホストのセットアップを定義するのに使用されます。DSC の全般的な目的は Ansible と同じになりますが、
実行方法が異なります。Ansible 2.4 以降では、
``win_dsc`` モジュールが追加され、
Windows ホストと対話するときに既存の DSC リソースを活用するために使用できます。

DSC の詳細は「`DSC Overview <https://docs.microsoft.com/en-us/powershell/scripting/dsc/overview/overview>`_」を参照してください。

ホスト要件
`````````````````
``win_dsc`` モジュールを使用するには、
Windows ホストに PowerShell v5.0 以降がインストールされている必要があります。Windows Server 2008 (R2以外) を除く、
サポートされているすべてのホストは、PowerShell v5 にアップグレードできます。

PowerShell の要件が満たされると、
DSC の使用は ``win_dsc`` モジュールでタスクを作成するのと同じくらい簡単です。

DSC を使用する理由
````````````
DSC および Ansible モジュールには、
リソースの状態を定義して保証するという共通の目標があります。このため、
DSC の `ファイルリソース <https://docs.microsoft.com/en-us/powershell/scripting/dsc/reference/resources/windows/fileresource>`_ や、
Ansible の ``win_file`` などのリソースを使用して、同じ結果を得ることができます。どちらを使用するかは、
シナリオによって異なります。

DSC リソースで Ansible モジュールを使用する理由:

* ホストが PowerShell v5.0 をサポートしていない、または簡単にアップグレードできない。
* DSC リソースが、Ansible モジュールに存在する機能を提供していない。たとえば、
  win_regedit は、``REG_NONE`` プロパティータイプを管理できますが、
  DSC の ``Registry`` リソースは管理できません。
* DSC リソースはチェックモードのサポートに制限があるが、
  一部の Ansible モジュールはより優れたチェックを備えている。
* DSC リソースでは差分モードがサポートされないが、一部の Ansible モジュールではサポートされる。
* Ansible モジュールは Ansible に組み込まれているが、カスタムリソースでは、
  事前にホストで追加のインストール手順を実行する必要がある。
* Ansible モジュールが機能する DSC リソースにバグがある。

Ansible モジュールで DSC リソースを使用する理由:

* Ansible モジュールは、DSC リソースに存在する機能をサポートしていない。
* 利用可能な Ansible モジュールがない。
* 既存の Ansible モジュールにバグがある。

結局のところ、タスクが DSC および Ansible モジュールのどちらで実行されるかは重要でありません。
重要なのは、タスクが正しく実行され、
Playbooks が理解しやすいかどうかです。Ansible よりも DSC の方を長く使用していて、それで問題が解決する場合は、
そのタスクに DSC を使用すると良いでしょう。

DSC の使用方法
```````````````
``win_dsc`` モジュールは、管理しているリソースに応じて変更できるように、
自由形式のオプションを採用しています。組み込みリソースの一覧は、
「`resources <https://docs.microsoft.com/en-us/powershell/scripting/dsc/resources/resources>`_」を参照してください。

たとえば `Registry <https://docs.microsoft.com/en-us/powershell/scripting/dsc/reference/resources/windows/registryresource>`_ リソースを使用した場合は、
以下は、Microsoft 社が提供している DSC 定義です。

.. code-block:: powershell

    Registry [string] #ResourceName
    {
        Key = [string]
        ValueName = [string]
        [ Ensure = [string] { Enable | Disable }  ]
        [ Force =  [bool]   ]
        [ Hex = [bool] ]
        [ DependsOn = [string[]] ]
        [ ValueData = [string[]] ]
        [ ValueType = [string] { Binary | Dword | ExpandString | MultiString | Qword | String }  ]
    }
    
タスクを定義するとき、``resource_name`` は、使用されている DSC リソースに設定する必要があります。
この場合、``resource_name`` は ``Registry`` に設定する必要があります。``module_version`` は、
インストールされている DSC リソースの特定のバージョンを参照できます。
空白のままにすると、デフォルトで最新バージョンになります。その他のオプションは、
``Key`` や 
``ValueName`` など、リソースの定義に使用されるパラメーターです。タスクのオプションでは大文字と小文字が区別されませんが、
DSC リソースオプションと、
Ansible の ``win_dsc`` オプションを区別しやすくなるため、大文字と小文字をそのまま維持することが推奨されます。

上記の DSC レジストリーリソースの Ansible タスクバージョンは、以下のようになります。

.. code-block:: yaml+jinja

    - name:Use win_dsc module with the Registry DSC resource
      win_dsc:
        resource_name:Registry
        Ensure:Present
        Key:HKEY_LOCAL_MACHINE\SOFTWARE\ExampleKey
        ValueName:TestValue
        ValueData:TestData

Ansible 2.8 以降、``win_dsc`` モジュールは DSC 定義を使用して、
Ansible からの入力オプションを自動的に検証します。つまり、オプション名が正しくない場合、必須オプションが設定されていない場合、
または値が有効な選択肢ではない場合は、
Ansible が失敗します。詳細レベル 3 以上 
(``-vvv``) で Ansible を実行する場合、戻り値には、
指定された ``resource_name`` に基づいて可能な呼び出しオプションが含まれます。以下は、
上記の ``Registry`` タスクの呼び出し結果の例になります。

.. code-block:: ansible-output

    changed: [2016] => {
        "changed": true,
        "invocation": {
            "module_args": {
                "DependsOn": null,
                "Ensure": "Present",
                "Force": null,
                "Hex": null,
                "Key": "HKEY_LOCAL_MACHINE\\SOFTWARE\\ExampleKey",
                "PsDscRunAsCredential_password": null,
                "PsDscRunAsCredential_username": null,
                "ValueData": [
                    "TestData"
                ],
                "ValueName": "TestValue",
                "ValueType": null,
                "module_version": "latest",
                "resource_name": "Registry"
            }
        },
        "module_version": "1.1",
        "reboot_required": false,
        "verbose_set": [
            "Perform operation 'Invoke CimMethod' with following parameters, ''methodName' = ResourceSet,'className' = MSFT_DSCLocalConfigurationManager,'namespaceName' = root/Microsoft/Windows/DesiredStateConfiguration'.",
            "An LCM method call arrived from computer SERVER2016 with user sid S-1-5-21-3088887838-4058132883-1884671576-1105.",
            "[SERVER2016]: LCM:  [ Start  Set      ]  [[Registry]DirectResourceAccess]",
            "[SERVER2016]:                            [[Registry]DirectResourceAccess] (SET) Create registry key 'HKLM:\\SOFTWARE\\ExampleKey'",
            "[SERVER2016]:                            [[Registry]DirectResourceAccess] (SET) Set registry key value 'HKLM:\\SOFTWARE\\ExampleKey\\TestValue' to 'TestData' of type 'String'",
            "[SERVER2016]: LCM:  [ End    Set      ]  [[Registry]DirectResourceAccess]  in 0.1930 seconds.",
            "[SERVER2016]: LCM:  [ End    Set      ]    in  0.2720 seconds.",
            "Operation 'Invoke CimMethod' complete.",
            "Time taken for configuration job to complete is 0.402 seconds"
        ],
        "verbose_test": [
            "Perform operation 'Invoke CimMethod' with following parameters, ''methodName' = ResourceTest,'className' = MSFT_DSCLocalConfigurationManager,'namespaceName' = root/Microsoft/Windows/DesiredStateConfiguration'.",
            "An LCM method call arrived from computer SERVER2016 with user sid S-1-5-21-3088887838-4058132883-1884671576-1105.",
            "[SERVER2016]: LCM:  [ Start  Test     ]  [[Registry]DirectResourceAccess]",
            "[SERVER2016]:                            [[Registry]DirectResourceAccess] Registry key 'HKLM:\\SOFTWARE\\ExampleKey' does not exist",
            "[SERVER2016]: LCM:  [ End    Test     ]  [[Registry]DirectResourceAccess] False in 0.2510 seconds.",
            "[SERVER2016]: LCM:  [ End    Set      ]    in  0.3310 seconds.",
            "Operation 'Invoke CimMethod' complete.",
            "Time taken for configuration job to complete is 0.475 seconds"
        ]
    }
    
``invocation.module_args`` キーは、
設定された実際の値と、設定されなかったその他の可能な値を示します。ただし、
これは DSC プロパティーのデフォルト値は表示せず、
Ansible タスクから設定されたもののみを表示します。セキュリティー上の理由から、
``*_password`` オプションは出力でマスクされます。他の機密モジュールオプションがある場合は、
タスクで ``no_log: True`` を設定して、すべてのタスク出力のログ記録を停止します。


プロパティータイプ
--------------
DSC リソースプロパティには、それぞれ関連付けられているタイプがあります。Ansible の Playbook は、
実行中に、定義されたオプションを正しいタイプに変換しようとします。
``[string]`` や ``[bool]`` のように単純な場合は、操作も簡単になりますが、
``[PSCredential]`` やアレイ (``[string[]]`` など) のような複雑なものには、
特定のルールが必要です。

PSCredential
++++++++++++
``[PSCredential]`` オブジェクトは、安全な方法で認証情報を保存するために使用されますが、
Ansible はこれを JSON 経由でシリアル化する方法がありません。DSC PSCredential プロパティーを設定するには、
そのパラメーターの定義に、
ユーザー名とパスワードにそれぞれ ``_username`` と ``_password`` が接尾辞として付けられた 2 つのエントリーが必要です。
例:

.. code-block:: yaml+jinja

    PsDscRunAsCredential_username: '{{ ansible_user }}'
    PsDscRunAsCredential_password: '{{ ansible_password }}'

    SourceCredential_username: AdminUser
    SourceCredential_password: PasswordForAdminUser
    
.. Note:: 2.8 より古いバージョンの Ansible では、Ansible のタスク定義で ``no_log: yes`` を設定して、
    使用される認証情報が、
    ログファイルやコンソール出力に保存されないようにする必要があります。

``[PSCredential]`` は、DSC リソースの MOF 定義の ``EmbeddedInstance("MSFT_Credential")`` 
で定義されています。

CimInstance タイプ
++++++++++++++++
``[CimInstance]`` オブジェクトは、
DSC が使用するディクショナリーオブジェクトを格納するために使用されます。YAML で ``[CimInstance]`` を受け取る値を定義することは、
YAML でディクショナリーを定義することと同じです。
たとえば、Ansibleで ``[CimInstance]`` 値を定義する場合は、以下のようにします。

.. code-block:: yaml+jinja

    # [CimInstance]AuthenticationInfo == MSFT_xWebAuthenticationInformation
    AuthenticationInfo:
      Anonymous: no
      Basic: yes
      Digest: no
      Windows: yes

上記の例では、
CIM インスタンスは、クラス `MSFT_xWebAuthenticationInformation <https://github.com/PowerShell/xWebAdministration/blob/dev/DSCResources/MSFT_xWebsite/MSFT_xWebsite.schema.mof>`_ の表現になります。
このクラスは、``Anonymous``、``Basic``、
``Digest``、および ``Windows`` の 4 つのブール変数を受け入れます。``[CimInstance]`` で使用するキーは、
それが表すクラスによって異なります。リソースのドキュメントを読んで、
使用できるキーと各キー値のタイプを確認してください。``module_version`` は、
``<resource name>.schema.mof`` にあります。

HashTable タイプ
++++++++++++++
``[HashTable]`` オブジェクトはディクショナリーでもありますが、定義できる、
または定義する必要がある厳密なキーのセットはありません。``[CimInstance]`` のように、
YAML の通常のディクショナリーの値のように定義します。``[HashTable]]`` は、
DSC リソース MOF 定義の ``EmbeddedInstance("MSFT_KeyValuePair")`` で定義されています。

アレイ
++++++
``[string[]]`` や ``[UInt32[]]`` のような単純なアレイはリストとして定義されます
または、コンマで区切られた文字列として、その型にキャストされます。値は DSC エンジンに渡される前に、
``win_dsc`` モジュールによって手動で解析されないため、
リストを使用することが推奨されます。たとえば、
Ansible で簡単なアレイを定義するには、以下のようにします。

.. code-block:: yaml+jinja

    # [string[]]
    ValueData: entry1, entry2, entry3
    ValueData:
    - entry1
    - entry2
    - entry3

    # [UInt32[]]
    ReturnCode:0,3010
    ReturnCode:
    - 0
    - 3010

``[CimInstance[]]`` (ディクショナリーのアレイ) のような複合型アレイは、
次のように定義できます。

.. code-block:: yaml+jinja

    # [CimInstance[]]BindingInfo == MSFT_xWebBindingInformation
    BindingInfo:
    - Protocol: https
      Port: 443
      CertificateStoreName: My
      CertificateThumbprint: C676A89018C4D5902353545343634F35E6B3A659
      HostName: DSCTest
      IPAddress: '*'
      SSLFlags: 1
    - Protocol: http
      Port: 80
      IPAddress: '*'

上記の例は、`MSFT_xWebBindingInformation <https://github.com/PowerShell/xWebAdministration/blob/dev/DSCResources/MSFT_xWebsite/MSFT_xWebsite.schema.mof>`_ クラスの値を 2 つ持つアレイです。
``[CimInstance[]]`` を定義するときは、
必ずリソースのドキュメントを参照して、定義で使用するキーを確認してください。

DateTime
++++++++
``[DateTime]`` オブジェクトは、`ISO 8601 <https://www.w3.org/TR/NOTE-datetime>`_ の日時形式で、
日付と時刻を表す DateTime文字列です。文字列が、
Windows ホストに適切にシリアル化されるようにするには、
``[DateTime]`` フィールドの値を YAML で引用する必要があります。たとえば、Ansibleで ``[DateTime]`` 値を定義する場合は、
以下のようにします。

.. code-block:: yaml+jinja

    # As UTC-0 (No timezone)
    DateTime: '2019-02-22T13:57:31.2311892+00:00'

    # As UTC+4
    DateTime: '2019-02-22T17:57:31.2311892+04:00'

    # As UTC-4
    DateTime: '2019-02-22T09:57:31.2311892-04:00'

上記のすべての値は、
UTC 日付時刻の 2019 年 2 月 22 日午後 1 時 57 分 31 秒と 2311892 ミリ秒と同じです。

別のユーザーとして実行
-------------------
デフォルトでは、DSC は各リソースを SYSTEM アカウントとして実行し、
Ansible がモジュールの実行に使用するアカウントではありません。つまり、
``HKEY_CURRENT_USER`` レジストリーハイブなど、
ユーザープロファイルに基づいて動的に読み込まれるリソースは、``SYSTEM`` プロファイルの下に読み込まれます。``PsDscRunAsCredential`` パラメーターは、
すべての DSC リソースが、
DSC エンジンを別のアカウントで強制的に実行するように設定できるパラメーターです。``PsDscRunAsCredential`` には、
``PSCredential`` のタイプがあるため、
``_username`` 接尾辞および ``_password`` 接尾辞で定義されます。

たとえば、レジストリーリソースタイプを使用して、
Ansible ユーザーの ``HKEY_CURRENT_USER`` ハイブにアクセスするタスクを定義する方法は次のとおりです。

.. code-block:: yaml+jinja

    - name: Use win_dsc with PsDscRunAsCredential to run as a different user
      win_dsc:
        resource_name: Registry
        Ensure: Present
        Key: HKEY_CURRENT_USER\ExampleKey
        ValueName: TestValue
        ValueData: TestData
        PsDscRunAsCredential_username: '{{ ansible_user }}'
        PsDscRunAsCredential_password: '{{ ansible_password }}'
      no_log: yes
    
カスタムの DSC リソース
````````````````````
DSC リソースは、Microsoft 社から提供される組み込みオプションに限定されません。カスタムモジュールをインストールすれば、
通常は利用できないその他のリソースを管理できます。

カスタムの DSC リソースの見つけ方
----------------------------
`PSGallery <https://www.powershellgallery.com/>`_ を使用して、
カスタムリソースと、Windows ホストにインストールする方法に関するドキュメントを確認できます。

``Find-DscResource`` コマンドレットを使用して、カスタムリソースを検索することもできます。例:

.. code-block:: powershell

    # Find all DSC resources in the configured repositories
    Find-DscResource

    # Find all DSC resources that relate to SQL
    Find-DscResource -ModuleName "*sql*"

.. Note:: ``x`` で始まる、
    Microsoft 社によって開発された DSC リソースは、リソースが実験的であり、サポート対象ではないことを意味します。

カスタムリソースのインストール
----------------------------
DSC リソースをホストにインストールする方法は 3 つあります。

* ``Install-Module`` コマンドレットを手動で使用
* Ansibleモジュール ``win_psmodule`` を使用
* モジュールを手動で保存して別のホストにコピー

以下の例は、
``win_psmodule`` を使用して ``xWebAdministration`` リソースをインストールする例になります。

.. code-block:: yaml+jinja

    - name: Install xWebAdministration DSC resource
      win_psmodule:
        name: xWebAdministration
        state: present

インストールすると、
``resource_name`` オプションを使用してそれを参照することで、win_dsc モジュールがリソースを使用できるようになります。

上記の最初の2つの方法は、ホストがインターネットにアクセスできる場合にのみ機能します。
ホストがインターネットにアクセスできない場合、
モジュールはまずインターネットにアクセスできる別のホストに上記の方法を使用してインストールし、
次にコピーする必要があります。モジュールをローカルファイルパスに保存するには、
次の PowerShell コマンドレットを実行します。

    Save-Module -Name xWebAdministration -Path C:\temp

これにより、``C:\temp`` に ``xWebAdministration`` という名前のフォルダーが作成され、
任意のホストにコピーできます。PowerShell がこのオフラインリソースを表示する場合は、
``PSModulePath`` 環境変数で設定されているディレクトリーセットにコピーする必要があります。
ほとんどの場合は、この変数により ``C:\Program Files\WindowsPowerShell\Module`` パスが設定されますが、
``win_path`` モジュールを使用して、
別のパスを追加できます。

例
````````
zip ファイルの抽出
------------------

.. code-block:: yaml+jinja

  - name: Extract a zip file
    win_dsc:
      resource_name: Archive
      Destination: C:\temp\output
      Path: C:\temp\zip.zip
      Ensure: Present

ディレクトリーの作成
------------------

.. code-block:: yaml+jinja

    - name: Create file with some text
      win_dsc:
        resource_name: File
        DestinationPath: C:\temp\file
        Contents: |
            Hello
            World
        Ensure: Present
        Type: File

    - name: Create directory that is hidden is set with the System attribute
      win_dsc:
        resource_name: File
        DestinationPath: C:\temp\hidden-directory
        Attributes: Hidden,System
        Ensure: Present
        Type: Directory

Azure の操作
-------------------

.. code-block:: yaml+jinja

    - name: Install xAzure DSC resources
      win_psmodule:
        name: xAzure
        state: present

    - name: Create virtual machine in Azure
      win_dsc:
        resource_name: xAzureVM
        ImageName: a699494373c04fc0bc8f2bb1389d6106__Windows-Server-2012-R2-201409.01-en.us-127GB.vhd
        Name: DSCHOST01
        ServiceName: ServiceName
        StorageAccountName: StorageAccountName
        InstanceSize: Medium
        Windows: yes
        Ensure: Present
        Credential_username: '{{ ansible_user }}'
        Credential_password: '{{ ansible_password }}'
    
IIS Web サイトのセットアップ
-----------------

.. code-block:: yaml+jinja

    - name: Install xWebAdministration module
      win_psmodule:
        name: xWebAdministration
        state: present

    - name: Install IIS features that are required
      win_dsc:
        resource_name: WindowsFeature
        Name: '{{ item }}'
        Ensure: Present
      loop:
      - Web-Server
      - Web-Asp-Net45

    - name: Setup web content
      win_dsc:
        resource_name: File
        DestinationPath: C:\inetpub\IISSite\index.html
        Type: File
        Contents: |
          <html>
          <head><title>IIS Site</title></head>
          <body>This is the body</body>
          </html>
        Ensure: present

    - name: Create new website
      win_dsc:
        resource_name: xWebsite
        Name: NewIISSite
        State: Started
        PhysicalPath: C:\inetpub\IISSite\index.html
        BindingInfo:
        - Protocol: https
          Port: 8443
          CertificateStoreName: My
          CertificateThumbprint: C676A89018C4D5902353545343634F35E6B3A659
          HostName: DSCTest
          IPAddress: '*'
          SSLFlags: 1
        - Protocol: http
          Port: 8080
          IPAddress: '*'
        AuthenticationInfo:
          Anonymous: no
          Basic: yes
          Digest: no
          Windows: yes

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   :ref:`playbooks_best_practices`
       ベストプラクティスのアドバイス
   :ref:`Windows モジュールリスト <windows_modules>`
       Windows 固有のモジュールリスト (すべて PowerShell に実装)
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
