.. _developing_testing:

***************
Ansible のテスト
***************

.. contents:: トピック
   :local:


Ansible への貢献をテストする理由
====================================

開発者にとって、最も価値のあることの 1 つが、GitHub の問題を確認バグ修正を手伝うことです。バグ修正は、ほとんど常に、機能開発よりも優先されるためです。 開発者ではなくても、バグの修正や機能のプル要求のテストを手伝うことは非常に価値のあることです。

Ansible ユーザーは、Playbook とロールの作成方法を理解していれば、自身が作成した作業をテストできるはずです。 GitHub のプル要求は、バグの動作を示すさまざまなテスト (Shippable など) を自動的に実行します。 ただし、貢献者は、自動化された GitHub チェック以外でも自身の作業をテストし、その証拠を PR で示すと、その作業がレビューされてマージされる可能性が高くなります。

Ansible のテスト方法、貢献をローカルでテストする方法、およびテスト機能を拡張する方法を説明します。



テストの種類
==============

テストは、大きく分けて以下のように分類されます。

:compile:
  * :ref:`testing_compile`
  * さまざまな Python バージョンに対して python コードのテスト
:sanity:
  * :ref:`testing_sanity`
  * 健全性テストは、静的なコード分析の実行に使用されるスクリプトとツールで構成されています。
  * これらのテストの主な目的は、Ansible コーディングの標準と要件を実施することです。
:integration:
  * :ref:`testing_integration`
  * モジュールおよび Ansible コア機能の機能テスト
:units:
  * :ref:`testing_units`
  * コードベースの個々の部分に対して直接テストを行います。


開発者にとって、最も価値のあることの 1 つが、
GitHub の問題一覧を確認してバグ修正を手伝うことです。 ほとんどの場合、
機能開発よりもバグ修正が優先されます。

開発者ではなくても、
バグの修正や機能のプル要求のテストを手伝うことは非常に価値のあることです。 Ansible ユーザーが Playbook やロールの書き方を熟知していれば統合テストを追加できるため、
バグが実際に動かしている様子を示す統合テストが付いた GitHub プル要求も、
大きな助けになるでしょう。


GitHub および Shippable でのテスト
=================================


組織
------------

プル要求 (PR: Pull Requests) が作成されると、継続的インテグレーション (CI) ツールである Shippable を使用してテストが行われます。結果はすべての PR の最後に表示されます。

Saltppable がエラーを検出し、それが PR で変更されたファイルにリンクされると、関連する行が GitHub のコメントとして追加されます。例::

   The test `ansible-test sanity --test pep8` failed with the following errors:

   lib/ansible/modules/network/foo/bar.py:509:17: E265 block comment should start with '# '

   The test `ansible-test sanity --test validate-modules` failed with the following errors:
   lib/ansible/modules/network/foo/bar.py:0:0: E307 version_added should be 2.4.Currently 2.3
   lib/ansible/modules/network/foo/bar.py:0:0: E316 ANSIBLE_METADATA.metadata_version: required key not provided @ data['metadata_version'].Got None

上記の例では、``--test pep8`` および ``--test validate-modules`` が問題を特定していることが分かります。このコマンドを使用すれば、変更した内容を GitHub にプッシュしたり、Shippable を待たなくても、ローカルで同じテストを実行して問題が修正されたことを確認できます。

Ansible がまだ利用できるようになっていない場合は、ローカルでチェックアウトを実行してください。

  source hacking/env-setup

次に、GitHub コメントで説明するテストを実行します。

  ansible-test sanity --test pep8
  ansible-test sanity --test validate-modules

GitHub のコメントに何が失敗したかが書かれていない場合は、PR の末尾にある「checks have failed」というメッセージの下にある「Details」ボタンをクリックして結果を確認することができます。

失敗した CI ジョブの再実行
--------------------------

時折、変更とは関係のない理由で PR が失敗することがあります。これには、以下のような理由が考えられます。

* yum や git リポジトリーなどの外部リソースにアクセスする際に一時的に問題が発生した場合。
* テストを実行するための仮想マシンを作成するタイムアウト。

いずれかの問題が発生しているようであれば、以下の方法で Shippable テストを再実行できます。

* PR を閉じて再度開く。
* PR に何らかの変更を加えて GitHub にプッシュする。

問題が解決しない場合は、Freenode IRC の ``#ansible-devel`` にお問い合わせください。


PR をテストする方法
================

理想的には、コードが機能することを証明するテストを追加することが推奨されます。特に、ユーザーが様々なプラットフォームにアクセスできない場合、または API や Web サービスを使用している場合は、これが必ずしも可能ではなく、テストが必ずしも包括的ではありません。このような場合は、シミュレーションされたインターフェースに対して実行される自動化よりも、実際の機器に対するライブテストの方が有益かもしれません。いずれにせよ、最初の段階でも常に手動でテストする必要があります。

Ansible の動作を熟知していれば、Ansible のテストを手伝うことは非常に簡単です。

設定: プル要求のチェック
----------------------------------

これは、以下の方法で実行できます。

* Ansible のチェックアウト
* メインブランチからのテストブランチの作成
* GitHub の問題のマージ
* テスト
* GitHub に特定の問題についてのコメント

