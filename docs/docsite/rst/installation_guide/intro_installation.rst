.. \_installation\_guide: .. \_intro\_installation\_guide:

インストールガイド
==================

.. contents::トピック

本書は Ansible インストールガイドです。

.. \_what\_will\_be\_installed:

基本情報 / インストール内容 \`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

Ansible はデフォルトでは、マシンを SSH プロトコル経由で管理します。

Ansible のインストールが済むと、Ansible によりデータベースが追加されることはなく、また、デーモンを起動したり、実行し続ける必要もありません。Ansibleを 1 台のマシン (ラップトップでも可) にインストールするだけで、そのマシンからリモートマシン全体を一元管理できます。Ansible は、リモートマシンの管理時には、ソフトウェアをマシンにインストールしたまま、あるいは実行したままにすることがないので、新しいバージョンに移行する場合に Ansible のアップグレードが問題になることはありません。

.. \_what\_version:

選択すべきバージョン\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

Ansible はソースから簡単に実行され、リモートマシンへのソフトウェアのインストールを必要としないため、ユーザーの多くが実質的に開発バージョンをフォローすることになります。

通常、Ansible のリリースサイクルは約 4 か月です。リリースサイクルがこのように短いため、マイナーバグの場合は、安定したブランチでバックポートを管理するのではなく、通常は次回のリリースで修正されます。メジャーバグについては、必要なときにメンテナンスリリースが行われますが、このようなことはあまり頻繁には起こりません。

Red Hat Enterprise Linux (TM)、CentOS、Fedora、Debian、または Ubuntu を実行しており、Ansible の最新リリースバージョンの実行を希望される場合には、OS パッケージマネージャーを使用することをお勧めします。

その他のインストールオプションについては、Python パッケージマネージャー「``pip``」を使用したインストールをお勧めします。

開発リリースをフォローして、最新の機能を使用およびテストする方向けに、ソースからの実行に関する情報を共有します。ソースから実行するプログラムはインストールの必要がありません。

.. \_control\_node\_requirements:

コントロールノードの要件 \`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

現在、Ansible は、Python 2 (バージョン 2.7) または Python 3 (バージョン 3.5 以降) がインストールされていればどのマシンからでも実行できます。Windows では、コントロールノードのサポートはありません。

これには、Red Hat、Debian、CentOS、MacOS をはじめ、各種 BSD が含まれます。

コントロールノードの選択時には、管理システムを管理対象マシンの近くで実行すると利点があることを念頭に置いてください。Ansible をクラウドで実行している場合は、そのクラウド内のマシンから実行することを検討してください。オープンなインターネット上で実行するよりも、同じクラウド内から実行するほうがうまく機能します。

.. 注::

    MacOS はデフォルトで、少数のファイルハンドル向けに設定されているため、15 個以上のフォークを使用する場合は、「sudo launchctl limit maxfiles unlimited」を使用して ulimit を増やす必要があります。このコマンドでは、「Too many open files」エラーも修正できます。


.. 警告::

    一部のモジュールおよびプラグインには追加の要件がありますので注意してください。モジュールでは、「ターゲット」マシンでこの追加要件を満たす必要があります。これについてはモジュール固有のドキュメントに記載されています。

.. \_managed\_node\_requirements:

管理ノードの要件\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

管理ノードでは通信手段が必要です。通常は ssh が使われます。デフォルトでは、管理ノードの通信に sftp を使用します。sftp を使用できない場合は、:file:`ansible.cfg` で scp に切り替えることができます。Python 2 (バージョン 2.6 以降) または Python 3 (バージョン 3.5 以降) も必要になります。

.. 注::

   * リモートノードで SELinux が有効になっている場合は、Ansible でコピー/ファイル/テンプレート関連の機能を使用する前にそれらのノードに libselinux-python をインストールしておくとよいでしょう。このパッケージがないリモートシステムに、libselinux-python をインストールするには、Ansible で :ref:`yum module<yum_module>` または :ref:`dnf module<dnf_module>` を使用してください。

   * デフォルトでは、Ansible は :file:`/usr/bin/python` にある python インタープリターを使用してそのモジュールを実行します。ただし、Linux ディストリビューションによっては、デフォルトで :file:`/usr/bin/python3` に Python 3 インタープリターしかインストールされていない場合があります。そのようなシステムでは、以下のようなエラーが表示される場合があります。

        "module_stdout": "/bin/sh: /usr/bin/python:No such file or directory\r\n"

     :ref:`ansible_python_interpreter<ansible_python_interpreter>` インベントリー変数 (:ref:`インベントリー`を参照) を設定してインタープリターを参照するか、使用するモジュール用の Python 2 インタープリターをインストールすることができます。Python 2 インタープリターが :command:`/usr/bin/python` にインストールされていない場合にも、:ref:`ansible_python_interpreter<ansible_python_interpreter>` を設定する必要があります。

   * Ansible の :ref:`raw module<raw_module>` および :ref:`script module<script_module>` は、Python のクライアント側インストールには依存せず実行できます。技術的には、Ansible で :ref:`raw module<raw_module>` を使用して Python の互換バージョンをインストールできるので、他のものもすべて使用できるようになります。たとえば、Python 2 を RHEL ベースのシステムにブートストラップする必要がある場合は、以下を使ってインストールできます。

     .. code-block:: shell

        $ ansible myhost --become -m raw -a "yum install -y python2"

.. \_installing\_the\_control\_node:

コントロールノードのインストール \`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\` .. \_from\_yum:

DNF または Yum 経由の最新リリース +++++++++++++++++++++++++++++

Fedora の場合:

.. code-block:: bash

    $ sudo dnf install ansible

RHEL および CentOS の場合:

.. code-block:: bash

    $ sudo yum install ansible

RHEL 7 および RHEL 8 用の RPM は、「`Ansible Engine リポジトリー <https://access.redhat.com/articles/3174981>`_ 」から入手できます。

