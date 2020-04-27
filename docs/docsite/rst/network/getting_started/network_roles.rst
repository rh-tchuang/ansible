
.. _using_network_roles:

*************************
Ansible ネットワークロールの使用
*************************

ロールは、連携する Ansible のデフォルト、ファイル、タスク、テンプレート、変数、およびその他の Ansible コンポーネントのセットです。:ref:`first_network_playbook` で確認したとおり、コマンドから Playbook に移行することで、複数のタスクを簡単に実行し、同じタスクを同じ順序で繰り返し実行できます。Playbook からロールへの移行により、順序付けされたタスクの再使用および共有がより簡単になります。:ref:`Ansible Galaxy <ansible_galaxy>` を見ると、自分のロールを共有し、他の人のロールを直接または間接的に使用できます。

.. contents::
   :local:

ロールについて
===================

ロールの役割とはなんですか。なぜそれを気にかける必要がありますか。Ansible ロールは基本的に、既知のファイル構造に分割される Playbook です。Playbook からロールに移動すると、Ansible ワークフローの共有、読み取り、および更新が容易になります。ユーザーは、独自のロールを作成できます。たとえば、独自の DNS Playbook を作成する必要はありません。代わりに、DNS サーバーおよびロールを指定して、これを設定します。

ワークフローをさらに単純化するために、Ansible Network チームは一般的なネットワークユースケース向けに一連のロールを作成しました。このようなロールを使用すると、ホイールを再作成する必要がなくなります。独自の ``create_vlan`` Playbook またはロールを作成し、維持する代わりに、ネットワークのトポロジーとインベントリーを記述するパーサーテンプレートの設計、コード化、および保守に集中し、Ansible のネットワークロールが機能するようにできます。Ansible Galaxy では、`ネットワーク関連のロール <https://galaxy.ansible.com/ansible-network>`_ を参照してください。

DNS Playbook のサンプル
---------------------

ロールの概念を実証するために、以下の例の ``playbook.yml`` は 2 つのタスクの Playbook を含む 1 つの YAML ファイルです。 この Ansible Playbook は Cisco IOS﻿ デバイスにホスト名を設定し、DNS (ドメイン名システム) サーバーを設定します。

.. code-block:: yaml

   ---
   - name: configure cisco routers
     hosts: routers
     connection: network_cli
     gather_facts: no
     vars:
       dns:"8.8.8.8 8.8.4.4"

     tasks:
      - name: configure hostname
        ios_config:
          lines: hostname {{ inventory_hostname }}

      - name: configure DNS
        ios_config:
          lines: ip name-server {{dns}}

``ansible-playbook`` コマンドを使用してこの Playbook を実行すると、以下の出力が表示されます。 この例では、``-l`` オプションを使用して Playbook を **rtr1** ノードでのみ実行することを制限します。

.. code-block:: bash

   [user@ansible ~]$ ansible-playbook playbook.yml -l rtr1

   PLAY [configure cisco routers] *************************************************

   TASK [configure hostname] ******************************************************
   changed: [rtr1]

   TASK [configure DNS] ***********************************************************
   changed: [rtr1]

   PLAY RECAP *********************************************************************
   rtr1                       : ok=2    changed=2    unreachable=0    failed=0


この Playbook はホスト名および DNS サーバーを設定しました。 Cisco IOS XE **rtr1** ルーターで設定を確認できます。

.. code-block:: bash

   rtr1#sh run | i name
   hostname rtr1
   ip name-server 8.8.8.8 8.8.4.4

Playbook のロールへの変換
---------------------------------

次の手順では、この Playbook を再利用可能なロールに変換します。ディレクトリー構造は手動で作成することも、``ansible-galaxy init`` を使用してロールの標準フレームワークを作成することもできます。

.. code-block:: bash

   [user@ansible ~]$ ansible-galaxy init system-demo
   [user@ansible ~]$ cd system-demo/
   [user@ansible system-demo]$ tree
   .
   ├── defaults
   │   └── main.yml
   ├── files
   ├── handlers
   │   └── main.yml
   ├── meta
   │   └── main.yml
   ├── README.md
   ├── tasks
   │   └── main.yml
   ├── templates
   ├── tests
   │   ├── inventory
   │   └── test.yml
   └── vars
     └── main.yml

