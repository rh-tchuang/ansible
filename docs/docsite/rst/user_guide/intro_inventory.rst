.. _intro_inventory:
.. _inventory:

***************************
インベントリーの構築方法
***************************

Ansible は、インベントリーと呼ばれるリスト、またはリストのグループを使用して、インフラストラクチャーにある複数の管理ノードまたは「ホスト」に対して同時に機能します。インベントリーが定義されたら、:ref:`パターン<intro_patterns>` を使用して Ansible で実行するホストまたはグループを選択します。

インベントリーのデフォルトの場所は、``/etc/ansible/hosts`` ファイルです。``-i <path>`` オプションを使用して、コマンドラインで別のインベントリーファイルを指定できます。また、「:ref:`intro_dynamic_inventory`」で説明されているように、複数のインベントリーファイルを同時に使用したり、動的またはクラウドのソースまたは異なる形式 (YAML、ini など) から複数のインベントリーを取得 (プル) することもできます。
バージョン 2.4 で導入された Ansible には、この柔軟でカスタマイズ可能な :ref:`inventory_plugins` があります。

.. contents::
   :local:

.. _inventoryformat:

インベントリーの基本: 形式、ホスト、およびグループ
============================================

インベントリーファイルは、所有するインベントリープラグインに応じて、以下に示す多くの形式のいずれかになります。
最も一般的な形式は INI および YAML です。基本的な INI である ``/etc/ansible/hosts`` は以下のようになります。

.. code-block:: text

    mail.example.com

    [webservers]
    foo.example.com
    bar.example.com

    [dbservers]
    one.example.com
    two.example.com
    three.example.com

括弧内の見出しはグループ名で、ホストを分類し、
どの時点で、どのような目的で、どのホストを制御するかを決定するのに使用されます。

以下は、同じ基本的なインベントリーファイルの YAML 形式です。

.. code-block:: yaml

  all:
    hosts:
      mail.example.com:
    children:
      webservers:
        hosts:
          foo.example.com:
          bar.example.com:
      dbservers:
        hosts:
          one.example.com:
          two.example.com:
          three.example.com:

.. _default_groups:

デフォルトのグループ
--------------

デフォルトグループは ``all`` および ``ungrouped`` です。``all`` グループにはすべてのホストが含まれます。
``ungrouped`` グループには、``all`` 以外のグループがないすべてのホストが含まれます。
すべてのホストは常に 2 つ以上のグループに所属します (``all`` と ``ungrouped``、または ``all`` とその他のグループ)。``all`` および ``ungrouped`` は常に存在しますが、暗黙的であり、``group_names`` のようなグループ一覧に表示されない場合があります。

.. _host_multiple_groups:

複数グループ内のホスト
------------------------

各ホストを複数のグループに配置できます。よく選択される方法です。たとえば、Atlanta のデータセンター内の実稼働 Web サーバーは [prod]、[atlanta]、および [webservers] と呼ばれるグループに含まれる場合があります。以下を追跡するグループを作成できます。

* なにを - アプリケーション、スタック、またはマイクロサービス (データベースサーバー、Web サーバーなど)
* どこで - (ローカル DNS、ストレージなどと通信する) データセンターまたはリージョン (例: 東、西)
* いつ - 実稼働リソースでのテストを回避する開発ステージ (例: 実稼働、テスト)

以前の YAML インベントリーを拡張して、上述の「いつ、どこで、なにを」が含まれるようにします。

.. code-block:: yaml

  all:
    hosts:
      mail.example.com:
    children:
      webservers:
        hosts:
          foo.example.com:
          bar.example.com:
      dbservers:
        hosts:
          one.example.com:
          two.example.com:
          three.example.com:
      east:
        hosts:
          foo.example.com:
          one.example.com:
          two.example.com:
      west:
        hosts:
          bar.example.com:
          three.example.com:
      prod:
        hosts:
          foo.example.com:
          one.example.com:
          two.example.com:
      test:
        hosts:
          bar.example.com:
          three.example.com:

