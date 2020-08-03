.. _using_galaxy:
.. _ansible_galaxy:

*****************
Galaxy ユーザーガイド
*****************

:dfn:`Ansible Galaxy` は、コミュニティーが開発したロールの検索、ダウンロード、共有を行う無料サイトである `Galaxy <https://galaxy.ansible.com>`_ の Web サイトを指します。

Galaxy を使用して、Ansible コミュニティーの優れたコンテンツで自動化プロジェクトを活性化させます。Galaxy は `ロール <playbooks_reuse_roles>`_ などの事前にパッケージ化された作業単位を提供し、Galaxy 3.2 では `コレクション <collections>`_ が新たに提供されました。
インフラストラクチャーのプロビジョニング、アプリケーションのデプロイ、および日々の作業を行うすべてのタスクにロールがあります。コレクション形式は、複数の Playbook、ロール、モジュール、およびプラグインが含まれる可能性のある自動化の包括的なパッケージを提供します。

.. contents::
   :local:
   :depth: 2
.. _finding_galaxy_collections:

Galaxy でコレクションの検索
=============================

Galaxy でコレクションを検索するには、以下を行います。

#. 左側のナビゲーションにある :guilabel:`検索` アイコンをクリックします。
#. *コレクション* にフィルターを設定します。
#. その他のフィルターを設定し、:guilabel:`Enter` を押します。

Galaxy は、検索条件に一致するコレクションのリストを表示します。

.. _installing_galaxy_collections:


コレクションのインストール
======================


Galaxy からコレクションのインストール
-----------------------------------

.. include:: ../shared_snippets/installing_collections.txt

.. _installing_ah_collection:

Automation Hub からのコレクションのダウンロード
----------------------------------------------------

``ansible-galaxy`` コマンドで Automation Hub からコレクションをダウンロードするには、以下を行います。

1. Automation Hub API トークンを取得します。https://cloud.redhat.com/ansible/automation-hub/token/ にアクセスし、バージョンのドロップダウンから :guilabel:`Get API token` をクリックして、API トークンをコピーします。
2. :file:`ansible.cfg` ファイルの ``[galaxy]`` セクションの下にある ``server_list`` オプションで Red Hat Automation Hub サーバーを設定します。

  .. code-block:: ini

      [galaxy]
      server_list = automation_hub

      [galaxy_server.automation_hub]
      url=https://cloud.redhat.com/api/automation-hub/
      auth_url=https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
      token=my_ah_token

3. Automation Hub でホストされるコレクションをダウンロードします。

  .. code-block:: bash

     ansible-galaxy collection install my_namespace.my_collection

.. seealso::
  `Automation Hub の使用 <https://www.ansible.com/blog/getting-started-with-ansible-hub>`_
    Automation Hub の概要

古いバージョンのコレクションのインストール
-------------------------------------------

.. include:: ../shared_snippets/installing_older_collection.txt

要件ファイルを使用した複数のコレクションのインストール
-----------------------------------------------------

.. include:: ../shared_snippets/installing_multiple_collections.txt


``ansible-galaxy`` クライアントの設定
------------------------------------------

.. include:: ../shared_snippets/galaxy_server_list.txt

.. _finding_galaxy_roles:

Galaxy でのロールの検索
=======================

Galaxy データベースは、タグ、プラットフォーム、作成者、および複数のキーワードで検索します。たとえば、以下のようになります。

.. code-block:: bash

    $ ansible-galaxy search elasticsearch --author geerlingguy

search コマンドは、検索に一致する最初の 1000 個の結果を一覧で返します。

.. code-block:: text

    Found 2 roles matching your search:

    Name                              Description
    ----                              -----------
    geerlingguy.elasticsearch         Elasticsearch for Linux.
    geerlingguy.elasticsearch-curator Elasticsearch curator for Linux.


ロールに関する詳細情報の取得
---------------------------------

``info`` コマンドを使用して、特定のロールに関する詳細を表示します。

.. code-block:: bash

    $ ansible-galaxy info username.role_name

これは、ロールの Galaxy にあるすべてのものを返します。

