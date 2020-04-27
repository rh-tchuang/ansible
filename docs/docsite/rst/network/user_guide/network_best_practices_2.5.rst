.. _network-best-practices:

************************
Ansible ネットワークの例
************************

本ガイドでは、Ansible を使用してネットワークインフラストラクチャーを管理する例を説明します。

.. contents::
   :local:

要件
=============

この例では、以下が必要です。

* **Ansible 2.5** (以降) がインストールされている。詳細は、:ref:`intro_installation_guide` を参照してください。
* Ansible と互換性のある 1 つ以上ネットワークデバイス。
* YAML :ref:`yaml_syntax` の基本的な理解。
* Jinja2 テンプレートの基本的な理解。詳細は、:ref:`playbooks_templating` を参照してください。
* 基本的な Linux コマンドラインのナレッジ。
* ネットワークスイッチおよびルーター設定に関する基本知識。


インベントリーファイルのグループおよび変数
=========================================

``inventory`` は、ホストからグループへのマッピングを定義する YAML または INI のような設定ファイルです。

この例では、インベントリーファイルは、``eos`` グループ、``ios`` グループ、``vyos`` グループを定義し、``switches`` という名前の「グループのグループ」を定義します。サブグループとインベントリーファイルの詳細は、:ref:`Ansible インベントリーグループのドキュメント <subgroups>` を参照してください。

Ansible は柔軟なツールであるため、接続情報と認証情報を指定する方法が複数あります。インベントリーファイルで ``[my_group:vars]`` 機能を使用することが推奨されます。変数内に SSH パスワード (Ansible Vault で暗号化) を指定すると、以下のようになります。

.. code-block:: ini

   [all:vars]
   # these defaults can be overridden for any group in the [group:vars] section
   ansible_connection=network_cli
   ansible_user=ansible

   [switches:children]
   eos
   ios
   vyos

   [eos]
   veos01 ansible_host=veos-01.example.net
   veos02 ansible_host=veos-02.example.net
   veos03 ansible_host=veos-03.example.net
   veos04 ansible_host=veos-04.example.net

   [eos:vars]
   ansible_become=yes
   ansible_become_method=enable
   ansible_network_os=eos
   ansible_user=my_eos_user
   ansible_password= !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     37373735393636643261383066383235363664386633386432343236663533343730353361653735
                     6131363539383931353931653533356337353539373165320a316465383138636532343463633236
                     37623064393838353962386262643230303438323065356133373930646331623731656163623333
                     3431353332343530650a373038366364316135383063356531633066343434623631303166626532
                     9562

   [ios]
   ios01 ansible_host=ios-01.example.net
   ios02 ansible_host=ios-02.example.net
   ios03 ansible_host=ios-03.example.net

   [ios:vars]
   ansible_become=yes
   ansible_become_method=enable
   ansible_network_os=ios
   ansible_user=my_ios_user
   ansible_password= !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     34623431313336343132373235313066376238386138316466636437653938623965383732373130
                     3466363834613161386538393463663861636437653866620a373136356366623765373530633735
                     34323262363835346637346261653137626539343534643962376139366330626135393365353739
                     3431373064656165320a333834613461613338626161633733343566666630366133623265303563
                     8472

   [vyos]
   vyos01 ansible_host=vyos-01.example.net
   vyos02 ansible_host=vyos-02.example.net
   vyos03 ansible_host=vyos-03.example.net

   [vyos:vars]
   ansible_network_os=vyos
   ansible_user=my_vyos_user
   ansible_password= !vault |
                     $ANSIBLE_VAULT;1.1;AES256
                     39336231636137663964343966653162353431333566633762393034646462353062633264303765
                     6331643066663534383564343537343334633031656538370a333737656236393835383863306466
                     62633364653238323333633337313163616566383836643030336631333431623631396364663533
                     3665626431626532630a353564323566316162613432373738333064366130303637616239396438
                     9853

ssh-agent を使用する場合、``ansible_password`` 行は必要ありません。ssh-agent でなく ssh キーを使用し、鍵が複数ある場合は、``ansible_ssh_private_key_file=/path/to/correct/key`` の ``[group:vars]`` セクションで、各接続に使用するキーを指定します。``ansible_ssh_`` オプションの詳細は、「:ref:`behavioral_parameters`」を参照してください。

.. FIXME FUTURE Gundalow - (書き込まれる) ネットワーク認証およびプロキシーページへのリンク

.. warning:: プレーンテキストにパスワードを保存しないでください。

パスワード暗号化用の Ansible vault
-------------------------------------

Ansible の「Vault」機能を使用すると、パスワードやキーなどの機密データを Playbook やロールでプレーンテキストとしてではなく、暗号化されたファイルに保存できます。この vault ファイルは、ソース制御に配布または配置することができます。詳細は :ref:`playbooks_vault` を参照してください。

