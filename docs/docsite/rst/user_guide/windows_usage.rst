Ansible と Windows の使用
=========================
Ansible を 使用して Windows を管理する場合、
Unix/Linux ホストに適用される構文とルールの多くは Windows にも適用されますが、
パスセパレーターや OS 固有のタスクなどのコンポーネントに関してはいくつか相違点があります。
ここでは、Windows 向けに Ansible を使用する場合の注意点を説明します。

.. contents:: トピック
   :local:

ユースケース
`````````
Ansible は、Windows サーバーにある多数のタスクを調整 (オーケストレート) するのに使用できます。
以下に、一般的なタスクに関するいくつかの例と情報を示します。

ソフトウェアのインストール
-------------------
Ansible を使用してソフトウェアをインストールできる主な方法は 3 つあります。

* ``win_chocolatey`` モジュールを使用する。この場合は、
  公開されているデフォルトの `Chocolatey <https://chocolatey.org/>`_ リポジトリーからプログラムデータを取得します。内部リポジトリーは、
  代わりに、``source`` オプションを設定して使用します。

* ``win_package`` モジュールを使用する。これにより、
  ローカル/ネットワークパスまたは URL から MSI または .exe インストーラーを使用してソフトウェアがインストールされます。

* ``win_command`` モジュールまたは ``win_shell`` モジュールを使用して手動でインストーラーを実行する。

``win_chocolatey`` モジュールは、パッケージがすでにインストールされていて最新かどうかを確認するための最も完全なロジックを備えているため、このモジュールを使用することが推奨されます。

以下は、3 つのすべてのオプションを使用して 7-Zip をインストールするいくつかの例です。

.. code-block:: yaml+jinja

    # Install/uninstall with chocolatey
    - name: Ensure 7-Zip is installed via Chocolatey
      win_chocolatey:
        name: 7zip
        state: present

    - name: Ensure 7-Zip is not installed via Chocolatey
      win_chocolatey:
        name: 7zip
        state: absent

    # Install/uninstall with win_package
    - name: Download the 7-Zip package
      win_get_url:
        url: https://www.7-zip.org/a/7z1701-x64.msi
        dest: C:\temp\7z.msi

    - name: Ensure 7-Zip is installed via win_package
      win_package:
        path: C:\temp\7z.msi
        state: present

    - name: Ensure 7-Zip is not installed via win_package
      win_package:
        path: C:\temp\7z.msi
        state: absent

    # Install/uninstall with win_command
    - name: Download the 7-Zip package
      win_get_url:
        url: https://www.7-zip.org/a/7z1701-x64.msi
        dest: C:\temp\7z.msi

    - name: Check if 7-Zip is already installed
      win_reg_stat:
        name: HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{23170F69-40C1-2702-1701-000001000000}
      register: 7zip_installed

    - name: Ensure 7-Zip is installed via win_command
      win_command: C:\Windows\System32\msiexec.exe /i C:\temp\7z.msi /qn /norestart
      when: 7zip_installed.exists == false

    - name: Ensure 7-Zip is uninstalled via win_command
      win_command: C:\Windows\System32\msiexec.exe /x {23170F69-40C1-2702-1701-000001000000} /qn /norestart
      when: 7zip_installed.exists == true

Microsoft OfficeやSQL Serverなどの一部のインストーラーでは、
認証情報の委譲または WinRM によって制限されたコンポーネントへのアクセスが必要です。これらの問題を回避する最良の方法は、
タスクで ``become`` を使用することです。``become`` を使用すると、
Ansible は、ホスト上でインタラクティブに実行されたかのようにインストーラーを実行します。

.. Note:: 多くのインストーラーは、WinRM 経由でエラー情報を適切に返しません。この場合、インストールがローカルで動作することが確認されている場合は、become を使用することが推奨されます。

.. Note:: 一部のインストーラーは、WinRM または HTTP サービスを再起動したり、一時的に利用できなくなったりするため、システムが到達不能であると Ansible により想定されます。

