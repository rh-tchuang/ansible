.. _windows_winrm:

Windows リモート管理
=========================
デフォルトで SSH を使用する Linux/Unix ホストとは異なり、
Windows ホストは WinRM で構成されます。このトピックでは、Ansible で WinRM を設定し、使用する方法を説明します。

.. contents:: トピック
   :local:

WinRM とは
``````````````
WinRM は、
Windows が別のサーバーとリモート通信するために使用する管理プロトコルです。HTTP/HTTPS を介して通信する SOAP ベースのプロトコルであり、
最近の全 Windows オペレーティングシステムに含まれています。Windows Server 2012 以降、
WinRM はデフォルトで有効になっていますが、
ほとんどの場合、Ansible で WinRM を使用するには追加の構成が必要です。

Ansible は、`pywinrm <https://github.com/diyan/pywinrm>`_ パッケージを使用して、
WinRM 経由で Windows サーバーと通信します。Ansible パッケージではデフォルトではインストールされませんが、
次のコマンドを実行してインストールできます。

.. code-block:: shell

   pip install "pywinrm>=0.3.0"

.. Note:: 複数の python バージョンがあるディストリビューションでは、pip2 または pip2.x を使用します。
    x は、Ansible が実行している python のマイナーバージョンになります。

認証オプション
``````````````````````
Windows ホストに接続する際に、
アカウントで認証するときに使用できるいくつかの異なるオプションがあります。認証タイプは、
``ansible_winrm_transport`` 変数を使用してインベントリーホストまたはグループに設定できます。

以下のマトリックスは、オプションの概要を示しています。

+-------------+----------------+---------------------------+-----------------------+-----------------+
| Option      | Local Accounts | Active Directory Accounts | Credential Delegation | HTTP Encryption |
+=============+================+===========================+=======================+=================+
| Basic       | Yes            | No                        | No                    | No              |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| Certificate | Yes            | No                        | No                    | No              |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| Kerberos    | No             | Yes                       | Yes                   | Yes             |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| NTLM        | Yes            | Yes                       | No                    | Yes             |
+-------------+----------------+---------------------------+-----------------------+-----------------+
| CredSSP     | Yes            | Yes                       | Yes                   | Yes             |
+-------------+----------------+---------------------------+-----------------------+-----------------+

基本
-----
基本認証は、認証オプションの中で最も簡単な認証オプションの 1 つですが、
最も安全が低いものでもあります。これは、ユーザー名とパスワードが単に base64 でエンコードされており、
安全なチャンネルが使用されていない場合 (HTTPS など) に、
誰でもデコードできるためです。基本認証は、ローカルアカウント (ドメインアカウントではない) のみに使用できます。

以下の例は、基本認証に設定されているホスト変数を示しています。

.. code-block:: yaml+jinja

    ansible_user:LocalUsername
    ansible_password:Password
    ansible_connection: winrm
    ansible_winrm_transport: basic

基本認証は、Windows ホストではデフォルトで有効ではありませんが、
PowerShell で以下を実行して有効にします。

    Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $true

証明書
-----------
証明書認証では、SSH キーペアに似たキーとして証明書を使用しますが、
ファイルフォーマットとキー生成プロセスでは異なります。

以下の例では、証明書認証に設定されたホスト変数を示しています。

.. code-block:: yaml+jinja

    ansible_connection: winrm
    ansible_winrm_cert_pem: /path/to/certificate/public/key.pem
    ansible_winrm_cert_key_pem: /path/to/certificate/private/key.pem
    ansible_winrm_transport: certificate

証明書認証は、Windows ホストではデフォルトでは有効になっていませんが、
PowerShell で次を実行することで有効にできます。

    Set-Item -Path WSMan:\localhost\Service\Auth\Certificate -Value $true

.. Note:: WinRM 向けに Ansible が使用する urllib3 ライブラリーはこの機能に対応していないため、
    暗号化された秘密鍵は使用できません。

証明書の生成
++++++++++++++++++++++
証明書は、ローカルユーザーにマッピングする前に生成する必要があります。
これは、以下のいずれかの方法で実行できます。

* OpenSSL
* PowerShell (``New-SelfSignedCertificate`` コマンドレットを使用)
* Active Directory 証明書サービス

Active Directory 証明書サービスはこのドキュメントの範囲外ですが、
ドメイン環境で実行する場合に使用する最適なオプションである可能性があります。詳細情報は、
「`Active Directory Certificate Services documentation <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc732625(v=ws.11)>`_」を参照してください。

.. Note:: PowerShell のコマンドレッドである ``New-SelfSignedCertificate`` を使用した認証用の証明書の生成は、
    Windows 10 または Windows Server 2012 R2 
    以降のホストから生成された場合に限り機能します。Ansible を使用するために、
    PFX 証明書から PEM ファイルに秘密キーを抽出するには、
    OpenSSL が引き続き必要です。

``OpenSSL`` で証明書を生成するには、以下を行います。

