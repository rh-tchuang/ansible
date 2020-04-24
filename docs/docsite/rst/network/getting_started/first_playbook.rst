
.. \_first\_network\_playbook:

***************************************************
最初のコマンドおよび Playbook の実行
***************************************************

このクイックチュートリアルで作業するために学習した概念を記載します。Ansible をインストールし、ネットワーク設定コマンドを手動で実行し、Ansible で同じコマンドを実行してから Playbook を作成するため、複数のネットワークデバイスでいつでもコマンドを実行できます。

.. contents:: トピック

要件
==================================================

このチュートリアルを実行する前に、以下が必要になります。

- Ansible 2.5 (以降) がインストールされている
- Ansible と互換性のある 1 つ以上ネットワークデバイス
- 基本的な Linux コマンドラインのナレッジ
- ネットワークスイッチおよびルーター設定に関する基本知識

Ansible のインストール
==================================================

希望する方法を使用して、Ansible をインストールします。:ref:`installation_guide` を参照してください。その後、このチュートリアルに戻ります。

Ansible のバージョンを確認します (2.5 以下である必要があります)。

.. code-block:: bash

   ansible --version


管理ノードへの手動接続の確立
==================================================

認証情報を確認するには、手動でネットワークデバイスに接続し、その設定を取得します。サンプルユーザーとデバイス名を実際の認証情報に置き換えます。たとえば、VyOS ルーターの場合は、以下のようになります。

.. code-block:: bash

   ssh my\_vyos\_user@vyos.example.net
   show config
   exit

この手動接続により、ネットワークデバイスの信頼性も確立され、既知のホストの一覧に RSA 鍵フィンガープリントが追加されます。(以前にデバイスを接続したことがある場合は、その信頼性がすでに確立されています。)


最初のネットワーク Ansible コマンドの実行
==================================================

ネットワークデバイスでコマンドを手動で接続して実行する代わりに、1 つの削除済み Ansible コマンドで設定を取得できます。

.. code-block:: bash

   ansible all -i vyos.example.net, -c network\_cli -u my\_vyos\_user -k -m vyos\_facts -e ansible\_network\_os=vyos

このコマンドのフラグは、7 つの値を設定します。
  \- コマンドを適用するホストグループ (この場合は all)
  \- インベントリー (-i, ターゲットに設定するデバイス (最後のコンマがない -i はインベントリーファイルを指定なし))
  \- 接続方法 (-c、ansible の接続方法および実行方法)
  \- ユーザー (-u、SSH 接続のユーザー名)
  \- SSH 接続の方法 (-k、パスワードのプロンプト有り)
  \- モジュール (-m、実行する ansible モジュール)
  \- 追加変数 (-e、この場合は、ネットワーク OS 値の設定)

注記:ssh 鍵で ``ssh-agent`` を使用する場合、Ansible は自動的にこれを読み込みます。``-k`` フラグは省略できます。


最初のネットワークの Ansible Playbook の作成および実行
==================================================

このコマンドを毎日実行する必要がある場合には、Playbook に保存し、ansible の代わりに ansible-playbook を使用して実行します。Playbook はコマンドラインにフラグを付けて指定した多くのパラメーターを保存でき、コマンドラインに入力を少なくすることができます。これには、2 つのファイル (Playbook とインベントリーファイル) が必要です。

1. :download:`first_playbook.yml <sample_files/first_playbook.yml>` をダウンロードします。これは以下のようになります。

.. literalinclude:: sample\_files/first\_playbook.yml
   :language: YAML

Playbook は、上記のコマンドラインの 7 つの中から 3 つの値 (グループ (``hosts: all``)、接続方法 (``connection: network_cli``) 、およびモジュール (各タスク)) を選択します。これらの値が Playbook に設定されると、それらをコマンドラインで省略できます。Playbook は、config 出力を表示する別のタスクも追加します。Playbook でモジュールが実行されると、出力はコンソールに書き込まれるのではなく、今後のタスクで使用するためにメモリーに保持されます。ここでのデバッグタスクを使用すると、シェルで結果を確認できます。