.. code-block:: text

    Role: username.role_name
        description: Installs and configures a thing, a distributed, highly available NoSQL thing.
        active: True
        commit: c01947b7bc89ebc0b8a2e298b87ab416aed9dd57
        commit_message: Adding travis
        commit_url: https://github.com/username/repo_name/commit/c01947b7bc89ebc0b8a2e298b87ab
        company: My Company, Inc.
        created: 2015-12-08T14:17:52.773Z
        download_count: 1
        forks_count: 0
        github_branch:
        github_repo: repo_name
        github_user: username
        id: 6381
        is_valid: True
        issue_tracker_url:
        license: Apache
        min_ansible_version: 1.4
        modified: 2015-12-08T18:43:49.085Z
        namespace: username
        open_issues_count: 0
        path: /Users/username/projects/roles
        scm: None
        src: username.repo_name
        stargazers_count: 0
        travis_status_url: https://travis-ci.org/username/repo_name.svg?branch=master
        version:
        watchers_count: 1


.. _installing_galaxy_roles:

Galaxy からのロールのインストール
============================

``ansible-galaxy`` コマンドが Ansible にバンドルされており、これを使用して Galaxy からロールをインストールするか、または git ベースの SCM から直接ロールをインストールすることができます。また、
これを使用して、Galaxy の Web サイトで新しいロールの作成、ロールの削除、またはタスクの実行を行います。

デフォルトでは、コマンドラインツールはサーバーアドレス *https://galaxy.ansible.com* を使用して Galaxy Web サイト API と通信します。`Galaxy プロジェクト<https://github.com/ansible/galaxy>`_ はオープンソースプロジェクトであるため、
独自の内部 Galaxy サーバーを実行し、デフォルトのサーバーアドレスを上書きしたい場合があります。この場合は、*--server* オプションを使用できます。
または、*ansible.cfg* ファイルで Galaxy サーバー値を設定して行います。*ansible.cfg* の値を設定する方法は、「:ref:`galaxy_server`」を参照してください。


ロールのインストール
----------------

``ansible-galaxy`` コマンドを使用して、`Galaxy の Web サイト<https://galaxy.ansible.com>`_ からロールをダウンロードします。

.. code-block:: bash

  $ ansible-galaxy install namespace.role_name

ロールをインストールする場所の設定
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

デフォルトでは、Ansible はパスのデフォルトリスト ``~/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles`` にあるディレクトリーで、最初に書き込み可能なディレクトリーにロールをダウンロードします。これは、``ansible-galaxy`` を実行しているユーザーのホームディレクトリーにロールをインストールします。

これは、以下のオプションのいずれかで上書きできます。

* セッション内に環境変数 :envvar:`ANSIBLE_ROLES_PATH` を設定します。
* ``ansible.cfg`` ファイルに ``roles_path`` を定義します。
* ``ansible-galaxy`` コマンドに ``--roles-path`` オプションを使用します。

以下は、``--roles-path`` を使用して現在の作業ディレクトリーにロールをインストールする例を示しています。

.. code-block:: bash

    $ ansible-galaxy install --roles-path . geerlingguy.apache

.. seealso::

   :ref:`intro_configuration`
      設定ファイルに関するすべて

ロールの特定バージョンのインストール
---------------------------------------

Galaxy サーバーがロールをインポートする場合は、Sandmantic Version 形式に一致する git タグをバージョンとしてインポートします。その後、インポートされたタグのいずれかを指定して、特定バージョンのロールをダウンロードできます。

ロールで利用可能なバージョンを表示するには、以下を行います。

#. Galaxy 検索ページでロールを検索します。
#. 名前をクリックして、利用可能なバージョンなどの詳細を表示します。

/<namespace>/<role name> を使用してロールに直接移動することもできます。たとえば、geerlingguy.apache ロールを表示するには、`<https://galaxy.ansible.com/geerlingguy/apache>`_ にアクセスします。

Galaxy から特定のバージョンのロールをインストールするには、コンマと GitHub リリースタグの値を追加します。たとえば、以下のようになります。

.. code-block:: bash

   $ ansible-galaxy install geerlingguy.apache,v1.0.0

git リポジトリーを直接指定し、ブランチ名またはコミットハッシュをバージョンとして指定することもできます。たとえば、次のコマンドは、
特定のコミットをインストールします。

.. code-block:: bash

   $ ansible-galaxy install git+https://github.com/geerlingguy/ansible-role-apache.git,0b7cd353c0250e87a26e0499e59e7fd265cc2f25