``one.example.com`` が、``dbservers`` グループ、``east`` グループ、および ``prod`` グループに存在することを確認できます。

このインベントリーの ``prod`` および ``test`` を簡素化するために、ネストされたグループを使用することもできます。

.. code-block:: yaml

  all:
    hosts:
      mail.example.com:
    children:
      webservers:
        hosts:
          foo.example.com:
          bar.example.com:
      dbservers:
        hosts:
          one.example.com:
          two.example.com:
          three.example.com:
      east:
        hosts:
          foo.example.com:
          one.example.com:
          two.example.com:
      west:
        hosts:
          bar.example.com:
          three.example.com:
      prod:
        children:
          east:
      test:
        children:
          west:

インベントリーを整理し、ホストをグループ化する方法は、「:ref:`inventory_setup_examples`」を参照してください。

ホスト範囲の追加
----------------------

同様のパターンを持つホストが多数ある場合は、各ホスト名を個別に表示するのではなく、ホストを範囲として追加できます。

INI の場合は、以下のようになります。

.. code-block:: text

    [webservers]
    www[01:50].example.com

YAML の場合は、以下のようになります。

.. code-block:: yaml

    ...
      webservers:
        hosts:
          www[01:50].example.com:

数値のパターンでは、必要に応じて、先頭にゼロを含めるか、または削除できます。範囲が含まれます。また、アルファベットの範囲を定義することもできます。

.. code-block:: text

    [databases]
    db-[a:f].example.com

インベントリーへの変数の追加
=============================

特定のホストまたはグループに関連する変数の値をインベントリーに保存できます。まず、メインのインベントリーファイルのホストおよびグループに変数を直接追加することができます。ただし、管理ノードを Ansible インベントリーに追加するため、変数を別々のホスト変数およびグループ変数のファイルに保存することが推奨されます。

.. _host_variables:

あるマシンへの変数の割り当て: ホスト変数
===================================================

1 台のホストに変数を簡単に割り当てると、後で Playbook で使用できます。INI の場合は、以下のようになります。

.. code-block:: text

   [atlanta]
   host1 http_port=80 maxRequestsPerChild=808
   host2 http_port=303 maxRequestsPerChild=909

YAML の場合は、以下のようになります。

.. code-block:: yaml

    atlanta:
      host1:
        http_port: 80
        maxRequestsPerChild: 808
      host2:
        http_port: 303
        maxRequestsPerChild: 909

非標準の SSH ポートなどの一意な値は、ホスト変数として機能します。コロンを使用してポート番号をホスト名の後に追加することで、ホスト変数として Ansible インベントリーに追加できます。

.. code-block:: text

    badwolf.example.com:5309

接続変数もホスト変数として機能します。

.. code-block:: text

   [targets]

   localhost              ansible_connection=local
   other1.example.com     ansible_connection=ssh        ansible_user=myuser
   other2.example.com     ansible_connection=ssh        ansible_user=myotheruser

.. note:: SSH 設定ファイル内に非標準の SSH ポートの一覧を表示した場合、``openssh`` 接続はそのポートを見つけて使用しますが、``paramiko`` 接続は行われません。

.. _inventory_aliases:

インベントリーエイリアス
-----------------

エイリアスをインベントリーに定義することもできます。

INI の場合は、以下のようになります。

.. code-block:: text

    jumper ansible_port=5555 ansible_host=192.0.2.50

YAML の場合は、以下のようになります。

.. code-block:: yaml

    ...
      hosts:
        jumper:
          ansible_port:5555
          ansible_host:192.0.2.50

上記の例では、ホストエイリアス「jumper」に対して Ansible を実行すると、ポート 5555 で 192.0.2.50 に接続します。
これは、静的 IP があるホスト、またはトンネル経由で接続しているホストでのみ機能します。

