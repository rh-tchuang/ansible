.. _intro_adhoc:

*******************************
アドホックコマンドの概要
*******************************

Ansible アドホックコマンドは `/usr/bin/ansible` コマンドラインツールを使用して、1 つのタスクを 1 つ以上の管理ノードで自動化します。アドホックコマンドは迅速かつ簡単ですが、再利用できません。では、なぜアドホックコマンドについて最初に学ぶのでしょうか。アドホックコマンドは、Ansible の単純さおよび能力を示しています。ここで学習する概念は、Playbook 言語に直接移植されます。紹介される例を読んで実行する前に、:ref:`intro_inventory` をお読みください。

.. contents::
   :local:

アドホックコマンドを使用する理由
========================

アドホックコマンドは、めったに繰り返さないタスクに最適です。たとえば、クリスマス休暇中にラボのマシンの電源をすべてオフにする場合は、Playbook を作成しないで、Ansible で 1 行の簡単なコマンドを実行できます。アドホックコマンドは以下のようになります。

.. code-block:: bash

    $ ansible [pattern] -m [module] -a "[module options]"

他のページで、:ref:`パターン<intro_patterns>` や :ref:`モジュール<working_with_modules>` の詳細を確認できます。

アドホックタスクのユースケース
==========================

アドホックタスクは、サーバーの再起動、ファイルのコピー、パッケージとユーザーの管理などに使用できます。アドホックタスクでは、Ansible モジュールを使用できます。Playbook などのアドホックタスクは宣言型モデルを使用して、
指定された最終状態に到達するのに必要なアクションを計算して実行します。アドホックタスクは、
開始する前に現在の状態を確認し、現在の状態が指定された最終状態と同じ場合は何も実行しない冪等性の形式を実現します。

サーバーの再起動
-----------------

``ansible`` コマンドラインユーティリティーのデフォルトモジュールは、:ref:`command モジュール<command_module>` です。アドホックタスクを使用してコマンドモジュールを呼び出し、アトランタにあるすべての Web サーバーを一度に 10 台ずつ再起動できます。Ansible がこれを行うには、アトランタのすべてのサーバーを、インベントリー内の [atlanta] グループにリストし、そのグループの各マシンの SSH 資格情報が有効である必要があります。[atlanta] グループの全サーバーを再起動するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible atlanta -a "/sbin/reboot"

デフォルトでは、Ansible は 5 つの同時プロセスのみを使用します。ホストの数が、フォーク数に設定された値よりも多い場合、Ansible はそのホストと通信しますが、少し時間がかかります。10 個の並列フォークで [atlanta] サーバーを再起動するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible atlanta -a "/sbin/reboot" -f 10

/usr/bin/ansible はデフォルトでユーザーアカウントから実行されます。別のユーザーで接続するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible atlanta -a "/sbin/reboot" -f 10 -u username

再起動には、おそらく権限昇格が必要です。``username`` としてサーバーに接続し、:ref:`become <become>` キーワードを使用して ``root`` でそのコマンドを実行します。

.. code-block:: bash

    $ ansible atlanta -a "/sbin/reboot" -f 10 -u username --become [--ask-become-pass]

``--ask-become-pass`` または ``-K`` を追加します。Ansible により、権限昇格に使用するパスワード (sudo/su/pfexec/doas/etc) の入力が求められます。

.. note::
   :ref:`コマンドモジュール <command_module>` は、
   piping や redirects などの拡張シェル構文に対応していません (ただし、シェル変数は常に機能します)。コマンドにシェル固有の構文が必要な場合は、
   代わりに `shell` モジュールを使用してください。相違点の詳細は、
   :ref:`working_with_modules` を参照してください。

これまでの例ではすべて、デフォルトの「command」モジュールを使用しています。別のモジュールを使用するには、モジュール名に ``-m`` を渡します。たとえば、:ref:`shell モジュール<shell_module>` を使用するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible raleigh -m shell -a 'echo $TERM'

(:ref:`Playbooks <working_with_playbooks>` ではなく) Ansible アドホック CLI でコマンドを実行する場合は、
シェル引用ルールに特に注意してください。
これにより、ローカルシェルは変数を保持し、Ansible に渡します。
たとえば、上記の例で一重引用符ではなく二重引用符を使用すると、
指定しているそのボックスの変数が評価されます。