.. code-block:: shell

    # Set the name of the local user that will have the key mapped to
    USERNAME="username"

    cat > openssl.conf << EOL
    distinguished_name = req_distinguished_name
    [req_distinguished_name]
    [v3_req_client]
    extendedKeyUsage = clientAuth
    subjectAltName = otherName:1.3.6.1.4.1.311.20.2.3;UTF8:$USERNAME@localhost
    EOL

    export OPENSSL_CONF=openssl.conf
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -out cert.pem -outform PEM -keyout cert_key.pem -subj "/CN=$USERNAME" -extensions v3_req_client
    rm openssl.conf
    

``New-SelfSignedCertificate`` で証明書を生成するには、以下を行います。

.. code-block:: powershell

    # Set the name of the local user that will have the key mapped
    $username = "username"
    $output_path = "C:\temp"

    # Instead of generating a file, the cert will be added to the personal
    # LocalComputer folder in the certificate store
    $cert = New-SelfSignedCertificate -Type Custom `
        -Subject "CN=$username" `
        -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.2","2.5.29.17={text}upn=$username@localhost") `
        -KeyUsage DigitalSignature,KeyEncipherment `
        -KeyAlgorithm RSA `
        -KeyLength 2048

    # Export the public key
    $pem_output = @()
    $pem_output += "-----BEGIN CERTIFICATE-----"
    $pem_output += [System.Convert]::ToBase64String($cert.RawData) -replace ".{64}", "$&`n"
    $pem_output += "-----END CERTIFICATE-----"
    [System.IO.File]::WriteAllLines("$output_path\cert.pem", $pem_output)

    # Export the private key in a PFX file
    [System.IO.File]::WriteAllBytes("$output_path\cert.pfx", $cert.Export("Pfx"))
    

.. Note:: PFX ファイルを pywinrm が使用できる秘密鍵に変換するには、
    OpenSSL で次のコマンドを実行します
    ``openssl pkcs12 -in cert.pfx -nocerts -nodes -out cert_key.pem -passin pass: -passout pass:``

証明書ストアへの証明書のインポート
+++++++++++++++++++++++++++++++++++++++++++++
証明書が生成されたら、
発行証明書を ``LocalMachine`` ストアの ``信頼されたルート証明機関`` にインポートする必要があり、
クライアント証明書の公開鍵は、
``LocalMachine`` ストアの ``Trusted People`` ディレクトリーに保存する必要があります。この例では、
発行した証明書と公開鍵は同じになります。

以下の例では、発行した証明書をインポートする方法を示します。

.. code-block:: powershell

    $cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
    $cert.Import("cert.pem")

    $store_name = [System.Security.Cryptography.X509Certificates.StoreName]::Root
    $store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine
    $store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location
    $store.Open("MaxAllowed")
    $store.Add($cert)
    $store.Close()


.. Note:: ADCSを使用して証明書を生成する場合、
    発行する証明書は既にインポートされているため、この手順は省略できます。

クライアント証明書の公開鍵をインポートするコードは以下のとおりです。

.. code-block:: powershell

    $cert = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Certificate2
    $cert.Import("cert.pem")

    $store_name = [System.Security.Cryptography.X509Certificates.StoreName]::TrustedPeople
    $store_location = [System.Security.Cryptography.X509Certificates.StoreLocation]::LocalMachine
    $store = New-Object -TypeName System.Security.Cryptography.X509Certificates.X509Store -ArgumentList $store_name, $store_location
    $store.Open("MaxAllowed")
    $store.Add($cert)
    $store.Close()


