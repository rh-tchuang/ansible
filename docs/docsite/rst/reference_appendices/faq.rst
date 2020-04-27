.. _ansible_faq:

よくある質問 (FAQ)
==========================

以下に、よくある質問とその回答を紹介しています。


.. _set_environment:

タスクや Playbook 全体に PATH または他の環境変数をどのように設定すればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

環境変数を設定するには、`environment` キーワードを使用します。environment キーワードは、プレイ内のタスクや他のレベルで使用できます。

    environment:
      PATH: "{{ ansible_env.PATH }}:/thingy/bin"
      SOME: value

.. note:: 2.0.1 以降で、gather_facts の設定タスクは、プレイからの環境ディレクティブも継承します。これがプレイレベルで設定されている場合には、`|default` フィルターを使用したエラーの回避が必要になる場合があります。

.. _faq_setting_users_and_ports:

異なるユーザーアカウントまたはポートでログインする必要のある各種マシンをどのように処理すればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

インベントリーファイルにインベントリー変数を設定する方法が最も簡単です。

たとえば、以下では、ホストに異なるユーザー名とポートが指定されています。

.. code-block:: ini

    [webservers]
    asdf.example.com  ansible_port=5000   ansible_user=alice
    jkl.example.com   ansible_port=5001   ansible_user=bob

任意で、使用する接続タイプを指定できます。

.. code-block:: ini

    [testcluster]
    localhost           ansible_connection=local
    /path/to/chroot1    ansible_connection=chroot
    foo.example.com     ansible_connection=paramiko

上記の値をグループ変数や、group_vars/<groupname> ファイルに格納できます。
変数を整理する方法、本ガイドの他の部分を参照してください。

.. _use_ssh:

Ansible を使用して接続を再利用したり、ケルベロス設定した SSH を有効にしたり、Ansible がローカルの SSH 設定を使用するにはどうしたらいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

設定ファイルのデフォルトの接続タイプを「ssh」に切り替えるか、Python Paramiko ライブラリーの代わりに、「-c ssh」で、
ネイティブの OpenSSH の接続を使用してください。 Ansible 1.2.1 以降では、OpenSSH が新しく、
オプションとして ControlPersist をサポートする場合にはデフォルトで「ssh」を使用します。

Paramiko は使用を開始するときには便利ですが、OpenSSH のタイプでは多数の詳細オプションを利用できます。 OpenSSH の接続タイプを使用する場合には、
ControlPersist をサポート可能な新しいマシンから Ansible を実行してください。 以前のクライアントを
管理し続けることが可能です。 RHEL 6、CentOS 6、SLES 10、または SLES 11 を使用している場合は、
OpenSSH のバージョンが若干古いため、以前のノードを管理している場合でも、Fedora または openSUSE のクライアントからの管理を検討するか、Paramiko を使用してください。

EL ボックスに Ansible を先にインストールしている場合には、新規ユーザーにとって Paramiko のほうが使用しやすいため、
Paramiko はデフォルトのままとなっています。

.. _use_ssh_jump_hosts:

アクセス権のないサーバーにジャンプホストを使用してアクセスできるように設定するにはどうすればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


`ansible_ssh_common_args` インベントリー変数に `ProxyCommand` を設定できます。該当のホストに接続したときに、
この変数に指定した引数は、
sftp/scp/ssh コマンドラインに追加されます。以下のインベントリーグループがある場合は::

..  code-block:: ini

    [gatewayed]
    foo ansible_host=192.0.2.1
    bar ansible_host=192.0.2.2

以下のコンテンツを使用して `group_vars/gatewayed.yml` を作成できます::

    ansible_ssh_common_args: '-o ProxyCommand="ssh -W %h:%p -q user@gateway.example.com"'

Ansible は、
`gatewayed` のグループのホストに接続しようとすると、コマンドラインに 3 つの引数を追加します。(`ansible.cfg` からの `ssh_args` に加えて、
上記の引数が使用されるため、
`ansible_ssh_common_args` の `ControlPersist` グローバル設定を繰り返す必要はありません。)

