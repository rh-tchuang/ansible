Playbook の概要
==================

.. contents::
   :local:

.. _about_playbooks:
.. _playbooks_intro:

Playbook について
```````````````

Playbook とは、アドホックタスク実行モードとは完全に異なる方法で Ansible を使用する方法で、
非常に強力です。

簡単に言えば、Playbook は、既存のものとは異なり、非常にシンプルな構成管理とマルチマシンデプロイメントシステムの基礎となりますが、
複雑なアプリケーションのデプロイメントに非常に適しています。

Playbook は構成を宣言できますが、
特定の順序でマシンセット間でさまざまなステップを往復する必要がある場合でも、
手動で指定したプロセスのステップを調整することもできます。 同期または非同期で、
タスクを起動できます。

アドホックタスク用にメインの ``/usr/bin/ansible`` プログラムを実行する場合がありますが、
Playbook はソース管理に保持され、
構成をプッシュしたり、
リモートシステムの構成が仕様どおりであることを確認したりするために使用される可能性が高くなります。

`ansible-examples repository <https://github.com/ansible/ansible-examples>`_ で、
これらの手法を多数説明している Playbook の全セットもあります。 先に進む場合は、
これらを別のタブで確認することが推奨されます。

ドキュメントの目次からは、いろいろなページに飛べるため、
このセクションが終了したら、ドキュメントのインデックスに戻ってください。

.. _playbook_language_example:

Playbook 言語の例
`````````````````````````

Playbook は YAML 形式 (:ref:`yaml_syntax` を参照) で表現され、最小限の構文を持っています。
これは、プログラミング言語やスクリプトではなく、構成またはプロセスのモデルを意図しています。

.. note::
   一部のエディターには、Playbook でクリーンな YAML 構文の作成に役立つアドオンがあります。詳細は「:ref:`other_tools_and_programs`」を参照してください。


各 Playbook は、リストにある 1 つ以上の「Plays」から構成されます。

Play の目的は、ホストのグループを、Ansible ではタスクと呼ばれるものに代表される、
明確に定義されたロールにマッピングすることです。 基本的なレベルでは、
タスクは ansible モジュールを呼び出します。

複数の「プレイ」の Playbook を作成することにより、
マルチマシンデプロイメントを調整して、webservers グループのすべてのマシンで特定のステップを実行し、
次に database サーバーグループで特定のステップを実行し、
さらに webservers グループでさらに多くのコマンドを実行できる、というようになります。

「プレイ」は多かれ少なかれスポーツと似ています。 さまざまなことを行うために、
システムに影響を与える多くのプレイを持つことができます。 特定の状態またはモデルを定義するだけではなく、
さまざまなプレイを同時に実行することができます。

.. _apache-playbook:

まず、ここに、プレイが 1 つだけ含まれてる ``verify-apache.yml`` という名前の Playbook があります。

    ---
    - hosts: webservers
      vars:
        http_port: 80
        max_clients: 200
      remote_user: root
      tasks:
      - name: ensure apache is at the latest version
        yum:
          name: httpd
          state: latest
      - name: write the apache config file
        template:
          src: /srv/httpd.j2
          dest: /etc/httpd.conf
        notify:
        - restart apache
      - name: ensure apache is running
        service:
          name: httpd
          state: started
      handlers:
        - name: restart apache
          service:
            name: httpd
            state: restarted

Playbook には複数のプレイを含めることができます。最初に Web サーバーを対象とし、
次にデータベースサーバーを対象とする Playbook があるとします。例::

    ---
    - hosts: webservers
      remote_user: root

      tasks:
      - name: ensure apache is at the latest version
        yum:
          name: httpd
          state: latest
      - name: write the apache config file
        template:
          src: /srv/httpd.j2
          dest: /etc/httpd.conf

    - hosts: databases
      remote_user: root

      tasks:
      - name: ensure postgresql is at the latest version
        yum:
          name: postgresql
          state: latest
      - name: ensure that postgresql is started
        service:
          name: postgresql
          state: started

この方法を使用して、対象とするホストグループ、
リモートサーバーにログインするユーザー名、
sudoを使用するかどうかなどを切り替えることができます。プレイは、タスクと同様に、
Playbook で指定された順序で上から下に実行されます。

以下では、Playbook 言語のさまざまな機能を説明します。

.. _playbook_basics:

基本
``````

.. _playbook_hosts_and_users:

ホストおよびユーザー
+++++++++++++++

Playbook の各プレイについて、インフラストラクチャー内のどのマシンを対象にするか、
どのリモートユーザーがステップ (タスクと呼ばれる) を完了するかを選択できます。

``hosts`` 行は、
:ref:`intro_patterns` のドキュメントで説明されているように、
コロンで区切られた 1 つ以上のグループまたはホストパターンのリストです。 ``remote_user`` は、ユーザーアカウントの名前です。

    ---
    - hosts: webservers
      remote_user: root

.. note::

    ``remote_user`` パラメーターは、以前は ``user`` と呼ばれていました。Ansible 1.4 で名前が変更され、**user** モジュール (リモートシステムでユーザーを作成するために使用) との区別がより明確になりました。

リモートユーザーは、タスクごとに定義することもできます::

    ---
    - hosts: webservers
      remote_user: root
      tasks:
        - name: test connection
          ping:
          remote_user: yourname

別のユーザーとしての実行に関するサポートも利用可能です (:ref:`become` を参照)。

    ---
    - hosts: webservers
      remote_user: yourname
      become: yes

``become`` キーワードを、プレイ全体ではなく特定のタスクで使用することもできます。

    ---
    - hosts: webservers
      remote_user: yourname
      tasks:
        - service:
            name: nginx
            state: started
          become: yes
          become_method: sudo


また、自身のユーザーとしてログインしてから、root とは別のユーザーになることもできます::

    ---
    - hosts: webservers
      remote_user: yourname
      become: yes
      become_user: postgres

su などの他の権限昇格メソッドを使用することもできます。

    ---
    - hosts: webservers
      remote_user: yourname
      become: yes
      become_method: su

sudo のパスワードを指定する必要がある場合は、``ansible-playbook`` に ``--ask-become-pass`` または ``-K`` を付けて実行します。
``become`` を使用して Playbook を実行し、Playbook がハングしているように見える場合は、
おそらく権限昇格のプロンプトでスタックしており、`Control-C` を使用して停止できます。
これにより、適切なパスワードを追加して Playbook を再実行できます。

.. important::

   root 以外のユーザーに対して ``become_user`` を使用すると、
   モジュールの引数が、``/tmp`` のランダムな一時ファイルに簡単に記述されます。
   これらは、コマンドの実行直後に削除されます。 これにより、
   たとえば「bob」ユーザーから「timmy」ユーザーに特権を変更した場合に限り発生させ、
   「bob」から「root」に変更した場合、
   または「bob」または「root」として直接ログインした場合には発生させません。 このデータが、
   一時的に読み取り可能 (書き込み不可) であることが懸念される場合は、
   `become_user` を設定して暗号化されていないパスワードを転送しないでください。 その他の場合は、``/tmp`` が使用されず、
   これは機能しません。Ansible は、
   password パラメーターをログに記録しないようにします。


.. _order:

.. versionadded:: 2.4

また、ホストの実行順序を制御することもできます。デフォルトは、インベントリーで指定されている順序に従います。

    - hosts: all
      order: sorted
      gather_facts:False
      tasks:
        - debug:
            var: inventory_hostname

順序に使用できる値は以下の通りです。

inventory:
    デフォルトです。インベントリーで「提供されたとおり」の順序になります。
reverse_inventory:
    名前が示すように、インベントリーで「提供されたとおり」のものと逆の順序になります。
sorted:
    ホストの名前をアルファベット順で並べます。
reverse_sorted:
    ホストの名前を
逆アルファベット順で並べます。
    ホストは実行ごとにランダムに並べられます


.. _tasks_list:

タスクリスト
++++++++++

各プレイにはタスクリストが含まれます。 タスクは、
次のタスクに進む前に、ホストパターンに一致するすべてのマシンに対して、
一度に 1 つずつ順番に実行されます。 プレイ内では、
すべてのホストが同じタスクディレクティブを取得することを理解することが重要です。 プレイの目的は、
選択したホストをタスクにマップすることです。

上から下に実行される Playbook を実行すると、タスクが失敗したホストは、
Playbook 全体のローテーションから除外されます。 問題が発生した場合は、Playbook ファイルを修正し、再実行します。

各タスクの目的は、非常に具体的な引数を使用してモジュールを実行することです。
変数はモジュールの引数で使用できます。

モジュールは冪等である必要があります。
つまり、モジュールをシーケンスで複数回実行すると、1 回だけ実行した場合と同じ結果になります。冪等性を達成する 1 つの方法は、
モジュールに、目的の最終状態がすでに実現しているかどうかを確認し、
その状態が実現している場合は、
アクションを実行せずに終了することです。Playbook が使用するすべてのモジュールが冪等である場合は、
Playbook 自体が冪等である可能性が高いため、
Playbook を再実行しても安全です。

**command** モジュールと **shell** モジュールは、通常、同じコマンドを再実行します。
これは、
``chmod`` または ``setsebool`` などのコマンドの場合は、まったく問題ありません。 これらのモジュールを冪等にするために使用できる ``creates`` 
フラグが利用できます。

すべてのタスクには ``name`` が必要です。
これは、Playbook の実行からの出力に含まれます。  これは人間が読める形式の出力であるため、
各タスクステップの適切な説明を提供すると便利です。 ただし、
名前が指定されていない場合は、
「action」に渡される文字列が出力に使用されます。

タスクは、レガシーの ``action: module options`` 形式を使用して宣言できますが、
より一般的な ``module: options`` 形式を使用することが推奨されます。
この推奨される形式はドキュメント全体で使用されていますが、
一部の Playbook では古い形式を使用している場合があります。

以下は基本的なタスクです。ほとんどのモジュールの場合と同様、
サービスモジュールは ``key=value`` 引数を取ります::

   tasks:
     - name: make sure apache is running
       service:
         name: httpd
         state: started

**command** モジュールおよび **shell** モジュールは、引数のリストを取り、
``key=value`` 形式を使用しない唯一のモジュールです。 これにより、
それらは予想どおりに機能します。

   tasks:
     - name: enable selinux
       command: /sbin/setenforce 1

**command** モジュールと **shell** モジュールは戻りコードを処理するため、コマンドがあり、
その正常な終了コードがゼロでない場合は、以下を行うことができます。

   tasks:
     - name: run this command and ignore the result
       shell: /usr/bin/somecommand || /bin/true

または、以下のようになります。

   tasks:
     - name: run this command and ignore the result
       shell: /usr/bin/somecommand
       ignore_errors:True


アクション行が長すぎて快適ではなくなった場合は、スペースで改行し、
継続している行にインデントを追加できます。

    tasks:
      - name:Copy ansible inventory file to client
        copy: src=/etc/ansible/hosts dest=/etc/ansible/hosts
                owner=root group=root mode=0644

変数はアクション行で使用できます。  たとえば、
``vars`` セクションで ``vhost`` という名前の変数を定義したとすると、次のようになります。

   tasks:
     - name: create a virtual host file for {{ vhost }}
template:
src: somefile.j2
dest: /etc/httpd/conf.d/{{ vhost }}

同じような変数は、後で使用するテンプレートで使用できます。

非常に基本的な Playbook では、すべてのタスクがそのプレイに直接リストされますが、
通常は、:ref:`playbooks_reuse` の説明に従って、タスクを破損させる方が分かりやすくなります。

.. _action_shorthand:

アクション (短縮形表記)
````````````````

.. versionadded:: 0.8

Ansible では、以下のようなモジュールリストが推奨されます。

    template:
        src: templates/foo.j2
        dest: /etc/foo.conf

Ansible の初期バージョンでは以下の形式が使用されていましたが、これは引き続き動作します。

    action: template src=templates/foo.j2 dest=/etc/foo.conf


.. _handlers:

ハンドラー: 変更時の操作の実行
``````````````````````````````````````

前述したように、モジュールは冪等である必要があり、
リモートシステムに変更を加えたときにリレーできます。  Playbook はこれを認識し、
変化に対応するために使用できる基本的なイベントシステムを備えています。

これらの「通知」アクションは、プレイのタスクの各ブロックの最後にトリガーされ、
複数の異なるタスクから通知された場合でも 1 回だけトリガーされます。

たとえば、複数のリソースが設定ファイルを変更したために Apache を再起動する必要があることを示している場合がありますが、
不必要な再起動を回避するために、
Apache は 1 回だけバウンスされます。

次に、ファイルの内容が変更されたときに 2 つのサービスを再起動する例を示します。
ただし、ファイルが変更された場合のみです。

   - name: template configuration file
     template:
       src: template.j2
       dest: /etc/foo.conf
     notify:
        - restart memcached
        - restart apache

タスクの ``notify`` セクションに挙げられているものは、
ハンドラーと呼ばれています。

ハンドラーはタスクのリストであり、通常のタスクと違いはなく、
グローバルに一意の名前で参照され、
通知機能によって通知されます。 ハンドラーに何も通知しないと、
実行されません。 ハンドラーに通知するタスクの数に関係なく、
特定のプレイでタスクがすべて完了すると、ハンドラーは 1 回だけ実行されます。

以下は、ハンドラーセクションの例です::

    handlers:
        - name: restart memcached
          service:
            name: memcached
            state: restarted
        - name: restart apache
          service:
            name: apache
            state: restarted

Ansible ハンドラーが変数を使用することが望ましい場合があります。たとえば、サービスの名前がディストリビューションによって若干異なる場合は、出力で各ターゲットマシンについて再起動したサービスの正確な名前を表示させる必要があります。ハンドラーの名前に変数を配置しないようにします。ハンドラー名は早期にテンプレート化されるため、Ansible には、以下のように、ハンドラー名に使用できる値がない場合があります。

    handlers:
    # this handler name may cause your play to fail!
    - name: restart "{{ web_service_name }}"

ハンドラー名で使用される変数が利用できない場合は、プレイ全体が失敗します。この変数を中間のプレイに変更すると、ハンドラーは新たに **作成されません**。

代わりに、変数をハンドラーの task パラメーターに設定します。以下のような ``include_vars`` を使用して値を読み込むことができます。

  .. code-block:: yaml+jinja

    tasks:
      - name:Set host variables based on distribution
        include_vars: "{{ ansible_facts.distribution }}.yml"

handlers:
  - name: restart web service
    service:
      name: "{{ web_service_name | default('httpd') }}"
      state: restarted
    

Ansible 2.2 以降、ハンドラーは一般的なトピックを「リッスン」することもでき、タスクは次のようにそれらのトピックに通知できます。

    handlers:
        - name: restart memcached
          service:
            name: memcached
            state: restarted
          listen: "restart web services"
        - name: restart apache
          service:
            name: apache
            state: restarted
          listen: "restart web services"

    tasks:
        - name: restart everything
          command: echo "this task will restart the web services"
          notify: "restart web services"

この使用により、複数のハンドラーをトリガーすることがはるかに簡単になります。また、
ハンドラーを名前から切り離し、
Playbook とロールの間でハンドラーを共有しやすくします (特に Galaxy などの共有ソースからサードパーティーのロールを使用する場合)。

.. note::
   * 通知ハンドラーは常に、notify-statement に記載される `順番ではなく`、定義される順序で実行されます。これは、`listen` を使用するハンドラーの場合でも当てはまります。
   *ハンドラー名と `listen` トピックは、グローバルな名前空間にあります。
   * ハンドラー名は一時的なものですが、`listen` トピックは一時的ではありません。
   * 固有のハンドラー名を使用します。同じ名前のハンドラーを複数トリガーすると、最初のハンドラーが上書きされます。定義された最後のもののみが実行されます。
   * インクルード内で定義されたハンドラーに通知することはできません。Ansible 2.1 の時点では、これは機能しますが、包含は `静的` である必要があります。

ロールについては後で説明しますが、次の点に注意してください。

* ``pre_tasks`` セクション、``tasks`` セクション、および ``post_tasks`` セクション内で通知されるハンドラーは、通知されたセクションの最後に自動的にフラッシュされます。
* ``roles`` セクション内で通知されるハンドラーは、``tasks`` セクションの最後ではなく、``tasks`` ハンドラーの前に自動的にフラッシュされます。
* ハンドラーはスコープのあるプレイであるため、ハンドラーは定義されているロールの外で使用できます。

すべてのハンドラーコマンドをすぐにフラッシュする必要がある場合は、以下を実行できます。

    tasks:
       - shell: some tasks go here
       - meta: flush_handlers
       - shell: some other tasks

上記の例では、``meta`` ステートメントに到達したときに、
キューに入れられたハンドラーが処理されます。 これは少しニッチなケースですが、
時々役に立ちます。

.. _executing_a_playbook:

Playbook の実行
````````````````````

これで、Playbook の構文の説明は終わります。では、Playbook はどのように実行するのでしょう。 これは簡単です。
並列処理レベル 10 を使用して Playbook を実行してみましょう。

    ansible-playbook playbook.yml -f 10

.. _playbook_ansible-pull:

Ansible-Pull
````````````

Ansible のアーキテクチャーを反転させて、ノードが設定をプッシュするのではなく、
中央の場所にチェックインするようにしたい場合は、そうすることができます。

``ansible-pull`` は、git から設定手順のリポジトリーをチェックアウトし、
そのコンテンツに対して ``ansible-playbook`` を実行する小さなスクリプトです。

チェックアウトの場所を負荷分散する場合、``ansible-pull`` は基本的に無限にスケーリングを行います。

詳細は、``ansible-pull --help`` を実行してください。

また、プッシュモードからの crontab で ``ansible-pull`` を設定する際に利用可能な `clever playbook <https://github.com/ansible/ansible-examples/blob/master/language_features/ansible_pull.yml>`_ もあります。

