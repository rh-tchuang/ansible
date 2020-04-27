.. _netconf_enabled_platform_options:

***************************************
Netconf が有効なプラットフォームオプション
***************************************

このページには、netconf 接続が Ansible でどのように機能するか、およびその使用方法に関する詳細が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================
.. table::
    :class: documentation-table

    ====================  ==========================================
    ..                   NETCONF

                          NETCONF を有効にする
                          ``junos_netconf`` 以外のすべてのモジュール
    ====================  ==========================================
    プロトコル              SSH 経由の XML

    認証情報           SSH キー / SSH-agent (存在する場合) を使用します。

                          パスワードを使用する場合は ``-u myuser -k`` を許可します。

    間接アクセス       bastion (ジャンプホスト) を経由

    接続設定   ``ansible_connection: netconf``
    ====================  ==========================================


レガシー Playbook の場合、Ansible は netconf_config モジュールに対してのみ ``ansible_connection=local`` に対応します。できるだけ早期に ``ansible_connection=netconf`` を使用するモダナイゼーションが推奨されます。

Ansible での NETCONF の使用
========================

NETCONF の有効化
----------------

NETCONF を使用してスイッチに接続する前に、以下を行う必要があります。

- ``pip install ncclient`` を使用して、コントロールノードに Python パッケージ ``ncclient`` をインストールします。
- Junos OS デバイスの netconf の有効化

Ansible 経由で新規スイッチで NETCONF を有効にするには、CLI 接続でプラットフォーム固有のモジュールを使用するか、手動で設定します。
たとえば、上記の CLI の例と同様にプラットフォームレベルの変数を設定し、以下のような Playbook のタスクを実行します。

.. code-block:: yaml

   - name:Enable NETCONF
     connection: network_cli
     junos_netconf:
     when: ansible_network_os == 'junos'

NETCONF を有効にしたら、変数を変更して NETCONF 接続を使用します。

NETCONF インベントリーの例 ``[junos:vars]``
------------------------------------------

.. code-block:: yaml

   [junos:vars]
   ansible_connection=netconf
   ansible_network_os=junos
   ansible_user=myuser
   ansible_password=!vault |


NETCONF タスクの例
--------------------

.. code-block:: yaml

   - name:Backup current switch config
     netconf_config:
       backup: yes
     register: backup_junos_location

設定可能な変数を含む NETCONF タスクの例
------------------------------------------------

.. code-block:: yaml

   - name: configure interface while providing different private key file path
     netconf_config:
       backup: yes
     register: backup_junos_location
     vars:
       ansible_private_key_file: /home/admin/.ssh/newprivatekeyfile

注記: netconf 接続プラグインの設定可能な変数は、「:ref:`netconf <netconf_connection>`」を参照してください。

Bastion/Jumphost の設定
------------------------------
ジャンプホストを使用して NETCONF 対応のデバイスに接続するには、``ANSIBLE_NETCONF_SSH_CONFIG`` 環境変数を設定する必要があります。

``ANSIBLE_NETCONF_SSH_CONFIG`` は、以下のいずれかに設定できます。
  - 1 または TRUE (デフォルトの SSH 設定ファイル ~/.ssh/config の使用を開始するため)。
  - カスタムの SSH 設定ファイルへの絶対パス。

SSH 設定ファイルは以下のようになります。 

.. code-block:: ini

  Host *
    proxycommand ssh -o StrictHostKeyChecking=no -W %h:%p jumphost-username@jumphost.fqdn.com
    StrictHostKeyChecking no

ジャンプホストの認証は、鍵ベースの認証を使用する必要があります。

SSH 設定ファイルで使用する秘密鍵のいずれかを指定できます。

.. code-block:: ini

  IdentityFile "/absolute/path/to/private-key.pem"

または、ssh-agent を使用できます。

ansible_network_os 自動検出
---------------------------------

ホストに対して ``ansible_network_os`` が指定されていない場合、Ansible は使用する ``network_os`` プラグインを自動的に検出しようとします。

``ansible_network_os`` 自動検出は、``auto`` を ``ansible_network_os`` として使用することで開始することもできます。(注記: 以前は、``auto`` の代わりに ``default`` が使用されていました。

.. include:: shared_snippets/SSH_warning.txt
