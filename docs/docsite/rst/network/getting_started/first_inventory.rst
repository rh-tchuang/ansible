***********************************************
インベントリーの構築
***********************************************

インベントリーを使用せずに Playbook を実行するには、いくつかのコマンドラインフラグが必要です。また、1 つのデバイスに対して Playbook を実行しても、同じ変更を手動で行うよりも効率性が大幅に向上するわけではありません。Ansible の機能をすべて活用する次のステップとして、インベントリーファイルを使用して管理ノードを ``ansible_network_os`` や SSH ユーザーなどの情報とともにグループにまとめることができます。完全に機能するインベントリーファイルは、ネットワークの信頼できる情報源として使用できます。インベントリーファイルを使用すると、コマンドが 1 つ含まれる 1 つの Playbook で、数百ものネットワークデバイスを維持できます。このページには、段階的にインベントリーファイルを構築する方法が記載されています。

.. contents:: トピック

基本的なインベントリー
==================================================

まず、インベントリーを論理的にグループにまとめます。ベストプラクティスは、サーバーおよびネットワークデバイスを、What (アプリケーション、スタック、またはマイクロサービス)、Where (データセンタまたは地域)、および When (開発段階) でグループ化することです。

- **What**: db、web、leaf、spine
- **Where**: east、west、floor\_19、building\_A
- **When**: dev、test、staging、prod

グループ名にスペースまたはハイフンは使用しないでください。またグループ名は数値で始めないでください (``19th_floor``ではなく ``nova_19`` を使用)。グループ名では、大文字と小文字が区別されます。

この小さなデータセンターの例では、基本的なグループ構造を示しています。グループは、構文 ``[metagroupname:children]`` を使用してグループをまとめることができ、メタグループのメンバーとしてグループを一覧表示できます。ここで、``network`` グループにはすべてのリーフとすべてのスパインが含まれます。グループ ``datacenter`` には、すべてのネットワークデバイスとすべての Web サーバーが含まれます。

.. code-block:: ini

   \[leafs]
   leaf01
   leaf02

   \[spines]
   spine01
   spine02

   \[network:children]
   leafs
   spines

   \[webservers]
   webserver01
   webserver02

   \[datacenter:children]
   network
   webservers


インベントリーへの変数の追加
================================================================================

次に、インベントリーの最初の Ansible コマンドに必要な多くの変数に値を設定するため、ansible-playbook コマンドでこれを省略できます。この例では、インベントリーに各ネットワークデバイスの IP、OS、および SSH ユーザーが含まれています。ネットワークデバイスが IP からのみアクセス可能である場合は、IP をインベントリーファイルに追加する必要があります。ホスト名を使用してネットワークデバイスにアクセスする場合は、IP は必要ありません。

.. code-block:: ini

   \[leafs]
   leaf01 ansible\_host=10.16.10.11 ansible\_network\_os=vyos ansible\_user=my\_vyos\_user
   leaf02 ansible\_host=10.16.10.12 ansible\_network\_os=vyos ansible\_user=my\_vyos\_user

   \[spines]
   spine01 ansible\_host=10.16.10.13 ansible\_network\_os=vyos ansible\_user=my\_vyos\_user
   spine02 ansible\_host=10.16.10.14 ansible\_network\_os=vyos ansible\_user=my\_vyos\_user

   \[network:children]
   leafs
   spines

   \[servers]
   server01 ansible\_host=10.16.10.15 ansible\_user=my\_server\_user
   server02 ansible\_host=10.16.10.16 ansible\_user=my\_server\_user

   \[datacenter:children]
   leafs
   spines
   servers

インベントリー内のグループ変数
================================================================================

グループ内のデバイスが、OS や SSH ユーザーなど、同じ変数値を共有している場合は、この値をグループ変数に統合することで、重複を減らし、メンテナンスを簡素化できます。