RHEL 8 用の Ansible Engine リポジトリーを有効にするには、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo subscription-manager repos --enable ansible-2.9-for-rhel-8-x86_64-rpms

RHEL 7 用の Ansible Engine リポジトリーを有効にするには、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo subscription-manager repos --enable rhel-7-server-ansible-2.9-rpms

現行サポート対象バージョンの RHEL、CentOS、および Fedora 用の RPM は、`EPEL <https://fedoraproject.org/wiki/EPEL>`_ および `releases.ansible.com <https://releases.ansible.com/ansible/rpm>`_ から入手できます。

Ansible バージョン 2.4 以降では、Python 2.6 以降が含まれている旧オペレーティングシステムを管理できます。

RPM を独自に構築することも可能です。チェックアウトまたは tarball のルートから、``make rpm`` コマンドを使用して、配布およびインストール可能な RPM を構築します。

.. code-block:: bash

    $ git clone https://github.com/ansible/ansible.git
    $ cd ./ansible
    $ make rpm
    $ sudo rpm -Uvh ./rpm-build/ansible-*.noarch.rpm

.. \_from\_apt:

Apt 経由の最新リリース (Ubuntu) ++++++++++++++++++++++++++++++++

Ubuntu ビルドは `こちら <https://launchpad.net/~ansible/+archive/ubuntu/ansible> の PPA` で入手できます。

自分のマシンに PPA を設定して Ansible をインストールするには、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo apt update
    $ sudo apt install software-properties-common
    $ sudo apt-add-repository --yes --update ppa:ansible/ansible
    $ sudo apt install ansible

.. 注::以前の Ubuntu ディストリビューションでは、「software-properties-common」は「python-software-properties」と呼ばれます。過去のバージョンでは ``apt`` ではなく ``apt-get`` を使用するほうがよい場合があります。また、``-u`` あるいは ``--update`` フラグが指定されているのは新しいディストリビューション (例: 18.04、18.10 など) のみなので注意してください。随時、スクリプトは調整してください。

Debian/Ubuntu パッケージは、ソースチェックアウトから構築することもできます。以下を実行します。

.. code-block:: bash

    $ make deb

ソースから実行して最新のパッケージを取得することも可能です。この点については以下で説明します。

Apt 経由の最新リリース (Debian) ++++++++++++++++++++++++++++++++

Debian を使用されている場合は Ubuntu PPA と同じソースを使用できます。

以下の行を /etc/apt/sources.list に追加します。

.. code-block:: bash

    deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main

次に、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
    $ sudo apt update
    $ sudo apt install ansible

