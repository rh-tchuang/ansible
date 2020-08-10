.. _using_local_modules_and_plugins:
.. _developing_locally:

**********************************
モジュールおよびプラグインをローカルで追加
**********************************

.. contents::
   :local:

Ansible を拡張する最も簡単で、最も速く、最も一般的な方法は、ローカルで使用するためにモジュールまたはプラグインをコピーするか、作成することです。チームまたは組織内で使用できるように、ローカルのモジュールとプラグインを Ansible コントロールノードに保管できます。ローカルのプラグインまたはモジュールを共有するには、ロールに組み込み、Ansible Galaxy に公開します。Galaxy からロールを使用していた場合は、ローカルのモジュールとプラグインを認識せずに使用していた可能性があります。存在しているローカルのモジュールまたはプラグインを使用している場合は、このページのみが必要になります。

ローカルのモジュールおよびプラグインで Ansible を拡張すると、ショートカットが多数利用できるようになります。

* 他のユーザーのモジュールおよびプラグインをコピーできます。
* 新しいモジュールを作成する場合は、任意のプログラミング言語を選択できます。
* メインの Ansible リポジトリーのクローンを作成する必要はありません。
* プル要求を開く必要はありません。
* テストを追加する必要はありません (ただし、この操作を推奨しています)。

Ansible が検索して使用できるようにローカルのモジュールまたはプラグインを保存するには、正しい「マジック」ディレクトリーにモジュールまたはプラグインを置きます。ローカルモジュールの場合は、ファイル名をモジュール名として使用します。たとえば、モジュールファイルが ``~/.ansible/plugins/modules/local_users.py`` の場合は、モジュール名に ``local_users`` を使用します。

.. _modules_vs_plugins:

モジュールおよびプラグイン: 相違点
===========================================
ローカル機能を Ansible に追加する場合は、モジュールまたはプラグインのどちらが必要か疑問に思われるかもしれません。相違点の概要は次のとおりです。

* モジュールは、Ansible API、:command:`ansible` コマンド、または :command:`ansible-playbook` コマンドで使用できる再利用可能なスタンドアロンスクリプトです。モジュールは定義されたインターフェースを提供し、引数を受け入れ、終了前に JSON 文字列を標準出力 (stdout) に出力して Ansible に情報を返します。モジュールは、別々のプロセスのターゲットシステム (通常はリモートシステム) 上で実行します。
* :ref:`プラグイン <plugins_lookup>` は Ansible のコア機能を強化し、``/usr/bin/ansible`` プロセス内のコントロールノードで実行します。プラグインは、Ansible のコア機能のオプションおよび拡張機能を提供します。データ変換、ロギング出力、インベントリーへの接続などです。

.. _local_modules:

モジュールをローカルで追加
=======================
Ansible は、特定のディレクトリーにあるすべての実行ファイルをモジュールとして自動的に読み込むため、以下の場所にローカルモジュールを作成または追加できます。

* ``ANSIBLE_LIBRARY`` 環境変数に追加されたディレクトリー (``$ANSIBLE_LIBRARY`` は、``$PATH`` のようにコロンで区切られたリストを取ります)
* ``~/.ansible/plugins/modules/``
* ``/usr/share/ansible/plugins/modules/``

モジュールファイルをこのいずれかの場所に保存すると、Ansible はそのファイルを読み込み、ローカルのタスク、Playbook、またはロールで使用できます。

``my_custom_module`` が利用できることを確認するには、以下を行います。

* ``ansible-doc -t module my_custom_module`` と入力します。そのモジュールのドキュメントが表示されるはずです。

ローカルモジュールを特定の Playbook でのみ使用するには、以下を行います。

* これを、Playbook を含むディレクトリーの ``library`` サブディレクトリーに保存します。

ローカルモジュールを 1 つのロールでのみ使用するには、以下を行います。

* このロール内の ``library`` と呼ばれるサブディレクトリーに格納します。

.. _distributing_plugins:
.. _local_plugins:

プラグインをローカルで追加
=======================
Ansible はプラグインを自動的に読み込み、プラグインのタイプに応じた名前が付けられたディレクトリーから、各タイプのプラグインを個別に読み込みます。以下は、プラグインディレクトリー名の一覧です。

    * action_plugins*
    * cache_plugins
    * callback_plugins
    * connection_plugins
    * filter_plugins*
    * inventory_plugins
    * lookup_plugins
    * shell_plugins
    * strategy_plugins
    * test_plugins*
    * vars_plugins

ローカルプラグインを自動的に読み込むには、以下の場所のいずれかにローカルプラグインを作成または追加します。

* 関連する ``ANSIBLE_plugin_type_PLUGINS`` 環境変数に追加されるディレクトリー (``$ANSIBLE_INVENTORY_PLUGINS``、``$ANSIBLE_VARS_PLUGINS`` などの変数は、``$PATH`` などのコロンで区切られたリストを取得します)
* ``~/.ansible/plugins/`` 内で適切な ``plugin_type`` の名前が付けられたディレクトリー (``~/.ansible/plugins/callback`` など)
* ``/usr/share/ansible/plugins/`` 内の適切な ``plugin_type`` の名前が付けられたディレクトリー (``/usr/share/ansible/plugins/action`` など)

プラグインファイルがこれらの場所のいずれかに置かれると、Ansible はそのファイルを読み込み、ローカルのモジュール、タスク、Playbook、またはロールで使用できます。または、``ansible.cfg`` ファイルを編集して、ローカルプラグインを含むディレクトリーを追加することもできます。詳細は「:ref:`ansible_configuration_settings`」を参照してください。

``plugins/plugin_type/my_custom_plugin`` が利用可能であることを確認するには、以下を行います。

* ``ansible-doc -t <plugin_type> my_custom_lookup_plugin`` と入力します。たとえば、``ansible-doc -t lookup my_custom_lookup_plugin`` です。そのプラグインのドキュメントが表示されるはずです。これは、上記の一覧で ``*`` のマークが付いたプラグインタイプを除くすべてのプラグインタイプで機能します。詳細は、:ref:`ansible-doc` を参照してください。

ローカルプラグインを特定の Playbook でのみ使用するには、以下を行います。

* これを Playbook を含むディレクトリーの適切な ``plugin_type`` (``callback_plugins`` または ``inventory_plugins`` など) のサブディレクトリーに保存します。

ローカルプラグインを 1 つのロールでのみ使用するには、以下を行います。

* ロール内の適切な ``plugin_type (``cache_plugins``、``strategy_plugins`` など) のサブディレクトリーに保存します。

ロールの一部として同梱されると、ロールがプレイで呼び出されるとすぐにプラグインが利用可能になります。
