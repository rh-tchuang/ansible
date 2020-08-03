.. _community_documentation_contributions:

*****************************************
Ansible ドキュメントへの貢献
*****************************************

Ansible ではドキュメントが多数提供されていますが、ドキュメントを作成するチームは小規模です。新機能、修正、および変更の情報を常に最新に保つには、コミュニティーによるサポートが重要です。

ドキュメントへの改善は、Ansible プロジェクトへの最初の貢献として適しています。本ガイドは YAML (モジュールドキュメント) または `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ (rST) で記述されているため、貢献者がプログラマーである必要はありません。Ansible を使用している場合は、Playbook ですでに YAML を使用しています。そして、rST はほとんどがテキストです。``Edit on GitHub`` オプションを使用すれば、git の経験も必要ではありません。

このドキュメントの Web サイトで、タイポやサンプルの間違い、不足しているトピックなどのエラーや脱落を見つけたら、私たちに知らせてください。Ansible ドキュメントをサポートする方法は次のとおりです。

.. contents::
   :local:

GitHub でドキュメントを直接編集
===============================

入力ミスやその他の簡単な修正は、サイトから直接ドキュメントを編集できます。このページの右上を見てください。``Edit on GitHub`` リンクは、ドキュメント内のすべてのページで利用できます。GitHub アカウントがある場合は、この方法で迅速かつ簡単なプル要求を送信できます。

``Edit on GitHub`` で docs.ansible.com からドキュメントの PR を送信するには、以下を行います。

#. ``Edit on GitHub`` をクリックします。#. GitHub アカウントで ansible リポジトリーのフォークを所有していない場合は、作成するように促されます。
#. タイプミスを修正したり、例文を更新したり、その他の変更を加えたりします。
#. GitHub ページの一番下にある ``Propose file change`` という見出しの下にある最初の四角い部分にコミットメッセージを入力します。より具体的な方が望ましいです。たとえば「fixes typo in my_module description (my_module の説明にあるタイポを修正)」といった具合です。2 つの目の四角い部分に詳細を記入することもできます。ここで、``+label: docsite_pr`` はそのままにしておきます。#. 緑色の「Propose file change」ボタンをクリックして変更を提案します。GitHub がブランチ作成とコミットを行い、「Comparing Changes」という見出しのページを開きます。
#. ``Create pull request`` をクリックして PR テンプレートを開きます。#. PR テンプレートには、変更に適した詳細などを記入します。PR のタイトルは、必要に応じて変更できます (デフォルトでは、コミットメッセージと同じタイトルになっています)。``Issue Type`` セクションで、``Docs Pull Request`` 行を除くすべての行を削除します。#. ``Create pull request`` ボタンをクリックして、変更内容を送信します。
#. Ansibot という名前の自動スクリプトがラベルを追加し、ドキュメントのメンターに通知を送り、CI テストが開始されるのをお待ちください。
#. 送信した PR に注意を払い続けてください。ドキュメントチームから変更を依頼される場合があります。

PR および問題の確認
=============================

開いているドキュメントの `問題 (issue) <https://github.com/ansible/ansible/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+label%3Adocs>`_ および `PR <https://github.com/ansible/ansible/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+label%3Adocs>`_ を確認して、貢献することもできます。役に立つレビューを追加するには、以下を参照してください。

- 「looks good to me (私には良さそうに見える)」というコメントは、他の人にもその理由が明らかな場合にのみ使用してください。
- 問題がある場合は、問題を再現してください。
- PR については、変更をテストしてください。

新しい問題または PR を開く
=============================

気づいた問題が複雑すぎて ``Edit on GitHub`` オプションでは修正できず、その問題が報告されていなかったり、PR が作成されていない場合は、``ansible/ansible`` で問題 (issue) や PR を作成してください。

GitHub の問題や PR には、以下のような内容を追加してください。

- 特定のタイトル
- 問題の詳細な説明 (何が問題なのか分からないと変更案の評価が困難になるため、PR の場合でも同様)
- その他の情報 (関連する問題や PR、外部ドキュメント、docs.ansible.com のページなど) へのリンク

複雑なドキュメントの PR を作成する前に
==========================================

ドキュメントに複数の変更を加えたり、それに複数の行を追加したりする場合は、プル要求を開始する前に、以下を行います。

#. 記述した内容が、`style_guide` に従っていることを確認してください。
#. 変更した内容が rST のエラーになっていないかテストしてください。
#. ページ、できればドキュメントサイト全体をローカルでビルドします。

ローカルマシンでドキュメントを扱うには、python-3.5 以降と、以下のパッケージがインストールされている必要があります。

- gcc
- jinja2
- libyaml
- Pygments >= 2.4.0
- pyparsing
- PyYAML
- rstcheck
- six
- sphinx
- sphinx-notfound-page
- straight.plugin

