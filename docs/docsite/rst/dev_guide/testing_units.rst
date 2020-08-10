:orphan:

.. _testing_units:

**********
ユニットテスト
**********

ユニットテストは、特定のライブラリーまたはモジュールを対象とする小規模の分離テストです。 Ansible のユニットテストは、
現在のところ Ansible の継続的インテグレーションプロセスの中で、
python からテストを実行する唯一の方法です。つまり、状況によっては、
テストはユニット以外のものも含まれます。

.. contents:: トピック

利用可能なテスト
===============

ユニットテストは `test/units 
「<https://github.com/ansible/ansible/tree/devel/test/units>`_」にあります。テストのディレクトリー構造は、
``lib/ansible/`` の構造と一致します。

テストの実行
=============

Ansible のユニットテストは、以下の操作を実行してコードベース全体で実行できます。

.. code:: shell

    cd /path/to/ansible/source
    source hacking/env-setup
    ansible-test units --tox

1 つのファイルに対して以下を行います。

.. code:: shell

   ansible-test units --tox apt

または、以下を実行して特定の Python バージョンに対して実行します。

.. code:: shell

   ansible-test units --tox --python 2.7 apt

モジュールユーティリティーなどのモジュール以外のものに対してユニットテストを実行している場合は、ファイルパス全体を指定します。

.. code:: shell

   ansible-test units --tox test/units/module_utils/basic/test_imports.py

高度な使用方法は、オンラインヘルプを参照してください。

   ansible-test units --help

プル要求を開くことで、
Ansible の継続的な統合システムでテストを実行することもできます。 これにより、
プル要求で行われた変更に基づいて実行するテストが自動的に決定されます。


依存関係のインストール
=======================

``ansible-test`` には多くの依存関係があります。``ユニット`` テストの場合は、``tox`` の使用が推奨されます。

依存関係は、``--requirements`` 引数を使用してインストールできます。
これにより、ユニットテストに必要な依存関係がすべてインストールされます。例:

.. code:: shell

   ansible-test units --tox --python 2.7 --requirements apache2_module


.. note:: tox バージョン要件

   ``--tox`` で ``ansible-test`` を使用する場合は、2.5.0 より新しいバージョンが必要です。


要件の一覧は、「`test/lib/ansible_test/_data/requirements
<https://github.com/ansible/ansible/tree/devel/test/lib/ansible_test/_data/requirements>`_」を参照してください。要件ファイルは、
それぞれのコマンドにちなんだ名前が付けられています。すべてのコマンドに適用される「`constraints
<https://github.com/ansible/ansible/blob/devel/test/lib/ansible_test/_data/requirements/constraints.txt>`_」
も参照してください。


ユニットテストの拡張
====================


.. warning:: ユニットテスト以外のもの

   外部サービスを必要とするテストを書き始めると、
   ユニットテストではなく統合テストを書くことができます。


ユニットテストの構造
``````````````````````

Ansible ドライブユニットテストは、`pytest` <https://docs.pytest.org/en/latest/>_ でテストします。つまり、
テストは ``test_<something>.py`` のようなファイル名に含まれる単純な関数か、
クラスとして書くことができます。

以下は、関数の例です。

  #this function will be called simply because it is called test_*()

  def test_add()
      a = 10
      b = 23
      c = 33
      assert a + b = c

以下はクラスの例です::

  import unittest

  class AddTester(unittest.TestCase)

      def SetUp()
          self.a = 10
          self.b = 23

      # this function will
      def test_add()
        c = 33
        assert self.a + self.b = c

     # this function will
      def test_subtract()
        c = -13
        assert self.a - self.b = c

関数ベースのインターフェースの方がシンプルで速いため、
モジュールにいくつかの基本的なテストを追加しようとしている場合は、
おそらくこの方法から始めるべきでしょう。 クラスベースのテストでは、前提条件の設定や分解をより整然と行うことができますため、
モジュールに多くのテストケースがある場合は、
それを使用するようにリファクタリングした方がよいでしょう。

テスト内で単純な ``assert`` を使用するアサーションは、
アサーション中に呼び出された関数のトレースバックにより、
失敗の原因に関する完全な情報を提供します。 これは、他の外部アサーションライブラリーよりも、
プレーンアサートが推奨されることを意味します。

ユニットテストスイートの多くは、
特にネットワークの分野では、複数のモジュール間で共有される関数を含んでいます。 このような場合は、
同じディレクトリーにファイルが作成され、


それが直接インクルードされます。
````````````````````````````

`test/units/` ディレクトリー構造内で、共通コードを可能な限り具体的にしてください。たとえば、
たとえば、Amazon モジュールのテストに固有の場合は、
`test/units/modules/cloud/amazon/` にある必要があります。カレントディレクトリーや親ディレクトリー以外のディレクトリーから、
共通のユニットテストコードをインポートしないでください。

ユニットテストから他のユニットテストをインポートしないでください。共通のコードは、
それ自体がテストではない専用のファイルに記述してください。


Fixtures ファイル
``````````````

デバイスからの結果のフェッチをモックアウトしたり、外部ライブラリーからの他の複雑なデータ構造を提供するために、
``fixtures`` を使用して事前に生成されたデータを読み込むことができます。

``test/units/modules/network/PLATFORM/fixtures/`` に含まれるテキストファイル

データは、``load_fixture`` メソッドを使用して読み込みます。

詳細は、「`eos_banner test
<https://github.com/ansible/ansible/blob/devel/test/units/modules/network/eos/test_eos_banner.py>`_」
を参照してください。

API のシミュレーションをしているのであれば、python のプラシーボが役に立つかもしれません。 詳細は、
「:ref:`testing_units_modules`」を参照してください。


新規ユニットテストまたは更新されたユニットテスト用のコード対応
```````````````````````````````````````````
新しいコードは、codecov.io のカバレージレポートには追加されないため (:ref:`development_testing` を参照)、
ローカルレポートが必要になります。 ほとんどの ``ansible-test`` コマンドでコードカバレージを収集することができます。
これは、テストを拡張する場所を示す際に特に便利です。

カバレージデータを収集するには、``--coverage`` 引数を ``ansible-test`` コマンドラインに追加します。

.. code:: shell

   ansible-test units --coverage apt
   ansible-test coverage html

結果は ``test/results/reports/coverage/index.html`` に書き込まれます。

Report は、複数の形式で生成できます。

* ``ansible-test coverage report`` - コンソールレポート
* ``ansible-test coverage html`` - HTML レポート
* ``ansible-test coverage xml`` - XML レポート

テストの実行間でデータを消去するには、``ansible-test coverage erase`` コマンドを使用します。 カバレージレポートの生成は、
「:ref:`testing_running_locally`」
を参照してください。


.. seealso::

   :ref:`testing_units_modules`
       ユニットテストモジュールに関する特別な考慮事項
   :ref:`testing_running_locally`
       カバレージデータの収集とレポートを含む、ローカルでのテストの実行
   `Python 3 ドキュメント - 26.4. unittest - ユニットテストのフレームワーク <https://docs.python.org/3/library/unittest.html>`_
       Python 3 における unittest フレームワークのドキュメント
   `Python 2 ドキュメント - 25.3. unittest - ユニットテストのフレームワーク <https://docs.python.org/3/library/unittest.html>`_
       サポートされている初期の unittest フレームワークのドキュメント - Python 2.6
   `pytest (より優れたプログラムを書き込むのに役立ちます) <https://docs.pytest.org/en/latest/>`_
       pytest のドキュメント: Ansible ユニットテストの実行に実際に使用されているフレームワーク