共通のインベントリー変数
--------------------------

以下の変数はインベントリー内のすべてのプラットフォームに共通ですが、特定のインベントリーグループまたはホストについて上書きできます。

:ansible_connection:

  Ansible は ansible-connection 設定を使用して、リモートデバイスへの接続方法を決定します。Ansible Networking を使用する場合は、Ansible がリモートノードを制限された実行環境のネットワークデバイスとして扱うように ``network_cli`` に設定します。この設定がないと、Ansible は ssh を使用してリモートに接続し、ネットワークデバイスで Python スクリプトを実行します。これは、Python がネットワークデバイスで利用できないため失敗します。
:ansible_network_os:
  このホストが対応するネットワークプラットフォームを Ansible に通知します。これは、``network_cli`` または ``netconf`` を使用する場合に必要です。
:ansible_user:リモートデバイス (スイッチ) に接続する際に使用するユーザーです。これを使用しないと、``ansible-playbook`` を実行しているユーザーが使用されます。
  接続先となるネットワークデバイスのユーザーを指定します。
:ansible_password:
  ``ansible_user`` がログインに使用するパスワード。指定しない場合は、SSH キーが使用されます。
:ansible_become:
  Enable モード (特権モード) を使用する場合は、次のセクションを参照してください。
:ansible_become_method:
  ``network_cli`` で、どのタイプの `become` を使用すべきか。唯一の有効なオプションは ``enable`` です。

権限昇格
--------------------

Arista EOS や Cisco IOS などの特定のネットワークプラットフォームには、異なる権限モードという概念があります。特定のネットワークモジュール (ユーザーを含むシステム状態を修正するモジュールなど) は、高い特権状態でのみ機能します。Ansible は、``connection: network_cli`` を使用する場合に ``become`` に対応します。これにより、必要な特定のタスクに対して権限を作成できます。``become: yes`` および ``become_method: enable`` を、以下に示すように、Ansible に、タスクを実行する前に権限モードに切り替わるように通知します。

.. code-block:: ini

   [eos:vars]
   ansible_connection=network_cli
   ansible_network_os=eos
   ansible_become=yes
   ansible_become_method=enable

詳細は、「:ref:`ネットワークモジュールで become の使用<become_network>`」を参照してください。


ジャンプホスト
----------

Ansible Controller にリモートデバイスへの直接のルートがなく、ジャンプホストを使用する必要がある場合は、その方法を「:ref:`Ansible ネットワークプロキシーコマンド<network_delegate_to_vs_ProxyCommand>`」を参照してください。

例 1: Playbook でファクトを収集し、バックアップファイルの作成
=====================================================================

Ansible ファクトモジュールは、他の Playbook で利用可能なシステム情報「ファクト」を収集します。

Ansible Networking には、多くのネットワーク固有のファクトモジュールが同梱されています。この例では、``_facts`` モジュールの :ref:`eos_facts <eos_facts_module>`、:ref:`ios_facts <ios_facts_module>`、および :ref:`vyos_facts <vyos_facts_module>` を使用してリモートネットワークデバイスに接続します。認証情報はモジュール引数から明示的に渡されるわけではないため、Ansible はインベントリーファイルからユーザー名およびパスワードを使用します。

Ansible の「ネットワークファクトモジュール」はシステムから情報を収集し、結果を ``ansible_net_`` という接頭辞が付けられたファクトに保存します。これらのモジュールで収集されるデータは、モジュールドキュメントの `Return Values` セクション (この場合は :ref:`eos_facts <eos_facts_module>` と :ref:`vyos_facts <vyos_facts_module>`) に記載されています。「Display some facts」タスクで ``ansible_net_version`` などのファクトを使用できます。

正しいモード (*``_facts``) を呼び出すようにするには、インベントリーファイルに定義されたグループに基づいてタスクが条件付きで実行されます。Ansible Playbook での条件付き使用の詳細は、「:ref:`the_when_statement`」を参照してください。

この例では、一部のネットワークスイッチを含むインベントリーファイルを作成してから、Playbook を実行してネットワークデバイスに接続し、その情報を返します。

手順 1:インベントリーの作成
------------------------------

まず、``inventory`` という名前のファイルを作成します。これには以下が含まれます。

.. code-block:: ini

   [switches:children]
   eos
   ios
   vyos

   [eos]
   eos01.example.net

   [ios]
   ios01.example.net

   [vyos]
   vyos01.example.net


手順 2:Playbook の作成
-----------------------------

次に、以下を含む ``facts-demo.yml`` という名前の Playbook ファイルを作成します。

