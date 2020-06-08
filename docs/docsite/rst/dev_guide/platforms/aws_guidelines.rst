.. _AWS_module_development:

****************************************************
Ansible Amazon AWS モジュール開発のガイドライン
****************************************************

Ansible AWS モジュールおよびこれらのガイドラインは、Ansible AWS Working Group が管理しています。 詳細は、
「
`AWS Working Group コミュニティーページ <https://github.com/ansible/community/wiki/aws>`_」を参照してください。
Ansible に AWS モジュールを提供することを計画している場合は、
特に類似のモジュールがすでに開発中である可能性があるため、
まずはワーキンググループに連絡することが推奨されます。

.. contents::
   :local:

既存のモジュールのメンテナンス
============================

バグの修正
-----------

boto に依存するコードに対するバグ修正は引き続き承認されます。可能であれば、
このコードは、boto3 を使用するように移植する必要があります。

新しい機能の追加
-------------------

比較的最近のバージョンの boto3 との下位互換性を保つようにしてください。つまり、
boto3 の新機能を使用する一部の機能を実装する場合は、
その機能を実際に実行する必要がある場合にのみ失敗し、
欠落している機能と最低限必要な boto3 のバージョンを示すメッセージが表示されます。

機能テスト (``hasattr('boto3.module', 'shiny_new_method')`` など) を使用して、
バージョンチェックではなく、boto3 が機能をサポートするかどうかを確認します。たとえば、``ec2`` モジュールは以下のようになります。

.. code-block:: python

   if boto_supports_profile_name_arg(ec2):
       params['instance_profile_name'] = instance_profile_name
   else:
       if instance_profile_name is not None:
           module.fail_json(msg="instance_profile_name parameter requires boto version 2.5.0 or higher")

boto3 への移行
------------------

Ansible 2.0 以前は、モジュールは boto3 または boto で記述されていました。一部のモジュールは、
boto3 に移植します。ライブラリー (boto および boto3) を使用せず boto3 を使用するため、boto を必要とするモジュールを移植する必要があります。すべてのモジュールから boto 依存関係を削除します。

AnsibleAWSModule へのコードの移植
---------------------------------

一部の古い AWS モジュールは、より効率的な ``AnsibleAWSModule`` ではなく、汎用の ``AnsibleModule`` をベースとして使用します。古いモジュールを ``AnsibleAWSModule`` に移植するには、以下を、

.. code-block:: python

   from ansible.module_utils.basic import AnsibleModule
   ...
   module = AnsibleModule(...)

以下のように変更します。

.. code-block:: python

   from ansible.module_utils.aws.core import AnsibleAWSModule
   ...
   module = AnsibleAWSModule(...)

その他の変更はほとんど必要ありません。AnsibleAWSModule は、
デフォルトでは AnsibleModule からメソッドを継承しませんが、
最も便利なメソッドが含まれています。問題が見つかった場合は、バグレポートを作成してください。

移植時には、
AnsibleAWSModule もデフォルトでデフォルトの ec2 引数の仕様を追加することに注意してください。移植前のモジュールでは、
次のように指定された共通の引数が表示されます。

.. code-block:: python

   def main():
       argument_spec = ec2_argument_spec()
       argument_spec.update(dict(
           state=dict(default='present', choices=['present', 'absent', 'enabled', 'disabled']),
           name=dict(default='default'),
           # ... and so on ...
       ))
       module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,)

これは、次のものと置き換えることができます。

.. code-block:: python

   def main():
       argument_spec = dict(
           state=dict(default='present', choices=['present', 'absent', 'enabled', 'disabled']),
           name=dict(default='default'),
           # ... and so on ...
       )
       module = AnsibleAWSModule(argument_spec=argument_spec, supports_check_mode=True,)

新規 AWS モジュールの作成
========================

boto3 および AnsibleAWSModule の使用
-------------------------------

すべての新規 AWS モジュールは boto3 および ``AnsibleAWSModule`` を使用する必要があります。

``AnsibleAWSModule`` は、
例外処理とライブラリー管理を大幅に簡素化し、boilerplate コードの量を減らします。``AnsibleAWSModule`` をベースとして使用できない場合は、
理由を文書化し、このルールの例外を要求する必要があります。

モジュールの名前付け
------------------

