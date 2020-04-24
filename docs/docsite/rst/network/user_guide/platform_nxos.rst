.. \_nxos\_platform\_options:

***************************************
NXOS プラットフォームのオプション
***************************************

Cisco NXOS は、複数の接続に対応します。このページには、各接続が Ansible でどのように機能するか、およびその使用方法に関する詳細が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                   CLI                                         NX-API
    ====================  ==========================================  =========================
    プロトコル              SSH                                         HTTP(S)

    認証情報           (存在する場合は) SSH キー / SSH-agent を使用します。        
                                                                      (存在する場合は) HTTPS 認証情報を使用します。
                          パスワードを使用する場合は ``-u myuser -k`` を許可します。

    間接アクセス       bastion (ジャンプホスト) を経由                   Web プロキシーを経由

    接続設定   ``ansible_connection: network_cli``         ``ansible_connection: httpapi``

                                                                      または

                                                                      ``provider`` ディクショナリーで、
                                                                      ``ansible_connection: local`` を
                                                                      ``auth_pass:`` とともに使用します。

    |enable_mode|         サポート対象: ``ansible_become: yes`` を      NX-API では対応していません。
                          ``ansible_become_method: enable`` および
                          ``ansible_become_password:`` とともに使用します。

    返されるデータ形式  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================

.. |enable\_mode| replace::Enable モード |br| (権限昇格) |br| 2.5.3 以降で対応


レガシー Playbook の場合でも、NXOS は ``ansible_connection: local`` に対応します。できるだけ早期に ``ansible_connection: network_cli`` または ``ansible_connection: httpapi`` を使用するモダナイゼーションが推奨されます。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/nxos.yml``
-----------------------------------

.. code-block:: yaml

   ansible\_connection: network\_cli
   ansible\_network\_os: nxos
   ansible\_user: myuser
   ansible\_password: !vault...
   ansible\_become: yes
   ansible\_become\_method: enable
   ansible\_become\_password: !vault...
   ansible\_ssh\_common\_args: '-o ProxyCommand="ssh -W %h:%p -q bastion01"'


- SSH キー (ssh-agent を含む) を使用している場合は、``ansible_password`` 設定を削除できます。
- (bastion/ジャンプホスト を経由せず) ホストに直接アクセスしている場合は、``ansible_ssh_common_args`` 設定を削除できます。
- bastion/ジャンプホスト 経由でホストにアクセスしている場合は、SSH パスワードを ``ProxyCommand`` ディレクティブに含めることができません。(``ps`` 出力などで) シークレットの漏えいを防ぐために、SSH は環境変数によるパスワードの提供に対応していません。

CLI タスクの例
----------------

.. code-block:: yaml

   - name:Backup current switch config (nxos)
     nxos\_config:
       backup: yes
     register: backup\_nxos\_location
     when: ansible\_network\_os == 'nxos'



Ansible での NX-API の使用
=======================

NX-API の有効化
---------------

NX-API を使用してスイッチに接続するには、NX-API を有効にする必要があります。Ansible 経由で新規スイッチで NX-API を有効にするには、CLI 接続で ``nxos_nxapi`` モジュールを使用します。上記の CLI の例のように group\_vars/nxos.yml を設定し、以下のような Playbook タスクを実行します。

.. code-block:: yaml

   - name:NX-API の有効化
      nxos\_nxapi:
          enable\_http: yes
          enable\_https: yes
      when: ansible\_network\_os == 'nxos'

HTTP/HTTPS およびローカル http を有効にするオプションの詳細は、:ref:`nxos_nxapi <nxos_nxapi_module>` モジュールのドキュメントを参照してください。

NX-API が有効になったら、NX-API 接続を使用するように ``group_vars/nxos.yml`` を変更します。

NX-API ``group_vars/nxos.yml`` の例
--------------------------------------

.. code-block:: yaml

   ansible\_connection: httpapi
   ansible\_network\_os: nxos
   ansible\_user: myuser
   ansible\_password: !vault...
   proxy\_env:
     http\_proxy: http://proxy.example.com:8080

- (Web プロキシーを経由せず) ホストに直接アクセスしている場合は、``proxy_env`` 設定を削除できます。
- ``https`` を使用して Web プロキシー経由でホストにアクセスする場合は、``http_proxy`` を ``https_proxy`` に変更します。


NX-API タスクの例
-------------------

.. code-block:: yaml

   - name:Backup current switch config (nxos)
     nxos\_config:
       backup: yes
     register: backup\_nxos\_location
     environment: "{{ proxy\_env }}"
     when: ansible\_network\_os == 'nxos'

この例では、``group_vars`` で定義された ``proxy_env`` 変数は、タスクのモジュールで使用される ``environment`` オプションに渡されます。

.. include:: shared\_snippets/SSH\_warning.txt

Cisco Nexus Platform のサポートマトリックス
===================================

以下のプラットフォームおよびソフトウェアのバージョンは、Cisco が本バージョンの Ansible で機能することが認定されています。

.. table:: プラットフォーム/ソフトウェア最小要件
     :align: center

     ===================  =====================
     サポートされるプラットフォームの最小 NX OS バージョン
     ===================  =====================
     Cisco Nexus N3k      7.0(3)I2(5) 以降
     Cisco Nexus N9k      7.0(3)I2(5) 以降
     Cisco Nexus N5k      7.3(0)N1(1) 以降
     Cisco Nexus N6k      7.3(0)N1(1) 以降
     Cisco Nexus N7k      7.3(0)D1(1) 以降
     ===================  =====================

.. table:: プラットフォームモデル
     :align: center

     ========  ==============================================
     プラットフォーム  説明
     ========  ==============================================
     N3k       サポートには、N30xx モデル、N31xx モデル、および N35xx モデルが含まれます。
     N5k       サポートには、N5xxx の全モデルが含まれます。
     N6k       サポートには、N6xxx の全モデルが含まれます。
     N7k       サポートには、N7xxx の全モデルが含まれます。
     N9k       サポートには、N9xxx の全モデルが含まれます。
     ========  ==============================================
