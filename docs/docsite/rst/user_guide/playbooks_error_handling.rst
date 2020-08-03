Playbook でのエラー処理
===========================

.. contents:: トピック

Ansible には通常、コマンドとモジュールの戻りコードを確認するためのデフォルトがあり、フェイルファーストを行います。
指定がない限りは、エラーを処理する必要があります。

0 とは異なるコマンドが返されることがありますが、エラーではありません。 コマンドが、
リモートシステムを「変更した」ことを常に報告する必要がない場合があります。 本セクションでは、
特定のタスクの Ansible のデフォルトの動作を変更して、
出力とエラー処理の動作が希望どおりになるようにする方法を説明します。

.. _ignoring_failed_commands:

失敗したコマンドの無視
````````````````````````

通常、Playbook はタスクが失敗したホストでこれ以上のステップの実行を停止します。
ただし、場合によっては、次に進みます。 これを行うには、以下のようなタスクを作成します。

    - name: this will not be counted as a failure
      command: /bin/false
      ignore_errors: yes

上記のシステムは、特定のタスクの障害の戻り値のみを管理することに注意してください。
したがって、未定義の変数が使用されているか、構文エラーが発生した場合は、ユーザーがアドレスを指定することが必要になるエラーが出力されます。
接続または実行の問題の失敗を防ぐ訳ではないことに注意してください。
この機能は、タスクを実行でき、「faileded」の値を返す必要がある場合にのみ機能します。

.. _resetting_unreachable:

到達できないホストのリセット
```````````````````````````

.. versionadded:: 2.2

接続の失敗により、ホストは「UNREACHABLE」として設定され、実行のアクティブなホストの一覧から削除されます。
この問題から回復するには、`meta: clear_host_errors` を使用して、現在フラグが付けられたホストをすべて再アクティベートできるため、
後続のタスクではそれを再び試行できます。


.. _handlers_and_failure:

ハンドラーおよび失敗
````````````````````

ホストでタスクが失敗すると、
以前に通知されたハンドラーはそのホストでは *実行されません*。これにより、
無関係な障害により、ホストが予期しない状態になる可能性があります。たとえば、タスクは構成ファイルを更新し、
ハンドラーにサービスを再起動するよう通知することができます。同じプレイで後でタスクが失敗した場合は、
構成を変更しても
サービスは再開しません。

この動作を変更するには、``--force-handlers`` コマンドラインオプションを使用するか、
または、プレイに ``force_handlers:True`` を追加するか、ansible.cfg に
``force_handlers = True`` を追加します。ハンドラーが強制されると、そのホストでタスクが失敗した場合でも、
通知されたときにハンドラーが強制されます。ホストが到達不能になるなど、
特定のエラーによりハンドラーが実行できなくなる可能性があることに注意してください。

.. _controlling_what_defines_failure:

定義の失敗の制御
````````````````````````````````

Ansible を使用すると、``failed_when`` 条件を使用して、各タスクに「失敗」の意味を定義できます。Ansible のすべての条件と同様、複数の ``failed_when`` 条件の一覧は暗黙的な ``and`` で結合され、*all* 条件を満たす場合にのみタスクは失敗します。条件のいずれかを満たすときに障害を発生させる場合は、明示的な ``or`` 演算子で条件を文字列に定義する必要があります。

コマンドの出力で単語またはフレーズを検索して、障害の有無を確認できます。

    - name:Fail task when the command error output prints FAILED
      command: /usr/bin/example-command -x -y -z
      register: command_result
      failed_when: "'FAILED' in command_result.stderr"

または、戻りコードに基いて確認できます。

    - name:Fail task when both files are identical
      raw: diff foo/file1 bar/file2
      register: diff_cmd
      failed_when: diff_cmd.rc == 0 or diff_cmd.rc >= 2

以前のバージョンの Ansible では、これは以下のように実行できます。

    - name: this command prints FAILED when it fails
      command: /usr/bin/example-command -x -y -z
      register: command_result
      ignore_errors:True

    - name: fail the play if the previous command did not succeed
      fail:
        msg: "the command failed"
      when: "'FAILED' in command_result.stderr"

障害のために複数の条件を組み合わせることもできます。このタスクは、両方の条件が true の場合に失敗します。

    - name:Check if a file exists in temp and fail task if it does
      command: ls /tmp/this_should_not_be_here
      register: result
      failed_when:
        - result.rc == 0
        - '"No such" not in result.stdout'

条件が満たされる場合にのみタスクが失敗する場合は、``failed_when`` 定義を以下のように変更します::

      failed_when: result.rc == 0 or "No such" not in result.stdout

不要な条件が多数ある場合は、``>`` を使用して、これを複数行の yaml 値に分割できます。


    - name: example of many failed_when conditions with OR
      shell: "./myBinary"
      register: ret
      failed_when: >
        ("No such file or directory" in ret.stdout) or
        (ret.stderr != '') or
        (ret.rc == 10)

.. _override_the_changed_result:

変更した結果の上書き
`````````````````````````````

シェル、コマンド、またはその他のモジュールが実行すると、
通常、マシンの状態に影響を与えたと考えるかどうかに基づいて、「変更された」ステータスを報告します。

場合によっては、戻りコードまたは出力に基づいて、
変更が加えられなかったことがわかり、「変更された」結果を上書きして、
レポート出力に表示されないようにするか、
ハンドラーを起動させないようにします。

    tasks:

      - shell: /usr/bin/billybass --mode="take me to the river"
        register: bass_result
        changed_when: "bass_result.rc != 2"

      # this will never report 'changed' status
      - shell: wall 'beep'
        changed_when: False

複数の条件を組み合わせて「変更」の結果を上書きすることもできます。

    - command: /bin/fake_command
      register: result
      ignore_errors: True
      changed_when:
        - '"ERROR" in result.stderr'
        - result.rc == 2

プレイの中止
`````````````````

ホストの残りのタスクを省略するだけでなく、障害時にプレイ全体を中止することが望ましい場合があります。

``any_errors_fatal`` オプションはプレイを終了し、その後のプレイが実行しないようにします。エラーが発生した場合は、現在のバッチのすべてのホストで致命的なタスクを終了し、その後にプレイの実行が停止します。``any_errors_fatal`` はプレイまたはブロックのレベルで設定できます。

     - hosts: somehosts
       any_errors_fatal: true
       roles:
         - myrole

     - hosts: somehosts
       tasks:
         - block:
             - include_tasks: mytasks.yml
           any_errors_fatal: true

より粒度の細かい制御では、``max_fail_percentage`` を使用して、特定の割合のホストが失敗した後に実行を中止できます。

ブロックの使用
````````````

単一タスク (ループを除く) に適用できるほとんどのタスクは :ref:`playbooks_blocks` レベルで適用できるため、タスクに共通するデータまたはディレクティブの設定がより簡単になります。
また、ブロックには、ほとんどのプログラミング言語で例外を処理するのと同じような方法でエラーを処理する機能が導入されています。
ブロックは、タスクの「faileded」ステータスのみを処理します。問題のあるタスク定義または到達不可能なホストは、「復旧可能な可能」エラーではありません。

    tasks:
    - name:Handle the error
      block:
        - debug:
            msg:'I execute normally'
        - name: i force a failure
          command: /bin/false
        - debug:
            msg:'I never execute, due to the above task failing, :-('
      rescue:
        - debug:
            msg:'I caught an error, can do stuff here to fix it, :-)'

これにより、その実行には含まれない ``ブロック`` タスクの失敗ステータスが「取り消され」、成功したかのように再生が続行します。
その他の例は、「:ref:`block_error_handling`」を参照してください。

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
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
