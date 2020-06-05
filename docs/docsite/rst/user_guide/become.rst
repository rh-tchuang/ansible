.. _become:

******************************************
権限昇格の理解: become
******************************************

Ansible は既存の権限昇格システムを使用して、root 権限または別のユーザーのパーミッションでタスクを実行します。この機能を使用すると、このマシンにログインしたユーザー (リモートユーザー) とは別のユーザー「になる (become)」ことができるため、この機能は ``become`` と呼ばれています。``become`` キーワードは、`sudo`、`su`、`pfexec`、`doas`、`pbrun`、`dzdo`、`ksu`、`runas`、`machinectl` などの既存の権限昇格ツールを利用します。

.. contents::
   :local:

become の使用
============

play ディレクティブまたは task ディレクティブ、接続変数、またはコマンドラインでの ``become`` の使用を制御できます。複数の方法で権限昇格プロパティーを設定する場合は、:ref:`一般的な優先順位ルール<general_precedence_rules>` を確認し、使用する設定を確認します。

Ansible に含まれる全 become プラグインの完全リストは、:ref:`become_plugin_list` にあります。

Become ディレクティブ
-----------------

play レベルまたは task レベルで ``become`` を制御するディレクティブを設定できます。接続変数を別のホストに設定すると、その変数を上書きできます。これは多くの場合は、ホスト間で異なります。これらの変数とディレクティブは独立しています。たとえば、``become_user`` を設定すると ``become`` に設定されません。

become
    権限昇格をアクティブにするには、``yes`` に設定します。

become_user
    希望する権限を持つユーザーに設定します。ログインしたユーザーではなく、`become` を行ったユーザーになります。ホストレベルで設定できる ``become: yes`` を意味しているわけではありません。デフォルト値は ``root`` です。

become_method
    (play レベルまたは task レベルで)、ansible.cfg に設定されたデフォルトのメソッドをオーバーライドし、:ref:`become_plugins` を使用するよう設定します。

become_flags
    (play レベルまたは task レベルで) を使用すると、タスクまたはロールに特定のフラグを使用できます。シェルに no login を設定する場合は、ユーザーを nobody に変更するのが一般的な方法です。Ansible 2.2 で追加されました。

たとえば、``root`` 以外のユーザーとして接続する際にシステムサービスを管理する (``root`` 権限が必要) には、``become_user`` (``root``) のデフォルト値を使用できます。

.. code-block:: yaml

    - name: Ensure the httpd service is running
      service:
        name: httpd
        state: started
      become: yes

``apache`` ユーザーとしてコマンドを実行するには、次を実行します。

.. code-block:: yaml

    - name:Run a command as the apache user
      command: somecommand
      become: yes
      become_user: apache

シェルが nologin の場合に ``nobody`` ユーザーとして何かを行うには、次を実行します。

.. code-block:: yaml

    - name:Run a command as nobody
      command: somecommand
      become: yes
      become_method: su
      become_user: nobody
      become_flags: '-s /bin/sh'

Become 接続変数
---------------------------

管理対象ノードまたはグループごとに異なる ``become`` オプションを定義できます。これらの変数はインベントリーで定義するか、通常の変数として使用できます。

ansible_become
    become ディレクティブと同等です。権限のエスカレーションが使用されるかどうかを指定します。

ansible_become_method
    使用する権限昇格方法

ansible_become_user
    権限昇格で become を行うユーザーを設定します。``ansible_become: yes`` を意味するものではありません。

ansible_become_password
    権限昇格パスワードを設定します。平文での秘密の使用を回避する方法は、「:ref:`playbooks_vault`」を参照してください。

たとえば、すべてのタスクを ``webserver`` という名前のサーバーで ``root`` として実行することを望んでいて、``manager`` ユーザーとしてのみ接続できる場合は、以下のようなインベントリーエントリーを使用できます。

.. code-block:: text

    webserver ansible_user=manager ansible_become=yes