.. note::
   ``key=value`` 構文を使用して INI 形式で渡される値が解釈される方法は、宣言される場所に応じて異なります。

   * ホストとインラインで宣言すると、INI 値は Python リテラル構造 (文字列、数値、タプル、リスト、辞書、ブール値、なし) として解釈されます。ホスト行は、行ごとに複数の ``key=value`` パラメーターを受け入れます。そのため、空白文字が区切り文字ではなく値の一部であることを示す方法が必要になります。

   * ``:vars`` セクションで宣言すると、INI 値は文字列として解釈されます。たとえば、``var=FALSE`` は「FALSE」に等しい文字列を作成します。ホスト行とは異なり、``:vars`` セクションは行ごとにエントリーを 1 つしか受け入れないため、``=`` に続くものはすべてエントリーの値である必要があります。

   * INI インベントリーに設定された変数の値を特定のタイプ (文字列やブール値など) にする必要がある場合は、タスクで常にそのタイプをフィルターで指定します。変数の使用時に INI インベントリーに設定されたタイプに依存しないでください。

   * 変数の実際のタイプの混乱を避けるために、インベントリーソースには YAML 形式を使用することを検討してください。YAML インベントリープラグインは、変数の値を一貫して正しく処理します。

通常は、システムポリシーを記述する変数を定義するのが最適な方法ではありません。メインのインベントリーファイルで変数を設定するのは簡単な方法です。「host_vars」ディレクトリーの個別ファイルに変数の値を保存するガイドラインは、「:ref:`splitting_out_vars`」を参照してください。

.. _group_variables:

多くのマシンへの変数の割り当て: グループ変数
======================================================

グループのすべてのホストが変数値を共有している場合は、その変数をグループ全体に一度に適用できます。INI の場合は、以下のようになります。

.. code-block:: text

   [atlanta]
   host1
   host2

   [atlanta:vars]
   ntp_server=ntp.atlanta.example.com
   proxy=proxy.atlanta.example.com

YAML の場合は、以下のようになります。

.. code-block:: yaml

    atlanta:
      hosts:
        host1:
        host2:
      vars:
        ntp_server: ntp.atlanta.example.com
        proxy: proxy.atlanta.example.com

グループ変数は、変数を複数のホストに同時に適用する便利な方法です。ただし、Ansible を実行する前に、インベントリー変数などの変数は常にホストレベルにフラットにします。ホストが複数グループのメンバーである場合、Ansible は、そのすべてのグループから変数の値を読み取ります。異なるグループ内の同じ変数に異なる値を割り当てる場合、Ansible は内部の :ref:`マージ用ルール<how_we_merge>` に基づいて、使用する値を選択します。

.. _subgroups:

変数値の継承: グループのグループ用グループ変数
----------------------------------------------------------------

INI の ``:children`` 接尾辞または YAML の ``children:`` エントリーを使用して、グループのグループを作成できます。
変数は、``:vars`` または ``vars:`` を使用して、これらのグループのグループに適用できます。

INI の場合は、以下のようになります。

.. code-block:: text

   [atlanta]
   host1
   host2

   [raleigh]
   host2
   host3

   [southeast:children]
   atlanta
   raleigh

   [southeast:vars]
   some_server=foo.southeast.example.com
   halon_system_timeout=30
   self_destruct_countdown=60
   escape_pods=2

   [usa:children]
   southeast
   northeast
   southwest
   northwest

YAML の場合は、以下のようになります。

.. code-block:: yaml

  all:
    children:
      usa:
        children:
          southeast:
            children:
              atlanta:
                hosts:
                  host1:
                  host2:
              raleigh:
                hosts:
                  host2:
                  host3:
            vars:
              some_server: foo.southeast.example.com
              halon_system_timeout: 30
              self_destruct_countdown: 60
              escape_pods: 2
          northeast:
          northwest:
          southwest:

一覧またはハッシュデータを保存する必要がある場合や、インベントリーファイルとは別にホストおよびグループ固有の変数を保持する必要がある場合は、:ref:`splitting_out_vars` を参照してください。

子グループには以下のプロパティーがあります。

 - 子グループのメンバーであるホストは、自動的に親グループのメンバーになります。
 - 子グループの変数は、親グループの変数よりも優先度が高くなります (オーバライド)。
 - グループに複数の親と子を追加することはできますが、循環関係は設定できません。
 - ホストは複数のグループに属することもできますが、ホストのインスタンスは **1 つ** だけであり、複数のグループからのデータをマージします。

.. _splitting_out_vars:

ホスト変数とグループ変数の整理
===================================

メインのインベントリーファイルに変数を格納できますが、個別のホスト変数とグループ変数のファイルを保存すると、変数値をより簡単に整理できる場合があります。ホスト変数およびグループの変数のファイルでは YAML 構文を使用する必要があります。有効なファイル拡張子は「.yml」、「.yaml」、「.json」です。ファイルに拡張子を付けなくても有効です。
YAML を初めて使用する場合は、:ref:`yaml_syntax` を参照してください。

Ansible は、インベントリーファイルまたは Playbook ファイルの相対パスを検索して、ホスト変数およびグループ変数のファイルを読み込みます。``/etc/ansible/hosts`` のインベントリーファイルに、「raleigh」および「webservers」というグループに属する「foosball」という名前のホストが含まれる場合、そのホストは次の場所にある YAML ファイルの変数を使用します。

.. code-block:: bash

    /etc/ansible/group_vars/raleigh # can optionally end in '.yml', '.yaml', or '.json'
    /etc/ansible/group_vars/webservers
    /etc/ansible/host_vars/foosball

たとえば、インベントリー内のホストをデータセンターごとにまとめ、各データセンターが独自の NTP サーバーおよびデータベースサーバーを使用する場合は、``/etc/ansible/group_vars/raleigh`` という名前のファイルを作成して、``raleigh`` グループの変数を保存できます。

.. code-block:: yaml

    ---
    ntp_server: acme.example.org
    database_server: storage.example.org

グループまたはホストの後に、名前を付けた *ディレクトリー* を作成することもできます。Ansible は、これらのディレクトリー内のすべてのファイルを辞書順で読み取ります。以下は、「raleigh」グループを使用した例となります。

.. code-block:: bash

    /etc/ansible/group_vars/raleigh/db_settings
    /etc/ansible/group_vars/raleigh/cluster_settings

「raleigh」グループのすべてのホストには、
これらのファイルで定義された変数が使用されます。これは、1 つのファイルが大きすぎる場合や、一部のグループ変数で Ansible Vault を使用する場合に、
お使いの変数を整理しておくのに非常に役立ちます。

``group_vars/`` ディレクトリーおよび ``host_vars/`` ディレクトリーを Playbook ディレクトリーに追加することもできます。``ansible-playbook`` コマンドは、デフォルトでこのようなディレクトリーを現在の作業ディレクトリーで検索します。他の Ansible コマンド (``ansible``、``ansible-console`` など) は、インベントリーディレクトリーで ``group_vars/`` および ``host_vars/`` のみを検索します。Playbook ディレクトリーからグループ変数およびホスト変数を読み込む他のコマンドが必要な場合は、コマンドラインで ``--playbook-dir`` オプションを指定する必要があります。
Playbook ディレクトリーとインベントリーディレクトリーの両方からインベントリーファイルを読み込む場合、Playbook ディレクトリーの変数は、インベントリーディレクトリーに設定された変数を上書きします。

git リポジトリー (または他のバージョン管理) でインベントリーファイルおよび変数を維持することは、
インベントリーおよびホスト変数への変更を追跡する優れた方法です。

.. _how_we_merge:

変数をマージする方法
========================

