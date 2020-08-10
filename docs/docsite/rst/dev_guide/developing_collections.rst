
.. _developing_collections:

**********************
コレクションの開発
**********************


コレクションは、Ansible コンテンツのディストリビューション形式です。コレクションを使用して Playbook、ロール、モジュール、プラグインをパッケージ化および配布できます。
`Ansible Galaxy` <https://galaxy.ansible.com>_ を使用してコレクションを公開および使用できます。

.. contents::
   :local:
   :depth: 2

.. _collection_structure:

コレクション構造
====================

コレクションは、単純なデータ構造に従います。いずれかのディレクトリーに属する特定のコンテンツがない場合は、いずれのディレクトリーも不要です。コレクションには、コレクションのルートレベルでの ``galaxy.yml`` ファイルが必要です。このファイルには、
Galaxy などのツールがコレクションをパッケージ化、構築、公開するのに必要なメタデータがすべて含まれています。

    collection/
    ├── docs/
    ├── galaxy.yml
    ├── plugins/
    │   ├── modules/
    │   │   └── module1.py
    │   ├── inventory/
    │   └── .../
    ├── README.md
    ├── roles/
    │   ├── role1/
    │   ├── role2/
    │   └── .../
    ├── playbooks/
    │   ├── files/
    │   ├── vars/
    │   ├── templates/
    │   └── tasks/
    └── tests/


.. note::
    * Ansible では、:file:`README` ファイルおよび :file:`/docs` フォルダー内のファイルでは、:file:`galaxy.yml` の ``.yml`` 拡張子のみが許可されます。
    * 完全なコレクション構造の例は、「`ドラフト コレクション<https://github.com/bcoca/collection>`_」を参照してください。
    * 現在すべてのディレクトリーが使用されているわけではありません。これらは今後の機能のプレースホルダーになります。

.. _galaxy_yml:

galaxy.yml
----------

コレクションには、コレクションアーティファクトのビルドに必要な情報が含まれる ``galaxy.yml`` ファイルが必要です。
詳細は、「:ref:`collections_galaxy_meta`」を参照してください。

.. _collections_doc_dir:

ドキュメンテーションディレクトリー
---------------

コレクションの一般的なドキュメントをここに置きます。Python docstring として埋め込まれたプラグインおよびモジュールの特定のドキュメントを保持します。``docs`` フォルダーを使用して、コレクションが提供するロールおよびプラグイン、ロール要件などを使用する方法を記述します。マークダウンを使用し、サブフォルダーは追加しません。

``ansible-doc`` を使用して、コレクション内のプラグインのドキュメントを表示します。

.. code-block:: bash

    ansible-doc -t lookup my_namespace.my_collection.lookup1

``ansible-doc`` コマンドでは、特定のプラグインのドキュメントを表示するために、完全修飾コレクション名 (FQCN) が必要です。この例では、``my_namespace`` は名前空間で、``my_collection`` はその名前空間内のコレクション名です。

.. note:: Ansible コレクションの名前空間は、``galaxy.yml`` ファイルで定義され、GitHub リポジトリー名と同等ではありません。

.. _collections_plugin_dir:

プラグインディレクトリー
------------------

モジュールだけでなく、FQCN を使用してほとんどのプラグインで使用可能な ``module_utils`` を含め、「プラグインタイプ別」の固有のサブディレクトリーを追加します。これは、すべてのプレイにロールをインポートしなくても、モジュール、検索、フィルターなどを配布する方法です。

VCS プラグインはコレクションではサポートされていません。キャッシュプラグインは、ファクトキャッシュのコレクションで使用できますが、インベントリープラグインではサポートされていません。

module_utils
^^^^^^^^^^^^

コレクションで ``module_utils`` を使用してコーディングする場合、Python の ``import`` ステートメントは、``ansible_collections`` 規則と FQCN を共に考慮する必要があります。生成される Python インポートは、``from ansible_collections.{namespace}.{collection}.plugins.module_utils.{util} import {something}`` のようになります。

デフォルトの Ansible ``module_utils`` とコレクションから提供されるものを使用した、
Python および PowerShell モジュールを示します。この例では、名前空間は ``ansible_example`` で、コレクションは ``community`` です。
Python の例では、問題の ``module_util`` が ``qradar`` と呼ばれ、
FQCN は ``ansible_example.community.plugins.module_utils.qradar`` となります。

