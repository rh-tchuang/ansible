.. _general_precedence_rules:

Ansible の動作の制御：優先順位のルール
=================================================

Ansible には、環境に最大限の柔軟性をもたせられるように、管理対象ノードへの接続方法や、接続後の動作など Ansible の動作を制御する手段が多数あります。
Ansible を使用して多数のサーバー、ネットワークデバイス、クラウドリソースを管理する場合に、Ansible の動作をさまざまな場所で定義して、さまざまな方法で Ansible にその情報を渡すことができます。
柔軟性があると便利ですが、優先順位ルールを理解していない場合には、逆効果となる可能性があります。

このような優先順位ルールは、複数の方法で定義できるオプション (設定オプション、コマンドラインオプション、Playbook キーワード、変数) に適用されます。

.. contents::
   :local:

優先順位のカテゴリー
---------------------

Ansible では、動作の制御に使用するソースが 4 つあります。カテゴリーは以下のとおりです (優先順位の低いもの (最も簡単にオーバーライドされる) から高いもの (他のすべてをオーバーライドする)に並べています)。

 * 設定オプション
 * コマンドラインオプション
 * Playbook キーワード
 * 変数

各カテゴリーは、そのカテゴリーよりも優先順位の低いカテゴリーからの情報をすべてオーバーライドします。たとえば、Playbook キーワードは、設定オプションをオーバーライドします。

各優先順位カテゴリーで、固有のルールが適用されます。ただし、一般的に「最後に定義 (last defined)」の内容が優先度が高く、以前の定義をオーバーライドします。

設定オプション
^^^^^^^^^^^^^^^^^^^^^^

:ref:`設定オプション<ansible_configuration_settings>` には ``ansible.cfg`` ファイルと環境変数の両方の値が含まれます。このカテゴリーでは、設定ファイルに指定した値のほうが優先順位が低くなります。Ansible は最初に検出した ``ansible.cfg`` ファイルを使用して、それ以外はすべて無視します。また、Ansible は``ansible.cfg`` がないか、以下の場所を上から順に検索します。

 * ``ANSIBLE_CONFIG`` (環境変数が設定されている場合)
 * ``ansible.cfg`` (現在のディレクトリー)
 * ``~/.ansible.cfg`` (ホームディレクトリー)
 * ``/etc/ansible/ansible.cfg``

環境変数は、``ansible.cfg`` のエントリーよりも優先順位が高くなっています。コントロールノードに環境変数を設定している場合には、Ansible が読み込む ``ansible.cfg`` ファイルの設定よりも、環境変数が優先されます。指定された環境変数の値は、Shell の通常の優先順位 (最後に定義した値が、それ以前の値をオーバーライド) に準拠します。

コマンドラインオプション
^^^^^^^^^^^^^^^^^^^^

コマンドラインオプションは、設定オプションをすべてオーバーライドします。

コマンドラインに直接入力すると、手動で入力した値が、それ以外の設定をすべてオーバーライドするように感じますが、Ansible の仕様は異なります。コマンドラインオプションの優先順位は低いため、オーバーライドできるのは、設定のみです。Playbook のキーワードや、インベントリーからの変数、Playbook から変数をオーバーライドすることはありません。

:ref:`general_precedence_extra_vars` を使用すると、コマンドライン以外の優先順位カテゴリーの他のソースからの設定をすべて、コマンドラインでオーバーライドできますが、これはコマンドラインオプションではなく、:ref:`variable<general_precedence_variables>` を渡す手段としてコマンドラインを使用しています。

コマンドラインで、単一の値しか許容できないパラメーターに複数の値を指定すると、最後に定義した値が優先されます。たとえば、以下の :ref:`ad-hoc task<intro_adhoc>` では、``mike`` ではなく、``carol`` として接続されます::

      ansible -u mike -m ping myhost -u carol

パラメーターによっては、複数の値を使用できます。以下の場合には、Ansible は、インベントリーファイル「inventory1」と「inventory2」に記載されているホストからの値をすべて追加します。

   ansible -i /path/inventory1 -i /path/inventory2 -m ping all

各 :ref:`コマンドラインツール<command_line_tools>` のヘルプは、対象のツールで利用可能なオプションを表示します。

Playbook キーワード
^^^^^^^^^^^^^^^^^

変数は、:ref:`Playbook のキーワード<playbook_keywords>`、コマンドラインオプション、設定オプションをすべてオーバーライドします。