証明書のアカウントへのマッピング
+++++++++++++++++++++++++++++++++++
証明書をインポートしたら、これをローカルユーザーアカウントにマッピングします。

    $username = "username"
    $password = ConvertTo-SecureString -String "password" -AsPlainText -Force
    $credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $username, $password

    # This is the issuer thumbprint which in the case of a self generated cert
    # is the public key thumbprint, additional logic may be required for other
    # scenarios
    $thumbprint = (Get-ChildItem -Path cert:\LocalMachine\root | Where-Object { $_.Subject -eq "CN=$username" }).Thumbprint

    New-Item -Path WSMan:\localhost\ClientCertificate `
        -Subject "$username@localhost" `
        -URI * `
        -Issuer $thumbprint `
        -Credential $credential `
        -Force


これが完了すると、hostvar ``ansible_winrm_cert_pem`` を公開鍵のパスに設定し、
``ansible_winrm_cert_key_pem`` 
変数を秘密鍵のパスに設定します。

NTLM
----
NTLM は、ローカルアカウントとドメインアカウントの両方を対応できる、
Microsoft 社が使用する古い認証メカニズムです。NTLM は、
デフォルトで WinRM サービスで有効になっていて、サービスを使用する前にセットアップは必要ありません。

NTLM は最も簡単に使用できる認証プロトコルであり、
``基本`` 認証よりも安全です。ドメイン環境で実行している場合は、NTLM の代わりに ``Kerberos`` 
を使用する必要があります。

Kerberos は NTLM の使用と比較して、以下のような利点があります。

* NTLM は古いプロトコルで、
  新しい暗号プロトコルに対応しません。
* NTLM は、
  認証段階でホストへのラウンドトリップをより多く必要とするため、認証に時間がかかります。
* Kerberos とは異なり、NTLM は認証情報の委譲を許可していません。

以下の例では、NTLM 認証を使用するように設定されているホスト変数を示しています。

.. code-block:: yaml+jinja

    ansible_user:LocalUsername
    ansible_password:Password
    ansible_connection: winrm
    ansible_winrm_transport: ntlm

Kerberos
--------
Kerberos は、
ドメイン環境に実行する際に使用する推奨認証オプションです。Kerberos は、
HTTP を介した認証情報の委譲やメッセージ暗号化などの機能に対応し、
WinRM を介して利用できるより安全なオプションの 1 つです。

Kerberos を適切に使用するには、
Ansible ホストでの追加のセットアップ作業が必要です。

以下の例は、Kerberos 認証に設定されたホスト変数を示しています。

.. code-block:: yaml+jinja

    ansible_user: username@MY.DOMAIN.COM
    ansible_password:Password
    ansible_connection: winrm
    ansible_winrm_transport: kerberos

Ansible バージョン 2.3 以降では、
Kerberos チケットは、``ansible_user`` および ``ansible_password`` に基づいて作成されます。古いバージョンの Ansible で実行している場合、
または ``ansible_winrm_kinit_mode`` が ``manual`` の場合は、
Kerberos チケットを取得しておく必要があります。詳細は、以下を参照してください。

設定可能な追加のホスト変数があります。

    ansible_winrm_kinit_mode: managed/manual (manual means Ansible will not obtain a ticket)
    ansible_winrm_kinit_cmd: the kinit binary to use to obtain a Kerberos ticket (default to kinit)
    ansible_winrm_service: overrides the SPN prefix that is used, the default is ``HTTP`` and should rarely ever need changing
    ansible_winrm_kerberos_delegation: allows the credentials to traverse multiple hops
    ansible_winrm_kerberos_hostname_override: the hostname to be used for the kerberos exchange

Kerberos ライブラリーのインストール
+++++++++++++++++++++++++++++++
Kerberos を使用する前にインストールする必要があるシステム依存関係があります。以下のスクリプトは、ディストリビューションに基づく依存関係を一覧表示します。

.. code-block:: shell

    # Via Yum (RHEL/Centos/Fedora)
    yum -y install python-devel krb5-devel krb5-libs krb5-workstation

    # Via Apt (Ubuntu)
    sudo apt-get install python-dev libkrb5-dev krb5-user

    # Via Portage (Gentoo)
    emerge -av app-crypt/mit-krb5
    emerge -av dev-python/setuptools

    # Via Pkg (FreeBSD)
    sudo pkg install security/krb5

    # Via OpenCSW (Solaris)
    pkgadd -d http://get.opencsw.org/now
    /opt/csw/bin/pkgutil -U
    /opt/csw/bin/pkgutil -y -i libkrb5_3

    # Via Pacman (Arch Linux)
    pacman -S krb5


依存関係がインストールされると、
``pip`` を使用して ``python-kerberos`` ラッパーをインストールできます。

.. code-block:: shell

    pip install pywinrm[kerberos]


ホスト Kerberos の設定
+++++++++++++++++++++++++
依存関係がインストールされたら、
ドメインと通信できるように Kerberosを 構成する必要があります。この構成は、
上記のスクリプトのパッケージとともにインストールされる ``/etc/krb5.conf`` ファイルを介して行われます。

Kerberos を設定するには、以下で始まるセクションで行います。

.. code-block:: ini

    [realms]

プライマリーおよびセカンダリーの Active Directory ドメインコントローラーの完全ドメイン名と、
完全修飾ドメイン名を追加します。これは、
次のようになります。

.. code-block:: ini

    [realms]
        MY.DOMAIN.COM = {
            kdc = domain-controller1.my.domain.com
            kdc = domain-controller2.my.domain.com
        }

以下で始まるセクションで、

.. code-block:: ini

    [domain_realm]

Ansible がアクセスする必要のある各ドメインに以下のような行を追加します。

.. code-block:: ini

    [domain_realm]
        .my.domain.com = MY.DOMAIN.COM

このファイルの他の設定 (デフォルトドメインなど) を設定できます。詳細は、
`krb5.conf <https://web.mit.edu/kerberos/krb5-1.12/doc/admin/conf_files/krb5_conf.html>`_
を参照してください。

