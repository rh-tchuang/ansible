.. _meraki_guide:

******************
Cisco Meraki ガイド
******************

.. contents::
   :local:


.. _meraki_guide_intro:

Cisco Meraki とは
=====================

Cisco Meraki は、エンタープライズ環境向けクラウドベースの使いやすいネットワークインフラストラクチャープラットフォームです。ほとんどのネットワークハードウェアは設定にコマンドラインインターフェース (CLI) を使用しますが、Meraki は、Meraki クラウドでホストされる使いやすいダッシュボードを使用します。オンプレミスの管理ハードウェアやソフトウェアは必要ありません。ビジネスを実行するためのネットワークインフラストラクチャーのみが必要になります。

MS スイッチ
-----------

Meraki MS スイッチには、フレーバーとフォーム要素が複数あります。Meraki スイッチは、10/100/1000/10000 ポートと、2.5/5/10Gbps のカッパー接続用である Cisco 社の mGig テクノロジーに対応しています。8、24、および 48 のポートフレーバーは、多くのモデルで利用可能な PoE (802.3af/802.3at/UPoE) で利用できます。

MX ファイアウォール
------------

Meraki の MX ファイアウォールは、レイヤー 3 ~ 7 のディープパケット検査に完全に対応しています。MX ファイアウォールは、IPsec、SSL VPN、および Meraki の使いやすい AutoVPN など、さまざまな VPN テクノロジーと互換性があります。

MR ワイヤレスアクセスポイント
-------------------------

MR アクセスポイントは、エンタープライズ向けで高パフォーマンスのアクセスポイントです。MRアクセスポイントには、高性能アプリケーション向けに、MIMO テクノロジーと統合ビームフォーマーが組み込まれています。BLE を使用すると、オンプレミスのアナリティクスプラットフォームを使用せずに高度な位置情報アプリケーションを開発できます。

Meraki モジュールの使用
========================

Meraki モジュールは、Ansible を使用して Meraki 環境を管理するユーザーフレンドリーなインターフェースを提供します。たとえば、特定の組織の SNMP 設定の詳細は、`meraki_snmp <meraki_snmp_module>` を使用して確認できます。

.. code-block:: yaml

    - name:Query SNMP settings
      meraki_snmp:
        api_key: abc123
        org_name:AcmeCorp
        state: query
      delegate_to: localhost

特定のオブジェクトの情報はクエリーできます。たとえば、`meraki_admin <meraki_admin_module>` モジュールのサポートです。

.. code-block:: yaml

    - name:Gather information about Jane Doe
      meraki_admin:
        api_key: abc123
        org_name:AcmeCorp
        state: query
        email: janedoe@email.com
      delegate_to: localhost

一般的なパラメーター
=================

すべての Ansible Meraki モジュールは、Meraki Dashboard API との通信に影響する以下のパラメーターに対応します。これらのほとんどは Meraki 開発者が使用するためのものです。一般的には使用しないでください。

    host
        Meraki Dashboard のホスト名または IP。

    use_https
        通信が HTTPS 経由で行われるべきかどうかを指定します。(``yes`` にデフォルト設定)

    use_proxy
        通信にプロキシーを使用するかどうか。

    validate_certs
        証明書を検証するか、または信頼するかを決定します。(``yes`` にデフォルト設定)

以下は、大抵のモジュールに使用される一般的なパラメーターです。

    org_name
        アクションを実行する組織の名前。

    org_id
        アクションを実行する組織の ID。

    net_name
        アクションを実行するネットワークの名前。

    net_id
        アクションを実行するネットワークの ID。

    state
        実行するアクションの一般的な仕様。「query」はルックアップを行います。「present」は作成または編集を行い、「absent」は削除を行います。

.. hint:: 可能な場合は、``org_id`` パラメーターおよび ``net_id`` パラメーターを使用します。``org_name`` と ``net_name`` には、ID 値を学習するために裏で実行する追加の API 呼び出しが必要です。``org_id`` と ``net_id`` の方がパフォーマンスが高くなります。 

Meraki 認証
=====================

Meraki Dashboard を使用した API アクセスにはすべて API キーが必要です。API キーは、組織の設定ページから生成できます。Playbook の各プレイには ``api_key`` パラメーターを指定する必要があります。

