.. _windows_setup:

Windows ホストのセットアップ
=========================
本書では、Ansible が Microsoft Windows ホストと通信する前に必要なセットアップを説明します。

.. contents::
   :local:

ホスト要件
`````````````````
Ansible が Windows ホストと通信して Windows モジュールを使用するには、
Windows ホストは次の要件を満たしている必要があります。

* Ansible は通常、
  Microsoft 社の現行サポートおよび拡張サポートの下で Windows バージョンを管理できます。Ansible は、
  Windows 7、8.1、10 などのデスクトップ OS と、
  Windows Server 2008、2008 R2、2012、2012 R2、2016、2019 などのサーバー OS を管理できます

* Ansible を使用するには、
  Windows ホストに PowerShell 3.0 以降および少なくとも .NET 4.0 をインストールする必要があります。

* WinRM リスナーを作成し、アクティベートする必要があります。詳細は、
  以下を参照してください。

.. Note:: Ansible 接続のベース要件であるものの、
    一部の Ansible モジュールには、
    OS や PowerShell の新しいバージョンなどの追加要件があります。ホストがこれらの要件を満たしているかどうかを判断するには、
    モジュールのドキュメントページを参照してください。

PowerShell および .NET Framework のアップグレード
---------------------------------------
Ansible では、Server 2008 や Windows 7 などの古いオペレーティングシステムで機能するために、PowerShell バージョン 3.0 および .NET Framework 4.0 以降が必要です。ベースイメージは、
この要件は満たしていません。`Upgrade-PowerShell.ps1` <https://github.com/jborean93/ansible-windows/blob/master/scripts/Upgrade-PowerShell.ps1>_ スクリプトを使用してこれらを更新できます。

このスクリプトを PowerShell から実行する例を以下に示します。

.. code-block:: powershell

    $url = "https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Upgrade-PowerShell.ps1"
    $file = "$env:temp\Upgrade-PowerShell.ps1"
    $username = "Administrator"
    $password = "Password"

    (New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
    Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force

    # Version can be 3.0, 4.0 or 5.1
    &$file -Version 5.1 -Username $username -Password $password -Verbose

完了したら、自動ログオンを削除し、
実行ポリシーをデフォルトの ``Restricted`` に戻す必要があります。これは、
次の PowerShell コマンドを使用して実行できます。

.. code-block:: powershell

    # This isn't needed but is a good security practice to complete
    Set-ExecutionPolicy -ExecutionPolicy Restricted -Force

    $reg_winlogon_path = "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
    Set-ItemProperty -Path $reg_winlogon_path -Name AutoAdminLogon -Value 0
    Remove-ItemProperty -Path $reg_winlogon_path -Name DefaultUserName -ErrorAction SilentlyContinue
    Remove-ItemProperty -Path $reg_winlogon_path -Name DefaultPassword -ErrorAction SilentlyContinue

スクリプトは、
インストールする必要のあるプログラム (.NET Framework 4.5.2 など) および必要な PowerShell バージョンを確認することで機能します。再起動が必要で、
``username`` パラメーターおよび ``password`` パラメーターが設定されている場合は、
スクリプトが自動的に再起動し、
再起動から戻ったときにログオンします。スクリプトは、追加のアクションが不要になり、
PowerShell バージョンは対象のバージョンと一致します。``username`` パラメーター、
および ``password`` のパラメーターが設定されていないと、スクリプトにより、
必要に応じて手動で再起動してログオンするように求められます。ユーザーが次にログインすると、
スクリプトは中断したところから続行し、
処理が必要なくなるまでプロセスが続行します。

.. Note:: Server 2008 で実行している場合は、SP2 がインストールされている必要があります。Server 2008 R2 または Windows 7 で実行している場合は、
    SP1 をインストールする必要があります。

.. Note:: Windows Server 2008 は PowerShell 3.0 のみをインストールできます。
    これよりも新しいバージョンを指定すると、スクリプトが失敗します。

.. Note:: ``username`` パラメーターおよび ``password`` のパラメーターは、
    平文でレジストリーに保存されます。スクリプトが終了した後にクリーンアップコマンドを実行して、
    ホストに認証情報が保存されていないことを確認してください。

WinRM メモリーホットフィックス
-------------------
PowerShell v3.0で実行する場合は、
WinRM で使用可能なメモリーの量を制限する WinRM サービスにバグがあります。このホットフィックスがインストールされていないと、
Windows ホストで、Ansible が特定のコマンドを実行できません。これらは、
システムのブートストラップ、
またはイメージングプロセスの一部としてインストールする必要があります。`Install-WMF3Hotfix.ps1 <https://github.com/jborean93/ansible-windows/blob/master/scripts/Install-WMF3Hotfix.ps1>`_ スクリプトを使用して、影響を受けるホストにホットフィックスをインストールできます。

