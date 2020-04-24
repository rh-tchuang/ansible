.. \_installation\_guide:
.. \_intro\_installation\_guide:

Ansible のインストール
===================

ここでは、さまざまなプラットフォームに Ansible をインストールする方法を説明します。
Ansible は、デフォルトで SSH プロトコルを介してマシンを管理するエージェントレス自動化ツールです。インストールが完了すると、
Ansible はデータベースを追加せず、起動または稼働し続けるデーモンもありません。 Ansibleを 1 台のマシン (ラップトップでも可) にインストールするだけで、そのマシンからリモートマシン全体を一元管理できます。 Ansible は、リモートマシンの管理時には、ソフトウェアをマシンにインストールしたまま、あるいは実行したままにすることがないので、新しいバージョンに移行する場合に Ansible のアップグレードが問題になることはありません。


.. contents::
  :local:

要件
--------------

Ansible をコントロールノードにインストールし、SSH (デフォルト) を使用して管理ノード (自動化するエンドデバイス) と通信します。

.. \_control\_node\_requirements:

コントロールノードの要件
^^^^^^^^^^^^^^^^^^^^^^^^^

現在、Ansible は、Python 2 (バージョン 2.7) または Python 3 (バージョン 3.5 以降) がインストールされていればどのマシンからでも実行できます。
これには、Red Hat、Debian、CentOS、MacOS をはじめ、各種 BSD が含まれます。
Windows では、コントロールノードのサポートはありません。

コントロールノードの選択時には、管理システムを管理対象マシンの近くで実行すると利点があることを念頭に置いてください。Ansible をクラウドで実行している場合は、そのクラウド内のマシンから実行することを検討してください。オープンなインターネット上で実行するよりも、同じクラウド内から実行するほうがうまく機能します。

.. note::

    MacOS はデフォルトで、少数のファイルハンドル向けに設定されているため、15 個以上のフォークを使用する場合は、「sudo launchctl limit maxfiles unlimited」を使用して ulimit を増やす必要があります。このコマンドでは、「Too many open files」エラーも修正できます。


.. warning::

    一部のモジュールおよびプラグインには追加の要件がありますので注意してください。モジュールでは、「ターゲット」マシン (管理ノード) でこの追加要件を満たす必要があります。これについてはモジュール固有のドキュメントに記載されています。

.. \_managed\_node\_requirements:

管理ノードの要件
^^^^^^^^^^^^^^^^^^^^^^^^^

管理ノードでは通信手段が必要です。通常は SSH が使われます。デフォルトでは、
管理ノードの通信に SFTP を使用します。SFTP を使用できない場合は、
:ref:`ansible.cfg <ansible_configuration_settings>` で SCP に切り替えることができます。 Python 2 (バージョン 2.6 以降) または Python 3 (バージョン 3.5 以降) も
必要になります。

.. note::

   * リモートノードで SELinux を有効にしている場合は、
     Ansible でコピー/ファイル/テンプレート関連の機能を使用する前に、libselinux-python をインストールすることもできます。Ansible で、
     :ref:`yum モジュール<yum_module>` または :ref:`dnf モジュール<dnf_module>` を使用して、
     リモートシステムにこのパッケージがインストールされていない場合はインストールできます。

   * デフォルトでは、Ansible は :file:`/usr/bin/python` にある Python インタープリターを使用して、
     そのモジュールを実行します。 ただし、Linux ディストリビューションによっては、
     デフォルトで :file:`/usr/bin/python3` に Python 3 インタープリターしかインストールされていない場合があります。 そのようなシステムでは、以下のようなエラーが表示される場合があります::

        "module_stdout": "/bin/sh: /usr/bin/python:No such file or directory\r\n"

     :ref:`ansible_python_interpreter<ansible_python_interpreter>` インベントリー変数を設定して (
     :ref:`inventory` を参照) インタープリターを指定するか、
     使用するモジュールに Python 2 インタープリターをインストールできます。Python
     2 インタープリターが :command:`/usr/bin/python` にインストールされていない場合にも、:ref:`ansible_python_interpreter<ansible_python_interpreter>` を設定する必要があります。

   * Ansible の:ref:`raw モジュール<raw_module>`、および :ref:`script モジュール<script_module>` は、
     実行する Python をインストールするクライアントに依存しません。 技術的には、
     Ansible で :ref:`raw モジュール<raw_module>` を使用して Python の互換バージョンをインストールできるため、他のものもすべて使用できるようになります。
     たとえば、Python 2 を RHEL ベースのシステムにブートストラップする必要がある場合は、
     以下を使用してインストールできます。

     .. code-block:: shell

        $ ansible myhost --become -m raw -a "yum install -y python2"