.. note::
    上記の変数は全 become プラグインに汎用的なものですが、プラグイン固有の変数を設定することもできます。
    そのプラグインが持つすべてのオプションとその定義方法の一覧は、各プラグインのドキュメントを参照してください。
    Ansible の become プラグインの完全リストは、:ref:`become_plugins` にあります。

Become コマンドラインオプション
---------------------------

--ask-become-pass, -K
    権限昇格パスワードを要求します。これは必ずしも使用されることは限りません。このパスワードはすべてのホストで使用されることに注意してください。

--become, -b
    become で操作を実行します (パスワードないことを示しています)

--become-method=BECOME_METHOD
    使用する権限昇格方法 (default=sudo) です。
    有効な選択肢は、[ sudo | su | pbrun | pfexec | doas | dzdo | ksu | runas | machinectl ] です。

--become-user=BECOME_USER
    このユーザー (デフォルトは root) として操作を実行します。--become/-b を意味するものではありません。

become のリスクと制限
===============================

特権の昇格はほとんど直感的ですが、それがどのように機能するかについては、
いくつかの制限があります。 問題が発生しないように、これらの点に注意する必要があります。

非特権ユーザーになるリスク
--------------------------------------

Ansible モジュールは、
最初にパラメーターをモジュールファイルに入力し、そのファイルをリモートマシンにコピーします。
そして最後にそこで実行します。

``become`` を使用せずにモジュールファイルが実行しているかどうか、
``become_user`` が root の場合、またはリモートマシンへの接続が root として作成された場合は、
何も問題がありません。 この場合、Ansible は、
ユーザーと root による読み取りのみを許可するパーミッション、
または切り替えられる非特権ユーザーによる読み取りのみを許可するパーミッションでモジュールファイルを作成します。

ただし、接続ユーザーと ``become_user`` の両方に権限がない場合、
モジュールファイルは Ansible が接続するユーザーとして書き込まれますが、
ファイルは Ansible が ``become`` に設定したユーザーが読み取り可能である必要があります。この場合、Ansible は、
Ansible モジュールの実行中に、モジュールファイルを誰でも読み取り可能にします。
モジュールの実行が完了すると、Ansible は一時ファイルを削除します。

モジュールに渡されるパラメーターのいずれかが本質的に機密であり、
クライアントマシンを信頼していない場合、これは潜在的な危険です。

この問題を解決する方法には、以下が含まれます。

* `パイプライン` を使用します。 パイプラインが有効な場合、
  Ansible はクライアント上の一時ファイルにモジュールを保存しません。 代わりに、
  モジュールをリモートの python インタープリターの stdin にパイプします。パイプライン処理は、
  ファイル転送を伴う python モジュール (たとえば、:ref:`copy <copy_module>`、
  :ref:`fetch <fetch_module>`、:ref:`template <template_module>`)、または非 python モジュールでは機能しません。

* 管理対象ホストに、
  POSIX.1e ファイルシステムの acl サポートをインストールします。 リモートホスト上の一時ディレクトリーが POSIX acl を有効にしてマウントされ、
  :command:`setfacl` ツールがリモートの ``PATH`` にある場合、
  Ansible は POSIX acl を使用して、誰もがファイルを読み取れるようにする代わりに、
  2 番目の非特権ユーザーとモジュールファイルを共有します。

* 非特権ユーザーには
  ならないようにしてください。 一時ファイルは、
  root になる (``become``) か、``become`` を使用しない場合は、UNIX ファイルのパーミッションにより保護されます。 Ansible 2.1 以降では、
  管理対象マシンに root として接続してから、
  非特権アカウントにアクセスするために ``become`` を使用する場合でも、UNIXファイルの権限は安全です。

.. warning:: Solaris ZFS ファイルシステムにはファイルシステム ACL がありますが、
    ACL は POSIX.1e ファイルシステムの acl ではありません (代わりに NFSv4 ACL になります)。 Ansible はこれらの ACL を使用して一時ファイルのパーミッションを管理できないため、
    リモートマシンが ZFS を使用している場合は、
    ``allow_world_readable_tmpfiles`` を使用する必要があります。