デフォルトでは、変数は、プレイの実行前に特定ホストにマージまたはフラット化されます。これにより、Ansible はホストとタスクに焦点を当てたままになるため、グループはインベントリーとホストの一致以外では残れません。デフォルトでは、Ansible はグループやホストに定義された変数を含む変数を上書きします (:ref:`DEFAULT_HASH_BEHAVIOUR<DEFAULT_HASH_BEHAVIOUR>` を参照)。順序/優先順位は「最低から最高へ」です。

- すべてのグループ (他のすべてのグループの「親」であるため)
- 親グループ
- 子グループ
- ホスト

デフォルトでは、Ansible は同じ親/子レベルでグループをマージし、最後に読み込まれたグループは以前のグループを上書きします。たとえば、a_group は b_group とマージされ、一致する b_group の変数は、a_group の変数を上書きします。

この動作を変更するには、グループ変数 ``ansible_group_priority`` を設定し、同じレベルのグループのマージ順序を変更します (親/子順序の解決後)。数値が大きいほど、後の数字がマージされ、優先度が高くなります。この変数が設定されていないと、デフォルトは ``1`` になります。例:

.. code-block:: yaml

    a_group:
        testvar: a
        ansible_group_priority:10
    b_group:
        testvar: b

この例では、両方のグループの優先順位が同じ場合、結果は通常 ``testvar == b`` になりますが、``a_group`` の優先度が高いため、結果は ``testvar == a`` になります。

.. note:: ``ansible_group_priority`` は、group_vars/ ではなくインベントリーソースでのみ設定でき、group_vars の読み込みで変数が使用されるため設定できます。

.. _using_multiple_inventory_sources:

複数のインベントリーソースの使用
================================

コマンドラインから複数のインベントリーパラメーターを指定するか、
ANSIBLE_INVENTORY を構成することにより、複数のインベントリーリソース (ディレクトリー、動的インベントリースクリプト、
またはインベントリープラグインによりサポートされるファイル) を同時に対象に指定できます。これは、特定のアクションに対して、ステージ環境や実稼働環境など、
通常は異なる環境を同時に対象に指定する場合に役立ちます。

以下のようなコマンドラインから 2 つのソースを対象とします。

.. code-block:: bash

    ansible-playbook get_logs.yml -i staging -i production

インベントリーに変数の競合がある場合、
その競合は「:ref:`how_we_merge`」および「:ref:`ansible_variable_precedence`」で説明されているルールに従って解決されることに注意してください。
マージの順序はインベントリーソースパラメーターの順序で制御されます。
ステージングインベントリーの ``[all:vars]`` で ``myvar = 1`` が定義され、実稼働インベントリーで ``myvar = 2`` が定義されると、
Playbook は ``myvar = 2`` で実行されます。Playbook を -i production -i staging で実行すると、
結果は逆になります。

**インベントリソースをディレクトリーに集約**

また、ディレクトリーで複数のインベントリーソースとソースタイプを組み合わせてインベントリーを作成することもできます。
これは、静的ホストと動的ホストを組み合わせて、1 つのインベントリーとして管理するのに役立ちます。
以下のインベントリーは、インベントリープラグインソース、動的インベントリースクリプト、
およびファイルを静的ホストと組み合わせたものです。

.. code-block:: text

    inventory/
      openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      dynamic-inventory.py   # add additional hosts with dynamic inventory script
      static-inventory       # add static hosts and groups
      group_vars/
        all.yml              # assign variables to all hosts

このインベントリーディレクトリーは、次のように簡単に対象に設定できます。

.. code-block:: bash

    ansible-playbook example.yml -i inventory

他のインベントリーソースに対する変数の競合またはグループのグループの依存関係がある場合は、
インベントリーソースのマージ順序を制御すると役に立ちます。インベントリーはファイル名に従って
アルファベット順にマージされるため、
ファイルに接頭辞を追加することで結果を制御できます。