.. \_what\_version:

インストールする Ansible バージョンの選択
---------------------------------------

インストールする Ansible バージョンは、特定のニーズに基づいて決定します。Ansible をインストールするには、以下のいずれかの方法を選択できます。

* OS パッケージマネージャー (Red Hat Enterprise Linux (TM)、CentOS、Fedora、Debian、または Ubuntu の場合) を使用して最新リリースをインストールします。
* ``pip`` (Python パッケージマネージャー) でインストールします。
* ソースからインストールして開発 (``devel``) バージョンにアクセスし、最新の機能を開発またはテストします。

.. note::

	Ansible のコンテンツをアクティブに開発している場合は、 ``devel`` からのみ Ansible を実行する必要があります。これは急速に変化するコードのソースであり、いつでも不安定になる可能性があります。


Ansible のリリースは、年に 2 ~ 3 回作成されます。リリースサイクルがこのように短いため、
マイナーバグの場合、通常は安定したブランチでバックポートを管理するのではなく、次のリリースで修正されます。
メジャーバグについては、必要なときにメンテナンスリリースが行われますが、このようなことはあまり頻繁には起こりません。


.. \_installing\_the\_control\_node:
.. \_from\_yum:

RHEL、CentOS、または Fedora への Ansible のインストール
----------------------------------------------

Fedora の場合:

.. code-block:: bash

    $ sudo dnf install ansible

RHEL および CentOS の場合:

.. code-block:: bash

    $ sudo yum install ansible

RHEL 7 および RHEL 8 の RPM は、`Ansible Engine リポジトリー <https://access.redhat.com/articles/3174981>`_ から入手できます。

RHEL 8 用の Ansible Engine リポジトリーを有効にするには、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo subscription-manager repos --enable ansible-2.9-for-rhel-8-x86_64-rpms

RHEL 7 用の Ansible Engine リポジトリーを有効にするには、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo subscription-manager repos --enable rhel-7-server-ansible-2.9-rpms

現在サポートされている RHEL、CentOS、および Fedora のバージョン用の RPM は、`releases.ansible.com <https://releases.ansible.com/ansible/rpm>`_ および `EPEL <https://fedoraproject.org/wiki/EPEL>`_ から入手できます。

Ansible バージョン 2.4 以降では、Python 2.6 以降が含まれている旧オペレーティングシステムを管理できます。

RPM を独自に構築することも可能です。チェックアウトまたは tarball のルートから、``make rpm`` コマンドを使用して、配布およびインストール可能な RPM を構築します。

.. code-block:: bash

    $ git clone https://github.com/ansible/ansible.git
$ cd ./ansible
$ make rpm
$ sudo rpm -Uvh ./rpm-build/ansible-*.noarch.rpm

.. \_from\_apt:

Ubuntu への Ansible のインストール
----------------------------

Ubuntu ビルドは `<https://launchpad.net/~ansible/+archive/ubuntu/ansible> の PPA`_ で利用できます。

自分のマシンに PPA を設定して Ansible をインストールするには、次のコマンドを実行します。

.. code-block:: bash

    $ sudo apt update
$ sudo apt install software-properties-common
$ sudo apt-add-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible

.. note:: 以前の Ubuntu ディストリビューションでは、「software-properties-common」は「python-software-properties」と呼ばれます。過去のバージョンでは ``apt`` ではなく ``apt-get`` を使用するほうがよい場合があります。また、``-u`` あるいは ``--update`` フラグが指定されているのは新しいディストリビューション (例: 18.04、18.10 など) のみなので注意してください。随時、スクリプトは調整してください。

Debian/Ubuntu パッケージは、ソースチェックアウトから構築することもできます。以下を実行します。

.. code-block:: bash

    $ make deb

ソースから実行して開発ブランチを取得することも可能です。この点については以下で説明します。

Debian への Ansible のインストール
----------------------------

Debian を使用されている場合は Ubuntu PPA と同じソースを使用できます。

以下の行を /etc/apt/sources.list に追加します。

.. code-block:: bash

    deb http://ppa.launchpad.net/ansible/ansible/ubuntu trusty main

次に、以下のコマンドを実行します。

.. code-block:: bash

    $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
$ sudo apt update
$ sudo apt install ansible

.. note:: この方法は、Debian Jessie および Stretch の Trusty ソースで検証されていますが、以前のバージョンではサポートされない可能性があります。過去のバージョンでは ``apt`` ではなく ``apt-get`` を使用するほうがよい場合があります。

portage を使用した Gentoo への Ansible のインストール
-----------------------------------------

.. code-block:: bash

    $ emerge -av app-admin/ansible

最新バージョンをインストールするには、出現する前に Ansible パッケージのマスク解除が必要になる場合があります。

.. code-block:: bash

    $ echo 'app-admin/ansible' >> /etc/portage/package.accept_keywords

FreeBSD への Ansible のインストール
-----------------------------

Ansible は Python 2 および 3 の両バージョンで動作しますが、FreeBSD パッケージは各 Python バージョンごとに異なります。
したがって、インストールには、以下を使用できます。

.. code-block:: bash

    $ sudo pkg install py27-ansible

または

.. code-block:: bash

    $ sudo pkg install py36-ansible


ポートからインストールすることもできます。以下を実行します。

.. code-block:: bash

    $ sudo make -C /usr/ports/sysutils/ansible install

特定のバージョン (つまり ``ansible25``) を選択することもできます。

以前のバージョンの FreeBSD は、以下のようなもので動作します (パッケージマネージャーの代わり)。

.. code-block:: bash

    $ sudo pkg install ansible

.. \_on\_macos:

MacOS への Ansible のインストール
---------------------------

Mac に Ansible をインストールするには ``pip`` を使用する方法が推奨されます。

手順は :ref:`from_pip` を参照してください。MacOS バージョン 10.12 以前を実行している場合に、Python Package Index に安全に接続するには最新の ``pip`` にアップグレードする必要があります。

.. \_from\_pkgutil:

Solaris への Ansible のインストール
-----------------------------

Ansible は、`OpenCSW の SysV パッケージ<https://www.opencsw.org/packages/ansible/>`_ として Solaris で利用できます。

.. code-block:: bash

    # pkgadd -d http://get.opencsw.org/now
# /opt/csw/bin/pkgutil -i ansible

.. \_from\_pacman:

Arch Linux への Ansible のインストール
---------------------------------

Ansible はコミュニティーリポジトリーで入手できます::

    $ pacman -S ansible

AUR には、`ansible-git <https://aur.archlinux.org/packages/ansible-git>`_ と呼ばれる GitHub から直接プルするための PKGBUILD があります。

ArchWiki の `Ansible <https://wiki.archlinux.org/index.php/Ansible>`_ ページも参照してください。

.. \_from\_sbopkg:

Slackware Linux への Ansible のインストール
-------------------------------------

Ansible ビルドスクリプトは `SlackBuilds.org <https://slackbuilds.org/apps/ansible/>`_ リポジトリーで入手できます。
`sbopkg <https://sbopkg.org/>` を使用してビルドし、インストールできます。

Ansible およびすべての依存関係を含むキューを作成します::

    # sqg -p ansible