バージョン 2.1 における新機能

Ansible は、知らないうちに、保護されずに ``become`` を使用することが簡単にできないようにします。Ansible 2.1 以降、
Ansible は、``become`` で安全に実行できない場合は、デフォルトでエラーを発生します。
パイプラインまたは POSIX ACL を使用できない場合は、特権のないユーザーとして接続する必要があります。
別の非特権ユーザーとして実行するには、``become`` を使用する必要があり、
管理対象ノードが、
そこで実行するモジュールが誰でも読み取り可能であるように十分に安全であると判断した場合は、
:file:`ansible.cfg` ファイルで ``allow_world_readable_tmpfiles`` をオンにできます。 ``allow_world_readable_tmpfiles`` を設定すると、
これがエラーから警告に変わり、
タスクが 2.1 以前のように実行されるようになります。

すべての接続プラグインでサポートされない
---------------------------------------

使用する接続プラグインでは、
権限昇格方法もサポートする必要があります。ほとんどの接続プラグインは、become をサポートしない場合は警告されます。常に root (jail、chroot など) として実行されるため、
これを無視する人もいます。

ホストごとに有効にできる方法は 1 つだけ
---------------------------------------

メソッドは連鎖できません。``sudo /bin/su -`` を使用してユーザーになる (become) ことはできません。
そのユーザーになるには、sudo でそのユーザーとしてコマンドを実行するか、
直接そのユーザーに su を実行するための権限が必要です (pbrun、pfexec、またはその他のサポートされている方法でも同じです)。

特権昇格は一般的なものにすること
------------------------------------

特権昇格パーミッションを特定のコマンドに制限できません。
Ansible は、
常に特定のコマンドを使用して何かを行うわけではありませんが、
毎回変更される一時ファイル名からモジュール (コード) を実行します。 許可されたコマンドとして「/sbin/service」または「/bin/chmod」がある場合は、
Ansible で、
モジュールを実行するために作成する一時ファイルとそのパスが一致しないため、
Ansible で失敗します。sudo/pbrun/doas 環境を特定のコマンドパスのみを実行するように制約するセキュリティールールがある場合は、
この制約のない特別なアカウントから Ansible を使用するか、
:ref:`ansible_tower` を使用して SSH 認証情報への間接アクセスを管理します。

pamd_systemd が設定する環境変数にアクセスできない場合
--------------------------------------------------------------

``systemd`` を init として使用するほとんどの Linux ディストリビューションでは、
systemd の意味で、``become`` が使用するデフォルトのメソッドは、
新しい「セッション」を開きません。``pam_systemd`` モジュールは新規セッションを完全に初期化しないため、
ssh を介して開かれた通常のセッションと比較すると驚くかもしれません。
``pam_systemd`` が設定する環境変数、
特に ``xdg_RUNTIME_DIR`` は、新しいユーザー用に設定されず、
継承されるか空になります。

``XDG_RUNTIME_DIR`` に依存する systemd コマンドを呼び出してバスにアクセスしようとすると、
問題が発生する可能性があります。

.. code-block:: console

   $ echo $XDG_RUNTIME_DIR

   $ systemctl --user status
   Failed to connect to bus: Permission denied

``pam_systemd`` を経由する新規 systemd セッションを開くように ``become`` 強制するには、
``become_method: machinectl`` を使用できます。

詳細は、「`この systemd の問題
<https://github.com/systemd/systemd/issues/825#issuecomment-127917622>`_」を参照してください。

.. _become_network:

become およびネットワーク自動化
=============================

バージョン 2.6 では、Ansible は、``enable`` モードに対応するすべての :ref:`Ansible 管理プラットフォーム <network_supported>` で、特権昇格に対して ``become`` をサポートします (``enable`` モードまたは特権が付いた EXEC モードに入ります)。``become`` を使用すると、``provider`` ディクショナリーの ``authorize`` オプションおよび ``auth_pass`` オプションが置き換えられます。