.. code-block:: text

    inventory/
      01-openstack.yml          # configure inventory plugin to get hosts from Openstack cloud
      02-dynamic-inventory.py   # add additional hosts with dynamic inventory script
      03-static-inventory       # add static hosts
      group_vars/
        all.yml                 # assign variables to all hosts

``01-openstack.yml`` がグループ ``all`` に ``myvar = 1`` を定義し、``02-dynamic-inventory.py`` が ``myvar = 2`` を定義し、
``03-static-inventory`` が ``myvar = 3`` を定義すると、Playbook は ``myvar = 3`` で実行されます。

インベントリープラグインおよび動的インベントリースクリプトの詳細は、:ref:`inventory_plugins` および :ref:`intro_dynamic_inventory` を参照してください。

.. _behavioral_parameters:

ホストへの接続: 動作用のインベントリーパラメーター
====================================================

上記のように、以下の変数を設定して、Ansible がリモートホストと対話する方法を制御します。

ホスト接続:

.. include:: shared_snippets/SSH_password_prompt.txt

ansible_connection
    ホストへの接続の種類。これには、ansible の接続プラグインの名前を使用できます。SSH プロトコルタイプは、``smart``、``ssh``、または ``paramiko`` です。 デフォルトは smart です。SSH 以外のタイプは、次のセクションで説明します。

すべての接続に対する一般的な設定:

ansible_host
    接続するホストの名前 (割り当てたいエイリアスと異なる場合)。
ansible_port
    デフォルトではない場合 (ssh の場合は 22) は、接続ポート番号。
ansible_user
    ホストに接続する際に使用するユーザー名。
ansible_password
    ホストへの認証に使用するパスワード (この変数をプレーンテキストで保存しないでください。常に Valut を使用してください。「:ref:`best_practices_for_variables_and_vaults`」を参照してください。)


SSH 接続に固有のキー:

ansible_ssh_private_key_file
    ssh が使用する秘密鍵ファイル。 複数のキーを使用し、SSH エージェントを使用しない場合に便利です。
ansible_ssh_common_args
    この設定は、常に :command:`sftp`、:command:`scp`、
    および :command:`ssh` のデフォルトのコマンドラインに追加されます。特定のホスト (またはグループ) に ``ProxyCommand`` 
    を設定するのに便利です。
ansible_sftp_extra_args
    この設定は、常にデフォルトの :command:`sftp` コマンドラインに追加されます。
ansible_scp_extra_args
    この設定は、常にデフォルトの :command:`scp` コマンドラインに追加されます。
ansible_ssh_extra_args
    この設定は、常にデフォルトの :command:`ssh` コマンドラインに追加されます。
ansible_ssh_pipelining
    SSH パイプを使用するかどうかを決定します。これにより、:file:`ansible.cfg` の ``pipelining`` 設定を上書きできます。
ansible_ssh_executable (バージョン 2.2 で追加)
    この設定により、システムの :command:`ssh` を使用するデフォルトの動作が上書きされます。これにより、:file:`ansible.cfg` の ``ssh_executable`` 設定を上書きできます。


権限の昇格 (詳細は :ref:`Ansible Privilege Escalation<become>` を参照):

ansible_become
    ``ansible_sudo`` または ``ansible_su`` と同等です。これにより、権限のエスカレーションを強制できます。
ansible_become_method
    権限昇格メソッドの設定を許可します。
ansible_become_user
    ``ansible_sudo_user`` または ``ansible_su_user`` と同等で、権限の昇格でユーザーを設定できます。
ansible_become_password
    ``ansible_sudo_password`` または ``ansible_su_password`` と同等で、特権昇格パスワードを設定できます (この変数をプレーンテキストで保存しないでください。常に Valut を使用してください。「:ref:`best_practices_for_variables_and_vaults`」を参照してください。)
