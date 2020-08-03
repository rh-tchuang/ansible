.. _playbooks_delegation:

委任、ローリングアップデート、およびローカルアクション
==============================================

.. contents:: トピック

Ansible は、最初からマルチ層デプロイメント用に設計されており、別のホストに代わって実行したり、一部のリモートホストを参照するローカル手順を行ったりする際にも適しています。

これは特に、ロードバランサーまたは監視システムと対話している可能性のある、継続的デプロイメントインフラストラクチャーまたはゼロダウンタイムのローリングアップデートを設定する場合に非常に適しています。

追加機能により、完了する順序を調整し、ローリングアップデート時に一度に処理するマシン数に対してバッチウインドウサイズを割り当てることができます。

本セクションでは、この機能をすべて説明します。 使用中の項目の例は、「`ansible-examples リポジトリー <https://github.com/ansible/ansible-examples/>`_」を参照してください。さまざまなアプリケーションのゼロダウンタイム更新手順の例がいくつかあります。

また、「:ref:`モジュールドキュメント<modules_by_category>`」セクションを参照してください。:ref:`ec2_elb<ec2_elb_module>`、:ref:`nagios<nagios_module>`、:ref:`bigip_pool<bigip_pool_module>`、その他の :ref:`network_modules` などのモジュールは、ここで説明した概念と上手に適合します。

また、「pre_task」と「post_task」の概念は、これらのモジュールを通常呼び出す場所であるため、:ref:`playbooks_reuse_roles` で読み取る必要もあります。

特定のタスク (`include`、`add_host`、`debug` など) は、常にコントローラーで実行されるため、委譲することができないことに注意してください。


.. _rolling_update_batch_size:

ローリングアップデートのバッチサイズ
`````````````````````````

デフォルトでは、Ansible はプレイで参照されるすべてのマシンを並行して管理しようとします。 ローリングアップデートのユースケースでは、``serial`` キーワードを使用して、Ansible が一度に管理するホストの数を定義できます。

    ---
    - name: test play
      hosts: webservers
      serial:2
      gather_facts:False

      tasks:
        - name: task one
          command: hostname
        - name: task two
          command: hostname

上記の例では、「webservers」グループに 4 台のホストがある場合は、
その 2 台でプレイが完了してから、次の 2 つのホストに移動します。


    PLAY [webservers] ****************************************

    TASK [task one] ******************************************
    changed: [web2]
    changed:[web1]

    TASK [task two] ******************************************
    changed: [web1]
    changed:[web2]

    PLAY [webservers] ****************************************

    TASK [task one] ******************************************
    changed: [web3]
    changed:[web4]

    TASK [task two] ******************************************
    changed: [web3]
    changed:[web4]

    PLAY RECAP ***********************************************
    web1      : ok=2    changed=2    unreachable=0    failed=0
    web2      : ok=2    changed=2    unreachable=0    failed=0
    web3      : ok=2    changed=2    unreachable=0    failed=0
    web4      : ok=2    changed=2    unreachable=0    failed=0


``serial`` キーワードはパーセンテージで指定することもできます。
これは、パスごとのホストの数を決定するために、プレイ中のホストの総数に適用されます。

    ---
    - name: test play
      hosts: webservers
      serial:"30%"

ホスト数がパス数に分割されない場合は、最終パスには残りの数が含まれます。

Ansible 2.2 の時点で、バッチサイズは以下のようにリストとして指定できます。

    ---
    - name: test play
      hosts: webservers
      serial:
        - 1
        - 5
        - 10

上記の例では、最初のバッチには単一のホストが含まれ、次のバッチには 5 つのホストが含まれ、
(ホストが残っている場合) 使用可能なすべてのホストが使用されるまで、後続のバッチごとに 10 のホストが含まれます。

複数のバッチサイズをパーセンテージとして一覧表示することもできます。

    ---
    - name: test play
      hosts: webservers
      serial:
        - "10%"
        - "20%"
        - "100%"

値を混在させたり、一致させることもできます。

    ---
    - name: test play
      hosts: webservers
      serial:
        - 1
        - 5
        - "20%"

.. note::
     パーセンテージを小さくしても、各パスのホスト数は常に 1 以上になります。


.. _maximum_failure_percentage:

最大失敗率
``````````````````````````

デフォルトでは、Ansible は、まだ失敗していないバッチにホストがある限り、アクションを継続します。プレイのバッチサイズは、``serial`` パラメーターによって決定します。``serial`` が設定されていない場合、バッチサイズは ``hosts:`` フィールドで指定されたすべてのホストになります。
上記のローリング更新など、状況によっては、
障害の特定のしきい値に達したときに再生を中止することが望ましい場合があります。これを実現するために、
次のようにプレイの最大失敗率を設定できます。

    ---
    - hosts: webservers
      max_fail_percentage:30
      serial:10

上記の例では、グループ内の 10 台のサーバーのうち 3 台以上のサーバーに障害が発生した場合は、残りのプレイは中止されます。

.. note::

     設定されたパーセンテージは、等しくせず、超過させる必要があります。たとえば、シリアルが 4 に設定されていて、2 つのシステムに障害が発生したときにタスクを中止したい場合は、
     割合を 50 ではなく 49 に設定する必要があります。

.. _delegation:

委譲
``````````


これは、実際にはローリングアップデートではありませんが、このような場合に頻繁に発生します。

他のホストを参照するあるホストでタスクを実行する場合は、タスクで「delegate_to」キーワードを使用します。
これは、負荷分散されたプールにノードを配置したり、削除したりするのに適しています。 また、停止時間帯の制御にも非常に役立ちます。
タスク、デバッグ、add_host、インクルードなどをすべて委譲しても意味がないことに注意してください。
「serial」キーワードを使用して、一度に実行するホストの数を制御することが推奨されます。

    ---
    - hosts: webservers
      serial: 5

      tasks:
        - name: take out of load balancer pool
          command: /usr/bin/take_out_of_pool {{ inventory_hostname }}
          delegate_to: 127.0.0.1

        - name: actual steps would go here
          yum:
            name: acme-web-stack
            state: latest

        - name: add back to load balancer pool
          command: /usr/bin/add_back_to_pool {{ inventory_hostname }}
          delegate_to: 127.0.0.1


このコマンドは、Ansible を実行しているマシンである 127.0.0.1 で実行します。また、タスクごとに使用できる簡易構文「local_action」もあります。上記と同じプレイブックがありますが、127.0.0.1 に委譲するための簡略構文を使用しています::

    ---
    # ...

      tasks:
        - name: take out of load balancer pool
          local_action: command /usr/bin/take_out_of_pool {{ inventory_hostname }}

    # ...

        - name: add back to load balancer pool
          local_action: command /usr/bin/add_back_to_pool {{ inventory_hostname }}

一般的なパターンは、ローカルアクションを使用して「rsync」を呼び出し、ファイルを管理対象サーバーに再帰的にコピーすることです。
以下は例になります。

    ---
    # ...

      tasks:
        - name: recursively copy files from management server to target
          local_action: command rsync -a /path/to/files {{ inventory_hostname }}:/path/to/target/

パスフレーズなしの SSH キーまたはこれが機能するように設定された ssh-agent が必要です。
そうでない場合は、rsync がパスフレーズを要求してきます。

引数をさらに指定する必要がある場合は、以下の構文を使用できます。

    ---
    # ...

      tasks:
        - name: Send summary mail
          local_action:
            module: mail
            subject: "Summary Mail"
            to: "{{ mail_recipient }}"
            body: "{{ mail_body }}"
          run_once: True

`ansible_host` 変数 (1.x の `ansible_ssh_host` プラグイン、または ssh/paramiko プラグインに固有) は、タスクが委譲されるホストを反映します。

.. _delegate_facts:

委譲されたファクト
```````````````

デフォルトでは、委譲タスクによって収集されるファクトは、ファクト (ホストへの委譲) を実際に生成したホストではなく、`inventory_hostname` (現在のホスト) に割り当てられます。
ディレクティブ `delegate_facts` は `True` に設定して、タスクの収集ファクトを、現在のホストではなく委譲されたホストに割り当てることができます。

    ---
    - hosts: app_servers

      tasks:
        - name: gather facts from db servers
          setup:
          delegate_to: "{{item}}"
          delegate_facts:True
          loop: "{{groups['dbservers']}}"

上記は、dbservers グループのマシンのファクトを収集し、ファクトを app_servers ではなく、それらのマシンに割り当てます。
これにより、dbservers がプレイに含まれていなくても、または `--limit` を使用して除外されていても、`hostvars['dbhost1']['ansible_default_ipv4']['address']` をルックアップできます。


.. _run_once:

1 度実行
````````

ホストのバッチに対してタスクを一度だけ実行しないといけない場合があります。
そのためには、タスクに「run_once」を設定します::

    ---
    # ...

      tasks:

        # ...

        - command: /opt/application/upgrade_db.py
          run_once: true

        # ...

このディレクティブは、現在のバッチの最初のホストで実行を強制的に試行し、すべての結果とファクトを同じバッチのすべてのホストに適用します。

このアプローチは、以下のようなタスクに条件を適用するのと同じです。

        - command: /opt/application/upgrade_db.py
          when: inventory_hostname == webservers[0]

