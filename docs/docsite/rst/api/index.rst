:orphan:

*************************
Ansible API のドキュメント
*************************

Ansible API はただいま準備中です。属性、クラス、関数、メソッド、およびモジュールのスタブ参照の説明は、今後追加されます。
``ansible.module_utils.basic`` および ``AnsibleModule`` に含まれる :ref:`モジュールユーティリティー<ansible.module_utils>` は、参照 & 付録のセクションで説明されています。

.. contents::
   :local:

属性
==========

.. py:attribute::AnsibleModule.params

モジュールで受け入れられるパラメーターです。

.. py:attribute:: ansible.module\_utils.basic.ANSIBLE\_VERSION

.. py:attribute:: ansible.module\_utils.basic.SELINUX\_SPECIAL\_FS

ansibleModule.\_selinux\_special\_fs が導入されたため、非推奨となりました。

.. py:attribute::AnsibleModule.ansible\_version

.. py:attribute::AnsibleModule.\_debug

.. py:attribute::AnsibleModule.\_diff

.. py:attribute::AnsibleModule.no\_log

.. py:attribute::AnsibleModule.\_selinux\_special\_fs

(以前の ansible.module\_utils.basic.SELINUX\_SPECIAL\_FS)

.. py:attribute::AnsibleModule.\_syslog\_facility

.. py:attribute:: self.playbook

.. py:attribute:: self.play

.. py:attribute:: self.task

.. py:attribute:: sys.path


クラス
=======

.. py:class:: ``ansible.module_utils.basic.AnsibleModule``
   :noindex:

AnsibleModule の基本的なユーティリティーです。

.. py:class::AnsibleModule

Ansible モジュールのメインクラスです。


関数
=========

.. py:function:: ansible.module\_utils.basic.\_load\_params()

パラメーターをロードします。


メソッド
=======

.. py:method::AnsibleModule.log()

Ansible の出力をログに記録します。

.. py:method::AnsibleModule.debug()

Ansible をデバッグします。

.. py:method::Ansible.get\_bin\_path()

実行可能ファイルのパスを取得します。

.. py:method::AnsibleModule.run\_command()

Ansible モジュール内でコマンドを実行します。

.. py:method:: module.fail\_json()

終了して、失敗を返します。

.. py:method:: module.exit\_json()

終了して、出力を返します。


モジュール
=======

.. py:module:: ansible.module\_utils

.. py:module:: ansible.module\_utils.basic

.. py:module:: ansible.module\_utils.url
