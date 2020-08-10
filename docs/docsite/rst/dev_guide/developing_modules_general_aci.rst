.. _aci_dev_guide:

****************************
Cisco ACI モジュールの開発 
****************************
Ansible 向けに新しい Cisco ACI モジュールを作成する方法に関する簡単なウォークスルーです。

Cisco ACI の詳細は「:ref:`Cisco ACI ユーザーガイド <aci_guide>`」を参照してください。

本項で取り上げられている内容:

.. contents::
   :depth: 3
   :local:


.. _aci_dev_guide_intro:

はじめに
============
Ansible にはすでに Cisco ACI モジュールの大規模なコレクションが同梱されていますが、ACI のオブジェクトモデルは膨大なものであり、可能な機能にすべて対応するには、1500 個以上のモジュールに簡単に対応できなければなりません。

特定の機能が必要な場合は、2 つのオプションがあります。

- ACI オブジェクトモデルを学習し、「:ref:`aci_rest` <aci_rest_module>」モジュールを使用して低レベルの APIC REST API を使用します。
- 独自の専用モジュールを作成することは、実際には非常に簡単です。

.. seealso::

   `ACI の基本: ACI ポリシー <https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/1-x/aci-fundamentals/b_ACI-Fundamentals/b_ACI-Fundamentals_chapter_010001.html>モデル`
       ACI オブジェクトモデルの優れた概要。
   `APIC 管理情報モデル参照 <https://developer.cisco.com/docs/apic-mim-ref/>`_
       APIC オブジェクトモデルの完全なリファレンス。
   `APIC REST API 設定ガイド <https://www.cisco.com/c/en/us/td/docs/switches/datacenter/aci/apic/sw/2-x/rest_cfg/2_1_x/b_Cisco_APIC_REST_API_Configuration_Guide.html>`_
       APIC REST API を設計および使用する方法についての詳細ガイドです。多数の例があります。


それでは、典型的な ACI モジュールがどのように構築されるかを見てみましょう。


.. _aci_dev_guide_module_structure:

ACI モジュール構造
====================

Python ライブラリーからのオブジェクトのインポート
---------------------------------------
以下のインポートは、ACI モジュール全体で標準のものです。

.. code-block:: python

    from ansible.module_utils.aci import ACIModule, aci_argument_spec
    from ansible.module_utils.basic import AnsibleModule


引数仕様の定義
--------------------------
最初の行は、標準の接続パラメーターをモジュールに追加します。その後、次のセクションでは、モジュール固有のパラメーターを使用して ``argument_spec`` ディクショナリーを更新します。モジュール固有のパラメーターには以下を含める必要があります。

* object_id (通常は名前)
* オブジェクトの設定可能なプロパティー
* 親オブジェクト ID (ルートまでのすべての親)
* 1 対 1 の関係である子クラスのみ (1 対多/多対多 では、独自のモジュールが適切に管理する必要があります)。
* 状態

  + ``state: absent`` (オブジェクトが存在しないことを確認する)
  + ``state: present`` (オブジェクトと設定が存在することを確認する (デフォルト))
  + ``state: query`` クラスのオブジェクトに関する情報を取得する

.. code-block:: python

    def main():
        argument_spec = aci_argument_spec()
        argument_spec.update(
            object_id=dict(type='str', aliases=['name']),
            object_prop1=dict(type='str'),
            object_prop2=dict(type='str', choices=['choice1', 'choice2', 'choice3']),
            object_prop3=dict(type='int'),
            parent_id=dict(type='str'),
            child_object_id=dict(type='str'),
            child_object_prop=dict(type='str'),
            state=dict(type='str', default='present', choices=['absent', 'present', 'query']),
        )


.. hint:: 設定引数のデフォルト値を指定しないでください。デフォルト値により、オブジェクトへの意図しない変更が生じる可能性があります。

AnsibleModule オブジェクトの使用
------------------------------
以下のセクションは、AnsibleModule インスタンスを作成します。モジュールはチェックモードをサポートする必要があるため、``argument_spec`` 引数および ``supports_check_mode`` 引数を渡します。これらのモジュールは、モジュールのクラスのすべてのオブジェクトに対する APIC のクエリーをサポートするため、オブジェクト/親 ID は ``state: absent`` または ``state: present`` の場合に限り必要になります。

