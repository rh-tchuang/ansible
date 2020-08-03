.. _playbooks_reuse_includes:

include および import
=======================

.. contents:: トピック

Include とImport
````````````````````

:ref:`playbooks_reuse` で説明されているように、include および import ステートメントは非常に似ていますが、Ansible エクゼキューターエンジンはこれらを非常に異なる方法で処理します。

- ``import*`` ステートメントはすべて、Playbook の解析時に事前処理されます。
- ``include*`` ステートメントはすべて、Playbook の実行中に発生する際に処理されます。

各タイプの使用時にトレードオフが発生する可能性があるドキュメントについては、:ref:`playbooks_reuse` を参照してください。

また、この動作は 2.4 で変更になったことに注意してください。Ansible 2.4 よりも前のバージョンでは、``include`` だけが利用可能で、文脈に応じて動作が異なります。

.. versionadded:: 2.4

Playbook のインポート
```````````````````

マスター Playbook に Playbook を追加できます。例::

    - import_playbook: webservers.yml
    - import_playbook: databases.yml

一覧表示される各 Playbook の play および task は、ここで直接定義されているかのように、リストに記載される順序で実行されます。

2.4 よりも前のバージョンでは、``include`` は、Playbook とタスクの両方で import および include として利用でき、機能していました。


.. versionadded:: 2.4

タスクファイルの追加 (include) およびインポート
``````````````````````````````````

タスクを異なるファイルに分割する方法は、複雑なタスクセットを整理したり、再利用したりする簡単な方法です。タスクファイルには、単に以下のタスクのフラットリストが含まれます。

    # common_tasks.yml
    - name: placeholder foo
      command: /bin/foo
    - name: placeholder bar
      command: /bin/bar

次に、``import_tasks`` または ``include_tasks`` を使用して、メインタスク一覧にあるファイルでタスクを実行できます。

    tasks:
    - import_tasks: common_tasks.yml
    # or
    - include_tasks: common_tasks.yml

import および include に変数を渡すこともできます::

    tasks:
    - import_tasks: wordpress.yml
      vars:
        wp_user: timmy
    - import_tasks: wordpress.yml
      vars:
        wp_user: alice
    - import_tasks: wordpress.yml
      vars:
        wp_user: bob

変数の継承および優先順位に関する詳細は、:ref:`ansible_variable_precedence` を参照してください。

タスクの include および import のステートメントは任意の深さで使用できます。

.. note::
    - 静的および動的は混在させることができますが、Playbook のバグを診断することが困難になる可能性があるため、この方法は推奨されません。
    - import および include に変数を渡す ``key=value`` 構文は非推奨になりました。代わりに YAML ``vars:`` を使用します。

Include および Import も ``handlers:`` セクションで使用できます。たとえば、Apache を再起動する方法を定義する場合は、すべての Playbook に対して一度だけ設定する必要があります。以下のような ``handlers.yml`` を作成する場合があります。

   # more_handlers.yml
   - name: restart apache
     service:
       name: apache
       state: restarted

メインの Playbook ファイルで以下を行います。

   handlers:
   - include_tasks: more_handlers.yml
   # or
   - import_tasks: more_handlers.yml

.. note::
    ハンドラーの制限またはトレードオフについては、:ref:`playbooks_reuse` を必ず参照してください。

通常の、include 以外のタスクおよびハンドラーと組み合わせることができます。

ロールの追加 (include) およびインポート
`````````````````````````````

ロールの追加およびインポートに関する詳細は、:ref:`playbooks_reuse_roles` を参照してください。

.. seealso::

   :ref:`yaml_syntax`
       YAML 構文について
   :ref:`working_with_playbooks`
       基本的な Playbook 言語機能を確認します。
   :ref:`playbooks_best_practices`
       実際の Playbook の管理に関するさまざまなヒント
   :ref:`playbooks_variables`
       Playbook の変数の詳細
   :ref:`playbooks_conditionals`
       Playbook の条件
   :ref:`playbooks_loops`
       Playbook のループ
   :ref:`all_modules`
       利用可能なモジュールについて
   :ref:`developing_modules`
       独自のモジュールを作成して Ansible を拡張する方法について
   `GitHub Ansible examples <https://github.com/ansible/ansible-examples>`_
       Github プロジェクトソースにあるすべての Playbook ファイル
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