Kerberos チケットの自動管理
++++++++++++++++++++++++++++++++++++
Ansible バージョン 2.3 以降では、
``ansible_user`` および ``ansible_password`` の両方がホストに指定されている場合は、デフォルトで Kerberos チケットが自動的に管理されます。このプロセスでは、
各ホストの一時的な認証情報キャッシュに、
新しいチケットが作成されます。これは、チケットが期限切れになる可能性を最小限に抑えるために、
各タスクが実行される前に行われます。一時的な認証情報キャッシュは、各タスクの完了後に削除され、
デフォルトの認証情報キャッシュに干渉しません。

自動チケット管理を無効にするには、
インベントリーから、``ansible_winrm_kinit_mode=manual`` を設定します。

自動チケット管理には、
コントロールホストシステムパス上に標準の ``kinit`` バイナリーが必要です。別の場所またはバイナリー名を指定するには、
``ansible_winrm_kinit_cmd`` hostvar を MIT krbv5 の、
``kinit`` と互換性のあるバイナリーへの完全修飾パスに設定します。

Kerberos チケットの手動管理
+++++++++++++++++++++++++++++++++
Kerberos チケットを手動で管理するには、``kinit`` バイナリーを使用します。新しいチケットを取得するには、
次のコマンドを使用します。

.. code-block:: shell

    kinit username@MY.DOMAIN.COM

.. Note:: ドメインは設定された Kerberos レルムに完全に一致し、大文字である必要があります。

取得したチケット (存在する場合) を確認するには、以下のコマンドを使用します。

.. code-block:: shell

    klist

取得したすべてのチケットを破棄するには、以下のコマンドを使用します。

.. code-block:: shell

    kdestroy

Kerberos のトラブルシューティング
++++++++++++++++++++++++
Kerberos は、
正しく機能するように構成された環境に依存しています。Kerberos の問題のトラブルシューティングを行うには、

* Windows ホストのホスト名には、IP アドレスではなく FQDN であることを確認します。

* 正引きおよび逆引きの DNS ルックアップがドメインで適切に機能しています。新しいチケットを取得するには、
  Windows ホストを名前で ping し、
  ``nslookup`` で返された IP アドレスを使用します。IP アドレスで ``nslookup`` を使用すると、
  同じ名前が返されます。

* Ansible ホストのクロックはドメインコントローラーと同期します。Kerberos は時間に敏感であり、
  わずかなクロックドリフトにより、
  チケット生成プロセスが失敗する可能性があります。

* ドメインの完全修飾ドメイン名が、
  ``krb5.conf`` ファイルで構成されていることを確認します。これを確認するには、以下を実行します。

    kinit -C username@MY.DOMAIN.COM
    klist

  ``klist`` によって返されるドメイン名が要求されたドメイン名とは異なる場合は、
  エイリアスが使用されています。別名ではなく完全修飾ドメイン名が使用されるように、
  ``krb5.conf`` ファイルを更新する必要があります。

* デフォルトの kerberos ツールが置き換えられるか、または変更されている場合 (一部の IdM ソリューションでこれを行う場合があります) は、Python Kerberos ライブラリーのインストールまたはアップグレード時に問題が発生する可能性があります。本書の執筆時点では、このライブラリーは ``pykerberos`` と呼ばれ、MIT ライブラリーと、Heimdal Kerberos ライブラリーの両方と連携していることが知られています。``pykerberos`` のインストールの問題を解決するには、Kerberos のシステム依存関係が満たされていることを確認し (`Installing the Kerberos Library`_ を参照)、PATH 環境変数からカスタム Kerberos ツーリングパスをすべて削除し、Python Kerberos ライブラリーパッケージのインストールを再試行します。

CredSSP
-------
CredSSP 認証は、
認証情報の委譲を許可する新しい認証プロトコルです。これは、
認証が成功した後にユーザー名とパスワードを暗号化し、
それを CredSSP プロトコルを使用してサーバーに送信することにより実現されます。

ユーザー名とパスワードはダブルホップ認証に使用されるサーバーに送信されるため、
Windows ホストが通信するホストが危険にさらされておらず、
信頼されていることを確認してください。

CredSSP は、ローカルアカウントとドメインアカウントの両方に使用でき、
HTTP を介したメッセージ暗号化もサポートしています。

CredSSP 認証を使用するには、以下のようにホスト変数を設定します。

.. code-block:: yaml+jinja

    ansible_user:Username
    ansible_password:Password
    ansible_connection: winrm
    ansible_winrm_transport: credssp

以下のように設定できる追加のホスト変数があります。

    ansible_winrm_credssp_disable_tlsv1_2: when true, will not use TLS 1.2 in the CredSSP auth process

CredSSP 認証は、Windows ホストではデフォルトで有効になっていませんが、
PowerShell で次を実行することで有効にできます。

.. code-block:: powershell

    Enable-WSManCredSSP -Role Server -Force

CredSSP ライブラリーのインストール
++++++++++++++++++++++++++

``requests-credssp`` ラッパーは、``pip`` を使用してインストールできます。

.. code-block:: bash

    pip install pywinrm[credssp]