作成した queuefile からパッケージを構築してインストールします (sbopkg がキューまたはパッケージを使用する必要がある場合の問題への回答 Q)::

    # sbopkg -k -i ansible

.. \_from swupd:

Clear Linux への Ansible のインストール
---------------------------------

Ansible およびその依存関係は、sysadmin ホスト管理バンドルの一部として利用できます::

    $ sudo swupd bundle-add sysadmin-hostmgmt

ソフトウェアの更新は、swupd ツールにより管理されます::

   $ sudo swupd update

.. \_from\_pip:

``pip`` を使用した Ansible のインストール
--------------------------------

Ansible は、Python パッケージマネージャー ``pip`` を使用してインストールできます。 Python のシステムに ``pip`` がまだない場合には、以下のコマンドを実行してインストールします::

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py --user

次に Ansible \[1]_ をインストールします::

    $ pip install --user ansible

または、開発バージョンを探している場合は、以下を実行します::

    $ pip install --user git+https://github.com/ansible/ansible.git@devel

MacOS Mavericks (10.9) にインストールしている場合は、コンパイラーにノイズが発生する可能性があります。回避するには以下を実行します::

    $ CFLAGS=-Qunused-arguments CPPFLAGS=-Qunused-arguments pip install --user ansible

``paramiko`` を必要とする ``paramiko`` 接続プラグインまたはモジュールを使用するには、必要なモジュール \[2]_ をインストールします::

    $ pip install --user paramiko

Ansible は、新規または既存の ``virtualenv`` 内にもインストールできます::

    $ python -m virtualenv ansible  # Create a virtualenv if one does not already exist
$ source ansible/bin/activate   # Activate the virtual environment
$ pip install ansible

Ansible をグローバルにインストールする場合は、以下のコマンドを実行します::

    $ sudo python get-pip.py
$ sudo pip install ansible

.. note::

    「sudo」を付けて「pip」を実行すると、システムにグローバルな変更が加えられます。「pip」はシステムパッケージマネージャーとは連携しないため、これが原因でシステムに変更が加えられ、不整合状態または不機能状態のままになる可能性があります。特に、これは MacOS の場合に当てはまります。システムのグローバルファイルの修正による影響を十分に理解していない場合には、「-user」を使用してインストールするようお推めします。

.. note::

    以前のバージョンの「pip」でのデフォルトは http://pypi.python.org/simple ですが、これはもう機能しません。
    Ansible をインストールする前に、最新バージョンの「pip」を使用していることを確認してください。
    古いバージョンの「pip」がインストールされている場合は、以下の「pip のアップグレードの説明 <https://pip.pypa.io/en/stable/installing/#upgrading-pip>_」 
 に従ってアップグレードできます。


.. \_from\_source:

ソース (devel) からの Ansible の実行
-----------------------------------

.. note::

	Ansible のコンテンツをアクティブに開発している場合は、 ``devel`` からのみ Ansible を実行する必要があります。これは急速に変化するコードのソースであり、いつでも不安定になる可能性があります。

Ansible は、ソースから簡単に実行できます。これを使用するのに ``root`` 権限は必要ありません。
実際にインストールするソフトウェアはありません。デーモンや、
データベースの設定も必要ありません。

.. note::

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

誤った警告やエラーが表示されないようにするには、以下を使用します::

    $ source ./hacking/env-setup -q

お使いのバージョンの Python に ``pip`` がインストールされていない場合は、インストールします::

    $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
$ python get-pip.py --user

Ansible は、インストールする必要がある以下の Python モジュールも使用します \[1]\_:

.. code-block:: bash

    $ pip install --user -r ./requirements.txt

Ansible チェックアウトを更新するには、pull-with-rebase を使用してローカルの変更がリプレイされるようにします。

.. code-block:: bash

    $ git pull --rebase

.. code-block:: bash

    $ git pull --rebase #same as above
$ git submodule update --init --recursive

