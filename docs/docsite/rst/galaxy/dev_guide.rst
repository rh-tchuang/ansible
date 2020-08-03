.. _developing_galaxy:

**********************
Galaxy 開発者ガイド
**********************

Ansible コミュニティーと共有するには、Galaxy でコレクションおよびロールをホストできます。Galaxy のコンテンツは、`ロール <playbooks_reuse_roles>`_ などの事前にパッケージ化された作業単位でフォーマットされ、Galaxy 3.2 では `コレクション <collections>`_ が新たに提供されました。
インフラストラクチャーのプロビジョニング、アプリケーションのデプロイ、および日々の作業を行うすべてのタスクにロールを作成できます。これに加えて、複数の Playbook、ロール、モジュール、およびプラグインを含む、自動化の包括的なパッケージを提供するコレクションを作成できます。

.. contents::
   :local:
   :depth: 2

.. _creating_collections_galaxy:

Galaxy のコレクションの作成
===============================

コレクションは、Ansible コンテンツのディストリビューション形式です。コレクションを使用して Playbook、ロール、モジュール、プラグインをパッケージ化および配布できます。
`Ansible Galaxy` <https://galaxy.ansible.com>_ を使用してコレクションを公開および使用できます。

コレクションの作成方法は、「:ref:`developing_collections`」を参照してください。

.. _creating_roles_galaxy:


Galaxy のロールの作成
=========================

``init`` コマンドを使用して新規ロールの基本構造を初期化し、ロールに必要なさまざまなディレクトリーおよび main.yml ファイルを作成する際の時間を短縮します。

.. code-block:: bash

   $ ansible-galaxy init role_name

上記により、現在の作業ディレクトリーに以下のディレクトリー構造が作成されます。

.. code-block:: text

   role_name/
       README.md
       .travis.yml
       defaults/
           main.yml
       files/
       handlers/
           main.yml
       meta/
           main.yml
       templates/
       tests/
           inventory
           test.yml
       vars/
           main.yml

ロールのリポジトリーを作成する場合、リポジトリーのルートは `role_name` である必要があります。

Force
-----

ロール名に一致するディレクトリーが現在の作業ディレクトリーに存在する場合は、init コマンドによりエラーが発生します。エラーを無視するには、
*--force* オプションを使用します。上記のサブディレクトリーとファイルを強制的に作成し、一致するものをすべて置き換えます。

Container enabled
-----------------

Container Enabled ロールを作成する場合は、``--type container`` を ``ansible-galaxy init`` に渡します。これにより、上記と同じディレクトリー構造が作成されますが、
Container Enabled ロールに適したデフォルトファイルが置かれます。たとえば、README.md の構造は少し異なり、*.travis.yml* ファイルテストは、
`Ansible Container <https://github.com/ansible/ansible-container>`_ を使用するロールをテストし、メタディレクトリーには *container.yml* ファイルが含まれます。

カスタムロールのスケルトンの使用
----------------------------

カスタムロールのスケルトンディレクトリーは、以下のように指定できます。

.. code-block:: bash

   $ ansible-galaxy init --role-skeleton=/path/to/skeleton role_name

スケルトンを指定すると init は以下のことを行います。

- すべてのファイルおよびディレクトリーをスケルトンから新しいロールにコピーします。
- templates ディレクトリー外で見つかった .j2 ファイルは、すべてテンプレートとして表示されます。現時点で唯一有用な変数は role_name です。
- .git ディレクトリーおよび .git_keep ファイルはコピーされません。

または、role_skeleton とファイルの無視は、ansible.cfgで設定できます

.. code-block:: text

  [galaxy]
  role_skeleton = /path/to/skeleton
  role_skeleton_ignore = ^.git$,^.\*/.git_keep$

Galaxy での認証
------------------------

Galaxy Web サイトでロールを管理するために ``import`` コマンド、``delete`` コマンド、および ``setup`` コマンドを使用するには認証が必要ですが、
そのためには、``login`` コマンドを使用できます。``login`` コマンドを使用する前に、Galaxy の Web サイトにアカウントを作成する必要があります。

``login`` コマンドでは、GitHub の認証情報を使用する必要があります。ユーザー名とパスワードを使用するか、`個人用アクセストークン` <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>_ を作成できます。トークンの作成を選択した場合は、識別の検証のみに使用されるため、トークンに最小限のアクセス権限を付与します。

以下は、GitHub のユーザー名とパスワードを使用した Galaxy Web サイトでの認証を示しています。

.. code-block:: text

   $ ansible-galaxy login

   We need your GitHub login to identify you.
   This information will not be sent to Galaxy, only to api.github.com.
   The password will not be displayed.

   Use --github-token if you do not want to enter your password.

   GitHub Username: dsmith
   Password for dsmith:
   Successfully logged into Galaxy as dsmith

ユーザー名とパスワードの使用を選択すると、パスワードは Galaxy に送信されません。これは、GitHub で認証し、個人用アクセストークンを作成するために使用されます。
次にトークンを Galaxy に送信し、Galaxy は ID を確認し、Galaxy アクセストークンを返します。認証が完了すると、
GitHub トークンは破棄されます。