.. _linting_playbooks:

Playbook の文法チェック
`````````````````

`ansible-lint <https://docs.ansible.com/ansible-lint/index.html>`_ を使用して Playbook の詳細チェックを実行する前に Playbook を実行できます。

たとえば、このセクションですでに説明した :ref:`verify-apache.yml playbook <apache-playbook>` で ``ansible-lint`` を実行すると、以下のような結果が得られます。

.. code-block:: bash

    $ ansible-lint verify-apache.yml
    [403] Package installs should not use latest
    verify-apache.yml:8
    Task/Handler: ensure apache is at the latest version
    
`ansible-lint のデフォルトルール <https://docs.ansible.com/ansible-lint/rules/default_rules.html>`_ ページでは、各エラーが説明されています。``[403]`` の場合に推奨される修正は、Playbook の ``state: latest`` を ``state: present`` に変更することです。


その他の Playbook 検証オプション
```````````````````````````````````
Playbook の検証に使用できるツールの詳細なリストは、:ref:`validate-playbook-tools` を参照してください。その他の考慮すべき事項を以下に示します。

* Playbook の構文を確認するには、``--syntax-check`` フラグを指定して ``ansible-playbook`` を使用します。これにより、
  パーサーを介して Playbook ファイルが実行され、インクルードファイルやロールなどに構文上の問題がないことが確認されます。

* Playbook の実行の下部を見て、
  対象となったノードの概要とその実行方法を確認します。一般的な障害と、致命的な「到達不能」な通信の試行は、個別にカウントされます。

* 成功したモジュールだけでなく、失敗したモジュールからの詳細な出力を表示する場合は、
  ``--verbose`` フラグを使用します。 これは、Ansible 0.5 以降で利用できます。

* 実行する前に Playbook の影響を受けるホストを確認するには、
  次のようにします::

      ansible-playbook playbook.yml --step

.. seealso::

   `ansible- <https://docs.ansible.com/ansible-lint/index.html>lint`
       Ansible Playbook 構文のテスト方法について
   :ref:`yaml_syntax`
       YAML 構文について
   :ref:`playbooks_best_practices`
       実際の Playbook の管理に関するさまざまなヒント
   :ref:`all_modules`
       利用可能なモジュールについて
   :ref:`developing_modules`
       独自のモジュールを作成して Ansible を拡張する方法について
   :ref:`intro_patterns`
       ホストの選択方法について
   `GitHub サンプルディレクトリー <https://github.com/ansible/ansible-examples>`_
       完全なエンドツーエンド Playbook の例
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
