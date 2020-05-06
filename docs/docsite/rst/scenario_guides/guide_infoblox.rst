.. _nios_guide:

************************
 Infoblox ガイド
************************

.. contents:: トピック

本ガイドでは、Infoblox NIOS (Network Identity Operating System) で Ansible を使用する方法を説明します。Ansible 統合では、Ansible Playbook を使用して、IP アドレス管理 (IPAM)、DNS、およびインベントリー追跡について Infoblox Core Network Services を自動化できます。

ドキュメントの簡単なサンプルタスクで、:ref:`NIOS モジュール <nios_net tools_modules>` について確認し、詳細な例は「`モジュールを使用した使用事例`_」のセクションを参照してください。Infoblox 製品の詳細は、`Infoblox <https://www.infoblox.com/>`_ の Web サイトを参照してください。

.. note:: 本ガイドで使用されている Playbook の例のほとんどは、GitHub リポジトリー `network-automation/infoblox_ansible <https://github.com/network-automation/infoblox_ansible>`_ から取得できます。

要件
=============
Infoblox で Ansible ``nios`` モジュールを使用する前に、Ansible コントロールノードに ``infoblox-client`` をインストールする必要があります。

.. code-block:: bash

    $ sudo pip install infoblox-client

.. note::
    Infoblox で Ansible を使用するには、WAPI 機能が有効になっている NIOS アカウントが必要です。

.. _nios_credentials:

認証情報および認証
==============================

Playbook で Infoblox の ``nios`` モジュールを使用するには、Infoblox システムにアクセスするための認証情報を設定する必要があります。 本ガイドの例では、``<playbookdir>/group_vars/nios.yml`` に保存されている認証情報を使用します。これらの値を、Infoblox 認証情報に置き換えます。

.. code-block:: yaml

    ---
    nios_provider:
      host:192.0.0.2
      username: admin
      password: ansible

NIOS Lookup プラグイン
===================

Ansible には、NIOS 用に以下の lookup プラグインが含まれます。

- :ref:`nios <nios_lookup>` - Infoblox WAPI API を使用して NIOS が指定されたオブジェクト (ネットワークビュー、DNS ビュー、ホストレコードなど) を取得します。
- :ref:`nios_next_ip <nios_next_ip_lookup>` - ネットワークから次に利用可能な IP アドレスを指定します。この例では、「`ホストレコードの作成`_」を参照してください。
- :ref:`nios_next_network <nios_next_network_lookup>` - ネットワークコンテナーで利用可能な次のネットワーク範囲を返します。

``connection: local`` を指定して、NIOS lookup プラグインをローカルに実行する必要があります。詳細は、「:ref:`lookup プラグイン <lookup_plugins>`」を参照してください。


すべてのネットワークビューの取得
----------------------------

すべてのネットワークビューを取得して変数に保存するには、:ref:`nios <nios_lookup>` lookup プラグインで :ref:`set_fact` <set_fact_module>モジュールを使用します。

.. code-block:: yaml

    ---
    - hosts: nios
      connection: local
      tasks:
        - name: fetch all networkview objects
          set_fact:
            networkviews: "{{ lookup('nios', 'networkview', provider=nios_provider) }}"

        - name: check the networkviews
          debug:
            var: networkviews


ホストレコードの取得
------------------------

ホストレコードのセットを取得するには、``nios`` lookup プラグインで ``set_fact`` モジュールを使用し、取得する特定ホストのフィルターを含めます。

.. code-block:: yaml

    ---
    - hosts: nios
      connection: local
      tasks:
        - name: fetch host leaf01
          set_fact:
             host: "{{ lookup('nios', 'record:host', filter={'name': 'leaf01.ansible.com'}, provider=nios_provider) }}"

        - name: check the leaf01 return variable
          debug:
            var: host

        - name: debug specific variable (ipv4 address)
          debug:
            var: host.ipv4addrs[0].ipv4addr

        - name: fetch host leaf02
          set_fact:
            host: "{{ lookup('nios', 'record:host', filter={'name': 'leaf02.ansible.com'}, provider=nios_provider) }}"

        - name: check the leaf02 return variable
          debug:
            var: host


この Playbook ``get_host_record.yml`` を実行すると、以下のような結果が表示されるはずです。

.. code-block:: none

    $ ansible-playbook get_host_record.yml

PLAY [localhost] ***************************************************************************************

    TASK [fetch host leaf01] ******************************************************************************
ok:[localhost]
    
    TASK [check the leaf01 return variable] *************************************************************
ok: [localhost] => {
    < ...output shortened...>
        "host": {
            "ipv4addrs": [
            {
                "configure_for_dhcp": false,
                "host": "leaf01.ansible.com",
            }
        ],
            "name": "leaf01.ansible.com",
            "view": "default"
        }
    }
    
    TASK [debug specific variable (ipv4 address)] ******************************************************
    ok: [localhost] => {
        "host.ipv4addrs[0].ipv4addr":"192.168.1.11"
    }
    
    TASK [fetch host leaf02] ******************************************************************************
ok:[localhost]
    
    TASK [check the leaf02 return variable] *************************************************************
    ok: [localhost] => {
    < ...output shortened...>
    "host": {
            "ipv4addrs": [
            {
                "configure_for_dhcp": false,
                "host": "leaf02.example.com",
                "ipv4addr": "192.168.1.12"
            }
        ],
        }
}
    
    PLAY RECAP ******************************************************************************************
    localhost                  : ok=5    changed=0    unreachable=0    failed=0
    
