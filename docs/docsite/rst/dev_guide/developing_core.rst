**********************************
Ansible Core Engine の開発
**********************************

Ansible Core Engine の多くの部分はプラグインであり、
Playbook ディレクティブまたは設定を介して交換できますが、
モジュール化されていないエンジンの部分がまだあります。 本ガイドでは、
これらがどのように連携するかについての洞察を説明します。

.. toctree::
   :maxdepth: 1

   developing_program_flow_modules

.. seealso::

   :ref:`developing_api`
       タスク実行用の Python API について
   :ref:`developing_plugins`
       プラグインの開発について
   `メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発メーリングリスト
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible-devel IRC chat channel