実際に使用する AWS の一部にあるモジュールの名前を指定します。経験則としては、
boto で使用するモジュールをすべて出発点として使用することが推奨されます。 名前をこれ以上省略しないでください。
AWS の主要コンポーネントのよく知られた省略形 (たとえば VPC または ELB) である場合は問題ありませんが、
独自に新しいものは作成しないでください。

サービスの名前が非常に一意でない限り、``aws_`` を接頭辞として使用することを検討してください。たとえば ``aws_lambda`` になります。

botocore および boto3 のインポート
----------------------------

``ansible.module_utils.ec2`` モジュールおよび ``ansible.module_utils.core.aws`` モジュールは、
どちらも自動的に boto3 と botocore をインポートします。 boto3 がシステムにない場合、
``HAS_BOTO3`` 変数は false に設定されます。 通常、
これはモジュールが boto3 を直接インポートする必要がないことを意味します。``HAS_BOTO3`` の確認はそのモジュールが行うため、
AnsibleAWSModule を使用するときに確認する必要はありません。

.. code-block:: python

   from ansible.module_utils.aws.core import AnsibleAWSModule
   try:
       import botocore
   except ImportError:
       pass  # handled by AnsibleAWSModule

または

.. code-block:: python

   from ansible.module_utils.basic import AnsibleModule
   from ansible.module_utils.ec2 import HAS_BOTO3
   try:
       import botocore
   except ImportError:
       pass  # handled by imported HAS_BOTO3

   def main():

       if not HAS_BOTO3:
           module.fail_json(msg='boto3 and botocore are required for this module')

AWS への接続
=================

AnsibleAWSModule は、boto3 接続を取得するためのヘルパーメソッド ``resource`` および ``client`` を提供します。
これらは、セキュリティートークンや boto プロファイルなど、より難解な接続オプションのいくつかを処理します。

基本的な AnsibleModule を使用する場合は、``get_aws_connection_info`` を使用してから ``boto3_conn`` を使用して AWS に接続する必要があります。
これらは同じ範囲の接続オプションを処理するためです。

これらのヘルパーは、欠落しているプロファイルや、必要なときに設定されていない領域にも使用できるため、必須ではありません。

ec2 への接続例を以下に示します。boto のような 
``NoAuthHandlerFound`` 例外処理はありません。代わりに、
接続を使用すると ``AuthFailure`` 例外が発生します。認証、パラメータ検証、パーミッションエラーをすべて確実に取得するには、
すべての boto3 接続呼び出しで、例外の ``ClientError`` および ``BotoCoreError`` を捕える必要があります。
例外処理は次のようになります。

.. code-block:: python

   module.client('ec2')

また、より高いレベルの ec2 リソースの場合は、次のようになります。

.. code-block:: python

   module.resource('ec2')


AnsibleAWSModule ではなく AnsibleModule に基づくモジュールに使用される旧式の接続例は次のとおりです。

.. code-block:: python

   region, ec2_url, aws_connect_params = get_aws_connection_info(module, boto3=True)
   connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)

.. code-block:: python

   region, ec2_url, aws_connect_params = get_aws_connection_info(module, boto3=True)
   connection = boto3_conn(module, conn_type='client', resource='ec2', region=region, endpoint=ec2_url, **aws_connect_params)


接続パラメーターに関する断片化された汎用ドキュメント
--------------------------------------------------------

ほとんどすべての AWS モジュールに含める必要がある、
:ref:`断片化された汎用ドキュメント <module_docs_fragments>` は 2 つあります。

* ``aws`` - 共通の boto 接続パラメーターが含まれます。
* ``ec2`` - 数多くの AWS モジュールに必要な共通の region パラメーターが含まれます。

一貫性を確保し、より難解な接続オプションを文書化するには、
このようなプロパティーを再文書化するのではなく、このような断片化されたドキュメントを使用する必要があります。例:

.. code-block:: python

   DOCUMENTATION = '''
   module: my_module
   # some lines omitted here
   requirements: [ 'botocore', 'boto3' ]
   extends_documentation_fragment:
       - aws
       - ec2
   '''

例外の処理
===================

boto3 または botocore の呼び出しを try ブロックにラップする必要があります。例外が発生した場合に、
それを処理する方法はいくつかあります。

