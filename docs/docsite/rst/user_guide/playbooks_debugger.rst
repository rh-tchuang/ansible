.. _playbook_debugger:

Playbook デバッガー
=================

.. contents:: トピック

Ansible には、ストラテジープラグインの一部としてデバッガーが含まれています。このデバッガーを使用すると、タスクをデバッグできます。
タスクのコンテキストで、デバッガーのすべての機能にアクセスできます。 たとえば、変数の値を確認または設定したり、モジュール引数を更新したり、新しい変数や引数でタスクを再実行して障害の原因を解決したりできます。

デバッガーを呼び出す方法は複数あります。

デバッガーキーワードの使用
++++++++++++++++++++++++++

.. versionadded:: 2.5

``debugger`` キーワードは、プレイ、ロール、ブロック、タスクなどの ``name`` 属性を指定するブロックで使用できます。

``debugger`` キーワードは、いくつかの値を受け入れます。

always
  結果に関係なく、常にデバッガーを呼び出します。

never
  結果に関係なく、デバッガーを呼び出しません。

on_failed
  タスクが失敗した場合に限りデバッガーを呼び出します。

on_unreachable
  ホストが到達できない場合に限りデバッガーを呼び出します。

on_skipped
  タスクがスキップされた場合に限りデバッガーを呼び出します。

これらのオプションは、デバッガーを有効または無効にするグローバル設定を上書きします。

タスクでは、以下のようになります。
`````````

::

    - name:Execute a command
      command: false
      debugger: on_failed

プレイでは、以下のようになります。
`````````

::

    - name:Play
      hosts: all
      debugger: on_skipped
      tasks:
        - name:Execute a command
          command: true
          when:False

指定したレベルが複数あると、具体的に指定した定義が適用されます。

    - name:Play
      hosts: all
      debugger: never
      tasks:
        - name:Execute a command
          command: false
          debugger: on_failed


設定または環境変数
+++++++++++++++++++++++++++++++++++++

.. versionadded:: 2.5

ansible.cfg では、以下のようになります。

    [defaults]
    enable_task_debugger = True

環境変数では、以下のようになります。

    ANSIBLE_ENABLE_TASK_DEBUGGER=True ansible-playbook -i hosts site.yml

この方法を使用すると、特に明示的に無効になっていない限り、
失敗したタスクまたは到達できないタスクによりデバッガーが呼び出されます。

ストラテジーとして
+++++++++++++

.. note::
     これは、2.5 より前の Ansible バージョンに一致する後方互換性があり、
     今後のリリースで削除される可能性があります。

``デバッグ`` ストラテジーを使用するには、以下のような ``ストラテジー`` 属性を変更します。

    - hosts: test
      strategy: debug
      tasks:
      ...

コードを変更しない場合は、
デバッガーを有効にしたり、以下のように ``ansible.cfg`` を変更したりするために ``ANSIBLE_STRATEGY=debug`` 環境変数を定義できます。

    [defaults]
    strategy = debug


例
++++++++

たとえば、以下のように Playbook を実行します。

    - hosts: test
      debugger: on_failed
      gather_facts: no
      vars:
        var1: value1
      tasks:
        - name: wrong variable
          ping: data={{ wrong_var }}

*wrong_var* 変数が定義されていないため、デバッガーが呼び出されます。

モジュールの引数を変更して、タスクを再実行します。

.. code-block:: none

    PLAY ***************************************************************************

    TASK [wrong variable] **********************************************************
    fatal: [192.0.2.10]: FAILED! => {"failed": true, "msg": "ERROR! 'wrong_var' is undefined"}
    Debugger invoked
    [192.0.2.10] TASK: wrong variable (debug)> p result._result
    {'failed': True,
     'msg': 'The task includes an option with an undefined variable. The error '
            "was: 'wrong_var' is undefined\n"
            '\n'
            'The error appears to have been in '
            "'playbooks/debugger.yml': line 7, "
            'column 7, but may\n'
            'be elsewhere in the file depending on the exact syntax problem.\n'
            '\n'
            'The offending line appears to be:\n'
            '\n'
            '  tasks:\n'
            '    - name: wrong variable\n'
            '      ^ here\n'}
    [192.0.2.10] TASK: wrong variable (debug)> p task.args
    {u'data': u'{{ wrong_var }}'}
    [192.0.2.10] TASK: wrong variable (debug)> task.args['data'] = '{{ var1 }}'
    [192.0.2.10] TASK: wrong variable (debug)> p task.args
    {u'data': '{{ var1 }}'}
    [192.0.2.10] TASK: wrong variable (debug)> redo
    ok: [192.0.2.10]

    PLAY RECAP *********************************************************************
    192.0.2.10               : ok=1    changed=0    unreachable=0    failed=0