接続の種類を ``connection: network_cli`` または ``connection: httpapi`` のいずれかに設定し、ネットワークデバイスの権限昇格に ``become`` を使用する必要があります。詳細は、:ref:`platform_options` および :ref:`network_modules` のドキュメントを参照してください。

昇格した権限は、それを必要とする特定のタスクのみ、またはプレイ全体でのみ、またはすべてのプレイで使用することができます。``become: yes`` および ``become_method: enable`` は、パラメーターが設定されるタスク、プレイ、または Playbook を実行する前に Ansible に ``enable`` モードに入るように指示します。

このエラーメッセージが表示される場合は、エラーメッセージを生成したタスクを成功させるには、``enable`` モードが必要があります。

.. code-block:: console

   Invalid input (privileged mode required)

特定のタスクに ``enable`` モードを設定するには、タスクレベルで ``become`` を追加します。

.. code-block:: yaml

   - name: Gather facts (eos)
     eos_facts:
       gather_subset:
         - "!hardware"
     become: yes
     become_method: enable

1 つのプレイのすべてのタスクに enable モードを設定するには、プレイレベルに ``become`` を追加します。

.. code-block:: yaml

   - hosts: eos-switches
     become: yes
     become_method: enable
     tasks:
       - name: Gather facts (eos)
         eos_facts:
           gather_subset:
             - "!hardware"

すべてのタスクに enable モードの設定
---------------------------------

多くの場合は、すべてのプレイのすべてのタスクで特権モードを使用したいと考えることがあります。これには、``group_vars`` を使用することが最適です。

**group_vars/eos.yml**

.. code-block:: yaml

   ansible_connection: network_cli
   ansible_network_os: eos
   ansible_user: myuser
   ansible_become: yes
   ansible_become_method: enable

enable モードのパスワード
^^^^^^^^^^^^^^^^^^^^^^^^^

``enable`` モードに入るパスワードが必要な場合は、以下のいずれかの方法で指定できます。

* :option:`--ask-become-pass <ansible-playbook --ask-become-pass>` コマンドラインオプションの指定
* ``ansible_become_password`` 接続変数の設定

.. warning::

   通知パスワードは平文で保存しないでください。Ansible Vault でパスワードやその他の秘密を暗号化する方法は、「:ref:`vault`」を参照してください。

authorize および auth_pass
-----------------------

Ansible は、引き続き ``connection: local`` (従来のネットワーク Playbook 用) による ``enable`` モードをサポートします。``connection: local`` で ``enable`` モードにするには、モジュールオプション ``authorize`` および ``auth_pass`` を使用します。

.. code-block:: yaml

   - hosts: eos-switches
     ansible_connection: local
     tasks:
       - name: Gather facts (eos)
         eos_facts:
           gather_subset:
             - "!hardware"
         provider:
           authorize: yes
           auth_pass: " {{ secret_auth_pass }}"

ネットワークデバイスの ``enable`` モードで一貫して ``become`` するように Playbook を更新することが推奨されます。``authorize`` ディクショナリーおよび ``provider`` ディクショナリーの使用は今後非推奨になります。詳細は、:ref:`platform_options` および :ref:`network_modules` のドキュメントを参照してください。

.. _become_windows:

Become および Windows
==================

Ansible 2.3 以降、
``become`` を使用して、``runas`` メソッドを Windows ホスト上で使用できるようになります。Windows の Become は、
Windows 以外のホストと同じインベントリーセットアップと呼び出し引数を ``become`` として使用するため、
セットアップ名と変数名は、このドキュメントで定義されているものと同じです。

``become`` は、別のユーザー ID の役割を担うために使用できますが、
Windows ホストでは他にも利用方法があります。重要な用途の 1 つは、
WinRM での実行時に課せられる制限の一部を回避します 
(ネットワーク委譲や、WUA API などの禁止システムコールへのアクセスなど)。``become`` を使用して ``ansible_user`` と同じユーザーになると、
これらの制限を回避し、
WinRM セッションでは通常アクセスできないコマンドを実行できます。

管理者権限
---------------------

