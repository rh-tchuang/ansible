:orphan:

.. _testing_module_documentation:

****************************
モジュールドキュメンテーションのテスト
****************************

メインの Ansible リポジトリーに組み込むモジュールを送信する前に、正しい HTML レンダリングついてモジュールドキュメントをテストする必要があります。また、argspec が Python ファイルのドキュメントと一致することを確認する必要があります。コミュニティーページは、:ref:`reStructuredText ドキュメントのテスト <testing_documentation_locally>` で詳細を提供しています。

モジュールドキュメントの HTML 出力を確認するには、次のコマンドを実行します。

#. 動作する :ref:`開発環境` <environment_setup> を確保します。
#. 必要な Python パッケージをインストールします (venv/virtualenv では「--user」を指定しません)。

   .. code-block:: bash

      pip install --user -r requirements.txt
      pip install --user -r docs/docsite/requirements.txt

#. モジュールが適切なディレクトリー (``lib/ansible/modules/$CATEGORY/mymodule.py``) にあることを確認してください。
#. モジュールドキュメント ``modules=mymodule make webdocs`` から HTML を構築します。
#.  複数のモジュールの HTML ドキュメントを作成するには、モジュール名をコンマで区切ったリスト (``MODULES=mymodule,mymodule2 make webdocs``) を使用します。
#. ``file:///path/to/docs/docsite/_build/html/modules/mymodule_module.html`` で HTML ページを表示します。

モジュールのドキュメントが ``argument_spec`` と一致するようにするには、以下を使用します。

#. 必要な Python パッケージをインストールします (venv/virtualenv では「--user」を指定しません)。

   .. code-block:: bash

      pip install --user -r test/runner/requirements/sanity.txt

#. run the ``validate-modules`` test::

    ansible-test sanity --test validate-modules mymodule
