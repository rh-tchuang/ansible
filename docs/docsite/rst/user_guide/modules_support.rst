.. _modules_support:

****************************
モジュールのメンテナンスおよびサポート
****************************

.. contents::
  :depth: 2
  :local:

メンテナンス
===========

同梱される各モジュールの保守、機能の追加、バグの修正を行う者が明確になるように、同梱される各モジュールには、保守に関する情報を提供するメタデータが関連付けられています。

コア
----

:ref:`コア保守<core_supported>` モジュールは、Ansible エンジニアリングチームにより保守されます。
これらのモジュールは、Ansible ディストリビューションの基本的な基盤に必須のものです。

ネットワーク
-------

:ref:`ネットワーク保守<network_supported>` モジュールは、Ansible ネットワークチームにより保守されます。追加のネットワークモジュールは、Ansible で保守されない認定済みまたはコミュニティーとして分類されています。


認定済み
---------

`認定 <https://access.redhat.com/articles/3642632>`_ モジュールは Ansible パートナーによって保守されます。

コミュニティー
---------

:ref:`コミュニティー保守<community_supported>` モジュールは、Ansible コミュニティーにより送信および保守されます。 これらのモジュールは Ansible により保守されず、利便性のために組み込まれています。

問題の報告
===============

モジュールにバグが見つかり、最新の安定性または開発バージョンの Ansible を実行していると思われる場合は、まず `Ansible リポジトリーで問題のトラッカー <https://github.com/ansible/ansible/issues>`_ を確認し、問題がすでに報告されているかどうかを確認します。報告されていない場合は報告してください。

バグの報告ではなく質問がある場合は、`ansible-project Google グループ <https://groups.google.com/forum/#%21forum/ansible-project>`_ または Ansible の "#ansible" channel, located on irc.freenode.net. でお問い合わせください。

開発指向のトピックは、`ansible-devel Google group <https://groups.google.com/forum/#%21forum/ansible-devel>`_ または Ansible の #ansible and #ansible-devel channels, located on irc.freenode.net. You should also read the :ref:`コミュニティーガイド<ansible_community_guide>`、:ref:`Ansible のテスト<developing_testing>`、および:ref:`開発者ガイド<developer_guide>` を参照してください。

モジュールは、`Ansible <https://github.com/ansible/ansible/tree/devel/lib/ansible/modules>`_ リポジトリーのサブディレクトリーにある GitHub でホストされます。

注記:Red Hat Ansible Automation 製品サブスクリプションをお持ちの場合は、`Red Hat カスタマーポータル<https:///access.redhat.com/>`_ から標準の問題報告プロセスを実行してください。

サポート
=======

同梱されている Ansible モジュールが Red Hat でどのようにサポートされているかは、
以下の `ナレッジベースの記事<https://access.redhat.com/articles/3166901>`_ と、`Red Hat カスタマーポータル <https://access.redhat.com/>`_ のその他のリソースを参照してください。

.. seealso::

   :ref:`モジュールインデックス<modules_by_category>`
       利用可能なモジュールの完全なリスト
   :ref:`intro_adhoc`
       /usr/bin/ansible におけるモジュールの使用例
   :ref:`working_with_playbooks`
       /usr/bin/ansible-playbook でモジュールを使用する例
   :ref:`developing_modules`
       独自のモジュールの作成方法
   `Ansible 認定モジュールの一覧 <https://access.redhat.com/articles/3642632>`_
       パートナー企業の Ansible 認定モジュールの概要一覧
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
