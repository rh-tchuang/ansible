************************************************************
ネットワーク自動化の相違点
************************************************************

ネットワーク自動化は、基本的な Ansible の概念を利用しますが、ネットワークモジュールの動作には重要な相違点があります。このイントロダクションを読むと、本ガイドの演習を学ぶ準備ができます。

.. contents:: トピック

コントロールノードでの実行
================================================================================

ほとんどの Ansible モジュールとは異なり、ネットワークモジュールは管理ノードで実行されません。ユーザーの観点から見ると、ネットワークモジュールは他のモジュールと同じように機能します。アドホックコマンド、Playbook、およびロールと連携します。ただし、背後では、ネットワークモジュールは他の (Linux/Unix および Windows) モジュールが使用する方法とは異なる方法を使用します。Ansible が Python で記述され、実行されます。ほとんどのネットワークデバイスは Python を実行できないため、Ansible ネットワークモジュールは ``ansible`` または ``ansible-playbook`` を実行する Ansible コントロールノードで実行されます。 

また、ネットワークモジュールは、バックアップファイルの宛先として、``backup`` オプションを提供するモジュールにコントロールノードを使用します。Linux/Unix モジュールでは、設定ファイルがすでに管理ノードに存在すると、バックアップファイルは、デフォルトで新しい、変更されたファイルと同じディレクトリーに書き込まれます。ネットワークモジュールはファイルに書き込まれないため、管理ノードの設定ファイルは更新されません。ネットワークモジュールは、通常 Playbook の root ディレクトリーにある `backup` ディレクトリーに、コントロールノードにバックアップファイルを書き込みます。

複数の通信プロトコル
================================================================================

ネットワークモジュールは管理ノードではなくコントロールノードで実行されるため、複数の通信プロトコルに対応できます。各ネットワークモジュールに選択される通信プロトコル (SSH 上の XML、SSH 上の CLI、HTTPS 上の API) は、プラットフォームとモジュールの目的によって異なります。ネットワークモジュールによっては、1 つのプロトコルにしか対応しないものもあります。最も一般的なプロトコルは、SSH 上の CLI です。``ansible_connection`` 変数で通信プロトコルを設定します。

.. csv-table::
   :header: "Value of ansible\_connection", "Protocol", "Requires", "Persistent?"
   :widths:30, 10, 10, 10

   "network\_cli", "CLI over SSH", "network\_os setting", "yes"
   "netconf", "XML over SSH", "network\_os setting", "yes"
   "httpapi", "API over HTTP/HTTPS", "network\_os setting", "yes"
   "local", "depends on provider", "provider setting", "no"

Ansible 2.6 以降では、``local`` ではなく、上記の永続的な接続タイプのいずれかを使用することが推奨されます。永続的な接続では、ホストおよび認証情報は、全タスクではなく一度のみ定義できます。各種プラットフォームで各接続タイプを使用する詳細は、:ref:`platform-specific <platform_options>` ページを参照してください。


ネットワークプラットフォーム別に整理されたモジュール
================================================================================

ネットワークプラットフォームは、モジュールのコレクションで管理できる共通のオペレーティングシステムを備えたネットワークデバイスセットです。 各ネットワークプラットフォームのモジュールは接頭辞を共有します。以下に例を示します。 

- Arista: ``eos_``
- Cisco: ``ios_``, ``iosxr_``, ``nxos_``
- Juniper: ``junos_``
- VyOS ``vyos_``

ネットワークプラットフォーム内のすべてのモジュールは、特定の要件を共有します。一部のネットワークプラットフォームには特別な違いがあります。詳細は、:ref:`platform-specific <platform_options>` のドキュメントを参照してください。


権限昇格: ``enable`` モード、``become``、および ``authorize``
================================================================================

複数のネットワークプラットフォームは、特権ユーザーによる特定タスクの実行が必要な、権限昇格に対応します。ネットワークデバイスでは、これは ``enable`` モード (\*nix 管理での ``sudo`` に相当) と呼ばれます。Ansible ネットワークモジュールは、これに対応するネットワークデバイスに権限昇格を提供します。``enable`` モードに対応するプラットフォームの詳細と、その使用方法は、:ref:`platform-specific <platform_options>` のドキュメントを参照してください。

``become`` を使用した権限昇格
-----------------------------------------

Ansible 2.6 より、トップレベルの Ansible パラメーター ``become: yes`` と ``become_method: enable`` を使用して、権限昇格に対応するネットワークプラットフォームで権限昇格を使用して、タスク、プレイ、Playbook を実行します。``become_method: enable`` とともに ``become: yes`` を使用して、``connection: network_cli`` または ``connection: httpapi`` を使用する必要があります。``network_cli`` を使用して Ansible をネットワークデバイスに接続する場合、``group_vars`` ファイルは以下のようになります。

.. code-block:: yaml

   ansible\_connection: network\_cli
   ansible\_network\_os: ios
   ansible\_become: yes
   ansible\_become\_method: enable

レガシー Playbook : 権限昇格の ``承認``
-----------------------------------------------------------------

Ansible 2.5 以前を実行している場合は、一部のネットワークプラットフォームは権限昇格に対応しますが、``network_cli`` 接続または ``httpapi`` 接続には対応していません。これには、バージョン 2.4 以前のすべてのプラットフォームと、バージョン 2.5 で ``eapi`` を使用した HTTPS 接続が含まれます。``ローカル`` 接続では、``provider`` ディクショナリーを使用し、``authorize: yes`` および ``auth_pass: my_enable_password`` を含める必要があります。このユースケースでは、``group_vars`` ファイルは以下のようになります。

.. code-block:: yaml

   ansible\_connection: local
   ansible\_network\_os: eos
   \# provider settings
eapi:
authorize: yes
auth\_pass: " {{ secret\_auth\_pass }}"
port: 80
transport: eapi
use\_ssl: no

また、タスクで ``eapi`` 変数を使用します。

.. code-block:: yaml

   tasks:
   \- name: provider demo with eos
     eos\_banner:
       banner: motd
       text: |
         this is test
         of multiline
         string
       state: present
       provider: "{{ eapi }}"

Ansible 2.6 は、``provider`` ディレクトリーを使用した ``connection: local`` の使用に対応しますが、この使用は将来非推奨となり、最終的に削除されます。

詳細は、「:ref:`Become およびネットワーク<become_network>`」を参照してください。