この最初のデモでは、**tasks** ディレクトリーおよび **vars** ディレクトリーのみを使用しています。 ディレクトリー構造は以下のようになります。

.. code-block:: bash

   [user@ansible system-demo]$ tree
   .
   ├── tasks
   │   └── main.yml
   └── vars
       └── main.yml

次に、``vars`` セクションおよび ``tasks`` セクションの内容を元の Ansible Playbook からロールに移動します。まず、これらのタスクを ``tasks/main.yml`` ファイルに移動します。

.. code-block:: bash

   [user@ansible system-demo]$ cat tasks/main.yml
   ---
   - name: configure hostname
     ios_config:
       lines: hostname {{ inventory_hostname }}

   - name: configure DNS
     ios_config:
       lines: ip name-server {{dns}}

次に、変数を ``vars/main.yml`` ファイルに移動します。

.. code-block:: bash

   [user@ansible system-demo]$ cat vars/main.yml
   ---
   dns:"8.8.8.8 8.8.4.4"

最後に、元の Ansible Playbook を変更して、``tasks`` セクションおよび ``vars`` セクションを削除し、``roles`` キーワードをロール名 (この場合は ``system-demo``) に追加します。 この Playbook があります。

.. code-block:: yaml

   ---
   - name: configure cisco routers
     hosts: routers
     connection: network_cli
     gather_facts: no

     roles:
       - system-demo

要約すると、このデモでは、3 つのディレクトリー数と 3 つの YAML ファイル数の合計を使用するようになりました。 ロールを表す ``system-demo`` ディレクトリーがあります。 この ``system-demo`` には、``tasks`` および ``vars`` の 2 つのディレクトリーがあります。 ``main.yml`` には、それぞれのフォルダーがあります。 ``vars/main.yml`` には、``playbook.yml`` の変数が含まれます。 ``tasks/main.yml`` には、``playbook.yml`` のタスクが含まれます。 ``playbook.yml`` ファイルは、vars および tasks を直接指定するのではなく、ロールを呼び出すように変更されました。 以下は、現在の作業ディレクトリーのツリーです。

.. code-block:: bash

   [user@ansible ~]$ tree
   .
   ├── playbook.yml
   └── system-demo
       ├── tasks
       │   └── main.yml
       └── vars
           └── main.yml

Playbook を実行すると、出力が若干異なる同じ動作になります。

.. code-block:: bash

   [user@ansible ~]$ ansible-playbook playbook.yml -l rtr1

   PLAY [configure cisco routers] *************************************************

   TASK [system-demo : configure hostname] ****************************************
   ok: [rtr1]

   TASK [system-demo : configure DNS] *********************************************
   ok: [rtr1]

   PLAY RECAP *********************************************************************
   rtr1             : ok=2    changed=0    unreachable=0    failed=0

上記のように、各タスクの前にロール名 (この場合は ``system-demo``) が追加されます。 複数のロールを含む Playbook を実行する場合、これはタスクがどこから呼び出されるかを正確に特定するのに役立ちます。 この Playbook は、開始した 1 つのファイル Playbook の動作が同じであるため、``変更`` せずに ``ok`` を返しました。

前述のように、Playbook は Cisco IOS-XE ルーターで以下の設定を生成します。

.. code-block:: bash

   rtr1#sh run | i name
   hostname rtr1
   ip name-server 8.8.8.8 8.8.4.4


このため、Ansible ロールは単に分解された Playbook として見なすことができます。ロールらはシンプルで、効果的で、再利用が可能です。 別のユーザーは、カスタムの「ハードコードされた」Playbook を作成する代わりに、単に ``system-demo`` ロールを含めることができます。

変数の優先度
-------------------

DNS サーバーを変更するにはどうすれば良いですか。 ロール構造内で ``vars/main.yml`` を変更することは想定されていません。Ansible には、特定のプレイの変数を指定できる場所が多数あります。変数および優先順位の詳細は、「:ref:`playbooks_variables`」を参照してください。変数を配置する場所は、実際には 21 個あります。 この一覧は一見すると過度に見えるかもしれませんが、ほとんどのユースケースでは、最も優先度の低い変数の場所や、最も優先度の高い変数を渡す方法のみを理解している必要があります。変数の配置場所に関する詳細は、:ref:`ansible_variable_precedence` を参照してください。

