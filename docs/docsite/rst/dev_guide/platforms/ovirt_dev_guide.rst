.. _oVirt_module_development:

oVirt Ansible モジュール
=====================

これは、oVirt/RHV と対話するためのモジュールセットです。本ガイドは、
oVirt/RHV モジュールを作成するための開発者コーディングガイドラインとして役立ちます。

.. contents::
   :local:

命名規則
------

-  すべてのモジュールは、``ovirt_`` 接頭辞で開始する必要があります。
-  すべてのモジュールは、
   管理するリソースにちなんで単数形で名前を付ける必要があります。
-  情報を収集するすべてのモジュールには、
   ``_info`` 接尾辞が必要です。

インターフェース
---------

-  すべてのモジュールは、管理するリソースの ID を返す必要があります。
-  すべてのモジュールは、管理するリソースのディレクトリーを返す必要があります。
-  後方互換性を保証するため、
   パラメーターの名前は変更しないでください。代わりにエイリアスを使用してください。
-  パラメーターが何らかの理由で冪等性を実現できない場合は、
   それを文書化してください。

相互運用性
----------------

-  すべてのモジュールは、
   API のバージョン 4 のすべてのマイナーバージョンに対して機能します。API のバージョン 3 には対応していません。

ライブラリー
---------

-  すべてのモジュールは、``ovirt_full_argument_spec`` または 
   ``ovirt_info_full_argument_spec`` を使用して標準入力を選択します (
   auth、``fetch_nested`` など)。
-  すべてのモジュールは、``extends_documentation_fragment``: ovirt を、
   ``ovirt_full_argument_spec`` とともに使用する必要があります。
-  すべての情報モジュールは、``extends_documentation_fragment`` を使用する必要があります。
   ``ovirt_info`` は、``ovirt_info_full_argument_spec`` とともに使用します。
-  すべてのモジュールに共通する関数は、
   再使用できるように ``module_utils/ovirt.py`` ファイルに実装する必要があります。
-  Python SDK バージョン 4 を使用する必要があります。

新しいモジュール開発
----------------------

:ref:`developing_modules` ファイルを最初に読んで、
すべてのモジュールに共通のプロパティー、
関数、および機能を把握してください。

oVirt エンティティー属性の冪等性を実現するために、
ヘルパークラスが作成されました。最初に行う必要があるのは、
このクラスを拡張していくつかのメソッドをオーバーライドすることです。

.. code:: python

    try:
        import ovirtsdk4.types as otypes
    except ImportError:
        pass

    from ansible.module_utils.ovirt import (
        BaseModule,
        equal
    )

    class ClustersModule(BaseModule):

        # The build method builds the entity we want to create.
        # Always be sure to build only the parameters the user specified
        # in their yaml file, so we don't change the values which we shouldn't
        # change. If you set the parameter to None, nothing will be changed.
        def build_entity(self):
            return otypes.Cluster(
                name=self.param('name'),
                comment=self.param('comment'),
                description=self.param('description'),
            )

        # The update_check method checks if the update is needed to be done on
        # the entity. The equal method doesn't check the values which are None,
        # which means it doesn't check the values which user didn't set in yaml.
        # All other values are checked and if there is found some mismatch,
        # the update method is run on the entity, the entity is build by
        # 'build_entity' method. You don't have to care about calling the update,
        # it's called behind the scene by the 'BaseModule' class.
        def update_check(self, entity):
            return (
                equal(self.param('comment'), entity.comment)
                and equal(self.param('description'), entity.description)
            )

上記のコードは、エンティティーを更新する必要があるかどうかのチェックを処理するため、
不要な場合はエンティティーを更新せず、
必要な SDK のエンティティーを構築します。

.. code:: python

    from ansible.module_utils.basic import AnsibleModule
    from ansible.module_utils.ovirt import (
        check_sdk,
        create_connection,
        ovirt_full_argument_spec,
    )

    # This module will support two states of the cluster,
    # either it will be present or absent. The user can
    # specify three parameters: name, comment and description,
    # The 'ovirt_full_argument_spec' function, will merge the
    # parameters created here with some common one like 'auth':
    argument_spec = ovirt_full_argument_spec(
        state=dict(
            choices=['present', 'absent'],
            default='present',
        ),
        name=dict(default=None, required=True),
        description=dict(default=None),
        comment=dict(default=None),
    )

    # Create the Ansible module, please always implement the
    # feautre called 'check_mode', for 'create', 'update' and
    # 'delete' operations it's implemented by default in BaseModule:
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    # Check if the user has Python SDK installed:
    check_sdk(module)

    try:
        auth = module.params.pop('auth')

        # Create the connection to the oVirt engine:
        connection = create_connection(auth)

        # Create the service which manages the entity:
        clusters_service = connection.system_service().clusters_service()

        # Create the module which will handle create, update and delete flow:
        clusters_module = ClustersModule(
            connection=connection,
            module=module,
            service=clusters_service,
        )

        # Check the state and call the appropriate method:
        state = module.params['state']
        if state == 'present':
            ret = clusters_module.create()
        elif state == 'absent':
            ret = clusters_module.remove()

        # The return value of the 'create' and 'remove' method is dictionary
        # with the 'id' of the entity we manage and the type of the entity
        # with filled in attributes of the entity. The 'change' status is
        # also returned by those methods:
        module.exit_json(**ret)
    except Exception as e:
        # Modules can't raises exception, it always must exit with
        # 'module.fail_json' in case of exception. Always use
        # 'exception=traceback.format_exc' for debugging purposes:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        # Logout only in case the user passed the 'token' in 'auth'
        # parameter:
        connection.close(logout=auth.get('token') is None)

モジュールがアクション処理 (たとえば、仮想マシンの起動) 
に対応する必要がある場合は、
仮想マシンの状態を正しく処理し、
モジュールの動作を文書化する必要があります。

.. code:: python

        if state == 'running':
            ret = vms_module.action(
                action='start',
                post_action=vms_module._post_start_action,
                action_condition=lambda vm: (
                    vm.status not in [
                        otypes.VmStatus.MIGRATING,
                        otypes.VmStatus.POWERING_UP,
                        otypes.VmStatus.REBOOT_IN_PROGRESS,
                        otypes.VmStatus.WAIT_FOR_LAUNCH,
                        otypes.VmStatus.UP,
                        otypes.VmStatus.RESTORING_STATE,
                    ]
                ),
                wait_condition=lambda vm: vm.status == otypes.VmStatus.UP,
                # Start action kwargs:
                use_cloud_init=use_cloud_init,
                use_sysprep=use_sysprep,
                # ...
            )

前述の例から分かるように、``action`` メソッドでは、``action_condition`` および 
``wait_condition`` を使用できます。
これは、仮想マシンオブジェクトをパラメーターとして受け入れるメソッドであるため、
アクションの前に仮想マシンが適切な状態にあるかどうかを確認できます。パラメーターの残りの部分は、
``start`` アクション用です。``pre_action`` パラメーターおよび ``post_action`` 
パラメーターを定義して、
アクション前またはアクション後のタスクを処理することもできます。

テスト
-------

-  統合テストは現在、
   `Jenkins <https://jenkins.ovirt.org/view/All/job/ovirt-system-tests_ansible-suite-master/>`__ 
   および
   `GitHub <https://github.com/oVirt/ovirt-system-tests/tree/master/ansible-suite-master/>`__ の oVirt の CI システムで行われています。
-  新しいモジュールを作成する場合、または既存のモジュールに新しい機能を追加する場合は、
   この統合テストの使用を検討してください。