今回は、タスクが正常に実行します。

.. _available_commands:

利用可能なコマンド
++++++++++++++++++

.. _pprint_command:

p(print) *task/task_vars/host/result*
`````````````````````````````````````

モジュールの実行に使用される値を出力します。

    [192.0.2.10] TASK: install package (debug)> p task
    TASK: install package
    [192.0.2.10] TASK: install package (debug)> p task.args
    {u'name': u'{{ pkg_name }}'}
    [192.0.2.10] TASK: install package (debug)> p task_vars
    {u'ansible_all_ipv4_addresses': [u'192.0.2.10'],
     u'ansible_architecture': u'x86_64',
     ...
    }
    [192.0.2.10] TASK: install package (debug)> p task_vars['pkg_name']
    u'bash'
    [192.0.2.10] TASK: install package (debug)> p host
    192.0.2.10
    [192.0.2.10] TASK: install package (debug)> p result._result
    {'_ansible_no_log':False,
     'changed':False,
     u'failed':True,
     ...
     u'msg': u"No package matching 'not_exist' is available"}

.. _update_args_command:

task.args[*key*] = *value*
``````````````````````````

モジュールの引数を更新します。

以下のような Playbook を実行すると、

    - hosts: test
      strategy: debug
      gather_facts: yes
      vars:
        pkg_name: not_exist
      tasks:
        - name: install package
          apt: name={{ pkg_name }}

パッケージ名が間違っているためにデバッガーが呼び出されるため、モジュールの引数を修正します。

    [192.0.2.10] TASK: install package (debug)> p task.args
    {u'name': u'{{ pkg_name }}'}
    [192.0.2.10] TASK: install package (debug)> task.args['name'] = 'bash'
    [192.0.2.10] TASK: install package (debug)> p task.args
    {u'name': 'bash'}
    [192.0.2.10] TASK: install package (debug)> redo

次に、新しい引数でタスクを再実行します。

.. _update_vars_command:

task_vars[*key*] = *value*
``````````````````````````

``task_vars`` を更新します。

上記と同じ Playbook を使用しますが、引数ではなく、``task_vars`` を修正します。

    [192.0.2.10] TASK: install package (debug)> p task_vars['pkg_name']
    u'not_exist'
    [192.0.2.10] TASK: install package (debug)> task_vars['pkg_name'] = 'bash'
    [192.0.2.10] TASK: install package (debug)> p task_vars['pkg_name']
    'bash'
    [192.0.2.10] TASK: install package (debug)> update_task
    [192.0.2.10] TASK: install package (debug)> redo

次に、新しい ``task_vars`` でタスクを再実行します。

.. note::
    2.5 では、これは ``vars`` から ``task_vars`` に更新され、python 関数 ``vars()`` と競合しませんでした。

.. _update_task_command:

u(pdate_task)
`````````````

バージョン 2.8 における新機能

このコマンドは、元のタスクのデータ構造および更新された ``task_vars`` が含まれるテンプレートからタスクを再作成します。

使用例は、上記の :ref:`update_vars_command` ドキュメントを参照してください。

.. _redo_command:

r(edo)
``````

タスクを再度実行します。

.. _continue_command:

c(ontinue)
``````````

続行するだけです。

.. _quit_command:

q(uit)
``````

デバッガーを終了します。Playbook の実行は中止します。

無料ストラテジーの使用
++++++++++++++++++++++++++

``空き`` ストラテジーでデバッガーを使用すると、
デバッガーがアクティブである間に、追加のタスクがキューに入ったり、実行したりしなくなります。さらに、タスクで ``redo`` を使用して再実行のスケジュールを設定すると、
Playbook に記載されている後続のタスクの後に再スケジュールされたタスクが実行することがあります。


.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