.. _file_transfer:

ファイルの管理
--------------

アドホックタスクでは、Ansible および SCP の機能を利用して、多くのファイルを複数のマシンに並行して転送できます。[atlanta] グループ内の全サーバーに直接ファイルを転送するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible atlanta -m copy -a "src=/etc/hosts dest=/tmp/hosts"

このようなタスクを繰り返す場合は、Playbook で :ref:`template<template_module>` モジュールを使用します。

:ref:`file<file_module>` モジュールにより、ファイルの所有者および権限を変更できます。同じオプションを
``copy`` モジュールに直接渡すこともできます。

.. code-block:: bash

    $ ansible webservers -m file -a "dest=/srv/foo/a.txt mode=600"
    $ ansible webservers -m file -a "dest=/srv/foo/b.txt mode=600 owner=mdehaan group=mdehaan"

``file`` モジュールは、``mkdir -p`` と同様、ディレクトリーも作成できます。

.. code-block:: bash

    $ ansible webservers -m file -a "dest=/path/to/c mode=755 owner=mdehaan group=mdehaan state=directory"

ディレクトリーを (再帰的に) 削除し、ファイルを削除します。

.. code-block:: bash

    $ ansible webservers -m file -a "dest=/path/to/c state=absent"

.. _managing_packages:

パッケージの管理
-----------------

アドホックタスクを使用して、yum などのパッケージ管理モジュールを使用して、管理ノードにパッケージをインストール、更新、または削除することもできます。パッケージを更新せずにインストールするには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible webservers -m yum -a "name=acme state=present"

パッケージの特定バージョンがインストールされていることを確認するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible webservers -m yum -a "name=acme-1.5 state=present"

パッケージが最新バージョンであることを確認するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible webservers -m yum -a "name=acme state=latest"

パッケージがインストールされていないことを確認するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible webservers -m yum -a "name=acme state=absent"

Ansible には、多くのプラットフォームでパッケージを管理するためのモジュールがあります。パッケージマネージャーのモジュールがない場合は、コマンドモジュールを使用してパッケージをインストールするか、パッケージマネージャーのモジュールを作成できます。

.. _users_and_groups:

ユーザーおよびグループの管理
-------------------------

アドホックタスクを使用すると、管理ノードでユーザーアカウントを作成、管理、および削除できます。

.. code-block:: bash

    $ ansible all -m user -a "name=foo password=<crypted password here>"

    $ ansible all -m user -a "name=foo state=absent"

グループやグループメンバーシップの操作方法など、利用可能なすべてのオプションの詳細は、
:ref:`user <user_module>` モジュールのドキュメントを参照してください。

.. _managing_services:

サービスの管理
-----------------

サービスがすべての Web サーバーで起動していることを確認します。

.. code-block:: bash

    $ ansible webservers -m service -a "name=httpd state=started"

または、すべての Web サーバーでサービスを再起動します。

.. code-block:: bash

    $ ansible webservers -m service -a "name=httpd state=restarted"

サービスが停止していることを確認します。

.. code-block:: bash

    $ ansible webservers -m service -a "name=httpd state=stopped"

.. _gathering_facts:

ファクトの収集
---------------

ファクトは、検出されたシステムに関する変数を表します。ファクトを使用して、タスクの条件付き実行を実装することもできますが、システムに関するアドホック情報を取得することもできます。すべてのファクトを表示するには、次のコマンドを実行します。

.. code-block:: bash

    $ ansible all -m setup

この出力をフィルターで絞り込んで、特定のファクトのみを表示することもできます。詳細は :ref:`setup <setup_module>` モジュールのドキュメントを参照してください。

これで、Ansible を実行する基本要素を理解できたので、:ref:`Ansible Playbook<playbooks_intro>` を使用して反復タスクを自動化する方法を学ぶ準備が整いました。

.. seealso::

   :ref:`intro_configuration`
       Ansible 設定ファイルの詳細
   :ref:`all_modules`
       利用可能なモジュールの一覧
   :ref:`working_with_playbooks`
       設定管理およびデプロイメントに Ansible の使用
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
