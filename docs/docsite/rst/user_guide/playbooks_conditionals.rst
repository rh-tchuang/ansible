.. _playbooks_conditionals:

条件 (Conditional)
============

.. contents:: トピック


多くの場合、プレイの結果は変数の値、ファクト (リモートシステムに関するもの)、または以前のタスク結果に依存する場合があります。
変数の値が他の変数に依存する場合があります。
ホストが他の基準に合致するかどうかに基づいてホストを管理するため、追加のグループを作成できます。このトピックでは、Playbook で条件がどのように使用されているかを説明します。

.. note:: Ansible で実行フローを制御するオプションは多数あります。サポートされるその他の条件の例は、http://jinja.pocoo.org/docs/dev/templates/#comparisons を参照してください。


.. _the_when_statement:

When ステートメント
``````````````````

特定のホストで特定のステップをスキップしたい場合があります。
これは、オペレーティングシステムが特定のバージョンである場合に、特定のパッケージをインストールしないという単純なものである場合もあれば、
または、ファイルシステムがいっぱいになった場合にクリーンアップ手順を実行するようなものかもしれません。

これは、Ansible で `when` 句を使用して簡単に実行できます。これには、二重中括弧のない生の Jinja2 式が含まれます (:ref:`group_by_module` を参照)。
これは実際には単純なものです。

    tasks:
      - name: "shut down Debian flavored systems"
        command: /sbin/shutdown -t now
        when: ansible_facts['os_family'] == "Debian"
        # note that all variables can be used directly in conditionals without double curly braces

括弧を使用して、条件をグループ化することもできます。

    tasks:
      - name: "shut down CentOS 6 and Debian 7 systems"
        command: /sbin/shutdown -t now
        when: (ansible_facts['distribution'] == "CentOS" and ansible_facts['distribution_major_version'] == "6") or
              (ansible_facts['distribution'] == "Debian" and ansible_facts['distribution_major_version'] == "7")

すべてが true である必要のある複数の条件 (論理的「and」) もリストとして指定できます。

    tasks:
      - name: "shut down CentOS 6 systems"
        command: /sbin/shutdown -t now
        when:
          - ansible_facts['distribution'] == "CentOS"
          - ansible_facts['distribution_major_version'] == "6"

多くの Jinja2 の「テスト」と「フィルター」も、when ステートメントで使用できます。
その一部は一意で、Ansible によって提供されます。 1 つのステートメントのエラーを無視して、
成功か失敗かに基づいて、条件付きで何かを行うことを決定するとします。

    tasks:
      - command: /bin/false
        register: result
        ignore_errors: True

      - command: /bin/something
        when: result is failed

      # In older versions of ansible use ``success``, now both are valid but succeeded uses the correct tense.
      - command: /bin/something_else
        when: result is succeeded

      - command: /bin/still/something_else
        when: result is skipped


.. note:: `success` と `succeeded` の両方 (`fail`/`failed` など) が有効です。


特定のシステムで利用可能なファクトを確認するには、Playbook で以下を実行できます。

    - debug: var=ansible_facts


ヒント: 場合によっては、文字列である変数を取得し、それに対して数学演算の比較を行いたいことがあります。 これは、以下のように実行できます。

    tasks:
      - shell: echo "only on Red Hat 6, derivatives, and later"
        when: ansible_facts['os_family'] == "RedHat" and ansible_facts['lsb']['major_release']|int >= 6

.. note:: 上記の例では、「lsb major_release」ファクトを返すために、ターゲットホストで lsb_release パッケージが必要になります。

