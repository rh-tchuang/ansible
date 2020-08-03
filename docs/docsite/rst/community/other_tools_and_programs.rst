.. _other_tools_and_programs:

########################
その他のツールおよびプログラム
########################

.. contents::
   :local:

Ansible コミュニティーは、Ansible プロジェクトで作業するためにさまざまなツールを使用します。ここでは、これらのツールの中でも特に人気のあるものをいくつか紹介します。

他にも追加すべきツールがあれば、このページの右上にある「Edit on GitHub」をクリックすると、この一覧を更新できます。

***************
人気のあるエディター
***************

Atom
====

GitHub で作成および保守されるオープンソースの無料 GUI テキストエディター。git プロジェクトの変更を追跡したり、GUI からコミットしたり、自分がどのブランチにいるかを確認できます。テーマをカスタマイズして色を変えたり、言語ごとに構文強調表示パッケージをインストールしたりできます。Atom は、Linux、macOS、および Windows にインストールできます。便利な Atom プラグインには以下が含まれます。

* `language-yaml <https://atom.io/packages/language-yaml>`_ - Atom での YAML の強調表示 (組み込み)。
* `linter-js-yaml <https://atom.io/packages/linter-js-yaml>`_ - js-yaml を介して Atom で YAML ファイルを解析。


Emacs
=====

無料でオープンソースのテキストエディターと IDE。オートインデント、構文強調表示、端末シェルでのビルドなどをサポートします。

* `yaml-mode <https://github.com/yoshiki/yaml-mode>`_ - YAML の強調表示と構文のチェック。
* `jinja2-mode <https://github.com/paradoxxxzero/jinja2-mode>`_ - Jinja2 の強調表示と構文の確認。
* `magit-mode <https://github.com/magit/magit>`_ - Emacs 内での git porcelain (磁器)。


PyCharm
=======

Python ソフトウェア開発向けの完全な IDE (統合開発環境)。これには、YAML 構文強調表示のサポートを含む、Python スクリプトを記述するのに必要なすべてのものと完全なソフトウェアが同梱されています。ロール/Playbook の作成には少し時間がかかりますが、モジュールを作成し、Ansible 用のコードを送信する場合は、非常に便利なツールになります。Ansible エンジンのデバッグに使用できます。


Sublime
=======

クローズドソースのサブスクリプション GUI テキストエディター。テーマを使用して GUI をカスタマイズしたり、言語の強調表示などの改良のためのパッケージをインストールしたりすることができます。Sublime は Linux、macOS、Windows にインストールできます。便利な Sublime プラグインには以下のものがあります。

* `GitGutter <https://packagecontrol.io/packages/GitGutter>`_ - git リポジトリー内のファイルに関する情報を表示します。
* `SideBarEnhancements <https://packagecontrol.io/packages/SideBarEnhancements>`_ - ファイルおよびディレクトリーのサイドバーに対する操作の強化を提供します。
* `Sublime Linter <https://packagecontrol.io/packages/SublimeLinter>`_ - Sublime Text 3 のコードの文法チェックフレームワークです。
* `Pretty YAML <https://packagecontrol.io/packages/Pretty%20YAML>`_ - Sublime Text 2 および 3 の YAML を事前設定します。
* `Yamllint <https://packagecontrol.io/packages/SublimeLinter-contrib-yamllint>`_ - yamllint に関する Sublime ラッパーです。


Visual Studio コード
==================

Microsoft が作成および管理するオープンソースの無料 GUI テキストエディター。便利な Visual Studio Code プラグインには以下が含まれます。


* `Red Hat による YAML サポート <https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml>`_ - Kubernetes と Kedge の構文サポートを組み込んだ yaml-language-server を通じて YAML サポートを提供します。
* `Ansible Syntax Highlighting Extension <https://marketplace.visualstudio.com/items?itemName=haaaad.ansible>`_ - YAML および Jinja2 サポート。
* `Ansible の Visual Studio Code 拡張機能 <https://marketplace.visualstudio.com/items?itemName=vscoss.vscode-ansible>`_ - オートコンプリート、構文強調表示。

vim
===

オープンソースの無料コマンドラインテキストエディター。便利な vim プラグインには以下が含まれます。