GitHub パスワードを使用しない場合や、GitHub で 2 段階認証を有効にしている場合は、*--github-token* オプションを使用して、作成する個人用アクセストークンを渡します。


ロールのインポート
-------------

``import`` コマンドには、最初に ``login`` コマンドを使用して認証する必要があります。認証後、所有またはアクセス権が付与された GitHub リポジトリーをインポートできます。

以下を使用してロールにインポートします。

.. code-block:: bash

  $ ansible-galaxy import github_user github_repo

デフォルトでは、コマンドは Galaxy がインポートプロセスを完了するまで待機し、インポートが進行するにつれて結果を表示します。

.. code-block:: text

      Successfully submitted import request 41
      Starting import 41: role_name=myrole repo=githubuser/ansible-role-repo ref=
      Retrieving GitHub repo githubuser/ansible-role-repo
      Accessing branch: master
      Parsing and validating meta/main.yml
      Parsing galaxy_tags
      Parsing platforms
      Adding dependencies
      Parsing and validating README.md
      Adding repo tags as role versions
      Import completed
      Status SUCCESS : warnings=0 errors=0

ブランチ
^^^^^^

*--branch* オプションを使用して、特定のブランチをインポートします。指定されていない場合は、リポジトリーのデフォルトブランチが使用されます。

ロール名
^^^^^^^^^

デフォルトでは、ロールに指定される名前は GitHub リポジトリー名から作成されます。ただし、*--role-name* オプションを使用してこれを上書きし、名前を設定できます。

待機なし
^^^^^^^

*--no-wait* オプションを指定すると、コマンドは結果を待ちません。ロールに関する最新のインポート結果は、Galaxy Web サイトで *My Imports* に移動して利用できます。

ロールの削除
-------------

``delete`` コマンドには、最初に ``login`` コマンドを使用して認証する必要があります。認証後、Galaxy Web サイトからロールを削除できます。GitHub のリポジトリーにアクセスできるロールのみを削除できます。

ロールを削除するには、以下を使用します。

.. code-block:: bash

  $ ansible-galaxy delete github_user github_repo

これは、Galaxy からロールを削除するだけです。実際の GitHub リポジトリーを削除したり、変更したりしません。


Travis 統合
-------------------

Galaxy と `Travis <https://travis-ci.org>`_ のロールの間に統合またはコネクションを作成できます。接続が確立されると、
Travis でのビルドは自動的に Galaxy でのインポートをトリガーし、そのロールに関する最新情報で検索インデックスを更新します。

``setup`` コマンドを使用して統合を作成しますが、統合を作成する前に、最初に ``login`` コマンドを使用して認証する必要があります。
Travis のアカウントおよび Travis トークンも必要になります。準備が整ったら、次のコマンドを使用して統合を作成します。

.. code-block:: bash

  $ ansible-galaxy setup travis github_user github_repo xxx-travis-token-xxx

setup コマンドには Travis トークンが必要ですが、トークンは Galaxy に保存されません。これは、
「`Travis ドキュメント <https://docs.travis-ci.com/user/notifications/>`_」で説明されたとおりにハッシュを作成するために、GitHub のユーザー名およびリポジトリーと共に使用されます。ハッシュは Galaxy に保存され、Travis から受け取った通知の検証に使用されます。

setup コマンドは、Galaxy が通知に応答できるようにします。Travis を設定してリポジトリーでビルドを実行し、通知を送信するには、
「`Travis getting started guide <https://docs.travis-ci.com/user/getting-started/>`_」の手順に従ってください。

ビルドの完了時に Galaxy に通知するように Travis に指示するには、.travis.yml ファイルに以下を追加します。

.. code-block:: text

    notifications:
        webhooks: https://galaxy.ansible.com/api/v1/notifications/


Travis 統合の一覧表示
^^^^^^^^^^^^^^^^^^^^^^^^

*--list* オプションを使用して、Travis 統合を表示します。

.. code-block:: bash

      $ ansible-galaxy setup --list


      ID         Source     Repo
      ---------- ---------- ----------
      2          travis     github_user/github_repo
      1          travis     github_user/github_repo


Travis 統合の削除
^^^^^^^^^^^^^^^^^^^^^^^^^^

*--remove* オプションを使用して、Travis 統合を無効化および削除します。

  .. code-block:: bash

    $ ansible-galaxy setup --remove ID

無効にする統合の ID を指定します。*--list* オプションを使用して ID を見つけることができます。


.. seealso::
  :ref:`collections`
    モジュール、Playbook、およびロールの共有可能なコレクション
  :ref:`playbooks_reuse_roles`
    Ansible ロールに関するすべて
  `メーリングリスト <https://groups.google.com/group/ansible-project>`_
    ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
  `irc.freenode.net <http://irc.freenode.net>`_
    #ansible IRC チャットチャンネル