CredSSP および TLS 1.2
+++++++++++++++++++
デフォルトでは、``requests-credssp`` ライブラリーは、
TLS 1.2 プロトコルを介して認証するように構成されています。TLS 1.2 は、
Windows Server 2012 および Windows 8 以降のリリースではデフォルトでインストールおよび有効化されます。

古いホストを CredSSP で使用できる方法は 2 つあります。

* ホットフィックスをインストールして有効にし、
  TLS 1.2 サポートを有効にします (Server 2008 R2およびWindows 7に推奨)。

* インベントリーで ``ansible_winrm_credssp_disable_tlsv1_2=True`` を設定して、
  TLS 1.0 で実行します。これは、
  TLS 1.2 に対応する方法がない Windows Server 2008 に接続する場合の唯一のオプションです

Windows ホストで TLS 1.2 を有効にする方法の詳細は、
「:ref:`winrm_tls12`」を参照してください。

CredSSP 証明書の設定
+++++++++++++++++++++++
CredSSP は TLS プロトコルを介して認証情報を暗号化することで機能し、デフォルトで自己署名証明書を使用します。WinRM サービス設定下の ``CertificateThumbprint`` オプションを使用して、
別の証明書の拇印を指定できます。

.. Note:: この証明書設定は、
    WinRM リスナーの証明書とは独立しています。CredSSP では、メッセージトランスポートは WinRM リスナー上で引き続き発生しますが、
    チャンネル内の TLS 暗号化メッセージはサービスレベルの証明書を使用します。

CredSSP に使用する証明書を明示的に設定するには、以下を実行します。

    # Note the value $certificate_thumbprint will be different in each
    # situation, this needs to be set based on the cert that is used.
    $certificate_thumbprint = "7C8DCBD5427AFEE6560F4AF524E325915F51172C"

    # Set the thumbprint value
    Set-Item -Path WSMan:\localhost\Service\CertificateThumbprint -Value $certificate_thumbprint

管理者以外のアカウント
``````````````````````````
WinRM は、デフォルトで、
ローカルの ``Administrators`` グループのアカウントからの接続のみを許可するように構成されています。これは以下を実行することで変更できます。

.. code-block:: powershell

    winrm configSDDL default

これにより ACL エディターが表示され、新規のユーザーまたはグループを追加できます。WinRM を介してコマンドを実行するには、
ユーザーとグループに、少なくとも ``Read`` および ``Execute`` のパーミッションが
有効になっている必要があります。

非管理アカウントは WinRM で使用できますが、
ほとんどの一般的なサーバー管理タスクにはある程度の管理アクセスが必要になるため、通常、ユーティリティーは制限されます。

WinRM 暗号化
````````````````
デフォルトでは、暗号化されていないチャンネルで実行すると WinRM は機能しません。
WinRM プロトコルは、TLS over HTTP (HTTPS) またはメッセージレベルの暗号化を使用している場合は、
チャンネルが暗号化されていると見なします。TLS での WinRM の使用は、
すべての認証オプションで機能するため推奨されるオプションですが、
WinRM リスナーで証明書を作成して使用する必要があります。

``ConfigureRemotingForAnsible.ps1`` は自己署名証明書を作成し、
その証明書を使用してリスナーを作成します。ドメイン環境の場合、
ADCS はドメイン自体が発行するホストの証明書も作成できます。

HTTPS の使用がオプションではない場合、
認証オプションが ``NTLM``、``Kerberos``、または ``CredSSP`` の場合は HTTP を使用できます。これらのプロトコルは、
サーバーに送信する前に、
独自の暗号化方法で WinRM ペイロードを暗号化します。暗号化は、代わりにより安全な TLS プロトコルを使用するため、
HTTPS で実行する場合、メッセージレベルの暗号化は使用されません。トランスポートとメッセージの両方の暗号化が必要な場合は、
ホスト変数の ``ansible_winrm_message_encryption=always`` 
を設定します。

最後の手段は、Windows ホストの暗号化要件を無効にすることです。```` は POSIX システムでエスケープ文字として使用されることが多いため、
操作でき、
リモートセッションは同じネットワーク上の誰でも完全に引き継ぐことができるため、
これは開発およびデバッグの目的でのみ使用する必要があります。暗号化要件を無効にするには、
以下を使用します::

    Set-Item -Path WSMan:\localhost\Service\AllowUnencrypted -Value $true

.. Note:: 絶対に必要でない限り、
    暗号化チェックを無効にしないでください。これにより、
    認証情報やファイルなどの機密情報がネットワーク上の他のユーザーに傍受される可能性があります。

