**********************************************************
Playbook の例: 継続的デリバリーおよびローリングアップグレード
**********************************************************

.. contents::
   :local:

.. _lamp_introduction:

継続的デリバリーとは
============================

継続的デリバリー (CD) は、ソフトウェアアプリケーションに更新を頻繁に配信することを意味します。

その概念は、より頻繁に更新することにより、特定の期間を待つ必要がなく、
組織が変化に対応するプロセスを改善できるということです。

1 時間ごと、またはより頻繁に更新をエンドユーザーにデプロイしている Ansible ユーザーもいます。
承認されたコード変更があるたびに更新する場合もあります。 そのためには、この更新をゼロダウンタイムで迅速に適用できるツールが必要です。

このドキュメントでは、Ansible の最も完全な Playbook サンプルの 1 つである lamp_haproxy をテンプレートとして使用して、
この目標を達成する方法を詳しく説明します。この例では、ロール、テンプレート、グループ変数などの多くの Ansible 機能を使用します。
また、
Web アプリケーションスタックのゼロダウンタイムローリングアップグレードを実行できるオーケストレーション Playbook も含まれています。

.. note::

   この例における最新の Playbook は、「`こちら
   <https://github.com/ansible/ansible-examples/tree/master/lamp_haproxy>`_」を参照してください。

Playbook は Apache、PHP、MySQL、Nagios、および HAProxy を CentOS ベースのサーバーセットにデプロイします。

ここでは、この Playbook の実行については説明しません。github プロジェクトに含まれている README と、
その例を参照してください。代わりに、Playbook の各部分を確認し、その動作を記述します。

.. _lamp_deployment:

サイトのデプロイメント
===============

まず、``site.yml`` から始めましょう。これは、サイト全体のデプロイメントの Playbook です。最初にサイトをデプロイし、
すべてのサーバーに更新をプッシュするのに使用できます。

.. code-block:: yaml

    ---
    # This playbook deploys the whole application stack in this site.

    # Apply common configuration to all hosts
    - hosts: all

      roles:
      - common

    # Configure and deploy database servers.
    - hosts: dbservers

      roles:
      - db

    # Configure and deploy the web servers. Note that we include two roles
    # here, the 'base-apache' role which simply sets up Apache, and 'web'
    # which includes our example web application.

    - hosts: webservers

      roles:
      - base-apache
      - web

    # Configure and deploy the load balancer(s).
    - hosts: lbservers

      roles:
      - haproxy

    # Configure and deploy the Nagios monitoring node(s).
    - hosts: monitoring

      roles:
      - base-apache
      - nagios

.. note::

   Playbook やプレイなどの用語に慣れていない場合は、:ref:`working_with_playbooks` を確認してください。

この Playbook では、5 つの Playbook があります。最初のホストは ``すべて`` のホストを対象にし、``共通`` のロールをすべてのホストに適用します。
これは、yum リポジトリー設定、ファイアウォール設定などのサイト全体で、すべてのサーバーに適用する必要がある設定です。

次の 4 つのプレイは、特定のホストグループに対して実行され、そのサーバーに特定のロールを適用します。
Nagios 監視、データベース、および Web アプリケーションのロールに加えて、
基本的な Apache セットアップをインストールおよび構成する ``base-apache`` ロールを実装しました。これは、
サンプル Web アプリケーションと Nagios ホストの両方で使用されます。

.. _lamp_roles:

再利用可能なコンテンツ: ロール
=======================

現時点では、ロールおよび Ansible の仕組みについて理解しておく必要があります。ロールは、
タスク、ハンドラー、テンプレート、ファイルなどのコンテンツを再利用可能なコンポーネントに整理する方法です。

この例には、``common``、``base-apache``、``db``、``haproxy``、``nagios``、および ``web`` の 6 つのロールがあります。ロールをどのように整理するかはユーザーとアプリケーション次第ですが、
ほとんどのサイトには、すべてのシステムに適用される 1 つ以上の共通のロールと、
サイトの特定部分をインストールおよび構成する一連のアプリケーション固有のロールがあります。

ロールは変数と依存関係を持つことができ、パラメーターをロールに渡すことでその動作を変更できます。
ロールの詳細は、:ref:`playbooks_reuse_roles` セクションをご覧ください。

.. _lamp_group_variables:

設定: グループ変数
==============================

グループ変数は、サーバーのグループに適用される変数です。テンプレートおよび Playbook で使用して動作をカスタマイズし、
簡単に変更できる設定とパラメーターを提供できます。この変数は、
インベントリーと同じ場所にある ``group_vars`` ディレクトリーに保存されます。
以下は、lamp_haproxy の ``group_vars/all`` ファイルです。予想どおりに、この変数はインベントリーのすべてのマシンに適用されます。

.. code-block:: yaml

   ---
   httpd_port:80
   ntpserver:192.0.2.23

これは YAML ファイルであり、より複雑な変数構造のリストおよびディクショナリーを作成できます。
この場合は、2 つの変数を設定しています。1 つは Web サーバーのポート用で、
もう 1 つはマシンが時刻同期に使用する NTP サーバー用です。

別のグループ変数ファイルです。これは、``dbservers`` グループのホストに適用される ``group_vars/dbservers`` です。

.. code-block:: yaml

   ---
   mysqlservice: mysqld
   mysql_port:3306
   dbuser: root
   dbname: foodb
   upassword: usersecret

上記の例を参照すると、同様に ``webservers`` グループと ``lbservers`` グループのグループ変数も存在します。

これらの変数はさまざまな場所で使用されます。これらは、``roles/db/tasks/main.yml`` のように Playbook で使用できます。

.. code-block:: yaml

   - name: Create Application Database
     mysql_db:
       name: "{{ dbname }}"
       state: present

   - name: Create Application DB User
     mysql_user:
       name: "{{ dbuser }}"
       password: "{{ upassword }}"
       priv: "*.*:ALL"
       host: '%'
       state: present

これらの変数は、``roles/common/templates/ntp.conf.j2`` で、テンプレートで使用することもできます。

.. code-block:: text

   driftfile /var/lib/ntp/drift

   restrict 127.0.0.1
   restrict -6 ::1

   server {{ ntpserver }}

   includefile /etc/ntp/crypto/pw

   keys /etc/ntp/keys

{{ and }} の変数置換構文が、テンプレートと変数の両方で同じであることを確認できます。中括弧内の構文は Jinja2 であり、
あらゆる種類の操作を実行して、
内部のデータにさまざまなフィルターを適用できます。テンプレートでは、for ループと if ステートメントを使用して、
``roles/common/templates/iptables.j2`` で次のようなより複雑な状況を処理することもできます。

.. code-block:: jinja

   {% if inventory_hostname in groups['dbservers'] %}
   -A INPUT -p tcp  --dport 3306 -j  ACCEPT
   {% endif %}

これは、現在操作しているマシンのインベントリー名 (``inventory_hostname``) が、
インベントリーグループ ``dbservers`` に存在するかどうかを確認するためのテストです。その場合、そのマシンはポート 3306 の iptables ACCEPT 行を取得します。

以下は、同じテンプレートの別の例です。

.. code-block:: jinja

   {% for host in groups['monitoring'] %}
   -A INPUT -p tcp -s {{ hostvars[host].ansible_default_ipv4.address }} --dport 5666 -j ACCEPT
   {% endfor %}

これは、``monitoring`` というグループのすべてのホストをループし、
Nagios がそのホストを監視できるように、各監視ホストのデフォルト IPv4 アドレスの ACCEPT 行を現在のマシンの iptables 構成に追加します。

Jinja2 およびその機能は、「`こちら <http://jinja.pocoo.org/docs/>`_」で詳しく学ぶことができます。
また、Ansible 変数全般は、「:ref:`playbooks_variables`」セクションを参照してください。

.. _lamp_rolling_upgrade:

ローリングアップグレード
===================

これで、Web サーバー、ロードバランサー、および監視を備え、完全にデプロイされたサイトができました。これは、どのように更新していきますか。これは、
Ansible のオーケストレーション機能が作用する場所です。一部のアプリケーションでは、「オーケストレーション」という用語を使用して基本的な順序付けまたはコマンドブラストを意味しますが、
Ansible は、オーケストレーションを「オーケストラのようにマシンを指揮すること」として扱い、かなり洗練されたエンジンを備えています。

Ansible には、多層アプリケーションで連携して操作を実行する機能があります。そのため、Web アプリケーションの高度なゼロダウンタイムローリングアップグレードを簡単に調整 (オーケストレーション) できます。これは、``rolling_update.yml`` と呼ばれる別の Playbook に実装されます。

