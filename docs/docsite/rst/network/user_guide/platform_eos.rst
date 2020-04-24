.. \_eos\_platform\_options:

***************************************
EOS プラットフォームのオプション
***************************************

Arista EOS は、複数の接続に対応します。このページには、各接続が Ansible でどのように機能するか、およびその使用方法に関する詳細が記載されています。

.. contents:: トピック

利用可能な接続
================================================================================

.. table::
    :class: documentation-table

    ====================  ==========================================  =========================
    ..                   CLI                                         eAPI
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
                                                                      ``transport: eapi`` とともに使用します

    |enable_mode|         サポート対象: |br|                             サポート対象: |br|

                          * ``ansible_become: yes`` を               * ``httpapi`` を
                            ``ansible_become_method: enable`` とともに使用します。      ``ansible_become: yes`` および
                                                                        ``ansible_become_method: enable`` とともに使用します。

                                                                      * ``local`` を
                                                                        ``provider`` ディレクトリーの
                                                                        ``authorize: yes`` および
                                                                        ``auth_pass:`` とともに使用します。

    返されるデータ形式  ``stdout[0].``                              ``stdout[0].messages[0].``
    ====================  ==========================================  =========================

.. |enable\_mode| replace::Enable モード |br| (権限昇格)


レガシー Playbook の場合でも、EOS は ``ansible_connection: local`` に対応します。できるだけ早期に ``ansible_connection: network_cli`` または ``ansible_connection: httpapi`` を使用するモダナイゼーションが推奨されます。

Ansible での CLI の使用
====================

CLI の例: ``group_vars/eos.yml``
----------------------------------

.. code-block:: yaml

   ansible\_connection: network\_cli
   ansible\_network\_os: eos
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

   - name:Backup current switch config (eos)
     eos\_config:
       backup: yes
     register: backup\_eos\_location
     when: ansible\_network\_os == 'eos'



Ansible での eAPI の使用
=====================

EAPI の有効化
-------------

eAPI を使用してスイッチに接続するには、eAPI を有効にする必要があります。Ansible 経由で新規スイッチで eAPI を有効にするには、CLI 接続で ``eos_eapi`` モジュールを使用します。上記の CLI の例のように group\_vars/EOS.yml を設定し、以下のような Playbook タスクを実行します。

.. code-block:: yaml

   - name:Enable eAPI
      eos\_eapi:
          enable\_http: yes
          enable\_https: yes
      become: true
      become\_method: enable
      when: ansible\_network\_os == 'eos'

HTTP/HTTPS 接続を有効にするオプションの詳細は、:ref:`eos_eapi <eos_eapi_module>` モジュールのドキュメントを参照してください。

eAPI が有効になったら、eAPI 接続を使用するように ``group_vars/eos.yml`` を変更します。

eAPI の例: ``group_vars/eos.yml``
-----------------------------------

.. code-block:: yaml

   ansible\_connection: httpapi
   ansible\_network\_os: eos
   ansible\_user: myuser
   ansible\_password: !vault...
   ansible\_become: yes
   ansible\_become\_method: enable
   proxy\_env:
     http\_proxy: http://proxy.example.com:8080

- (Web プロキシーを経由せず) ホストに直接アクセスしている場合は、``proxy_env`` 設定を削除できます。
- ``https`` を使用して Web プロキシー経由でホストにアクセスする場合は、``http_proxy`` を ``https_proxy`` に変更します。


eAPI タスクの例
-----------------

.. code-block:: yaml

   - name:Backup current switch config (eos)
     eos\_config:
       backup: yes
     register: backup\_eos\_location
     environment: "{{ proxy\_env }}"
     when: ansible\_network\_os == 'eos'

この例では、``group_vars`` で定義された ``proxy_env`` 変数は、タスクのモジュールの ``environment`` オプションに渡されます。

``connection: local`` を使用した eAPI の例
-----------------------------------------

``group_vars/eos.yml``:

.. code-block:: yaml

   ansible\_connection: local
   ansible\_network\_os: eos
   ansible\_user: myuser
   ansible\_password: !vault...
   eapi:
     host: "{{ inventory\_hostname }}"
     transport: eapi
     authorize: yes
     auth\_pass: !vault...
   proxy\_env:
     http\_proxy: http://proxy.example.com:8080

eAPI タスク:

.. code-block:: yaml

   - name:Backup current switch config (eos)
     eos\_config:
       backup: yes
       provider: "{{ eapi }}"
register: backup\_eos\_location
environment: "{{ proxy\_env }}"
     when: ansible\_network\_os == 'eos'

この例では、``group_vars`` で定義された 2 つの変数がタスクのモジュールに渡されます。

- ``eapi`` 変数は、モジュールの ``provider`` オプションに渡されます。
- ``proxy_env`` 変数は、モジュールの ``environment`` オプションに渡されます。

.. include:: shared\_snippets/SSH\_warning.txt