最も低い優先度
^^^^^^^^^^^^^^^^^

最も低い優先度は、ロール内の ``defaults`` ディレクトリーです。 これは、変数を指定できる可能性のあるその他の 20 の場所はすべて、``デフォルト`` 値よりも優先されることを意味します。 ``system-demo`` ロールからの変数の優先順位を一番低くするには、``vars`` ディレクトリーの名前を ``defaults`` に変更します。

.. code-block:: bash

   [user@ansible system-demo]$ mv vars defaults
   [user@ansible system-demo]$ tree
   .
   ├── defaults
   │   └── main.yml
   ├── tasks
   │   └── main.yml

デフォルトの動作を上書きするために、Playbook に新規の ``vars`` セクションを追加します (ここでは、``dns`` 変数が 8.8.8.8 および 8.8.4.4 に設定されています)。 このデモでは、``dns`` を 1.1.1.1 に設定し、``playbook.yml`` は以下のようになります。

.. code-block:: yaml

   ---
   - name: configure cisco routers
     hosts: routers
     connection: network_cli
     gather_facts: no
     vars:
       dns: 1.1.1.1
     roles:
       - system-demo

この更新された Playbook を **rtr2** で実行します。

.. code-block:: bash

   [user@ansible ~]$ ansible-playbook playbook.yml -l rtr2

**rtr2** Cisco ルーターの設定は以下のようになります。

.. code-block:: bash

   rtr2#sh run | i name-server
   ip name-server 1.1.1.1

Playbook で設定された変数が ``defaults`` ディレクトリーよりも優先されるようになりました。 実際に、変数を設定する他の場所も、``defaults`` ディレクトリーの値よりも優先されます。

最も高い優先度
^^^^^^^^^^^^^^^^^^

ロール内の ``defaults`` ディレクトリーで変数を指定すると、常に優先順位が一番低くなります。一方、``-e`` または ``--extra-vars=`` を使用して ``vars`` を追加の変数として指定すると、常に優先順位が最も高くなります。 ``-e`` オプションを使用して Playbook を再実行すると、``defaults`` ディレクトリー (8.8.4.4 および 8.8.8.8) と、1.1.1.1 dns サーバーを含む Playbook に新たに作成された ``vars`` の両方が上書きされます。

.. code-block:: bash

   [user@ansible ~]$ ansible-playbook playbook.yml -e "dns=192.168.1.1" -l rtr3

Cisco IOS XE ルーターの結果には、優先度の最も高い 192.168.1.1 設定のみが含まれます。

.. code-block:: bash

   rtr3#sh run | i name-server
   ip name-server 192.168.1.1

これはどのように役立ちますか。 なぜそれを気にかけないといけませんか。 追加の変数は通常、ネットワークオペレーターがデフォルトをオーバーライドするために使用されます。 この強力な例は、Red Hat Ansible Tower と Survey 機能です。 Web UI で、ネットワークオペレーターに Web フォームによるパラメーターの入力を要求できます。 これは、非技術的 Playbook の作成者が Web ブラウザーを使用して Playbook を実行するのが非常に簡単な場合があります。詳細は、「 `Ansible Tower Job Template Surveys <https://docs.ansible.com/ansible-tower/latest/html/userguide/workflow_templates.html#surveys>`_ 」を参照してください。


Ansible で対応しているネットワークロール
===============================

Ansible Network チームは、Ansible Galaxy で `ネットワーク関連のロール <https://galaxy.ansible.com/ansible-network>`_ を開発し、対応します。このようなロールを使用して、ネットワーク自動化の作業を開始できます。このようなロールは、最新の Ansible ネットワークコンテンツにアクセスできるように約 2 時間ごとに更新されます。

このようなロールは以下のカテゴリーに分類されます。