上記の出力は、``nios`` lookup プラグインによって取得した ``leaf01.ansible.com`` および ``leaf02.ansible.com`` のホストレコードを示しています。この Playbook は、他の Playbook で使用できる変数に情報を保存します。これにより、Infoblox を単一のソースとして使用し、動的に変更する情報を収集して使用できます。Ansible 変数の使用方法の詳細は、:ref:`playbooks_variables` を参照してください。取得できるその他のデータオプションは、:ref:`nios <nios_lookup>` の例を参照してください。

この Playbook には、`Infoblox lookup playbooks <https://github.com/network-automation/infoblox_ansible/tree/master/lookup_playbooks>`_ でアクセスできます。

モジュールとのユースケース
======================

``nios`` モジュールをタスク内で使用して、共通の Infoblox ワークフローを簡素化できます。これらの例に従う前に、:ref:`NIOS 認証情報<nios_credentials>` を必ず設定してください。

IPv4 ネットワークの設定
---------------------------

IPv4 ネットワークを設定するには、:ref:`nios_network <nios_network_module>` モジュールを使用します。

.. code-block:: yaml

    ---
    - hosts: nios
      connection: local
      tasks:
        - name:Create a network on the default network view
          nios_network:
            network:192.168.100.0/24
            comment: sets the IPv4 network
            options:
              - name: domain-name
                value: ansible.com
            state: present
            provider: "{{nios_provider}}"

最後のパラメーター ``provider`` は、``group_vars/`` ディレクトリーに定義された変数 ``nios_provider`` を使用します。

ホストレコードの作成
----------------------

新たに作成した IPv4 ネットワーク上に `leaf03.ansible.com` という名前のホストレコードを作成するには、以下を実行します。

.. code-block:: yaml

    ---
    - hosts: nios
      connection: local
      tasks:
        - name: configure an IPv4 host record
          nios_host_record:
            name: leaf03.ansible.com
            ipv4addrs:
              - ipv4addr:
                  "{{ lookup('nios_next_ip', '192.168.100.0/24', provider=nios_provider)[0] }}"
            state: present
    provider: "{{nios_provider}}"

この例の IPv4 アドレスは、:ref:`nios_next_ip <nios_next_ip_lookup>` lookup プラグインを使用して、ネットワーク上で次に利用可能な IPv4 アドレスを検索します。

正引き DNS ゾーンの作成
---------------------------

正引き DNS ゾーンを設定するには、``nios_zone`` モジュールを使用します。

.. code-block:: yaml

    ---
    - hosts: nios
      connection: local
      tasks:
        - name:Create a forward DNS zone called ansible-test.com
          nios_zone:
            name: ansible-test.com
            comment: local DNS zone
            state: present
            provider: "{{ nios_provider }}"

逆引き DNS ゾーンの作成
---------------------------

逆引き DNS ゾーンを設定するには、以下を行います。

.. code-block:: yaml

    ---
    - hosts: nios
      connection: local
      tasks:
        - name: configure a reverse mapping zone on the system using IPV6 zone format
          nios_zone:
            name:100::1/128
            zone_format:IPV6
            state: present
            provider: "{{ nios_provider }}"

動的インベントリースクリプト
========================

Infoblox 動的インベントリースクリプトを使用して、Infoblox NIOS でネットワークノードのインベントリーをインポートできます。Infoblox からインベントリーを収集するには、以下の 2 つのファイルが必要です。

- `infoblox.yaml <https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/infoblox.yaml>`_ - NIOS プロバイダーの引数とオプションフィルターを指定するファイル。

- `infoblox.py <https://raw.githubusercontent.com/ansible/ansible/devel/contrib/inventory/infoblox.py>`_ - NIOS インベントリーを取得する python スクリプトです。

Infoblox 動的インベントリースクリプトを使用するには、以下を実行します。

#. Download the ``infoblox.yaml`` ファイルを作成し、これを ``/etc/ansible`` ディレクトリーに保存します。

NIOS 認証情報が含まれる #. Modify the ``infoblox.yaml`` ファイル

#. Download the ``infoblox.py`` ファイルを ``/etc/ansible/hosts`` ディレクトリーに保存します。

実行可能にする #. Change the permissions on the ``infoblox.py`` ファイル

.. code-block:: bash

    $ sudo chmod +x /etc/ansible/hosts/infoblox.py

必要に応じて、``./infoblox.py --list`` を使用してスクリプトをテストできます。数分後に、Infoblox インベントリーが JSON 形式で表示されるはずです。以下のように Infoblox 動的インベントリースクリプトを明示的に使用できます。

.. code-block:: bash

    $ ansible -i infoblox.py all -m ping

Infoblox 動的インベントリースクリプトをインベントリーディレクトリー (デフォルトでは ``etc/ansible/hosts``) に追加することで暗黙的に使用することもできます。詳細は、:ref:`dynamic_inventory` を参照してください。

.. seealso::

  `Infoblox Web サイト <https://www.infoblox.com//>`_
      Infoblox の Web サイト
  `Infoblox および Ansible デプロイメントガイド <https://www.infoblox.com/resources/deployment-guides/infoblox-and-ansible-integration>`_
      Infoblox が提供する Ansible 統合のデプロイメントガイド。
  `Ansible 2.5 での Infoblox 統合 <https://www.ansible.com/blog/infoblox-integration-in-ansible-2.5>`_
      Infoblox に関する Ansible ブログ投稿。
  :ref:`Ansible NIOS モジュール <nios_net tools_modules>`
      対応している NIOS モジュールの一覧 (サンプル例あり)
  `Infoblox Ansible のサンプル <https://github.com/network-automation/infoblox_ansible>`_
      Infoblox の Playbook サンプル
