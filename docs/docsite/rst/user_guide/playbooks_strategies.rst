.. _playbooks_strategies:

Playbook の実行の制御: strategy など
===================================================

デフォルトでは、Ansible は 5 フォークを使用して、任意のホストで次のタスクを開始する前に、プレイの影響を受けるすべてのホストで各タスクを実行します。このデフォルト動作を変更する場合は、異なるストラテジープラグインを使用するか、フォークの数を変更するか、``serial`` などのプレイレベルのキーワードからいずれかを適用します。

.. contents::
   :local:

ストラテジーの選択
--------------------
上記のデフォルトの動作は :ref:`リニアストラテジー<linear_strategy>` です。Ansible は、:ref:`debug ストラテジー<debug_strategy>` (:ref:`playbook_debugger` を参照) および :ref:`free ストラテジー<free_strategy>` 
を含むその他のストラテジーを提供します。

    - hosts: all
      strategy: free
      tasks:
      ...

上記のように各プレイに異なるストラテジーを選択するか、``defaults`` stanza の ``ansible.cfg`` で優先されるストラテジーをグローバルに設定できます。

    [defaults]
    strategy = free

すべてのストラテジーは、:ref:`ストラテジープラグイン<strategy_plugins>` として実装されます。仕組みの詳細は、各ストラテジープラグインのドキュメントを参照してください。

フォークの数の設定
---------------------------
利用可能な処理能力があり、さらに多くのフォークを使用する場合は、``ansible.cfg`` で数値を設定できます。

    [defaults]
    forks = 30

または、コマンドライン `ansible-playbook -f 30 my_playbook.yml` で渡します。

キーワードを使用した実行の制御
-----------------------------------
一部のプレイレベル :ref:`keyword<playbook_keywords>` は、プレイの実行にも影響を与えます。最も一般的なのは ``serial`` です。これは、一度に管理するホストの番号、パーセンテージ、または数の一覧を設定します。すべてのストラテジーで ``serial`` を設定すると、Ansible はホストを「バッチ」するように指示し、次の「バッチ」を開始する前に、指定した数またはホストのパーセンテージでプレイを完了します。これは、:ref:`ローリングアップデート<rolling_update_batch_size>` で特に便利です。

実行に影響する次のキーワードは ``throttle`` で、ブロックおよびタスクレベルでも使用できます。このキーワードは、forks 設定または ``serial`` を使用して設定するワーカーの数を最大限に制限します。これは、CPU 集約型またはレート制限 API と対話する可能性のあるタスクを制限するのに役に立ちます。

    tasks:
    - command: /path/to/cpu_intensive_command
      throttle: 1

プレイの実行に影響する他のキーワードには、``ignore_errors``、``ignore_unreachable``、および ``any_errors_fatal`` が含まれます。これらのキーワードはストラテジーではないことに注意してください。これは、プレイレベルのディレクティブまたはオプションです。

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