インベントリーオプション
`````````````````
Ansible の Windows サポートは、
いくつかの標準変数に依存して、リモートホストのユーザー名、パスワード、接続タイプを示します。これらの変数は、インベントリーで最も簡単に設定できますが、
インベントリー最も簡単に設定できますが、``host_vars``/
レベルまたは ``group_vars`` レベルで設定します。

インベントリーを設定する際に、以下の変数が必要になります。

.. code-block:: yaml+jinja

    # It is suggested that these be encrypted with ansible-vault:
    # ansible-vault edit group_vars/windows.yml
    ansible_connection: winrm

    # May also be passed on the command-line via --user
    ansible_user: Administrator

    # May also be supplied at runtime with --ask-pass
    ansible_password: SecretPasswordGoesHere


上記の変数を使用して、
Ansible は HTTPS 経由の基本認証で Windows ホストに接続します。``ansible_user`` に ``username@MY.DOMAIN.COM`` のような UPN 値がある場合は、
``ansible_winrm_transport`` が、
``kerberos`` 以外に設定されていない限り、
認証オプションは自動的に Kerberos を使用しようとします。

WinRM 接続の追加構成では、
次のカスタムインベントリー変数も対応しています。

* ``ansible_port``: WinRM が実行するポートは、HTTPS が ``5986`` で、これがデフォルトとなります。
  HTTP は ``5985`` です。

* ``ansible_winrm_scheme``: WinRM 接続に使用する接続スキーム 
  (``http`` または ``https``) を指定します。Ansible は、``ansible_port`` が ``5985`` でない限り、
  デフォルトで ``https`` を使用します。

* ``ansible_winrm_path``:WinRM エンドポイントへの代替パスを指定します。
  Ansible はデフォルトで ``/wsman`` を使用します。

* ``ansible_winrm_realm``: Kerberos 
  認証に使用するレルムを指定します。``ansible_user`` に ``@`` が含まれている場合、
  Ansible は、

* デフォルトで ``ansible_winrm_transport`` の ``@`` に続くユーザー名の部分を使用します。1 つ以上の認証トランスポートオプションを
  コンマ区切りリストとして指定します。デフォルトでは、Ansible は、
  ``kerberos`` モジュールがインストールされていてレルムが定義されている場合は、``kerberos, basic`` を使用しますが、
それ以外の場合は ``plaintext`` になります。

* ``ansible_winrm_server_cert_validation``: サーバー証明書の検証モードを指定します 
  (``ignore`` または ``validate``) です。Ansible は、
  Python 2.7.9 以降では ``validate`` がデフォルトになります。
  Windows 自己署名証明書に対して証明書検証エラーが発生します。WinRM リスナーで検証可能な証明書が構成されていない限り、
  これは、
  ``ignore`` に設定する必要があります。

* ``ansible_winrm_operation_timeout_sec``: WinRM 操作のデフォルトのタイムアウトを増やします。
  Ansible は、デフォルトで ``20`` を使用します。

* ``ansible_winrm_read_timeout_sec``: WinRM 読み取りタイムアウトを増やすと、
  Ansible は、デフォルトで ``30`` を使用します。断続的なネットワークの問題があり、
  読み取りタイムアウトエラーが引き続き発生する場合に役立ちます。

* ``ansible_winrm_message_encryption``: 使用するメッセージ暗号化操作 (``auto``、``always``、``never``) をしています。
  Ansible は、デフォルトで ``auto`` を使用します。
  ``auto`` は、
  ``ansible_winrm_scheme`` が ``http`` であり、``ansible_winrm_transport`` がメッセージの暗号化をサポートしている場合にのみ、メッセージの暗号化が使用されることを意味します。
  ``always`` は、メッセージの暗号化が使用されることを意味します。
  ``never`` は、メッセージ暗号化が使用されないことを意味します。

* ``ansible_winrm_ca_trust_path``:``certifi`` モジュールで使用されるものとは異なる 
  cacert コンテナーを指定するために使用されます。HTTPS 証明書を参照してください。
  詳細は、「検証」セクションを参照してください。

* ``ansible_winrm_send_cbt``: HTTPS を介して ``ntlm`` または ``kerberos`` を使用すると、
  認証ライブラリーは、中間者攻撃を軽減するために、
  チャンネルバインディングトークンを送信しようとします。このフラグは、このようなバインディングが送信されるかどうかを制御します 
  (デフォルト: ``yes``)。

* ``ansible_winrm_*``: ``*`` の代わりに、
  ``winrm.Protocol`` でサポートされる追加のキーワード引数が提供されます。

さらに、
認証オプションごとに設定する必要がある特定の変数もあります。詳細は、上記の認証のセクションを参照してください。

.. Note:: Ansible 2.0 で、``ansible_ssh_user``、
    ``ansible_ssh_pass``、``ansible_ssh_host``、および ``ansible_ssh_port`` が廃止され、
    ``ansible_user``、``ansible_password``、``ansible_host``、
    および ``ansible_port`` になりました。2.0 より前のバージョンの Ansible を使用している場合は、
    古いスタイル (``ansible_ssh_*``) を代わりに使用する必要があります。Ansible の古いバージョンでは、
    短い変数は警告なしに無視されます。

.. Note:: ``ansible_winrm_message_encryption`` は、
    TLS を介して行われるトランスポートの暗号化とは異なります。WinRM ペイロードは、
    たとえ ``ansible_winrm_message_encryption=never`` であっても、HTTPS で実行された場合でも TLS で暗号化されます。

IPv6 アドレス
``````````````
IPv6 アドレスは、IPv4 アドレスまたはホスト名の代わりに使用できます。このオプションは、
通常、インベントリーに設定されます。Ansible は、
`ipaddress <https://docs.python.org/3/library/ipaddress.html>`_ パッケージを使用してアドレスを解析し、
pywinrm に正しく渡そうとします。