.. note::

    Xcode を使用する macOS に、``--ignore-installed` を使用して ``six`` および ``pyparsing`` をインストールして、``sphinx`` に対応するバージョンを取得する必要がある場合があります。

.. _testing_documentation_locally:

ドキュメントのローカルでのテスト
---------------------------------

rST エラーに対して個別のファイルをテストするには、以下を行います。

.. code-block:: bash

   rstcheck changed_file.rst

ローカルでのドキュメントのビルド
----------------------------------

ドキュメントのビルドは、エラーと変更を確認するのに最適な方法です。エラーなしで `rstcheck` を実行したら、``ansible/docs/docsite`` に移動し、確認するページをビルドします。

単一の rST ページのビルド
^^^^^^^^^^^^^^^^^^^^^^^^^^

make ユーティリティーで単一の RST ファイルをビルドするには、以下を実行します。

.. code-block:: bash

   make htmlsingle rst=path/to/your_file.rst

たとえば、以下のようになります。

.. code-block:: bash

   make htmlsingle rst=community/documentation_contributions.rst

このプロセスはすべてのリンクをコンパイルしますが、ログ出力は最小限になります。新しいページを作成する場合や、より詳細なログ出力が必要な場合は、「:ref:`build_with_sphinx-build`」の説明を参照してください。

.. note::

    ``make htmlsingle`` は、``rst=`` で提供されるパスの先頭に ``rst/`` を追加するため、自動補完でファイル名を入力することができません。これが間違っている場合は、以下のようにエラーメッセージが表示されます。

      - ``docs/docsite/rst/`` ディレクトリーから ``make htmlsingle`` を実行した場合は、*** No rule to make target `htmlsingle' Stop.`` メッセージが表示されます。
      - rST ドキュメントへの完全パスを使用して ``docs/docsite/`` ディレクトリーから ``make htmlsingle`` を実行した場合は、``sphinx-build: error: cannot find files ['rst/rst/community/documentation_contributions.rst']`` メッセージが表示されます。


すべての rST ページのビルド
^^^^^^^^^^^^^^^^^^^^^^^^^^

モジュールのドキュメント以外のすべての rST ファイルをビルドするには、以下を実行します。

.. code-block:: bash

   MODULES=none make webdocs

モジュールドキュメントと rST ページのビルド
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

いくつかのモジュールとすべての rST ファイルを使用してドキュメントをビルドするには、コンマ区切りリストを使用します。

.. code-block:: bash

   MODULES=one_module,another_module make webdocs

すべてのモジュールドキュメントとすべての rST ファイルをビルドするには、以下を実行します。

.. code-block:: bash

   webdocs の作成

.. _build_with_sphinx-build:

``sphinx-build`` で rST ファイルのビルド
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

上級ユーザーは、sphinx ユーティリティーを使用して 1 つ以上の rST ファイルを直接ビルドすることができます。``sphinx-build`` は、内部リンクが作成たれないため、1 ページのみをビルドする場合は、誤解を招く ``undefined label`` 警告を返します。ただし、``sphinx-build`` は、インデントエラーや ``x-string without end-string`` 警告など、より広範な構文のフィードバックを返します。これは特に、ゼロから新しいページを作成している場合に役に立ちます。``sphinx-build`` でページをビルドするには、以下のようにします。

.. code-block:: bash

  sphinx-build [options] sourcedir outdir [filenames...]

ファイル名を指定することもできますし、すべてのファイルに ``–a`` を指定することもできます。もしくは、両方を省略して新しいまたは変更されたファイルだけをコンパイルすることもできます。

たとえば、以下のようになります。

.. code-block:: bash

  sphinx-build -b html -c rst/ rst/dev_guide/ _build/html/dev_guide/ rst/dev_guide/developing_modules_documenting.rst

最終テストの実行
^^^^^^^^^^^^^^^^^^^^^^^

ドキュメントのプル要求を送信すると、自動化されたテストが実行します。同じテストをローカルで実行できます。これを行うには、リポジトリーのトップディレクトリーに移動して以下を実行します。

.. code-block:: bash

  make clean && bin/ansible-test sanity --test docs-build && bin/ansible-test sanity --test rstcheck

ただし、以前ドキュメントを生成した時の rST ファイルが残っていると、このテストを混乱させることがあります。そのために、リポジトリーのクリーンコピー上で実行するのが最も安全です。これは、``make clean`` の目的でもあります。この 3 つの行を一度に 1 行ずつ入力して、各行が成功したことを手動で確認する場合、``&&`` は必要ありません。

ドキュメントワーキンググループへの参加
=======================================

ドキュメントワーキンググループは始まったばかりです。詳細は「`community repo <https://github.com/ansible/community>`_」を参照してください。

.. seealso:: 「:ref:`モジュールドキュメントのテストの詳細 <testing_module_documentation>`」および「:ref:`モジュールの文書化の詳細 <module_documenting>`」
