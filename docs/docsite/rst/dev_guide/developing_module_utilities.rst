.. _developing_module_utilities:

*************************************
モジュールユーティリティーの使用および開発
*************************************

Ansible は、独自のモジュールを開発する際に使用できるヘルパー関数を提供するモジュールユーティリティー、
または共有コードのスニペットを多数提供します。basic.py モジュールユーティリティーは、
Ansible ライブラリーにアクセスするための主要なエントリーポイントを提供します。
すべての Python Ansible モジュールは、
``ansible.module_utils`` から何かをインポートする必要があります。一般的なオプションとして、``AnsibleModule`` をインポートする方法があります。

  from ansible.module_utils.basic import AnsibleModule

``ansible.module_utils`` 名前空間は簡単な Python パッケージではありません。
インポートを抽出し、
アクティブな構成から派生した :ref:`検索パス <ansible_search_path>` に対して名前空間に一致するものを解決することにより、
タスクの呼び出しごとに動的に構築されます。

独自のローカルモジュールのメンテナンスの負担を軽減するために、
複製されたコードを 1 つまたは複数のモジュールユーティリティーに追加し、モジュールにインポートします。たとえば、``my_shared_code`` ライブラリーをインポートする独自のカスタムモジュールがある場合は、以下のように ``./module_utils/my_shared_code.py`` ファイルに置くことがあります。

  from ansible.module_utils.my_shared_code import MySharedCodeClient

``ansible-playbook`` を実行すると、Ansible はローカルの ``module_utils`` ディレクトリー内のファイルを :ref:`Ansible 検索パス<ansible_search_path>` で定義される順序で ``ansible.module_utils`` 名前空間にマージします。

モジュールユーティリティーの命名および検索
===================================

通常、モジュールユーティリティーの機能は、その名前や場所からわかります。たとえば、``openstack.py`` には、OpenStack インスタンスと連携するモジュールのユーティリティーが含まれます。
一般的なユーティリティー (さまざまな種類のモジュールによって使用される共有コード) は、``common`` のサブディレクトリーまたはルートディレクトリーに存在します。特定のモジュールのセットで使用され、
通常、
これらのモジュールのディレクトリーをミラーリングするサブディレクトリーにあります。例:

* ``lib/ansible/module_utils/urls.py`` には URL の解析用の共有コードが含まれます。
* ``lib/ansible/module_utils/storage/emc/`` には、EMC に関連する共有コードが含まれます。
*  ``lib/ansible/modules/storage/emc/`` には、EMC に関連するモジュールが含まれています。

このパターンを独自のモジュールユーティリティーで行うと、あらゆるものを見つけ、使用することが容易になります。

.. _standard_mod_utils:

標準のモジュールユーティリティー
=========================

Ansible には、``module_utils`` ファイルの大規模なライブラリーが同梱されています。
Ansible のメインのパスの、
``lib/ansible/module_utils`` ディレクトリーに、
ユーティリティーソースコードがあります。以下の最も広く使用されているユーティリティーを説明しています。特定のモジュールユーティリティーの詳細は、
「`module_utils のソースコード <https://github.com/ansible/ansible/tree/devel/lib/ansible/module_utils>`_」を参照してください。

.. include:: shared_snippets/licensing.txt

- ``api.py`` - 汎用 API モジュールをサポートします。
- ``basic.py`` - Ansible モジュールの一般的な定義およびヘルパーユーティリティー
- ``common/dict_transformations.py`` - ディクショナリー変換のヘルパー関数
- ``common/file.py`` - ファイルを操作するヘルパー関数
- ``common/text/`` - テキストの変換およびフォーマットを行うヘルパー関数
- ``common/parameters.py`` - モジュールパラメーターを処理するヘルパー関数
- ``common/sys_info.py`` - ディストリビューションおよびプラットフォーム情報を取得する機能
- ``common/validation.py`` - モジュール引数仕様に対してモジュールパラメーターを検証するためのヘルパー関数
- ``facts/`` - ファクトを返すモジュールのユーティリティーディレクトリー。詳細は、「`PR 23012` <https://github.com/ansible/ansible/pull/23012>_」を参照してください。
- ``ismount.py`` - os.path.ismount を修正する単一のヘルパー関数
- ``json_utils.py`` - 先頭行や末尾行など、モジュール JSON 出力に関する関連のない出力をフィルタリングするユーティリティー
- ``known_hosts.py`` - known_hosts ファイルで作業するためのユーティリティー
- ``network/common/config.py`` - ネットワークモジュールによって使用される設定ユーティリティーの機能
- ``network/common/netconf.py`` - Netconf トランスポートを使用するモジュールの定義およびヘルパー関数
- ``network/common/parsing.py`` - ネットワークモジュールの定義およびヘルパー関数
- ``network/common/network.py`` - ネットワークデバイスでコマンドを実行する機能
- ``network/common/utils.py`` - コマンドと比較演算子、およびその他のネットワークモジュールで使用するために使用するその他のユーティリティーを定義します。
- ``powershell/`` - Windows PowerShell モジュールの定義およびヘルパー関数のディレクトリー
- ``pycompat24.py`` - Python 2.4 の例外回避策
- ``service.py`` - モジュールが Linux サービスと連携できるようにするユーティリティー (未使用のプレースホルダー)
- ``shell.py`` - モジュールによるシェルの作成およびシェルコマンドの使用を許可する関数
- ``six/__init__.py`` - Python 2 と Python 3 の両方と互換性のあるコードを書き込む際に助けとなる `Six Python ライブラリー <https://pythonhosted.org/six/>`_ のバンドルコピー
- ``splitter.py`` - Jinja2 テンプレートを使用する文字列分割および操作ユーティリティー
- ``urls.py`` - http および https リクエストを操作するユーティリティー
