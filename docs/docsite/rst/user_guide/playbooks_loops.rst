.. _playbooks_loops:

*****
ループ
*****

タスクを複数回繰り返す場合があります。コンピュータープログラミングでは、これはループと呼ばれます。一般的な Ansible ループには、:ref:`ファイルモジュール<file_module>` を使用して複数のファイルやディレクトリーの所有権の変更が含まれます。これにより、:ref:`ユーザーモジュール <user_module>` で複数のユーザーを作成し、
特定の結果に達成するまでポーリングの手順を繰り返します。Ansible はループを作成するためのキーワードである ``loop`` と ``with_<lookup>`` を提供します。

.. note::
   * Ansible 2.5 に ``loop`` が追加されました。``with_<lookup>`` には完全に代わりませんが、ほとんどのユースケースで推奨されます。
   * ``with_<lookup>`` の使用は非推奨になっていません。この構文は、今後も有効です。
   * ``loop`` 構文を改善する場合は、このページと `changelog` <https://github.com/ansible/ansible/tree/devel/changelogs>_ で更新を確認します。

.. contents::
   :local:

``loop`` と ``with_*`` の比較
=================================

* ``with_<lookup>`` キーワードは、:ref:`lookup_plugins` に依存します。さらに、``items`` は lookup です。
* ``loop`` キーワードは ``with_list`` と同等で、単純なループに最適です。
* ``loop`` キーワードは文字列を入力として受け付けません。「:ref:`query_vs_lookup`」を参照してください。
* 通常、「:ref:`migrating_to_loop`」で対応している ``with_*`` を使用すると、``loop`` を使用するように更新できます。
* ``with_items`` は暗黙的な単一レベルのフラット処理を実行するため、``with_items`` を ``loop`` に変更する場合は注意してください。正確な結果に一致するために、``loop`` で ``flatten(1)`` の使用が必要になる場合があります。たとえば、同じような出力を取得するには、以下を使用します。

.. code-block:: yaml

  with_items:
    - 1
    - [2,3]
    - 4

以下が必要です。

  loop: "{{ [1, [2,3] ,4] | flatten(1) }}"

* ループ内で ``lookup`` を使用する必要のある ``with_*`` ステートメントは、``loop`` キーワードを使用するよう変換しないでください。たとえば、代わりに、以下を行います。

.. code-block:: yaml

  loop: "{{ lookup('fileglob', '*.txt', wantlist=True) }}"

保持する方が見た目がすっきりします::

  with_fileglob: '*.txt'

.. _standard_loops:

標準ループ
==============

シンプルなリストでの反復
----------------------------

繰り返されるタスクは、文字列の単純なリストで標準ループとして記述できます。このリストはタスクに直接定義できます::

    - name: add several users
      user:
        name: "{{ item }}"
        state: present
        groups: "wheel"
      loop:
         - testuser1
         - testuser2

変数ファイルでリストを定義するか、プレイの「vars」セクションで、タスク内のリストの名前を参照します。

    loop: "{{ somelist }}"

これらの例のいずれも、以下と同等です::

    - name: add user testuser1
      user:
        name: "testuser1"
        state: present
        groups: "wheel"

    - name: add user testuser2
      user:
        name: "testuser2"
        state: present
        groups: "wheel"

一部のプラグインでリストを直接パラメーターに渡すことができます。:ref:`yum_module`、:ref:`apt_module` などのほとんどのパッケージモジュールにはこの機能があります。利用可能な場合は、リストをパラメーターに渡す方が、タスクにループするよりも適切です。例::

   - name: optimal yum
     yum:
       name: "{{  list_of_packages  }}"
       state: present

   - name: non-optimal yum, slower and may cause issues with interdependencies
     yum:
       name: "{{  item  }}"
       state: present
     loop: "{{  list_of_packages  }}"

:ref:`モジュールのドキュメント <modules_by_category>` で、特定モジュールのパラメーターにリストを渡すことができるかどうかを確認します。

ハッシュリストを繰り返し処理
-------------------------------

ハッシュリストがある場合は、ループでサブキーを参照できます。例::

    - name: add several users
      user:
        name: "{{ item.name }}"
        state: present
        groups: "{{ item.groups }}"
      loop:
        - { name: 'testuser1', groups: 'wheel' }
        - { name: 'testuser2', groups: 'root' }
    
:ref:`playbooks_conditionals` をループと組み合わせると、各アイテムについて ``when:`` ステートメントが個別に処理されます。
例は、:ref:`the_when_statement` を参照してください。

ディクショナリーでの反復
---------------------------

ディクショナリーでループするには、``dict2items`` :ref:`dict_filter` を使用します::

    - name: create a tag dictionary of non-empty tags
      set_fact:
        tags_dict: "{{ (tags_dict|default({}))|combine({item.key: item.value}) }}"
      loop: "{{ tags|dict2items }}"
      vars:
        tags:
          Environment: dev
          Application: payment
          Another: "{{ doesnotexist|default() }}"
      when: item.value != ""
    