更新のインストール
------------------
``win_updates`` モジュールおよび ``win_hotfix`` モジュールを使用して、
ホストに更新またはホットフィックスをインストールできます。``win_updates`` モジュールは、カテゴリーごとに複数の更新をインストールするために使用されます。
一方、``win_hotfix`` は、
ローカルにダウンロードされた単一の更新またはホットフィックスファイルをインストールするために使用できます。

.. Note:: ``win_hotfix`` モジュールには、
    DISM PowerShell コマンドレットが存在する必要があります。このようなコマンドレットは、
    Windows Server 2012 以降でのみデフォルトで追加され、古い Windows ホストにインストールする必要があります。

次の例は、``win_updates`` の使用方法を示しています。

.. code-block:: yaml+jinja

    - name: Install all critical and security updates
      win_updates:
        category_names:
        - CriticalUpdates
        - SecurityUpdates
        state: installed
      register: update_result

    - name: Reboot host if required
      win_reboot:
      when: update_result.reboot_required

次の例は、``win_hotfix`` を使用して、
更新またはホットフィックスを 1 つインストールする方法を示しています。

.. code-block:: yaml+jinja

    - name:Download KB3172729 for Server 2012 R2
      win_get_url:
        url: http://download.windowsupdate.com/d/msdownload/update/software/secu/2016/07/windows8.1-kb3172729-x64_e8003822a7ef4705cbb65623b72fd3cec73fe222.msu
        dest:C:\temp\KB3172729.msu

    - name:Install hotfix
      win_hotfix:
        hotfix_kb:KB3172729
        source:C:\temp\KB3172729.msu
        state: present
      register: hotfix_result

    - name:Reboot host if required
      win_reboot:
      when: hotfix_result.reboot_required

ユーザーとグループの設定
-----------------------
Ansible を使用して、ローカルとドメインの両方で Windows ユーザーとグループを作成できます。

ローカル
+++++
``win_user`` モジュール、``win_group`` モジュール、および ``win_group_membership`` モジュールは、
Windows ユーザー、グループ、およびグループメンバーシップをローカルで管理します。

以下は、
同じホスト上のディレクトリーにアクセスできるローカルアカウントとグループを作成する例です。

.. code-block:: yaml+jinja

    - name: Create local group to contain new users
      win_group:
        name: LocalGroup
        description: Allow access to C:\Development folder

    - name: Create local user
      win_user:
        name: '{{ item.name }}'
        password: '{{ item.password }}'
        groups: LocalGroup
        update_password: no
        password_never_expires: yes
      loop:
      - name: User1
        password: Password1
      - name: User2
        password: Password2

    - name: Create Development folder
      win_file:
        path: C:\Development
        state: directory

    - name: Set ACL of Development folder
      win_acl:
        path: C:\Development
        rights: FullControl
        state: present
        type: allow
        user: LocalGroup

    - name: Remove parent inheritance of Development folder
      win_acl_inheritance:
        path: C:\Development
        reorganize: yes
        state: absent
    
ドメイン
++++++
``win_domain_user`` モジュールおよび ``win_domain_group`` モジュールが、
ドメイン内のユーザーとグループを管理します。以下は、
ドメインユーザーのバッチを確実に作成する例です。

.. code-block:: yaml+jinja

    - name: Ensure each account is created
      win_domain_user:
        name: '{{ item.name }}'
        upn: '{{ item.name }}@MY.DOMAIN.COM'
        password: '{{ item.password }}'
        password_never_expires: no
        groups:
        - Test User
        - Application
        company: Ansible
        update_password: on_create
      loop:
      - name: Test User
        password: Password
      - name: Admin User
        password: SuperSecretPass01
      - name: Dev User
        password: '@fvr3IbFBujSRh!3hBg%wgFucD8^x8W5'
    
コマンドの実行
----------------
タスクに利用できる適切なモジュールがない場合、
コマンドまたはスクリプトは、``win_shell`` モジュール、``win_command`` モジュール、``raw`` モジュール、および ``script`` モジュールを使用して実行できます。