.. code-block:: yaml

   - name: "Demonstrate connecting to switches"
     hosts: switches
     gather_facts: no

     tasks:
       ###
       # Collect data
       #
       - name: Gather facts (eos)
         eos_facts:
         when: ansible_network_os == 'eos'

       - name: Gather facts (ops)
         ios_facts:
         when: ansible_network_os == 'ios'

       - name: Gather facts (vyos)
         vyos_facts:
         when: ansible_network_os == 'vyos'

       ###
       # Demonstrate variables
       #
       - name: Display some facts
         debug:
           msg: "The hostname is {{ ansible_net_hostname }} and the OS is {{ ansible_net_version }}"

       - name: Facts from a specific host
         debug:
           var: hostvars['vyos01.example.net']

       - name: Write facts to disk using a template
         copy:
           content: |
             #jinja2: lstrip_blocks: True
             EOS device info:
               {% for host in groups['eos'] %}
               Hostname: {{ hostvars[host].ansible_net_hostname }}
               Version: {{ hostvars[host].ansible_net_version }}
               Model: {{ hostvars[host].ansible_net_model }}
               Serial: {{ hostvars[host].ansible_net_serialnum }}
               {% endfor %}

             IOS device info:
               {% for host in groups['ios'] %}
               Hostname: {{ hostvars[host].ansible_net_hostname }}
               Version: {{ hostvars[host].ansible_net_version }}
               Model: {{ hostvars[host].ansible_net_model }}
               Serial: {{ hostvars[host].ansible_net_serialnum }}
               {% endfor %}

             VyOS device info:
               {% for host in groups['vyos'] %}
               Hostname: {{ hostvars[host].ansible_net_hostname }}
               Version: {{ hostvars[host].ansible_net_version }}
               Model: {{ hostvars[host].ansible_net_model }}
               Serial: {{ hostvars[host].ansible_net_serialnum }}
               {% endfor %}
           dest: /tmp/switch-facts
         run_once: yes

       ###
       # Get running configuration
       #

       - name: Backup switch (eos)
         eos_config:
           backup: yes
         register: backup_eos_location
         when: ansible_network_os == 'eos'

       - name: backup switch (vyos)
         vyos_config:
           backup: yes
         register: backup_vyos_location
         when: ansible_network_os == 'vyos'

       - name: Create backup dir
         file:
           path: "/tmp/backups/{{ inventory_hostname }}"
           state: directory
           recurse: yes

       - name: Copy backup files into /tmp/backups/ (eos)
         copy:
           src: "{{ backup_eos_location.backup_path }}"
           dest: "/tmp/backups/{{ inventory_hostname }}/{{ inventory_hostname }}.bck"
         when: ansible_network_os == 'eos'

       - name: Copy backup files into /tmp/backups/ (vyos)
         copy:
           src: "{{ backup_vyos_location.backup_path }}"
           dest: "/tmp/backups/{{ inventory_hostname }}/{{ inventory_hostname }}.bck"
         when: ansible_network_os == 'vyos'

手順 3:Playbook の実行
----------------------------

Playbook を実行するには、コンソールプロンプトから以下を実行します。

.. code-block:: console

   ansible-playbook -i inventory facts-demo.yml

このコマンドを実行すると、以下のような出力が返されます。

.. code-block:: console

   PLAY RECAP
   eos01.example.net          : ok=7    changed=2    unreachable=0    failed=0
   ios01.example.net          : ok=7    changed=2    unreachable=0    failed=0
   vyos01.example.net         : ok=6    changed=2    unreachable=0    failed=0

手順 4:Playbook の結果の検証
--------------------------------------

次に、スイッチファクトを含む作成したファイルの内容を確認します。

.. code-block:: console

   cat /tmp/switch-facts

バックアップファイルを確認することもできます。

.. code-block:: console

   find /tmp/backups


`ansible-playbook` が失敗する場合は、:ref:`network_debug_troubleshooting` のデバッグ手順に従ってください。


.. _network-agnostic-examples:

例 2: ネットワークに依存しないモジュールを使用した Playbook の単純化
==============================================================

(この例は、元々 Sean Cavanaugh - `@IPvSean <https://github.com/IPvSean>`_ が投稿したブログ「 `Deep Dive on cli_command for Network Automation <https://www.ansible.com/blog/deep-dive-on-cli-command-for-network-automation>`_」で紹介されました。)

お使いの環境に複数のネットワークプラットフォームがある場合には、ネットワークに依存しないモジュールを使用して Playbook を単純化できます。``eos_config``、``ios_config``、``junos_config`` などのプラットフォーム固有モジュールの代わりに、``cli_command`` または ``cli_config`` などネットワークに依存しないモジュールを使用できます。これにより、Playbook で必要なタスクおよび条件の数が減ります。

.. note::
  ネットワークに依存しないモジュールには、:ref:`network_cli <network_cli_connection>` 接続プラグインが必要です。