2. 以下のコマンドを使用して Playbook を実行します。

.. code-block:: bash

   ansible-playbook -i vyos.example.net, -u ansible -k -e ansible\_network\_os=vyos first\_playbook.yml

Playbook には、2 つのタスクを持つプレイが 1 つ含まれており、次のような出力が生成されます。

.. code-block:: bash

   $ ansible-playbook -i vyos.example.net, -u ansible -k -e ansible\_network\_os=vyos first\_playbook.yml

   PLAY \[First Playbook]
   ***************************************************************************************************************************

   TASK \[Get config for VyOS devices]
   ***************************************************************************************************************************
   ok: \[vyos.example.net]

   TASK \[Display the config]
   ***************************************************************************************************************************
   ok: \[vyos.example.net] => {
       "msg":"The hostname is vyos and the OS is VyOS"
   }

3. デバイス設定を取得できるようになったため、Ansible での更新を試行してください。最初の Playbook の拡張バージョンである :download:`first_playbook_ext.yml <sample_files/first_playbook_ext.yml>` をダウンロードします。

.. literalinclude:: sample\_files/first\_playbook\_ext.yml
   :language: YAML

最初の Playbook の拡張では、1 つのプレイに 4 つのタスクがあります。上記と同じコマンドで実行します。この出力では、Ansible が設定に加えられた変更が表示されます。

.. code-block:: bash

   $ ansible-playbook -i vyos.example.net, -u ansible -k -e ansible\_network\_os=vyos first\_playbook\_ext.yml

   PLAY \[First Playbook]
   ************************************************************************************************************************************

   TASK \[Get config for VyOS devices]
   **********************************************************************************************************************************
   ok: \[vyos.example.net]

   TASK \[Display the config]
   *************************************************************************************************************************************
   ok: \[vyos.example.net] => {
       "msg":"The hostname is vyos and the OS is VyOS"
   }

   TASK \[Update the hostname]
   *************************************************************************************************************************************
   changed: \[vyos.example.net]

   TASK \[Get changed config for VyOS devices]
   *************************************************************************************************************************************
   ok: \[vyos.example.net]

   TASK \[Display the changed config]
   *************************************************************************************************************************************
   ok: \[vyos.example.net] => {
       "msg":"The hostname is vyos-changed and the OS is VyOS"
   }

   PLAY RECAP
   ************************************************************************************************************************************
   vyos.example.net           : ok=6    changed=1    unreachable=0    failed=0



.. \_network\_gather\_facts:

ネットワークデバイスからのファクトの収集
====================================

``gather_facts`` キーワードが、標準化された鍵と値のペアでネットワークデバイスファクトの収集に対応するようになりました。これらのネットワークファクトをさらにタスクに送信して、ネットワークデバイスを管理できます。

また、新しい ``gather_network_resources`` パラメーターを、ネットワークの ``*_facts`` モジュール (:ref:`eos_facts <eos_facts_module>` など) とともに使用すると、以下のようにデバイス設定のサブセットのみを返すことができます。

.. code-block:: yaml

  - hosts: arista
    gather\_facts:True
    gather\_subset: min
    module\_defaults:
      eos\_facts:
        gather\_network\_resources: interfaces

Playbook は以下のインターフェースのファクトを返します。

.. code-block:: yaml

  ansible\_facts:
     ansible\_network\_resources:
        interfaces:
        \- enabled: true
          name:Ethernet1
          mtu:'1476'
        \- enabled: true
          name:Loopback0
        \- enabled: true
          name:Loopback1
        \- enabled: true
          mtu:'1476'
          name:Tunnel0
        \- enabled: true
          name:Ethernet1
        \- enabled: true
          name:Tunnel1
        \- enabled: true
          name:Ethernet1


これは、``gather_subset: interfaces`` を設定するだけで返される内容のサブセットを返すことに注意してください。

これらのファクトを保存し、:ref:`eos_interfaces <eos_interfaces_module>` リソースモジュールなどの別のタスクで直接使用できます。
