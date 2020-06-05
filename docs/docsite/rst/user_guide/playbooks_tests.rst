.. _playbooks_tests:

Test
-----

.. contents:: トピック


Jinja の `Test <http://jinja.pocoo.org/docs/dev/templates/#tests>`_ は、テンプレート式を評価し、True または False を返す方法です。
Jinja には、これらの多くが同梱されています。公式の Jinja テンプレートドキュメントの「`builtin tests`_」を参照してください。

テストとフィルターの主な相違点は、Jinja テストが比較に使用される点です。Jira ではフィルターはデータ操作に使用され、アプリケーションが異なります。テストは、``map()`` や ``select()`` などのリスト処理フィルターで使用して、リスト内の項目を選択することもできます。

すべてのテンプレートと同様に、テストは常に、ローカルデータをテストする際にタスクのターゲットでは **なく**、Ansible コントローラーで実行されます。

このような Jinja2 テストに加えて、Ansible はより多くのものを提供しており、ユーザーは独自のテストを簡単に作成できます。

.. _test_syntax:

Test の構文
```````````

`Test の構文 <http://jinja.pocoo.org/docs/dev/templates/#tests>`_ は、`フィルター構文 <http://jinja.pocoo.org/docs/dev/templates/#filters>`_ (``variable | filter``) とは異なります。従来の Ansible では、jinja のテストとフィルターの両方がテストとして登録されており、フィルター構文を使用してそれを参照できます。

Ansible 2.5 の時点では、jinja テストをフィルターとして使用すると警告が生成されます。

jinja テストを使用するための構文は、以下のとおりです。

    variable is test_name

例::

    result is failed

.. _testing_strings:

文字列のテスト
```````````````

サブ文字列または正規表現に対して文字列と一致させるには、フィルターの「match」、「search」、または「regex」を使用します。

    vars:
      url: "http://example.com/users/foo/resources/bar"

    tasks:
        - debug:
            msg: "matched pattern 1"
          when: url is match("http://example.com/users/.*/resources/.*")

        - debug:
            msg: "matched pattern 2"
          when: url is search("/users/.*/resources/.*")

        - debug:
            msg: "matched pattern 3"
          when: url is search("/users/")

        - debug:
            msg: "matched pattern 4"
          when: url is regex("example.com/\w+/foo")

「match」には文字列の先頭にゼロ以上の文字が必要です。「search」には文字列のサブセットの一致のみが必要になります。デフォルトでは、「regex」は `search` のように機能しますが、`regex` 表現は他のテストも実行するように設定できます。

.. _testing_versions:

バージョン比較
``````````````````

.. versionadded:: 1.6

.. note:: 2.5 では、``version_compare`` の名前が ``version`` に変更されました。

``ansible_facts['distribution_version']`` バージョンが「12.04」以降であることを確認するなど、
バージョン番号を比較するには、``version`` テストを使用できます。

``version`` テストを使用して ``ansible_facts['distribution_version']`` を評価することもできます::

    {{ ansible_facts['distribution_version'] is version('12.04', '>=') }}

``ansible_facts['distribution_version']`` が 12.04 以上の場合は、このテストで True が返り、それ以外の場合は False が返ります。

``version`` テストでは、以下の演算子を受け入れます。

    <, lt, <=, le, >, gt, >=, ge, ==, =, eq, !=, <>, ne

このテストは、3 番目のパラメーター (``strict``) も受け入れます。これは、``distutils.version.StrictVersion`` で定義されている厳格なバージョン解析を使用すべきかどうかを定義します。 デフォルトは、``False`` (``distutils.version.LooseVersion`` を使用) で、``True`` は厳格なバージョン解析を有効にします::

    {{ sample_version_var is version('1.0', operator='lt', strict=True) }}


.. _math_tests:

セット理論テスト
````````````````

.. versionadded:: 2.1

.. note:: 2.5 では、``issubset`` と ``issuperset`` の名前が、``subset`` および ``superset`` にそれぞれ変更になりました。

リストに別のリストが含まれているか、またはリストが別のリストに含まれているかを確認するには、「subset」および「superset」を使用します::

    vars:
        a: [1,2,3,4,5]
        b: [2,3]
    tasks:
        - debug:
            msg:"A includes B"
          when: a is superset(b)

        - debug:
            msg:"B is included in A"
          when: b is subset(a)

.. _contains_test:

リストに値が含まれるかどうかのテスト
```````````````````````````````

.. versionadded:: 2.8

Ansible には、同様に動作する ``contains`` テストが含まれますが、``in`` テストで提供される Jinja2 とは逆の動作が含まれています。
``contains`` テストは、``select`` フィルター、``reject`` フィルター、``selectattr``、および ``rejectattr`` フィルターと連携するように設計されています。

    vars:
      lacp_groups:
        - master: lacp0
          network:10.65.100.0/24
          gateway:10.65.100.1
          dns4:
            - 10.65.100.10
            - 10.65.100.11
          interfaces:
            - em1
            - em2

        - master: lacp1
          network:10.65.120.0/24
          gateway:10.65.120.1
          dns4:
            - 10.65.100.10
            - 10.65.100.11
          interfaces:
              - em3
              - em4

    tasks:
      - debug:
          msg: "{{ (lacp_groups|selectattr('interfaces', 'contains', 'em1')|first).master }}"

.. _path_tests:

.. versionadded:: 2.4

`any` および `all` を使用して、リスト内のいずれかの要素が true かどうかを確認できます。

  vars:
    mylist:
        - 1
        - "{{ 3 == 3 }}"
        - True
    myotherlist:
        - False
        - True
  tasks:

    - debug:
        msg: "all are true!"
      when: mylist is all

    - debug:
        msg: "at least one is true"
      when: myotherlist is any


パスのテスト
`````````````

.. note:: 2.5 では、以下のテストの名前が変更になり、``is_`` 接頭辞が削除されました。

以下のテストは、コントローラー上のパスに関する情報を提供します。

    - debug:
        msg: "path is a directory"
      when: mypath is directory

    - debug:
        msg: "path is a file"
      when: mypath is file

    - debug:
        msg: "path is a symlink"
      when: mypath is link

    - debug:
        msg: "path already exists"
      when: mypath is exists

    - debug:
        msg: "path is {{ (mypath is abs)|ternary('absolute','relative')}}"

    - debug:
        msg: "path is the same file as path2"
      when: mypath is same_file(path2)

    - debug:
        msg: "path is a mount"
      when: mypath is mount


.. _test_task_results:

タスクの結果
````````````

以下のタスクは、タスクのステータスを確認するためのテストを示しています。

    tasks:

      - shell: /usr/bin/foo
        register: result
        ignore_errors: True

      - debug:
          msg: "it failed"
        when: result is failed

      # in most cases you'll want a handler, but if you want to do something right now, this is nice
      - debug:
          msg: "it changed"
        when: result is changed

      - debug:
          msg: "it succeeded in Ansible >= 2.1"
        when: result is succeeded

      - debug:
          msg: "it succeeded"
        when: result is success

      - debug:
          msg: "it was skipped"
        when: result is skipped

.. note:: 2.1 以降、文法を厳密にする必要がある場合に、success、failure、change、および skip を使用して、文法が一致できるようにすることもできます。



.. _builtin tests: http://jinja.pocoo.org/docs/templates/#builtin-tests

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_variables`
       変数の詳細
   :ref:`playbooks_loops`
       Playbook でのループ
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   :ref:`playbooks_best_practices`
       Playbook のベストプラクティス
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
