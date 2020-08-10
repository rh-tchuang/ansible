.. _developing_modules_general_windows:

**************************************
Windows モジュールウォークスルー
**************************************

本セクションでは、
Ansible Windows モジュールの開発、テスト、デバッグの開発手順 (ウォークスルー) を説明します。

Windows モジュールは Powershell で書かれており、
Windows ホスト上で実行する必要があるため、このガイドは通常の開発ウォークスルーガイドとは異なります。

本項で説明する内容:

.. contents::
   :local:


Windows 環境の設定
=========================

Ansible を実行するホストで実行できる Python モジュール開発とは異なり、
Windows モジュールは、Windows ホスト用に記述してテストする必要があります。
Windows の評価版は Microsoft からダウンロードすることができますが、
このイメージは通常、
さらに修正を加えなければ Ansible で使用できません。Ansible で使用できるように Windows ホストをセットアップする最も簡単な方法は、
Vagrant を使用して仮想マシンをセットアップすることです。
Vagrantは、ボックス (*box*) と呼ばれる既存の OS イメージをダウンロードして、
VirtualBox のようなハイパーバイザーにデプロイするために使用されます。これらのボックスはオフラインで作成して保存するか、
Vagrant Cloud 
と呼ばれる中央リポジトリーからダウンロードします。

このガイドでは、
`Vagrant Cloud <https://app.vagrantup.com/boxes/search?utf8=%E2%9C%93&sort=downloads&provider=&q=jborean93>`_ にもアップロードされている `packer-windoze <https://github.com/jborean93/packer-windoze>`_ リポジトリーで作成された Vagrant ボックスを使用します。
これらのイメージがどのように作成されているかの詳細は、
GitHubのリポジトリーにある ``README`` ファイルを参照してください。

作業を開始する前に、
以下のプログラムをインストールする必要があります (インストール方法は Vagrant および VirtualBox のドキュメントを参照してください)。

- Vagrant
- VirtualBox

仮想マシンで Windows サーバーを作成
===============================

1 つの Windows Server 2016 インスタンスを作成するには、次のコマンドを実行します。

.. code-block:: shell

    vagrant init jborean93/WindowsServer2016
    vagrant up

これにより、Vagrant Cloud から Vagrant ボックスをダウンロードしてホスト上のローカルボックスに追加し、
VirtualBox でそのインスタンスを起動します。初めて起動すると、
Windows の仮想マシンは、sysprep プロセスを経て、
HTTP および HTTPS の WinRM リスナーを自動的に作成します。Vagrant はリスナーがオンラインになるとプロセスを終了します。
これで、仮想マシンが Ansible で使用できるようになりました。

Ansible インベントリーの作成
===========================

以下の Ansible インベントリーファイルを使用して、
新しく作成した Windows 仮想マシンに接続できます。

.. code-block:: ini

    [windows]
    WindowsServer  ansible_host=127.0.0.1

    [windows:vars]
    ansible_user=vagrant
    ansible_password=vagrant
    ansible_port=55986
    ansible_connection=winrm
    ansible_winrm_transport=ntlm
    ansible_winrm_server_cert_validation=ignore

.. note:: ポート ``55986`` は、Vagrant により、作成された Windows ホストに転送されます。
    これが既存のローカルポートと競合すると、
    Vagrant は自動的にランダムに別のポートを使用し、
    出力にその旨を表示します。

作成される OS はイメージセットに基づいています。以下のイメージが
使用できます。

- `jborean93/WindowsServer2008-x86 <https://app.vagrantup.com/jborean93/boxes/WindowsServer2008-x86>`_
- `jborean93/WindowsServer2008-x64 <https://app.vagrantup.com/jborean93/boxes/WindowsServer2008-x64>`_
- `jborean93/WindowsServer2008R2 <https://app.vagrantup.com/jborean93/boxes/WindowsServer2008R2>`_
- `jborean93/WindowsServer2012 <https://app.vagrantup.com/jborean93/boxes/WindowsServer2012>`_
- `jborean93/WindowsServer2012R2 <https://app.vagrantup.com/jborean93/boxes/WindowsServer2012R2>`_
- `jborean93/WindowsServer2016 <https://app.vagrantup.com/jborean93/boxes/WindowsServer2016>`_