ここでは、空のタグを設定しないため、空でないタグのみを含むディクショナリーを作成します。

ループによる変数の登録
=================================

ループの出力を変数として登録できます。例::

   - shell: "echo {{ item }}"
     loop:
       - "one"
       - "two"
     register: echo

ループで ``register`` を使用すると、変数に配置されたデータ構造には、モジュールからのすべての応答のリストである ``results`` 属性が含まれます。これは、ループなしで ``register`` を使用する際に返されるデータ構造とは異なります。

    {
        "changed": true,
        "msg": "All items completed",
        "results": [
            {
                "changed": true,
                "cmd": "echo \"one\" ",
                "delta": "0:00:00.003110",
                "end": "2013-12-19 12:00:05.187153",
                "invocation": {
                    "module_args": "echo \"one\"",
                    "module_name": "shell"
                },
                "item": "one",
                "rc": 0,
                "start": "2013-12-19 12:00:05.184043",
                "stderr": "",
                "stdout": "one"
            },
            {
                "changed": true,
                "cmd": "echo \"two\" ",
                "delta": "0:00:00.002920",
                "end": "2013-12-19 12:00:05.245502",
                "invocation": {
                    "module_args": "echo \"two\"",
                    "module_name": "shell"
                },
                "item": "two",
                "rc": 0,
                "start": "2013-12-19 12:00:05.242582",
                "stderr": "",
                "stdout": "two"
            }
        ]
    }
    
登録済みの変数で後続のループを実行して結果を検査すると、以下のようになります。

    - name: Fail if return code is not 0
      fail:
        msg: "The command ({{ item.cmd }}) did not have a 0 return code"
      when: item.rc != 0
      loop: "{{ echo.results }}"
    
反復時に、現在のアイテムの結果は変数に配置されます。

    - shell: echo "{{ item }}"
      loop:
        - one
        - two
      register: echo
      changed_when: echo.stdout != "one"

.. _complex_loops:

複雑なループ
=============

入れ子のリストでの反復
---------------------------

Jinja2 式を使用すると、複雑なリストを繰り返すことができます。たとえば、ループはネスト化されたリストを組み合わせることができます。

    - name: give users access to multiple databases
      mysql_user:
        name: "{{ item[0] }}"
        priv: "{{ item[1] }}.*:ALL"
        append_privs: yes
        password: "foo"
      loop: "{{ ['alice', 'bob'] |product(['clientdb', 'employeedb', 'providerdb'])|list }}"


.. _do_until_loops:

条件が満たされるまでタスクの再試行
----------------------------------------

.. versionadded:: 1.4

``until`` キーワードを使用して、特定の条件を満たすまでタスクを再試行できます。 以下は例です。

    - shell: /usr/bin/foo
      register: result
      until: result.stdout.find("all systems go") != -1
      retries:5
      delay:10

このタスクは、各試行の 10 秒の遅延で最大 5 回実行されます。任意の試行の結果が標準出力 (stdout) で「all systems go」の場合、タスクは成功します。「retries」のデフォルト値は 3 で、「delay」は 5 です。

個別の再試行の結果を表示するには、``-vv`` でプレイを実行します。

``until`` を使用してタスクを実行し、結果を変数として登録する場合は、登録済み変数には「attempts」というキーが含まれ、タスクの再試行回数を記録します。

.. note:: タスクを再試行するには、``until`` パラメーターを設定する必要があります。``until`` が定義されていない場合、``retries`` パラメーターの値は 1 に強制されます。

インベントリーのループ
----------------------

インベントリーをループしたり、そのサブセットのみをループするには、``ansible_play_batch`` 変数または ``groups`` 変数で通常の ``loop`` を使用します。

    # show all the hosts in the inventory
    - debug:
        msg: "{{ item }}"
      loop: "{{ groups['all'] }}"

    # show all the hosts in the current play
    - debug:
        msg: "{{ item }}"
      loop: "{{ ansible_play_batch }}"

また、以下のような特定の lookup プラグイン ``inventory_hostnames`` も使用できます。

    # show all the hosts in the inventory
    - debug:
        msg: "{{ item }}"
      loop: "{{ query('inventory_hostnames', 'all') }}"

    # show all the hosts matching the pattern, ie all but the group www
    - debug:
        msg: "{{ item }}"
      loop: "{{ query('inventory_hostnames', 'all:!www') }}"

パターンの詳細は、:ref:`intro_patterns` を参照してください。

.. _query_vs_lookup:

``loop`` のリスト入力の確保: ``query`` 対 ``lookup``
==========================================================

``loop`` キーワードは、リストを入力として要求しますが、``lookup`` キーワードは、デフォルトでコンマ区切りの値の文字列を返します。Ansible 2.5 では、常にリストを返す :ref:`query` という名前の新しい Jinja2 関数が導入され、``loop`` キーワードの使用時に lookup プラグインからより単純なインターフェースと予測可能な出力が提供されます。

``wantlist=True`` を使用して ``lookup`` がリストを ``loop`` に返すように強制したり、代わりに ``query`` を使用できます。