`ssh -W` は、OpenSSH 5.4 以降でのみ利用できます。以前のバージョンでは、
`nc %h:%p` を実行するか、
bastion ホストで同等のコマンドを実行する必要があります。

Ansible の以前のバージョンでは、
`~/.ssh/config` のホスト 1 台または複数台に適切な `ProxyCommand` を設定するか、
`ansible.cfg` に `ssh_args` をグローバルに設定する必要がありました。

.. _ssh_serveraliveinterval:

Ansible がダウンしているターゲットを適宜検出できるようにするにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

``ansible.cfg`` の ``ssh_args`` に ``-o ServerAliveInterval=NumberOfSeconds`` を追加してください。このオプションがないと、Ansible は TCP 接続がタイムアウトになるまで待機します。別の解決策として、グローバルの SSH 設定に、``ServerAliveInterval`` を追加してください。``ServerAliveInterval`` に適した値は、ユーザーが決定します。ただし、SSH のデフォルトは ``ServerAliveCountMax=3`` であるため、SSH セッションの終了前に設定した値が 3 倍になる点に注意してください。

.. _ec2_cloud_performance:

EC2 内の管理の速度を高めるにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++

ラップトップから EC2 マシンを管理しないようにしてください。 先に EC2 内の管理ノードに接続して、
そこから Ansible を実行してください。

.. _python_interpreters:

リモートマシンの /usr/bin/python に Python インタープリターを配置せずに、Python に対応するにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Ansible モジュールはどの言語でも記述できますが、Ansible を動作させるコアモジュールなど、
Ansible モジュールの多くは Python で記述されています。

デフォルトでは、Ansible は、リモートシステムにある :command:`/usr/bin/python` を見つけることができることを前提としています。
つまり、Python2 のバージョン 2.6 以降、または Python3 のバージョン 3.5 以降です。

ホストに ``ansible_python_interpreter`` のインベントリー変数を設定すると、Ansible に対して、
Python インタープリターをこのインベントリー変数の値に自動で置き換えるように指示を出します。このように、
お使いのシステムの :command:`/usr/bin/python` が互換性のある Python インタープリターを参照していない場合には、
希望の Python を参照できます。

プラットフォームによっては、デフォルトで Python3 しかインストールされていない場合もあります。Python3 が、
:command:`/usr/bin/python` としてインストールされていない場合は、
``ansible_python_interpreter`` を使用してこのインタープリターへのパスを設定する必要があります。コアモジュールの多くが Python 3 と連携しますが、
特別な目的を持つモジュールでは、特殊なケースでバグが発生したり、Python 3 と連携しない可能性があります。一時的な回避策として、
管理ホストに Python 2 をインストールし、
``ansible_python_interpreter`` を使用して、この Python を使用するように、Ansible を設定できます。モジュールのドキュメントに、Python 2 が必要であると記載されていない場合には、
今後この非互換性の問題が解決されるように、`バグトラッカー
<https://github.com/ansible/ansible/issues>`_ で、バグを報告してください。