ホストがオンラインになっている場合は、RDP を介して ``127.0.0.1:3389`` でアクセスできますが、
競合があるとポートが異なる場合があります。ホストを削除するには、
``vagrant destroy --force`` を実行すると、
Vagrant は自動的に仮想マシンと、その仮想マシンに関連付けられている他のファイルを削除します。

これは、1 つの Windows インスタンスでモジュールをテストする際に便利ですが、
ドメインベースのモジュールではこれらのホストは変更なしでは動作しません。`ansible-windows <https://github.com/jborean93/ansible-windows/tree/master/vagrant>`_ 
にある Vagrantfile は、
Ansible で使用するテストドメイン環境を作成するために使用できます。このリポジトリーには、
Ansible と Vagrant の両方がドメイン環境で複数の Windows ホストを作成するのに使用する 
3 つのファイルが含まれています。これらのファイルは以下のようになります。

- ``Vagrantfile`` - ``inventory.yml`` のインベントリー設定を読み込んで、必要なホストをプロビジョニングする Vagrant ファイルです。
- ``inventory.yml`` - 必要なホストと、IP アドレスや転送ポートなどの他の接続情報が含まれています。
- ``main.yml`` - Vagrant より呼び出された Ansible Playbook は、ドメインコントローラーをプロビジョニングし、子ホストをドメインに参加させます。

デフォルトでは、これらのファイルは以下の環境を作成します。

- Windows Server 2016 で実行しているドメインコントローラー 1 つ
- ドメインに参加している各 Windows Server のメジャーバージョンの子ホスト 5 台
- ドメイン (DNS 名 ``domain.local``)
- 各ホストのローカル管理者アカウント (ユーザー名 ``vagrant`` およびパスワード ``vagrant``)
- ドメイン管理者アカウント ``vagrant-domain@domain.local`` (パスワード ``VagrantPass1``)

ドメイン名とアカウントは、
必要に応じて ``inventory.yml`` ファイル内の変数 ``domain_*`` を変更することで変更できます。また、インベントリーファイルは、
``domain_children`` キーの下に定義されているホストを変更することで、
より多く (またはより少ない) サーバーをプロビジョニングするように変更することもできます。ホスト変数 ``ansible_host`` は、
VirtualBox のホスト専用ネットワークアダプターに割り当てられるプライベート IP で、
``vagrant_box`` は、
仮想マシンの作成に使用されるボックスです。

環境のプロビジョニング
============================

そのまま環境をプロビジョニングするには、次を実行します。

.. code-block:: shell

    git clone https://github.com/jborean93/ansible-windows.git
    cd vagrant
    vagrant up

.. note:: Vagrant は各ホストを順次プロビジョニングしていくため、
    完了するまでに時間がかかることがあります。もし、ドメインを設定する Ansible フェーズでエラーが発生した場合は、
    ``vagrant provision`` を実行してそのステップを再実行してください。

Vagrant で Windows インスタンスを 1つ設定するのとは異なり、
これらのホストには転送ポートだけでなく、
IP アドレスを使用して直接アクセスすることもできます。通常のプロトコルポートが使用されるため、
ホスト専用のネットワークアダプターを使用してアクセスする方が簡単です。たとえば、RDP は現在も ``3389`` で使用されています。ホストのみのネットワーク IP を使用して解決できない場合は、
以下の転送ポートを使用して 、
``127.0.0.1`` を介して以下のプロトコルにアクセスすることができます。

- ``RDP``: 295xx
- ``SSH``: 296xx
- ``WinRM HTTP``: 297xx
- ``WinRM HTTPS``: 298xx
- ``SMB``: 299xx

``xx`` を、
ドメインコントローラーが ``00`` で始まり、そこからインクリメントされるインベントリーファイルのエントリー番号に置き換えます。たとえば、
デフォルトの ``inventory.yml`` ファイルでは、
WinRM over HTTPS for ``SERVER2012R2`` は ``domain_children`` の 4 番目のエントリーであるため、ポート ``29804`` で転送されます。

.. note:: SSH サーバーは、Server 2008 (R2 以外) を除くすべての Windows ホストで利用できますが、
    Windows ホストを管理する Ansible のサポート接続ではないため、
    Ansible では使用しないでください。

