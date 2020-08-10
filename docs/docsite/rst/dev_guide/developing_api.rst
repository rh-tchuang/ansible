.. _developing_api:

**********
Python API
**********

.. contents:: トピック

.. note:: この API は、Ansible の内部使用を目的としています。Ansible は、API の古いバージョンと後方互換性を保てなくなる可能性のある API にいつでも変更を加えることができます。このため、Ansible では外部の使用はサポートされません。

API の観点から Ansible を使用する方法は複数あります。  Ansible Python APIを使用してノードを制御したり、
Ansible を拡張してさまざまな Python イベントに応答したり、
プラグインを作成したり、外部データソースからのインベントリデータをプラグインしたりできます。 本ガイドは、
Ansible の実行および Playbook API の基本的な概要および例を提示します。

Python 以外の言語からプログラムで Ansible を使用する場合、イベントを非同期にトリガーする場合、またはアクセス制御とロギングの要求がある場合は、
`Ansible Tower のドキュメント` <https://docs.ansible.com/ansible-tower/>`_ を参照してください。

.. note:: Ansible はプロセスのフォークに依存しているため、この API はスレッドセーフではありません。

.. _python_api_example:

Python API の例
==================

この例は、いくつかのタスクを最小限に実行する方法を示す簡単なデモです::

    #!/usr/bin/env python

    import json
    import shutil
    from ansible.module_utils.common.collections import ImmutableDict
    from ansible.parsing.dataloader import DataLoader
    from ansible.vars.manager import VariableManager
    from ansible.inventory.manager import InventoryManager
    from ansible.playbook.play import Play
    from ansible.executor.task_queue_manager import TaskQueueManager
    from ansible.plugins.callback import CallbackBase
    from ansible import context
    import ansible.constants as C

    class ResultCallback(CallbackBase):
        """A sample callback plugin used for performing an action as results come in

        If you want to collect all results into a single object for processing at
        the end of the execution, look into utilizing the ``json`` callback plugin
        or writing your own custom callback plugin
        """
        def v2_runner_on_ok(self, result, **kwargs):
            """Print a json representation of the result

            This method could store the result in an instance attribute for retrieval later
            """
            host = result._host
            print(json.dumps({host.name: result._result}, indent=4))

    # since the API is constructed for CLI it expects certain options to always be set in the context object
    context.CLIARGS = ImmutableDict(connection='local', module_path=['/to/mymodules'], forks=10, become=None,
                                    become_method=None, become_user=None, check=False, diff=False)

    # initialize needed objects
    loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets
    results_callback = ResultCallback()

    # create inventory, use path to host config file as source or hosts in a comma separated string
    inventory = InventoryManager(loader=loader, sources='localhost,')

    # variable manager takes care of merging all the different sources to give you a unified view of variables available in each context
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # create data structure that represents our play, including tasks, this is basically what our YAML loader does internally.
    play_source =  dict(
            name = "Ansible Play",
            hosts = 'localhost',
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module='shell', args='ls'), register='shell_out'),
                dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
             ]
        )

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
    tqm = None
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  passwords=passwords,
                  stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
              )
        result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structures we use to communicate with them
        if tqm is not None:
            tqm.cleanup()

        # Remove ansible tmpdir
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)


.. note:: Ansibleは、標準出力 (stdout)、標準エラー (stderr)、Ansible ログに直接出力する表示オブジェクトを介して警告とエラーを発行します。

``ansible`` コマンドラインツール (``lib/ansible/cli/``) のソースコードは、
GitHub <https://github.com/ansible/ansible/tree/devel/lib/ansible/cli>`_ で利用できます。

.. seealso::

   :ref:`developing_inventory`
       動的インベントリー統合の開発
   :ref:`developing_modules_general`
       モジュール開発を始める
   :ref:`developing_plugins`
       プラグインの開発方法
   `開発メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発トピックのメーリングリスト
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC チャットチャンネル
