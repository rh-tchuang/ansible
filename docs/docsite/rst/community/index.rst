.. _ansible_community_guide:

***********************
Ansible コミュニティーガイド
***********************

Ansible コミュニティーガイドにようこそ!

本ガイドの目的は、Ansible コミュニティーに貢献する際に必要な知識をすべて説明することです。あらゆる種類の貢献が、Ansible の継続的な成功に必要なものであり、歓迎されます。

このページでは、本セクションにたどり着いたユーザーにとって最も一般的な状況や質問の概要を説明します。従来の目次形式をご希望のユーザー向けに、ページの一番下に目次が用意されています。


はじめに
===============

* このコミュニティーに参加して間もないです。Ansible の :ref:`code_of_conduct` はどこで確認できますか。
* Ansible に貢献する際に何に同意しているのか知りたいのです。Ansible には :ref:`contributor_license_agreement` がありますか。
* 貢献したいのですが、方法がわかりません。:ref:`簡単に貢献する方法 <how_can_i_help>` はありますか。
* 他の Ansible ユーザーと話をしてみたいです。`私が参加できる Ansible Meetup <https://www.meetup.com/topics/ansible/>`_ はどのように探せばいいですか。
* 質問があります。:ref:`Ansible のメーリングリストや IRC チャンネル <communication>` で答えを見つけるにはどうすればいいですか。
* Ansible についてもっと知りたいです。どうすればよいでしょうか。

  * `本を読む <https://www.ansible.com/resources/ebooks>`_。
  * `認定を受ける <https://www.ansible.com/products/training-certification>`_。
  * `イベントに参加する <https://www.ansible.com/community/events>`_。
  * `スタートガイドを確認する <https://www.ansible.com/resources/get-started>`_。
  * `ビデオを見る <https://www.ansible.com/resources/videos>`_ (Ansible Automates、AnsibleFest、ウェビナーの録画など)。

* Ansible の新しいバージョンに関する最新情報を知りたいです。`新しいリリースの発表 <https://groups.google.com/forum/#!forum/ansible-announce>`_ はどのように行われますか。
* 最新のリリースを使用したいです。:ref:`どのリリースが最新のリリース <release_schedule>` かを知るにはどうすれば良いですか。

使い慣れてきた頃
============

* Ansible が破損しているように見えます。:ref:`バグを報告 <reporting_bugs>` するにはどうすれば良いですか。
* Ansible が提供していない機能が必要です。:ref:`機能を要求 <request_features>` するにはどうすれば良いですか。
* 特定の機能が必要です。:ref:`Ansible の将来のリリースで予定されている <roadmaps>` ものを確認するにはどうすれば良いですか。
* 特定の Ansible 機能に関心がある、または専門知識があります (VMware、Linode など)。:ref:`ワーキンググループ <working_group_list>` に参加するにはどうすれば良いですか。
* 機能や修正に関する議論に参加したいです。GitHub の問題やプル要求を確認するにはどうすれば良いですか。
* docs.ansible.com でタイポなどの誤りを見つけました。:ref:`ドキュメントを改善 <community_documentation_contributions>` するにはどうすれば良いですか。


Ansible リポジトリーの使用
=============================

* 変更を初めて Ansible でコーディングしたいです。:ref:`Python 開発環境を設定 <environment_setup>` するにはどうしたら良いですか。
* 開発者としてもっと効率的に作業したいです。Ansible 開発をサポートする :ref:`エディター、Linter などのツール <other_tools_and_programs>` はどうやって見つければ良いですか。
* 自分の PR を Ansible のガイドラインに沿ったものにしたいです。:ref:`Ansible でのコーディング <developer_guide>` に関するガイダンスはどこにありますか。
* Ansible のロードマップ、リリース、およびプロジェクトについて詳しく知りたいです。:ref:`開発サイクル <community_development_process>` に関する情報はどこにありますか。
* Ansible を新しい API やその他のリソースに接続したいです。:ref:`関連モジュールのグループに貢献 <developing_modules_in_groups>` するにはどうすれば良いですか。
* プル要求に ``needs_rebase`` というマークが付いています。:ref:`自分の PR をリベース <rebase_guide>` するにはどうすれば良いですか。
* Ansible の古いバージョンを使用していますが、``devel`` ブランチですでに修正されているバグを、私の使用しているバージョンで修正してほしいです。:ref:`バグ修正の PR をバックポート <backport_process>` するにはどうすれば良いですか。
* オープンになっているプル要求でテストに失敗しているものがあります。Ansible の :ref:`テスト (CI) プロセス <developing_testing>` について学ぶにはどうすれば良いですか。
* モジュールメンテナーになるための準備ができました。:ref:`メンテナー向けガイドライン <maintainers>` を教えてください。
* 私が保守しているモジュールが古くなりました。:ref:`モジュールを非推奨 <deprecating_modules>` にするにはどうすれば良いですか。

従来の目次
=============================

コミュニティーガイド全体をお読みになりたい方は、こちらのページを順番にご覧ください。

.. toctree::
   :maxdepth: 2

   code_of_conduct
   how_can_I_help
   reporting_bugs_and_features
   documentation_contributions
   communication
   development_process
   contributor_license_agreement
   triage_process
   other_tools_and_programs
   ../dev_guide/style_guide/index

.. toctree::
   :caption: 貢献者向け各ガイドライン
   :maxdepth: 1

   committer_guidelines
   maintainers
   release_managers
   github_admins
