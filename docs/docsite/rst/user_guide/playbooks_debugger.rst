.. _playbook_debugger:

***************
Debugging tasks
***************

Ansible offers a task debugger so you can try to fix errors during execution instead of fixing them in the playbook and then running it again. You have access to all of the features of the debugger in the context of the task. You can check or set the value of variables, update module arguments, and re-run the task with the new variables and arguments. The debugger lets you resolve the cause of the failure and continue with playbook execution.

.. contents::
   :local:

Invoking the debugger
=====================

There are multiple ways to invoke the debugger.

Using the debugger keyword
--------------------------

.. versionadded:: 2.5

The ``debugger`` keyword can be used on any block where you provide a ``name`` attribute, such as a play, role, block or task. The ``debugger`` keyword accepts five values:

.. table::
   :class: documentation-table

   ========================= ======================================================
   Value                     Result
   ========================= ======================================================
   always                    Always invoke the debugger, regardless of the outcome

   never                     Never invoke the debugger, regardless of the outcome

   on_failed                 Only invoke the debugger if a task fails

   on_unreachable            Only invoke the debugger if the a host was unreachable

   on_skipped                Only invoke the debugger if the task is skipped

When you use the ``debugger`` keyword, the setting you use overrides any global configuration to enable or disable the debugger. If you define ``debugger`` at two different levels, for example in a role and in a task, the more specific definition wins: the definition on a task overrides the definition on a block, which overrides the definition on a role or play.

Here are examples of invoking the debugger with the ``debugger`` keyword::

    # on a task
    - name: Execute a command
      command: false
      debugger: on_failed

    # on a play
    - name: My play
      hosts: all
      debugger: on_skipped
      tasks:
        - name: Execute a command
          command: true
          when: False

In this example, the task will open the debugger when it fails, because the task-level definition overrides the play-level definition::

    - name: Play
      hosts: all
      debugger: never
      tasks:
        - name: Execute a command
          command: false
          debugger: on_failed

In configuration or an environment variable
-------------------------------------------

.. versionadded:: 2.5

You can turn the task debugger on or off globally with a setting in ansible.cfg or with an environment variable. The only options are ``True`` or ``False``. If you set the configuration option or environment variable to ``True``, Ansible runs the debugger on failed tasks by default.

To invoke task debugger from ansible.cfg::

    [defaults]
    enable_task_debugger = True

To use an an environment variable to invoke the task debugger::

    ANSIBLE_ENABLE_TASK_DEBUGGER=True ansible-playbook -i hosts site.yml

When you invoke the debugger using this method, any failed task will invoke the debugger, unless it is explicitly disabled for that role, play, block, or task. If you need more granular control what conditions trigger the debugger, use the ``debugger`` keyword.

As a strategy
-------------

.. note::
     This is a backwards compatible method, to match Ansible versions before 2.5,
     and may be removed in a future release

To use the ``debug`` strategy, change the ``strategy`` attribute like this::

    - hosts: test
      strategy: debug
      tasks:
      ...

You can also set the strategy to ``debug`` with the environment variable ``ANSIBLE_STRATEGY=debug``, or by modifying ``ansible.cfg``::

    [defaults]
    strategy = debug


Using the debugger
==================

Once you invoke the debugger, you can use the seven :ref:`available_commands` to work through the error Ansible encountered. For example, if you run the playbook below, Ansible invokes the debugger because the variable *wrong_var* is undefined::

    - hosts: test
      debugger: on_failed
      gather_facts: no
      vars:
        var1: value1
      tasks:
        - name: wrong variable
          ping: data={{ wrong_var }}

From the debug prompt, you can change the module arguments and run the task again.

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

With correctly defined variables, the task runs successfully.

.. _available_commands:

Available debug commands
========================

You can use these seven commands at the debug prompt:

.. _pprint_command:

p(print) *task/task_vars/host/result*
-------------------------------------

Print values used to execute a module::

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
    {'_ansible_no_log': False,
     'changed': False,
     u'failed': True,
     ...
     u'msg': u"No package matching 'not_exist' is available"}

.. _update_args_command:

task.args[*key*] = *value*
--------------------------

Update a module argument. This sample playbook has an invalid package name::

    - hosts: test
      strategy: debug
      gather_facts: yes
      vars:
        pkg_name: not_exist
      tasks:
        - name: install package
          apt: name={{ pkg_name }}

When you run the playbook, the invalid package name triggers an error, and Ansible invokes the debugger. You can fix the package name by viewing, then updating the module argument::

    [192.0.2.10] TASK: install package (debug)> p task.args
    {u'name': u'{{ pkg_name }}'}
    [192.0.2.10] TASK: install package (debug)> task.args['name'] = 'bash'
    [192.0.2.10] TASK: install package (debug)> p task.args
    {u'name': 'bash'}
    [192.0.2.10] TASK: install package (debug)> redo

When the module argument is correct, use ``redo`` to run the task again with new args.

.. _update_vars_command:

task_vars[*key*] = *value*
--------------------------

Update ``task_vars``. You could fix the same playbook above by viewing, then updating the task variables instead of the module args::

    [192.0.2.10] TASK: install package (debug)> p task_vars['pkg_name']
    u'not_exist'
    [192.0.2.10] TASK: install package (debug)> task_vars['pkg_name'] = 'bash'
    [192.0.2.10] TASK: install package (debug)> p task_vars['pkg_name']
    'bash'
    [192.0.2.10] TASK: install package (debug)> update_task
    [192.0.2.10] TASK: install package (debug)> redo

When you update task variables, you must use ``update_task`` to load the new variables before using ``redo`` to run the task again.

.. note::
    In 2.5 this was updated from ``vars`` to ``task_vars`` to avoid conflicts with the ``vars()`` python function.

.. _update_task_command:

u(pdate_task)
-------------

.. versionadded:: 2.8

Re-create the task from the original task data structure and templates with updated task variables. See the entry :ref:`update_vars_command` for an example of use.

.. _redo_command:

r(edo)
------

Run the task again.

.. _continue_command:

c(ontinue)
----------

Continue executing.

.. _quit_command:

q(uit)
------

Quit the debugger. The playbook execution is aborted.

Debugging and the free strategy
===============================

If you use the debugger with the ``free`` strategy, Ansible will not queue or execute any further tasks while the debugger is active. Additionally, using ``redo`` on a task to schedule it for re-execution may cause the rescheduled task to execute after subsequent tasks listed in your playbook.


.. seealso::

   :ref:`playbooks_intro`
       An introduction to playbooks
   `User Mailing List <https://groups.google.com/group/ansible-devel>`_
       Have a question?  Stop by the google group!
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