* 一般的な ``ClientError`` を取得するか、
    ``is_boto3_error_code`` で特定のエラーコードを探します。
* ``aws_module.fail_json_aws()`` を使用して、標準的な方法でモジュール障害を報告します。
* AWSRetry を使用して再試行します。
* ``fail_json()`` を使用して、``ansible.module_utils.aws.core`` を使用せずに問題を報告します。
* 例外の処理方法が分かっている場合は、何らかのカスタマイズ作業を行います。

botocore 例外処理の詳細は、`botocore エラーのドキュメント <https://botocore.readthedocs.io/en/latest/client_upgrades.html#error-handling>`_ を参照してください。

is_boto3_error_code の使用
-------------------------

``ansible.module_utils.aws.core.is_boto3_error_code`` を使用して単一の AWS エラーコードを捕えるには、
except 句で ``ClientError`` の代わりにそれを呼び出します。この場合は、
``InvalidGroup.NotFound`` エラーコード *のみ* がここで捕えられ、
その他のエラーは、プログラムの他の場所で処理するために発生します。

.. code-block:: python

   try:
       info = connection.describe_security_groups(**kwargs)
   except is_boto3_error_code('InvalidGroup.NotFound'):
       pass
   do_something(info)  # do something with the info that was successfully returned

fail_json_aws() の使用
---------------------

AnsibleAWSModule には、
例外を適切に報告するための特別なメソッド ``module.fail_json_aws()`` があります。 例外でこれを呼び出すと、
Ansible の詳細モードで使用するためのトレースバックとともにエラーが報告されます。

可能な場合は、すべての新しいモジュールに AnsibleAWSModule を使用する必要があります。既存のモジュールに大量の例外処理を追加する場合は、
AnsibleAWSModule を使用するようにモジュールを移行することが推奨されます。
これを行うために必要な変更はほとんどありません。

.. code-block:: python

   from ansible.module_utils.aws.core import AnsibleAWSModule

   # Set up module parameters
   # module params code here

   # Connect to AWS
   # connection code here

   # Make a call to AWS
   name = module.params.get['name']
   try:
       result = connection.describe_frooble(FroobleName=name)
   except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
       module.fail_json_aws(e, msg="Couldn't obtain frooble %s" % name)

通常、ここですべての通常の例外を捕えても問題がないことに注意してください。
ただし、botocore 以外の例外が予想される場合は、すべてが期待どおりに機能するかどうかをテストする必要があります。

返された boto3 エラーに基づいてアクションを実行する必要がある場合は、このエラーコードを使用します。

.. code-block:: python

   # Make a call to AWS
   name = module.params.get['name']
   try:
       result = connection.describe_frooble(FroobleName=name)
   except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == 'FroobleNotFound':
           workaround_failure()  # This is an error that we can work around
       else:
           module.fail_json_aws(e, msg="Couldn't obtain frooble %s" % name)
   except botocore.exceptions.BotoCoreError as e:
       module.fail_json_aws(e, msg="Couldn't obtain frooble %s" % name)

fail_json() and avoiding ansible.module_utils.aws.core の使用
------------------------------------------------------------

Boto3 は、例外が発生したときに多くの有用な情報を提供するため、
メッセージと共にこれをユーザーに渡します。

.. code-block:: python

   from ansible.module_utils.ec2 import HAS_BOTO3
   try:
       import botocore
   except ImportError:
       pass  # caught by imported HAS_BOTO3

   # Connect to AWS
   # connection code here

   # Make a call to AWS
   name = module.params.get['name']
   try:
       result = connection.describe_frooble(FroobleName=name)
   except botocore.exceptions.ClientError as e:
       module.fail_json(msg="Couldn't obtain frooble %s: %s" % (name, str(e)),
                        exception=traceback.format_exc(),
                        **camel_dict_to_snake_dict(e.response))

注記: 後者は python3 では機能しないため、
`e.message` ではなく `str(e)` を使用します。

返された boto3 エラーに基づいてアクションを実行する必要がある場合は、このエラーコードを使用します。

.. code-block:: python

   # Make a call to AWS
   name = module.params.get['name']
   try:
       result = connection.describe_frooble(FroobleName=name)
   except botocore.exceptions.ClientError as e:
       if e.response['Error']['Code'] == 'FroobleNotFound':
           workaround_failure()  # This is an error that we can work around
       else:
           module.fail_json(msg="Couldn't obtain frooble %s: %s" % (name, str(e)),
                            exception=traceback.format_exc(),
                            **camel_dict_to_snake_dict(e.response))
   except botocore.exceptions.BotoCoreError as e:
       module.fail_json_aws(e, msg="Couldn't obtain frooble %s" % name)


API スロットリング (レート制限) とページネーション
=============================================

多くの結果を返すメソッドの場合、
boto3 はしばしば `paginators <https://boto3.readthedocs.io/en/latest/guide/paginators.html>`_ を提供します。呼び出すメソッドに ``NextToken`` パラメーターまたは ``Marker`` パラメーターがある場合は、
おそらく、ページネーションが存在するかどうかを確認する必要があります。
サービスに Paginator がある場合は、各 boto3 サービスのリファレンスページの上部に、
その Paginator へのリンクがあります。paginators を使用するには、paginator オブジェクトを取得し、
適切な引数を指定して ``paginator.paginate`` を呼び出してから、``build_full_result`` を呼び出します。

AWS API を頻繁に呼び出すときはいつでも、API スロットリングが発生する可能性があります。
また、バックオフを確実にするために使用できる ``AWSRetry`` デコレーターがあります。例外処理は再試行の正常な動作を妨げる可能性があるため 
(AWSRetry はスロットル例外を捕えて正しく機能する必要があるため)、
バックオフ関数を提供し、
バックオフ関数の周りに例外処理を配置する必要があります。

ストラテジーの ``exponential_backoff`` または ``jittered_backoff`` を使用できます
詳細は、クラウドの ``module_utils`` ()/lib/ansible/module_utils/cloud.py)、
および「`AWS Architecture blog <https://www.awsarchitectureblog.com/2015/03/backoff.html>`_」を参照してください。

これら 2 つのアプローチの組み合わせは次のとおりです。

.. code-block:: python

   @AWSRetry.exponential_backoff(retries=5, delay=5)
   def describe_some_resource_with_backoff(client, **kwargs):
        paginator = client.get_paginator('describe_some_resource')
        return paginator.paginate(**kwargs).build_full_result()['SomeResource']

   def describe_some_resource(client, module):
       filters = ansible_dict_to_boto3_filter_list(module.params['filters'])
       try:
           return describe_some_resource_with_backoff(client, Filters=filters)
       except botocore.exceptions.ClientError as e:
           module.fail_json_aws(e, msg="Could not describe some resource")


基本となる API 呼び出し ``describe_some_resources`` が、``ResourceNotFound`` 例外を発生させた後、
``AWSRetry`` はこれが出力されなくなるまで再試行する合図としてこれを受け取ります。
これは、リソースを作成するときに、リソースが存在するまで再試行できるようにするためです。

リソースが存在せず再試行しない場合に ``None`` を返すだけで、
``describe_some_resource_with_backoff`` で認証エラーまたはパラメーター検証エラーを処理するには、
次が必要になります。

.. code-block:: python

   @AWSRetry.exponential_backoff(retries=5, delay=5)
   def describe_some_resource_with_backoff(client, **kwargs):
        try:
            return client.describe_some_resource(ResourceName=kwargs['name'])['Resources']
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFound':
                return None
            else:
                raise
        except BotoCoreError as e:
            raise

   def describe_some_resource(client, module):
       name = module.params.get['name']
       try:
           return describe_some_resource_with_backoff(client, name=name)
       except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
           module.fail_json_aws(e, msg="Could not describe resource %s" % name)


AWSRetry を使いやすくするために、
``AnsibleAWSModule`` によって返されたクライアントをラップできるようになりました。クライアントからの呼び出しになります。クライアントに再試行を追加する場合は、
クライアントを作成します。

.. code-block:: python

   module.client('ec2', retry_decorator=AWSRetry.jittered_backoff(retries=10))

そのクライアントからの呼び出しは、
`aws_retry` 引数を使用して、呼び出し時に渡されるデコレーターを使用するために作成できます。デフォルトでは、再試行は使用されません。

.. code-block:: python

   ec2 = module.client('ec2', retry_decorator=AWSRetry.jittered_backoff(retries=10))
   ec2.describe_instances(InstanceIds=['i-123456789'], aws_retry=True)

   # equivalent with normal AWSRetry
   @AWSRetry.jittered_backoff(retries=10)
   def describe_instances(client, **kwargs):
       return ec2.describe_instances(**kwargs)

   describe_instances(module.client('ec2'), InstanceIds=['i-123456789'])

呼び出しは指定された回数再試行されるため、
呼び出し元の関数をバックオフデコレーターでラップする必要はありません。

また、モジュールパラメーターを使用して、``AWSRetry.jittered_backoff`` API によって使用される ``retries``、``delay``、
``max_delay`` の各パラメーターのカスタマイズを使用することもできます。ここでは、
`cloudformation <cloudformation_module>` モジュールを見てみましょう。

すべての Amazon モジュールを均一にするには、モジュールパラメーターの前に ``backoff_`` を付けます。これにより、``retries`` は ``backoff_retries`` になり、
 同様に ``backoff_delay`` や ``backoff_max_delay`` も付けられます。

戻り値
================

boto3 を使用して呼び出しを行うと、
モジュールで返すべきいくつかの有用な情報が返されます。 呼び出し自体に関連する情報だけでなく、
いくつかの応答メタデータもあります。 これをユーザーに返すことは問題なく、有用な場合もあります。

Boto3 はすべての値をキャメルケースで返します。 Ansible は、
変数名の Python 標準仕様に従い、snake_case を使用します。`camel_dict_to_snake_dict` と呼ばれる module_utils/ec2.py にヘルパー関数があり、boto3 応答を snake_case に簡単に変換できます。
これにより、boto3 応答を snake_case に簡単に変換できます。

このヘルパー関数を使用し、boto3 が返す値の名前を変更しないでください。
たとえば、boto3 が「SecretAccessKey」値を返す場合は、これを「AccessKey」に変更しないでください。

.. code-block:: python

   # Make a call to AWS
   result = connection.aws_call()

   # Return the result to the user
   module.exit_json(changed=True, **camel_dict_to_snake_dict(result))

IAM JSON ポリシーの処理
============================

モジュールが IAM JSON ポリシーを受け入れる場合は、モジュール仕様でタイプを「json」に設定します。たとえば、
以下のようになります。

.. code-block:: python

   argument_spec.update(
       dict(
           policy=dict(required=False, default=None, type='json'),
       )
   )

AWS が、送信された順序でポリシーを返すことはほとんどありません。したがって、
この差異を処理する `compare_policies` ヘルパー関数を使用します。

`compare_policies` は 2 つのディクショナリーを取得し、再帰的にソートし、比較のためにハッシュを可能にし、
異なる場合は True を返します。

.. code-block:: python

   from ansible.module_utils.ec2 import compare_policies

   import json

   # some lines skipped here

   # Get the policy from AWS
   current_policy = json.loads(aws_object.get_policy())
   user_policy = json.loads(module.params.get('policy'))

   # Compare the user submitted policy to the current policy ignoring order
   if compare_policies(user_policy, current_policy):
       # Update the policy
       aws_object.set_policy(user_policy)
   else:
       # Nothing to do
       pass

タグの処理
=================

AWS にはリソースタグの概念があります。通常、boto3 API には、
リソースのタグ付けとタグ付け解除のための呼び出しがあります。 たとえば、ec2 API には create_tags および delete_tags の呼び出しがあります。

Ansible AWS モジュールでは、
デフォルトで true に設定されている `purge_tags` パラメーターを使用するのが一般的です。

`purge_tags` パラメーターは、
既存のタグが Ansible タスクで指定されていない場合に削除されることを示しています。

タグの処理を容易にするために、`compare_aws_tags` ヘルパー関数があります。2 つのディクショナリーを比較し、
設定するタグと削除するタグを返すことができます。 詳細は、
以下の helper 関数セクションを参照してください。

helper 関数
================

Ansible ec2.py module_utils の接続関数に加えて、
以下に説明するいくつかの便利な関数があります。

camel_dict_to_snake_dict
------------------------

boto3 は、結果をディクショナリーで返します。 ディクショナリーのキーはキャメルケース形式です。Ansible 形式に沿って、
この関数はキーを snake_case に変換します。

``camel_dict_to_snake_dict`` は、``ignore_list`` と呼ばれる任意のパラメーターを取ります。
これは、変換しないキーの一覧です。これは通常、``tags`` ディクショナリーに役に立ちます。
この子キーは大文字と小文字を区別して保持する必要があります。

他のオプションのパラメーターも ``元に戻すことが可能`` です。デフォルトでは、``HTTPEndpoint`` は ``http_endpoint`` に変換されます。
これは、``snake_dict_to_camel_dict`` により ``HttpEndpoint`` に変換されます。
``reversible=True`` を渡すと、HTTPEndpoint を ``h_t_t_p_endpoint`` に変換され、これが ``HTTPEndpoint`` に変換されます。

snake_dict_to_camel_dict
------------------------

`inspection_dict_to_camel_dict` は、スネークケースのキーをキャメルケースに変換します。デフォルトでは、最初に ECS の目的で導入されたため、
これは dromedaryCase に変換されます。`capitalize_first` と呼ばれる任意のパラメーター (デフォルトは `False`) を使用して、
CamelCase に変換できます。

ansible_dict_to_boto3_filter_list
---------------------------------

フィルターの Ansible リストを、ディクショナリーの boto3 フレンドリーリストに変換します。 これは、
すべての boto3 `_facts` モジュールに役に立ちます。

boto_exception
--------------

boto または boto3 から返された例外を渡します。この関数は、例外からメッセージを一貫して取得します。

非推奨: 代わりに `AnsibleAWSModule` の `fail_json_aws` を使用してください。


boto3_tag_list_to_ansible_dict
------------------------------

boto3 タグリストを Ansible ディクショナリーに変換します。Boto3 は、
デフォルトで「Key」と「Value」と呼ばれるキーを含むディクショナリーのリストとしてタグを返します。 このキー名は、関数の呼び出し時に上書きできます。
たとえば、タグのリストをすでにキャメルケースにしている場合は、
代わりに小文字のキー名、つまり「key」と「value」を渡すことができます。

この関数は、リストを単一のディクショナリーに変換します。
dict キーはタグキーで、dict 値はタグの値です。

ansible_dict_to_boto3_tag_list
------------------------------

上記とは反対です。Ansible ディクショナリーを、ディクショナリーの boto3 タグ一覧に変換します。「Key」と「Value」が適切でない場合は、
使用されているキー名を再度上書きできます。

get_ec2_security_group_ids_from_names
-------------------------------------

この関数は、セキュリティーグループ名またはセキュリティーグループ ID の組み合わせを渡します。
そして、この関数は ID の一覧を返します。 セキュリティーグループ名は VPC 全体で一意である必要はないため、
既知の場合は VPC ID も渡す必要があります。

compare_policies
----------------

意味のある違いがあるかどうかを確認するためにポリシーの 2 つのディクショナリーを渡し、
違いある場合は true を返します。これにより、dict が再帰的にソートされ、比較前にハッシュ可能になります。

この方法は、順序を変更しても不要な変更が発生しないように、
ポリシーを比較するときに必ず使用する必要があります。

compare_aws_tags
----------------

タグの 2 つのディクショナリーと任意のパージパラメーターを渡します。この関数はディクショナリーを返します。
これには、変更するキーペアと、削除する必要のあるタグキー名の一覧が含まれています。 パージは、
デフォルトで True です。 パージが False の場合は、既存のタグが変更されません。

この関数は、boto3 の「add_tags」関数および「remove_tags」 関数を使用する場合に役に立ちます。この関数を呼び出す前に、
他のヘルパー関数 `boto3_tag_list_to_ansible_dict` を使用して、
適切なタグのディクショナリーを取得します。AWS API は統一されていないため (EC2 と Lambda など)、
(Lambda) を変更しなくても機能するものもあれば、
これらの値を使用する前に変更が必要な場合があります (EC2など、タグの設定を解除して `[{'Key': key1}, {'Key': key2}]` の形式にする必要があります)。

AWS モジュールの統合テスト
=================================

すべての新しい AWS モジュールには、
モジュールに影響する AWS API の変更が確実に検出されるように、統合テストを含める必要があります。少なくとも、これは主要な API 呼び出しをカバーし、
文書化された戻り値がモジュール結果に存在することを確認する必要があります。

統合テストの実行に関する一般的な情報は、
Module Development Guide <testing_integration>` の :ref:`Integration Tests ページを参照してください。

モジュールの統合テストは、`test/integration/targets/MODULE_NAME` に追加する必要があります。

`test/integration/targets/MODULE_NAME/aliases` にエイリアスファイルが必要です。このファイルには、
目的が 2 つあります。最初に、それが AWS テストであることを示し、
テストフレームワークがテスト実行中に AWS 認証情報を使用できるようにします。次に、テストをテストグループに入れて、
継続的インテグレーションビルドでテストを実行します。

新規モジュールのテストは、既存の AWS テストと同じグループに追加する必要があります。通常は、
`aws_s3 テストエイリアスファイル <https://github.com/ansible/ansible/blob/devel/test/integration/targets/aws_s3/aliases>`_ などの既存のエイリアスをコピーするだけで終わりです。

統合テストの AWS 認証情報
-------------------------------------

テストフレームワークは、適切な AWS 認証情報を使用したテストの実行を処理します。
この認証情報は、次の変数で、テストに利用できます。

* `aws_region`
* `aws_access_key`
* `aws_secret_key`
* `security_token`

したがって、テスト内の AWS モジュールの呼び出しでは、必ずこれらのパラメーターを設定する必要があります。各呼び出しでこれらが重複しないようにするには、
:ref:`module_defaults <module_defaults>` を使用することが推奨されます。例:

.. code-block:: yaml

   - name: set connection information for aws modules and run tasks
     module_defaults:
       group/aws:
         aws_access_key: "{{ aws_access_key }}"
         aws_secret_key: "{{ aws_secret_key }}"
         security_token: "{{ security_token | default(omit) }}"
         region: "{{ aws_region }}"

     block:

     - name: Do Something
       ec2_instance:
         ... params ...

     - name: Do Something Else
       ec2_instance:
         ... params ...

統合テスト用の AWS パーミッション
-------------------------------------

:ref:`統合テストガイド <testing_integration>` で説明されているように、
``hacking/aws_config/testing_policies/`` には、
AWS 統合テストを実行するために必要なパーミッションを含む IAM ポリシーが定義されています。CI で使用されるパーミッションは、``hacking/aws_config/testing_policies`` のパーミッションよりも制限されています。
CI の場合は、特定のテストに合格できるようにする、最も制限の厳しいポリシーが必要です。

モジュールが新しいサービスとやり取りする場合、または別の方法で新しいパーミッションが必要な場合は、
プル要求を送信するとテストが失敗し、`Ansibullbot <https://github.com/ansible/ansibullbot/blob/master/ISSUE_HELP.md>`_ は PR に修正が必要なタグを付けます。
継続的インテグレーションビルドによって使用されるロールには、追加のパーミッションが自動的に付与されません。インテグレーションテストの実行に必要な最低限の IAM パーミッションを指定する必要があります。

PR にテストの失敗がある場合には、パーミッションが不足していることだけがその失敗の原因かどうかを慎重に確認してください。他の失敗の原因を除外している場合は、`ready_for_review` タグを使用してコメントを追加し、
それが権限の不足によるものであることを説明します。

テストに合格するまでプル要求をマージすることはできません。パーミッションがないためにプル要求が失敗する場合は、以下を実行します。
テストを実行するのに必要な最小 
IAM パーミッションを収集する必要があります。

PR に合格するために必要な IAM パーミッションを確認する場合は、以下の 2 つの方法があります。

* 最も許容度の高い IAM ポリシーから始めて、テストを実行し、テストが実際に使用するリソースに関する情報を収集し、その出力に基づいてポリシーを構築します。このアプローチは、`AnsibleAWSModule` を使用するモジュールでのみ機能します。
* 最も許容度の低い IAM ポリシーから開始し、テストを実行して障害を検出し、その障害に対処するリソースのパーミッションを追加してから、繰り返します。モジュールが `AnsibleAWSModule` ではなく `AnsibleModule` を使用する場合は、この方法を使用する必要があります。

最も許容度の高い IAM ポリシーを使用するには、以下を実行します。

1) すべてのアクションを許可する `IAM ポリシー <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html#access_policies_create-start>`_ を作成します (``Action`` および ``Resource`` を ``*``` に設定します)。
2) このポリシーを使用してローカルでテストを実行します。AnsibleAWSModule ベースのモジュールでは、``debug_botocore_endpoint_logs`` オプションは自動的に ``yes`` に設定されるため、PLAY RECAP の後に AWS ACTIONS のリストが表示され、使用されているすべてのパーミッションが示されます。テストで boto/AnsibleModule モジュールを使用している場合は、最も許容度の低いポリシーで開始する必要があります (下記参照)。
3）テストが使用するアクションのみを許可するようにポリシーを変更します。可能な場合はアカウント、リージョン、および接頭辞を制限します。ポリシーが更新されるまで数分待機します。
4) 新規ポリシーのみを許可するユーザーまたはロールでテストを再実行します。
5) テストに失敗し、トラブルシューティング (以下のヒントを参照) を行い、ポリシーを変更し、テストを再実行し、制限的なポリシーでテストに合格するまでプロセスを繰り返します。
6) `テストポリシー <https://github.com/mattclay/aws-terminator/tree/master/aws/policy>`_ に対して最低限必要なポリシーを提案するプル要求を開きます。

最も許容度の低い IAM ポリシーから開始するには、以下を実行します。

1) IAM パーミッションを持たないローカルの統合テストを実行します。
2) テストが失敗した場合はエラーを確認します。
    a) エラーメッセージがリクエストで使用されるアクションを示す場合は、アクションをポリシーに追加します。
    b) エラーメッセージがリクエストで使用されるアクションを示していない場合は、以下を行います。
        - 通常、アクションはメソッド名の CamelCase バージョンです。たとえば、ec2 クライアントの場合、`describe_security_groups` メソッドはアクション `ec2:DescribeSecurityGroups` に相関します。
        - アクションを特定するには、ドキュメントを参照してください。
    c) エラーメッセージが要求で使用されるリソース ARN を示す場合は、アクションをそのリソースに制限します。
    d) エラーメッセージに、使用されたリソース ARN が示されない場合は、以下を行います。
        - ドキュメントを参照して、アクションをリソースに制限できるかどうかを判断します。
        - アクションが制限されている場合は、ドキュメントを使用して ARN を構築し、ポリシーに追加します。
3) `IAM ポリシー <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html#access_policies_create-start>`_ に障害の原因となったアクションまたはリソースを追加します。ポリシーが更新されるまで数分待機します。
4) ユーザーまたはロールにこのポリシーを割り当てテストを再実行します。
5) 同じエラーの同じ場所でテストが失敗する場合は、トラブルシューティングを行う必要があります (以下のヒントを参照してください)。最初のテストに合格したら、次のエラーに対してステップ 2 と 3 を繰り返します。制限的なポリシーでテストに合格するまで、プロセスを繰り返します。
6) `テストポリシー <https://github.com/mattclay/aws-terminator/tree/master/aws/policy>`_ に対して最低限必要なポリシーを提案するプル要求を開きます。

IAM ポリシーのトラブルシューティング
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ポリシーに変更を加えたら、ポリシーが更新されるまで数分待ってからテストを再実行します。
- `ポリシーシミュレーター <https://policysim.aws.amazon.com/>`_ を使用して、ポリシー内の (該当する場合はリソースによって制限されている) が許可されていることを確認します。
- 特定のリソースにアクションを制限する場合は、リソースを一時的に `*` に置き換えます。ワイルドカードリソースでテストに合格した場合は、ポリシーのリソース定義に問題があります。
- 上記の最初のトラブルシューティングでより多くの洞察が得られない場合、AWS は追加の未公開のリソースおよびアクションを使用している可能性があります。
- 手がかりについては、サービスの AWS FullAccess ポリシーを調べます。
- 各種の AWS サービスの `Actions, Resources and Condition Keys <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_actions-resources-contextkeys.html>`_ の一覧など、AWS ドキュメントを再度読みます。
- トラブルシューティングの相互参照として `cloudonaut <https://iam.cloudonaut.io>`_ ドキュメントをご覧ください。
- 検索エンジンを使用します。
- Ansible IRC チャンネル freenode IRC の #ansible-aws に問い合わせます。

テストがサポート対象外としてマークされる必要がある場合があります。
1) テストが完了するまで 10 分または 15 分かかります。
2) テストにより、高価なリソースが作成されます。
3) テストは、インラインポリシーを作成します。