Windows の多くのタスクを完了するには、管理者権限が必要です。``runas`` になるメソッドを使用すると、
Ansibleは、
リモートユーザーが使用できるすべての権限でモジュールを実行しようとします。ユーザートークンの昇格に失敗すると、
実行中に制限されたトークンを使用し続けます。

昇格された特権で become プロセスを実行するには、
ユーザーに ``SeDebugPrivilege`` が必要です。この権限は、デフォルトで管理者に割り当てられます。デバッグ特権が使用できない場合、
become プロセスは、
限られた特権とグループのセットで実行します。

Ansible が取得できたトークンのタイプを判別するには、
次のタスクを実行します。

.. code-block:: yaml

    - win_whoami:
      become: yes

出力は以下のようになります。

.. code-block:: ansible-output

    ok: [windows] => {
        "account": {
            "account_name": "vagrant-domain",
            "domain_name": "DOMAIN",
            "sid": "S-1-5-21-3088887838-4058132883-1884671576-1105",
            "type": "User"
        },
        "authentication_package": "Kerberos",
        "changed": false,
        "dns_domain_name": "DOMAIN.LOCAL",
        "groups": [
            {
                "account_name": "Administrators",
                "attributes": [
                    "Mandatory",
                    "Enabled by default",
                    "Enabled",
                    "Owner"
                ],
                "domain_name": "BUILTIN",
                "sid": "S-1-5-32-544",
                "type": "Alias"
            },
            {
                "account_name": "INTERACTIVE",
                "attributes": [
                    "Mandatory",
                    "Enabled by default",
                    "Enabled"
                ],
                "domain_name": "NT AUTHORITY",
                "sid": "S-1-5-4",
                "type": "WellKnownGroup"
            },
        ],
        "impersonation_level": "SecurityAnonymous",
        "label": {
            "account_name": "High Mandatory Level",
            "domain_name": "Mandatory Label",
            "sid": "S-1-16-12288",
            "type": "Label"
        },
        "login_domain": "DOMAIN",
        "login_time": "2018-11-18T20:35:01.9696884+00:00",
        "logon_id": 114196830,
        "logon_server": "DC01",
        "logon_type": "Interactive",
        "privileges": {
            "SeBackupPrivilege": "disabled",
            "SeChangeNotifyPrivilege": "enabled-by-default",
            "SeCreateGlobalPrivilege": "enabled-by-default",
            "SeCreatePagefilePrivilege": "disabled",
            "SeCreateSymbolicLinkPrivilege": "disabled",
            "SeDebugPrivilege": "enabled",
            "SeDelegateSessionUserImpersonatePrivilege": "disabled",
            "SeImpersonatePrivilege": "enabled-by-default",
            "SeIncreaseBasePriorityPrivilege": "disabled",
            "SeIncreaseQuotaPrivilege": "disabled",
            "SeIncreaseWorkingSetPrivilege": "disabled",
            "SeLoadDriverPrivilege": "disabled",
            "SeManageVolumePrivilege": "disabled",
            "SeProfileSingleProcessPrivilege": "disabled",
            "SeRemoteShutdownPrivilege": "disabled",
            "SeRestorePrivilege": "disabled",
            "SeSecurityPrivilege": "disabled",
            "SeShutdownPrivilege": "disabled",
            "SeSystemEnvironmentPrivilege": "disabled",
            "SeSystemProfilePrivilege": "disabled",
            "SeSystemtimePrivilege": "disabled",
            "SeTakeOwnershipPrivilege": "disabled",
            "SeTimeZonePrivilege": "disabled",
            "SeUndockPrivilege": "disabled"
        },
        "rights": [
            "SeNetworkLogonRight",
            "SeBatchLogonRight",
            "SeInteractiveLogonRight",
            "SeRemoteInteractiveLogonRight"
        ],
        "token_type": "TokenPrimary",
        "upn": "vagrant-domain@DOMAIN.LOCAL",
        "user_flags": []
    }
    
``label`` キーの下の ``account_name`` エントリーは、
ユーザーに管理者権限があるかどうかを決定します。返されるラベルと、
そのラベルが表すものは次のとおりです。