Windows 新しいモジュール開発
==============================

新しいモジュールを作成する際には、以下の点に留意してください。

- モジュールのコードは Powershell (.ps1) ファイルにあり、ドキュメントは同じ名前の Python (.py) ファイルに含まれています。
- モジュールでは ``Write-Host/Debug/Verbose/Error`` を使用せず、``$module.Result`` 変数に返す必要のあるものを追加します。
- モジュールを失敗させるには、``$module.FailJson("failure message here")`` を呼び出して、Exception または ErrorRecord を 2 番目の引数に設定して、より詳細なエラーメッセージを表示できます。
- 例外または ErrorRecord を 2 つ目の引数として ``FailJson("failure", $_)`` に渡すと、より詳細な出力を取得できます。
- ほとんどの新規モジュールには、主要な Ansible コードベースにマージする前にチェックモードと統合テストが必要です。
- 大規模なコードブロックで try/catch 文を使用するのは避け、個別の呼び出しに使用することで、エラーメッセージがより分かりやすくなるようにします。
- Try/catch 文の使用時に特定の例外を試して捕え (キャッチし) ます。
- 必要な場合を除き PSCustomObject は使用しないでください。
- 重複する作業を行わないように、``./lib/ansible/module_utils/powershell/`` にある共通の関数を探して、そこにあるコードを使用してください。これらの関数は  ``#Requires -Module *`` という行を追加することでインポートすることができます。* はインポートするファイル名で、Ansible を介して実行する場合に、自動的に Windows ターゲットに送信されたモジュールコードが含まれています。
- PowerShell モジュールユーティリティーの他に、C# モジュールユーティリティーが ``./lib/ansible/module_utils/csharp/`` にあります。これは、``#AnsibleRequires -CSharpUtil *`` 行が存在する場合に、モジュール実行に自動的にインポートされます。
- C# および PowerShell モジュールユーティリティーは同じ目的を達成していますが、C# では Win32 API の呼び出しなどの低レベルのタスクを実装することができるため、場合によってはより速く達成できます。
- このコードが Windows Server 2008 以降の Powershell v3 以降で動作することを確認してください。最小バージョンより新しい Powershell または OS が必要な場合は、ドキュメントにこの内容が明確に反映されていることを確認してください。
- Ansible は、strictmode バージョン 2.0 でモジュールを実行します。必ず、開発スクリプトの先頭に ``Set-StrictMode -Version 2.0`` と記述して、この機能を有効にしてテストしてください。
- 可能であれば、実行可能な呼び出しよりも、ネイティブの Powershell コマンドレットを優先してください。
- エイリアスの代わりに完全なコマンドレット名を使用してください (例: ``rm`` ではなく ``Remove-Item``)。
- コマンドレットで名前付きパラメーターを使用します (例: ``Remove-Item C:\temp`` ではなく ``Remove-Item -Path C:\temp``)。

非常に基本的なパワーシェルモジュール `win_environment <https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/windows/win_environment.ps1>`_ が以下に含まれています。これは、check-mode および diff-support を実装する方法を示し、特定の条件が満たされるとユーザーに警告を表示します。

.. .. include:: ../../../../lib/ansible/modules/windows/win_environment.ps1
..    :code: powershell

.. literalinclude:: ../../../../lib/ansible/modules/windows/win_environment.ps1
   :language: powershell

もう少し高度なモジュールとしては `win_uri <https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/windows/win_uri.ps1>`_ がありますが、ここで、さまざまなパラメーター型 (bool、str、int、list、dict、path) の使用方法やパラメーターの選択方法、モジュールを失敗させる方法、例外の処理方法などを紹介しています。

新しい ``AnsibleModule`` ラッパーの一部として、入力パラメーターが定義され、
引数の仕様に基づいて検証されます。以下のオプションは、引数仕様のルートレベルで設定できます。

