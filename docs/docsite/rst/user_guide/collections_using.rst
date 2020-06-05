
.. _collections:

*****************
コレクションの使用
*****************

コレクションは、Playbook、ロール、モジュール、およびプラグインを含むことができる Ansible コンテンツのディストリビューション形式です。
`Ansible Galaxy <https://galaxy.ansible.com>`_ を使用してコレクションをインストールして使用できます。

.. contents::
   :local:
   :depth: 2

.. _collections_installing:

コレクションのインストール
======================


``ansible-galaxy`` を使用したコレクションのインストール
----------------------------------------------

.. include:: ../shared_snippets/installing_collections.txt

.. _collections_older_version:

古いバージョンのコレクションのインストール
-------------------------------------------

.. include:: ../shared_snippets/installing_older_collection.txt

.. _collection_requirements_file:

要件ファイルを使用して複数のコレクションのインストール
-----------------------------------------------------

.. include:: ../shared_snippets/installing_multiple_collections.txt

.. _galaxy_server_config:

``ansible-galaxy`` クライアントの設定
------------------------------------------

.. include:: ../shared_snippets/galaxy_server_list.txt


.. _using_collections:

Playbook でのコレクションの使用
===============================

インストールが完了すると、完全修飾コレクション名 (FQCN) でコレクションコンテンツを参照できます。

.. code-block:: yaml

     - hosts: all
       tasks:
         - my_namespace.my_collection.mymodule:
             option1: value

これは、ロールまたはコレクションで配布されるすべてのタイプのプラグインで機能します。

.. code-block:: yaml

     - hosts: all
       tasks:
         - import_role:
             name: my_namespace.my_collection.role1

         - my_namespace.mycollection.mymodule:
             option1: value

         - debug:
             msg: '{{ lookup("my_namespace.my_collection.lookup1", 'param1')| my_namespace.my_collection.filter1 }}'


多くの入力を回避するには、Ansible 2.8 に追加された ``collections`` キーワードを使用できます。


.. code-block:: yaml

     - hosts: all
       collections:
        - my_namespace.my_collection
       tasks:
         - import_role:
             name: role1

         - mymodule:
             option1: value

         - debug:
             msg: '{{ lookup("my_namespace.my_collection.lookup1", 'param1')| my_namespace.my_collection.filter1 }}'

このキーワードは、namespace 以外のプラグイン参照の「検索パス」を作成します。ロールやその他のものはインポートされません。
非アクションプラグインまたはモジュールプラグインには、引き続き FQCN が必要です。

.. seealso::

  :ref:`developing_collections`
      コレクションを開発するか、または変更します。
  :ref:`collections_galaxy_meta`
       コレクションのメタデータ構造を理解します。
  `メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発メーリングリスト
  `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