Playbook またはインベントリーで定義される変数も使用できます。`|bool` フィルターをブール値以外の変数に適用してください (文字列変数「yes」、「on」、「1」、「true」など）。 たとえば、変数のブール値に基づいてタスクを実行する例を示します。

    vars:
      epic: true
      monumental: "yes"

条件の実行は以下のようになります。

    tasks:
        - shell: echo "This certainly is epic!"
          when: epic or monumental|bool

または::

    tasks:
        - shell: echo "This certainly isn't epic!"
          when: not epic

必要な変数が設定されていない場合は、省略するか、Jinja2 の `定義済み` テストを使用して失敗します。例::

    tasks:
        - shell: echo "I've got '{{ foo }}' and am not afraid to use it!"
          when: foo is defined

        - fail: msg="Bailing out. this play requires 'bar'"
          when: bar is undefined

これは、特に vars ファイルの条件付きインポートと組み合わせると役に立ちます (下記参照)。
例のように、変数はすでに暗示されているため、条件内で変数を使用する `{{ }}` は必要ありません。

.. _loops_and_conditionals:

ループおよび条件
``````````````````````
`when` をループと組み合わせる (:ref:`playbooks_loops` を参照) と、各項目について `when` ステートメントが個別に処理されることに注意してください。これは、以下のように設計されます。

    tasks:
        - command: echo {{ item }}
          loop: [ 0, 2, 4, 6, 8, 10 ]
          when: item > 5

定義されたループ変数に応じてタスク全体を省略する必要がある場合は、`|default` フィルターを使用して空のイテレーターを指定します。

        - command: echo {{ item }}
          loop: "{{ mylist|default([]) }}"
          when: item > 5


ループで dict を使用している場合は、以下のようになります。

        - command: echo {{ item.key }}
          loop: "{{ query('dict', mydict|default({})) }}"
          when: item.value > 5
    
.. _loading_in_custom_facts:

カスタムファクトでの読み込み
```````````````````````

また、必要に応じて独自のファクトを指定することも簡単です。これについては「:ref:`developing_modules`」で説明します。 そのようなファクトを実行する場合は、
タスクリストの一番上にある独自のカスタムファクト収集モジュールを呼び出すだけで、
そこに返される変数に将来のタスクからアクセスできるようになります。

    tasks:
        - name: gather site specific fact data
          action: site_facts
        - command: /usr/bin/thingy
          when: my_custom_fact_just_retrieved_from_the_remote_system == '1234'

.. _when_roles_and_includes:

「When」のロール、インポート、およびインクルードへの適用
```````````````````````````````````````````````

複数のタスクがすべて同じ条件ステートメントを共有する場合は、
以下のように条件をタスクインクルードステートメントに付加できることに注意してください。 すべてのタスクが評価されますが、条件はすべてのタスクに適用されます。

    - import_tasks: tasks/sometasks.yml
      when: "'reticulating splines' in output"

.. note:: 2.0 よりも前のバージョンでは、これはタスクインクルードで機能しましたが、Playbook のインクルードでは機能しません。 2.0 では、両方で機能します。

またはロールで使用します。

    - hosts: webservers
      roles:
         - role: debian_stock_config
           when: ansible_facts['os_family'] == 'Debian'

この条件に一致しないシステムでこのアプローチを使用すると、Ansible ではデフォルトで「skipped」出力が多数記録されます。
多くの場合、:ref:`group_by モジュール <group_by_module>` は、同じことを実現するより効率的な方法です。
「:ref:`os_variance`」を参照してください。

インポートの代わりに ``include_*`` タスクで条件が使用される場合、これはインクルードタスク自体に `のみ` 適用され、
インクルードファイルに含まれるその他のタスクには適用されません。この区別が重要な状況は、以下のとおりです。

    # We wish to include a file to define a variable when it is not
    # already defined

    # main.yml
    - import_tasks: other_tasks.yml # note "import"
      when: x is not defined

    # other_tasks.yml
    - set_fact:
        x: foo
    - debug:
        var: x

これは、インクルード時に、次と同じように展開されます::

    - set_fact:
        x: foo
      when: x is not defined
    - debug:
        var: x
      when: x is not defined

``x`` が最初に定義されていないと、``debug`` タスクはスキップされます。 ``import_tasks`` の代わりに ``include_tasks`` を使用することにより、
``other_tasks.yml`` からの両方のタスクが期待どおりに実行されます。

``include`` と ``import`` の相違点は、:ref:`playbooks_reuse` を参照してください。

.. _conditional_imports:

条件付きインポート
```````````````````

.. note:: これは、頻繁に使用されない高度なトピックです。

特定の基準に基づいて Playbook で特定の動作が異なる場合があります。
複数のプラットフォームおよび OS バージョンで動作する Playbook がある方がよい例です。

たとえば、Apache パッケージの名前は CentOS と Debian の間で異なる場合があります。
ただし、Ansible Playbook では、最小限の構文で簡単に処理されます。

    ---
    - hosts: all
      remote_user: root
      vars_files:
        - "vars/common.yml"
        - [ "vars/{{ ansible_facts['os_family'] }}.yml", "vars/os_defaults.yml" ]
      tasks:
      - name: make sure apache is started
        service: name={{ apache }} state=started

.. note::
   変数「ansible_facts['os_family']」は、
   vars_files に定義されているファイル名のリストに挿入されています。

各種の YAML ファイルにはキーと値のみが含まれます::

    ---
    # for vars/RedHat.yml
    apache: httpd
    somethingelse: 42

どのように機能しますか。 Red Hat オペレーティングシステム (「CentOS」など) の場合は、
Ansible がインポートしようとする最初のファイルは「vars/RedHat.yml」です。そのファイルが存在しない場合、Ansible は「vars/os_defaults.yml」の読み込みを試みます。リストにファイルが見つからなかった場合は、
エラーが発生します。

Debian では、
Ansible は最初に「vars/RedHat.yml」ではなく「vars/Debian.yml」を探してから、「vars/os_defaults.yml」に戻ります。

Ansible の設定アプローチ - 変数をタスクから分離し、
Playbook がネストされた条件付きの任意のコードにならないようにします。追跡する決定ポイントが少ないため、より単純で監査可能な構成ルールが得られます。

変数に基づくファイルとテンプレートの選択
````````````````````````````````````````````````

.. note:: これは、頻繁に使用されない高度なトピックです。 このセクションは、おそらく読み飛ばすことができます。

コピーする設定ファイルや使用するテンプレートが変数に依存する場合があります。
以下のコンストラクトは、特定ホストの変数に適した使用可能な最初のファイルを選択します。これにより、テンプレートに if 条件が多数ある場合よりも分かりやすくなります。

以下の例は、CentOS と Debian で大きく異なる設定ファイルをテンプレート化する方法を示しています。

    - name: template a file
      template:
          src: "{{ item }}"
          dest: /etc/myapp/foo.conf
      loop: "{{ query('first_found', { 'files': myfiles, 'paths': mypaths}) }}"
      vars:
        myfiles:
          - "{{ansible_facts['distribution']}}.conf"
          -  default.conf
        mypaths: ['search_location_one/somedir/', '/opt/other_location/somedir/']
    
登録変数
``````````````````

Playbook では、特定のコマンドの結果を変数に保存して、
後でアクセスすると便利な場合があります。 この方法でコマンドモジュールを使用すると、多くの点でサイト固有のファクトを記述する必要がなくなります。
たとえば、特定のプログラムが存在するかどうかをテストできます。

.. note:: 登録は、条件によりタスクが省略された場合でも行われます。これにより、``is skipped`` の変数をクエリーして、タスクが試行されたかどうかを判断します。

「register」 キーワードは、結果を保存する変数を決定します。 生成される変数は、テンプレート、アクション行、または *when* ステートメントで使用できます。 これは、以下のようになります (簡単な例の場合)::

    - name: test play
      hosts: all

      tasks:

          - shell: cat /etc/motd
            register: motd_contents

          - shell: echo "motd contains the word hi"
            when: motd_contents.stdout.find('hi') != -1

前述のように、登録した変数の文字列の内容は、「stdout」の値でアクセスできます。
登録した結果は、以下のようにリストに変換されている (またはすでにリストになっている) 場合、タスクのループで使用できます。
「stdout_lines」は、
すでにオブジェクトでも使用できますが、
必要に応じて「home_dirs.stdout.split()」を呼び出し、他のフィールドで分割することもできます::

    - name: registered variable usage as a loop list
      hosts: all
      tasks:

        - name: retrieve the list of home directories
          command: ls /home
          register: home_dirs

        - name: add home dirs to the backup spooler
          file:
            path: /mnt/bkspool/{{ item }}
            src: /home/{{ item }}
            state: link
          loop: "{{ home_dirs.stdout_lines }}"
          # same as loop: "{{ home_dirs.stdout.split() }}"
    

前述のように、登録した変数の文字列の内容は、「stdout」の値でアクセスできます。
登録された変数の文字列の内容が空かどうかを確認できます::

    - name: check registered variable for emptiness
      hosts: all

      tasks:

          - name: list contents of directory
            command: ls mydir
            register: contents

          - name: check contents for emptiness
            debug:
              msg: "Directory is empty"
            when: contents.stdout == ""

一般的に使用されるファクト
```````````````````

以下のファクトは条件で頻繁に使用されます。例については、上記を参照してください。

.. _ansible_distribution:

ansible_facts['distribution']
-----------------------------

使用できる値 (関連リストではなく一部です):

    Alpine
    Altlinux
    Amazon
    Archlinux
    ClearLinux
    Coreos
    CentOS
    Debian
    Fedora
    Gentoo
    Mandriva
    NA
    OpenWrt
    OracleLinux
    RedHat
    Slackware
    SMGL
    SUSE
    Ubuntu
    VMwareESX

..「`OSDIST_LIST`」を参照してください。

.. _ansible_distribution_major_version:

ansible_facts['distribution_major_version']
-------------------------------------------

これは、オペレーティングシステムのメジャーバージョンになります。たとえば、Ubuntu 16.04 の場合は、値が `16` になります。

.. _ansible_os_family:

ansible_facts['os_family']
--------------------------

使用できる値 (関連リストではなく一部です):

    AIX
    Alpine
    Altlinux
    Archlinux
    Darwin
    Debian
    FreeBSD
    Gentoo
    HP-UX
    Mandrake
    RedHat
    SGML
    Slackware
    Solaris
    Suse
    Windows

..Ansible は、`OS_FAMILY_MAP` を確認します。一致するものがない場合は、`platform.system()` の値を返します。

.. seealso::

   :ref:`working_with_playbooks`
       Playbook の概要
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   :ref:`playbooks_best_practices`
       Playbook のベストプラクティス
   :ref:`playbooks_variables`
       変数の詳細
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