Ansible の「Vault」機能を使用すると、パスワードやキーなどの機密データを、Playbook やロールのプレーンテキストとしてではなく、暗号化されたファイルに保存できます。この vault ファイルは、ソース制御に配布または配置することができます。詳細は「:ref:`playbooks_vault`」を参照してください。

API キーが正しくないと、Meraki の API は 404 エラーを返します。このキーが正しくないことを示す特別なエラーはありません。404 エラーを受け取った場合は、最初に API キーを確認してください。

返されたデータ構造
========================

Meraki およびその関連する Ansible モジュールは、リストの形式でほとんどの情報を返します。たとえば、これは、管理者のクエリーを行う ``meraki_admin`` により情報を返します。リストが 1 つしかなくても、リストを返します。

.. code-block:: json

    [
        {
            "orgAccess": "full", 
            "name": "John Doe",
            "tags": [],
            "networks": [],
            "email": "john@doe.com",
            "id": "12345677890"
        }
    ]
    
返されたデータの処理
======================

Meraki の応答データは、応答に対して適切にキー付けされたディクショナリーの代わりにリストを使用するため、特定の情報についてデータのクエリーを行う際には、特定のストラテジーを使用する必要があります。多くの状況では、Jinja2 関数 ``selectattr()`` を使用してください。

既存データと新規データのマージ
=============================

Ansible の Meraki モジュールは、データの操作を許可しません。たとえば、ファイアウォールのルールセットの途中にルールを挿入しないといけない場合があります。Ansible モジュールおよび Meraki モジュールには、データを操作するために直接マージする方法がありません。ただし、プレイリストでいくつかのタスクを使用して、ルールを挿入し、新しいルールを追加して再びマージする必要があるリストを分割できます。関係する手順は以下のとおりです。

1. 空の「前」リストおよび「後」リストを作成します
    ::

        vars:
          - front_rules: []
          - back_rules: []
2. Meraki から既存のファイアウォールルールを取得して、新しい変数を作成します
    ::

        - name:Get firewall rules
          meraki_mx_l3_firewall:
            auth_key: abc123
            org_name:YourOrg
            net_name:YourNet
            state: query
          delegate_to: localhost
          register: rules
        - set_fact:
            original_ruleset: '{{rules.data}}'
3. 新しいルールを作成します。新しいルールは、以降の手順で他のリストにマージできるように、リストに記載する必要があります。空白 `-` により、マージするルールがリストに追加されます
    ::

        - set_fact:
            new_rule:
              - 
                - comment:Block traffic to server
                  src_cidr:192.0.1.0/24
                  src_port: any
                  dst_cidr:192.0.1.2/32
                  dst_port: any
                  protocol: any
                  policy: deny
4. ルールを複数のリストに分割します。ここでは、既存のルールセットが 2 つのルールの長さであることを前提とします
    ::

        - set_fact:
            front_rules: '{{front_rules + [ original_ruleset[:1] ]}}'
        - set_fact:
            back_rules: '{{back_rules + [ original_ruleset[1:] ]}}'
5. ルールを、中間の新しいルールとマージします
    ::

        - set_fact:
            new_ruleset: '{{front_rules + new_rule + back_rules}}'
6. 新しいルールセットを Meraki にアップロードします
    ::

        - name:Set two firewall rules
          meraki_mx_l3_firewall:
            auth_key: abc123
            org_name:YourOrg
            net_name:YourNet
            state: present
            rules: '{{ new_ruleset }}'
          delegate_to: localhost

エラー処理
==============

Ansible の Meraki モジュールは、不適切なパラメーターや互換性のないパラメーターが指定されている場合に失敗することがよくあります。ただし、モジュールが情報を受け入れても Meraki API がデータを拒否する場合があります。これが発生すると、HTTP ステータス 400 戻りコードのエラーが ``body`` フィールドに返されます。

API キーが正しくないと、Meraki の API は 404 エラーを返します。このキーが正しくないことを示す特別なエラーはありません。404 エラーを受け取った場合は、最初に API キーを確認してください。404 エラーは、不適切なオブジェクト ID (``org_id`` など) が指定されている場合も発生します。
