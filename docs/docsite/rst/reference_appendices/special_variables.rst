.. _special_variables:

特別な変数
=================

マジック
-----
マジック変数は、ユーザーが直接設定できません。Ansible がシステム内の状態を反映してこの変数を常にオーバーライドします。

ansible_check_mode
    チェックモードかどうかを指定するブール値

ansible_dependent_role_names
    他のプレイの依存関係として現在のプレイにインポートされているロールの名前

ansible_diff_mode
    diff モードかどうかを指定するブール値

ansible_forks
    今回の実行で利用可能な最大フォーク数 (整数)

ansible_inventory_sources
    インベントリーとして使用されるソースの一覧

ansible_limit
    Ansible の現在の実行に対して、CLI オプション ``--limit`` として指定する内容

ansible_loop
    ``loop_control.extended`` で有効にした場合に loop の拡張情報を含むディクショナリー/マップ

ansible_loop_var
    ``loop_control.loop_var`` に渡す値の名前。``2.8`` で追加

ansible_index_var
    ``loop_control.index_var`` に渡す値の名前。``2.9`` で追加

ansible_parent_role_names
    現在のロールが :ref:`include_role <include_role_module>` アクションまたは :ref:`import_role <import_role_module>` アクションで実行されていると、この変数には親のロールの全一覧と、その一覧の最初の項目である最新のロール (このロールを追加/インポートしたロール) が含まれます。
    複数の包含がある場合には、この一覧は *最後* のロール (このロールに含まれるロール) を、一覧の *最初* の項目として一覧に追加します。固有のロールを一覧に複数回存在させることも可能です。

    例:ロール **A** にロール **B** に含まれている場合、ロール B の内部では ``ansible_parent_role_names`` は ``['A']`` と等しくなります。If role **B** then includes role **C**, the list becomes ``['B', 'A']``.

ansible_parent_role_paths
    現在のロールが :ref:`include_role <include_role_module>` アクションまたは :ref:`import_role <import_role_module>` アクションで実行されていると、この変数には親のロールの全一覧と、その一覧の最初の項目である最新のロール (このロールを追加/インポートしたロール) が含まれます。
    この一覧の順番は、``ansible_parent_role_names`` を参照してください。

ansible_play_batch
    シリアルで制限される現在のプレイ実行に含まれるアクティブなホスト一覧 (「バッチ」と呼ばれます)。失敗したホストや到達不可能なホストは、「アクティブ」とはみなされません。

ansible_play_hosts
    Ansible_play_batch と同じ

ansible_play_hosts_all
    プレイが対象としたホストの一覧

ansible_play_role_names
    現在のプレイに現在インポートされているロールの名前。この一覧には、依存関係を介して暗黙的に組み込まれるロール名は **含まれません**
    。

ansible_playbook_python
    Ansible が使用する Python インタープリターへのコントローラー上のパス

ansible_role_names
    現在のプレイにインポートされているロール名、
    または現在のプレイにインポートされているロールの依存関係として参照されているロール名

ansible_run_tags
    CLI オプション ``--tags`` の内容。現在の実行に含まれるタグを指定します。

ansible_search_path
    アクションプラグインとルックアップの現在の検索パス。``template: src=myfile`` を指定したときに検索する相対パスです。

ansible_skip_tags
    CLI オプション ``--skip_tags`` の内容。このオプションでは、現在の実行で省略するタグを指定します。

ansible_verbosity
    Ansible の現在の詳細レベル設定

ansible_version
   現在実行の Ansible のバージョンに関する情報を含むディクショナリー/マップ。full、major、minor、revision、string などのキーが含まれます。

group_names
    現在のホストが所属するグループの一覧

groups
    インベントリー内の全グループを含むディクショナリー/マップ。各グループには、所属するホストの一覧が含まれます。

hostvars
    インベントリー内の全ホスト、そのホストに割当てられた変数を含むディクショナリー/マップ。

inventory_hostname
    プレイで繰り返される「現在」のホストのイベントリー名

inventory_hostname_short
    `inventory_hostname` の短縮版

inventory_dir
    `inventory_hostname` を最初に定義したインベントリーソースのディレクトリー

inventory_file
    `inventory_hostname` を最初に定義したインベントリーソースのファイル名

omit
    タスクのオプションを省略できるようにする特別変数 (つまり ``- user: name=bob home={{ bobs_home|default(omit) }}``)

play_hosts
    非推奨。ansible_play_batch と同じです。

ansible_play_name
    現在実行されているプレイの名前。``2.8`` で追加されました。

playbook_dir
    ``ansible-playbook`` コマンドラインに渡した Playbook のディレクトリーへのパス

role_name
    現在実行中のロール名

role_names
    非推奨。ansible_play_role_names と同じです。

role_path
    現在実行中のロールのディレクトリーへのパス

ファクト
-----
ファクト (Fact) は、現在のホストに関連する情報 (`inventory_hostname`) を含む変数です。この変数は、最初に収集した場合にのみ利用できます。

ansible_facts
    `inventory_hostname` が収集またはキャッシュする「ファクト」が含まれます。
    ファクトは通常、:ref:`setup <setup_module>` モジュールによって再生されますが、すべてのモジュールはファクトを返すことができます。

ansible_local
    `inventory_hostname` が収集またはキャッシュする「ローカルファクト」が含まれます。
    利用可能なキーは、作成したカスタムファクトによって異なります。
    詳細は、:ref:`setup <setup_module>` モジュールを参照してください。

.. _connection_variables:

接続変数
---------------------
接続変数は通常、ターゲットでのアクション実行方法を具体的に設定する時に使用します。接続変数の大半が connection プラグインに対応しますが、connection プラグイン固有のものではなく、通常は shell、terminal、become などの他のプラグインも使用します。
各 connection/become/shell/etc プラグインは、自身のオーバーライドや固有の変数を定義するため、一般的なもののみを説明します。
接続変数が :ref:`構成設定<ansible_configuration_settings>`、:ref:`コマンドラインオプション<command_line_tools>`、および :ref:`Playbook キーワード<playbook_keywords>` と相互作用する方法は、:ref:`general_precedence_rules` を参照してください。

ansible_become_user
    特権昇格後に Ansible が昇格するユーザーこのユーザーは、「ログインユーザー」が利用できる必要があります。

ansible_connection
    ターゲットホストでタスクに実際に使用する connection プラグイン

ansible_host
    `inventory_hostname` の代わりに使用するターゲットホストの ip/名前

ansible_python_interpreter
    Ansible がターゲットホストで使用すべき Python 実行ファイルへのパス

ansible_user
    Ansible がログインするユーザー