* `Ansible vim <https://github.com/pearofducks/ansible-vim>`_ - Ansible 2.x の vim 構文プラグイン。YAML Playbook、Jinja2 テンプレート、および Ansible ホストファイルをサポートします。


*****************
開発ツール
*****************

関連する問題および PR の検索
==============================

既存の問題およびプル要求 (PR) を特定する方法は複数あります。

- `ファイル別の PR` <https://ansible.sivel.net/pr/byfile.html>_ - 個別ファイルによるオープンのプル要求の現在の一覧を表示します。Ansible モジュールのメンテナーにとって不可欠なツールです。
- `jctanner の Ansible ツール<https://github.com/jctanner/ansible-tools>`_ Ansible 開発に役立つヘルパースクリプトのさまざまなコレクション。

.. _validate-playbook-tools:

******************************
Playbook を検証するためのツール
******************************

- `Ansible Lint <https://github.com/ansible/ansible-lint>`_ - Ansible Playbook の公式かつ高度な設定可能なベストプラクティスです。
- `Ansible Review` <https://github.com/willthames/ansible-review>_ - コードレビュー用に設計された Ansible Lint の拡張機能です。
- `Molecule <https://github.com/ansible/molecule>`_ は、Anbile による Ansible のプレイおよびロールのテストフレームワークです。
- `yamllint <https://yamllint.readthedocs.io/en/stable/>`__ は、キーの繰り返しやインデントの問題など、構文の有効性を確認するコマンドラインユーティリティーです。


***********
その他のツール
***********

- `Ansible cmdb <https://github.com/fboender/ansible-cmdb>`_ - Ansible のファクト収集の出力を受け取り、システム設定情報が含まれる静的 HTML 概要ページに変換します。
- `Ansible Inventory Grapher <https://github.com/willthames/ansible-inventory-grapher>`_ - インベントリーの継承階層と、変数がインベントリーで定義されているレベルを視覚的に表示します。
- `Ansible Playbook Grapher <https://github.com/haidaraM/ansible-playbook-grapher>`_ - Ansible Playbook のタスクおよびロールを表すグラフを作成するコマンドラインツールです。
- `Ansible Shell <https://github.com/dominis/ansible-shell>`_ - すべてのモジュールのタブ補完が組み込まれている Ansible 用のインタラクティブシェルです。
- `Ansible Silo <https://github.com/groupon/ansible-silo>`_ - Docker による自己完結型の Ansible 環境です。
- `Ansigenome <https://github.com/nickjj/ansigenome>`_ - Ansible ロールの管理に役立つように設計されたコマンドラインツールです。
- `ARA <https://github.com/openstack/ara>`_ - Ansible Playbook の実行を記録し、コールバックプラグインとして Ansible と統合することにより、記録されたデータをユーザーおよびシステムが利用できる直感的なものにします。
- `Awesome Ansible <https://github.com/jdauphant/awesome-ansible>`_ - Awesome Ansible 共同キュレーションの一覧です。
- `AWX <https://github.com/ansible/awx>`_ - Ansible 上に構築された Web ベースのユーザーインターフェース、REST API、およびタスクエンジンを提供します。AWX は、Red Hat Ansible Automation サブスクリプションに含まれる Red Hat Ansible Tower のアップストリームプロジェクトです。
- `Mitogen for Ansible <https://mitogen.networkgenomics.com/ansible_detailed.html>`_ - `Mitogen <https://github.com/dw/mitogen/>`_ ライブラリーを使用して、より効率的な方法で Ansible Playbook を実行します (実行時間を短縮します)。
- `OpsTools-ansible <https://github.com/centos-opstools/opstools-ansible>`_ - Ansible を使用して、`OpsTools <https://wiki.centos.org/SpecialInterestGroup/OpsTools>`_ のサポートを提供する環境を設定します。中央型ロギングと分析、可用性監視、パフォーマンスの監視などです。
- `TD4A <https://github.com/cidrblock/td4a>`_ - 自動化のテンプレート設計。TD4A は、jinja2 テンプレートの構築とテストを行うための視覚的な設計支援ツールです。これは、yaml 形式のデータを jinja2 テンプレートと組み合わせ、出力をレンダリングします。