.. code-block:: python

    from ansible.module_utils.basic import AnsibleModule
    from ansible.module_utils._text import to_text

    from ansible.module_utils.six.moves.urllib.parse import urlencode, quote_plus
    from ansible.module_utils.six.moves.urllib.error import HTTPError
    from ansible_collections.ansible_example.community.plugins.module_utils.qradar import QRadarRequest

    argspec = dict(
        name=dict(required=True, type='str'),
        state=dict(choices=['present', 'absent'], required=True),
    )

    module = AnsibleModule(
        argument_spec=argspec,
        supports_check_mode=True
    )

    qradar_request = QRadarRequest(
        module,
        headers={"Content-Type": "application/json"},
        not_rest_data_keys=['state']
    )

``__init__.py`` ファイルから何かをインポートするには、ファイル名を使用する必要があります。

.. code-block:: python

    from ansible_collections.namespace.collection_name.plugins.callback.__init__ import CustomBaseClass

PowerShell の例では、問題の ``module_util`` は ``hyperv`` となり、
FCQN は ``ansible_example.community.plugins.module_utils.hyperv`` となります。

.. code-block:: powershell

    #!powershell
    #AnsibleRequires -CSharpUtil Ansible.Basic
    #AnsibleRequires -PowerShell ansible_collections.ansible_example.community.plugins.module_utils.hyperv

    $spec = @{
        name = @{ required = $true; type = "str" }
        state = @{ required = $true; choices = @("present", "absent") }
    }
    $module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

    Invoke-HyperVFunction -Name $module.Params.name

    $module.ExitJson()
    
.. _collections_roles_dir:

roles ディレクトリー
----------------

コレクションロールは既存ロールとほぼ同じですが、いくつか制限があります。

 - ロール名は、小文字の英数字を使用し、``_`` を追加してから、アルファベットで指定します。
 - コレクションのロールにはプラグインを含めることができません。プラグインは、コレクションの ``plugins`` ディレクトリーツリーに置かれている必要があります。各プラグインは、コレクションのすべてのロールからアクセスできます。

ロールのディレクトリー名はロール名として使用されます。したがって、
ディレクトリー名は上記のロール名のルールに準拠する必要があります。
ロール名がこれらのルールに準拠していないと、Galaxy へのコレクションのインポートは失敗します。

「従来のロール」をコレクションに移行することはできますが、上記のルールに従わなければなりません。従わない場合は、ロールの名前を変更する必要があります。ロールベースのプラグインをコレクションの特定のディレクトリーに移動したりリンクしたりする必要があります。

.. note::

    GitHub リポジトリーから直接 Galaxy にインポートされたロールの場合は、
    ロールのメタデータに ``role_name`` の値を設定すると、Galaxy が使用するロール名が上書きされます。コレクションの場合、この値は無視されます。コレクションをインポートする場合、
    Galaxy は、ロールディレクトリーをロールの名前としてを使用し、メタデータ値 ``role_name`` を無視します。

playbooks ディレクトリー
--------------------

現在準備中です。

test ディレクトリー
----------------

現在準備中です。コレクションのテストがここに常にあることが期待されます。


.. _creating_collections:

コレクションの作成
======================

コレクションを作成するには、以下を行います。

#. :ref:`ansible-galaxy collection init<creating_collections_skeleton>` を使用してコレクションを初期化し、スケルトンディレクトリー構造を作成します。
#. コンテンツをコレクションに追加しｍす。
#. :ref:`ansible-galaxy collection build<building_collections>` を使用して、コレクションをコレクションアーティファクトに構築します。。
#. :ref:`ansible-galaxy collection publish<publishing_collections>` を使用して、コレクションアーティファクトを Galaxy に公開します。

これにより、ユーザーが、そのコレクションをシステムにインストールできるようになります。

現在、``ansible-galaxy collection`` コマンドは以下のサブコマンドを実装しています。

* ``init``: Ansible に含まれるデフォルトテンプレートまたは独自のテンプレートに基づいて、基本的なコレクションのスケルトンを作成します。
* ``build``: Galaxy または独自のリポジトリーにアップロードできるコレクションアーティファクトを作成します。
* ``publish``: 構築したコレクションアーティファクトを Galaxy に公開します。
* ``install``: コレクションを 1 つまたは複数インストールします。

``ansible-galaxy`` cli ツールの詳細は、man ページの :ref:`ansible-galaxy` を参照してください。

.. _creating_collections_skeleton:

コレクションスケルトンの作成
------------------------------

新規コレクションを開始するには、以下を使用します。

.. code-block:: bash

    collection_dir#> ansible-galaxy collection init my_namespace.my_collection