* ``Medium``: Ansible は、昇格したトークンの取得に失敗し、
  限られたトークンで実行されました。ユーザーに割り当てられた特権のサブセットのみがモジュールの実行中に利用可能であり、
  ユーザーには管理者権限がありません。

* ``High``: 昇格されたトークンが使用され、
  ユーザーに割り当てられたすべての特権は、モジュールの実行時に利用できます。

* ``System``: ``NT AUTHORITY\System`` アカウントが使用され、
  権限レベルは、利用可能な中で最も高いものになります。

出力には、
ユーザーに付与されている特権のリストも表示されます。特権の値が ``無効`` になっている場合、
特権はログオントークンに割り当てられますが、有効になっていません。ほとんどのシナリオでは、
これらの特権は必要なときに自動的に有効になります。

2.5 よりも古いバージョンの Ansible で実行するか、
通常の ``runas`` 昇格プロセスが失敗した場合、昇格したトークンは次の方法で取得できます。

* オペレーティングシステムを完全に制御できる ``System`` に 
  ``become_user`` を設定します。

* WinRM で、
  Ansible が接続するユーザーに ``SeTcbPrivilege`` を付与します。``SeTcbPrivilege`` は、
  オペレーティングシステムの完全な制御を許可する高レベルの特権です。デフォルトでは、この特権はユーザーに付与されません。
  この特権をユーザーまたはグループに付与する場合は注意が必要です。
  この特権の詳細は、
  「`Act as part of the operating system <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/dn221957(v=ws.11)>`_」を参照してください。
  以下のタスクを使用して、Windows ホストでこの権限を設定できます。

  .. code-block:: yaml

    - name: grant the ansible user the SeTcbPrivilege right
      win_user_right:
        name: SeTcbPrivilege
        users: '{{ansible_user}}'
        action: add

* ユーザーになる前に、ホストで UAC をオフにし、再起動します。UAC は、
  ``最小特権`` の原則で、
  アカウントを実行するように設計されたセキュリティープロトコルです。以下のタスクを実行して、
  UAC をオフにできます。

  .. code-block:: yaml

    - name: turn UAC off
      win_regedit:
        path: HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\policies\system
        name: EnableLUA
        data: 0
        type: dword
        state: present
      register: uac_result

    - name: reboot after disabling UAC
      win_reboot:
      when: uac_result is changed

.. Note:: ``SeTcbPrivilege`` を付与するか UAC をオフにすると、
    Windows のセキュリティーの脆弱性が発生する可能性があるため、これらの手順を実行する場合は注意が必要です。

ローカルサービスアカウント
----------------------

Ansible バージョン 2.5 より前のバージョンでは、``become`` は、
ローカルまたはドメインのユーザーアカウントを持つ Windows でのみ有効でした。これらの古いバージョンでは、``System`` や ``NetworkService`` などのローカルサービスアカウントは、
``become_user`` として使用できませんでした。この制限は、
Ansible の 2.5 リリース以降、この制限は解除されました。``become_user`` 
で設定できる 3 つのサービスアカウントは次のとおりです。

* System
* NetworkService
* LocalService

ローカルサービスアカウントにはパスワードがないため、
``ansible_become_password`` パラメーターは必要ありません。指定しても無視されます。


パスワードを設定しない Become
---------------------------------

Ansible 2.8 以降、Windows のローカルアカウントまたはドメインアカウントになるために、
``become`` が使用できるようになりました。この方法が機能するには、
次の要件を満たす必要があります。

* 接続ユーザーには ``SeDebugPrivilege`` 権限が割り当てられている
* 接続ユーザーは ``BUILTIN\Administrators`` グループに属している
* ``become_user`` に ユーザー権限 ``SeBatchLogonRight`` または ``SeNetworkLogonRight`` がある

パスワードなしの become の使用は、2 つの方法のいずれかで可能です。

* アカウントがすでにログオンしている場合は、既存のログオンセッションのトークンを複製する
* S4U を使用してリモートホストでのみ有効なログイントークンを生成する