.. 注::この方法は、Debian Jessie および Stretch の Trusty ソースで検証されていますが、以前のバージョンではサポートされない可能性があります。過去のバージョンでは ``apt`` ではなく ``apt-get`` を使用するほうがよい場合があります。

Portage 経由の最新リリース (Gentoo) ++++++++++++++++++++++++++++++++++++

.. code-block:: bash

    $ emerge -av app-admin/ansible

最新バージョンをインストールするには、emerge コマンド実行前に Ansible パッケージのマスク解除が必要になる場合があります。

.. code-block:: bash

    $ echo 'app-admin/ansible' >> /etc/portage/package.accept_keywords

pkg 経由の最新リリース (FreeBSD) +++++++++++++++++++++++++++++++++

Ansible は Python 2 および 3 の両バージョンで動作しますが、FreeBSD パッケージは各 Python バージョンごとに異なります。したがって、インストールには、以下を使用できます。

.. code-block:: bash

    $ sudo pkg install py27-ansible

または

.. code-block:: bash

    $ sudo pkg install py36-ansible


ポートからインストールすることもできます。以下を実行します。

.. code-block:: bash

    $ sudo make -C /usr/ports/sysutils/ansible install

特定のバージョン (すなわち ``ansible25``) を選択することもできます。

以前のバージョンの FreeBSD は、以下のようなもので動作します (パッケージマネージャーの代わり)。

.. code-block:: bash

    $ sudo pkg install ansible

.. \_on\_macos:

MacOS での最新のリリース ++++++++++++++++++++++++++

Mac に Ansible をインストールするには ``pip`` を使用する方法が推奨されます。

手順は、「`Pip 経由の最新リリース`_ 」のセクションに記載されています。MacOS バージョン 10.12 以前を実行している場合に、Python Package Index に安全に接続するには最新の ``pip`` にアップグレードする必要があります。

.. \_from\_pkgutil:

OpenCSW 経由の最新リリース (Solaris) +++++++++++++++++++++++++++++++++++++

Solaris をご利用の場合には、Ansible は、`OpenCSW <https://www.opencsw.org/packages/ansible/> から SysV パッケージ` として入手できます。

.. code-block:: bash

    # pkgadd -d http://get.opencsw.org/now
    # /opt/csw/bin/pkgutil -i ansible

.. \_from\_pacman:

Pacman 経由の最新リリース (Arch Linux) +++++++++++++++++++++++++++++++++++++++

Ansible はコミュニティーリポジトリーで入手できます。

    $ pacman -S ansible

AUR には、GitHub から直接プルするための、`ansible-git <https://aur.archlinux.org/packages/ansible-git>`_ という PKGBUILD があります。

ArchWiki の `Ansible <https://wiki.archlinux.org/index.php/Ansible>`_ のページも参照してください。

.. \_from\_sbopkg:

sbopkg 経由の最新のリリース (Slackware Linux) ++++++++++++++++++++++++++++++++++++++++++++

Ansible のビルドスクリプトは `SlackBuilds.org <https://slackbuilds.org/apps/ansible/>`_ リポジトリーで入手できます。`sbopkg <https://sbopkg.org/>`_ を使用してビルドおよびインストールできます。

Ansible およびすべての依存関係を含むキューを作成します。

    # sqg -p ansible

作成した queuefile からパッケージを構築してインストールします (sbopkg がキューまたはパッケージを使用する必要がある場合の問題への回答 Q)。

    # sbopkg -k -i ansible

.. \_from swupd:

swupd 経由の最新のリリース (Clear Linux) +++++++++++++++++++++++++++++++++++++++

Ansible およびその依存関係は、sysadmin ホスト管理バンドルの一部として利用できます。

    $ sudo swupd bundle-add sysadmin-hostmgmt

ソフトウェアの更新は、swupd ツールにより管理されます。

   $ sudo swupd update

.. \_from\_pip:

Pip 経由の最新のリリース+++++++++++++++++++++++

Ansible は、Python パッケージマネージャー ``pip`` を使用してインストールできます。Python のシステムに ``pip`` がまだない場合には、以下のコマンドを実行してインストールします。

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user

次に Ansible をインストールします \[1]\_::

    $ pip install --user ansible