これにより、コレクションのコンテンツをディレクトリーに追加できるようになります。コレクションに置けるものは、
https://github.com/bcoca/collection を参照してください。


.. _docfragments_collections:

コレクションでのドキュメントフラグメントの使用
--------------------------------------------

コレクションにドキュメントフラグメントを含めるには、以下を行います。

#. ``plugins/doc_fragments/fragment_name`` ドキュメントのフラグメントに作成します。

#. FQCN を使用したドキュメントフラグメントを参照します。

.. code-block:: yaml

   extends_documentation_fragment:
     - community.kubernetes.k8s_name_options
     - community.kubernetes.k8s_auth_options
     - community.kubernetes.k8s_resource_options
     - community.kubernetes.k8s_scale_options

:ref:`module_docs_fragments` は、ドキュメントフラグメントの基本を説明します。`kubernetes <https://github.com/ansible-collections/kubernetes>`_ コレクションには完全な例が含まれます。

また、FQCN を使用してコレクション間でドキュメントフラグメントを共有することもできます。

.. _building_collections:

コレクションの構築
--------------------

コレクションを構築するには、コレクションのルートディレクトリーから ``ansible-galaxy collection build`` を実行します。

.. code-block:: bash

    collection_dir#> ansible-galaxy collection build

これにより、現在のディレクトリーに構築されたコレクションの tarball が作成されます。これは Galaxy にアップロードできます。

    my_collection/
    ├── galaxy.yml
    ├── ...
    ├── my_namespace-my_collection-1.0.0.tar.gz
    └── ...


.. note::
    * コレクションアーティファクトのビルド時に、特定のファイルおよびフォルダーは除外されます。これは作業が進行中で、現在は設定できないため、コレクションアーティファクトに配布したくないファイルが含まれる場合があります。
    * 今回の非推奨となった ``Mazer`` ツールをコレクションに使用した場合は、``ansible-galaxy`` でコレクションをビルドする前に、:file:`releases/` ディレクトリーに追加したすべてのファイルを削除します。
    * ``ansible-test`` でテストしている場合は、:file:`tests/output` ディレクトリーを削除する必要もあります。
    * 現在の Galaxy の tarball 最大サイズは 2 MB です。


この tarball は、配布方法として主に Galaxy にアップロードすることを目的としていますが、
ターゲットシステムにコレクションをインストールするために直接使用することもできます。

.. _trying_collection_locally:

ローカルでコレクションを試行
--------------------------

コレクションを tarball からインストールすると、ローカルでコレクションを試すことができます。以下では、
隣接する Playbook がコレクションにアクセスできるようになります。

.. code-block:: bash

   ansible-galaxy collection install my_namespace-my_collection-1.0.0.tar.gz -p ./collections


パスには、:ref:`COLLECTIONS_PATHS` で設定された値の 1 つを使用する必要があります。これはまた、Ansible 自体がコレクションを使用しようとするときに、
コレクションを見つけることを期待する場所でもあります。パスの値を指定しない場合、``ansible-galaxy collection install`` は、
:ref:`COLLECTIONS_PATHS` で定義された最初のパス (デフォルトでは ~``~/.ansible/collections``) にコレクションをインストールします。

次に、Playbook 内でローカルコレクションの使用を試行します。例および詳細は、「:ref:`コレクションの使用 <using_collections>`」を参照してください。

.. _publishing_collections:

コレクションの公開
----------------------

``ansible-galaxy collection publish`` コマンドまたは Galaxy UI 自体を使用して、コレクションを Galaxy に公開できます。コレクションをアップロードするには、Galaxy で名前空間が必要です。詳細は、Galaxy docsite の「`Galaxy 名前空間 <https://galaxy.ansible.com/docs/contributing/namespaces.html#galaxy-namespaces>`_」を参照してください。

.. note:: コレクションのバージョンをアップロードしたら、そのバージョンを削除または変更できません。アップロードする前に、すべての情報が適切であることを確認します。

.. _galaxy_get_token:

トークンまたは API キーの取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

コレクションを Galaxy にアップロードするには、最初に API トークン (CLI の ``ansible-galaxy`` コマンドで ``--api-key``) を取得する必要があります。API トークンは、コンテンツを保護するために使用するシークレットトークンです。

API トークンを取得するには、以下を行います。

* `Galaxy プロファイルの設定` <https://galaxy.ansible.com/me/preferences>_ ページに移動し、:guilabel:`API トークン` をクリックします。
* Automation Hub の場合は、https://cloud.redhat.com/ansible/automation-hub/token/ にアクセスし、バージョンのドロップダウンから :guilabel:`Get API token` をクリックします。

