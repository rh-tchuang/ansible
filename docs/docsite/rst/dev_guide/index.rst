.. _developer_guide:

***************
開発者ガイド
***************

Ansible 開発者ガイドにようこそ!

**本ガイドの対象者**

ローカルでカスタムモジュールまたはプラグインを使用して Ansible を拡張する、モジュールまたはプラグインを作成する、既存のモジュールに機能を追加する、またはテストの対象を広げる場合は、このガイドが役立ちます。開発者向けの詳細な情報として、モジュールのテストおよびドキュメント方法と、モジュールまたはプラグインをメインの Ansible リポジトリーで許可するための前提条件を記載しました。

以下の中から、お客様のニーズに最も適したタスクを選んでください。

* ユースケースに対応する方法を探している。

   * :ref:`ローカルにカスタムプラグインまたはモジュール <developing_locally>` を追加したい。
   * :ref:`私のユースケースではモジュールを開発することが適切なアプローチ <module_dev_should_you>` であるかどうかを知りたい。
   * :ref:`コレクションを開発 <developing_collections>` したい。

* 上記の情報を読んで、モジュールを開発したい。

   * コーディングを始める前に何を知っておくべきか。
   * :ref:`Python 開発環境を設定 <environment_setup>` したい。
   * :ref:`モジュールの作成 <developing_modules_general>` を開始したい。
   * 特定のモジュールを作成したい。
      * :ref:`ネットワークモジュール` <developing_modules_network>
      * :ref:`Windows モジュール` <developing_modules_general_windows>
      * :ref:`Amazon モジュール` <AWS_module_development>
      * :ref:`OpenStack モジュール` <OpenStack_module_development>
      * :ref:`oVirt/RHV モジュール` <oVirt_module_development>
      * :ref:`VMware モジュール` <VMware_module_development>
   * Ansible を新製品 (データベース、クラウドプロバイダー、ネットワークプラットフォームなど) と統合する :ref:`一連の関連モジュールを記述 <developing_modules_in_groups>` したい。

* コードを改良したい。

   * :ref:`モジュールコードをデバッグ <debugging>` したい。
   * :ref:`テストを追加 <developing_testing>` したい。
   * :ref:`モジュールを文書化 <module_documenting>` したい。
   * :ref:`ネットワークプラットフォーム用のモジュールセットを文書化 <documenting_modules_network>` したい。
   * :ref:`記述方法が適切で使用可能なモジュールコードの規則とヒント <developing_modules_best_practices>` に従いたい。
   * :ref:`コードが Python 2 および Python 3 で実行することを確認 <developing_python_3>` したい。

* 他の開発プロジェクトで作業したい。

   * :ref:`プラグインを記述 <developing_plugins>` したい。
   * :ref:`インベントリーの新しいソースに Ansible を接続 <developing_inventory>` したい。
   * :ref:`古いモジュールを廃止 <deprecating_modules>` したい。

* Ansible プロジェクトに貢献したい。

  * :ref:`Ansible への貢献方法を理解 <ansible_community_guide>` したい。
  * :ref:`モジュールまたはプラグインを提供 <developing_modules_checklist>` したい。
  * :ref:`Ansible への貢献に関する使用許諾契約を理解 <contributor_license_agreement>` したい。

本ガイドをすべて読む場合は、以下に示す順番でページを表示してください。

.. toctree::
   :maxdepth: 2

   developing_locally
   developing_modules
   developing_modules_general
   developing_modules_checklist
   developing_modules_best_practices
   developing_python_3
   debugging
   developing_modules_documenting
   developing_modules_general_windows
   developing_modules_general_aci
   platforms/aws_guidelines
   platforms/openstack_guidelines
   platforms/ovirt_dev_guide
   platforms/vmware_guidelines
   developing_modules_in_groups
   testing
   module_lifecycle
   developing_plugins
   developing_inventory
   developing_core
   developing_program_flow_modules
   developing_api
   developing_rebasing
   developing_module_utilities
   developing_collections
   collections_galaxy_meta
   overview_architecture