ansible_become_exe
    ``ansible_sudo_exe`` または ``ansible_su_exe`` と同等で、選択した昇格メソッドの実行ファイルを設定できます。
ansible_become_flags
    ``ansible_sudo_flags`` または ``ansible_su_flags`` と同等で、選択した昇格メソッドに渡すフラグを設定できます。これは、``sudo_flags`` オプションの :file:`ansible.cfg` でグローバルに設定することもできます。

リモートホスト環境パラメーター:

.. _ansible_shell_type:

ansible_shell_type
    ターゲットシステムのシェルタイプ。:ref:`ansible_shell_executable<ansible_shell_executable>` を非 Bourne (sh) 互換シェルに設定しない限り、
    この設定は使用しないでください。 デフォルトのコマンドは、
    ``sh`` スタイルの構文を使用してフォーマットされます。 これを ``csh`` または ``fish`` に設定すると、
    ターゲットシステムで実行されるコマンドがシェルの構文に従います。

.. _ansible_python_interpreter:

ansible_python_interpreter
    ターゲットホストの Python のパス。これは、複数の Python があるシステム、
    または \*BSD などの :command:`/usr/bin/python` にないシステム、または :command:`/usr/bin/python` が 
    2.X シリーズの Python 以外のシステムに役に立ちます。 :command:`/usr/bin/env` メカニズムは使用しません。
    リモートユーザーのパスを正しく設定する必要があり、また :program:`python` 実行ファイルの名前が python であることを前提としています。
    実行ファイルの名前は、:program:`python2.6` のようになります。

ansible_*_interpreter
    ruby や perl などのあらゆるもので動作し、:ref:`ansible_python_interpreter<ansible_python_interpreter>` と同じように機能します。
    これは、そのホストで実行するモジュールのシバンに代わるものです。

.. versionadded:: 2.1

.. _ansible_shell_executable:

ansible_shell_executable
    ansible コントローラーがターゲットマシンで使用するシェルを設定し、
    :file:`ansible.cfg` の ``executable`` を上書きします。
    このデフォルトは :command:`/bin/sh` です。 :command:`/bin/sh` を使用できない場合 
    (つまり :command:`/bin/sh` がターゲットマシンにインストールされず、
    sudo から実行できない場合) に限り変更してください。

Ansible-INI ホストファイルの例:

.. code-block:: text

  some_host         ansible_port=2222     ansible_user=manager
  aws_host          ansible_ssh_private_key_file=/home/example/.ssh/aws.pem
  freebsd_host      ansible_python_interpreter=/usr/local/bin/python
  ruby_module_host  ansible_ruby_interpreter=/usr/bin/ruby.1.9.3

SSH 以外の接続タイプ
------------------------

前のセクションで説明したように、Ansible は SSH で Playbook を実行しますが、接続タイプはこれに限定されません。
ホスト固有のパラメーター ``ansible_connection=<connector>`` を使用すると、接続タイプを変更できます。
SSH ベースでない以下のコネクターを利用できます。

**local**

このコネクターは、Playbook をコントロールマシン自体にデプロイするために使用できます。

**docker**

このコネクターは、ローカルの Docker クライアントを使用して Playbook を直接 Docker コンテナーにデプロイします。以下のパラメーターは、このコネクターにより処理されます。

ansible_host
    接続先の Docker コンテナーの名前。
ansible_user
    コンテナー内で動作するユーザー名。ユーザーはコンテナー内に存在している必要があります。
ansible_become
    ``true`` に設定すると、``become_user`` はコンテナー内で動作するために使用されます。
ansible_docker_extra_args
    Docker が認識する追加の引数を持つ文字列を指定できますが、これはコマンド固有ではありません。このパラメーターは、主に、使用するリモート Docker デーモンを設定するために使用されます。

以下は、作成されたコンテナーに即時にデプロイする例を示しています。