- ``mutually_exclusive``: リストのリストで、内側のリストには一緒に設定できないモジュールオプションが含まれています。
- ``no_log``: モジュールが Windows イベントログにログを出力しないようにします。
- ``options``: キーがモジュールオプションで、値がそのオプションの仕様となるディクショナリーです。
- ``required_by``: キーで指定されたオプションが設定されている場合に、値で指定されたオプションも設定しなければならないディクショナリーです。
- ``required_if``: 3 または 4 つの要素が含まれるリストが記載されるリストです。
    * 最初の要素は、値を確認するモジュールオプションです。
    * 2 つ目の要素は、1 つ目の要素によって指定されるオプションの値です。一致すると必須の if チェックが実行します。
    * 3 つ目の要素は、上記が一致した場合に必要なモジュールオプションのリストです。
    *  4 番目の要素 (任意) は、3 番目の要素のすべてのモジュールオプションが必要なのか (デフォルト: ``$false``)、1 つだけが必要なのか (``$true``) を示すブール値です。
- ``required_one_of``: 少なくとも 1 つは設定しなければならないモジュールオプションが含まれているリストが記載されるリストです。
- ``required_together``: 一緒に設定しなければならないモジュールオプションが含まれているリストが記載されるリストです。
- ``supports_check_mode``: モジュールがチェックモードに対応しているかどうか (デフォルトは ``$false`` です)。

モジュールの実際の入力オプションは、``options`` 値内にディクショナリーとして設定されます。このディレクトリーのキーはモジュールオプション名であり、
値はそのモジュールオプションの仕様です。各仕様には、
以下のオプションを設定できます。

- ``aliases``: モジュールオプションのエイリアスのリストです。
- ``choices``: モジュールオプションの有効な値のリストです。``type=list`` の場合、各リストの値が choices に対して検証され、リスト自体は検証されません。
- ``default``: モジュールオプションのデフォルト値 (設定されていない場合)
- ``elements``: ``type=list`` の場合、各リスト値のタイプが設定され、値は ``type`` と同じになります。
- ``no_log``: ``module_invocation`` 戻り値で返される前に入力値をサニタイズします。
- ``removed_in_version``: 非推奨のモジュールオプションを削除すると、警告が設定されている場合はエンドユーザーに警告が表示されます。
- ``required``: モジュールオプションが設定されていないと失敗します。
- ``type``: モジュールオプションのタイプです。設定されていない場合は、デフォルトで ``str`` に設定されます。有効なタイプは以下のとおりです。
    * ``bool``: ブール値です。
    * ``dict``: ディクショナリーの値です。入力が JSON または key=value 文字列の場合は、ディクショナリーに変換されます。
    * ``float``: float または `Single` <https://docs.microsoft.com/en-us/dotnet/api/system.single?view=netframework-4.7.2>_ 値
    * ``int``: Int32 値
    * ``JSON``: 入力がディクショナリーである場合に値が JSON 文字列に変換される文字列です。
    * ``list``: 値のリスト。``elements=<type>`` は、設定されている場合に個別のリスト値タイプを変換できます。``elements=dict`` の場合、``options`` が定義されると、値は引数仕様に対して検証されます。入力が文字列である場合、文字列は ``,`` で分割され、空白文字はすべてトリミングされます。
    * ``path``: ``%TEMP%`` などの値が環境値に基づいて展開される文字列。入力値が ``\\?\`` で始まると、展開は実行されません。
    * ``raw``: Ansible によって渡される値で変換が行われません。
    * ``SID``: Windows セキュリティー識別子の値または Windows アカウント名を `SecurityIdentifier <https://docs.microsoft.com/en-us/dotnet/api/system.security.principal.securityidentifier?view=netframework-4.7.2>`_ 値に変換します。
    * ``str``: 値は文字列に変換されます。

``type=dict`` または ``type=list`` および ``elements=dict`` の場合は、そのモジュールオプションに以下のキーを設定することもできます。

- 値は、``True`` の場合はそのキーの ``options`` 仕様のデフォルトになり、``False`` の場合は null です。モジュールオプションがユーザーによって定義されておらず、``type=dict`` の場合に限り有効です。
- ``mutually_exclusive``: ルートレベルの ``mutually_exclusive`` と同じですが、サブディクショナリーの値に対して検証されます。
- ``options``: ルートレベルの ``options`` と同じですが、サブオプションの有効なオプションが含まれています。
- ``required_if``: ルートレベルの ``required_if`` と同じですが、サブディクショナリーの値に対して検証されます。
- ``required_by``: ルートレベルの ``required_by`` と同じですが、サブディクショナリーの値に対して検証されます。
- ``required_together``: ルートレベルの ``required_together`` と同じですが、サブディクショナリーの値に対して検証されます。
- ``required_one_of``: ルートレベルの ``required_one_of`` と同じですが、サブディクショナリーの値に対して検証されます。