.. code-block:: python

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=[
            ['state', 'absent', ['object_id', 'parent_id']],
            ['state', 'present', ['object_id', 'parent_id']],
        ],
    )
    

マッピング変数定義
---------------------------
AnsibleModule オブジェクトが開始したら、必要なパラメーター値を ``params`` から抽出し``、データ検証を行う必要があります。通常、抽出する必要があるパラメーターは ACI オブジェクト設定およびその子設定に関連するパラメーターのみです。検証する整数オブジェクトがある場合、ここで検証を行う必要があります。``ACIModule.payload()`` メソッドは文字列変換を処理します。

.. code-block:: python

    object_id = object_id
    object_prop1 = module.params['object_prop1']
    object_prop2 = module.params['object_prop2']
    object_prop3 = module.params['object_prop3']
    if object_prop3 is not None and object_prop3 not in range(x, y):
        module.fail_json(msg='Valid object_prop3 values are between x and (y-1)')
    child_object_id = module.params[' child_objec_id']
    child_object_prop = module.params['child_object_prop']
    state = module.params['state']


ACIModule オブジェクトの使用
--------------------------
ACIModule クラスは、ACI モジュールのロジックの大部分を処理します。ACIModule は機能を AnsibleModule オブジェクトに拡張するため、モジュールインスタンスをクラスのインスタンス化に渡す必要があります。

.. code-block:: python

    aci = ACIModule(module)

ACIModule には、モジュールによって使用される 6 つの主なメソッドがあります。

* construct_url
* get_existing
* payload
* get_diff
* post_config
* delete_config

最初の 2 つのメソッドは、``state`` パラメーターに渡される値に関係なく使用されます。

URL の構築
^^^^^^^^^^^^^^^^^
``construct_url()`` メソッドは、オブジェクトと対話するために適切な URL と、URL に追加して結果にフィルターを設定する適切なフィルター文字列を動的にビルドするために使用されます。

* ``state`` が ``query`` でない場合、URL は APIC にアクセスするベース URL とオブジェクトにアクセスするための識別名です。フィルター文字列は返されたデータを設定データにのみ制限します。
* ``state`` が ``query`` される場合、使用される URL およびフィルター文字列は、オブジェクトに渡されるパラメーターによって異なります。この方法は複雑性を処理するため、新しいモジュールの追加が容易になります。また、すべてのモジュールがどのタイプのデータを返すかに一貫性を持たせるようにします。

.. note:: 設計目標は、値を持つすべての ID パラメーターを取り、可能な限り最も具体的なデータを返すことです。タスクに ID パラメーターを指定しないと、クラスのすべてのオブジェクトが返されます。タスクが ID パラメーターで構成されている場合は、特定のオブジェクトのデータが返されます。ID パラメーターの一部が渡されると、モジュールは URL およびフィルター文字列を適切にビルドするために渡された ID を使用します。

``construct_url()`` メソッドは 2 つの必須引数を取ります。

* **self** - クラスインスタンスで自動的に渡されます。
* **root_class** - ``aci_class`` キー、``aci_rn`` キー、``target_filter`` キー、および ``module_object`` キーで構成されるディクショナリー

  + **aci_class** - APIC で使用されるクラスの名前 (例: ``fvTenant``)

  + **aci_rn** - オブジェクトの相対名 (例: ``tn-ACME``)。

  + **target_filter** - エントリーのサブセットを選択するクエリー文字列を構成するキーと値のペアを持つディクショナリー (例: ``{'name': 'ACME'}``)

  + **module_object** - このクラスの特定のオブジェクト (例: ``ACME``)

例: 

.. code-block:: python

    aci.construct_url(
        root_class=dict(
            aci_class='fvTenant',
            aci_rn='tn-{0}'.format(tenant),
            target_filter={'name': tenant},
            module_object=tenant,
        ),
    )

``aci_tenant`` などの一部のモジュールは root クラスであるため、メソッドに追加の引数を渡す必要はありません。

``construct_url()`` メソッドは、4 つの任意の引数を取ります。最初の 3 つの引数が上記のように root クラスを模倣しますが、これは子オブジェクト用です。

* subclass_1 - ``aci_class`` キー、``aci_rn`` キー、``target_filter`` キー、および ``module_object`` キーで構成されるディクショナリー

  + 例: Application Profile Class (AP)