これらの例では、以下を行います。

    loop: "{{ query('inventory_hostnames', 'all') }}"

    loop: "{{ lookup('inventory_hostnames', 'all', wantlist=True) }}"


.. _loop_control:

ループへのコントロールの追加
========================
.. versionadded:: 2.1

``loop_control`` キーワードを使用すると、ループを便利な方法で管理できます。

``label`` を使用したループ出力の制限
-----------------------------------
.. versionadded:: 2.2

複雑なデータ構造をループするとき、タスクのコンソール出力が膨大になる可能性があります。表示される出力を制限するには、``label`` ディレクティブに ``loop_control`` を付けて使用します::

    - name: create servers
      digital_ocean:
        name: "{{ item.name }}"
        state: present
      loop:
        - name: server1
          disks: 3gb
          ram: 15Gb
          network:
            nic01: 100Gb
            nic02: 10Gb
            ...
      loop_control:
        label: "{{ item.name }}"
    
このタスクの出力には、複数行の ``{{ item }}`` 変数の内容全体ではなく、各 ``アイテム`` の ``item`` フィールドのみが表示されます。

.. note:: これは、機密性の高いデータを保護せずに、コンソールの出力をより読みやすくするために使用します。機密データが ``loop`` 内にある場合は、開示を防ぐために、タスクで ``no_log: yes`` を設定します。

ループ内での一時停止
---------------------
.. versionadded:: 2.2

タスクループの各アイテムの実行間隔を (秒単位) で制御するには、``loop_control`` で ``pause`` ディレクティブを使用します。

    # main.yml
    - name: create servers, pause 3s before creating next
      digital_ocean:
        name: "{{ item }}"
        state: present
      loop:
        - server1
        - server2
      loop_control:
        pause: 3

``index_var`` のあるループでの進捗の追跡
---------------------------------------------------
.. versionadded:: 2.5

ループ内の場所を追跡するには、``loop_control`` で ``index_var`` ディレクティブを使用します。このディレクティブは、現在のループインデックスを含む変数名を指定します。

  - name: count our fruit
    debug:
      msg: "{{ item }} with index {{ my_idx }}"
    loop:
      - apple
      - banana
      - pear
    loop_control:
      index_var: my_idx

``loop_var`` を使用した内部変数および外部変数名の定義
---------------------------------------------------------
.. versionadded:: 2.1

``include_tasks`` を使用して 2 つのループタスクをネスト化できます。ただし、デフォルトでは Ansible は各ループのループ変数の ``アイテム`` を設定します。これは、内部のネストされたループが外部ループからの ``アイテム`` の値を上書きすることを意味します。
``loop_var`` を ``loop_control`` とともに使用して、各ループの変数名を指定できます。

    # main.yml
    - include_tasks: inner.yml
      loop:
        - 1
        - 2
        - 3
      loop_control:
        loop_var: outer_item

    # inner.yml
    - debug:
        msg: "outer item={{ outer_item }} inner item={{ item }}"
      loop:
        - a
        - b
        - c

.. note:: Ansible が、定義されている変数を使用していることを現在のループが検出すると、タスクが失敗するためにエラーが発生します。

拡張ループ変数
-----------------------
.. versionadded:: 2.8

Ansible 2.8 では、``拡張`` オプションを使用してループ制御に拡張ループ情報を取得できます。このオプションは、以下の情報を公開します。

==========================  ===========
変数                    説明
--------------------------  -----------
``ansible_loop.allitems``   ループ内のすべてのアイテムのリスト。
``ansible_loop.index``      ループの現在の反復。(1 インデックス化)
``ansible_loop.index0``     ループの現在の反復。(0 インデックス化)
``ansible_loop.revindex``   ループの最後からの反復回数 (1 インデックス化)
``ansible_loop.revindex0``  ループの最後からの反復回数 (0 インデックス化)
``ansible_loop.first``      最初の反復の場合は ``True``。
``ansible_loop.last``       最後の反復の場合は ``True``。
``ansible_loop.length``     ループ内のアイテム数。
``ansible_loop.previtem``   ループの以前の反復のアイテム。最初の反復時に未定義です。
``ansible_loop.nextitem``   ループの次の反復からのアイテム。最後の反復時に未定義です。
==========================  ===========

::

      loop_control:
        extended: yes

loop_var の名前へのアクセス
-----------------------------------
.. versionadded:: 2.8

Ansible 2.8 では、``ansible_loop_var`` 変数を使用して ``loop_control.loop_var`` に提供された値の名前を取得できます。

ロールの作成者は、必要な ``loop_var`` 値を指定する代わりに、ループを許可するロールを作成することで、次の方法で値を収集できます。

    "{{ lookup('vars', ansible_loop_var) }}"

.. _migrating_to_loop:

with_X から loop への移行
=============================

.. include:: shared_snippets/with2loop.txt

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   :ref:`playbooks_best_practices`
       Playbook のベストプラクティス
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_variables`
       変数の詳細
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