Playbook を確認すると、Playbook が 2 つのプレイで構成されていることを確認できます。最初のプレイは非常にシンプルで、以下のようになります。

.. code-block:: yaml

   - hosts: monitoring
     tasks: []

ここで何が起こるでしょうか。またタスクがないのはなぜでしょうか。Ansible は、操作を行う前にサーバーから「ファクト」を収集していることを認識している可能性があります。これらのファクトは、ネットワーク情報、OS/ディストリビューションのバージョンなど、あらゆる場合に役に立ちます。この場合は、更新を行う前に、環境内の全監視サーバーについて知っておく必要があります。そのため、この簡単なプレイにより、監視サーバーでファクト収集手順が強制されます。このパターンは時折確認し、覚えておくと便利です。

次の部分は更新のプレイです。最初の部分は以下のようになります。

.. code-block:: yaml

   - hosts: webservers
     user: root
     serial:1

これは、通常のプレイ定義で、``webservers`` グループで動作します。``serial`` キーワードは、Ansible に一度に操作するサーバー数を示します。これが指定されていないと、Ansible はこれらの操作を、設定ファイルで指定されているデフォルトの「フォーク」制限まで並列処理します。ただし、ゼロダウンタイムローリングアップグレードでは、多数のホストで一度に操作しない場合があります。Web サーバーの数が少ない場合は、たとえば ``serial`` を 1 に設定します (一度に 1 台のホスト)。100 台ある場合は、たとえば ``serial`` を 10 に設定します (一度に 10 台)。

以下は更新プレイの次の部分です。

.. code-block:: yaml

   pre_tasks:
   - name: disable nagios alerts for this host webserver service
     nagios:
       action: disable_alerts
       host: "{{ inventory_hostname }}"
       services: webserver
     delegate_to: "{{ item }}"
     loop: "{{ groups.monitoring }}"

   - name: disable the server in haproxy
     shell: echo "disable server myapplb/{{ inventory_hostname }}" | socat stdio /var/lib/haproxy/stats
     delegate_to: "{{ item }}"
     loop: "{{ groups.lbservers }}"

.. note::
   - ``serial`` キーワードにより、プレイを「バッチ」で強制的に実行します。各バッチは、ホストのサブ選択とともに完全なプレイとしてカウントされます。
     これにより、プレイの動作にいくつかの影響が生じます。たとえば、バッチのすべてのホストが失敗すると、プレイは失敗し、実行全体が失敗します。``max_fail_percentage`` と併用する場合には、これを考慮する必要があります。

``pre_tasks`` キーワードを使用すると、ロールが呼び出される前に実行するタスクを一覧表示できます。これにより、1 分でより妥当になります。これらのタスクの名前を見ると、Nagios アラートを無効にしてから、現在更新中の Web サーバーを HAProxy ロードバランシングプールから削除していることがわかります。

``delegate_to`` 引数および ``loop`` 引数を一緒に使用すると、Ansible が各監視サーバーとロードバランサーをループし、Web サーバーに「代わって」監視サーバーまたは負荷分散サーバーでその操作を実行 (操作を委譲) します。プログラミング用語では、外部ループは Web サーバーのリスト、内部ループは監視サーバーのリストになります。

HAProxy ステップは少し複雑になることに注意してください。 この例では HAProxy を使用していますが、これは無料で利用できるため、インフラストラクチャーに (たとえば) F5 や Netscaler がある場合 (あるいは AWS Elastic IP を設定している場合) は、代わりにコア Ansible に含まれるモジュールを使用して通信することができます。 Nagios の代わりに他の監視モジュールを使用する場合もありますが、ここでは「事前タスク」セクションの主な目的のみを示しており、サーバーは監視対象外になり、ローテーションがなくなります。

次の手順では、適切なロールを Web サーバーに再適用します。これにより、``web`` ロールおよび ``base-apache`` ロールの設定管理宣言が Web サーバーに適用されます。これには、Web アプリケーションコード自体の更新も含まれます。この方法で行う必要はありません。代わりに、単に Web アプリケーションを更新することもできますが、これはロールを使用してタスクを再利用する方法の良い例です。

