.. _working_with_playbooks:

Playbook の使用
======================

Playbook は Ansible の設定、デプロイメント、オーケストレーション言語です。リモートのシステムが実施するポリシー、または一般的な IT プロセスの一連の手順を記述します。

Ansible モジュールがワークショップのツールである場合、Playbook は手順のマニュアルにあり、ホストのインベントリーは実際のマテリアルになります。

基本的なレベルでは、Playbook を使用して、リモートマシンの設定およびデプロイメントを管理できます。 より高度なレベルでは、ローリングアップデートに関連する複数層のロールアウトを分類し、アクションを他のホストに委譲し、途中でモニタリングサーバーやロードバランサーと対話できます。

ここでは多くの情報がありますが、すべてを一度に学習する必要はありません。 小規模な機能を開始し、
必要に応じてより多くの機能を選択できます。

Playbook は人間が判読できるように設計されており、基本的なテキスト言語で開発されます。 Playbook と、
そこに含まれるファイルを整理する方法は複数あり、その方法と、Ansible を最大限に活用する提案を提供します。

Playbook ドキュメントと一緒に、`「Example Playbooks」 <https://github.com/ansible/ansible-examples>`_ を参照してください。 ここでは、ベストプラクティスと、さまざまな概念をまとめて配置する方法を説明しています。

.. toctree::
   :maxdepth: 2

   playbooks_intro
   playbooks_reuse
   playbooks_variables
   playbooks_templating
   playbooks_conditionals
   playbooks_loops
   playbooks_blocks
   playbooks_special_topics
   playbooks_strategies
   playbooks_best_practices
   guide_rolling_upgrade