Playbook キーワード内の優先順位は、Playbook の内容 (一般的な設定より具体的な設定が優先される) により左右されます。

- プレイ (最も一般的)
- blocks/includes/imports/roles (任意、タスクを含めることも、blocks/includes/imports/roles の設定を相互に含めることができる)
- タスク (最も具体的)

簡単な例::

   - hosts: all
     connection: ssh
     tasks:
       - name:This task uses ssh.
         ping:

       - name:This task uses paramiko.
         connection: paramiko
         ping:

この例では、``connection`` キーワードは、プレイレベルで ``ssh`` に設定されます。最初のタスクはこの値を継承して、``ssh`` を使用して接続します。次のタスクはこの値を継承してオーバーライドし、``paramiko`` を使用して接続します。
blocks や roles でも同じロジックが適用されます。プレイ内の task、block、role はすべて、プレイレベルのキーワードを継承します。キーワードより task または block、role を優先させるには、task、block、role 内の対象のキーワードに異なる値を定義します。

上記は、変数ではなく、キーワードである点に注意してください。Playbook や変数ファイルはいずれも YAML で設定しますが、それぞれ重要性が異なります。
Playbook はコマンドまたは Ansible の「状態記述」構造で、変数は Playbook をより動的に使用できるようにするためのデータです。

.. _general_precedence_variables:

変数
^^^^^^^^^

変数は、Playbook のキーワード、コマンドラインオプション、設定オプションすべてをオーバーライドします。

同等の Playbook キーワード、コマンドラインオプション、および設定オプションを含む変数は :ref:`connection_variables` と呼ばれています。このカテゴリーは、当初は設定パラメーター向けに設計されてましたが、一時ディレクトリーや Python インタープリターなど、他のコア変数を含めるように拡張されました。

接続変数はすべての変数と同様に、複数の手法や場所で設定できます。ホストとグループの変数は、:ref:`インベントリー<intro_inventory>` で定義できます。:ref:`playbooks<about_playbooks>` の ``vars:`` ブロックで、タスクとプレイの変数を定義できます。ただし、上記は、キーワードや設定オプションではなく、データを格納する変数です。Playbook キーワード、コマンドラインオプション、設定オプションをオーバーライドする変数は、他の変数が使用する :ref:`変数の優先順位 <ansible_variable_precedence>` と同じルールに従います。

変数は、Playbook に設定される場合には、Playbook キーワードと同じ継承ルールに従います。プレイの値を設定すると、タスク、ブロック、またはロールの値をオーバーライドできます。

   - hosts: cloud
     gather_facts: false
     become: yes
     vars:
       ansible_become_user: admin
     tasks:
       - name:This task uses admin as the become user.
         dnf:
           name: some-service
           state: latest
       - block:
           - name:This task uses service-admin as the become user.
             # a task to configure the new service
           - name:This task also uses service-admin as the become user, defined in the block.
             # second task to configure the service
vars:
ansible_become_user: service-admin
       - name:This task (outside of the block) uses admin as the become user again.
         service:
           name: some-service
           state: restarted

変数の範囲: 値が有効な期間
""""""""""""""""""""""""""""""""""""""""""""""

Playbook に設定した変数の値は、その値を定義する Playbook オブジェクト内にのみ存在します。このような「範囲が Playbook オブジェクト」の変数は、他のプレイなど、後続のオブジェクトでは利用できません。

インベントリー、vars プラグイン、:ref:`set_fact<set_fact_module>` や :ref:`include_vars<include_vars_module>` といったモジュールの使用など、ホストやグループに直接関連付けられた変数値は、全プレイで利用できます。また、上記のような「範囲がホスト」の変数は ``hostvars[]`` ディクショナリーで利用できます。

.. _general_precedence_extra_vars:

コマンドラインでの追加変数 (``-e``) の使用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

コマンドラインで追加変数 (``--extra-vars`` または ``-e``) を使用して、他のカテゴリーの全設定をオーバーライドできます。``-e`` で渡される値は、コマンドラインオプションではなく変数で、他で設定した変数をはじめ、設定オプション、コマンドラインオプション、Playbook キーワードをオーバーライドします。たとえば、以下のタスクでは、``carol`` ではなく ``brian`` として接続されます。

   ansible -u carol -e 'ansible_user=brian' -a whoami all

変数名と値は、``--extra-vars`` で指定する必要があります。
