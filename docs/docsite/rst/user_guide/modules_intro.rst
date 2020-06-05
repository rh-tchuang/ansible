.. _intro_modules:

モジュールの概要
=======================

モジュール (「タスクプラグイン」または「ライブラリープラグイン」とも呼ばれます) は、コマンドラインまたは Playbook タスクで使用可能なコードの個別単位です。Ansible は、通常のリモートターゲットノードで各モジュールを実行し、戻り値を収集します。

コマンドラインからモジュールを実行できます。

    ansible webservers -m service -a "name=httpd state=started"
    ansible webservers -m ping
    ansible webservers -m command -a "/sbin/reboot -t now"

各モジュールは引数の取得をサポートします。 ほとんどすべてのモジュールは、``key=value`` 引数を
スペースで区切って指定します。 一部のモジュールは引数を取らず、
command/shell モジュールは単に実行するコマンドの文字列を取ります。

Playbook から、Ansible モジュールは同じような方法で実行されます。

    - name: reboot the servers
      action: command /sbin/reboot -t now

これは、以下のように短縮できます。

    - name: reboot the servers
      command: /sbin/reboot -t now

もしくは、「complex args」とも呼ばれる YAML 構文を使用して、モジュールに引数を渡します。

    - name: restart webserver
      service:
        name: httpd
        state: restarted

すべてのモジュールは JSON 形式のデータを返します。つまり、モジュールはどのプログラミング言語でも記述できます。モジュールは冪等であるべきで、現在の状態が目的の最終状態と一致することを検出した場合は変更を行わないようにする必要があります。Ansible Playbook で使用すると、モジュールは追加のタスクを実行するように「ハンドラー」に通知する形式で「変更イベント」をトリガーできます。

各モジュールのドキュメントは、コマンドラインで ansible-doc ツールを使用してアクセスできます。

    ansible-doc yum

利用可能なモジュールの一覧は、「:ref:`Module Docs <modules_by_category>`」を参照してください。または、コマンドラインで次のコマンドを実行します。

    ansible-doc -l


.. seealso::

   :ref:`intro_adhoc`
       /usr/bin/ansible におけるモジュールの使用例
   :ref:`working_with_playbooks`
       /usr/bin/ansible-playbook でモジュールを使用する例
   :ref:`developing_modules`
       独自のモジュールの作成方法
   :ref:`developing_api`
       Python API でモジュールを使用する例
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       _#ansible IRC chat channel