ただし、結果はすべてのホストに適用されます。

多くのタスクと同様、任意で「delegate_to」とペアにして、以下を実行する個々のホストを指定できます。

        - command: /opt/application/upgrade_db.py
          run_once: true
          delegate_to: web01.example.org

委譲の場合と同様に、アクションは委譲されたホストで実行されますが、情報はタスクの元のホストの情報になります。

.. note::
     「serial」と併用すると、「run_once」のマークが付けられたタスクが *各* シリアルバッチの 1 つホストで実行されます。
     タスクが「serial」モードに関係なく 1 回だけ実行されることが重要である場合は、
     :code:`when: inventory_hostname == ansible_play_hosts_all[0]` コンストラクトを使用します。

.. note::
    条件 (つまり `when:`) は、「first host」の変数を使用して、タスクが実行されるかどうかを判断し、他のホストはテストされません。

.. note::
    すべてのホストにファクトを設定するデフォルトの動作を回避するとき、特定のタスクまたはブロックの場合は、`delegate_facts: True` を設定します。

.. _local_playbooks:

ローカルの Playbook
```````````````

SSH 経由で接続するのではなく、Playbook をローカルで使用すると便利です。 これは、Playbook を crontab に配置することにより、システムの構成を保証するのに役立ちます。
crontab に Playbook を配置することで、システムの設定を保証します。 これは、
Anaconda キックスタートなどの OS インストーラー内で Playbook を実行するのにも使用できます。

Playbook 全体をローカルで実行するには、「hosts:」行を「hosts: 127.0.0.1」 として、以下のように Playbook を実行します。

    ansible-playbook playbook.yml --connection=local

または、Playbook 内の他のプレイでデフォルトのリモート接続タイプが使用されている場合でも、
1 つのプレイブックプレイでローカル接続を使用できます。

    ---
    - hosts:127.0.0.1
      connection: local

.. note::
    接続をローカルに設定し、ansible_python_interpreter が設定されていないと、たとえば、モジュールは /usr/bin/python で実行され、{{ ansible_playbook_python }} では実行されません。
    たとえば、host_vars/localhost.yml の "{{ ansible_playbook_python }}" に、
    ansible_python_interpreter: を設定します。この問題は、代わりに ``local_action`` または ``delegate_to: localhost`` を使用して回避できます。



.. _interrupt_execution_on_any_error:

エラーで実行の中断
````````````````````````````````

「any_errors_fatal」オプションを使用すると、マルチホストプレイのすべてのホストの障害は致命的として扱われ、現在のバッチのすべてのホストが致命的なタスクを終了するとすぐに Ansible は終了します。後続のタスクおよびプレイは実行されません。ブロックにレスキューセクションを追加して、致命的なエラーから復旧できます。

場合によっては「serial」の実行は適していません。(動的インベントリーが原因で) ホストの数は予測不可能であり、速度は極めて重要ですが (同時実行が必要)、Playbook の実行を続行するにはすべてのタスクが 100% 成功する必要があります。

たとえば、ユーザーからサービスにトラフィックを渡すために、一部のロードバランサーを持つ多くのデータセンターにあるサービスを検討します。サービスの deb-packages をアップグレードするデプロイ Playbook があります。Playbook には以下のような段階があります。

- ロードバランサーのトラフィックを無効にする (同時にオフにする必要があります)
- サービスを正常に停止する
- ソフトウェアをアップグレードする (この手順には、テストとサービスの起動が含まれます)
- ロードバランサーでトラフィックを有効にする (同時に有効にする必要があります)

サービスは「alive」ロードバランサーで停止することはできません。最初に無効にする必要があります。そのため、いずれかのサーバーが最初の段階で失敗した場合は、次のステージを非表示にすることはできません。

データセンター「A」の場合、Playbook は以下の方法で記述できます。

    ---
    - hosts: load_balancers_dc_a
      any_errors_fatal: True

      tasks:
        - name: 'shutting down datacenter [ A ]'
          command: /usr/bin/disable-dc

    - hosts: frontends_dc_a

      tasks:
        - name: 'stopping service'
          command: /usr/bin/stop-software
        - name: 'updating software'
          command: /usr/bin/upgrade-software

    - hosts: load_balancers_dc_a

      tasks:
        - name: 'Starting datacenter [ A ]'
          command: /usr/bin/enable-dc


この例では、すべてのロードバランサーが正常に無効になっている場合にのみ、Ansible は、フロントエンドでソフトウェアのアップグレードを開始します。

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   `GitHub にある Ansible の例 <https://github.com/ansible/ansible-examples>`_
       フルスタックデプロイメントの例が多数あります。
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
