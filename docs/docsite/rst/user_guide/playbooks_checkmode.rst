.. _check_mode_dry:

チェックモード (「ドライラン」)
======================

.. versionadded:: 1.1

.. contents:: トピック

ansible-playbook を ``--check`` で実行すると、リモートシステムで変更は行われません。 代わりに、
「チェックモード」(プライマリーコアモジュールのほとんどを含みますが、すべてのモジュールで行わなければいけないわけではありません) をサポートするために、インストルメント化されたモジュールはいずれも、
変更を行うのではなく、行った変更を報告します。 チェックモードに対応していないその他のモジュールでも、アクションは実行されませんが、変更内容は報告されません。

チェックモードは単に有効で、以前のコマンドの結果に依存する条件を使用するステップがある場合には、
それほど役に立たない可能性があります。 ただし、一度に 1 つのノードに対する基本的な設定管理のユースケースには便利です。

例:

    ansible-playbook foo.yml --check

.. _forcing_to_run_in_check_mode:

タスクのチェックモードの有効化または無効化
``````````````````````````````````````````

.. versionadded:: 2.2

個々のタスクについてチェックモードの動作変更が必要になる場合があります。これは、``check_mode`` オプションを使用して行います。
このオプションは、タスクに追加できます。

以下のオプションがあります。

1. Playbook が ``--check`` **なし** で呼び出される場合でも、強制的にタスクを **チェックモードで** 実行します。これは ``check_mode: yes`` と呼ばれています。
2. Playbook が ``--check`` **で** 呼び出される場合でも、タスクを **通常モードで実行** することを強制し、システムに変更を加えます。これは ``check_mode: no`` と呼ばれます。

.. note:: バージョン 2.2 より前のバージョンでは、``check_mode: no`` と同等のもののみが存在します。この表記は ``always_run: yes`` です。

``yes``/``no`` の代わりに、``when`` 句と同様に Jinja2 式を使用できます。

例:

  tasks:
    - name: this task will make changes to the system even in check mode
      command: /something/to/run --even-in-check-mode
      check_mode: no

    - name: this task will always run under checkmode and not change the system
      lineinfile:
          line: "important config"
          dest: /path/to/myconfig.conf
          state: present
      check_mode: yes


``check_mode: yes`` で 1 つのタスクを実行すると、
ansible モジュールをテストするテストを作成するのに役立ちます。
このテストは、モジュール自体をテストするか、モジュールが変更を加える条件をテストします。
``register`` を使用して (:ref:`playbooks_conditionals` を参照)、
潜在的な変更を確認できます。

「変数」のチェックモードに関する情報
`````````````````````````````````````````

.. versionadded:: 2.1

チェックモードの一部のタスクでエラーをスキップまたは無視する場合は、
ブール値のマジック変数 ``ansible_check_mode`` を使用できます。
これは、チェックモード時に ``True`` に設定されます。

例:


  tasks:

    - name: this task will be skipped in check mode
      git:
        repo: ssh://git@github.com/mylogin/hello.git
        dest: /home/mylogin/hello
      when: not ansible_check_mode

    - name: this task will ignore errors in check mode
      git:
        repo: ssh://git@github.com/mylogin/hello.git
        dest: /home/mylogin/hello
      ignore_errors: "{{ ansible_check_mode }}"

.. _diff_mode:

``--diff`` で差異の表示
```````````````````````````````````

.. versionadded:: 1.1

ansible-playbook への ``--diff`` オプションは ``--check`` (上記を参照) で非常に役に立ちますが、単独で使用することもできます。
このフラグが指定され、モジュールがこれをサポートすると、Ansible は加えた変更をレポートします。``--check`` と併用した場合には、加えた変更は Ansible により報告されます。
これはほとんどの場合は、ファイル (テンプレートなど) を操作するモジュールで使用されますが、他のモジュールでも「前」および「後」の情報 (ユーザーなど) が表示される場合があります。
diff 機能は大量の出力を生成するため、一度に 1 つのホストをチェックする場合に最適な方法です。例::

    ansible-playbook foo.yml --check --diff --limit foo.example.com

.. versionadded:: 2.4

``--diff`` オプションを指定すると、機密情報が明らかになります。このオプションは、``diff: no`` を指定することでタスクに対して無効にできます。

例:

  tasks:
    - name: this task will not report a diff when the file changes
      template:
        src: secret.conf.j2
        dest: /etc/secret.conf
        owner: root
        group: root
        mode: '0600'
      diff: no
