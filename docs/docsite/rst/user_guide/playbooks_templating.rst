.. _playbooks_templating:

テンプレート作成 (Jinja2)
===================

変数セクションですでに参照されているように、Ansible は Jinja2 のテンプレート作成を使用して動的な式を有効にし、変数にアクセスします。
Ansible は利用可能なフィルターおよびテストの数を大幅に拡張し、新しいプラグインタイプ lookup を追加します。

すべてのテンプレートは、タスクが送信され、対象のマシンで実行する前に、Ansible コントローラーで実行されます。これは、ターゲットの要件を最小限にするために行われます (コントローラーでは jinja2 のみが必要)。また、タスクに必要な最小限の情報を渡すことができるため、ターゲットマシンはコントローラーがアクセスできるすべてのデータのコピーを必要としません。

.. contents:: トピック

.. toctree::
   :maxdepth: 2

   playbooks_filters
   playbooks_tests
   playbooks_lookups
   playbooks_python_version

.. _templating_now:

現在の時間を取得
````````````````````

.. versionadded:: 2.8

Jinja2 関数 ``now()`` は、Python datetime オブジェクトまたは現在の時間を表す文字列を取得します。

``now()`` 関数は 2 つの引数をサポートします。

utc
  UTC で現在の時間を取得するには、``True`` を指定します。デフォルトは ``False`` です。

fmt
  フォーマット済みの日時文字列を返すために使用される `strftime <https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior>`_ 
  文字列を受け入れます。


.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_loops`
       Playbook でのループ
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   :ref:`playbooks_best_practices`
       Playbook のベストプラクティス
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