Python モジュールのシバン (!#) の行は置き換えないでください。 デプロイ時に Ansible が自動でこれを実行します。

また、これは `ansible_ruby_interpreter`、perl: `ansible_perl_interpreter` など、どのインタープリターでも機能するため、
任意のスクリプト言語で記述したカスタムモジュールにこれを使用して、インタープリターの場所を管理できます。

モジュールのシバンの行 (`#!/usr/bin/env <other>`) に `env` を挿入すると、
この機能は無視され、リモートの `$PATH` の設定が使用されます。

.. _installation_faqs:

Ansible インストール中に Ansible パッケージに必要な依存関係にどのように対応すればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Ansible のインストール時に `No package 'libffi' found` または `fatal error Python.h:No such file or directory`
などのエラーが発生する場合があります。このようなエラーは通常、Ansible で必要なパッケージの依存関係パッケージがない場合に発生します。
たとえば、`libffi` パッケージは `pynacl` と `paramiko` (Ansible -> paramiko -> pynacl -> libffi) の依存関係です。

このような依存関係の問題を解決するには、OS ネイティブのパッケージマネージャー (`yum`、`dnf`、または `apt` またはパッケージのインストールガイドに記載のもの) のインストールが必要になる場合があります。

このような依存関係とそのインストール方法は、各パッケージのドキュメントを参照してください。

一般的なプラットフォームの問題
++++++++++++++++++++++

Red Hat では、どのような顧客のプラットフォームをサポートしていますか
---------------------------------------------

さまざまなプラットフォームをサポートしています。具体的な一覧は、`ナレッジベースの記事<https://access.redhat.com/articles/3168091>`_ を参照してください。

virtualenv での実行
-----------------------

コントローラーの virtualenv に Ansible を簡単にインストールできます。

.. code-block:: shell

    $ virtualenv ansible
$ source ./ansible/bin/activate
$ pip install ansible

Python 2 ではなく Python 3 で実行する場合は、以下のように変更する場合があります。

.. code-block:: shell

    $ virtualenv -p python3 ansible
$ source ./ansible/bin/activate
$ pip install ansible

pip で入手できないライブラリーを使用する必要がある場合 (
例: SELinux が有効な Red Hat Enterprise Linux または Fedora などのシステムにある SELinux Python のバインディング) は、
virtualenv にインストールする必要があります。 方法は 2 種類あります。

* virtualenv の作成時に、``--system-site-packages`` を指定して、
  お使いのシステムの Python にインストールされているライブラリーを使用します。

  .. code-block:: shell

      $ virtualenv ansible --system-site-packages

* システムから手動でこれらのファイルをコピーします。 たとえば、SELinux バインディングでは、以下を行うことができます。

  .. code-block:: shell

      $ virtualenv ansible --system-site-packages
$ cp -r -v /usr/lib64/python3.*/site-packages/selinux/ ./py3-ansible/lib64/python3.*/site-packages/
      $ cp -v /usr/lib64/python3.*/site-packages/*selinux*.so ./py3-ansible/lib64/python3.*/site-packages/


BSD の実行
--------------

.. seealso:: :ref:`working_with_bsd`


Solaris での実行
------------------

デフォルトでは Solaris 10 以前では POSIX 以外のシェルを実行しますが、
Ansible が使用するデフォルトの tmp ディレクトリー ( :file:`~/.ansible/tmp`) を正しく展開しません。Solaris マシンでモジュールの問題が発生する場合には、
上記が問題の可能性が高いです。回避策はいくつかあります。

* 使用するシェル (:ref:`C shell<csh_shell>`、:ref:`fish shell<fish_shell>`、および :ref:`Powershell<powershell_shell>` のプラグインのドキュメントを参照) で正しく展開されるパスに、``remote_tmp`` を設定します。 設定する ansible 設定ファイルで、
  以下を指定します。

    remote_tmp=$HOME/.ansible/tmp

  Ansible 2.5 以降では、以下のようにインベントリーでホストごとに設定することも可能です。

    solaris1 ansible_remote_tmp=$HOME/.ansible/tmp

* :ref:`ansible_shell_executable<ansible_shell_executable>` を、POSIX の互換性のあるシェルのパスに設定します。 たとえば、
  多数の Solaris ホストの POSIX シェルは、:file:`/usr/xpg4/bin/sh` に配置されているため、
  インベントリーのこの値を以下のように設定できます。

    solaris1 ansible_shell_executable=/usr/xpg4/bin/sh

  (bash、ksh および zsh がインストールされている場合には、これも POSIX の互換性が必要です)。

z/OS での実行
---------------

z/OS でターゲットとして Ansible を実行しようとすると、複数の共通のエラーが発生する可能性があります。

* z/OS 向けの Python バージョン 2.7.6 は、内部で文字列を EBCDIC として表現するため、Ansible では機能しない。

  この制限を回避するには、文字列を ASCII で表現する `python for z/OS <https://www.rocketsoftware.com/zos-open-source>`_ (2.7.13 または 3.6.1) をダウンロードしてインストールしてください。 バージョン 2.7.13 では機能することが確認されています。

* `/etc/ansible/ansible.cfg` で ``pipelining = False`` と指定されている場合には、Ansible モジュールは Python の実行エラーが何であっても、sftp 経由でバイナリーモードで転送される。

  .. error::
      SyntaxError:Non-UTF-8 code starting with \\'\\x83\\' in file /a/user1/.ansible/tmp/ansible-tmp-1548232945.35-274513842609025/AnsiballZ\_stat.py on line 1, but no encoding declared; see https://python.org/dev/peps/pep-0263/ for details

  これを修正するには、`/etc/ansible/ansible.cfg` で ``pipelining = True`` と指定してください。

* Python インタープリターがターゲットホストのデフォルトの場所 ``/usr/bin/python`` で検出できない。

  .. error::
      /usr/bin/python:EDC5129I No such file or directory

  これを解決するには、以下のようにインベントリーでパスを Python インストールに設定してください。

    zos1 ansible_python_interpreter=/usr/lpp/python/python-2017-04-12-py27/python27/bin/python

* ``The module libpython2.7.so was not found.`` のエラーで Python が起動しない。

  .. error::
    EE3501S The module libpython2.7.so was not found.

  z/OS では、gnu bash から python を実行する必要があります。 gnu bash が ``/usr/lpp/bash`` でインストールされている場合には、インベントリーで ``ansible_shell_executable`` を指定して修正できます。

    zos1 ansible_shell_executable=/usr/lpp/bash/bin/bash


.. _use_roles:

コンテンツを再利用/再配信できるようにする最適な方法は何ですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Playbook ドキュメントの「ロール」の情報をまだ読んでいない場合は、一読してください。 Playbook のコンテンツを自己完結型にし、
git submodules などと連携させて、他とのコンテンツ共有が容易になります。

このようなプラグインタイプの詳細は、Ansible の拡張方法に関する詳細を API ドキュメントで確認してください。

.. _configuration_file:

設定ファイルの配置場所はどこですか。または、どのように設定すればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


:ref:`intro_configuration` を参照してください。

.. _who_would_ever_want_to_disable_cowsay_but_ok_here_is_how:

cowsay はどのように無効化すればいいですか
++++++++++++++++++++++++

cowsay がインストールされている場合には、Playbook を実行すると、Ansible がすべてを引き受けて処理します。 プロフェッショナルな cowsay なしの環境で作業することにした場合には、
cowsay をアンインストールするか、ansible.cfg に ``nocows=1`` を設定するか、:envvar:`ANSIBLE_NOCOWS` の環境変数を設定します。

.. code-block:: shell-session

    export ANSIBLE_NOCOWS=1

.. _browse_facts:

ansible_ variables の一覧をどのようにすれば確認できますか
++++++++++++++++++++++++++++++++++++++++++++++++++++++

Ansible はデフォルトで、管理対象のマシンの「ファクト」を収集し、このファクトには Playbook またはテンプレートでアクセスできます。あるマシンに関するファクトの一覧を表示するには、「setup」モジュールを ad-hoc アクションとして実行できます。

.. code-block:: shell-session

    ansible -m setup hostname

このコマンドでは、特定のホストで利用可能な全ファクトのディクショナリーが出力されます。ページャーの出力をパイプする場合には、インベントリー変数や内部の「magic」変数は含まれません。「ファクト」以外の情報が必要な場合には、次の質問を確認してください。


.. _browse_inventory_vars:

ホストに定義されたインベントリー変数をすべて確認するにはどうすればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

以下のコマンドを実行すると、ホストのインベントリー変数を確認できます。

.. code-block:: shell-session

    ansible-inventory --list --yaml


.. _browse_host_vars:

ホスト固有の全変数を確認するにはどうすればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++

ホスト固有の変数をすべて確認するには以下を実行します (ファクトや他のソースが含まれる可能性があります)。

.. code-block:: shell-session

    ansible -m debug -a "var=hostvars['hostname']" localhost

ファクトキャッシュを使用していない限り、上記のタスクに含まれるファクトについては、通常、先にファクトを収集する Play を使用する必要があります。


.. _host_loops:

テンプレート内のグループに含まれるホストの一覧をループするにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

一般的なパターンとして、サーバー一覧でテンプレート設定ファイルを生成するなど、
ホストグループ内のホスト一覧で繰り返し作業を行います。これには、以下のようにお使いのテンプレートで "$groups" ディクショナリーにアクセスするだけです。

.. code-block:: jinja

    {% for host in groups['db_servers'] %}
        {{ host }}
    {% endfor %}

このようなホストに関するファクト (例: 各ホスト名の IP アドレスなど) を使用する必要がある場合には、ファクトが生成されていることを確認する必要があります。たとえば、db_servers と対話するプレイがあることを確認します。

    - hosts:  db_servers
      tasks:
        - debug: msg="doesn't matter what you do, just that they were talked to previously."

次に、以下のように、テンプレート内のファクトを使用できます。

.. code-block:: jinja

    {% for host in groups['db_servers'] %}
       {{ hostvars[host]['ansible_eth0']['ipv4']['address'] }}
    {% endfor %}

.. _programatic_access_to_a_variable:

プログラムで変数名にアクセスするにはどうすればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++

たとえば、ロールのパラメーターや他の入力情報で使用するインターフェースを指定する場合など、任意のインターフェースの IPv4 アドレスを取得する必要があるときなどに、
プログラムで変数名にアクセスします。 以下のように、変数名は、以下のように文字列を追加することで構築できます。

.. code-block:: jinja

    {{ hostvars[inventory_hostname]['ansible_' + which_interface]['ipv4']['address'] }}

変数の全 namespace に含まれるディクショナリーであるため、hostvars 全体をチェックするにはコツが必要です。
「inventory_hostname」はマジック変数で、ホストループでループを行う現在のホストを指定します。

「dynamic_variables_」も参照してください。


.. _access_group_variable:

グループ変数にアクセスするにはどうすればいいですか
+++++++++++++++++++++++++++++++++

Ansible は、技術的にはグループ変数にアクセスせず、直接グループを使用するわけではありません。グループは、ホスト選択のラベルとして機能し、変数を一括で割り当てる手段を提供します。グループは、第一級オブジェクトではありません。Ansible が関心があるのは、ホストとタスクのみです。

ただし、対象のグループに含まれるホストを選択すると、変数にアクセスできます。例については、first_host_in_a_group_ below を参照してください。


.. _first_host_in_a_group:

グループ内の最初のホストの変数にアクセスするにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++

webservers グループの最初の webserver の IP アドレスが必要な場合にはどうすればいいですか。 Ansible ではこれも可能です。 動的なインベントリーを使用する場合には、
最初に使用するホストに一貫性がないため、
インベントリーが静的な場合や推測可能な場合以外での使用は推奨されません。 (:ref:`ansible_tower` を使用する場合には、データベースの順番を使用するため、
クラウドベースのインベントリースクリプトを使用している場合でも問題はありません)。

以下に方法を示します。

.. code-block:: jinja

    {{ hostvars[groups['webservers'][0]]['ansible_eth0']['ipv4']['address'] }}

webserver グループの最初のマシンのホスト名を取得している点に注意してください。 テンプレートでこれを行う場合は、
Jinja2 (#set' directive to simplify this, or in a playbook, you could also use set_fact::) を使用できます。

    - set_fact: headnode={{ groups[['webservers'][0]] }}

    - debug: msg={{ hostvars[headnode].ansible_eth0.ipv4.address }}

ドットの代わりにカッコの構文を使用している点に注意してください。これはどこでも使用できます。

.. _file_recursion:

ターゲットホストにファイルを再帰的にコピーするにはどうすればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++

「copy」モジュールには、再帰的なパラメーターがあります。 ただし、大量のファイルを効率的に処理するには、「synchronize」モジュールも確認してください。 「synchroize」モジュールは、rsync もラップします。 copy と synchroize モジュールの情報は、モジュールのインデックスを参照してください。

.. _shell_env:

shell 環境変数にアクセスするにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++

既存の変数 ON THE CONTROLLER へのアクセスだけが必要な場合は、lookup プラグイン「env」を使用してください。
たとえば、管理マシンで HOME 環境変数の値にアクセスするには、以下を指定します。

   ---
   # ...
vars:
local_home: "{{ lookup('env','HOME') }}"


ターゲットマシンの環境変数の場合には、'ansible_env' 変数のファクトを使用して入手します。

.. code-block:: jinja

   {{ ansible_env.SOME_VARIABLE }}

タスクの実行に環境変数を設定する必要がある場合には、:ref:`高度な Playbook <playbooks_special_topics>` セクションの :ref:`playbooks_environment` を参照してください。
ターゲットマシンで環境変数を設定する方法は複数存在します。テンプレートの :ref:`template <template_module>` モジュール、:ref:`replace <replace_module>` モジュールまたは :ref:`lineinfile <lineinfile_module>` モジュールを使用して、環境変数をファイルに導入できます。
OS、ディストリビューション、設定により、変数するファイルは異なります。

.. _user_passwords:

ユーザーモジュールの暗号化パスワードを生成するにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Ansible ad-hoc コマンドを使用するのが最も簡単なオプションです。

.. code-block:: shell-session

    ansible all -i localhost, -m debug -a "msg={{ 'mypassword' | password_hash('sha512', 'mysecretsalt') }}"

また、他に優れたオプションとして、大半の Linux システムで利用可能な mkpasswd ユーティリティーを使用する方法があります。

.. code-block:: shell-session

    mkpasswd --method=sha-512


お使いのシステムにこのユーティリティーがインストールされていない場合 (例: MacOS を使用している場合など) には、
Python を使用してこのようなパスワードを簡単に生成できます。まず、`Passlib <https://bitbucket.org/ecollins/passlib/wiki/Home>`_ パスワードが、
hashing ライブラリーにインストールされていることを確認します。

.. code-block:: shell-session

    pip install passlib

ライブラリーの準備ができたら、以下のように SHA512 パスワードの値を生成できます。

.. code-block:: shell-session

    python -c "from passlib.hash import sha512_crypt; import getpass; print(sha512_crypt.using(rounds=5000).hash(getpass.getpass()))"

統合された :ref:`hash_filters` を使用して、ハッシュ化されたパスワードを生成します。
Playbook や host_vars にプレーンテキストのパスワードを挿入するべきではありません。代わりに、:ref:`playbooks_vault` を使用して、機密データを暗号化してください。

OpenBSD には、ベースステムの encrypt(1) と呼ばれる、よく似たオプションがあります。

.. code-block:: shell-session

    encrypt

.. _dot_or_array_notation:

Ansible では、変数のドット表記とアレイ表記が可能ですが、どちらの表記を使用するべきですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ドット表記は Jinja からのもので、
特殊文字を使用せずに変数と合わせて使用できます。変数にドット (.)、コロン (:)、またはハイフン (-) が含まれていて、
キーが 2 つのアンダースコアで開始および終了する場合、
またはキーが既知のパブリック属性のいずれかを使用する場合は、配列表記を使用する方が安全です。既知のパブリック属性の一覧は、「:ref:`playbooks_variables`」
を参照してください。

.. code-block:: jinja

    item[0]['checksum:md5']
    item['section']['2.1']
    item['region']['Mid-Atlantic']
    It is {{ temperature['Celsius']['-3'] }} outside.

また、アレイ表記は、動的な変数の構成が可能です。詳細は、dynamic_variables_ を参照してください。

「ドット表記」の他の問題として、ドット表記のキーによっては、Python ディクショナリーの属性とメソッドと競合するため、問題が発生する可能性があります。

.. code-block:: jinja

    item.update # this breaks if item is a dictionary, as 'update()' is a python method for dictionaries
item['update'] # this works


.. _argsplat_unsafe:

変数からタスク引数の一括設定をすると安全でないのはどのような場合ですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


ディクショナリー型の変数からタスクの引数をすべて設定できます。この手法は、
動的な実行シナリオで便利な場合があります。ただし、
セキュリティーのリスクが伴います。これは推奨されないため、以下のようなことを行ったときに、
Ansible は警告を表示します。

    #...
vars:
  usermod_args:
    name: testuser
    state: present
    update_password: always
tasks:
- user: '{{ usermod_args }}'

この特定の例は、安全です。ただし、
``usermod_args`` に渡されるパラメーターや値が、
ウイルスなどに感染したターゲットマシンの ``host facts`` に含まれる悪意のある値で上書きされる可能性があるため、
このようなタスクの構築にはリスクがあります。このリスクを軽減するには、以下を実行します。

* :ref:`ansible_variable_precedence` にある優先順位で、``host facts`` より優先順位の高いレベルで一括変数を設定します (変数はファクトより優先度が高いので、上記の例は安全です)
* ファクトの値が変数と競合しないように :ref:`inject_facts_as_vars` 設定オプションを無効にします (元の警告も無効になります)


.. _commercial_support:

Ansible のトレーニングはありますか
++++++++++++++++++++++++++++++

はい。あります。 サービスおよびトレーニングサービスに関する情報は、`サービスページ <https://www.ansible.com/products/consulting>`_ を参照してください。詳細は、`info@ansible.com <mailto:info@ansible.com>`_ までお問い合わせください。

また、定期的に、Web ベースのトレーニングも無料で提供しています。今後発表されるウェビナーの詳細は、`ウェビナーページ <https://www.ansible.com/resources/webinars-training>`_ を参照してください。


.. _web_interface:

Web インターフェースや REST API などがありますか
++++++++++++++++++++++++++++++++++++++++++

はい。あります。 Ansible, Inc は、Ansible がより強力で使いやすくなるように、優れた製品を提供しています。:ref:`ansible_tower` を参照してください。


.. _docs_contributions:

ドキュメントへの変更を提出するにはどうすればいいですか
++++++++++++++++++++++++++++++++++++++++++++++

ご質問ありがとうございます。 Ansible のドキュメントは、主要プロジェクトの git リポジトリーに保存されており、寄稿に関する説明が `GitHub の README <https://github.com/ansible/ansible/blob/devel/docs/docsite/README.md>` に記載されています。 こちらを参照してください。


.. _keep_secret_data:

Playbook に機密データを保存するにはどうすればいいですか?
+++++++++++++++++++++++++++++++++++++++++

Ansible のコンテンツに機密データを保存してそのコンテンツを公開するか、ソースコントロールに保持する場合は、:ref:`playbooks_vault` を参照してください。

-v (詳細) モードの使用時にコマンドをタスクに渡さないようにしたり、結果を表示しないようにする場合に、以下のタスクまたは Playbook 属性が便利です。

    - name: secret task
      shell: /usr/bin/do_something --value={{ secret_value }}
      no_log:True

詳細な出力を確認できるユーザーに対して、出力を詳細に保ちながらも、機密情報を非表示にするときに使用できます。

no_log 属性は、プレイ全体にも適用できます。

    - hosts: all
      no_log:True

ただし、これを使用すると、プレイのデバッグが困難になります。 Playbook が完了すると、
この属性は単一のタスクにのみ適用することが推奨されます。no_log 属性
を使用しても、
:envvar:`ANSIBLE_DEBUG` 環境変数で Ansible 自体をデバッグするときに、データが表示されてしまう点に注意してください。


.. _when_to_use_brackets:
.. _dynamic_variables:
.. _interpolate_variables:

{{ }} はいつ使用すればいいですか。また、変数または動的な変数名を挿入するにはどうすればいいですか
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

不動のルールとして、``when:``' 条件を使用する場合以外は ``{{ }}`` を使用します。
この条件は、式の解決として Jinja2 を調べます。
したがって、``when:``、``failed_when:``、および ``changed_when:`` はテンプレート化されるため、``{{ }}`` の追加は回避してください。

それ以外のケースでは、``loop`` または ``with_`` 句などを指定せずに以前は変数を使用できていた場合でも、常にカッコを使用するようにしてください。理由は、未定義の変数と文字列を区別しにくいためです。

他には「波括弧は並べて使用できない」というルールがありますが、これは頻繁に見受けられます。

.. code-block:: jinja

     {{ somevar_{{other_var}} }}

上記の例は想定通り、機能しません。動的変数を使用する必要がある場合には、随時、以下を使用してください。

.. code-block:: jinja

    {{ hostvars[inventory_hostname]['somevar_' + other_var] }}

「non host vars」の場合には、:ref:`vars lookup<vars_lookup>` プラグインを使用できます。

.. code-block:: jinja

     {{ lookup('vars', 'somevar_' + other_var) }}


.. _why_no_wheel:

なぜ X 形式で提供していないのですか
+++++++++++++++++++++++++++++++

多くの場合に、メンテナンスができるかどうかに関係します。ソフトウェアの提供方法は多数あり、全プラットフォームで Ansible をリリースするリソースがありません。
場合によっては、技術的な問題があります。たとえば、Python Wheels には依存関係がありません。

.. _ansible_host_delegated:

タスクを委譲した場合に元の ansible_host をどのように取得すればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

ドキュメントに記載されているように、接続変数は ``delegate_to`` ホストから取得されるので、``ansible_host`` は上書きされますが、
``hostvars`` を使用して元の ansible_host にアクセスできます。

   original_host: "{{ hostvars[inventory_hostname]['ansible_host'] }}"

これは、``ansible_user``、``ansible_port`` などのように、上書きされた接続変数すべてに有効です。


.. _scp_protocol_error_filename:

ファイルの取得時の「protocol error: filename does not match request」のエラーはどのように修正すればいいですか
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

OpenSSH の比較的新しいリリースには、SCP クライアントに `バグ <https://bugzilla.mindrot.org/show_bug.cgi?id=2966>`_ があり、ファイル転送メカニズムとして SCP を使用する場合に、Ansible コントローラーで以下のエラーがトリガーされる可能性があります。

    failed to transfer file to /tmp/ansible/file.txt\r\nprotocol error: filename does not match request

新しいリリースでは、SCP は、取得するファイルのパスが要求したパスと一致するかを検証しようとします。
リモートのファイル名が、
パスでスペースや ASCII 文字以外の文字を引用符でエスケープする必要がある場合には、検証に失敗します。このエラーを回避するには、以下を行います。

* ``scp_if_ssh`` を ``smart`` (先に SFTP を試す) または ``False`` に設定して、SCP の代わりに SFTP を使用します。以下の 4 つの方法から 1 つ実行してください。
    * ``smart`` のデフォルトの設定に依存する。``scp_if_ssh`` が明示的にどこにも設定されていない場合に機能します。
    * <group_variables>インベントリーに :ref:`ホスト変数` <host_variables>または :ref:`グループ変数` を設定 (``ansible_scp_if_ssh: False``) する。
    * コントロールノードで環境変数を設定する (``export ANSIBLE_SCP_IF_SSH=False``)。
    * Ansible の実行時に、環境変数 ``ANSIBLE_SCP_IF_SSH=smart ansible-playbook``を指定する。
    * ``ansible.cfg`` ファイルを変更 (``scp_if_ssh=False`` を ``[ssh_connection]`` セクションに追加) する。
* SCP を使用する必要がある場合には、``-T`` の引数を設定して、SCP クライアントにパスの検証を無視するように指示します。以下の 3 つの方法から 1 つ実行してください。
    * :ref:`ホスト変数 <host_variables>` または :ref:`グループ変数 <group_variables>` を設定する (``ansible_scp_extra_args=-T``)。
    * 環境変数をエクスポートするか、指定する (``ANSIBLE_SCP_EXTRA_ARGS=-T``)。
    * ``ansible.cfg`` ファイルを変更する (``scp_extra_args=-T`` を ``[ssh_connection]`` セクションに追加)。

.. note:: ``-T`` の使用時に ``invalid argument`` エラーが表示される場合は、SCP クライアントがファイル名を検証しておらず、このエラーはトリガーされません。

.. _i_dont_see_my_question:

ここに記載されている以外に質問があります。
++++++++++++++++++++++++++++

以下のセクションに、IRC および Google グループへのリンクがあります。こちらから、質問をしてください。

.. seealso::

   :ref:`working_with_playbooks`
       Playbook の概要
   :ref:`playbooks_best_practices`
       ベストプラクティスのアドバイス
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
