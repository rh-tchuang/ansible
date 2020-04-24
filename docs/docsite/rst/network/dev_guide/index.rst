.. \_network\_developer\_guide:

**************************************
ネットワーク自動化のための開発者ガイド
**************************************

Ansible ネットワーク自動化のための開発者ガイドへようこそ

**本書の対象者**

モジュールまたはプラグインを作成して、ネットワークの自動化向けに Ansible を拡張する場合は、本書をご利用ください。本ガイドはネットワークに特化しています。モジュールおよびプラグインの作成、テスト、文書化の方法や、メインの Ansible リポジトリーで受け入れられるモジュールまたはプラグインの前提条件を理解しておく必要があります。 詳細は、:ref:`developer_guide` を参照してください。作業を続行する前に、以下の点を確認してください。

* :ref:`カスタムプラグインまたはモジュールをローカルで追加<developing_locally>` する方法
* :ref:`モジュールの開発が自身のユースケースに適切なアプローチである<module_dev_should_you>` かどうかを確認する方法
* :ref:`Python 開発環境を設定<environment_setup>` する方法
* :ref:`モジュールの記述を開始 <developing_modules_general>` する方法


必要なことを最も適切に説明しているネットワーク開発者タスクを選択してください。

   * :ref:`ネットワークリソースモジュールを開発 <developing_resource_modules>` する
   * :ref:`ネットワーク接続プラグインを開発 <developing_plugins_network>` する
   * :ref:`ネットワークプラットフォーム用のモジュールセットを文書化 <documenting_modules_network>` する

本書をすべて読む場合は、以下の順番でページを表示してください。

.. toctree::
  :maxdepth: 1

  developing\_resource\_modules\_network
  developing\_plugins\_network
  documenting\_modules\_network