ファイルからの複数ロールのインストール
-------------------------------------

:file:`requirements.yml` ファイルにロールを追加して、複数のロールをインストールできます。ファイルのフォーマットは YAML で、
ファイル拡張子は *.yml* または *.yaml* のいずれかにする必要があります。

以下のコマンドを使用して、:file:`requirements.yml:` に含まれるロールをインストールします。

.. code-block:: bash

    $ ansible-galaxy install -r requirements.yml

ここでも、拡張機能は重要です。*.yml* 拡張を省略すると、``ansible-galaxy`` CLI は、ファイルが古い (現在は非推奨な)、
基本的な形式であると見なします。

このファイルの各ロールには、以下の属性が 1 つ以上あります。

   src
     ロールのソース。Galaxy からダウンロードする場合は *namespace.role_name* 形式を使用します。
     それ以外の場合は、git ベースの SCM 内のリポジトリーを指定する URL を指定します。以下の例を参照してください。これは必須の属性です。
   scm
     SCM を指定します。本ガイドの執筆中は、*git* または *hg* のみが許可されています。以下の例を参照してください。デフォルトは *git* です。
   version:
     ダウンロードするロールのバージョン。リリースタグの値、コミットハッシュ、またはブランチ名を指定します。デフォルトは、リポジトリーでデフォルトとして設定されたブランチに設定されます。それ以外の場合は *master* にデフォルト設定されます。
   name:
     ロールを特定の名前にダウンロードします。Galaxy からダウンロードする場合にデフォルトは Galaxy 名に設定されます。
     それ以外の場合は、リポジトリーの名前がデフォルトになります。

以下の例を、*requirements.yml* でロールを指定するためのガイドとして使用してください。

.. code-block:: yaml

    # from galaxy
    - name: yatesr.timezone

    # from GitHub
    - src: https://github.com/bennojoy/nginx

    # from GitHub, overriding the name and specifying a specific tag
    - name: nginx_role
      src: https://github.com/bennojoy/nginx
      version: master

    # from a webserver, where the role is packaged in a tar.gz
    - name: http-role-gz
      src: https://some.webserver.example.com/files/master.tar.gz

    # from a webserver, where the role is packaged in a tar.bz2
    - name: http-role-bz2
      src: https://some.webserver.example.com/files/master.tar.bz2

    # from a webserver, where the role is packaged in a tar.xz (Python 3.x only)
    - name: http-role-xz
      src: https://some.webserver.example.com/files/master.tar.xz

    # from Bitbucket
    - src: git+https://bitbucket.org/willthames/git-ansible-galaxy
      version: v1.4

    # from Bitbucket, alternative syntax and caveats
    - src: https://bitbucket.org/willthames/hg-ansible-galaxy
      scm: hg

    # from GitLab or other git-based scm, using git+ssh
    - src: git@gitlab.company.com:mygroup/ansible-base.git
      scm: git
      version: "0.1"  # quoted, so YAML doesn't parse this as a floating-point value

同じ requirements.yml ファイルからのロールおよびコレクションのインストール
---------------------------------------------------------------------

同じ要件ファイルからロールとコレクションをインストールできますが、いくつか注意点があります。

.. code-block:: yaml

    ---
    roles:
      # Install a role from Ansible Galaxy.
      - name: geerlingguy.java
        version: 1.9.6

    collections:
      # Install a collection from Ansible Galaxy.
      - name: geerlingguy.php_roles
        version: 0.9.3
        source: https://galaxy.ansible.com

.. note::
   ロールとコレクションの両方を 1 つの要件ファイルで指定できますが、個別にインストールする必要があります。
   ``ansible-galaxy role install -r requirements.yml`` はロールのみをインストールし、``ansible-galaxy collection install -r requirements.yml -p ./`` はコレクションのみをインストールします。

複数のファイルからの複数ロールのインストール
---------------------------------------------

大規模なプロジェクトの場合、:file:`requirements.yml` ファイルの ``include`` ディレクティブにより、大きなファイルを複数の小さなファイルに分割できます。

たとえば、プロジェクトに :file:`requirements.yml` ファイルと :file:`webserver.yml` ファイルが含まれるとします。