.. code-block:: ini

   \[leafs]
   leaf01 ansible\_host=10.16.10.11
   leaf02 ansible\_host=10.16.10.12

   \[leafs:vars]
   ansible\_network\_os=vyos
   ansible\_user=my\_vyos\_user

   \[spines]
   spine01 ansible\_host=10.16.10.13
   spine02 ansible\_host=10.16.10.14

   \[spines:vars]
   ansible\_network\_os=vyos
   ansible\_user=my\_vyos\_user

   \[network:children]
   leafs
   spines

   \[servers]
   server01 ansible\_host=10.16.10.15
   server02 ansible\_host=10.16.10.16

   \[datacenter:children]
   leafs
   spines
   servers

変数の構文
================================================================================

変数値の構文はインベントリー、Playbook、および ``group_vars`` ファイル (以下を参照) で異なります。Playbook と ``group_vars`` ファイルはいずれも YAML で記述されますが、変数の使用方法はそれぞれ異なります。

- ini 形式のインベントリーファイルでは、変数の値 ``ansible_network_os=vyos`` に構文 ``key=value`` を使用する **必要** があります。
- Playbook および ``group_vars`` ファイルを含む ``.yml`` 拡張子または ``.yaml`` 拡張子を持つファイルでは、YAML 構文 ``key: value`` を使用する **必要** があります。

  - ``group_vars`` ファイルで、完全な ``鍵`` 名 ``ansible_network_os: vyos`` を使用します。
  - Playbook で、短縮 ``鍵`` の名前を使用します。これにより、接頭辞 ``ansible`` が削除され ``network_os: vyos`` になります。


プラットフォームによりインベントリーのグループ化
================================================================================

インベントリーが拡大するにつれ、プラットフォーム別にデバイスをグループにまとめることができます。これにより、プラットフォームにあるすべてのデバイスにプラットフォーム固有の変数を簡単に指定できます。

.. code-block:: ini

   \[vyos\_leafs]
   leaf01 ansible\_host=10.16.10.11
   leaf02 ansible\_host=10.16.10.12

   \[vyos\_spines]
   spine01 ansible\_host=10.16.10.13
   spine02 ansible\_host=10.16.10.14

   \[vyos:children]
   vyos\_leafs
   vyos\_spines

   \[vyos:vars]
   ansible\_connection=network\_cli
   ansible\_network\_os=vyos
   ansible\_user=my\_vyos\_user

   \[network:children]
   vyos

   \[servers]
   server01 ansible\_host=10.16.10.15
   server02 ansible\_host=10.16.10.16

   \[datacenter:children]
   vyos
   servers

この設定では、2 つのフラグのみを使用して first\_playbook.yml を実行できます。

.. code-block:: console

   ansible-playbook -i inventory -k first\_playbook.yml

``-k`` フラグを使用して、プロンプトで SSH パスワードを入力します。または、``ansible-vault`` を使用して、SSH や他のシークレット、およびパスワードを group\_vars ファイルに保存して保護できます。


``ansible-vault`` による機密データの保護
================================================================================

``ansible-vault`` コマンドは、パスワードなどのファイルや個々の変数の暗号化を提供します。このチュートリアルでは、1 つの SSH パスワードを暗号化する方法を説明します。以下のコマンドを使用して、その他の機密情報 (データベースパスワード、権限昇格パスワードなど) を暗号化できます。

最初に、ansible-vault 自体にパスワードを作成する必要があります。これは暗号化キーとして使用されるため、Ansible プロジェクト全体で多数の異なるパスワードを暗号化できます。Playbook の実行時に、1 つのパスワード (ansible-vault パスワード) を使用してすべてのシークレット (暗号した値) にアクセスできます。以下は簡単な例です。

ファイルを作成して、ansible-vault のパスワードを書き込みます。

.. code-block:: console

   echo "my-ansible-vault-pw" > ~/my-ansible-vault-pw-file

VyOS ネットワークデバイス用に暗号化された ssh パスワードを作成し、作成したファイルから ansible-vault パスワードをプルします。

.. code-block:: console

   ansible-vault encrypt\_string --vault-id my\_user@~/my-ansible-vault-pw-file 'VyOS\_SSH\_password' --name 'ansible\_password'