以下の PowerShell コマンドはホットフィックスをインストールします。

.. code-block:: powershell

    $url = "https://raw.githubusercontent.com/jborean93/ansible-windows/master/scripts/Install-WMF3Hotfix.ps1"
    $file = "$env:temp\Install-WMF3Hotfix.ps1"

    (New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)
    powershell.exe -ExecutionPolicy ByPass -File $file -Verbose

詳細は、Microsoft 社の「`ホットフィックスのドキュメント <https://support.microsoft.com/en-us/help/2842230/out-of-memory-error-on-a-computer-that-has-a-customized-maxmemorypersh>`_」を参照してください。

WinRM の設定
```````````
Powershell が少なくともバージョン 3.0 にアップグレードされたら、最後のステップは、
Ansible が接続できるように WinRM サービスを構成することです。Ansible が、
Windows ホストとインターフェースで接続できるかを制御する WinRM サービスには、
``listener`` と ``service`` と名前の 2 つの主要コンポーネント (構成設定) があります。

各コンポーネントの詳細は以下で確認できますが、
`ConfigureRemotingForAnsible.ps1 <https://github.com/ansible/ansible/blob/devel/examples/scripts/ConfigureRemotingForAnsible.ps1>`_ を使用して、
基本を設定できます。このスクリプトは、
自己署名証明書を使用して HTTP リスナーと HTTPS リスナーの両方を設定し、
サービスで ``基本`` 認証オプションを有効にします。

このスクリプトを使用するには、以下を PowerShell で実行します。