モジュール型は、値をモジュールオプションで必要とされるものに変換するデリゲート関数にすることもできます。たとえば、
次のスニペットの例は、``UInt64`` 値を作成するカスタム型を作成する方法を示しています。

.. code-block:: powershell

    $spec = @{
        uint64_type = @{ type = [Func[[Object], [UInt64]]]{ [System.UInt64]::Parse($args[0]) } }
    }
    $uint64_type = $module.Params.uint64_type

不明な場合は、他のコアモジュールを見て、
そこにどのように実装されているかを見てみましょう。

Windows がタスクを完了させるために、複数の方法が提示されることがあります。
モジュールを書くときに好ましい順序は以下のようになります。

- ネイティブの Powershell コマンドレット (``Remove-Item -Path C:\temp -Recurse`` など)
- .NET クラス (``[System.IO.Path]::GetRandomFileName()`` など)
- (``New-CimInstance`` コマンドレットを使用した) WMI オブジェクト
- (``New-Object -ComObject`` コマンドレットを使用した) COM オブジェクト
- ``Secedit.exe`` などのネイティブ実行ファイルへの呼び出し

PowerShell モジュールは、PowerShell に組み込まれている ``#Requires`` オプションの一部と、
``#AnsibleRequires`` で指定されている 
Ansible 固有の要件をサポートしています。これらのステートメントはスクリプトの任意の場所に配置することができますが、
最も一般的なのはスクリプトの先頭付近です。これらを使用することで、
チェック項目を書かなくてもモジュールの要件を簡単に記述できるようになります。各 ``requires`` 文は、
それぞれ独立した行に記述しなければなりませんが、
1 つのスクリプトに複数の requires 文を記述することができます。

以下のチェックは、Ansible モジュール内で使用できます。

- ``#Requires -Module Ansible.ModuleUtils.<module_util>``: Ansible 2.4 で追加され、モジュール実行のために読み込む module_util を指定します。
- ``#Requires -Version x.y``: Ansible 2.5 で追加され、モジュールに必要な PowerShell のバージョンを指定します。この要件を満たしていないと、モジュールは失敗します。
- ``#AnsibleRequires -OSVersion x.y``: Ansible 2.5 で追加され、モジュールが必要とする OS ビルドバージョンを指定します。この要件を満たしていない場合は失敗します。実際の OS バージョンは ``[Environment]::OSVersion.Version`` から得られます。
- ``#AnsibleRequires -Become``: Ansible 2.5 で追加され、exec ランナーが ``become`` でモジュールを強制的に実行します。これは主に WinRM の制限を回避するために使用されます。``ansible_become_user`` を指定しないと、代わりに ``SYSTEM`` アカウントが使用されます。
- ``#AnsibleRequires -CSharpUtil Ansible.<module_util>``: Ansible 2.8 で追加され、モジュール実行に読み込む C# module_unil を指定します。

他のすべての using 文を使用する場合は、スクリプトの先頭に ``using Ansible.<module_util>;`` 行を使用すると、
その他の C# のモジュールユーティリティーを参照できます。


Windows モジュールユーティリティー
========================

Python モジュールと同様、
PowerShell モジュールにも PowerShell 内でヘルパー関数を提供するモジュールユーティリティーが多数用意されています。これらの module_utils は、
PowerShell モジュールに以下の行を追加することでインポートできます。

.. code-block:: powershell

    #Requires -Module Ansible.ModuleUtils.Legacy

これにより、``./lib/ansible/module_utils/powershell/Ansible.ModuleUtils.Legacy.psm1`` にあるmodule_util がインポートされ、
そのすべての関数を呼び出すことができるようになります。Ansible 2.8 では、
Windows モジュールユーティリティーを C# で記述し、``lib/ansible/module_utils/csharp`` に保存することもできます。
これらの module_utils は、
PowerShell モジュールに次の行を追加することでインポートできます。