.. _upload_collection_ansible_galaxy:

ansible-galaxy を使用したアップロード
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::
  デフォルトでは、(:ref:`galaxy_server` の :file:`ansible.cfg` ファイルに記載されていているように) ``ansible-galaxy`` は https://galaxy.ansible.com を Galaxy サーバーとして使用します。Ansible Galaxy にコレクションを公開するだけの場合は、これ以上の設定は必要ありません。Red Hat Automation Hub またはその他の Galaxy サーバーを使用している場合は、「:ref:`ansible-galaxy クライアントの設定 <galaxy_server_config>`」を参照してください。

``ansible-galaxy`` コマンドでコレクションアーティファクトをアップロードするには、以下を使用します。

.. code-block:: bash

     ansible-galaxy collection publish path/to/my_namespace-my_collection-1.0.0.tar.gz --api-key=SECRET

上記のコマンドは、Galaxy の Web サイトからコレクションをアップロードしたかのように、インポートプロセスをトリガーします。
このコマンドは、インポート処理が完了するまで待機してからステータスを報告します。インポート結果を待たずに続行したい場合は、
``--no-wait`` 引数を使用して、
`My Imports <https://galaxy.ansible.com/my-imports/>`_ ページでインポートの進行状況を手動で確認してください。

API キーは、コンテンツを保護するために Galaxy サーバーによって使用されるシークレットトークンです。詳細は、「:ref:`galaxy_get_token`」を参照してください。

.. _upload_collection_galaxy:

Galaxy の Web サイトからコレクションをアップロードします。
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Galaxy でコレクションアーティファクトを直接アップロードするには、以下を行います。

#. `My content <https://galaxy.ansible.com/my-content/namespaces>_` ページに移動し、名前空間のいずれかの **コンテンツを追加** ボタンをクリックします。
#. **コンテンツの追加** ダイアログから、**新規コレクションのアップロード** をクリックして、ローカルファイルシステムからコレクションアーカイブファイルを選択します。

コレクションをアップロードする場合は、どの名前空間を選択しても問題ありません。コレクションが、
``galaxy.yml`` ファイルのコレクションメタデータに指定した名前空間にアップロードされます。あなたが名前空間の所有者でないと、
アップロード要求は失敗します。

Galaxy がコレクションをアップロードして受け入れると、**My Imports** ページにリダイレクトされます。
このページには、コレクションに含まれるメタデータやコンテンツに関するエラーや警告など、インポート処理の出力が表示されます。

.. _collection_versions:

コレクションのバージョン
-------------------

コレクションのバージョンをアップロードしたら、そのバージョンを削除または変更することはできません。アップロードする前に、
すべてが問題なく見えることを確認してください。コレクションを変更する唯一の方法は、新しいバージョンをリリースすることです。コレクションの最新バージョン (バージョン番号の高いもの) は、Galaxy のすべての場所に表示されるバージョンになりますが、
ユーザーは古いバージョンもダウンロードできます。

コレクションのバージョンは、バージョン番号に `セマンティックバージョン` <https://semver.org/>_ を使用します。詳細と例は、公式ドキュメントをお読みください。つまり、以下のようになります。

* 互換性のない API 変更のメジャーバージョンのバージョン番号 (例: `x.y.z` の x)。
* 後方互換の方法で新機能のマイナーバージョンのバージョン番号 (例: `x.y.z` の y)。
* 後方互換のバグ修正向けのインクリメントパッチのバージョン番号 (例: `x.y.z` の z)。

.. _migrate_to_collection:

Ansible コンテンツのコレクションへの移行
=========================================

`content_collector ツール <https://github.com/ansible/content_collector>`_ を使用すると、既存モジュールのコレクションへの移行を試すことができます。``content_collector`` は、コンテンツを Ansible ディストリビューションからコレクションに移行するのに役に立つ Playbook です。

.. warning::

	このツールは現在開発中であり、現時点では実験とフィードバックのためにのみ提供されています。

詳細および使用方法のガイドラインは、「`content_collector README <https://github.com/ansible/content_collector>`_」を参照してください。

.. seealso::

   :ref:`collections`
       コレクションのインストールおよび使用方法はこちらを参照してください。
   :ref:`collections_galaxy_meta`
       コレクションのメタデータ構造を理解します。
   :ref:`developing_modules_general`
       Ansible モジュールの作成方法について
   `メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発メーリングリスト
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC チャットチャンネル