* subclass_2 - ``aci_class`` キー、``aci_rn`` キー、``target_filter`` キー、および ``module_object`` キーで構成されるディクショナリー

  + 例: エンドポイントグループ (EPG)

* subclass_3 - ``aci_class`` キー、``aci_rn`` キー、``target_filter`` キー、および``module_object`` キーで構成されるディクショナリー

  + 例: EPG への契約のバインド

* child_classes - モジュールがサポートする子クラスの APIC 名のリスト。

  + 1 つのリストであっても、これはリストです
  + これらは、APIC が使用する分かりにくい名前です。
  + 可能な場合は、返された child_classes を制限するために使用されます。
  + 例: ``child_classes=['fvRsBDSubnetToProfile', 'fvRsNdPfxPol']``

.. note:: APIC は、特殊文字 ([、]、および -) を要求したり、名前にオブジェクトのメタデータ (「VLAN」プールの場合は「vlanns」) を使用したりすることがあります。モジュールは、予想される入力の単純さに保つために、特殊文字の追加または複数のパラメーターの結合を処理する必要があります。

既存設定の取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
URL およびフィルター文字列が構築されると、モジュールはオブジェクトの既存の設定を取得できるようになります。

* ``state: present`` は、タスクで入力された比較に使用する設定を取得します。既存の値と異なるすべての値は更新されます。
* ``state: absent`` は、既存の設定を使用して項目が存在し、削除する必要があるかどうかを確認します。
* ``state: query`` は、これを使用してタスクのクエリーを実行し、既存のデータを報告します。

.. code-block:: python

    aci.get_existing()


state が present の場合
^^^^^^^^^^^^^^^^^^^^^
``state: present`` の場合、モジュールは既存の設定とタスクエントリーに対して diff を実行する必要があります。値を更新する必要がある場合、モジュールは更新が必要な項目のみを持つ POST 要求を行います。一部のモジュールには、別のオブジェクトと 1 対 1 の関係にある子があります。このような場合は、モジュールを使用して子オブジェクトを管理できます。

ACI ペイロードの構築
""""""""""""""""""""""""
``aci.payload()`` メソッドは、提案されたオブジェクト設定のディクショナリーを構築するために使用されます。タスクの値を提供しなかったパラメーターはすべて、ディクショナリー (オブジェクトとその子の両方) から削除されます。値を持つパラメーターは文字列に変換され、既存の設定と比較するために使用される最後のディクショナリーオブジェクトに追加されます。

``aci.payload()`` メソッドは、モジュールが子オブジェクトを管理するかどうかに応じて、2 つの必須引数と、1 つの任意の引数を取ります。

* ``aci_class`` はオブジェクトのクラスの APIC 名です (例: ``aci_class='fvBD'``)。
* ``class_config`` は POST 要求のペイロードとして使用する適切なディクショナリーです。

  + キーは APIC で使用される名前と一致する必要があります。
  + 値は ``module.params`` の対応する値である必要があります。これらは上記の変数です。

* ``child_configs`` は任意で、子設定のディクショナリーのリストです。

  + 子設定には、属性設定部分だけでなく、完全な子オブジェクトディクショナリーが含まれます。
  + 設定部分は、オブジェクトと同じ方法で構築されます。

.. code-block:: python

    aci.payload(
        aci_class=aci_class,
        class_config=dict(
            name=bd,
            descr=description,
            type=bd_type,
        ),
        child_configs=[
            dict(
                fvRsCtx=dict(
                    attributes=dict(
                        tnFvCtxName=vrf
                    ),
                ),
            ),
        ],
    )
    

要求の実行
""""""""""""""""""""""
``get_diff()`` メソッドは diff の実行に使用され、必要な引数 ``aci_class`` を 1 つだけ取ります。
例: ``aci.get_diff(aci_class='fvBD')``

``post_config()`` メソッドは、必要に応じて APIC に対して POST 要求を実行するために使用されます。この方法は引数を取らず、チェックモードを処理します。
例: ``aci.post_config()``


サンプルコード
""""""""""""
.. code-block:: guess

    if state == 'present':
        aci.payload(
            aci_class='<object APIC class>',
            class_config=dict(
                name=object_id,
                prop1=object_prop1,
                prop2=object_prop2,
                prop3=object_prop3,
            ),
            child_configs=[
                dict(
                    '<child APIC class>'=dict(
                        attributes=dict(
                            child_key=child_object_id,
                            child_prop=child_object_prop
                        ),
                    ),
                ),
            ],
        )

        aci.get_diff(aci_class='<object APIC class>')

        aci.post_config()
    

state が absent の場合
^^^^^^^^^^^^^^^^^^^^
タスクが state を absent に設定すると、``delete_config()`` メソッドのみが必要になります。このメソッドは引数を取らず、チェックモードを処理します。

.. code-block:: guess

        elif state == 'absent':
            aci.delete_config()


モジュールの終了
^^^^^^^^^^^^^^^^^^
モジュールを終了するには、ACIModule メソッドの ``exit_json()`` を呼び出します。このメソッドでは、自動的に一般的な戻り値が返されます。

.. code-block:: guess

        aci.exit_json()

    if __name__ == '__main__':
        main()


.. _aci_dev_guide_testing:

ACI ライブラリー関数のテスト
=============================
以下の python スクリプトを使用すると、APIC ハードウェアにアクセスしなくても ``construct_url()`` 引数および ``payload()`` 引数をテストできます。

.. code-block:: guess

    #!/usr/bin/python
    import json
    from ansible.module_utils.network.aci.aci import ACIModule

    # Just another class mimicing a bare AnsibleModule class for construct_url() and payload() methods
    class AltModule():
        params = dict(
            host='dummy',
            port=123,
            protocol='https',
            state='present',
            output_level='debug',
        )

    # A sub-class of ACIModule to overload __init__ (we don't need to log into APIC)
    class AltACIModule(ACIModule):
        def __init__(self):
            self.result = dict(changed=False)
            self.module = AltModule()
            self.params = self.module.params

    # Instantiate our version of the ACI module
    aci = AltACIModule()

    # Define the variables you need below
    aep = 'AEP'
    aep_domain = 'uni/phys-DOMAIN'

    # Below test the construct_url() arguments to see if it produced correct results
    aci.construct_url(
        root_class=dict(
            aci_class='infraAttEntityP',
            aci_rn='infra/attentp-{}'.format(aep),
            target_filter={'name': aep},
            module_object=aep,
        ),
        subclass_1=dict(
            aci_class='infraRsDomP',
            aci_rn='rsdomP-[{}]'.format(aep_domain),
            target_filter={'tDn': aep_domain},
            module_object=aep_domain,
        ),
    )

    # Below test the payload arguments to see if it produced correct results
    aci.payload(
        aci_class='infraRsDomP',
        class_config=dict(tDn=aep_domain),
    )

    # Print the URL and proposed payload
    print 'URL:', json.dumps(aci.url, indent=4)
    print 'PAYLOAD:', json.dumps(aci.proposed, indent=4)


これにより、以下が生成されます。

.. code-block:: yaml

    URL: "https://dummy/api/mo/uni/infra/attentp-AEP/rsdomP-[phys-DOMAIN].json"
    PAYLOAD: {
        "infraRsDomP": {
            "attributes": {
                "tDn": "phys-DOMAIN"
            }
        }
    }

健全性チェックのテスト
-------------------------
次のようなフォークから実行できます。

.. code-block:: bash

    $ ansible-test sanity --python 2.7 lib/ansible/modules/network/aci/aci_tenant.py

.. seealso::

   :ref:`testing_sanity`
        健全性テストを構築する方法に関する情報


ACI 統合テストのテスト
-----------------------------
以下を実行できます。

.. code-block:: bash

    $ ansible-test network-integration --continue-on-error --allow-unsupported --diff -v aci_tenant

.. note:: テストの実行に適切な python バージョンを使用するには、``--python 2.7`` または ``--python 3.6`` を追加しないといけない場合があります。

*test/integration/inventory.networking* で使用されたインベントリーを編集し、以下のように追加することもできます。

.. code-block:: ini

    [aci:vars]
    aci_hostname=my-apic-1
    aci_username=admin
    aci_password=my-password
    aci_use_ssl=yes
    aci_use_proxy=no

    [aci]
    localhost ansible_ssh_host=127.0.0.1 ansible_connection=local

.. seealso::

   :ref:`testing_integration`
       インテグレーションテストの構築方法に関する情報。


テストカバレージのテスト
-------------------------
以下を実行できます。

.. code-block:: bash

    $ ansible-test network-integration --python 2.7 --allow-unsupported --coverage aci_tenant
    $ ansible-test coverage report