``raw`` モジュールは、Powershell コマンドをリモートで実行するだけです。``raw`` には、
Ansible が通常使用するラッパーがないため、``become``、``async``、
および環境変数は機能しません。

``script`` モジュールは、
1 つ以上の Windows ホスト上の Ansible コントローラーからスクリプトを実行します。``raw`` と同様に、``script`` は現在、
``become``、``async``、または環境変数をサポートしていません。

``win_command`` モジュールは、実行ファイルまたはバッチファイルであるコマンドを実行するために使用され、
``win_shell`` モジュールは、シェル内でコマンドを実行するのに使用されます。

コマンドまたはシェルの選択
+++++++++++++++++++++++++
``win_shell`` モジュールおよび ``win_command`` モジュールの両方を使用して、1 つまたは複数のコマンドを実行できます。
``win_shell``モジュールは、``PowerShell`` や ``cmd`` などのシェルのようなプロセス内で実行されるため、
``<``、``>``、``|``、``;``、``&&``、``||`` などのシェル演算子にアクセスできます複数行のコマンドは、``win_shell`` でも実行できます。

``win_command`` モジュールは、シェルの外でプロセスを実行するだけです。シェルコマンドを、
``cmd.exe`` や ``PowerShell.exe`` などのシェル実行ファイルに渡すことで、
``mkdir`` や ``New-Item`` などのシェルコマンドを引き続き実行できます。

以下は、``win_command`` および ``win_shell`` の使用例です。

.. code-block:: yaml+jinja

    - name: Run a command under PowerShell
      win_shell: Get-Service -Name service | Stop-Service

    - name: Run a command under cmd
      win_shell: mkdir C:\temp
      args:
        executable: cmd.exe

    - name: Run a multiple shell commands
      win_shell: |
        New-Item -Path C:\temp -ItemType Directory
        Remove-Item -Path C:\temp -Force -Recurse
        $path_info = Get-Item -Path C:\temp
        $path_info.FullName

    - name: Run an executable using win_command
      win_command: whoami.exe

    - name: Run a cmd command
      win_command: cmd.exe /c mkdir C:\temp

    - name: Run a vbs script
      win_command: cscript.exe script.vbs

.. Note:: ``mkdir``、``del``、``copy`` などの一部のコマンドは、
    CMD シェルにのみ存在します。``win_command`` で実行するには、
    先頭に ``cmd.exe /c`` が付いています。

引数のルール
++++++++++++++
``win_command`` を使用してコマンドを実行する場合は、
標準のWindows 引数ルールが適用されます。

* 各引数は空白で区切られます。
  空白はスペースまたはタブのいずれかです。

