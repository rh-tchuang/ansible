.. \_junos\_platform\_options:

***************************************
Junos OS プラットフォームのオプション
***************************************

Juniper Junos OS は、複数の接続に対応します。このページには、各接続が Ansible でどのように機能するか、およびその使用方法に関する詳細が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                   CLI                                         NETCONF

                          ``junos_netconf`` および ``junos_command``       NETCONF を有効にする ``junos_netconf`` ,
                          モジュールのみ                      以外のすべてのモジュール
    ====================  ==========================================  =========================
    プロトコル              SSH                                         SSH 経由の XML

    認証情報           (存在する場合は) SSH キー / SSH-agent を使用します。        (存在する場合は) SSH キー / SSH-agent を使用します。

                          パスワードを使用する場合は ``-u myuser -k`` を許可します。  パスワードを使用する場合は ``-u myuser -k`` を許可します。

    間接アクセス       bastion (ジャンプホスト) を経由                   bastion (ジャンプホスト) を経由

    接続設定   ``ansible_connection: network_cli``         ``ansible_connection: netconf``

    |enable_mode Junos OS は対応していません。 Junos OS は対応していません。

    返されるデータ形式 "stdout[0]." * json: "result[0]['software-information'][0]['host-name'][0]['data'] foo lo0"
                                                                      * text: ``result[1].interface-information[0].physical-interface[0].name[0].data foo lo0``
                                                                      * xml: ``result[1].rpc-reply.interface-information[0].physical-interface[0].name[0].data foo lo0``
    ====================  ==========================================  =========================

.. |enable\_mode| replace::Enable モード |br| (権限昇格)


レガシー Playbook の場合、Ansible はすべての JUNOS モジュールで ``ansible_connection=local`` に対応します。できるだけ早期に ``ansible_connection=netconf`` または ``ansible_connection=network_cli`` を使用するモダナイゼーションが推奨されます。

Ansible での CLI の使用
====================

CLI インベントリーの例 ``[junos:vars]``
--------------------------------------

.. code-block:: yaml

   \[junos:vars]
   ansible\_connection=network\_cli
   ansible\_network\_os=junos
   ansible\_user=myuser
   ansible\_password=!vault...
   ansible\_ssh\_common\_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Retrieve Junos OS version
     junos\_command:
       commands: show version
     when: ansible\_network\_os == 'junos'


Ansible での NETCONF の使用
========================

NETCONF の有効化
----------------

NETCONF を使用してスイッチに接続する前に、以下を行う必要があります。

- ``pip install ncclient`` を使用して、コントロールノードに python パッケージ ``ncclient`` をインストールします。
- Junos OS デバイスの netconf の有効化

Ansible 経由で新規スイッチで NETCONF を有効にするには、CLI 接続で ``junos_netconf`` モジュールを使用します。上記の CLI の例と同様にプラットフォームレベルの変数を設定し、以下のような Playbook のタスクを実行します。

.. code-block:: yaml

   - name:Enable NETCONF
     connection: network\_cli
     junos\_netconf:
     when: ansible\_network\_os == 'junos'

NETCONF を有効にしたら、変数を変更して NETCONF 接続を使用します。

NETCONF インベントリーの例 ``[junos:vars]``
------------------------------------------

.. code-block:: yaml

   \[junos:vars]
   ansible\_connection=netconf
   ansible\_network\_os=junos
   ansible\_user=myuser
   ansible\_password=!vault |
   ansible\_ssh\_common\_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


NETCONF タスクの例
--------------------

.. code-block:: yaml

   - name:Backup current switch config (junos)
     junos\_config:
       backup: yes
     register: backup\_junos\_location
     when: ansible\_network\_os == 'junos'


.. include:: shared\_snippets/SSH\_warning.txt
