:orphan:

.. _testing_compile:

*************
コンパイルテスト
*************

.. contents:: トピック

概要
========

コンパイルテストでは、サポートされているすべての python バージョンで、ソースファイルの構文が有効かどうかを確認します。

- 2.4 (Ansible 2.3 のみ)
- 2.6
- 2.7
- 3.5
- 3.6

注記: Ansible 2.4 以前では、``ansible-test sanity --test compile`` を使用するサニティーテストの代わりに、コンパイルテストが専用のサブコマンド ``ansible-test compile`` によって提供されていました。

ローカルでのコンパイルテストの実行
=============================

コンパイルテストを実行するには、次のように、コードベース全体でテストを実行できます。

.. code:: shell

    cd /path/to/ansible/source
    source hacking/env-setup
    ansible-test sanity --test compile

1 つのファイルに対して以下を行います。

.. code:: shell

   ansible-test sanity --test compile lineinfile

または、以下を実行して特定の Python バージョンに対して実行します。

.. code:: shell

   ansible-test sanity --test compile --python 2.7 lineinfile

高度な使用方法は、ヘルプを参照してください。

.. code:: shell

   ansible-test sanity --help


依存関係のインストール
=======================

``ansible-test`` にはいくつかの依存関係があります。``コンパイル`` テストでは、デフォルトである ``--local`` を使用してテストを実行することが推奨されます。

依存関係は、``--requirements`` 引数を使用してインストールできます。例:

.. code:: shell

   ansible-test sanity --test compile --requirements lineinfile



要件の詳細は、`test/runner/requirements <https://github.com/ansible/ansible/tree/devel/test/runner/requirements>`_ を参照してください。要件ファイルは、各コマンドの後に名前が付けられます。すべてのコマンドに適用可能な `制約 <https://github.com/ansible/ansible/blob/devel/test/runner/requirements/constraints.txt>`_ も参照してください。


コンパイルテストの拡張
=======================

コンパイルテストに変更が必要な場合は、`Testing Working Group Agenda <https://github.com/ansible/community/blob/master/meetings/README.md>`_ にコメントを追加してください。その内容について話し合うことができます。
