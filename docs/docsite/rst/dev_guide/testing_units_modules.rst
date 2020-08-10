:orphan:

.. _testing_units_modules:

****************************
Ansible モジュールのユニットテスト
****************************

.. highlight:: python

.. contents:: トピック

はじめに
============

本ドキュメントは、なぜ、どのように、いつ Ansible モジュールのユニットテストを使用すべきかを説明します。
このドキュメントは、Ansible の他の部分には適用されませんが、
推奨事項は、通常、Python の標準仕様と似ています。 Ansible のユニットテストについては、
開発者ガイドの「:ref:`testing_units`」に基本的な説明があります。 このドキュメントは、
新たに Ansible モジュールを作成するユーザーが読めるようになっているはずです。もし不完全または分からない箇所がある場合は、
バグを登録するか、Ansible IRC で助けを求めてください。

ユニットテストとは
====================

Ansible には、:file:`test/units` ディレクトリーにユニットテストのセットが含まれています。これらのテストは主に Ansible そのものを対象としていますが、
Ansible のモジュールにも対応しています。 ユニットテストの構造はコードベースの構造と一致しているため、
:file:`test/units/modules/` ディレクトリーにあるテストは、
モジュールグループ別に整理されています。

統合テストはほとんどのモジュールに使用できますが、
統合テストではケースを検証できない場合もあります。 つまり、
Ansible のユニットテストケースは最小限のユニットのみをテストするだけにとどまらず、
場合によってはある程度のレベルにある機能テストを含むこともあります。


ユニットテストを使用する理由
===================

Ansibleのユニットテストには利点と欠点があります。これを理解することが重要です。
利点には以下のようなものがあります。

* ほとんどのユニットテストは、ほとんどの Ansible の統合テストよりもはるかに高速です。 ユニットテストの完全なスイートは、
  開発者が自身のローカルシステムで定期的に実行できます。
* ユニットテストは、
  モジュールが動作するように設計されているシステムにアクセスできない開発者が実行することができ、
  コア機能への変更がモジュールの期待どおりであることを検証できます。
* ユニットテストは、
  非現実的なソフトウェアのテストを可能にするシステム関数を簡単に置き換えることができます。 たとえば、``sleep()`` 関数を置き換えることができ、
  実際に 10 分間待つことなく 10 分間のスリープが呼び出されたかどうかを確認します。
* ユニットテストは、Python の各バージョンで実行されます。これにより、
  コードが異なる Python のバージョンでも同じように動作することを確認できます。

ユニットテストには、いくつかの潜在的な欠点もあります。ユニットテストは、
通常、実際に便利で価値のある機能を直接テストせず、
代わりに内部実装をテストします。

* ソフトウェア内部にある、見に見えない機能をテストするユニットテストは、
  それらの内部機能を変更しなければならない場合、
  リファクタリングを困難にする場合があります (下記の「方法」の命名も参照してください)。
* 内部機能が正常に動作していても、
  テストした内部コードと実際の結果との間に問題が発生する可能性があります。

通常、(Ansible YAML で記述される) Ansible 統合テストは、
ほとんどのモジュール機能に対してより良いテストを提供します。 これらのテストがすでに機能をテストしていて、
うまく機能している場合は、同じ領域をカバーするユニットテストを提供する意味はほとんどないかもしれません。

ユニットテストを使うタイミング
======================

ユニットテストが、
統合テストよりも適切な選択である状況はたくさんあります。たとえば、統合テストでテストすることが不可能なもの、遅いもの、
または非常に難しいものをテストすることです。

* 特定のネットワーク障害や例外のような、
  強制することができない稀な、奇妙な、およびランダムな状況を強制する
* 遅い設定 API の広範なテスト
* Shippable で実行されているメインの Ansible 継続的インテグレーションの一部として、
  統合テストを実行できない状況。



迅速なフィードバックの提供
------------------------

例: 
  rds_instance のテストケースの 1 つのステップには、
  最大 20 分 (Amazonで RDS インスタンスを作成する時間) かかる場合があります。 テスト実行は、
  全体で 1 時間以上かかることもあります。 16 個のユニットテストは、
  すべて 2 秒以内に実行を完了します。