以下に、実行する方法を説明します。

.. warning::
   GitHub のプル要求から送られてきたソースコードをテストすることにはリスクが伴います。
   送られてきたソースコードには、間違いや悪意のあるコードが含まれていて、システムに影響を及ぼす可能性があるからです。すべてのテストは、
   仮想マシン上で行うことが推奨されます。クラウドインスタンスでもローカルでもかまいません。 このため、Vagrant や Docker を好んで使用するユーザーもいますが、
   これは任意です。また、その OS のバージョンに固有の機能 (apt、yum など) もいくつかあるため、
   Linux などの様々なフレーバーが使用されている仮想マシンを用意しておくと便利です。


作業用に新しい領域を作成します::


   git clone https://github.com/ansible/ansible.git ansible-pr-testing
   cd ansible-pr-testing

次に、テストするプル要求を見つけ、
その上部にあるソースと宛先のリポジトリーを記述した行を書き留めます。以下のようになります。

   Someuser wants to merge 1 commit into ansible:devel from someuser:feature_branch_name

.. note:: ``ansible:devel`` テストのみ

   他のブランチへのプル要求は使用できないため、PR 要求のターゲットは ``ansible:devel`` にすることが重要です。ドットリリースは、Ansible のスタッフが入念に選択しています。

末尾の username とブランチは重要な部分になります。以下のように git コマンドに変換されます。

   git checkout -b testing_PRXXXX devel
   git pull https://github.com/someuser/ansible.git feature_branch_name

最初のコマンドは、``testing_PRXXXX`` という名前の新しいブランチを作成し、切り替えます。XXXX は、プル要求に関連付けられる実際の問題 (issue) の番号です (1234 など)。このブランチは、``devel`` ブランチに基づいています。2 つ目のコマンドは、users 機能ブランチから、新たに作成されたブランチに新規コードをプルします。

.. note::
   GitHub ユーザーインターフェースで、プル要求が正常にマージされないと示された場合は、マージの競合を解決しなければならないため、git およびコーディングにあまり精通していない場合は、続行しないことが推奨されます。これは、元のプル要求の投稿者の責任です。

.. note::
   一部のユーザーは機能ブランチを作成しないため、``devel`` のバージョンに関連性のないコミットが複数ある場合に、問題が発生する可能性があります。ソースが ``someuser:devel`` のように表示される場合は、プル要求に記載されているコミットが 1 つだけであることを確認してください。

Ansible のソースには、
Ansible の開発者が頻繁に使用するフルインストールを必要とせず、ソースから直接 Ansible を使えるようにするスクリプトが含まれています。

ソースを作成するだけ (Linux/Unix の用語を使用するために) で、すぐに使い始めることができます。

   source ./hacking/env-setup

このスクリプトは、``PYTHONPATH`` 環境変数を変更します (他にもいくつかあります)。
これは、シェルセッションが開いている間は一時的に設定されます。

プル要求のテスト
------------------------

この時点でテストを開始する準備が整いました。

何をテストするかのアイデアをいくつか挙げてみましょう。

* 例題を含むテスト Playbook を作成し、それらが正しく機能するかどうかを確認します。
* Python のバックトレースが返されているかどうかをテストします (これはバグです)。
* 異なるオペレーティングシステムで、または異なるバージョンのライブラリーに対してテストします。


潜在的な問題があれば、プル要求にコメントを追加する必要があります (機能が正常に動作する場合もコメントしてもかまいません)。忘れずに ``ansible --version`` の出力を転載してください。

例:

   Works for me!Tested on `Ansible 2.3.0`. I verified this on CentOS 6.5 and also Ubuntu 14.04.

PR が問題を解決しない場合や、ユニット/統合テストでエラーが発生した場合には、代わりにその出力を転載してください。

   | This doesn't work for me.
   |
   | When I ran this Ubuntu 16.04 it failed with the following:
   |
   |   \```
   |   some output
   |   StackTrace
   |   some other output
   |   \```

オンラインのコードカバレージ
````````````````````

「`オンラインのコードカバレージレポート <https://codecov.io/gh/ansible/ansible>`_」は、
Ansible のテストの改善点を特定するのに適しています。 赤い色を追ってレポートを掘り下げていけば、
テストが存在しないファイルを調べることができます。 コードがどのように動作するかを明確に示す統合テストとユニットテストの両方を追加し、
重要な Ansible 機能を検証し、
テストがない領域のテストカバレージを高めることは、
Ansible の改善に役立つ有益な方法です。

コードカバレージレポートは、
新機能の開発が行われる Ansible の ``devel`` ブランチのみを対象としています。 プル要求や新しいコードは codecov.io のカバレージレポートには含まれていないため、
ローカルでのレポートが必要になります。 ほとんどの ``ansible-test`` コマンドで、
コードカバレージを収集することができます。
これは特に拡張先を特定するのに便利です。詳細は、:ref:`testing_running_locally` を参照してください。


テストに関する詳細情報
================================

Ansible テストを改善する詳細な計画を確認したい場合は、
「`Testing Working Group <https://github.com/ansible/community/blob/master/meetings/README.md>`_にご参加ください。
