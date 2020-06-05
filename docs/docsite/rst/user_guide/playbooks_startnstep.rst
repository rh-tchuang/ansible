start および step
======================

ここでは、Playbook を実行する選択肢がいくつかあります。以下のモードは、新規プレイまたはデバッグのテストに非常に便利です。


.. _start_at_task:

Start-at-task
`````````````
特定のタスクで Playbook の実行を開始する場合は、``--start-at-task`` オプションを使用して開始できます。

    ansible-playbook playbook.yml --start-at-task="install packages"

上記は、「install packages」という名前のタスクで Playbook の実行を開始します。


.. _step:

手順
````

Playbook は、``--step`` を使用して対話形式で実行することもできます。

    ansible-playbook playbook.yml --step

これにより、ansible が各タスクで停止し、そのタスクを実行するかどうかを尋ねます。
「configure ssh」という名前のタスクがあるとします。Playbook の実行が停止し、次のように尋ねられます。

    Perform task: configure ssh (y/n/c):

「y」と答えるとタスクが実行し、「n」と答えるとタスクをスキップし、
「c」と答えると残りのタスクがすべて実行します。

