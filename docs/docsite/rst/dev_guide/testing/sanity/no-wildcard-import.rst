:orphan:

ワイルドカードの import は使用しない
==================

:code:`import *` の使用は、名前空間を汚染し、
デバッグを妨害し、コードの静的分析を妨害する悪い習慣です。 このような理由から、
Ansible コードでは、:code:`import *` の使用を制限する必要があります。 代わりに、
必要な特定の名前をインポートするようにコードを変更してください。

未修正コードの例:

.. code-block:: python

    from ansible.module_utils.six import *
    if isinstance(variable, string_types):
        do_something(variable)

    from ansible.module_utils.basic import *
    module = AnsibleModule()

修正されたコードの例:

.. code-block:: python

    from ansible.module_utils import six
    if isinstance(variable, six.string_types):
        do_something(variable)

    from ansible.module_utils.basic import AnsibleModule
    module = AnsibleModule()