* 引数は二重引用符 (``"``) で囲むことができます。これらの引用符内のすべては、
  空白が含まれている場合でも、単一の引数として解釈されます。

* バックスラッシュ ```` が前に付いた二重引用符は、
  単なる二重引用符 ``"`` として解釈され、引数の区切り文字として解釈されません。

* バックスラッシュは、二重引用符の直前にない限り、
  文字どおりに解釈されます (```` == ```` および ``\"`` == ``"`` など)。

* 偶数個のバックスラッシュの後に二重引用符が続く場合は、
  すべてのペアの引数で 1 つのバックスラッシュが使用され、
  二重引用符は引数の文字列区切り文字として使用されます。

* 奇数のバックスラッシュの後に二重引用符が続く場合は、
  各ペアの引数で 1 つのバックスラッシュが使用され、
  二重引用符はエスケープされ、

引数でリテラルの二重引用符が作成されます。

.. code-block:: yaml+jinja

    - win_command: C:\temp\executable.exe argument1 "argument 2" "C:\path\with space" "double \"quoted\""

    argv[0] = C:\temp\executable.exe
    argv[1] = argument1
    argv[2] = argument 2
    argv[3] = C:\path\with space
    argv[4] = double "quoted"

    - win_command: '"C:\Program Files\Program\program.exe" "escaped \\\" backslash" unquoted-end-backslash\'

    argv[0] = C:\Program Files\Program\program.exe
    argv[1] = escaped \" backslash
    argv[2] = unquoted-end-backslash\

    # Due to YAML and Ansible parsing '\"' must be written as '{% raw %}\\{% endraw %}"'
    - win_command: C:\temp\executable.exe C:\no\space\path "arg with end \ before end quote{% raw %}\\{% endraw %}"

    argv[0] = C:\temp\executable.exe
    argv[1] = C:\no\space\path
    argv[2] = arg with end \ before end quote\"
    
詳細は「`escaping arguments <https://msdn.microsoft.com/en-us/library/17w5ykft(v=vs.85).aspx>`\_」を参照してください。

スケジュールされたタスクの作成と実行
-------------------------------------
WinRM には、
特定のコマンドの実行時にエラーを引き起こすいくつかの制限があります。これらの制限を回避する 1 つの方法は、
スケジュールされたタスクを介してコマンドを実行することです。スケジュールされたタスクは、
スケジュールに従って別のアカウントで実行ファイルを実行する機能を提供する Windows コンポーネントです。

Ansible バージョン 2.5 では、Windows でスケジュールされたタスクを簡単に操作できるようにするモジュールが追加されました。
以下は、
実行後に自身を削除するスケジュールされたタスクとしてスクリプトを実行する例です。

.. code-block:: yaml+jinja

    - name: Create scheduled task to run a process
      win_scheduled_task:
        name: adhoc-task
        username: SYSTEM
        actions:
        - path: PowerShell.exe
          arguments: |
            Start-Sleep -Seconds 30  # This isn't required, just here as a demonstration
            New-Item -Path C:\temp\test -ItemType Directory
        # Remove this action if the task shouldn't be deleted on completion
        - path: cmd.exe
          arguments: /c schtasks.exe /Delete /TN "adhoc-task" /F
        triggers:
        - type: registration

    - name: Wait for the scheduled task to complete
      win_scheduled_task_stat:
        name: adhoc-task
      register: task_stat
      until: (task_stat.state is defined and task_stat.state.status != "TASK_STATE_RUNNING") or (task_stat.task_exists == False)
      retries: 12
      delay: 10

.. Note:: 上記の例で使用されているモジュールは、
    Ansible バージョン 2.5 で更新/追加されました。

Windows のパスのフォーマット
```````````````````````````
Windows は、多くの点で従来の POSIX オペレーティングシステムとは異なります。主な変更点の 1 つは、
パス区切り文字としての ``/`` から ```` へのシフトです。```` は POSIX システムでエスケープ文字として使用されることが多いため、
これは、
Playbook の作成方法に大きな問題を引き起こす可能性があります。

Ansible では、2 つの異なるスタイルの構文を使用できます。それぞれ Windows のパスセパレーターの扱いが異なります。

YAML スタイル
----------
タスクに YAML 構文を使用する場合、
ルールは YAML 標準仕様によって明確に定義されます

* 通常の文字列 (引用符なし) を使用する場合、
  YAMLは バックスラッシュをエスケープ文字と見なしません。

* 単一引用符 ``'`` を使用する場合、
  YAML はバックスラッシュをエスケープ文字と見なしません。

* 二重引用符 ``"`` を使用する場合、
  バックスラッシュはエスケープ文字と見なされ、別のバックスラッシュでエスケープする必要があります。

.. Note:: YAML で絶対に必要または要求される場合にのみ文字列を引用し、
    その後は単一引用符を使用する必要があります。

YAML 仕様では、`次のエスケープシーケンス <https://yaml.org/spec/current.html#id2517668>`_ が考慮されます。

* ``\0``, ``\\``, ``\"``, ``\_``, ``\a``, ``\b``, ``\e``, ``\f``, ``\n``, ``\r``, ``\t``,
  ``\v``, ``\L``, ``\N`` and ``\P`` -- 1 文字のエスケープ

* ``<TAB>``, ``<SPACE>``, ``<NBSP>``, ``<LNSP>``, ``<PSP>`` -- 特殊文字

* ``\x..`` -- 2 桁の 16 進エスケープ

* ``\u....`` -- 4 桁の 16 進エスケープ

* ``\U........`` -- 8 桁の 16 進エスケープ

Windows パスの記述方法の例を次に示します。

    # GOOD
    tempdir: C:\Windows\Temp

    # WORKS
    tempdir: 'C:\Windows\Temp'
    tempdir: "C:\\Windows\\Temp"

    # BAD, BUT SOMETIMES WORKS
    tempdir: C:\\Windows\\Temp
    tempdir: 'C:\\Windows\\Temp'
    tempdir: C:/Windows/Temp

これは失敗する例です。

.. code-block:: text

    # FAILS
    tempdir: "C:\Windows\Temp"

この例は、必要な場合の単一引用符の使用を示しています。

    ---
    - name:Copy tomcat config
      win_copy:
        src: log4j.xml
        dest: '{{tc_home}}\lib\log4j.xml'

従来の key=value スタイル
----------------------
従来の ``key=value`` 構文は、
アドホックコマンドのコマンドライン、または Playbook 内で使用されます。バックスラッシュ文字をエスケープする必要があるため、
Playbook でこのスタイルを使用することは推奨されません。Playbook が読みにくくなります。
従来の構文は、Ansible の特定の実装に依存し、
引用符 (単一と二重の両方) は、
Ansible による解析方法に影響を与えません。

Ansible の key=value パーサー parse\_kv() は、
次のエスケープシーケンスを考慮します。

* ``\``, ``'``, ``"``, ``\a``, ``\b``, ``\f``, ``\n``, ``\r``, ``\t``、および 
  ``\v`` -- 1 文字のエスケープ

* ``\x..`` -- 2 桁の 16 進エスケープ

* ``\u....`` -- 4 桁の 16 進エスケープ

* ``\U........`` -- 8 桁の 16 進エスケープ

* ``\N{...}`` -- 名前による Unicode 文字

これは、バックスラッシュが一部のシーケンスのエスケープ文字であることを意味します。
通常、この形式ではバックスラッシュをエスケープする方が安全です。

key=value スタイルで Windows パスを使用する例を次に示します。

.. code-block:: ini

    # GOOD
    tempdir=C:\\Windows\\Temp

    # WORKS
    tempdir='C:\\Windows\\Temp'
    tempdir="C:\\Windows\\Temp"

    # BAD, BUT SOMETIMES WORKS
    tempdir=C:\Windows\Temp
    tempdir='C:\Windows\Temp'
    tempdir="C:\Windows\Temp"
    tempdir=C:/Windows/Temp

    # FAILS
    tempdir=C:\Windows\temp
    tempdir='C:\Windows\temp'
    tempdir="C:\Windows\temp"

失敗した例は完全には失敗していませんが、``\t`` を 
``<TAB>`` を文字で置き換えます。その結果、``tempdir`` が、``C:\Windows<TAB>emp`` になります。

制限事項
```````````
ここでは、Ansible と Windows でできないことを説明します。

* PowerShell のアップグレード

* WinRM リスナーとの対話

WinRM は通常の対話中にオンラインで実行されているサービスに依存しているため、PowerShell をアップグレードしたり、Ansible で WinRM リスナーと対話することはできません。このアクションにより、接続が失敗します。これは技術的には ``async`` またはスケジュールされたタスクを使用することで回避できますが、そのようなメソッドは、実行するプロセスがAnsible が使用する基本的な接続を中断する場合は脆弱であり、
ブートストラッププロセスまたはイメージが作成される前に残されるのが最適です。

Windows モジュールの開発
``````````````````````````
Windows 用の Ansible モジュールは PowerShell で記述されているため、
Windows モジュールの開発ガイドは、標準の標準モジュールの開発ガイドとは大きく異なります。詳細は、
「:ref:`developing_modules_general_windows`」参照してください。

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