.. code-block:: powershell

    #AnsibleRequires -CSharpUtil Ansible.Basic

これにより、
``./lib/ansible/module_utils/csharp/Ansible.Basic.cs`` にある module_util をインポートし、実行中の型を自動的に読み込みます。C# モジュールユーティリティーは、ユーティリティーの先頭にある using 文に以下の行を追加することで、お互いを参照して一緒に読み込むことができます。

.. code-block:: csharp

    using Ansible.Become;

C# ファイルには、コンパイルパラメーターを制御するために設定できる特別なコメントがあります。以下のコメントをスクリプトに追加することができます。

- ``//AssemblyReference -Name <assembly dll> [-CLR [Core|Framework]]``: コンパイル中に参照するアセンブリー DLL です。任意の ``-CLR`` フラグを使用して、.NET Core、Framework、またはその両方 (省略されている場合) で実行するときに参照するかどうかを表示することもできます。
- ``//NoWarn -Name <error id> [-CLR [Core|Framework]]``: コードをコンパイルする際に無視するコンパイラー警告 ID です。任意の ``-CLR`` は上記と同じように機能します。警告のリストは、「`コンパイラーエラー <https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-messages/index>`_」を参照してください。

この他に、以下のプリプロセッサーシンボルも定義されています。

- ``CORECLR``: このシンボルは、PowerShell が .NET Core を介して実行されている場合に表示されます。
- ``WINDOWS``: このシンボルは、PowerShell が Windows で実行している場合に表示されます。
- ``UNIX``: このシンボルは、PowerShell が Unix で実行している場合に表示されます。

これフラグの組み合わせは、
.NET Framework と .NET Core の両方でモジュールユーティリティーを相互運用可能にするのに役立ちます。

.. code-block:: csharp

    #if CORECLR
    using Newtonsoft.Json;
    #else
    using System.Web.Script.Serialization;
    #endif

    //AssemblyReference -Name Newtonsoft.Json.dll -CLR Core
    //AssemblyReference -Name System.Web.Extensions.dll -CLR Framework

    // Ignore error CS1702 for all .NET types
    //NoWarn -Name CS1702

    // Ignore error CS1956 only for .NET Framework
    //NoWarn -Name CS1956 -CLR Framework


以下に Ansible と一緒にパッケージ化されている module_utils リストと、
それらが何をするのかの一般的な説明を示します。

- ArgvParser: 引数のリストを Windows の引数解析ルールに準拠しているエスケープされた文字列に変換するのに使用されるユーティリティー。
- CamelConversion: camelCase strings/lists/dicts を snake_case に変換するのに使用されるユーティリティー。
- CommandUtil: Windows プロセスを実行し、stdout/stderr と rc を異なるオブジェクトとして返すために使用されるユーティリティー。
- FileUtil: ``C:\pagefile.sys`` のような特殊なファイルを扱うために ``Get-ChildItem`` および ``Test-Path`` を拡張するユーティリティー。
- Legacy: Ansible モジュールの一般的な定義およびヘルパーユーティリティー。
- LinkUtil: シンボリックリンク、分岐点、ハードインクに関する情報を作成、削除、取得するユーティリティー。
- SID: ユーザーやグループを Windows SID に変換したり、Windows SID をユーザーやグループに変換するのに使用するユーティリティー。

特定のモジュールユーティリティーとその要件に関する詳細は、`「Ansible 
モジュールユーティリティーのソースコード <https://github.com/ansible/ansible/tree/devel/lib/ansible/module_utils/powershell>`_」を参照してください。

PowerShell モジュールユーティリティーは、カスタムモジュールで使用するために、
標準の Ansible ディストリビューションの外に保存できます。カスタム module_utils は、
Playbook またはロールのルートディレクトリーにある ``module_utils`` 
という名前のディレクトリーに置かれます。

C# モジュールユーティリティーは、カスタムモジュールで使用するために、標準の Ansible ディストリビューションの外に保存することもできます。PowerShell ユーティリティーと同様、``module_utils`` という名前のディレクトリーに保存され、
ファイル名は拡張子 ``.cs`` で終わり、``Ansible.`` で始まり、ユーティリティーで定義された名前空間にちなんだ名前でなければなりません。