.. code-block:: powershell

    $url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
    $file = "$env:temp\ConfigureRemotingForAnsible.ps1"

    (New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

    powershell.exe -ExecutionPolicy ByPass -File $file

このスクリプトと一緒に設定できるさまざまなスイッチとパラメーター 
(``-EnableCredSSP`` や ``-ForceNewSSLCert`` など) があります。これらのオプションのドキュメントは、
スクリプトそのものの上部にあります。

.. Note:: ConfigureRemotingForAnsible.ps1 スクリプトは、
    トレーニングと開発のみを目的としており、
    設定 ( ``Basic`` 認証など）が有効になっているため、
    これは本質的に安全ではない場合があります。実稼働環境出は使用しないようにしてください。

WinRM リスナー
--------------
WinRM サービスは、1 つまたは複数のポートで要求をリッスンします。これらのポートにはそれぞれ、
リスナーが作成され、設定されています。

WinRM サービスで実行している現在のリスナーを表示するには、
次のコマンドを使用します。

.. code-block:: powershell

    winrm enumerate winrm/config/Listener

これにより、以下のような出力が表示されます。

    Listener
        Address = *
        Transport = HTTP
        Port = 5985
        Hostname
        Enabled = true
        URLPrefix = wsman
        CertificateThumbprint
        ListeningOn = 10.0.2.15, 127.0.0.1, 192.168.56.155, ::1, fe80::5efe:10.0.2.15%6, fe80::5efe:192.168.56.155%8, fe80::
    ffff:ffff:fffe%2, fe80::203d:7d97:c2ed:ec78%3, fe80::e8ea:d765:2c69:7756%7

    Listener
        Address = *
        Transport = HTTPS
        Port = 5986
        Hostname = SERVER2016
        Enabled = true
        URLPrefix = wsman
        CertificateThumbprint = E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE
        ListeningOn = 10.0.2.15, 127.0.0.1, 192.168.56.155, ::1, fe80::5efe:10.0.2.15%6, fe80::5efe:192.168.56.155%8, fe80::
    ffff:ffff:fffe%2, fe80::203d:7d97:c2ed:ec78%3, fe80::e8ea:d765:2c69:7756%7

上記の例では、リスナーがアクティベートされています。
HTTP 経由のポート 5985 でリッスンしているものと、HTTPS 経由のポート 5986 でリッスンしているものがあります。理解するのに役に立つ重要なオプションの一部は
次のとおりです。

* ``Transport``: リスナーが HTTP または HTTPS のどちらで実行されている場合でも、
  データをさらに変更する必要なく暗号化されるため、
  HTTPS 経由でリスナーを使用することが推奨されます。

* ``Port``: リスナーが実行するポート。デフォルトは HTTP が ``5985`` で、
  HTTPS が ``5986`` です。このポートは必要に応じて変更でき、
  ホスト変数 ``ansible_port`` に対応します。

* ``URLPrefix``: リッスンする URL 接頭辞で、デフォルトは ``wsman`` です。これが変更すると、
  ホスト変数 ``ansible_winrm_path`` は、
  同じ値に設定する必要があります。

* ``CertificateThumbprint``: HTTPS リスナーを介して実行する場合、
  これは、
  接続で使用される Windows 証明書ストア内の証明書の拇印です。証明書自体の詳細を取得するには、
  PowerShell で関連する証明書の拇印を使用して、次のコマンドを実行します。

    $thumbprint = "E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE"
    Get-ChildItem -Path cert:\LocalMachine\My -Recurse | Where-Object { $_.Thumbprint -eq $thumbprint } | Select-Object *

WinRM リスナーの設定
++++++++++++++++++++
WinRM リスナーを設定するには、3 つの方法があります。

* HTTP の場合は ``winrm quickconfig`` を使用し、
  HTTPS の場合は ``winrm quickconfig -transport:https`` を使用します。これは、
  ドメイン環境外で実行する場合に使用する最も簡単なオプションであり、
  単純なリスナーが必要です。その他のオプションとは異なり、このプロセスには、
  必要なポートに対してファイアウォールを開き、WinRM サービスを開始するという追加の利点もあります。

* グループポリシーオブジェクトの使用。これは、ホストがドメインのメンバーであるときにリスナーを作成する最良の方法です。
  これは、
  ユーザー入力なしで構成が自動的に行われるためです。グループポリシーオブジェクトの詳細は、
  `Group Policy Objects documentation <https://msdn.microsoft.com/en-us/library/aa374162(v=vs.85).aspx>`_ を参照してください。

* PowerShell を使用して、特定の設定でリスナーを作成します。これにより、
  以下の PowerShell コマンドで行います。

  .. code-block:: powershell

      $selector_set = @{
          Address = "*"
          Transport = "HTTPS"
      }
      $value_set = @{
          CertificateThumbprint = "E6CDAA82EEAF2ECE8546E05DB7F3E01AA47D76CE"
      }

      New-WSManInstance -ResourceURI "winrm/config/Listener" -SelectorSet $selector_set -ValueSet $value_set

  この PowerShell cmdlet をともなう他のオプションを表示するには、
  `New-WSManInstance` <https://docs.microsoft.com/en-us/powershell/module/microsoft.wsman.management/new-wsmaninstance?view=powershell-5.1>_ を参照してください。

.. Note:: HTTPS リスナーを作成する場合は、
    既存の証明書を作成して ``LocalMachine\My`` 証明書ストアに保存する必要があります。このストアに証明書が存在しない場合、
    ほとんどのコマンドは失敗します。

WinRM リスナーの削除
+++++++++++++++++++++
WinRM リスナーを削除するには、以下を実行します。
# Remove all listeners
    Remove-Item -Path WSMan:\localhost\Listener\* -Recurse -Force

    # Only remove listeners that are run over HTTPS
    Get-ChildItem -Path WSMan:\localhost\Listener | Where-Object { $_.Keys -contains "Transport=HTTPS" } | Remove-Item -Recurse -Force

.. Note:: ``Keys`` オブジェクトは文字列の配列であるため、
    異なる値を含めることができます。デフォルトでは、``Transport=`` および ``Address=`` のキーが含まれます。
    これは、winrm 列挙の winrm/config/Listeners の値に対応します。

WinRM サービスオプション
---------------------
認証オプションやメモリー設定など、
WinRM サービスコンポーネントの動作を制御するために設定できるオプションがいくつかあります。

現在のサービス設定オプションの出力を取得するには、
次のコマンドを使用します。

.. code-block:: powershell

    winrm get winrm/config/Service
    winrm get winrm/config/Winrs

これにより、以下のような出力が表示されます。

    Service
        RootSDDL = O:NSG:BAD:P(A;;GA;;;BA)(A;;GR;;;IU)S:P(AU;FA;GA;;;WD)(AU;SA;GXGW;;;WD)
        MaxConcurrentOperations = 4294967295
        MaxConcurrentOperationsPerUser = 1500
        EnumerationTimeoutms = 240000
        MaxConnections = 300
        MaxPacketRetrievalTimeSeconds = 120
        AllowUnencrypted = false
        Auth
            Basic = true
            Kerberos = true
            Negotiate = true
            Certificate = true
            CredSSP = true
            CbtHardeningLevel = Relaxed
        DefaultPorts
            HTTP = 5985
            HTTPS = 5986
        IPv4Filter = *
        IPv6Filter = *
        EnableCompatibilityHttpListener = false
        EnableCompatibilityHttpsListener = false
        CertificateThumbprint
        AllowRemoteAccess = true

    Winrs
        AllowRemoteShellAccess = true
        IdleTimeout = 7200000
        MaxConcurrentUsers = 2147483647
        MaxShellRunTime = 2147483647
        MaxProcessesPerShell = 2147483647
        MaxMemoryPerShellMB = 2147483647
        MaxShellsPerUser = 2147483647

これらのオプションの多くはめったに変更する必要はありませんが、
WinRM を介した操作に簡単に影響を与える可能性があるオプションをいくつか理解しておくと役立ちます。重要なオプションのいくつかは
次のとおりです。

* ``Service\AllowUnencrypted``:このオプションは、
  WinRM がメッセージの暗号化なしで HTTP 経由で実行されるトラフィックを許可するかどうかを定義します。メッセージレベルの暗号化は、
  ``ansible_winrm_transport`` が ``ntlm`` 
  ``kerberos`` または ``credssp`` の場合に限り可能です。デフォルトではこれは ``false`` であり、
  WinRM メッセージのデバッグ時にのみ ``true`` に設定する必要があります。

* ``Service\Auth*``: これらのフラグは、
  WinRM サービスで許可される認証オプションを定義します。デフォルトでは、``Negotiate (NTLM)`` および 
  ``Kerberos`` が有効になっています。

* ``Service\Auth\CbtHardeningLevel``: チャネルバインディングトークンを検証しない (None)、
  検証したが必要ではない (Relaxed)、
  または検証して必要 (Stric) かどうかを指定します。CBT は、
  HTTPS 経由で、NTLM または Kerberos に接続している場合にのみ使用されます。

* ``Service\CertificateThumbprint``: これは、
  CredSSP 認証で使用される TLS チャンネルの暗号化に使用される証明書の拇印です。デフォルトでは空になります。
  WinRM サービスの開始時に自己署名証明書が生成され、
  TLS プロセスで使用されます。

* ``Winrs\MaxShellRunTime``: これは、
  リモートコマンドの実行が許可される最大時間 (ミリ秒) です。

* ``Winrs\MaxMemoryPerShellMB``: これは、シェルの子プロセスを含め、
  シェルごとに割り当てられるメモリーの最大量です。

PowerShell の ``Service`` キーの下にある設定を変更するには、以下を行います。

    # substitute {path} with the path to the option after winrm/config/Service
    Set-Item -Path WSMan:\localhost\Service\{path} -Value "value here"

    # for example, to change Service\Auth\CbtHardeningLevel run
    Set-Item -Path WSMan:\localhost\Service\Auth\CbtHardeningLevel -Value Strict

PowerShell の ``Winrs`` キーで設定を変更するには、以下を実行します。

    # Substitute {path} with the path to the option after winrm/config/Winrs
    Set-Item -Path WSMan:\localhost\Shell\{path} -Value "value here"

    # For example, to change Winrs\MaxShellRunTime run
    Set-Item -Path WSMan:\localhost\Shell\MaxShellRunTime -Value 2147483647

.. Note:: ドメイン環境で実行している場合、これらのオプションの一部は GPO によって設定され、
    ホスト自体を変更することはできません。鍵が GPO で設定され、
    値の横にテキスト ``[Source="GPO"]`` が含まれます。

一般的な WinRM の問題
-------------------
WinRM にはさまざまな設定オプションがあるため、
セットアップおよび構成を行うのが困難になる可能性があります。この複雑さのため、Ansible によって示される問題は、
実際にはホストのセットアップの問題である可能性があります。

問題がホストの問題かどうかを判断する簡単な方法の 1 つに、
別の Windows ホストから次のコマンドを実行して、
対象となる Windows ホストに接続することです。

    # Test out HTTP
    winrs -r:http://server:5985/wsman -u:Username -p:Password ipconfig

    # Test out HTTPS (will fail if the cert is not verifiable)
    winrs -r:https://server:5986/wsman -u:Username -p:Password -ssl ipconfig

    # Test out HTTPS, ignoring certificate verification
    $username = "Username"
    $password = ConvertTo-SecureString -String "Password" -AsPlainText -Force
    $cred = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $password

    $session_option = New-PSSessionOption -SkipCACheck -SkipCNCheck -SkipRevocationCheck
    Invoke-Command -ComputerName server -UseSSL -ScriptBlock { ipconfig } -Credential $cred -SessionOption $session_option

これに失敗する場合は、問題が WinRM 設定に関連している可能性があります。成功した場合は、WinRM 設定には関連していない可能性があります。引き続きトラブルシューティングの提案を読みください。

HTTP 401/認証情報の拒否
+++++++++++++++++++++++++++++
HTTP 401 エラーは、
認証プロセスが初期接続に失敗したことを示します。これを確認するには、次のような事項があります。

* 認証情報が正しいことを確認して、
  ``ansible_user`` および ``ansible_password`` を使用してインベントリーで適切に設定されていることを確認します。

* ユーザーがローカルの Administrators グループのメンバーであるか、
  アクセスが明示的に許可されていることを確認します 
  (``winrs`` コマンドを使用した接続テストを使用してこれを除外できます)。

* ``ansible_winrm_transport`` で設定した認証オプションが、
  ``Service\Auth*`` の下で有効になっていることを確認します。

* HTTPS ではなく HTTP で実行している場合は、``ntlm``、``kerberos``、または ``credssp`` 
  と ``ansible_winrm_message_encryption: auto`` を使用して、メッセージ暗号化を有効にします。
  別の認証オプションを使用している場合、またはインストールされている pywinrm バージョンをアップグレードできない場合は、
  ``Service\AllowUnencrypted`` を ``true`` に設定できますが、
  これはトラブルシューティングにのみ推奨されます。

* ダウンストリームパッケージである ``pywinrm``、``requests-ntlm``、
  ``requests-kerberos``、または ``requests-credssp``、もしくはそのうちの複数のものが、``pip`` を使用して最新の状態になります。

* Kerberos 認証を使用する場合は、``Service\Auth\CbtHardeningLevel`` が 
  ``Strict`` に設定されていないことを確認してください。

* 基本認証または証明書認証を使用する場合は、
  ユーザーがドメインアカウントではなくローカルアカウントであることを確認してください。ドメインアカウントが、
  基本認証およびおよび認証情報で動作しません。

HTTP 500 Error
++++++++++++++
これは WinRM サービスでエラーが発生したことを示します。以下の事項を
確認してください。

* 現在のオープンシェルの数が、
  ``WinRsMaxShellsPerUser`` 
  または他の Winrs クォーターを超過していないことを確認します。

タイムアウトエラー
+++++++++++++++
これらは通常、Ansible がホストに到達できないネットワーク接続のエラーを示しています。
Ansible がホストに到達できません。確認すべき事項には以下が含まれます。

* ファイアウォールが、設定された WinRM リスナーポートをブロックするように設定されていないことを確認します。
* WinRM リスナーが、ホストの変数によって設定されたポートおよびパスで有効になっていることを確認します。
* ``winrm`` サービスが Windows ホスト上で実行され、
  自動起動に設定されていることを確認します。

接続拒否エラー
+++++++++++++++++++++++++
これらは通常、
ホスト上の WinRM サービスと通信しようとしたときのエラーを示しています。以下の点を確認します。

* WinRM サービスがホストで稼働していることを確認します。``(Get-Service -Name winrm).Status`` を使用して、
  サービスのステータスを取得します。
* ホストのファイアウォールが WinRM ポートでのトラフィックを許可していることを確認します。デフォルトでは空になります。
  HTTP の場合は ``5985``、HTTPS の場合は ``5986`` です。

インストーラーが WinRM サービスまたは HTTP サービスを再起動して、このエラーが発生することがあります。文字列が、
別の Windows ホストから 
``win_psexec`` を使用することです。

Windows SSH の設定
`````````````````
Ansible 2.8 では、Windows 管理ノードの実験的な SSH 接続が追加されました。

.. warning::
    この機能は自己責任で使用してください。
    Windows でのSSH の使用は実験的なものであり、
    実装は機能リリースで後方互換性のない変更を行う場合があります。サーバーのコンポーネントは、
    インストールされているバージョンによっては信頼できない場合があります。

Win32-OpenSSH のインストール
------------------------
Windows で SSH を使用する最初の手順は、Windows ホストにサービス `Win32-OpenSSH <https://github.com/PowerShell/Win32-OpenSSH>`_ 
をインストールすることです。Microsoft 社は、Windows 機能を通じて ``Win32-OpenSSH`` をインストールする方法を提供していますが、
現在、
このプロセスを通じてインストールされるバージョンは古いため、Ansible では動作しません。Ansible で使用する ``Win32-OpenSSH`` をインストールするには、
次の 3 つのインストールオプションのいずれかを選択します。

* Microsoft 社が提供する `インストール手順 <https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH>`_ に従い、
  サービスを手動でインストールします。

* ``win_chocolatey`` を使用してサービスをインストールします。

    - name: install the Win32-OpenSSH service
      win_chocolatey:
        name: openssh
        package_params: /SSHServerFeature
        state: present

* `jborean93.win_openssh <https://galaxy.ansible.com/jborean93/win_openssh>`_ などの既存の Ansible Galaxy ロールを使用します::

    # Make sure the role has been downloaded first
    ansible-galaxy install jborean93.win_openssh

    # main.yml
    - name: install Win32-OpenSSH service
      hosts: windows
      gather_facts: no
      roles:
      - role: jborean93.win_openssh
        opt_openssh_setup_service: True

.. note:: ``Win32-OpenSSH`` は現在もベータ製品であり、
    新機能とバグ修正を含むように常に更新されています。Windows の接続オプションとして SSH を使用している場合は、
    上記の 3 つの方法のいずれかから、
    最新リリースをインストールすることが強く推奨されます。

Win32-OpenSSH シェルの設定
-----------------------------------

デフォルトでは、``Win32-OpenSSH`` は ``cmd.exe`` をシェルとして使用します。別のシェルを構成するには、
Ansible タスクを使用してレジストリー設定を定義します。

    - name: set the default shell to PowerShell
      win_regedit:
        path: HKLM:\SOFTWARE\OpenSSH
        name: DefaultShell
        data: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
        type: string
        state: present

    # Or revert the settings back to the default, cmd
    - name: set the default shell to cmd
      win_regedit:
        path: HKLM:\SOFTWARE\OpenSSH
        name: DefaultShell
        state: absent

Win32-OpenSSH 認証
----------------------------
Windows での Win32-OpenSSH 認証は、
Unix/Linux ホストでの SSH 認証に似ています。平文のパスワードまたは SSH 公開鍵認証を使用し、
公開鍵を、
ユーザーのプロファイルディレクトリーの ``.ssh`` ディレクトリーにある ``authorized_key`` ファイルに追加し、
SSH サービスが使用する ``sshd_config`` ファイルを使用して、
Unix/Linux ホストで行うのと同じようにサービスを設定することができます。

Ansible で SSH キー認証を使用する場合、リモートセッションはユーザーの認証情報にアクセスできず、
ネットワークリソースにアクセスしようとすると失敗します。
これは、ダブルホップまたは認証情報の委譲の問題としても知られています。この問題を回避するには、
2 つの方法があります。

* ``ansible_password`` を設定して平文テキストのパスワード認証を使用する
* リモートリソースへのアクセスを必要とするユーザーの認証情報を使用して、タスクで ``become`` を使用する

Windows で SSH 用に Ansible の設定
--------------------------------------
Ansible が Windows ホストに SSH を使用するように設定するには、接続変数を 2 つ設定する必要があります。

* ``ansible_connection`` を ``ssh``に設定します。
* ``ansible_shell_type`` を ``cmd`` または ``powershell`` に設定します。

``ansible_shell_type`` 変数は、Windows ホストで構成された ``DefaultShell`` を反映する必要があります。
Windows ホストで設定します。``DefaultShell`` を PowerShell に変更すると、
デフォルトシェルの場合は ``cmd`` に設定するか、または ``powershell`` に設定されます。

Windows での SSH に関する既知の問題
--------------------------------
Windows で SSH を使用することは実験的なものであり、さらに多くの問題が明らかになることが予想されます。
既知のものは以下のとおりです。

* ``powershell`` がシェルタイプの場合は、``v7.9.0.0p1-Beta`` よりも古い Win32-OpenSSH バージョンは機能しません。
* SCP も有効ですが、SFTP は、ファイルのコピーまたは取得時に使用する、推奨される SSH ファイル転送メカニズムです。


.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_best_practices`
       ベストプラクティスのアドバイス
   :ref:`Windows モジュールリスト <windows_modules>`
       Windows 固有のモジュールリスト (すべて PowerShell に実装)
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
