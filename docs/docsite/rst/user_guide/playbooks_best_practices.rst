.. _playbooks_best_practices:

ベストプラクティス
==============

Ansible と Ansible Playbook を最大限に活用するためのヒントをいくつか紹介します。

これらのベストプラクティスを示す Playbook の例は、「`ansible-examples リポジトリー <https://github.com/ansible/ansible-examples>`」を参照してください。 (注記: この例では、最新のリリースではすべての機能を使用しているわけではありませんが、優れたリファレンスになります。

.. contents:: トピック

.. _content_organization:

コンテンツの整理
++++++++++++++++++++++

以下のセクションでは、Playbook コンテンツを整理するさまざまな方法を示します。

ただし、Ansible の使用はお客様のニーズに合わせる必要があるため、ここで紹介しているアプローチを変更し、必要に応じて整理してください。

Playbook コンテンツを整理する重要な方法の 1 つに、Ansible の「ロール」編成機能があります。
これは、Playbook のメインページの一部として文書化されています。 :ref:`playbooks_reuse_roles` で利用可能なロールのドキュメントを読み取って理解してください。

.. _directory_layout:

ディレクトリーのレイアウト
````````````````

ディレクトリーのトップレベルには、以下のようなファイルおよびディレクトリーが含まれます。

    production                # inventory file for production servers
    staging                   # inventory file for staging environment

    group_vars/
       group1.yml             # here we assign variables to particular groups
       group2.yml
    host_vars/
       hostname1.yml          # here we assign variables to particular systems
       hostname2.yml

    library/                  # if any custom modules, put them here (optional)
    module_utils/             # if any custom module_utils to support modules, put them here (optional)
    filter_plugins/           # if any custom filter plugins, put them here (optional)

    site.yml                  # master playbook
    webservers.yml            # playbook for webserver tier
    dbservers.yml             # playbook for dbserver tier

    roles/
        common/               # this hierarchy represents a "role"
            tasks/            #
                main.yml      #  <-- tasks file can include smaller files if warranted
            handlers/         #
                main.yml      #  <-- handlers file
            templates/        #  <-- files for use with the template resource
                ntp.conf.j2   #  <------- templates end in .j2
            files/            #
                bar.txt       #  <-- files for use with the copy resource
                foo.sh        #  <-- script files for use with the script resource
            vars/             #
                main.yml      #  <-- variables associated with this role
            defaults/         #
                main.yml      #  <-- default lower priority variables for this role
            meta/             #
                main.yml      #  <-- role dependencies
            library/          # roles can also include custom modules
            module_utils/     # roles can also include custom module_utils
            lookup_plugins/   # or other types of plugins, like lookup in this case

        webtier/              # same kind of structure as "common" was above, done for the webtier role
        monitoring/           # ""
        fooapp/               # ""

.. 注記:トップレベルの Playbook が多すぎる (たとえば、特定のホットフィックス用に作成した Playbook がある) 場合は、代わりに playbooks/ ディレクトリを使用することが推奨されます。 大きくなるにつれて、この方法が推奨されます。 これを行う場合は、ansible.cfg で roles_path を設定し、ロールの場所を見つけます。

.. _alternative_directory_layout:

代替ディレクトリーレイアウト
````````````````````````````

または、``group_vars``/``host_vars`` を含む各インベントリーファイルを別のディレクトリーに置くこともできます。これは、``group_vars``/``host_vars`` に、さまざまな環境で一般的ではない場合に特に便利です。レイアウトは次のようになります。

    inventories/
       production/
          hosts               # inventory file for production servers
          group_vars/
             group1.yml       # here we assign variables to particular groups
             group2.yml
          host_vars/
             hostname1.yml    # here we assign variables to particular systems
             hostname2.yml

       staging/
          hosts               # inventory file for staging environment
          group_vars/
             group1.yml       # here we assign variables to particular groups
             group2.yml
          host_vars/
             stagehost1.yml   # here we assign variables to particular systems
             stagehost2.yml

    library/
    module_utils/
    filter_plugins/

    site.yml
    webservers.yml
    dbservers.yml

    roles/
        common/
        webtier/
        monitoring/
        fooapp/

このレイアウトにより、大規模な環境でより柔軟になり、異なる環境間でインベントリー変数を完全に分離できます。欠点は、ファイルが多くなるため、メンテナンスが難しくなることです。

.. _use_dynamic_inventory_with_clouds:

クラウドでの動的インベントリーの使用
`````````````````````````````````

クラウドプロバイダーを使用している場合は、静的ファイルでインベントリーを管理しないでください。 「:ref:`intro_dynamic_inventory`」を参照してください。

これは単にクラウドに当てはまるわけではありません。
インフラストラクチャー内のシステムの正規リストを維持している別のシステムがある場合、動的インベントリーの使用は一般的に素晴らしいアイデアです。

.. _staging_vs_prod:

ステージング環境と実稼働環境を区別する方法
``````````````````````````````````````````

静的インベントリーを管理する場合には、さまざまなタイプの環境をどのように区別するかをよく尋ねられます。 次の例は、
これを行うための適切な方法を示しています。 同様のグループ化方法を動的インベントリーに適合させることができます。
たとえば、AWSタグ「environment:production」の適用を検討すると、「ec2_tag_environment_production」という名前のシステムが自動的に検出されます。

ただし、静的なインベントリーの例を見てみましょう。 以下の *実稼働* ファイルには、すべての実稼働ホストのインベントリーが含まれます。

ホスト (ロール) の目的と、地理的またはデータセンターの場所 (該当する場合) に基づいてグループを定義することが推奨されます。

    # file: production

    [atlanta_webservers]
    www-atl-1.example.com
    www-atl-2.example.com

    [boston_webservers]
    www-bos-1.example.com
    www-bos-2.example.com

    [atlanta_dbservers]
    db-atl-1.example.com
    db-atl-2.example.com

    [boston_dbservers]
    db-bos-1.example.com

    # webservers in all geos
    [webservers:children]
    atlanta_webservers
    boston_webservers

    # dbservers in all geos
    [dbservers:children]
    atlanta_dbservers
    boston_dbservers

    # everything in the atlanta geo
    [atlanta:children]
    atlanta_webservers
    atlanta_dbservers

    # everything in the boston geo
    [boston:children]
    boston_webservers
    boston_dbservers
    
.. _groups_and_hosts:

グループ変数およびホスト変数
````````````````````````

本セクションでは、上記の例で説明します。

グループは組織には適していますが、すべてのグループが適しているわけではありません。 変数を割り当てることもできます。 たとえば、atlanta に NTP サーバーがあり、ntp.conf を設定する際にそのサーバーを使用する必要があります。 以下でこれらの設定を行います。

    ---
    # file: group_vars/atlanta
    ntp: ntp-atlanta.example.com
    backup: backup-atlanta.example.com

変数も、地理的情報だけでなく、 Web サーバーには、データベースサーバーにとって意味のない設定があります::

    ---
    # file: group_vars/webservers
    apacheMaxRequestsPerChild: 3000
    apacheMaxClients: 900

デフォルト値または汎用的に true である値がある場合は、それらを group_vars/all というファイルに配置します::

    ---
    # file: group_vars/all
    ntp: ntp-boston.example.com
    backup: backup-boston.example.com

host_vars ファイル内のシステムで特定のハードウェア領域を定義することは可能ですが、以下を実行する必要がない限り回避します::

    ---
    # file: host_vars/db-bos-1.example.com
    foo_agent_port: 86
    bar_agent_port: 99

動的インベントリーソースを使用している場合には、多くの動的グループが自動的に作成されます。 したがって、「class:webserver」のようなタグは、
「group_vars/ec2_tag_class_webserver」ファイルから変数を自動的に読み込みます。

.. _split_by_role:

トップレベルの Playbook をロールごとに分離
`````````````````````````````````````````

site.yml では、インフラストラクチャー全体を定義する Playbook をインポートします。 この例では、
他のいくつかの Playbook をインポートしているだけの非常に短いものになります::

    ---
    # file: site.yml
    - import_playbook: webservers.yml
    - import_playbook: dbservers.yml

webservers.yml (これも最上位にあります) のようなファイルで、webservers グループの構成を、webservers グループによって実行されるロールにマッピングします。

    ---
    # file: webservers.yml
    - hosts: webservers
      roles:
        - common
        - webtier

ここでの考え方は、site.yml を「実行」することでインフラストラクチャー全体を構成することを選択でき、
または webservers.yml を実行することでサブセットを実行することを選択できるというものです。 これは ansible の 「--limit」パラメーターと似ていますが、より明示的なものになります::

   ansible-playbook site.yml --limit webservers
   ansible-playbook webservers.yml

.. _role_organization:

ロールのタスクおよびハンドラーの整理
````````````````````````````````````````

以下は、ロールの仕組みを記述するタスクファイルの例です。 ここで一般的なロールは NTP を設定するだけですが、必要に応じてさらに多くのことができます。

    ---
    # file: roles/common/tasks/main.yml

    - name: be sure ntp is installed
      yum:
        name: ntp
        state: present
      tags: ntp

    - name: be sure ntp is configured
      template:
        src: ntp.conf.j2
        dest: /etc/ntp.conf
      notify:
        - restart ntpd
      tags: ntp

    - name: be sure ntpd is running and enabled
      service:
        name: ntpd
        state: started
        enabled: yes
      tags: ntp

以下はハンドラーファイルの例です。 確認のために、ハンドラーは特定のタスクが変更を報告したときにのみ起動し、
各プレイの終わりに実行されます::

    ---
    # file: roles/common/handlers/main.yml
    - name: restart ntpd
      service:
        name: ntpd
        state: restarted

詳細は、「:ref:`playbooks_reuse_roles`」を参照してください。


.. _organization_examples:

この組織が可能にすること (例)
`````````````````````````````````````````

上記の手順では、基本的な組織構造を共有しています。

このレイアウトが有効なユースケースにはどんなものがありますか。 たくさんあります。 インフラストラクチャー全体を再設定する場合は、次のようにします::

    ansible-playbook -i production site.yml

全面的に NTP を再設定するには、以下を実行します::

    ansible-playbook -i production site.yml --tags ntp

Web サーバーのみを再設定するには、以下を実行します::

    ansible-playbook -i production webservers.yml

ボストンにある Web サーバーの場合::

    ansible-playbook -i production webservers.yml --limit boston

最初の 10 個の場合、および次の 10 個の場合：

    ansible-playbook -i production webservers.yml --limit boston[0:9]
    ansible-playbook -i production webservers.yml --limit boston[10:19]

もちろん、基本的なアドホックなものも可能です::

    ansible boston -i production -m ping
    ansible boston -i production -m command -a '/sbin/reboot'

以下のような便利なコマンドがあります。

    # confirm what task names would be run if I ran this command and said "just ntp tasks"
    ansible-playbook -i production webservers.yml --tags ntp --list-tasks

    # confirm what hostnames might be communicated with if I said "limit to boston"
    ansible-playbook -i production webservers.yml --limit boston --list-hosts

.. _dep_vs_config:

デプロイメントと設定組織
````````````````````````````````````````

上記の設定モデルは、標準的な設定トポロジーです。 マルチ層デプロイメントを実行する場合は、
層を飛び越えてアプリケーションを展開するいくつかの Playbook が追加されます。 この場合の「site.yml」は、
「deploy_exampledotcom.yml」などの Playbook で拡大できますが、一般的な概念は引き続き適用できます。

「Playbook」をスポーツのメタファーとして考えてください。インフラストラクチャーに対して常に 1 セットのプレイを用意する必要はありません。
さまざまなタイミングで、さまざまな目的で使用する状況に応じたプレイを行うことができます。

Ansible を使用すると、同じツールを使用してデプロイと設定を行うことができるため、必要なことはおそらく、グループを再利用し、
OS 設定をアプリのデプロイとは別のプレイブックに保持するだけです。

.. _staging_vs_production:

ステージと実稼働
+++++++++++++++++++++

前述のように、ステージ環境 (またはテスト環境) と実稼働環境を分離した状態にしておくと、ステージ環境と実稼働環境に別のインベントリーファイルを使用することが推奨されます。  このように、-i を使用してターゲットに選択できます。 それらすべてを 1 つのファイルに保存すると、驚く結果になるかもしれません。

実稼働環境で試す前に、ステージング環境でテストすることは強く推奨されます。 環境は同じサイズである必要はなく、
グループ変数を使用してこれらの環境の違いを制御できます。

.. _rolling_update:

ローリングアップデート
+++++++++++++++

「serial」キーワードの理解が必要です。 Web サーバーファームを更新する場合は、
それを使用して、バッチで一度に更新するマシンの数を制御する必要があります。

「:ref:`playbooks_delegation`」を参照してください。

.. _mention_the_state:

状態について常に言及する
++++++++++++++++++++++++

「state」パラメーターは、多くのモジュールに対してオプションです。 「state=present」または「state = absent」のいずれの場合でも、
特に一部のモジュールが追加の状態をサポートしているため、明確にするために常にそのパラメーターを Playbook に残しておくことが最善です。

.. _group_by_roles:

ロール別グループ
++++++++++++++

このヒントで少し繰り返しますが、繰り返す価値があります。システムは複数のグループに置くことができます。 :ref:`intro_inventory` および :ref:`intro_patterns` を参照してください。  *webservers* や *dbservers* などにちなんで名付けられたグループを持つことは、
非常に強力な概念であるため、例では繰り返されています。

これにより、Playbook はロールに基づいてマシンをターゲットに設定でき、
グループ変数システムを使用してロール固有の変数を割り当てることができます。

「:ref:`playbooks_reuse_roles`」を参照してください。

.. _os_variance:

異なるオペレーティングシステムとディストリビューション
++++++++++++++++++++++++++++++++++++++++++

2 つの異なるオペレーティングシステム間で異なるパラメーターを処理する場合、これを処理する優れた方法は、
group_by モジュールを使用することです。

これにより、そのグループがインベントリーファイルに定義されていない場合でも、特定の基準に一致するホストの動的グループが作成されます。

   ---

    - name: talk to all hosts just so we can learn about them
      hosts: all
      tasks:
        - name: Classify hosts depending on their OS distribution
          group_by:
            key: os_{{ ansible_facts['distribution'] }}

    # now just on the CentOS hosts...

    - hosts: os_CentOS
      gather_facts: False
      tasks:
        - # tasks that only happen on CentOS go here

これにより、オペレーティングシステム名に基づいてすべてのシステムが動的グループに入れられます。

グループ固有の設定が必要な場合は、以下を実行することもできます。例::

    ---
    # file: group_vars/all
    asdf: 10

    ---
    # file: group_vars/os_CentOS
    asdf: 42

上記の例では、CentOS マシンは asdf の値「42」を取得しますが、他のマシンは「10」を取得します。
これは、変数を設定するだけでなく、特定のロールを特定のシステムにのみ適用するために使用できます。

または、変数のみが必要な場合は、以下を実行します。

    - hosts: all
      tasks:
        - name:Set OS distribution dependent variables
          include_vars: "os_{{ ansible_facts['distribution'] }}.yml"
        - debug:
            var: asdf

これにより、OS 名に基づいて変数がプルされます。

.. _ship_modules_with_playbooks:

Playbook での Ansible モジュールのバンドル
+++++++++++++++++++++++++++++++++++++++

Playbook に YAML ファイルとの関連で :file:`./library` ディレクトリーがある場合は、このディレクトリーを使用して Ansible モジュールを追加できます。
ansible モジュールパスには自動的に表示されます。 これは、Playbook と併用するモジュールを維持するのに適した方法です。 これは、
このセクションの冒頭のディレクトリー構造の例に示されています。

.. _whitespace:

空白およびコメント
+++++++++++++++++++++++

空白を使用して項目を分割し、コメントを使用することが推奨されます ('#' で始まります)。

.. _name_tasks:

常にタスクに名前を付ける
+++++++++++++++++

特定のタスクの「名前」を省略することも可能ですが、
代わりに何かが行われている理由について説明することが推奨されます。 この名前は、Playbook の実行時に表示されます。

.. _keep_it_simple:

シンプルのままにする
++++++++++++++

何かを簡単にできるときは、簡単にしてください。 Ansible のすべての機能を
同時に使用することはしないでください。 ニーズにあったものを
使用してください。 たとえば、外部インベントリーファイルを使用するとき、``vars``、
``vars_files``、``vars_prompt``、および ``--extra-vars`` 
がすべて必要になることはおそらくないはずです。

何かが複雑に感じられる場合は、おそらく実際に複雑で、単純化する良い機会かもしれません。

.. _version_control:

バージョン制御
+++++++++++++++

バージョン制御を使用します。 Playbook およびインベントリーファイルを git (または別のバージョン管理システム) 
に保存し、
変更を加えたらコミットします。 このようにして、インフラストラクチャーを自動化するルールをいつ、
なぜ変更したかを説明する監査証跡を取得できます。

.. _best_practices_for_variables_and_vaults:

変数および Vault
++++++++++++++++++++++++++++++++++++++++

一般的なメンテナンスには、``grep`` または同様のツールを使用して Ansible 設定で変数を見つけることが一般的です。Vault はこれらの変数を可視化するため、間接的な層で作業するのが最適です。Playbook の実行時に、Ansible は非暗号化ファイルで変数を見つけ、機密性の高い変数はすべて暗号化されたファイルから取得します。

そのためのベストプラクティスは、グループの名前が付けられた ``group_vars/`` サブディレクトリーから始めます。このサブディレクトリー内に、``vars`` と ``vault`` という名前のファイルを作成します。``vars`` ファイルで、機密性の高い変数など、必要な変数をすべて定義します。次に、すべての機密変数を ``vault`` ファイルにコピーし、この変数の前に ``vault_`` を付けます。``vars`` ファイルの変数を調整して、jinja2 構文を使用して一致する ``vault_`` 変数を参照し、``vault`` ファイルがvault で暗号化されていることを確認する必要があります。

このベストプラクティスでは、変数ファイルおよび vault ファイルの量、またはその名前に制限はありません。


.. seealso::

   :ref:`yaml_syntax`
       YAML 構文について
   :ref:`working_with_playbooks`
       基本的な Playbook 機能の確認
   :ref:`all_modules`
       利用可能なモジュールについて
   :ref:`developing_modules`
       独自のモジュールを作成して Ansible を拡張する方法について
   :ref:`intro_patterns`
       ホストの選択方法について
   `GitHub サンプルディレクトリー <https://github.com/ansible/ansible-examples>`_
       Github プロジェクトソースから 完全な Playbook ファイル
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
