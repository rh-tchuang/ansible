.. _playbooks_lookups:

lookup
-------

lookup プラグインを使用すると、外部データソースにアクセスできます。すべてのテンプレートと同様、このプラグインは Ansible コントロールマシンで評価されファイルシステムの読み取り、外部データストアおよびサービスへの接続を含めることができます。このデータは、Ansible で標準のテンプレートシステムを使用して利用できるようになります。

.. note::
    - ルックアップは、リモートコンピューターではなく、ローカルコンピューターで行われます。
    - これは、実行したスクリプトのディレクトリーで実行されるローカルタスクではなく、ロールまたはプレイを含むディレクトリーで実行します。
    - wantlist=True を lookup に渡して、Jinja2 テンプレート「for」ループで使用できます。
    - ルックアップは高度な機能です。Ansible プレイの知識を組み込むには、十分な実用的な知識が必要です。

.. warning:: lookup によってはシェルに引数を渡します。リモート/信頼されていないソースから変数を使用する場合には、`|quote` フィルターで、安全に使用できるようにします。

.. contents:: トピック

.. _lookups_and_loops:

lookup および loop
`````````````````

*lookup プラグイン* は、シェルコマンドやキー値ストアなどの外部データソースにクエリーする手段です。

Ansible 2.5 以前は、ほとんどの場合、ルックアップはループの ``with_<lookup>`` 構造で間接的に使用されていました。Ansible バージョン 2.5 以降、lookup は ``loop`` キーワードに入力される Jinja2 式の一部としてより明示的に使用されます。


.. _lookups_and_variables:

lookup および変数
`````````````````````

lookup を使用する 1 つの方法は、変数を設定することです。これらのマクロは、タスク (またはテンプレート) で使用されるたびに評価されます。

    vars:
      motd_value: "{{ lookup('file', '/etc/motd') }}"
tasks:
  - debug:
      msg: "motd value is {{ motd_value }}"
    
詳細と、利用可能な lookup プラグインの完全な一覧は、:ref:`plugins_lookup` を参照してください。

.. seealso::

   :ref:`working_with_playbooks`
       Playbook の概要
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_variables`
       変数の詳細
   :ref:`playbooks_loops`
       Playbook でのループ
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