ファイルに保存せずに ansible-vault パスワードを入力する必要がある場合は、プロンプトを要求できます。

.. code-block:: console

   ansible-vault encrypt\_string --vault-id my\_user@prompt 'VyOS\_SSH\_password' --name 'ansible\_password'

および、``my_user`` に vault パスワードに入力します。

:option:`--vault-id <ansible-playbook --vault-id>` フラグは、ユーザーごとに異なる vault パスワード、または異なるレベルのアクセスを許可します。この出力には、``ansible-vault`` コマンドのユーザー名 ``my_user`` が含まれ、YAML 構文 ``key: value`` 値を使用します。

.. code-block:: yaml

   ansible\_password: !vault |
          $ANSIBLE\_VAULT;1.2;AES256;my\_user
          66386134653765386232383236303063623663343437643766386435663632343266393064373933
          3661666132363339303639353538316662616638356631650a316338316663666439383138353032
          63393934343937373637306162366265383461316334383132626462656463363630613832313562
          3837646266663835640a313164343535316666653031353763613037656362613535633538386539
          65656439626166666363323435613131643066353762333232326232323565376635
   Encryption successful

INI 形式はインラインの vault に対応していないため、以下は YAML インベントリーから抽出を使用する例です。

.. code-block:: yaml

  ...

  vyos: \# this is a group in yaml inventory, but you can also do under a host
vars:
ansible\_connection: network\_cli
ansible\_network\_os: vyos
ansible\_user: my\_vyos\_user
ansible\_password:  !vault |
$ANSIBLE\_VAULT;1.2;AES256;my\_user
66386134653765386232383236303063623663343437643766386435663632343266393064373933
3661666132363339303639353538316662616638356631650a316338316663666439383138353032
63393934343937373637306162366265383461316334383132626462656463363630613832313562
3837646266663835640a313164343535316666653031353763613037656362613535633538386539
65656439626166666363323435613131643066353762333232326232323565376635

   ...

INI インベントリーでインラインの vault 化した変数を使用するには、これを YAML 形式の「vars」ファイルに保存する必要があります。
これは host\_vars/ または group\_vars/ にあり、自動的に ``vars_files`` または ``include_vars`` 経由でプレイから取得または参照されます。

この設定で Playbook を実行するには、``-k`` フラグを削除し、``vault-id`` のフラグを追加します。

.. code-block:: console

   ansible-playbook -i inventory --vault-id my\_user@~/my-ansible-vault-pw-file first\_playbook.yml

または、vault パスワードファイルの代わりにプロンプトを使用します。

.. code-block:: console

   ansible-playbook -i inventory --vault-id my\_user@prompt first\_playbook.yml

元の値を表示するには、デバッグモジュールを使用します。(この例で使用しているように) YAML ファイルが `ansible_connection` 変数を定義する場合は、次のコマンドを実行すると有効になることに注意してください。これを防ぐには、ansible\_connection 変数なしでファイルのコピーを作成してください。

.. code-block:: console

   cat vyos.yml | grep -v ansible\_connection >> vyos\_no\_connection.yml

   ansible localhost -m debug -a var="ansible\_password" -e "@vyos\_no\_connection.yml" --ask-vault-pass
   Vault password:

   localhost | SUCCESS => {
       "ansible\_password":"VyOS\_SSH\_password"
   }


.. warning::

   Vault のコンテンツは、暗号化に使用されたパスワードでのみ復号できます。パスワードを使用して停止し、新規パスワードに移動する必要がある場合は、``ansible-vault rekey myfile`` で既存の vault コンテンツを更新し、再暗号化してから、古いパスワードと新規パスワードを指定します。vault の内容のコピーは古いパスワードで暗号化したまま、引き続き古いパスワードで複号できます。

インベントリーファイルの構築に関する詳細は、:ref:`インベントリーの概要<intro_inventory>` を参照してください。ansible-vault の詳細は、:ref:`Ansible Vault の全ドキュメント<vault>` を参照してください。

コマンド、Playbook、およびインベントリーの基本を理解したら、より複雑な Ansible Network の例をいくつか説明します。
