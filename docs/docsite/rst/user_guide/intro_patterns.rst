.. _intro_patterns:

パターン: ホストおよびグループを対象とする
====================================

アドホックコマンドまたは Playbook から Ansible を実行する場合には、実行する管理ノードまたはグループを選択する必要があります。パターンにより、インベントリー内の特定のホストやグループに対してコマンドおよび Playbook を実行できます。Ansible パターンは、1 台のホスト、IP アドレス、インベントリーグループ、グループセット、またはインベントリーのすべてのホストを参照できます。パターンは柔軟性が高く、ホストのサブセットを除外または要求したり、ワイルドカードや正規表現を使用したりできます。Ansible は、パターンに含まれるすべてのインベントリーホストで実行します。

.. contents::
   :local:

パターンの使用
--------------

アドホックコマンドまたは Playbook を実行する際は、ほとんどいつでもパターンを使用できます。パターンは、フラグのない :ref:`アドホックコマンド<intro_adhoc>` の唯一の要素です。通常、これは 2 番目の要素です。

    ansible <pattern> -m <module_name> -a "<module options>""

例::

    ansible webservers -m service -a "name=httpd state=restarted"

Playbook では、パターンは各プレイの ``hosts:`` 行の内容になります。

.. code-block:: yaml

   - name: <play_name>
     hosts: <pattern>

例::

    - name: restart webservers
      hosts: webservers

多くの場合、コマンドまたは Playbook を複数のホストに対して一度に実行するため、パターンは多くの場合インベントリグループを参照します。アドホックコマンドと上記の Playbook は、``webservers`` グループ内のすべてのマシンに対して実行されます。

.. _common_patterns:

一般的なパターン
---------------

以下の表は、インベントリーホストおよびグループを対象に設定する一般的なパターンを示しています。

.. table::
   :class: documentation-table

   ====================== ================================ ===================================================
   説明            パターン                       ターゲット
   ====================== ================================ ===================================================
   すべてのホスト              すべて (または \*)

   1 台のホスト               host1

   複数のホスト         host1:host2 (または host1,host2)

   1 つのグループ              webservers

   複数のグループ        webservers:dbservers             webservers 上のすべてのホストと、dbservers 上のすべてのホスト

   グループの除外       webservers:!atlanta              atlanta 上のホストを除く webservers のすべてのホスト

   グループの包含 webservers:&staging              ステージ状態にある webservers のすべてのホスト
   ====================== ================================ ===================================================

.. note:: ホストの一覧を指定する場合は、コンマ (``,``) またはコロン (``:``) のいずれかを使用できます。範囲と IPv6 アドレスを扱う場合は、コンマが推奨されます。

基本的なパターンを把握したら、それを組み合わせることができます。この例では、以下のようになります。

    webservers:dbservers:&staging:!phoenix

「phoenix」グループのマシンを除き、
「staging」グループにある「webservers」グループおよび「dbservers」グループにあるすべてのマシンを対象とします。

ホストがインベントリーで FQDN または IP アドレスにより名前が付けられている限り、FQDN または IP アドレスでワイルドカードパターンを使用できます。

   192.0.\*
   \*.example.com
   \*.com

ワイルドカードパターンおよびグループを同時に組み合わせることができます。

    one*.com:dbservers

パターンの制限
-----------------------

パターンはインベントリーによって異なります。ホストまたはグループがインベントリーに記載されていない場合は、ターゲットにパターンを使用することはできません。パターンにインベントリーに表示されない IP アドレスまたはホスト名が含まれる場合は、以下のようなエラーが表示されます。

.. code-block:: text

   [WARNING]:No inventory was parsed, only implicit localhost is available
   [WARNING]:Could not match supplied host pattern, ignoring: *.not_in_inventory.com

お使いのパターンはインベントリー構文に一致する必要があります。ホストを :ref:`alias<inventory_aliases>` として定義する場合は、以下の指定します。

.. code-block:: yaml

    atlanta:
      host1:
        http_port:80
        maxRequestsPerChild:808
        host:127.0.0.2

エイリアスをパターンで使用する必要があります。上記の例では、パターンで ``host1`` を使用する必要があります。IP アドレスを使用する場合は、以下のようなエラーが再度表示されます。

   [WARNING]:Could not match supplied host pattern, ignoring:127.0.0.2

詳細なパターンオプション
------------------------

上記の一般的なパターンはほとんどのニーズに対応しますが、Ansible では、対象とするホストおよびグループを定義する他の方法もいくつか提供します。

パターンにおける変数の使用
^^^^^^^^^^^^^^^^^^^^^^^^^^^

変数を使用して ``-e`` 引数を使用してグループ指定子を ansible-playbook に渡すことができます。

    webservers:!{{ excluded }}:&{{ required }}

パターンにおけるグループの位置の使用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ホストまたはホストのサブセットは、グループ内のその位置で定義できます。たとえば、以下のグループの場合は、

    [webservers]
    cobweb
    webbing
    weber

subscripts を使用して、webservers グループ内のホストまたは範囲を個別に選択できます。

    webservers[0]       # == cobweb
    webservers[-1]      # == weber
    webservers[0:2]     # == webservers[0],webservers[1]
                        # == cobweb,webbing
    webservers[1:]      # == webbing,weber
    webservers[:3]      # == cobweb,webbing,weber

パターンで正規表現の使用
^^^^^^^^^^^^^^^^^^^^^^^^^

パターンを正規表現として指定するには、``~``:: でパターンを開始します。

    ~(web|db).*\.example\.com

パターンおよび ansible-playbook フラグ
-----------------------------------

Playbook で定義したパターンの動作は、コマンドラインオプションを使用して変更できます。たとえば ``-i 127.0.0.2,`` を指定して、1 台のホストで ``hosts: all`` を定義する Playbook を実行できます。これは、対象とするホストがインベントリーで定義されていない場合でも有効です。``--limit`` フラグを使用して、特定の実行で対象とするホストを制限することもできます。

    ansible-playbook site.yml --limit datacenter2

最後に ``--limit`` を使用して、ファイル名の前に ``@`` を付けることで、ファイルからホストの一覧を読み込むことができます。

    ansible-playbook site.yml --limit @retry_hosts.txt

Ansible コマンドおよび Playbook でパターンに関する知識を活用するには、:ref:`intro_adhoc` および :ref:`playbooks_intro` を参照してください。

.. seealso::

   :ref:`intro_adhoc`
       基本コマンドの例
   :ref:`working_with_playbooks`
       Ansible の設定管理言語について
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