IPv6 アドレスを使用してホストを定義する場合は、
IPv4 アドレスまたはホスト名と同じように IPv6 アドレスを追加するだけです。

.. code-block:: ini

    [windows-server]
    2001:db8::1

    [windows-server:vars]
    ansible_user=username
    ansible_password=password
    ansible_connection=winrm


.. Note:: ipaddress ライブラリーは、デフォルトで Python 3.x にのみ含まれています。Python 2.7 で IPv6 アドレスを使用するには、
    バックポートされたパッケージをインストールする ``pip install ipaddress`` 
    を実行してください。

HTTPS 証明書の検証
````````````````````````````
TLS プロトコルの一部として、証明書が検証され、ホストがサブジェクトと一致し、
クライアントがサーバー証明書の発行者を信頼していることを確認します。
自己署名証明書、
または ``ansible_winrm_server_cert_validation: ignore`` 設定を使用する場合は、
これらのセキュリティーメカニズムを無視します。自己署名証明書は常に ``ignore`` フラグが必要ですが、
認証局から発行された証明書は
引き続き検証できます。

ドメイン環境で HTTPS リスナーを設定するより一般的な方法の 1 つは、
Active Directory 証明書サービス (AD CS) を使用することです。AD CS は、
証明書署名要求 (CSR) から署名付き証明書を生成するために使用されます。
WinRM HTTPS リスナーが AD CS などの別の機関によって署名された証明書を使用している場合は、
TLS ハンドシェイクの一部としてその発行者を信頼するように 
Ansible を設定できます。

Ansible が AD CS のような認証局 (CA) を信頼できるようにするには、
CA の発行者証明書を PEM エンコードされた証明書としてエクスポートできます。```` は POSIX システムでエスケープ文字として使用されることが多いため、
証明書検証のソースとして使用できます。
これは、CA チェーンとも呼ばれます。

CA チェーンには、1 つまたは複数の発行者証明書を含めることができ、
各エントリーは新しい行に含まれます。次に、検証プロセスの一部としてカスタム CA チェーンを使用するには、
``ansible_winrm_ca_trust_path`` 
をファイルのパスに設定します。この変数が設定されていない場合は、
Python パッケージ 
`certifi <https://github.com/certifi/python-certifi>`_ のインストールパスにあるデフォルトの CA チェーンが代わりに使用されます。

.. Note:: 各 HTTP 呼び出しは、
    システムに組み込まれた証明書ストアを信頼機関として使用しない Python 要求ライブラリーによって実行されます。
    サーバーの証明書発行者がシステムのトラストストアにのみ追加されている場合、
    証明書の検証は失敗します。

.. _winrm_tls12:

TLS 1.2 のサポート
```````````````
WinRM は HTTP プロトコルで実行されるため、
HTTPS を使用すると、TLS プロトコルが WinRM メッセージの暗号化に使用されます。TLS は、
クライアントとサーバーの両方で、
利用可能な最適なプロトコルと暗号スイートを自動的にネゴシエートしようとします。一致が見つからない場合、
Ansible は次のようなメッセージでエラーを出力します。

    HTTPSConnectionPool(host='server', port=5986):Max retries exceeded with url: /wsman (Caused by SSLError(SSLError(1, '[SSL: UNSUPPORTED_PROTOCOL] unsupported protocol (_ssl.c:1056)')))

一般的に、
これは Windows ホストが TLS v1.2 に対応するように構成されていない場合ですが、
Ansible コントローラーに古い OpenSSL バージョンがインストールされていることを意味する場合もあります。

Windows 8 と Windows Server 2012 には TLS v1.2 がインストールされ、
デフォルトで有効になっていますが、
Server 2008 R2 や Windows 7 などの古いホストは手動で有効にする必要があります。

.. Note:: Server 2008 の TLS 1.2 パッチには、
    Ansible が Windows ホストに接続するのを停止するバグがあります。これは、
    TLS 1.2 を使用するように Server 2008 を構成できないことを意味します。Server 2008 R2 および Windows 7 はこの問題の影響を受けず、
    TLS 1.2 を使用できます。

Windows ホストが対応しているプロトコルを確認するには、
Ansible コントローラーで次のコマンドを実行します::

    openssl s_client -connect <hostname>:5986

出力には TLS セッションに関する情報が含まれ、
``Protocol`` 行にはネゴシエートされたバージョンが表示されます。

    New, TLSv1/SSLv3, Cipher is ECDHE-RSA-AES256-SHA
    Server public key is 2048 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    No ALPN negotiated
    SSL-Session:
        Protocol  : TLSv1
        Cipher    : ECDHE-RSA-AES256-SHA
        Session-ID: 962A00001C95D2A601BE1CCFA7831B85A7EEE897AECDBF3D9ECD4A3BE4F6AC9B
        Session-ID-ctx:
        Master-Key: ....
        Start Time: 1552976474
        Timeout   : 7200 (sec)
        Verify return code: 21 (unable to verify the first certificate)
    ---

    New, TLSv1/SSLv3, Cipher is ECDHE-RSA-AES256-GCM-SHA384
    Server public key is 2048 bit
    Secure Renegotiation IS supported
    Compression: NONE
    Expansion: NONE
    No ALPN negotiated
    SSL-Session:
        Protocol  : TLSv1.2
        Cipher    : ECDHE-RSA-AES256-GCM-SHA384
        Session-ID: AE16000050DA9FD44D03BB8839B64449805D9E43DBD670346D3D9E05D1AEEA84
        Session-ID-ctx:
        Master-Key: ....
        Start Time: 1552976538
        Timeout   : 7200 (sec)
        Verify return code: 21 (unable to verify the first certificate)

ホストが ``TLSv1`` を返す場合は、
TLS v1.2 が有効になるように構成する必要があります。これを行うには、
次の PowerShell スクリプトを実行します。

.. code-block:: powershell

    Function Enable-TLS12 {
        param(
            [ValidateSet("Server", "Client")]
            [String]$Component = "Server"
        )

        $protocols_path = 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols'
        New-Item -Path "$protocols_path\TLS 1.2\$Component" -Force
        New-ItemProperty -Path "$protocols_path\TLS 1.2\$Component" -Name Enabled -Value 1 -Type DWORD -Force
        New-ItemProperty -Path "$protocols_path\TLS 1.2\$Component" -Name DisabledByDefault -Value 0 -Type DWORD -Force
    }

    Enable-TLS12 -Component Server

    # Not required but highly recommended to enable the Client side TLS 1.2 components
    Enable-TLS12 -Component Client

    Restart-Computer

以下の Ansible タスクを使用して TLS v1.2 を有効にすることもできます。

.. code-block:: yaml+jinja

    - name: enable TLSv1.2 support
      win_regedit:
        path: HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.2\{{ item.type }}
        name: '{{ item.property }}'
        data: '{{ item.value }}'
        type: dword
        state: present
      register: enable_tls12
      loop:
      - type: Server
        property: Enabled
        value: 1
      - type: Server
        property: DisabledByDefault
        value: 0
      - type: Client
        property: Enabled
        value: 1
      - type: Client
        property: DisabledByDefault
        value: 0

    - name: reboot if TLS config was applied
      win_reboot:
      when: enable_tls12 is changed
    
Windows ホストが提供する暗号スイートと同様に、
TLS プロトコルを構成する方法は他にもあります。このような設定を管理する GUI を提供できるツールの 1 つに、
Nartac Software 社の「`IIS Crypto <https://www.nartac.com/Products/IISCrypto/>`_」
が

あります。
```````````
WinRM プロトコルの設計により、WinRM を使用するときにいくつかの制限があり、
Ansible の Playbook を作成するときに問題が発生する可能性があります。
これには、以下が含まれます。

* 認証情報はほとんどの認証タイプに委譲されないため、
  ネットワークリソースにアクセスしたり、
  特定のプログラムをインストールするときに認証エラーが発生します。

* WinRM 経由で実行すると、Windows Update API への多くの呼び出しがブロックされます。

* 認証情報の委譲がない、または WinRM 経由の WUA などの禁止 Windows API にアクセスするため、
  一部のプログラムは WinRM でインストールできません。

* WinRM の下のコマンドは、非対話型セッションで実行されます。
  これにより、特定のコマンドまたは実行ファイルの実行が妨げられる可能性があります。

* 一部のインストーラー (Microsoft SQL Server など) で使用される ``DPAPI`` 
  と対話するプロセスを実行することはできません。

この制限の一部は、以下のいずれかを実行して軽減できます。

* (``ansible_winrm_kerberos_delegation=true`` で) ``ansible_winrm_transport`` を ``credssp`` または ``kerberos`` に設定し、
  ダブルホップの問題を回避します。
  ネットワークリソースへアクセスします。

* すべての WinRM 制限を回避し、ローカルと同じようにコマンドを実行するには、``become`` 
  を使用します。``credssp`` のような認証トランスポートを使用する場合とは異なり、
  これは非インタラクティブな制限と、
  WUA や DPAPI などの API 制限も削除します。

* スケジュールされたタスクを使用して、
  ``win_scheduled_task`` モジュールで作成できるコマンドを実行します。``become`` になるように、
  これはすべての WinRM 制限を回避して、モジュールではなくコマンドのみを実行できます。


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
       #ansible IRC chat channel
