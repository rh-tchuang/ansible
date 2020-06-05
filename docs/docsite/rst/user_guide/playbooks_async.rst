.. _playbooks_async:

非同期アクションおよびポーリング
================================

デフォルトでは Playbook ブロックのタスクです。
つまり、タスクが各ノードで実行されるまで接続は開いたままになります。 これは常に望ましいとは限りません。
SSH タイムアウトよりも長い操作を実行している可能性もあります。

時間限定のバックグラウンド操作
----------------------------------

バックグラウンドで長時間実行する操作を実行し、後でステータスを確認できます。
たとえば、``long_running_operation`` を、
タイムアウトは 3600 秒 (``-B``) で、
ポーリングなし (``-P``) でバックグラウンドで非同期に実行するには以下のようになります::

    $ ansible all -B 3600 -P 0 -a "/usr/bin/long_running_operation --do-stuff"

後でジョブのステータスを確認する場合は、
``async_status`` モジュールを使用できます。
バックグラウンドで元のジョブの実行時に、返されたジョブ ID を渡します。

    $ ansible web1.example.com -m async_status -a "jid=488359678239.2844"

30 分間実行し、60 秒ごとにステータスをポーリングするには、以下を実行します。

    $ ansible all -B 1800 -P 60 -a "/usr/bin/long_running_operation --do-stuff"

Poll モードはスマートであるため、ポーリングがマシンで開始する前にすべてのジョブが起動します。
ジョブをすべて迅速に開始する場合は、必ず ``--forks`` の値を
大きくしてください。時間制限 (秒単位) が経過した後 (``-B``)、
そのリモートノードのプロセスが終了します。

通常は、
長時間バックグラウンドで実行しているシェルコマンドまたはソフトウェアのアップグレードのみになります。 コピーモジュールのバックグラウンドでは、バックグラウンドファイルの転送は行われません。:ref:`Playbooks <working_with_playbooks>` は、ポーリングもサポートし、簡単な構文を使用します。

ブロックまたはタイムアウトの問題を回避するには、非同期モードを使用してすべてのタスクを一度に実行し、完了するまでポーリングできます。

非同期モードの動作は、`poll` の値によって異なります。

接続のタイムアウトの回避 (poll > 0)
-----------------------------------

``poll`` が正の値の場合、Playbook は完了、失敗、タイムアウトになるまでタスクでブロックされ *続けます*。

この場合、`async` は、接続メソッドのタイムアウトによって制限されるのではなく、このタスクに適用するタイムアウトを明示的に設定します。

タスクを非同期で起動するには、
最大ランタイムと、ステータスをポーリングする頻度を指定します。 デフォルトの poll 値は、
`poll` の値を指定しないと、``DEFAULT_POLL_INTERVAL`` 設定により設定されます。

    ---

    - hosts: all
      remote_user: root

      tasks:

      - name: simulate long running op (15 sec), wait for up to 45 sec, poll every 5 sec
        command: /bin/sleep 15
        async:45
        poll:5

.. note::
   async 時間制限のデフォルトはありません。 「async」キーワードを省略する場合、
   このタスクは、同期的に実行されます。
   これは、Ansible のデフォルトです。

.. note::
  Ansible 2.3 の時点で、async はチェックモードをサポートしていないため、
  タスクをチェックモードで実行すると失敗します。チェックモードでタスクを飛ばす方法は、:ref:`check_mode_dry` 
  を参照してください。


同時タスク: poll = 0
--------------------------

``poll`` が 0 の場合は、Ansible がタスクを開始し、結果を待たずに次のタスクにすぐに移動します。

シーケンスの観点からは、これは非同期プログラミングになります。タスクを同時に実行できるようになりました。

Playbook の実行は、非同期タスクを確認し直すことなく終了します。

非同期タスクは、`async` 値に応じて完了、失敗、またはタイムアウトが行われるまで実行されます。

タスクとの同期ポイントが必要な場合は、これを登録してジョブ ID を取得し、:ref:`async_status <async_status_module>` モジュールを使用してこれを確認します。

ポーリング値を 0 に指定すると、タスクを非同期的に実行できます::

    ---

    - hosts: all
      remote_user: root

      tasks:

      - name: simulate long running op, allow to run for 45 sec, fire and forget
        command: /bin/sleep 15
        async:45
        poll:0

.. note::
   Playbook で、同じリソースに対して別のコマンドを実行することが想定される場合を除いて、
   (yum トランザクションなどの) 排他的ロックが必要となる操作で、
   ポーリング値 0 を指定して、タスクを非同期的に実行しないでください。

.. note::
   ``--forks`` に高い値を使用すると、
   非同期タスクの開始がさらに速くなります。 これにより、ポーリングの効率も高まります。

タスクを非同期的に実行し、後で確認する場合は、
以下のようにタスクを実行できます。

      ---
      # Requires ansible 1.8+
      - name: 'YUM - async task'
        yum:
          name: docker-io
          state: present
        async: 1000
        poll: 0
        register: yum_sleeper

      - name: 'YUM - check on async task'
        async_status:
          jid: "{{ yum_sleeper.ansible_job_id }}"
        register: job_result
        until: job_result.finished
        retries: 30

.. note::
   これにより、``async:`` の値が十分に高くない場合は、
   「check on it later」タスクが失敗します。
   ``async_status:`` が探している一時ステータスファイルが書き込まれていないか、存在しないためです。

同時に実行するタスクの量を制限しながら複数の非同期タスクを実行する場合は、
次のように実行できます。

    #####################
    # main.yml
    #####################
    - name: Run items asynchronously in batch of two items
      vars:
        sleep_durations:
          - 1
          - 2
          - 3
          - 4
          - 5
        durations: "{{ item }}"
      include_tasks: execute_batch.yml
      loop: "{{ sleep_durations | batch(2) | list }}"

    #####################
    # execute_batch.yml
    #####################
    - name: Async sleeping for batched_items
      command: sleep {{ async_item }}
      async: 45
      poll: 0
      loop: "{{ durations }}"
      loop_control:
        loop_var: "async_item"
      register: async_results

    - name: Check sync status
      async_status:
        jid: "{{ async_result_item.ansible_job_id }}"
      loop: "{{ async_results.results }}"
      loop_control:
        loop_var: "async_result_item"
      register: async_poll_results
      until: async_poll_results.finished
      retries: 30

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