最初のシナリオでは、
become プロセスはその別のログオンから生成されます。これは、既存の RDP ログオン、コンソールログオンの場合がありますが、
常に発生するとは限りません。これは、スケジュールされたタスクの 
``Run only when user is logged on`` オプションに似ています。

become アカウントの別のログオンが存在しない場合は、
S4U を使用して新しいログオンを作成し、それを介してモジュールを実行します。これは、スケジュールされたタスクの、``Do not store password`` オプションを使用して、
``ユーザーがログオンしているかどうかにかかわらず実行する`` 
のと似ています。このシナリオでは、
become プロセスは通常の WinRM プロセスのようなネットワークリソースにアクセスできません。

パスワードなしで become を使用することと、パスワードがないアカウントになる (become) ことを区別するには、
``ansible_become_password`` を未定義のままにするか、
``ansible_become_password:`` を定義します。

.. Note:: Ansible の実行時に既存のトークンがユーザーに対して存在するという保証はないため、
  become プロセスが、
  ローカルリソースにのみアクセスできるようになるという大きな変化があります。タスクがネットワークリソースにアクセスする必要がある場合は、
  パスワード付きの become になります。

パスワードのないアカウント
---------------------------

.. Warning:: セキュリティーに関する一般的なベストプラクティスとして、パスワードのないアカウントを許可しないでください。

Ansible を使用して、
パスワードのない Windowsアカウント (``Guest`` アカウントなど) になる (become) ことができます。パスワードなしのアカウントになるには、
通常どおり変数を設定しますが、``ansible_become_password: "`` を設定します。

このようなアカウントで become を有効にする前に、ローカルポリシー 
`Accounts:Limit local account use of blank passwords to console logon only <https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/jj852174(v=ws.11)>`_ 
を無効にする必要があります。これは、
Group Policy Object (GPO) を介して、またはこの Ansible タスクを使用して実行できます。

.. code-block:: yaml

   - name: allow blank password on become
     win_regedit:
       path: HKLM:\SYSTEM\CurrentControlSet\Control\Lsa
       name: LimitBlankPasswordUse
       data: 0
       type: dword
       state: present

.. Note:: これは、パスワードのないアカウント用に限定されます。ただし、
    become_user にパスワードがある場合は、
    ``ansible_become_password`` でアカウントのパスワードを設定する必要があります。

Windows での Become フラグ
------------------------

Ansible 2.5 では、``become_flags`` パラメーターが ``runas`` の become メソッドに追加されています。
このパラメーターは、``become_flags`` タスクディレクティブを使用して設定するか、
``ansible_become_flags`` を使用して Ansible の構成で設定できます。このパラメーターで最初にサポートされる 2 つの有効な値は、
``logon_type`` および 
``logon_flags`` です。

.. Note:: これらのフラグは、LocalSystem などのローカルサービスアカウントではなく、通常のユーザーアカウントになる (become) 場合にのみ設定する必要があります。

``logon_type`` キーは、実行するログオン操作のタイプを設定します。値は、
次のいずれかに設定できます。

* ``interactive``: デフォルトのログオンタイプ。プロセスは、
  プロセスをローカルで実行する場合と同じコンテキストで実行されます。これは、
  すべての WinRM 制限を回避するため、推奨される使用方法です。

* ``batch``: パスワードが設定されたスケジュール済みタスクに似たバッチコンテキストで
  プロセスを実行します。これは、ほとんどの WinRM 制限を回避する必要があり、
  ``become_user`` 
  が対話的にログオンすることを許可されていない場合に役立ちます。

* ``new_credentials``: 呼び出し元ユーザーと同じ認証情報で実行しますが、
  送信接続は、``become_user`` と ``become_password`` のコンテキストで実行され、
  ``runas.exe /netonly`` に似ています。``logon_flags`` フラグも、
  ``netcredentials_only`` に設定できるようにする必要があります。プロセスが、
  別の認証情報セットを使用してネットワークリソース (SMB 共有など) にアクセスする必要がある場合は、
  このフラグを使用します。