ユニットテストでコードを実行できることで提供される時間が短いため、
そのテストが後で問題を発見しないことが多かったとしても、
モジュールのバグ修正を行う際にユニットテストを作成する価値があります。 基本的な目標として、すべてのモジュールは、
統合テストが完了するのを待つことなく、
簡単なケースで迅速なフィードバックを提供するユニットテストを少なくとも 1 つは用意すべきです。

外部インターフェースを正しく使用すること
-------------------------------------------

ユニットテストは、*最終的な出力が変更されない場合でも*、外部サービスの実行方法が仕様に合致しているか、
あるいは可能な限り効率的であるかを確認できます。

例: 
  パッケージマネージャーは、各パッケージを個別にインストールするよりも、
  複数のパッケージを一度にインストールする方がはるかに効率的であることが多くなります。最終的な結果は同じです。
  すべてのパッケージがインストールされるため、
  統合テストで効率性を検証することは困難です。模擬パッケージマネージャを提供し、
  それが一度に呼ばれることを検証するため、モジュール効率について価値のあるテストを構築できます。

もう 1 つの関連する用途は、
API が異なる挙動をするバージョンを持っている場合です。新しいバージョンで作業しているプログラマーが、新しい API バージョンで動作するようにモジュールを変更して、
意図せずに古いバージョンを壊してしまうことがあります。 この時、テストケースで、
古いバージョンの呼び出しが正しく行われるかどうかを確認すると、
この問題を回避するのに役立ちます。 このような状況では、テストケースの名前にバージョン番号を含めることが非常に重要です 
(下記の「`ユニットテストの命名`_」を参照してください。)

特定の設計テストの提供
--------------------------------

コードの特定の部分に対する要件を構築し、
その要件に合わせてコーディングすることで、ユニットテストは、時にはコードを改善し、
将来の開発者がそのコードを理解する _助けとなります_。

一方で、コードの内部実装の詳細をテストするユニットテストは、
ほとんどの場合、良いことよりも悪いことの方が多いです。 インストールするパッケージがリストに記載されているかどうかをテストすることは、
効率化のためにそのリストをディクショナリーに変更を加える必要があったときに、
将来の開発者の作業遅らせ、混乱させることになります。この問題は、テストの名前を明確にして、
将来の開発者がそのテストケースを削除することがすぐに分かるようにすることで多少は軽減できますが、
テストケースを完全に除外して、
モジュールの引数として提供されるすべてのパッケージをインストールするなど、コードの中で本当に価値のある機能をテストする方が良いことがよくあります。


Ansible モジュールをユニットテストする方法
================================

モジュールのユニットテストにはいくつかの手法があります。 ユニットテストのないほとんどのモジュールは、
テストを非常に困難にする方法で構造化されており
コードよりも多くの作業を必要とする非常に複雑なテストにつながる可能性があることに注意してください。 ユニットテストを効果的に使用すると、
コードを再構築することになるかもしれません。これは適していることが多く、
全体的にコードがより適切になります。適切な再構築により、コードがより明確になり、理解しやすくなります。


ユニットテストの命名
-----------------

ユニットテストは論理的な名前が必要です。テストされるモジュールで作業している開発者がテストケースを壊してしまった場合、
ユニットテストが何を対象としているのかが名前から簡単に分かるようにする必要があります。
ユニットテストが特定のソフトウェアや API のバージョンとの互換性を検証するように設計されている場合は、
ユニットテストの名前にバージョンを含めてください。

たとえば、``test_v2_state_present_should_call_create_server_with_name()`` は適切ですが、
``test_create_server()`` は適切ではありません。


モックの使用
------------

モックオブジェクト (https://docs.python.org/3/library/unittest.mock.html から) は、
特別なケースや難しいケースのユニットテストを構築するのに非常に便利ですが、
コーディングが複雑で紛らわしくなる場合があります。 モックの適切な使い方としては、
API をシミュレートすることが挙げられます。「six」場合、
python パッケージ「mock」は Ansible にバンドルされています ``import ansible.compat.tests.mock`` を使用してください)。例を参照してください。

モックオブジェクトで障害ケースを確実に可視化
----------------------------------------------------

:meth:`module.fail_json` のような関数は通常、実行を終了することが期待されます。モックモジュールオブジェクトを使用して実行すると、
モックは常に関数呼び出しから別のモックを返すため、
このようなことは起こりません。上記のように例外を発生させるようにモックを設定することもできますし、
各テストでこれらの関数が呼び出されていないことを主張することもできます。例::

  module = MagicMock()
  function_to_test(module, argument)
  module.fail_json.assert_not_called()

これは、メインモジュールを呼び出す場合だけでなく、
モジュールオブジェクトを取得するモジュール内の他のほとんどの関数を呼び出す場合にも適用されます。


実際のモジュールのモック化
----------------------------

実際のモジュールの設定は非常に複雑で (下記の `Passing Arguments`_ を参照)、
ほとんどの場合、モジュールを使用するほとんどの関数では必要なくなります。代わりに、モックオブジェクトをモジュールとして使用し、
テストしている関数に必要なモジュール属性を作成することができます。この場合、
モジュールの終了関数は、例外を発生させるか、
呼ばれていないことを確認するかのどちらかで、上記で述べたように特別な処理が必要になることに注意してください。例::

    class AnsibleExitJson(Exception):
        """Exception class to be raised by module.exit_json and caught by the test case"""
        pass

    # you may also do the same to fail json
    module = MagicMock()
    module.exit_json.side_effect = AnsibleExitJson(Exception)
    with self.assertRaises(AnsibleExitJson) as result:
        return = my_module.test_this_function(module, argument)
    module.fail_json.assert_not_called()
    assert return["changed"] == True
    
ユニットテストケースでの API 定義
-----------------------------------

API のインタラクションは通常、Ansible の統合テストセクションで定義されている機能テストを使用してテストするのがベストですが、
これは実際の API に対して実行されます。 ユニットテストの方が
適しているケースもいくつかあります。

API の仕様に対してモジュールを定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このケースは、Ansible が使用する API を提供しているが、
ユーザーの制御が及ばない Web サービスと対話するモジュールにとって特に重要です。

API からデータを返す呼び出しのカスタムエミュレーションを書くことで、
API の仕様で明確に定義されている機能のみが
メッセージに含まれていることを確認できます。 つまり、正しいパラメーターを使用しているかどうかを確認し、
それ以外は何も使用していないことを確認することができます。


*例: rds_instance ユニットテストでは、単純なインスタンスの状態が定義されています*::

    def simple_instance_list(status, pending):
        return {u'DBInstances': [{u'DBInstanceArn': 'arn:aws:rds:us-east-1:1234567890:db:fakedb',
                                  u'DBInstanceStatus': status,
                                  u'PendingModifiedValues': pending,
                                  u'DBInstanceIdentifier': 'fakedb'}]}
    
次に、これを使用して状態のリストを作成します。

    rds_client_double = MagicMock()
    rds_client_double.describe_db_instances.side_effect = [
        simple_instance_list('rebooting', {"a": "b", "c": "d"}),
        simple_instance_list('available', {"c": "d", "e": "f"}),
        simple_instance_list('rebooting', {"a": "b"}),
        simple_instance_list('rebooting', {"e": "f", "g": "h"}),
        simple_instance_list('rebooting', {}),
        simple_instance_list('available', {"g": "h", "i": "j"}),
        simple_instance_list('rebooting', {"i": "j", "k": "l"}),
        simple_instance_list('available', {}),
        simple_instance_list('available', {}),
    ]
    
これらの状態はモックオブジェクトからの戻り値として使用され、
``await`` 関数が RDS インスタンスがまだ設定を完了していないことを意味するすべての状態を確実に待機するようにします。
configuration::

   rds_i.await_resource(rds_client_double, "some-instance", "available", mod_mock,
                        await_pending=1)
   assert(len(sleeper_double.mock_calls) > 5), "await_pending didn't wait enough"

これを実行することで、
統合テストでは確実に誘発させることができないにもかかわらず、
現実には予測できないような、潜在的に異常なことが起こる可能性がある場合に ``await`` 関数が待機し続けるかどうかをチェックしています。

複数の API バージョンに対して動作するモジュールの定義
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

このケースは、
相互作用するソフトウェアのバージョンがいくつも異なるモジュールにとって特に重要です。
たとえば、多数のバージョンのオペレーティングシステムで動作することが予想されるパッケージインストールモジュールなどです。

様々なバージョンの API から、以前に保存されたデータを使用することで、
バージョンが非常に曖昧でテスト中に利用できそうにない場合でも、
そのバージョンのシステムから送信される実際のデータに対してコードがテストされることを確実にすることができます。

Ansible ユニットテストの特殊なケース
======================================

Ansible モジュールの環境に対してユニットテストするための特別なケースがいくつかあります。
最も一般的なものを以下に示します。その他の提案については、
既存のユニットテストのソースコードを確認したり、
Ansible の IRC チャンネルやメーリングリストで質問してください。

モジュール引数処理
--------------------------

モジュールの主な関数の実行には、以下の 2 つの問題があります。

* モジュールは ``STDIN`` で引数を受け入れる必要があるため、
  引数を正しく設定してモジュールがパラメーターとして受け取るようにするのは少し難しくなります。
* すべてのモジュールは :meth:`module.fail_json`、
  または :meth:`module.exit_json` のいずれかを呼び出して終了する必要がありますが、テスト環境ではこれらは正しく動作しません。

引数の渡し方
-----------------

..以下の関数はライブラリーファイルで提供されているため、
   https://github.com/ansible/ansible/pull/31456 が解決したら、本セクションを一度更新する必要があります。

モジュールに正しく引数を渡すには、
ディクショナリーをパラメータとして受け取る ``set_module_args`` メソッドを使用します。モジュールの作成や引数の処理は、
ユーティリティーの基本セクションにある :class:`AnsibleModule` オブジェクトを使用して行います。通常は、
``STDIN`` で入力を受け付けますが、これはユニットテストには不便です。特別な変数が設定されている場合は、
モジュールへの入力が ``STDIN`` であったかのように処理されます。モジュールを設定する前にこの関数を呼び出すだけです。

    import json
    from units.modules.utils import set_module_args
    from ansible.module_utils._text import to_bytes

    def test_already_registered(self):
        set_module_args({
            'activationkey': 'key',
            'username': 'user',
            'password': 'pass',
        })

終了を適切に処理
-----------------------

..以下の終了および失敗の関数はライブラリーファイルで提供されるため、
   https://github.com/ansible/ansible/pull/31456 が解決したら、本セクションを一度更新する必要があります。

:meth:`module.exit_json` 関数は、
終了時にエラー情報を ``STDOUT``に書き込むため、
テスト環境では適切に動作しません。これは、この関数 (および :meth:`module.fail_json`) を、
例外を発生させる関数に置き換えることで緩和できます。

    def exit_json(*args, **kwargs):
        if 'changed' not in kwargs:
            kwargs['changed'] = False
        raise AnsibleExitJson(kwargs)

これで、最初に呼び出された関数が正しい例外であるかどうかをテストするだけで、
期待したものであることを確認することができるようになりました。

    def test_returned_value(self):
        set_module_args({
            'activationkey': 'key',
            'username': 'user',
            'password': 'pass',
        })

        with self.assertRaises(AnsibleExitJson) as result:
            my_module.main()

:meth:`module.fail_json` (モジュールからの失敗の戻り値に使用される) や、
``aws_module.fail_json_aws()`` (Amazon Web Services 用のモジュールで使用される) 
を置き換えるのと同じ手法を使うことができます。

主な関数の実行
-------------------------

モジュールにおける主な実関数を実行する場合は、モジュールをインポートし、上記のように引数を設定し、
適切な終了例外を設定してからモジュールを実行する必要があります。

    # This test is based around pytest's features for individual test functions
    import pytest
    import ansible.modules.module.group.my_module as my_module

    def test_main_function(monkeypatch):
        monkeypatch.setattr(my_module.AnsibleModule, "exit_json", fake_exit_json)
        set_module_args({
            'activationkey': 'key',
            'username': 'user',
            'password': 'pass',
        })
        my_module.main()


外部実行ファイルへの呼び出しの処理
--------------------------------------

モジュールは、外部コマンドを実行するのに :meth:`AnsibleModule.run_command` を使用する必要があります。このメソッドは、
モックする必要があります。

以下は、:meth:`AnsibleModule.run_command` (:file:`test/units/modules/packaging/os/test_rhn_register.py` から入手) の簡単なモック例です。

        with patch.object(basic.AnsibleModule, 'run_command') as run_command:
            run_command.return_value = 0, '', ''  # successful execution, no output
                with self.assertRaises(AnsibleExitJson) as result:
                    self.module.main()
                self.assertFalse(result.exception.args[0]['changed'])
        # Check that run_command has been called
        run_command.assert_called_once_with('/usr/bin/command args')
        self.assertEqual(run_command.call_count, 1)
        self.assertFalse(run_command.called)


完全な例
------------------

以下の例は、上記のモックを再利用し、
:meth:`Ansible.get_bin_path` 用に新たにモックを追加した完全なスケルトンです::

    import json

    from ansible.compat.tests import unittest
    from ansible.compat.tests.mock import patch
    from ansible.module_utils import basic
    from ansible.module_utils._text import to_bytes
    from ansible.modules.namespace import my_module


    def set_module_args(args):
        """prepare arguments so that they will be picked up during module creation"""
        args = json.dumps({'ANSIBLE_MODULE_ARGS': args})
        basic._ANSIBLE_ARGS = to_bytes(args)


    class AnsibleExitJson(Exception):
        """Exception class to be raised by module.exit_json and caught by the test case"""
        pass


    class AnsibleFailJson(Exception):
        """Exception class to be raised by module.fail_json and caught by the test case"""
        pass


    def exit_json(*args, **kwargs):
        """function to patch over exit_json; package return data into an exception"""
        if 'changed' not in kwargs:
            kwargs['changed'] = False
        raise AnsibleExitJson(kwargs)


    def fail_json(*args, **kwargs):
        """function to patch over fail_json; package return data into an exception"""
        kwargs['failed'] = True
        raise AnsibleFailJson(kwargs)


    def get_bin_path(self, arg, required=False):
        """Mock AnsibleModule.get_bin_path"""
        if arg.endswith('my_command'):
            return '/usr/bin/my_command'
        else:
            if required:
                fail_json(msg='%r not found !' % arg)


    class TestMyModule(unittest.TestCase):

        def setUp(self):
            self.mock_module_helper = patch.multiple(basic.AnsibleModule,
                                                     exit_json=exit_json,
                                                     fail_json=fail_json,
                                                     get_bin_path=get_bin_path)
            self.mock_module_helper.start()
            self.addCleanup(self.mock_module_helper.stop)

        def test_module_fail_when_required_args_missing(self):
            with self.assertRaises(AnsibleFailJson):
                set_module_args({})
                self.module.main()


        def test_ensure_command_called(self):
            set_module_args({
                'param1': 10,
                'param2': 'test',
            })

            with patch.object(basic.AnsibleModule, 'run_command') as mock_run_command:
                stdout = 'configuration updated'
                stderr = ''
                rc = 0
                mock_run_command.return_value = rc, stdout, stderr  # successful execution

                with self.assertRaises(AnsibleExitJson) as result:
                    my_module.main()
                self.assertFalse(result.exception.args[0]['changed']) # ensure result is changed

            mock_run_command.assert_called_once_with('/usr/bin/my_command --value 10 --name test')


テストモジュールの設定などを可能にするためのモジュールの再構築
-------------------------------------------------------------------------

多くの場合、モジュールには、
モジュールを設定してからその他のアクションを実行する ``main()`` 関数があります。これにより、引数処理の確認が困難になることがあります。これは、
モジュールの設定と初期化を別の関数に移すことで簡単にできます。例::

    argument_spec = dict(
        # module function variables
        state=dict(choices=['absent', 'present', 'rebooted', 'restarted'], default='present'),
        apply_immediately=dict(type='bool', default=False),
        wait=dict(type='bool', default=False),
        wait_timeout=dict(type='int', default=600),
        allocated_storage=dict(type='int', aliases=['size']),
        db_instance_identifier=dict(aliases=["id"], required=True),
    )

    def setup_module_object():
        module = AnsibleAWSModule(
            argument_spec=argument_spec,
            required_if=required_if,
            mutually_exclusive=[['old_instance_id', 'source_db_instance_identifier',
                                 'db_snapshot_identifier']],
        )
        return module

    def main():
        module = setup_module_object()
        validate_parameters(module)
        conn = setup_client(module)
        return_dict = run_task(module, conn)
        module.exit_json(**return_dict)
    
これにより、モジュールの開始関数に対してテストを実行できるようになりました。

    def test_rds_module_setup_fails_if_db_instance_identifier_parameter_missing():
        # db_instance_identifier parameter is missing
        set_module_args({
            'state': 'absent',
            'apply_immediately': 'True',
         })

        with self.assertRaises(AnsibleFailJson) as result:
            self.module.setup_json

``test/units/module_utils/aws/test_rds.py`` を併せて参照してください。

``argument_spec`` ディクショナリーは、モジュール変数に表示されることに注意してください。これは、
引数の明示的なテストを可能にし、
テスト用のモジュールオブジェクトを簡単に作成できるという利点があります。

この再構築の手法は、モジュールが設定したオブジェクトを問い合わせるモジュールの部分など、その他の機能をテストする場合にも役に立ちます。

Python 2 の互換性を維持するためのトラップ
============================================

``Python`` 2.6 標準ライブラリーの ``mock`` ライブラリーを使用する場合は、
多くの assert 関数が欠落していますが、成功したかのように返されます。 これは、Python 3 のドキュメントで _new_ というマークが付いている関数を *使用しない* ように、
テストケースが細心の注意を払う必要があることを示しています。
これは、古いバージョンの Python で実行したときにコードが壊れていても、テストは常に成功する可能性が高いからです。

これに役立つ開発アプローチは、
すべてのテストが Python 2.6 で実行されていることと、
テストケース内の各アサーションが Ansible でコードを壊してその失敗を誘発することで動作することが確認されているという点を確認することです。

.. warning:: Python 2.6 互換性の維持

    モジュールは Python 2.6 との互換性を維持する必要があるため、
    モジュールのユニットテストも、Python 2.6 との互換性を維持する必要があることに注意してください。


.. seealso::

   :ref:`testing_units`
       Ansible unit テストドキュメント
   :ref:`testing_running_locally`
       カバレージデータの収集とレポートを含む、ローカルでのテストの実行
   :ref:`developing_modules_general`
       モジュール開発を始める
   `Python 3 ドキュメント - 26.4. ユニットテスト - ユニットテストのフレームワーク <https://docs.python.org/3/library/unittest.html>`_
       Python 3 におけるユニットテストフレームワークのドキュメント
   `Python 2 ドキュメント - 25.3. ユニットテスト - ユニットテストのフレームワーク <https://docs.python.org/3/library/unittest.html>`_
       サポートされている初期のユニットテストフレームワークのドキュメント (Python 2.6)
   `pytest (より優れたプログラムを書き込むのに役立ちます) <https://docs.pytest.org/en/latest/>`_
       pytest のドキュメント - Ansible ユニットテストの実行に実際に使用されているフレームワーク
   `開発メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発トピックのメーリングリスト
   `コードのテスト (「The Hitchhiker's Guide to Python!」より) <https://docs.python-guide.org/writing/tests/>`_
       Python コードのテストに関する一般的なアドバイス
   `YouTube で公開されている Uncle Bob による多数の動画 <https://www.youtube.com/watch?v=QedpQjxBPMA&list=PLlu0CT-JnSasQzGrGzddSczJQQU7295D2>`_
       ユニットテストは、
       Extreme Programming (XP)、クリーンコーディングを含むソフトウェア開発の様々な哲学の一部です。 Uncle Bob は、どのようにしてこの恩恵を受けることができるのかを説明します。
   `「Why Most Unit Testing is Waste」 <https://rbcs-us.com/documents/Why-Most-Unit-Testing-is-Waste.pdf>`_
       ユニットテストの大半が無駄である理由
   `「Why Most Unit Testing is Waste」への回答<https://henrikwarne.com/2014/09/04/a-response-to-why-most-unit-testing-is-waste/>`_
       ユニットテストの価値を維持する方法を指摘した回答