.. code-block:: yaml

   roles:
   - common
   - base-apache
   - web

最後に、``post_tasks`` セクションで、Nuppet 設定への変更を元に戻し、Web サーバーを負荷分散プールに戻します。

.. code-block:: yaml

   post_tasks:
   - name: Enable the server in haproxy
     shell: echo "enable server myapplb/{{ inventory_hostname }}" | socat stdio /var/lib/haproxy/stats
     delegate_to: "{{ item }}"
     loop: "{{ groups.lbservers }}"

   - name: re-enable nagios alerts
     nagios:
       action: enable_alerts
       host: "{{ inventory_hostname }}"
       services: webserver
     delegate_to: "{{ item }}"
     loop: "{{ groups.monitoring }}"

NetScaler、F5、または Elastic Load Balancer を使用する場合は、代わりに適切なモジュールに置き換えてください。

.. _lamp_end_notes:

その他のロードバランサーの管理
=============================

この例では、単純な HAProxy ロードバランサーを使用して Web サーバーをフロントエンドします。これは簡単に設定でき、管理が容易です。前述したように、Ansible には、Citrix NetScaler、F5 BigIP、Amazon Elastic Load Balancers などのさまざまなロードバランサーのサポートが組み込まれています。詳細は「:ref:`working_with_modules`」ドキュメントを参照してください。

その他のロードバランサーについては、上記の HAProxy の場合と同様にシェルコマンドを送信するか、ロードバランサーが公開している場合は API を呼び出す必要があります。Ansible にモジュールがあるロードバランサーの場合、それが API に接続する場合は ``local_action`` として実行できます。ローカルアクションの詳細は「:ref:`playbooks_delegation`」セクションをご覧ください。 コアモジュールがないハードウェアで何か面白いものを開発すると、コアを組み込む優れたモジュールになる可能性があります。

.. _lamp_end_to_end:

継続的デリバリーのエンドツーエンド
==============================

更新プログラムをアプリケーションに自動的にデプロイできるようになりましたが、それをどのように結び付けますか。多くの組織では、`Jenkins <https://jenkins.io/>`_ や `Atlassian Bamboo <https://www.atlassian.com/software/bamboo>`_ のような継続的インテグレーションツールを使用して、開発、テスト、リリース、デプロイのステップを結び付けています。`Gerrit <https://www.gerritcodereview.com/>`_ などのツールを使用して、アプリケーションコード自体または Ansible Playbook、あるいはその両方にコミットするコードレビューステップを追加することもできます。

環境によっては、テスト環境に継続的にデプロイし、その環境に対して統合テストバッテリーを実行してから、実稼働環境に自動的にデプロイする場合があります。 または、シンプルに保ち、ローリングアップデートを使用して、特にテスト環境または実稼働環境にオンデマンドでデプロイすることもできます。 これはすべてあなた次第です。

継続的インテグレーションシステムとの統合では、``ansible-playbook`` コマンドラインツールを使用して、もしくは :ref:`ansible_tower` を使用している場合は ``tower-cli`` または組み込みの REST API を使用して、Playbook の実行を簡単にトリガーできます。 tower-cli コマンド「joblaunch」は、REST API 経由でリモートジョブを生成し、非常に洗練されています。

これにより、Ansible を使用して多層アプリケーションを構築し、顧客への継続的な配信を最終的な目標として、そのアプリで操作を調整 (オーケストレート) する方法について良い考えが浮かぶはずです。ローリングアップグレードのアイデアを、アプリのさまざまな部分に拡張できます。たとえば、フロントエンド Web サーバーをアプリケーションサーバーとともに追加するか、SQL データベースを MongoDB や Riak などに置き換えます。Ansible は、複雑な環境を簡単に管理し、一般的な操作を自動化する機能を提供します。

.. seealso::

   `lamp_haproxy の例 <https://github.com/ansible/ansible-examples/tree/master/lamp_haproxy>`_
       ここで説明した lamp_haproxy の例です。
   :ref:`working_with_playbooks`
       Playbook の概要
   :ref:`playbooks_reuse_roles`
       Playbook のロールの概要
   :ref:`playbooks_variables`
       Ansible 変数の概要
   `Ansible.com:継続的デリバリー <https://www.ansible.com/use-cases/continuous-delivery>`_
       Ansible を使用した継続的デリバリーの概要
