.. _module_defaults:

モジュールのデフォルト
===============

同じ引数で同じモジュールを繰り返し呼び出す場合は、``module_defaults`` 属性を使用して、その特定のモジュールのデフォルト引数を定義すると便利です。

以下に基本的な例を示します。

    - hosts: localhost
      module_defaults:
        file:
          owner: root
          group: root
          mode: 0755
      tasks:
        - file:
            state: touch
            path: /tmp/file1
        - file:
            state: touch
            path: /tmp/file2
        - file:
            state: touch
            path: /tmp/file3

``Module_defaults`` 属性は、プレイ、ブロック、およびタスクのレベルで使用できます。タスクに明示的に指定されているモジュール引数は、そのモジュール引数に対して確立されたデフォルトを上書きします。

    - block:
        - debug:
            msg: "a different message"
      module_defaults:
        debug:
          msg: "a default message"

空の dict を指定して、モジュールの以前に設定されたデフォルトを削除することもできます。

    - file:
        state: touch
        path: /tmp/file1
      module_defaults:
        file: {}

.. note::
    プレイレベルで設定されるモジュールのデフォルト (``include_role`` または ``import_role`` を使用する際のブロックまたはタスクのレベル) は、使用されるロールに適用されます。これにより、ロールで予期しない動作が発生する可能性があります。

この機能のより実用的なユースケースを以下に示します。

auth を必要とする API との対話

    - hosts: localhost
      module_defaults:
        uri:
          force_basic_auth: true
          user: some_user
          password: some_password
      tasks:
        - uri:
            url: http://some.api.host/v1/whatever1
        - uri:
            url: http://some.api.host/v1/whatever2
        - uri:
            url: http://some.api.host/v1/whatever3

特定の EC2 関連のモジュールにデフォルトの AWS リージョンを設定します。

    - hosts: localhost
      vars:
        my_region: us-west-2
      module_defaults:
        ec2:
          region: '{{ my_region }}'
        ec2_instance_info:
          region: '{{ my_region }}'
        ec2_vpc_net_info:
          region: '{{ my_region }}'
    
.. _module_defaults_groups:

モジュールのデフォルトグループ
----------------------

.. versionadded:: 2.7

Ansible 2.7 は preview-status 機能を追加して、共通のパラメーターセットを共有するモジュールをグループ化します。これにより、
クラウドモジュールなどの API ベースのモジュールを多用して、Playbook を簡単に作成できます。

+-------+---------------------------+-----------------+
| Group | Purpose                   | Ansible Version |
+=======+===========================+=================+
| aws   | Amazon Web Services       | 2.7             |
+-------+---------------------------+-----------------+
| azure | Azure                     | 2.7             |
+-------+---------------------------+-----------------+
| gcp   | Google Cloud Platform     | 2.7             |
+-------+---------------------------+-----------------+
| k8s   | Kubernetes                | 2.8             |
+-------+---------------------------+-----------------+
| os    | OpenStack                 | 2.8             |
+-------+---------------------------+-----------------+

グループ名の前に `group/` を追加して (例: `group/aws`)、`module_defaults` でグループを使用します。

Playbook では、一般的な AWS リージョンの設定など、モジュールのグループ全体にモジュールのデフォルトを設定できます。

.. code-block:: YAML

    # example_play.yml
    - hosts: localhost
      module_defaults:
        group/aws:
          region: us-west-2
      tasks:
      - aws_s3_bucket_info:
      # now the region is shared between both info modules
      - ec2_ami_info:
          filters:
            name: 'RHEL*7.5*'