* ``network``: キャッシュされた認証情報なしで、
  ネットワークコンテキストでプロセスを実行します。これにより、
  認証情報の委譲なしで通常の WinRM プロセスを実行するのと同じ種類のログオンセッションが行われ、
  同じ制限の下で動作します。

* ``network_cleartext``: ``network`` ログオンタイプと同様ですが、
  代わりに認証情報をキャッシュして、ネットワークリソースにアクセスできるようにします。これは、
  認証情報の委譲を使用して通常の WinRM プロセスを実行するのと同じ種類のログオンセッションです。

詳細情報は、
「`dwLogonType <https://docs.microsoft.com/en-gb/windows/desktop/api/winbase/nf-winbase-logonusera>`_」を参照してください。

``logon_flags`` キーは、
新しいプロセスの作成時に Windows がユーザーのログを記録する方法を指定します。値は、以下の複数の値、またはゼロを設定できます。

* ``with_profile``: 設定されているデフォルトのログオンフラグ。プロセスは、
  ``HKEY_USERS`` レジストリキーのユーザーのプロファイルを、``HKEY_CURRENT_USER`` に読み込みます。

* ``netcredentials_only``: プロセスは、呼び出し元と同じトークンを使用しますが、
  リモートリソースにアクセスするときは、
  ``become_user`` および ``become_password`` します。これは、信頼関係がないドメイン間シナリオで役に立ち、
  ``new_credentials`` ``logon_type`` とともに使用する必要があります。

デフォルトでは、``logon_flags=with_profile`` が設定されています。
プロファイルを読み込まない場合は ``logon_flags=`` を設定します。
プロファイルを ``netcredentials_only`` で読み込む必要がある場合は、``logon_flags=with_profile,netcredentials_only`` を設定します。

詳細は、「`dwLogonFlags <https://docs.microsoft.com/en-gb/windows/desktop/api/winbase/nf-winbase-createprocesswithtokenw>`_」を参照してください。

Windows タスクで ``become_flags`` を使用する例を以下に示します。

.. code-block:: yaml

  - name: copy a file from a fileshare with custom credentials
    win_copy:
      src: \\server\share\data\file.txt
      dest: C:\temp\file.txt
      remote_src: yes
    vars:
      ansible_become: yes
      ansible_become_method: runas
      ansible_become_user: DOMAIN\user
      ansible_become_password: Password01
      ansible_become_flags: logon_type=new_credentials logon_flags=netcredentials_only

  - name: run a command under a batch logon
    win_whoami:
    become: yes
    become_flags: logon_type=batch

  - name: run a command and not load the user profile
    win_whomai:
    become: yes
    become_flags: logon_flags=


Windows における become 制限
--------------------------------

* Windows Server 2008、2008 R2、および Windows 7 で、``async`` および ``become`` でタスクを実行できるのは、
  Ansible 2.7 以降を使用している場合のみです。

* デフォルトでは、become ユーザーは対話型セッションでログオンするため、
  Windows ホストでログオンする権利が必要です。``SeAllowLogOnLocally`` 特権を継承しない場合、
  または ``SeDenyLogOnLocally`` 特権を継承する場合は、
  become プロセスでは失敗します。特権を追加するか、``logon_type`` フラグを設定して、
  使用するログオンタイプを変更します。

* Ansible バージョン 2.3 よりも前のバージョンでは、
  ``ansible_winrm_transport`` は ``basic`` または ``credssp`` のいずれかでした。この制限は、
  Ansible 2.4 リリース以降、すべてのホストで解除されました。
  ただし、Windows Server 2008 (R2 バージョン以外) を除きます。

* ``ansible_become_method: runas`` を使用するために、セカンダリーログオンサービス ``seclogon`` が実行する必要があります。

.. seealso::

   `メーリングリスト <https://groups.google.com/forum/#!forum/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `webchat.freenode.net <https://webchat.freenode.net>`_
       #ansible IRC chat channel