* **ユーザーロール** - 設定の管理など、ユーザーロールはタスクにフォーカスします。`config_manager <https://galaxy.ansible.com/ansible-network/config_manager>`_、 `cloud_vpn <https://galaxy.ansible.com/ansible-network/cloud_vpn>`_ などのロールを Playbook で直接使用します。これらのロールはプラットフォーム/プロバイダーに依存しないため、異なるネットワークプラットフォームまたはクラウドプロバイダーで同じロールおよび Playbook を使用できます。
* **プラットフォームプロバイダーロール** - プロバイダーロールは、ユーザーロールとさまざまなネットワーク OS の間で変換され、それぞれ API が異なります。各プロバイダーロールは、対応しているユーザーロールからの入力を許可し、特定のネットワーク OS 用にその入力を変換します。ネットワークユーザーロールは、このようなプロバイダーロールに依存して機能を実装します。たとえば、 `config_manager <https://galaxy.ansible.com/ansible-network/config_manager>`_ ユーザーロールは `cisco_ios <https://galaxy.ansible.com/ansible-network/cisco_ios>`_ プロバイダーロールを使用して、Cisco IOS ネットワークデバイスにタスクを実装します。
* **クラウドのプロバイダーロールおよびプロビジョナーロール** - 同様に、クラウドユーザーロールは、クラウドのプロバイダーロールおよびプロビジョナーロールに依存して、特定のクラウドプロバイダーのクラウド機能を実装します。たとえば、 `cloud_vpn <https://galaxy.ansible.com/ansible-network/cloud_vpn>`_ ロールは、AWS と通信する `aws <https://galaxy.ansible.com/ansible-network/aws>`_ プロバイダーロールに依存します。


ネットワークユーザーロールに最低でも 1 つのプラットフォームプロバイダーロールをインストールし、``ansible_network_provider`` をそのプロバイダー (``ansible_network_provider: ansible-network.cisco_ios`` など) に設定する必要があります。Ansible Galaxy は、Ansible Galaxy のロール詳細に記載されているその他の依存関係を自動的にインストールします。

たとえば、Cisco IOS デバイスで ``config_manager`` ロールを使用するには、以下のコマンドを使用します。

.. code-block:: bash

   [user@ansible]$ ansible-galaxy install ansible-network.cisco_ios
   [user@ansible]$ ansible-galaxy install ansible-network.config_manager

ロールは、Ansible Galaxy の例 (各ロールの **Read Me** タブ) で詳細に説明されています。

ネットワークロールのリリースサイクル
===========================

Ansible ネットワークチームは、更新および新しいロールを 2 週間ごとにリリースします。Ansible Galaxy のロール詳細は利用可能なロールバージョンを一覧表示し、GitHub リポジトリーで、ロールの各バージョンで変更されたものを一覧表示する changelog ファイル (``cisco_ios`` `CHANGELOG.rst <https://github.com/ansible-network/cisco_ios/blob/devel/CHANGELOG.rst>`_ など) を検索できます。

Ansible Galaxy ロールバージョンには、2 つのコンポーネントがあります。

* メジャーリリース番号 - (2.6 など) このロールが対応する Ansible Engine のバージョンを示します。
* ロールのリリースサイクルを示し、Ansible Engine のマイナーリリースバージョンを反映しないマイナーリリース番号 (.1 など)。

インストールされたロールの更新
------------------------

ロールの Ansible Galaxy ページには、利用可能なバージョンの一覧が表示されます。ローカルにインストールされたロールを新規または異なるバージョンに更新するには、バージョンおよび ``--force`` オプションを指定して ``ansible-galaxy install`` コマンドを使用します。このバージョンに対応するために、依存するロールの手動更新が必要になる場合があります。依存するロールの最小バージョン要件は、Galaxy のロール **Read Me** タブを参照してください。

.. code-block:: bash

  [user@ansible]$ ansible-galaxy install ansible-network.network_engine,v2.7.0 --force
  [user@ansible]$ ansible-galaxy install ansible-network.cisco_nxos,v2.7.1 --force

.. seealso::

       `Ansible Galaxy ドキュメント <https://galaxy.ansible.com/docs/>`_
           Ansible Galaxy ユーザーガイド
       `Ansible で対応するネットワークロール <https://galaxy.ansible.com/ansible-network>`_
           Ansible Galaxy での Ansible が対応するネットワークおよびクラウドロールの一覧
