:orphan:

.. _testing_running_locally:

***************
Ansible のテスト
***************

.. contents:: トピック

本書では、以下を行う方法を説明します。

* ``ansible-test`` を使用してテストをローカルで実行します。
* 拡張します。

要件
============

Python 2.7 以降で ``ansible-test`` を実行する特別な要件はありません。
Python 2.6 には ``argparse`` パッケージが必要です。
各 ``ansible-test`` コマンドの要件は、後で説明します。


テスト環境
=================

ほとんどの ``ansible-test`` コマンドは、テストを簡単にするために、1 つ以上の分離テスト環境での実行をサポートします。


リモート
------

``--remote`` オプションは、クラウドホスト環境でテストを実行します。
この機能を使用するには API キーが必要です。

    統合テストに推奨されます。

詳細は、「`list of supported platforms and versions` <https://github.com/ansible/ansible/blob/devel/test/runner/completion/remote.txt>_」 の一覧を参照してください。

環境変数
---------------------

環境変数を使用してテストを操作する際には、以下の制限事項に留意してください。環境変数は以下のようになります。

* ``--docker`` オプションまたは ``--remote`` オプションを使用する場合は、ホストからテスト環境に伝播されません。
* ``common_environment`` 関数の ``test/runner/lib/util.py`` でホワイトリスト化されない限り、テスト環境に公開されません。
* ``passenv`` 定義を使用して ``test/runner/tox.ini`` でホワイトリスト化しない限り、``--tox`` オプションを使用してテスト環境に公開されません。

    例: ``ansible-test integration --tox`` の実行時に、``ANSIBLE_KEEP_REMOTE_FILES=1`` を設定できます。ただし、``--docker`` オプションを使用すると、
    Docker 環境にアクセスするには、``ansible-test shell`` を実行する必要があります。シェルプロンプトで一度、環境変数を設定でき、
    テストが実行されました。これは、
    「:ref:`AnsibleModule ベースのモジュールのデバッグ <debugging_ansiblemodule_based_modules>`」の指示に従って、コンテナー内でテストをデバッグする際に便利です。

インタラクティブシェル
=================

``ansible-test shell`` コマンドを使用して、テストを実行するのに使用する同じ環境でインタラクティブシェルを取得します。例:

* ``ansible-test shell --docker`` - デフォルトの docker コンテナーでシェルを開きます。
* ``ansible-test shell --tox 3.6`` - Python 3.6 ``tox`` 環境でシェルを開きます。


コードの対象範囲
=============

コードの対象範囲レポートは、
より多くのテストが記述されるべき未テストのコードを簡単に識別することができます。 オンラインレポートは利用できますが、``devel`` ブランチのみを対象としています 
( :ref:`developing_testing` を参照)。 新規コードのローカルレポートが必要な場合。

``--coverage`` オプションをテストコマンドに追加して、コードの対象範囲のデータを収集します。 分離された python を作成する 
``--tox`` オプションまたは ``--docker`` オプションを使用していない場合は、
``-requirements`` オプションを使用して、
対象モジュールの正しいバージョンがインストールされている必要があります。

   ansible-test units --coverage apt
   ansible-test integration --coverage aws_lambda --tox --requirements
   ansible-test coverage html


レポートは、複数の形式で生成できます。

* ``ansible-test coverage report`` - コンソールレポート
* ``ansible-test coverage html`` - HTML レポート
* ``ansible-test coverage xml`` - XML レポート

テストの実行間でデータを消去するには、``ansible-test coverage erase`` コマンドを使用します。機能の一覧は、オンラインヘルプを参照してください。

   ansible-test coverage --help
