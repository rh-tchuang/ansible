.. _ansible_documentation:

Ansible ドキュメント
=====================

Ansible について
\`\`\`\`\`\`\`\`\`\`\`\`\`

Ansible は IT 自動化ツールです。 このツールを使用すると、システムの構成、ソフトウェアの展開、より高度なITタスク (継続的なデプロイメントやダウンタイムなしのローリング更新など) のオーケストレーションが可能になります。

Ansible の主な目標は単純かつ使いやすいことです。また、セキュリティーと信頼性を重視し、最小限の可動部品、トランスポートでの OpenSSH の使用 (他のトランスポートおよびプルモードを代替として使用)、プログラムに精通していない人でも監査を可能にする言語も備えています。

簡素化はあらゆる規模の環境に関連しているため、開発者、システム管理者、リリースエンジニア、IT マネージャーなど、あらゆるタイプのビジーユーザー向けに設計されています。Ansible は、わずかなインスタンスしかない小規模のセットアップから、インスタンスが数千にも上るエンタープライズ環境まで、すべての環境を管理するのに適しています。

Ansible は、エージェントを使用しない方法でマシンを管理します。リモートデーモンをアップグレードする方法、
またはデーモンがアンインストールされているためにシステムを管理できない問題は決して発生しません。 OpenSSH は、相互評価が最も行われたオープンソースコンポーネントの 1 つであるため、セキュリティーの危険性は大幅に軽減されます。Ansible は、既存の OS 認証情報に依存してリモートマシンへのアクセスを制御します。必要に応じて、Ansible は、Kerberos、LDAP、およびその他の集中化された認証管理システムと簡単に接続できます。

本ガイドは、本ページの左上にある Ansible のバージョンについて説明します。Red Hat は、複数のバージョンの Ansible とドキュメントを管理しているため、参照しているドキュメントが、使用している Ansible のバージョンのものであることを確認してください。最新の機能については、その機能が追加された Ansible のバージョンを記載しています。

Ansible は、Ansible のメジャーリリースを年に約 3 ~ 4 回リリースします。コアアプリケーションは若干複雑になり、言語の設計および設定の単純性が高まります。ただし、開発および提供されている新しいモジュールとプラグインを取り巻くコミュニティーは非常に迅速に動き、リリースごとに新しいモジュールが多数追加されます。


.. toctree::
   :maxdepth: 2
   :caption: インストール、アップグレード、および設定

   installation_guide/index
   porting_guides/porting_guides

.. toctree::
   :maxdepth: 2
   :caption: Ansible の使用

   user_guide/index

.. toctree::
   :maxdepth: 2
   :caption: Ansible への貢献

   community/index

.. toctree::
   :maxdepth: 2
   :caption: Ansible の拡張

   dev_guide/index

.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Ansible の一般的なシナリオ

   scenario_guides/cloud_guides
   scenario_guides/network_guides
   scenario_guides/virt_guides

.. toctree::
   :maxdepth: 2
   .. toctree:::maxdepth:ネットワークの自動化における Ansible:caption::maxdepth:

   network/index

.. toctree::
   :maxdepth: 2
   :caption: Ansible Galaxy

   galaxy/user_guide.rst
   galaxy/dev_guide.rst


.. toctree::
   :maxdepth: 1
   :caption: 参照 & 付録

   ../modules/modules_by_category
   reference_appendices/playbooks_keywords
   reference_appendices/common_return_values
   reference_appendices/config
   reference_appendices/general_precedence
   reference_appendices/YAMLSyntax
   reference_appendices/python_3_support
   reference_appendices/interpreter_discovery
   reference_appendices/release_and_maintenance
   reference_appendices/test_strategies
   dev_guide/testing/sanity/index
   reference_appendices/faq
   reference_appendices/glossary
   reference_appendices/module_utils
   reference_appendices/special_variables
   reference_appendices/tower
   reference_appendices/logging


.. toctree::
   :maxdepth: 2
   :caption: リリースノート

.. toctree::
   :maxdepth: 2
   :caption: ロードマップ

   roadmap/index.rst