または、最新の開発バージョンを探している場合は、以下を実行します。

    $ pip install --user git+https://github.com/ansible/ansible.git@devel

MacOS Mavericks (10.9) にインストールしている場合は、コンパイラーにノイズが発生する可能性があります。回避するには以下を実行します。

    $ CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip install --user ansible

``paramiko`` を必要とする ``paramiko`` 接続プラグインまたはモジュールを使用するには、必要なモジュール \[2]_ をインストールします。

    $ pip install --user paramiko

Ansible は、新規または既存の ``virtualenv`` 内にもインストールできます。

    $ python -m virtualenv ansible  # virtualenv がない場合に作成します
    $ source ansible/bin/activate   # 仮想環境をアクティブにします
    $ pip install ansible

Ansible をグローバルにインストールする場合は、以下のコマンドを実行します。

    $ sudo python get-pip.py
    $ sudo pip install ansible

.. 注::

    「sudo」を付けて「pip」を実行すると、システムにグローバルな変更が加えられます。「pip」はシステムパッケージマネージャーとは連携しないため、これが原因でシステムに変更が加えられ、不整合状態または不機能状態のままになる可能性があります。特に、これは MacOS の場合に当てはまります。システムのグローバルファイルの修正による影響を十分に理解していない場合には、「-user」を使用してインストールするようお推めします。

.. 注::

    以前のバージョンの「pip」でのデフォルトは http://pypi.python.org/simple ですが、これはもう機能しません。
    Ansible をインストールする前に、最新バージョンの「pip」を使用していることを確認してください。
    古いバージョンの「pip」がインストールされている場合は、以下の「pip のアップグレードの説明 <https://pip.pypa.io/en/stable/installing/#upgrading-pip>」_ に従ってアップグレードできます。

.. \_tagged\_releases:

タグ付けされたリリースの tarball +++++++++++++++++++++++++++

git チェックアウトせずに、Ansible をパッケージ化したり、ローカルパッケージをご自身で構築する場合があります。リリースした tarball は `Ansible ダウンロード <https://releases.ansible.com/ansible>`_ ページで入手できます。

また、これらのリリースは、`git リポジトリー <https://github.com/ansible/ansible/releases>`_ で最新バージョンにタグ付けされています。




.. \_from\_source:

ソースからの実行 +++++++++++++++++++

Ansible は、ソースから簡単に実行できます。使用するのに``root`` 権限は必要なく、実際にインストールすべきソフトウェアはありません。デーモンやデータベースの設定も必要ありません。そのため、コミュニティーの多くのユーザーが、常に Ansible の開発バージョンを使用しているため、実装時に新機能を活用でき、容易にプロジェクトに貢献できます。インストールすべきものがないため、ほとんどのオープンソースプロジェクトと比べてかなり容易に開発バージョンをフォローできます。

.. 注::

   Ansible Tower をコントロールノードとして使用する場合は、Ansible のソースインストールを使用しないでください。OS パッケージマネージャー (``apt`` もしくは ``yum`` など) または ``pip`` を使用して、安定したバージョンをインストールしてください。


ソースからインストールするには、Ansible git リポジトリーのクローンを作成します。

.. code-block:: bash

    $ git clone https://github.com/ansible/ansible.git
    $ cd ./ansible

``git`` で Ansible リポジトリーのクローンを作成したら、Ansible 環境を設定します。

Bash の使用:

.. code-block:: bash

    $ source ./hacking/env-setup

Fish の使用::

    $ source ./hacking/env-setup.fish

誤った警告やエラーが表示されないようにするには、以下を使用します。

    $ source ./hacking/env-setup -q

お使いのバージョンの Python に ``pip`` がインストールされていない場合は、インストールします。

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    $ python get-pip.py --user

Ansible は、以下の Python モジュールも使用し、このモジュールもインストールする必要があります \[1]\_。

.. code-block:: bash

    $ pip install --user -r ./requirements.txt

Ansible チェックアウトを更新するには、pull --rebase を使用してローカルの変更がリプレイされるようにします。

.. code-block:: bash

    $ git pull --rebase

.. code-block:: bash

    $ git pull --rebase # 上記と同様
    $ git submodule update --init --recursive