:file:`webserver.yml` ファイルの内容は次のとおりです。

.. code-block:: bash

    # from github
    - src: https://github.com/bennojoy/nginx

    # from Bitbucket
    - src: git+http://bitbucket.org/willthames/git-ansible-galaxy
      version: v1.4

以下は、:file:`webserver.yml` ファイルが含まれる :file:`requirements.yml` ファイルの内容を示しています。

.. code-block:: bash

  # from galaxy
  - name: yatesr.timezone
  - include: <path_to_requirements>/webserver.yml

両方のファイルから全ロールをインストールするには、root ファイルを渡します (この場合、コマンドラインの :file:`requirements.yml` は、
以下のようになります。

.. code-block:: bash

    $ ansible-galaxy install -r requirements.yml

.. _galaxy_dependencies:

依存関係
------------

また、ロールは他のロールに依存し、依存関係のあるロールをインストールすると、それらの依存関係が自動的にインストールされます。

ロールの一覧を指定して、``meta/main.yml`` ファイルにロール依存関係を指定します。ロールのソースが Galaxy の場合は、
``namespace.role_name`` 形式のロールのみを指定できます。``requirements.yml`` でより複雑な形式を使用し、``src``、``scm``、``version``、および ``name`` を指定することもできます。

以下は、依存するロールを持つ ``meta/main.yml`` ファイルの例になります。

.. code-block:: yaml

    ---
    dependencies:
      - geerlingguy.java

    galaxy_info:
      author: geerlingguy
      description: Elasticsearch for Linux.
      company: "Midwestern Mac, LLC"
      license: "license (BSD, MIT)"
      min_ansible_version: 2.4
      platforms:
      - name: EL
        versions:
        - all
      - name: Debian
        versions:
        - all
      - name: Ubuntu
        versions:
        - all
      galaxy_tags:
        - web
        - system
        - monitoring
        - logging
        - lucene
        - elk
        - elasticsearch

タグは、依存関係チェーンを介して*継承* されます。タグをロールおよびそのすべての依存関係に適用するには、タグをロール内のすべてのタスクに適用せずに、ロールに適用する必要があります。

依存関係として一覧表示されるロールは、条件およびタグのフィルタリングの対象となり、
適用されているタグや条件によっては、完全には実行されない場合があります。

ロールのソースが Galaxy の場合は、ロールを *namespace.role_name* 形式で指定します。

.. code-block:: yaml

    dependencies:
      - geerlingguy.apache
      - geerlingguy.ansible


または、以下のように :file:`requirements.yml` で使用される複雑な形式でロールの依存関係を指定することもできます。

.. code-block:: yaml

    dependencies:
      - name: geerlingguy.ansible
      - name: composer
        src: git+https://github.com/geerlingguy/ansible-role-composer.git
        version: 775396299f2da1f519f0d8885022ca2d6ee80ee8

``ansible-galaxy`` で依存関係が発生すると、各依存関係が ``roles_path`` に自動的にインストールされます。プレイの実行中に依存関係がどのように処理されるかを理解するには、「:ref:`playbooks_reuse_roles`」を参照してください。

.. note::

    Galaxy は、すべてのロールの依存関係が Galaxy に存在することを想定しているため、
    依存関係は ``namespace.role_name`` 形式で指定されます。``src`` の値が URL である依存関係でロールをインポートすると、インポートプロセスに失敗します。

インストール済みロールの一覧表示
--------------------

``list`` を使用して、*roles_path* にインストールされている各ロールの名前およびバージョンを表示します。

.. code-block:: bash

    $ ansible-galaxy list
      - ansible-network.network-engine, v2.7.2
      - ansible-network.config_manager, v2.6.2
      - ansible-network.cisco_nxos, v2.7.1
      - ansible-network.vyos, v2.7.3
      - ansible-network.cisco_ios, v2.7.0

インストールされたロールの削除
------------------------

``remove`` を使用してロールを *roles_path* から削除します。

.. code-block:: bash

    $ ansible-galaxy remove namespace.role_name


.. seealso::
  :ref:`collections`
    モジュール、Playbook、およびロールの共有可能なコレクション
  :ref:`playbooks_reuse_roles`
    既知のディレクトリー構造の再利用可能なタスク、ハンドラー、およびその他のファイル