.. code-block:: yaml

   - name: create jenkins container
     docker_container:
       docker_host: myserver.net:4243
       name: my_jenkins
       image: jenkins

   - name: add container to inventory
     add_host:
       name: my_jenkins
       ansible_connection: docker
       ansible_docker_extra_args: "--tlsverify --tlscacert=/path/to/ca.pem --tlscert=/path/to/client-cert.pem --tlskey=/path/to/client-key.pem -H=tcp://myserver.net:4243"
       ansible_user: jenkins
     changed_when: false

   - name: create directory for ssh keys
     delegate_to: my_jenkins
     file:
       path: "/var/jenkins_home/.ssh/jupiter"
       state: directory

利用可能なプラグインとサンプルの一覧は、:ref:`connection_plugin_list` を参照してください。

.. note:: ドキュメントを最初から読んでいる場合は、これが Ansibleプレイブックの初めての例になるかもしれません。これはインベントリーファイルではありません。
          Playbook については、ドキュメントで後ほど詳細に説明します。

.. _inventory_setup_examples:

インベントリーの設定例
========================

.. _inventory_setup-per_environment:

例:環境ごとのインベントリー
--------------------------------------

複数の環境を管理する必要がある場合は、
インベントリーごとに 1 つの環境のホストのみを定義することが推奨されます。これにより、
実際に、
「ステージング」サーバーを更新する必要がある場合などに、
「テスト」環境内のノードの状態を誤って変更する可能性が減ります。

上記の例では、
:file:`inventory_test` ファイルを使用できます。

.. code-block:: ini

  [dbservers]
  db01.test.example.com
  db02.test.example.com

  [appservers]
  app01.test.example.com
  app02.test.example.com
  app03.test.example.com

このファイルには、
「テスト」環境の一部であるホストのみが含まれます。:file:`inventory_staging` と呼ばれる別のファイルで
「ステージング」マシンを定義します。

.. code-block:: ini

  [dbservers]
  db01.staging.example.com
  db02.staging.example.com

  [appservers]
  app01.staging.example.com
  app02.staging.example.com
  app03.staging.example.com

:file:`site.yml` という名前の Playbook を、
テスト環境のすべてのアプリケーションサーバーに適用するには、
次のコマンドを使用します。

  ansible-playbook -i inventory_test site.yml -l appservers

.. _inventory_setup-per_function:

例:機能別にグループ化
--------------------------

前のセクションでは、
同じ機能を持つホストをクラスター化するためにグループを使用する例を説明しました。これにより、
たとえば、データベースサーバーに影響を与えることなく、
Playbook またはロール内でファイアウォールルールを定義できます。

.. code-block:: yaml

  - hosts: dbservers
    tasks:
    - name: allow access from 10.0.0.1
      iptables:
        chain: INPUT
        jump: ACCEPT
        source: 10.0.0.1

.. _inventory_setup-per_location:

例: ロケーション別にグループ化
--------------------------

他のタスクは、特定のホストが置かれる場所が重要になる可能性があります。たとえば、
``db01.test.example.com`` および ``app01.test.example.com`` が DC1 にあり、
``db02.test.example.com`` が DC2 にあるとします。

.. code-block:: ini

  [dc1]
  db01.test.example.com
  app01.test.example.com

  [dc2]
  db02.test.example.com

実際には、
たとえば特定のデータセンター内のすべてのノードを更新する日と、
置かれている場所に関係なくすべてのアプリケーションサーバーを更新する日が必要になるため、
このすべての設定を組み合わせて使用することがあります。

.. seealso::

   :ref:`inventory_plugins`
       動的ソースまたは静的ソースからのインベントリーのプル
   :ref:`intro_dynamic_inventory`
       クラウドプロバイダーなどの動的ソースからのインベントリーのプル
   :ref:`intro_adhoc`
       基本コマンドの例
   :ref:`working_with_playbooks`
       Ansible の設定、デプロイメント、オーケストレーション言語について
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