env-setup スクリプトを実行すると、実行がチェックアウトから行われ、デフォルトのインベントリーファイルが ``/etc/ansible/hosts`` になります。オプションで、``/etc/ansible/hosts`` 以外のインベントリーファイル (:ref:`インベントリー`を参照) を指定できます。

.. code-block:: bash

    $ echo "127.0.0.1" > ~/ansible_hosts
    $ export ANSIBLE_INVENTORY=~/ansible_hosts

インベントリーファイルの詳細については、本マニュアル内で後述します。

では、ping コマンドを使ってテストしていきましょう。

.. code-block:: bash

    $ ansible all -m ping --ask-pass

「sudo make install」も使用できます。

.. \_shell\_completion:

シェル補完 \`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

Ansible 2.9 の時点では、Ansible コマンドラインユーティリティーのシェル補完を利用できます。これは、``argcomplete`` というオプションの依存関係を使用して提供されます。``argcomplete`` は bash をサポートし、また制限付きで zsh および tcsh もサポートします。

``python-argcomplete`` は、Red Hat Enterprise ベースのディストリビューションでは EPEL からインストールでき、その他の多くのディストリビューションでは標準 OS リポジトリーで入手できます。

インストールと設定に関する詳細については、`argcomplete のドキュメント <https://argcomplete.readthedocs.io/en/latest/>_` を参照してください。

インストール ++++++++++

yum/dnf 経由
-----------

Fedora の場合:

.. code-block:: bash

    $ sudo dnf install python-argcomplete

RHEL および CentOS の場合:

.. code-block:: bash

    $ sudo yum install epel-release
    $ sudo yum install python-argcomplete

apt 経由
-------

.. code-block:: bash

    $ sudo apt install python-argcomplete

pip 経由
-------

.. code-block:: bash

    $ pip install argcomplete

設定 +++++++++++

Ansible コマンドラインユーティリティーのシェル補完を可能にする argcomplete の設定方法は、2 通りあります。コマンド単位の方法とグローバルな方法です。

グローバル
--------

グローバル補完には bash 4.2 が必要です。

.. code-block:: bash

    $ sudo activate-global-python-argcomplete

上記を実行すると、bash 補完ファイルがグローバルロケーションに書き込まれます。ロケーションを変更するには ``--dest`` を使用します。

コマンド単位
-----------

bash 4.2 がない場合は、各スクリプトを個別に登録する必要があります。

.. code-block:: bash

    $ eval $(register-python-argcomplete ansible)
    $ eval $(register-python-argcomplete ansible-config)
    $ eval $(register-python-argcomplete ansible-console)
    $ eval $(register-python-argcomplete ansible-doc)
    $ eval $(register-python-argcomplete ansible-galaxy)
    $ eval $(register-python-argcomplete ansible-inventory)
    $ eval $(register-python-argcomplete ansible-playbook)
    $ eval $(register-python-argcomplete ansible-pull)
    $ eval $(register-python-argcomplete ansible-vault)

上記のコマンドは ``~/.profile`` や ``~/.bash_profile`` などのシェルプロファイルファイルに配置することをお勧めします。

zsh または tcsh
-----------

`argcomplete のドキュメント <https://argcomplete.readthedocs.io/en/latest/>_` を参照してください。

.. \_getting\_ansible:

GitHub 上の Ansible \`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

GitHub アカウントがある場合には、`GitHub プロジェクト <https://github.com/ansible/ansible>`_ をフォローするのもよいでしょう。このプロジェクトは、バグおよび機能に関する意見を共有するための問題トラッカーが保持されている場所でもあります。


.. seealso::

   :ref:`intro_adhoc` 基本的なコマンド例、 :ref:`working_with_playbooks` Ansible の設定管理言語の学習 :ref:`installation_faqs` FAQ 関連の Ansible インストール`メーリングリスト <https://groups.google.com/group/ansible-project>`_ 質問がある場合、サポートが必要な場合、ご意見がある場合には、Google グループをのぞいてみてください。`irc.freenode.net <http://irc.freenode.net>`_ #ansible IRC チャットチャンネルのリスト

... \[1] MacOS への「pycrypto」パッケージのインストールに問題がある場合には、``CC=clang sudo -E pip install pycrypto`` を試してみてください。.. \[2] ``paramiko`` は 2.8 より前の Ansible の ``requirements.txt`` に含まれています。
