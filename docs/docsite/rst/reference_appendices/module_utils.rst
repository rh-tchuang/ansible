.. _ansible.module_utils:
.. _module_utils:

***************************************************************
Ansible 参考資料:モジュールユーティリティー
***************************************************************

このページでは、
Python で Ansible モジュールを記述するときに役立つユーティリティーをまとめています。


AnsibleModule
--------------

この機能を使用するには、モジュールに ``from ansible.module_utils.basic import AnsibleModule`` を追加します。

.. autoclass:: ansible.module_utils.basic.AnsibleModule
   :members:


基本
------

この機能を使用するには、モジュールに ``import ansible.module_utils.basic`` を追加します。

.. automodule:: ansible.module_utils.basic
   :members:
