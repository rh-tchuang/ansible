:orphan:

.. _testing_sanity:

************
サニティーテスト
************

.. contents:: トピック

サニティーテストは、静的コード分析の実行に使用されるスクリプトおよびツールで構成されています。
これらのテストの主な目的は、Ansible コーディングの仕様および要件を適用することです。

テストは ``ansible-test sanity`` で実行されます。
``--test`` オプションを使用しない限り、利用可能なテストはすべて実行されます。


実行方法
==========

.. code:: shell

   source hacking/env-setup

   # Run all sanity tests
   ansible-test sanity

   # Run all sanity tests against against certain files
   ansible-test sanity lib/ansible/modules/files/template.py

   # Run all tests inside docker (good if you don't have dependencies installed)
   ansible-test sanity --docker default

   # Run validate-modules against a specific file
   ansible-test sanity --test validate-modules lib/ansible/modules/files/template.py

利用可能なテスト
===============

テストは、``ansible-test sanity --list-tests`` で一覧表示できます。

各種テストや特定された問題を解決する方法の詳細は <all_sanity_tests>、「`サニティーテスト <all_sanity_tests>`」の一覧を参照してください。
