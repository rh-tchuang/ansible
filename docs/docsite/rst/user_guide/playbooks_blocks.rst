.. _playbooks_blocks:

Block
======

Block は、タスクの論理グループおよびプレイのエラー処理を許可します。単一タスク (ループを除く) に適用できるほとんどのタスクはブロックレベルで適用できるため、タスクに共通するデータまたはディレクティブの設定がより簡単になります。これは、ディレクティブがブロック自体に影響を与えるわけではありませんが、ブロックで囲まれたタスクに引き継がれます。つまり、ブロック自体ではなく、タスクに適用される `タイミング` です。


.. code-block:: YAML
 :emphasize-lines:3
 :caption: 内部に名前付きタスクを含む block の例

  tasks:
    - name:Install, configure, and start Apache
      block:
        - name: install httpd and memcached
          yum:
            name:
            - httpd
            - memcached
            state: present

        - name: apply the foo config template
          template:
            src: templates/src.j2
            dest: /etc/foo.conf
        - name: start service bar and enable it
          service:
            name: bar
            state: started
            enabled:True
      when: ansible_facts['distribution'] == 'CentOS'
      become: true
      become_user: root
      ignore_errors: yes

上記の例では、3 つの各タスクはブロックから `when` 条件を追加し、
タスクのコンテキストで評価してから実行されます。また、引用符で囲まれたすべてのタスクに対して、
特権昇格ディレクティブを継承して「become to root」を有効化します。最後に、``ignore_errors: yes`` は、一部のタスクが失敗しても Playbook の実行を継続します。

ブロック内のタスクの名前は、Ansible 2.3 以降で利用できます。Playbook の実行時に実行するタスクが分かりやすくなるように、ブロック内またはその他のすべてのタスクで名前を使用することが推奨されます。

.. _block_error_handling:

ブロックのエラー処理
`````````````````````

また、ブロックには、ほとんどのプログラミング言語で例外を処理するのと同じような方法でエラーを処理する機能が導入されています。
ブロックは、タスクの「faileded」ステータスのみを処理します。問題のあるタスク定義または到達不可能なホストは、「復旧可能な可能」エラーではありません。

.. _block_rescue:
.. code-block:: YAML
 :emphasize-lines: 3,10
 :caption: Block error handling example

  tasks:
  - name: Handle the error
    block:
      - debug:
          msg: 'I execute normally'
      - name: i force a failure
        command: /bin/false
      - debug:
          msg: 'I never execute, due to the above task failing, :-('
    rescue:
      - debug:
          msg: 'I caught an error, can do stuff here to fix it, :-)'

これにより、実行に失敗したタスクのステータスが「取り消され」、成功したかのように再生が続行されます。

また、``always`` セクションもあります。これは、タスクのステータスに関係なく実行されます。

.. _block_always:
.. code-block:: YAML
 :emphasize-lines: 2,9
 :caption: Block with always section

  - name: Always do X
    block:
      - debug:
          msg: 'I execute normally'
      - name: i force a failure
        command: /bin/false
      - debug:
          msg: 'I never execute :-('
    always:
      - debug:
          msg: "This always executes, :-)"

これをすべて一緒に追加して、複雑なエラー処理を実行できます。

.. code-block:: YAML
 :emphasize-lines:2,9,16
 :caption: すべてのセクションのブロック

 - name:Attempt and graceful roll back demo
   block:
     - debug:
         msg:'I execute normally'
     - name: i force a failure
       command: /bin/false
     - debug:
         msg:'I never execute, due to the above task failing, :-('
   rescue:
     - debug:
         msg:'I caught an error'
     - name: i force a failure in middle of recovery! >:-)
       command: /bin/false
     - debug:
         msg:'I also never execute :-('
   always:
     - debug:
         msg:"This always executes"


``rescue`` セクションが実行されたエラーがあると、``block`` のタスクは通常どおり実行されます。
以前のエラーからの復旧に必要な作業と併用してください。
``always`` セクションは、``block`` セクションおよび ``rescue`` セクションで前にエラーが発生したかどうかに関わらず実行されます。
``rescue`` セクションが正常に完了した場合は、エラーステータスが「消去」されるため (報告はされない)、プレイが続行されることに注意してください。
これは、``max_fail_percentage`` 設定または ``any_errors_fatal`` 設定を発生させませんが、Playbook の統計には表示されることを意味します。

別の例として、エラーが発生した後にハンドラーを実行する方法があります。

.. code-block:: YAML
 :emphasize-lines: 6,10
 :caption: Block run handlers in error handling


  tasks:
    - name: Attempt and graceful roll back demo
      block:
        - debug:
            msg: 'I execute normally'
          changed_when: yes
          notify: run me even after an error
        - command: /bin/false
      rescue:
        - name: make sure all handlers run
          meta: flush_handlers
  handlers:
     - name: run me even after an error
       debug:
         msg: 'This handler runs even on error'


バージョン 2.1 における新機能

また、Ansible は、ブロックの ``rescue`` 部分にタスクの変数をいくつか提供します。

ansible_failed_task
    「failed」を返してレスキューを発生させたタスク。たとえば、名前を取得するには、``ansible_failed_task.name`` を使用します。

ansible_failed_result
    rescue を発生させた、失敗したタスクの戻り値。これは、``register`` キーワードでこの変数を使用するのと同じです。

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
