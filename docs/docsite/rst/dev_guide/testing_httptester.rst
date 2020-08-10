:orphan:

**********
httptester
**********

.. contents:: トピック

概要
========

``httptester`` は、:ref:`testing_integration` で必要な特定のリソースをホストするために使用される docker コンテナーです。これにより、(git やパッケージリポジトリーなどの) 外部リソースを必要とする CI テストが回避され、一時的に利用できなくなるとテストが失敗します。

以下の機能を提供する HTTP テストエンドポイント。

* httpbin
* nginx
* SSL
* SNI


ソースファイルは `http-test-container <https://github.com/ansible/http-test-container>`_ リポジトリーにあります。

httptester の拡張
====================

``httptester`` を改善するタイミングがある場合は、重複作業を回避するために、「`Testing Working Group Agenda <https://github.com/ansible/community/blob/master/meetings/README.md>`_」にコメントを追加します。
