.. _iosxr_platform_options:

***************************************
IOS-XR プラットフォームのオプション
***************************************

IOS-XR は、複数の接続に対応します。このページには、各接続が Ansible でどのように機能するか、およびその使用方法に関する詳細が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                   CLI                                         NETCONF

                                                                      ``iosxr_banner``、
                                                                      ``iosxr_interface``、``iosxr_logging``、
                                                                      ``iosxr_system``、``iosxr_user`` モジュールに限定
    ====================  ==========================================  =========================
    プロトコル              SSH                                         SSH 経由の XML

    認証情報           (存在する場合は) SSH キー / SSH-agent を使用します。        (存在する場合は) SSH キー / SSH-agent を使用します。

                          パスワードを使用する場合は ``-u myuser -k`` を許可します。  パスワードを使用する場合は ``-u myuser -k`` を許可します。

    間接アクセス       bastion (ジャンプホスト) を経由                   bastion (ジャンプホスト) を経由

    接続設定   ``ansible_connection: network_cli``         ``ansible_connection: netconf``

    |enable_mode|         対応していません。                               対応していません。

    返されるデータ形式  各モジュールのモジュールドキュメントを参照してください。    各モジュールのモジュールドキュメントを参照してください。
    ====================  ==========================================  =========================

.. |enable_mode| replace::Enable モード |br| (権限昇格)


レガシー Playbook の場合、Ansible はすべての IOS-XR モジュールで ``ansible_connection=local`` に対応します。できるだけ早期に ``ansible_connection=netconf`` または ``ansible_connection=network_cli`` を使用するモダナイゼーションが推奨されます。

Ansible での CLI の使用
====================

CLI インベントリーの例 ``[iosxr:vars]``
--------------------------------------

.. code-block:: yaml

   [iosxr:vars]
   ansible_connection=network_cli
   ansible_network_os=iosxr
   ansible_user=myuser
   ansible_password=!vault...
   ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Retrieve IOS-XR version
     iosxr_command:
       commands: show version
     when: ansible_network_os == 'iosxr'


Ansible での NETCONF の使用
========================

NETCONF の有効化
----------------

NETCONF を使用してスイッチに接続する前に、以下を行う必要があります。

- ``pip install ncclient`` を使用して、コントロールノードに python パッケージ ``ncclient`` をインストールします。
- Cisco IOS-XR デバイスで NETCONF を有効にします。

Ansible 経由で新しいスイッチで NETCONF を有効にするには、CLI 接続で ``iosxr_netconf`` モジュールを使用します。上記の CLI の例と同様にプラットフォームレベルの変数を設定し、以下のような Playbook のタスクを実行します。

.. code-block:: yaml

   - name:Enable NETCONF
     connection: network_cli
     iosxr_netconf:
     when: ansible_network_os == 'iosxr'

NETCONF を有効にしたら、変数を変更して NETCONF 接続を使用します。

NETCONF インベントリーの例: ``[iosxr:vars]``
------------------------------------------

.. code-block:: yaml

   [iosxr:vars]
   ansible_connection=netconf
   ansible_network_os=iosxr
   ansible_user=myuser
   ansible_password=!vault |
   ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


NETCONF タスクの例
--------------------

.. code-block:: yaml

   - name:Configure hostname and domain-name
     iosxr_system:
       hostname: iosxr01
       domain_name: test.example.com
       domain_search:
         - ansible.com
         - redhat.com
         - cisco.com

.. include:: shared_snippets/SSH_warning.txt