env-setup スクリプトを実行すると、実行がチェックアウトから行われ、
デフォルトのインベントリーファイルが ``/etc/ansible/hosts`` になります。必要に応じて、``/etc/ansible/hosts`` 以外のインベントリーファイルを指定できます (:ref:`インベントリー` を参照)。


.. code-block:: bash

    $ echo "127.0.0.1" > ~/ansible_hosts
$ export ANSIBLE_INVENTORY=~/ansible_hosts

インベントリーファイルの詳細は、「:ref:`インベントリー`」を参照してください。

では、ping コマンドを使ってテストしていきましょう。

.. code-block:: bash

    $ ansible all -m ping --ask-pass

「sudo make install」も使用できます。

.. \_tagged\_releases:

タグ付けされたリリースの tarball の場所
-----------------------------------

git チェックアウトせずに、Ansible をパッケージ化したり、ローカルパッケージをご自身で構築する場合があります。 リリースの tarball は、`Ansible downloads <https://releases.ansible.com/ansible>`_ ページで入手できます。

リリースは、`git repository` <https://github.com/ansible/ansible/releases>_ でリリースバージョンのタグが付けされています。


.. \_shell\_completion:

Ansible コマンドシェルの完了
--------------------------------

Ansible 2.9 では、Ansible コマンドラインユーティリティーのシェル補完が利用でき、
``argcomplete`` と呼ばれる任意の依存関係により提供されます。``argcomplete`` は bash に対応し、zsh と tcsh のサポートは限定されています。

``python-argcomplete`` は、Red Hat Enterprise ベースのディストリビューションでは EPEL からインストールでき、その他の多くのディストリビューションでは標準 OS リポジトリーで入手できます。

インストールと設定の詳細は、「`argcomplete のドキュメント <https://argcomplete.readthedocs.io/en/latest/>`\_」を参照してください。

RHEL、CentOS、または Fedora への ``argcomplete`` のインストール
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fedora の場合:

.. code-block:: bash

    $ sudo dnf install python-argcomplete

RHEL および CentOS の場合:

.. code-block:: bash

    $ sudo yum install epel-release
$ sudo yum install python-argcomplete


``apt`` を使用した ``argcomplete`` のインストール
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ sudo apt install python-argcomplete


``pip`` を使用した ``argcomplete`` のインストール
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ pip install argcomplete

``argcomplete`` の設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ansible コマンドラインユーティリティーのシェル補完を可能にする ``argcomplete`` の設定方法は、2 通りあります。

グローバル
"""""""""

グローバル補完には bash 4.2 が必要です。

.. code-block:: bash

    $ sudo activate-global-python-argcomplete

これにより、bash 補完ファイルがグローバルの場所に書き込まれます。``--dest`` を使用してロケーションを変更します。

コマンド単位
"""""""""""

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

上記のコマンドは、``~/.profile``、``~/.bash_profile`` などのシェルプロファイルファイルに置くことが推奨されます。

zsh または tcsh での``argcomplete``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`argcomplete ドキュメント <https://argcomplete.readthedocs.io/en/latest/>`_ を参照してください。

.. \_getting\_ansible:

GitHub 上の Ansible
-----------------

以下の場合は、`GitHub プロジェクト<https://github.com/ansible/ansible>`_ をフォローすることもできます。
GitHub アカウントがある。このプロジェクトは、
バグおよび機能に関する意見を共有するための問題トラッカーが保持されている場所でもあります。


.. seealso::

   :ref:`intro_adhoc`
       基本コマンドの例
   :ref:`working_with_playbooks`
       Ansible の設定管理言語について
   :ref:`installation_faqs`
       FAQ に関連する Ansible インストール
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       \#ansible IRC chat channel

..\[1] MacOS への「pycrypto」パッケージのインストールに問題がある場合は、``CC=clang sudo -E pip install pycrypto`` を試す必要がある場合があります。
.. 2.8 よりも前の Ansible の ``requirements.txt`` には、\[2] ``paramiko`` が含まれていました。