次の例は、
``Ansible.ModuleUtils.ModuleUtil1`` および ``Ansible.ModuleUtils.ModuleUtil2`` と呼ばれる 2 つの PowerShell カスタム module_utils と、``Ansible.CustomUtil`` という名前の名前空間を含む C# ユーティリティーを含むロール構造です。

    meta/
      main.yml
    defaults/
      main.yml
    module_utils/
      Ansible.ModuleUtils.ModuleUtil1.psm1
      Ansible.ModuleUtils.ModuleUtil2.psm1
      Ansible.CustomUtil.cs
    tasks/
      main.yml

各 PowerShell module_util は、
ファイルの最後に ``Export-ModuleMember`` でエクスポートされた関数を少なくとも 1 つ含まなければなりません。たとえば、以下のようになります。

.. code-block:: powershell

    Export-ModuleMember -Function Invoke-CustomUtil, Get-CustomInfo


Windows Playbook モジュールのテスト
===============================

Ansible Playbook でモジュールをテストできます。例:

- Playbook ``touch testmodule.yml`` をディレクトリーに作成します。
- 同じディレクトリーにインベントリーファイル ``touch hosts`` を作成します。
- Windows ホストへの接続に必要な変数を指定してインベントリーファイルを設定します。
- 以下を新しい Playbook ファイルに追加します。

    ---
    - name: test out windows module
      hosts: windows
      tasks:
      - name: test out module
        win_module:
          name: test name

- Playbook ``ansible-playbook -i hosts testmodule.yml`` を実行します。

これは、
新しいモジュールを使用して Ansible がどのように動作するかを端から端まで確認するのに便利です。モジュールをテストする他の方法には、
以下ようなものがあります。


Windows のデバッグ
=================

現在、モジュールのデバッグは Windows ホスト上でしかできません。これは新しいモジュールを開発したり、
バグの修正を実装したりするときに便利です。これを設定するために
必要な手順をいくつか紹介します。

- モジュールスクリプトを Windows サーバーにコピーします。
- ``./lib/ansible/module_utils/powershell`` および ``./lib/ansible/module_utils/csharp`` を上記のスクリプトと同じディレクトリーにコピーします。
- モジュールコードにあるすべての ``#Requires -Module`` 行の先頭に ``#`` を追加してください。これは、``#Requires -Module`` で始まる行にのみ必要です。
- 以下を、サーバーにコピーされたモジュールスクリプトの先頭に追加します。

.. code-block:: powershell

    # Set $ErrorActionPreference to what's set during Ansible execution
    $ErrorActionPreference = "Stop"

    # Set the first argument as the path to a JSON file that contains the module args
    $args = @("$($pwd.Path)\args.json")

    # Or instead of an args file, set $complex_args to the pre-processed module args
    $complex_args = @{
        _ansible_check_mode = $false
        _ansible_diff = $false
        path = "C:\temp"
        state = "present"
    }

    # Import any C# utils referenced with '#AnsibleRequires -CSharpUtil' or 'using Ansible.;
    # The $_csharp_utils entries should be the context of the C# util files and not the path
    Import-Module -Name "$($pwd.Path)\powershell\Ansible.ModuleUtils.AddType.psm1"
    $_csharp_utils = @(
        [System.IO.File]::ReadAllText("$($pwd.Path)\csharp\Ansible.Basic.cs")
    )
    Add-CSharpType -References $_csharp_utils -IncludeDebugInfo

    # Import any PowerShell modules referenced with '#Requires -Module`
    Import-Module -Name "$($pwd.Path)\powershell\Ansible.ModuleUtils.Legacy.psm1"

    # End of the setup code and start of the module code
    #!powershell

モジュールに必要な場合は ``$complex_args`` にさらに引数を追加したり、
その構造を持つ JSON ファイルでモジュールオプションを定義することもできます。

    {
        "ANSIBLE_MODULE_ARGS": {
            "_ansible_check_mode": false,
            "_ansible_diff": false,
            "path": "C:\\temp",
            "state": "present"
        }
    }

Powershell スクリプトのデバッグに使用できる IDE が複数あり、
以下の 2 つが 最も一般的なものになります。

- `Powershell ISE`_
- `Visual Studio コード`_