プラットフォーム固有のモジュールを含む Playbook のサンプル
----------------------------------------------

この例では、Arista EOS、Cisco NXOS、Juniper JunOS の 3 つのプラットフォームを想定しています。 ネットワークに依存しないモジュールを使用しないと、サンプル Playbook にはプラットフォーム固有のコマンドと共に、以下の 3 つのタスクが含まれる場合があります。

.. code-block:: yaml

  ---
  - name:Run Arista command
    eos_command:
      commands: show ip int br
    when: ansible_network_os == 'eos'

  - name:Run Cisco NXOS command
    nxos_command:
      commands: show ip int br
    when: ansible_network_os == 'nxos'

  - name:Run Vyos command
    vyos_command:
      commands: show interface
    when: ansible_network_os == 'vyos'

ネットワークに依存しないモジュール ``cli_command`` を使用した簡単な Playbook
----------------------------------------------------------------

これらのプラットフォーム固有のモジュールは、以下のようにネットワークに依存しない ``cli_command`` モジュールに置き換えることができます。

.. code-block:: yaml

  ---
  - hosts: network
    gather_facts: false
    connection: network_cli

    tasks:
      - name:Run cli_command on Arista and display results
        block:
        - name:Run cli_command on Arista
          cli_command:
            command: show ip int br
          register: result

        - name:Display result to terminal window
          debug:
            var: result.stdout_lines
        when: ansible_network_os == 'eos'

      - name:Run cli_command on Cisco IOS and display results
        block:
        - name:Run cli_command on Cisco IOS
          cli_command:
            command: show ip int br
          register: result

        - name:Display result to terminal window
          debug:
            var: result.stdout_lines
        when: ansible_network_os == 'ios'

      - name:Run cli_command on Vyos and display results
        block:
        - name:Run cli_command on Vyos
          cli_command:
            command: show interfaces
          register: result

        - name:Display result to terminal window
          debug:
            var: result.stdout_lines
        when: ansible_network_os == 'vyos'


プラットフォームタイプ別に group_vars を使用する場合は、この Playbook をさらに簡単にできます。

.. code-block:: yaml

  ---
  - name:Run command and print to terminal window
    hosts: routers
    gather_facts: false

    tasks:
      - name:Run show command
        cli_command:
          command: "{{show_interfaces}}"
        register: command_output


group_vars を使用すると、この詳細の例を表示できます。また、設定のバックアップの例は、`ネットワークに依存しない例 <https://github.com/network-automation/agnostic_example>`_ で確認できます。

``cli_command`` での複数のプロンプトの使用
------------------------------------------------

``cli_command`` は、複数のプロンプトにも対応します。

.. code-block:: yaml

  ---
  - name:Change password to default
    cli_command:
      command: "{{ item }}"
      prompt:
        - "New password"
        - "Retype new password"
      answer:
        - "mypassword123"
        - "mypassword123"
      check_all:True
    loop:
      - "configure"
      - "rollback"
      - "set system root-authentication plain-text-password"
      - "commit"

このコマンドに関する詳細は、:ref:`cli_command <cli_command_module>` を参照してください。


実装に関する注意点
====================


デモ変数
--------------

これらのタスクは、ディスクにデータを書き込む必要はありませんが、この例では、特定のデバイスまたは名前付きホストのファクトにアクセスする方法を実証するために使用されます。

Ansible ``hostvars`` を使用すると、名前付きホストから変数にアクセスできます。これを行わないと、名前付きホストではなく、現在のホストの詳細が返されます。

詳細は「:ref:`magic_variables_and_hostvars`」を参照してください。

実行中の設定の取得
-------------------------

:ref:`eos_config <eos_config_module>` モジュールおよび :ref:`vyos_config <vyos_config_module>` モジュールには ``backup:`` オプションがあり、これを設定するとモジュールは変更前にリモートデバイスから現在の ``running-config`` の完全バックアップを作成します。バックアップファイルは、Playbook root ディレクトリーの ``backup`` ディレクトリーに書き込まれます。ディレクトリーが存在しない場合は作成されます。

バックアップファイルを別の場所に移動する方法を実証するために、結果を登録し、ファイルを ``backup_path`` に保存されているパスに移動します。

この方法でタスクの変数を使用する場合は、Ansible にこれが変数であることを伝えるために、二重引用符 (``"``) と二重中括弧 (``{{...}}``) を使用します。

トラブルシューティング
===============

接続エラーが出た場合は、インベントリーと Playbook で誤字または不足している行を再度確認してください。それでも問題が発生した場合は、:ref:`network_debug_troubleshooting` のデバッグ手順に従ってください。

.. seealso::

  * :ref:`network_guide`
  * :ref:`intro_inventory`
  * :ref:`Vault ベストプラクティス <best_practices_for_variables_and_vaults>`
