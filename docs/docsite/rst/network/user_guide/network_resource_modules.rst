.. _resource_modules:

************************
ネットワークリソースモジュール
************************

Ansible 2.9 では、さまざまなネットワークデバイスの管理を単純化し、標準化するネットワークリソースモジュールが導入されました。


.. contents::
   :local:

ネットワークリソースモジュールの概要
=======================================

ネットワークデバイスは、設定を、ネットワークサービスに適用するセクション (インターフェース、VLAN など) に分割します。Ansible ネットワークリソースモジュールは、これを利用してネットワークデバイス設定内のサブセクションや *リソース* の設定を可能にします。ネットワークリソースモジュールは、ネットワークデバイスが異なっても、ユーザーが体験する内容は同じになります。


ネットワークリソースモジュールの状態
===============================

ネットワークリソースモジュールを使用するには、モジュールの実行内容に状態を割り当てます。リソースモジュールは以下の状態に対応します。

merged
  Ansible は、デバイス上の設定をタスクに指定した設定と統合します。

replaced
  Ansible が、デバイス上の設定のサブセクションを、タスクに指定した設定のサブセクションに置き換えます。

overridden
  Ansible は、タスクに指定した設定で、リソースに対するデバイス上の設定を上書きします。デバイスへのアクセスを削除できるため (たとえば、管理インターフェースの設定を上書きするなど)、この状態には注意してください。

deleted
  Ansible は、デバイス上の設定サブセクションを削除して、デフォルト設定を復元します。

gathered
  Ansible は、ネットワークデバイスから収集したリソースの詳細を表示し、結果の ``gathered`` キーでアクセスします。

rendered
  Ansible は、デバイスネイティブ形式 (Cisco IOS CLI など) のタスクで指定される設定をレンダリングします。Ansible は、このレンダリングされた設定を、結果の ``rendered`` キーで返します。この状態はネットワークデバイスと通信せず、オフラインで使用できることに注意してください。

parsed
  Ansible は、``running_configuration`` オプションから、結果の ``parsed`` キーに含まれる Ansible 構造化データに設定を解析します。この状態はオフラインで使用できるように、ネットワークデバイスから設定を収集しないことに注意してください。

ネットワークリソースモジュールの使用
==============================

この例では、異なる状態設定に基づいて、Cisco IOS デバイスで L3 インターフェースリソースを設定します。

 .. code-block:: YAML

   - name: configure l3 interface
     ios_l3_interfaces:
       config: "{{ config }}"
       state: <state>

以下の表は、このタスクをさまざまな状況で変更した最初のリソースの設定の例を示しています。

+-----------------------------------------+------------------------------------+-----------------------------------------+
| リソースの開始設定         | タスクが指定する設定 (YAML) | デバイスでの最終的なリソース設定  |
+=========================================+====================================+=========================================+
| .. code-block:: text                    |  .. code-block:: yaml              | *merged*                                |
|                                         |                                    |  .. code-block:: text                   |
|   interface loopback100                 |   config:                          |                                         |
|    ip address 10.10.1.100 255.255.255.0 |   - ipv6:                          |    interface loopback100                |
|    ipv6 address FC00:100/64             |    - address: fc00::100/64         |     ip address 10.10.1.100 255.255.255.0|
|                                         |    - address: fc00::101/64         |     ipv6 address FC00:100/64            |
|                                         |    name: loopback100               |     ipv6 address FC00:101/64            |
|                                         |                                    +-----------------------------------------+
|                                         |                                    | *replaced*                              |
|                                         |                                    |  .. code-block:: text                   |
|                                         |                                    |                                         |
|                                         |                                    |   interface loopback100                 |
|                                         |                                    |    no ip address                        |
|                                         |                                    |    ipv6 address FC00:100/64             |
|                                         |                                    |    ipv6 address FC00:101/64             |
|                                         |                                    +-----------------------------------------+
|                                         |                                    | *overridden*                            |
|                                         |                                    |  誤った使用例。これは、デバイスから  |
|                                         |                                    |  すべてのインターフェースを削除します。         |
|                                         |                                    | (mgmt インターフェースを含む) 以下を除く   |
|                                         |                                    |  設定されている loopback100             |
|                                         |                                    +-----------------------------------------+
|                                         |                                    | *deleted*                               |
|                                         |                                    |  .. code-block:: text                   |
|                                         |                                    |                                         |
|                                         |                                    |   interface loopback100                 |
|                                         |                                    |    no ip address                        |
+-----------------------------------------+------------------------------------+-----------------------------------------+

ネットワークリソースモジュールは、以下の詳細を返します。

* *before* 状態 - タスクが実行する前の既存リソース設定。
* *after* 状態 - タスク実行後にネットワークデバイスに存在する新しいリソース設定。
* Commands - このデバイスに設定されるすべてのコマンド

.. code-block:: yaml

   ok: [nxos101] =>
     result:
       after:
         contact:IT Support
         location:Room E, Building 6, Seattle, WA 98134
         users:
         - algorithm: md5
           group: network-admin
           localized_key: true
           password:'0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           privacy_password:'0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           username: admin
       before:
         contact:IT Support
         location:Room E, Building 5, Seattle HQ
         users:
         - algorithm: md5
           group: network-admin
           localized_key: true
           password:'0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           privacy_password:'0x73fd9a2cc8c53ed3dd4ed8f4ff157e69'
           username: admin
       changed: true
       commands:
       - snmp-server location Room E, Building 6, Seattle, WA 98134
       failed: false


例:ネットワークデバイス設定が変更されていないことを確認
====================================================================

以下の Playbook は、:ref:`eos_l3_interfaces <eos_l3_interfaces_module>` モジュールを使用してネットワークデバイス設定のサブセット (レイヤー 3 インターフェースのみ) を収集し、情報が正確であり、変更されていないことを確認します。この Playbook は、:ref:`eos_facts <eos_facts_module>` の結果を、``eos_l3_interfaces`` モジュールに直接渡します。


.. code-block:: yaml

  - name:Example of facts being pushed right back to device.
    hosts: arista
    gather_facts: false
    tasks:
      - name: grab arista eos facts
        eos_facts:
          gather_subset: min
          gather_network_resources: l3_interfaces

  - name:Ensure that the IP address information is accurate.
    eos_l3_interfaces:
      config: "{{ ansible_network_resources['l3_interfaces'] }}"
      register: result

  - name:Ensure config did not change.
    assert:
      that: not result.changed

.. seealso::

  `Ansible 2.9 のネットワーク機能 <https://www.ansible.com/blog/network-features-coming-soon-in-ansible-engine-2.9>`_
    ネットワークリソースモジュールに関する入門ブログの投稿。
  `ネットワークリソースモジュールの詳細 <https://www.ansible.com/deep-dive-into-ansible-network-resource-module>`_
    ネットワークリソースモジュールの詳細な説明