.. _Powershell ISE: https://docs.microsoft.com/en-us/powershell/scripting/core-powershell/ise/how-to-debug-scripts-in-windows-powershell-ise
.. _Visual Studio Code: https://blogs.technet.microsoft.com/heyscriptingguy/2017/02/06/debugging-powershell-script-in-visual-studio-code-part-1/

Ansible がモジュールに渡した引数を表示するには、
以下の手順に従います。

- Ansible コマンドの前に :envvar:`ANSIBLE_KEEP_REMOTE_FILES=1<ANSIBLE_KEEP_REMOTE_FILES>` を付けて、Ansible が exec ファイルをサーバ上に保持するように指定します。
- Ansible がモジュールの実行に使用したのと同じユーザーアカウントを使用して Windows サーバーにログインします。
- ``%TEMP%\..`` に移動します。これには、``ansible-tmp-`` で始まるディレクトリーが含まれている必要があります。
- このフォルダー内で、モジュールの PowerShell スクリプトを開きます。
- このスクリプトは、``$json_raw`` にある生の JSON スクリプトで、``module_args`` の下にモジュール引数が含まれています。これらの引数は、デバッグスクリプトで定義される ``$complex_args`` 変数に手動で割り当てたり、``args.json`` ファイルに置いたりできます。


Windows のユニットテスト
====================

現在、Ansible CI で Powershell モジュールのユニットテストを実行するメカニズムはありません。


Windows 統合テスト
===========================

Ansible モジュールの統合テストは、通常、Ansible ロールとして記述されます。これらのテストロールは、
``./test/integration/targets`` にあります。最初にテスト環境を設定し、
Ansible が接続するテストインベントリーを設定する必要があります。

この例では、
2 台のホストに接続して win_stat の統合テストを実行するためのテストインベントリーを設定します。

- コマンド ``source ./hacking/env-setup`` を実行して環境を準備します。
- ``./test/integration/inventory.winrm.template`` のコピーを作成し、``inventory.winrm`` という名前を付けます。
- ``[windows]`` の下にエントリーを入力し、ホストへの接続に必要な変数を設定します。
- WinRM と、設定された認証方法をサポートするのに :ref:`必要な Python モジュールをインストール <windows_winrm>` します。
- 統合テストを実行するには、``ansible-test windows-integration win_stat`` を実行します。``win_stat`` はテストするロールに置き換えることができます。

これにより、そのロールに現在定義されているテストがすべて実行されます。ansible-playbook と同じように、
``-v`` 引数を使用して、
詳細レベルを設定できます。

新しいモジュールのテストを開発する場合、シナリオをチェックモードで 1 回、
チェックモードではない状態で 1 回テストすることが推奨されます。これにより、
チェックモードでは何も変更を加えずに変更を報告し、
2 回目の実行では冪等で変更を報告しないことを保証します。たとえば、以下のようになります。

.. code-block:: yaml

    - name: remove a file (check mode)
      win_file:
        path: C:\temp
        state: absent
      register: remove_file_check
      check_mode: yes

    - name: get result of remove a file (check mode)
      win_command: powershell.exe "if (Test-Path -Path 'C:\temp') { 'true' } else { 'false' }"
      register: remove_file_actual_check

    - name: assert remove a file (check mode)
      assert:
        that:
        - remove_file_check is changed
        - remove_file_actual_check.stdout == 'true\r\n'

    - name: remove a file
      win_file:
        path: C:\temp
        state: absent
      register: remove_file

    - name: get result of remove a file
      win_command: powershell.exe "if (Test-Path -Path 'C:\temp') { 'true' } else { 'false' }"
      register: remove_file_actual

    - name: assert remove a file
      assert:
        that:
        - remove_file is changed
        - remove_file_actual.stdout == 'false\r\n'

    - name: remove a file (idempotent)
      win_file:
        path: C:\temp
        state: absent
      register: remove_file_again

    - name: assert remove a file (idempotent)
      assert:
        that:
        - not remove_file_again is changed


Windows の通信および開発サポート
=============================================

Windows における Ansible 開発に関する説明は、IRC チャンネル ``#ansible-devel`` またはフリーノード ``#ansible-windows`` 
に参加してください。

Ansible 製品の使用に関する質問とディスカッションは、
``#ansible`` チャンネルを使用してください。
