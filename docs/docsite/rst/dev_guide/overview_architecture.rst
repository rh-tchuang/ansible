********************
Ansible アーキテクチャー
********************

Ansible は、クラウドプロビジョニング、設定管理、アプリケーションのデプロイメント、サービス内オーケストレーション、およびその他の IT のニーズを自動化する非常にシンプルな IT 自動化エンジンです。

Ansible は、リリースされたその日から多層デプロイメント用に設計されており、システムを 1 つずつ管理する代わりに、すべてのシステムがどのように相互に関連しているかを記述することで、IT インフラストラクチャーをモデル化します。

エージェントを使用せず、カスタムセキュリティーインフラストラクチャーを追加しないため、簡単にデプロイメントできます。最も重要なことは、非常に単純な言語 (YAML を Ansible Playbook の形式で使用) を使用しているため、分かりやすい英語に近づける方法で自動化ジョブを記述できます。

本セクションでは、Ansible の動作の概要を簡単に説明します。これにより各ピースがどのように組み合わされているかを確認できます。

.. contents::
   :local:

モジュール
=======

Ansible は、ノードに接続し、「Ansible モジュール」と呼ばれるスクリプトをノードにプッシュすることで機能します。ほとんどのモジュールは、システムの希望の状態を記述するパラメーターを受け入れます。
その後、Ansible はこれらのモジュールを実行して (デフォルトでは SSH 上)、終了すると削除されます。モジュールのライブラリーはどのマシンにも配置でき、サーバー、デーモン、またはデータベースは必要ありません。

:ref:`モジュールは自身で作成 <developing_modules_general>` できますが、その前に、:ref:`作成すべきかどうか <developing_modules>` を検討する必要があります。通常、任意のターミナルプログラム、テキストエディター、およびおそらくバージョン管理システムを使用して、コンテンツへの変更を追跡します。JSON を返すことができる任意の言語 (Ruby、Python、bash など) で特殊なモジュールを作成できます。

モジュールユーティリティー
================

複数のモジュールが同じコードを使用する場合は、Ansible がこの機能をモジュールユーティリティーとして保存し、重複とメンテナンスを最小限に抑えます。たとえば、URL を解析するコードは ``lib/ansible/module_utils/url.py`` です。:ref:`自身でモジュールユーティリティーを作成 <developing_module_utilities>` することもできます。モジュールユーティリティーは Python または PowerShell でのみ記述できます。

プラグイン
=======

:ref:`プラグイン <plugins_lookup>` は Ansible のコア機能を拡張します。モジュールは、ターゲットシステムにおいて個別のプロセス (通常はリモートシステム上にある) で実行されるのに対して、プラグインは ``/usr/bin/ansible`` プロセス内のコントロールノードで実行されます。プラグインは、データの変換、出力のログ出力、インベントリーへの接続など、Ansible のコア機能のオプションおよび拡張機能を提供します。Ansible には、便利なプラグインが多数同梱されています。また、:ref:`自身でプラグイン <developing_plugins>` を簡単に記述することもできます。たとえば、:ref:`インベントリープラグイン <developing_inventory>` を作成して、JSON を返すデータソースに接続できます。プラグインは Python で記述する必要があります。

インベントリー
=========

デフォルトでは、Ansible は、自身が作成したグループにすべての管理マシンを配置するファイル (INI、YAML など) で管理するマシンを表します。

新規マシンを追加するための、追加の SSL 署名サーバーはありません。したがって、NTP または DNS の問題が原因で特定のマシンがリンクされない理由を判断する手間がかかります。

インフラストラクチャーに信頼できる別のソースがある場合は、Ansible もこれに接続できます。Ansible は、EC2、Rackspace、OpenStack などのソースからインベントリー、グループ、および変数情報を取り出すことができます。

プレーンテキストのインベントリーファイルは次のようになります。

    ---
    [webservers]
    www1.example.com
    www2.example.com

    [dbservers]
    db0.example.com
    db1.example.com

インベントリーホストの一覧が作成されると、単純なテキストファイル形式で (「group_vars/」または「host_vars/」という名前のサブディレクトリー内、またはインベントリーファイルに直接) 割り当てることができます。

または、上述のように、動的インベントリーを使用して、EC2、Rackspace、OpenStack のようなデータソースからインベントリーをプルすることもできます。

