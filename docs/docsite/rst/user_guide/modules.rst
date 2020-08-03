.. _working_with_modules:

モジュールの使用
====================

.. toctree::
   :maxdepth: 1

   modules_intro
   ../reference_appendices/common_return_values
   modules_support
   ../modules/modules_by_category


Ansible には、
リモートホスト上または :ref:`Playbooks <working_with_playbooks>` を介して直接実行できる多数のモジュール　(「モジュールライブラリー」と呼ばれています) が同梱されています。

ユーザーはモジュールを自作することもできます。このようなモジュールは、
サービス、パッケージ、またはファイルなどのシステムリソースを制御したり、システムコマンドの実行を処理したりできます。


.. seealso::

   :ref:`intro_adhoc`
       /usr/bin/ansible におけるモジュールの使用例
   :ref:`playbooks_intro`
       /usr/bin/ansible-playbook におけるモジュール使用の概要
   :ref:`developing_modules_general`
       独自のモジュールの作成方法
   :ref:`developing_api`
       Python API でモジュールを使用する例
   :ref:`interpreter_discovery`
       ターゲットホストでの適切な Python インタープリターの設定
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