Playbook
=========

Playbook は、インフラストラクチャートポロジーの複数のスライスを細かく調整 (オーケストレーション) することができ、同時に取り組むマシンの数を非常に細かく制御することができます。 ここからが、Ansible で最も魅力的な点になります。

Ansible のオーケストレーションへのアプローチは、細かく調整された簡素化の 1 つです。通常、自動化コードは今後何年にもわたって完全に理解できるものであり、特別な構文や機能について覚えておくべきことはほとんどないためです。

以下は単純な Playbook の例です。

    ---
    - hosts: webservers
    serial: 5 # update 5 machines at a time
    roles:
    - common
    - webapp

    - hosts: content_servers
    roles:
    - common
    - content

.. _ansible_search_path:

Ansible 検索パス
=======================

モジュール、モジュールユーティリティー、プラグイン、Playbook、およびロールは複数の場所に置くことができます。自身でコードを記述して Ansible のコア機能を拡張する場合は、
Ansible コントロールノードの異なる場所に同じ名前を持つ複数のファイルが存在する場合があります。検索パスにより、Ansible が特定のプレイブックの実行で検出して使用するこれらのファイルが決まります。

Ansible の検索パスは、実行時に段階的に増えます。Ansibleは、
特定の実行に含まれる各 Playbook とロールを見つけると、
その Playbook またはロールに関連するすべてのディレクトリーを検索パスに追加します。これらのディレクトリーは、
Playbook またはロールの実行が終了した後でも、
実行中はスコープ内に残ります。Ansibleは、モジュール、モジュールユーティリティー、プラグインを次の順序でロードします。

1. コマンドラインで指定した Playbook に隣接するディレクトリー。``ansible-playbook /path/to/play.yml`` で Ansible を実行し、次のディレクトリーが存在する場合は、そのディレクトリーを Ansible が追加します。

   .. code-block:: bash

      /path/to/modules
      /path/to/module_utils
      /path/to/plugins

2. コマンドラインで指定した Playbook が静的にインポートする 
   Playbook に隣接するディレクトリー。``play.yml`` に ``- import_playbook: /path/to/subdir/play1.yml`` が含まれていて、
   次のディレクトリーが存在する場合は、そのディレクトリーを Ansible が追加します。

   .. code-block:: bash

      /path/to/subdir/modules
      /path/to/subdir/module_utils
      /path/to/subdir/plugins

3. Playbook によって参照されるロールディレクトリーのサブディレクトリー。``play.yml`` が ``myrole`` を実行し、
   次のディレクトリーが存在する場合は、そのディレクトリーを Ansible が追加します。

   .. code-block:: bash

      /path/to/roles/myrole/modules
      /path/to/roles/myrole/module_utils
      /path/to/roles/myrole/plugins

4. ``ansible.cfg`` でデフォルトパスとして指定されたディレクトリー、
   または関連する環境変数で指定されたディレクトリー (さまざまなプラグインタイプのパスを含む)。詳細は、「:ref:`ansible_configuration_settings`」を参照してください。
   ``ansible.cfg`` フィールドの例:

   .. code-block:: bash

      DEFAULT_MODULE_PATH
      DEFAULT_MODULE_UTILS_PATH
      DEFAULT_CACHE_PLUGIN_PATH
      DEFAULT_FILTER_PLUGIN_PATH

   環境変数の例:

   .. code-block:: bash

      ANSIBLE_LIBRARY
      ANSIBLE_MODULE_UTILS
      ANSIBLE_CACHE_PLUGINS
      ANSIBLE_FILTER_PLUGINS

5. Ansible ディストリビューションに同梱される標準ディレクトリー。

.. caution::

   ユーザーが指定したディレクトリーにあるモジュール、
   モジュールユーティリティー、およびプラグインは標準バージョンを上書きします。これには、一般的な名前のファイルも含まれます。
   たとえば、ユーザーが指定したディレクトリーに``basic.py`` という名前のファイルがある場合は、
   標準の ``ansible.module_utils.basic`` が上書きされます。

   同じ名前のモジュール、モジュールユーティリティー、またはプラグインが複数のユーザ指定ディレクトリーにある場合、コマンドラインでのコマンドの順序や、各プレイでのインクルードとロールの順序は、その特定のプレイでどのモジュールが見つかり、使用されるかによって異なります。
