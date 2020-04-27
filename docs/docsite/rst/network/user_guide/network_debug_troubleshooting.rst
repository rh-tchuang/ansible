.. _network_debug_troubleshooting:

***************************************
ネットワークデバッグおよびトラブルシューティングガイド
***************************************

.. contents::
   :local:


はじめに
============

Ansible バージョン 2.1 以降、使い慣れた Ansible モデルで Playbook のオーサリングとモジュール開発を使用して、異種ネットワークデバイスを管理できるようになりました。Ansible は、SSH 経由の CLI および API (利用可能な場合) のトランスポートの両方を使用して、増加するネットワークデバイスに対応します。

本セクションでは、Ansible 2.3 でネットワークモジュールをデバッグし、トラブルシューティングを行う方法を説明します。



トラブルシューティングの方法
===================

本セクションでは、ネットワークモジュールに関するトラブルシューティングを説明します。

通常、エラーは以下のカテゴリーのいずれかに分類されます。

:認証の問題:
  * 認証情報を正しく指定できない
  * リモートデバイス (ネットワークスイッチ/ルーター) が他の認証方法にフォールバックしない
  * SSH 鍵の問題
:タイムアウトの問題:
  * 大量のデータを取得しようとすると発生することがある
  * 認証の問題を実際にマスクする可能性がある
:Playbook の問題:
  * ``ProxyCommand`` の代わりに ``delegate_to`` を使用する。詳細は、「:ref:`ネットワークプロキシーガイド<network_delegate_to_vs_ProxyCommand>`」を参照してください。

.. warning:: ``unable to open shell``

  Ansible 2.3 では、``unable to open shell`` メッセージが新しくなりました。これは、``ansible-connection`` デーモンを実行して、
  リモートネットワークデバイスと対話することに失敗したことを示しています。これは通常、認証に問題があることを意味します。詳細は、本ガイドの
  「認証および接続の問題」セクションを参照してください。

.. _enable_network_logging:

ネットワークロギングの有効化とログファイルの読み取り方法
-------------------------------------------------------

**プラットフォーム:** 任意

Ansible 2.3 では、Ansible Networking モジュールに関する問題の診断およびトラブルシューティングに役立つように、ロギングが改善されています。

ロギングは非常に詳細であるため、デフォルトでは無効になっています。これは、ansible-playbook を実行するマシンである ansible-controller の :envvar:`ANSIBLE_LOG_PATH` オプションおよび :envvar:`ANSIBLE_DEBUG` オプションで有効にできます。

``ansible-playbook`` を実行する前に、以下のコマンドを実行してロギングを有効にします。

   # Specify the location for the log file
   export ANSIBLE_LOG_PATH=~/ansible.log
   # Enable Debug
   export ANSIBLE_DEBUG=True

   # Run with 4*v for connection level verbosity
   ansible-playbook -vvvv ...

Ansible の実行が完了したら、ansible-controller で作成されたログファイルを確認できます。

.. code::

  less $ANSIBLE_LOG_PATH

  2017-03-30 13:19:52,740 p=28990 u=fred |  creating new control socket for host veos01:22 as user admin
  2017-03-30 13:19:52,741 p=28990 u=fred |  control socket path is /home/fred/.ansible/pc/ca5960d27a
  2017-03-30 13:19:52,741 p=28990 u=fred |  current working directory is /home/fred/ansible/test/integration
  2017-03-30 13:19:52,741 p=28990 u=fred |  using connection plugin network_cli
  ...
  2017-03-30 13:20:14,771 paramiko.transport userauth is OK
  2017-03-30 13:20:15,283 paramiko.transport Authentication (keyboard-interactive) successful!
  2017-03-30 13:20:15,302 p=28990 u=fred |  ssh connection done, setting terminal
  2017-03-30 13:20:15,321 p=28990 u=fred |  ssh connection has completed successfully
  2017-03-30 13:20:15,322 p=28990 u=fred |  connection established to veos01 in 0:00:22.580626


このログ通知は、以下のようになります。

* ``p=28990`` は、``ansible-connection`` プロセスの PID (プロセス ID) です。
* ``u=fred`` は、ansible を `実行` しているユーザーです (接続しようとしているリモートユーザーではありません)。
* ``creating new control socket for host veos01:22 as user admin`` は、host:port をユーザーとします。
* ``control socket path is`` は、永続的な接続ソケットが作成されるディスクの場所です。
* ``using connection plugin network_cli`` は、永続的な接続が使用されていることを示しています。
* ``connection established to veos01 in 0:00:22.580626`` は、リモートデバイスでシェルを取得するのに要した時間になります。


.. 注記:Port None ``creating new control socket for host veos01:None``

   ログでポートが ``None`` と報告される場合は、デフォルトのポートが使用されていることを示しています。
   今後の Ansible リリースではこのメッセージが改善され、ポートが常にログに記録されるようになります。

ログファイルは詳細情報であるため、grep を使用して特定の情報を検索できます。たとえば、``creating new control socket for host`` 行で ``pid`` を確認したら、他の接続ログエントリーを検索できます。

  grep "p=28990" $ANSIBLE_LOG_PATH


ネットワークデバイスの対話ロギングの有効化
----------------------------------------------

**プラットフォーム:** 任意

Ansible 2.8 の機能により、デバイスの対話のログがログファイルに追加され、
Ansible Networking モジュールに関する問題の診断とトラブルシューティングに役立ちます。メッセージは、上記のセクションで説明されているように、Ansible 設定ファイルの ``log_path`` 設定オプション、
または :envvar:`ANSIBLE_LOG_PATH` を設定することで、参照されるファイルに記録されます。

.. warning::
  デバイスの対話メッセージは、ターゲットデバイスで実行されたコマンドと返された応答で構成されます。
  このログデータには、パスワードを含む機密情報がプレーンテキストで含まれる可能性があるため、デフォルトでは無効になっています。
  さらに、データの偶発的な漏洩を防ぐために、
  この設定を有効にすると、すべてのタスクで警告が表示され、有効になっているホストと、データが記録されている場所が指定されます。

このオプションを有効にした場合のセキュリティーへの影響を完全に理解してください。デバイス対話ロギングは、設定ファイルで設定するか、環境を設定してグローバルに有効にするか、または特殊な変数をタスクに渡すことでタスクごとに有効にすることができます。

``ansible-playbook`` を実行する前に、以下のコマンドを実行してロギングを有効にします。

   # Specify the location for the log file
   export ANSIBLE_LOG_PATH=~/ansible.log


特定のタスクのデバイス対話ログを有効にします。

.. code-block:: yaml

  - name: get version information
    ios_command:
      commands:
        - show version
    vars:
      ansible_persistent_log_messages: True


これをグローバル設定にするには、以下を ``ansible.cfg`` ファイルに追加します。

.. code-block:: ini

   [persistent_connection]
   log_messages = True

または、環境変数 `ANSIBLE_PERSISTENT_LOG_MESSAGES` を有効にします。

   # Enable device interaction logging
   export ANSIBLE_PERSISTENT_LOG_MESSAGES=True

接続の初期化時にタスク自体が失敗する場合は、このオプションをグローバルに有効にすることが推奨されます。
個別のタスクが断続的に失敗する場合は、
そのタスクに対してこのオプションを有効にして根本原因を見つけることができます。

Ansible の実行が完了したら、ansible-controller で作成されたログファイルを確認できます。

.. note:: このオプションを有効にすると、機密情報がログファイルに記録されてセキュリティの脆弱性が生じる可能性があるため、
          セキュリティーの影響を十分に理解してください。


エラーの分離
------------------

**プラットフォーム:** 任意

トラブルシューティングにおけるあらゆる作業と同様に、テストケースをできるだけ簡略化することが重要です。

Ansible の場合は、1 つのリモートデバイスに対してのみ実行するようにすることでこれを実行できます。

* ``ansible-playbook --limit switch1.example.net...`` の使用
* アドホックコマンド ``ansible`` の使用

`ad-hoc` は、``/usr/bin/ansible-playbook`` というオーケストレーション言語ではなく、Ansible を実行して ``/usr/bin/ansible`` を使用してクイックコマンドを実行することを意味します。この場合は、リモートデバイスで 1 つのコマンドを実行してみると、接続性を確認できます。

  ansible -m eos_command -a 'commands=?' -i inventory switch1.example.net -e 'ansible_connection=local' -u admin -k

上記の例では、以下を行います。

* インベントリーファイル ``inventory`` で指定された ``switch1.example.net`` に接続する
* ``eos_command`` モジュールを使用する
* ``?`` コマンドを実行する
* ユーザー名 ``admin`` を使用して接続する
* ``-k`` を指定して ssh パスワードを要求するように Ansible に通知する

SSH キーが正しく設定されている場合は、``-k`` パラメーターを指定する必要はありません。

それでも接続が失敗した場合は、これを enable_network_logging パラメーターと組み合わせることができます。例::

   # Specify the location for the log file
   export ANSIBLE_LOG_PATH=~/ansible.log
   # Enable Debug
   export ANSIBLE_DEBUG=True
   # Run with 4*v for connection level verbosity
   ansible -m eos_command -a 'commands=?' -i inventory switch1.example.net -e 'ansible_connection=local' -u admin -k

次に、ログファイルを確認し、このドキュメントの残りの部分で、関連するエラーメッセージを見つけます。

..他の認証方法の詳細は、LINKTOAUTHHOWTODOCS を参照してください。

.. _socket_path_issue:

カテゴリー "socket_path issue"
============================

**プラットフォーム:** 任意

``socket_path does not exist or cannot be found`` メッセージおよび ``unable to connect to socket`` メッセージは、Ansible 2.5 で導入されました。このメッセージは、リモートネットワークデバイスとの通信に使用されるソケットが利用できないか、存在しないことを示しています。


例:

.. code-block:: none

   fatal: [spine02]: FAILED! => {
       "changed": false,
       "failed": true,
       "module_stderr": "Traceback (most recent call last):\n  File \"/tmp/ansible_TSqk5J/ansible_modlib.zip/ansible/module_utils/connection.py\", line 115, in _exec_jsonrpc\nansible.module_utils.connection.ConnectionError: socket_path does not exist or cannot be found\n",
       "module_stdout": "",
       "msg": "MODULE FAILURE",
       "rc": 1
   }

または

.. code-block:: none

   fatal: [spine02]: FAILED! => {
       "changed": false,
       "failed": true,
       "module_stderr": "Traceback (most recent call last):\n  File \"/tmp/ansible_TSqk5J/ansible_modlib.zip/ansible/module_utils/connection.py\", line 123, in _exec_jsonrpc\nansible.module_utils.connection.ConnectionError: unable to connect to socket\n",
       "module_stdout": "",
       "msg": "MODULE FAILURE",
       "rc": 1
   }

解決するためのヒント:

「:ref:`ネットワークロギングの有効化<enable_network_logging>`」の手順に従います。

ログファイルから特定されたエラーメッセージが以下の場合は、

.. code-block:: yaml

   2017-04-04 12:19:05,670 p=18591 u=fred |  command timeout triggered, timeout value is 30 secs

または

.. code-block:: yaml

   2017-04-04 12:19:05,670 p=18591 u=fred |  persistent connection idle timeout triggered, timeout value is 30 secs

:ref:`タイムアウトの問題 <timeout_issues>` に記載されている手順に従います。


.. _unable_to_open_shell:

カテゴリー "Unable to open shell"
===============================


**プラットフォーム:** 任意

Ansible 2.3 では、``unable to open shell`` メッセージが新たに追加されました。このメッセージは、``ansible-connection`` デーモンがリモートネットワークデバイスと正常に対話できないことを示します。これは通常、認証に問題があることを意味します。これは「catch all」メッセージであるため、:ref:logging`a_note_about_logging` を有効にして根本的な問題を見つける必要があります。



例:

.. code-block:: none

  TASK [prepare_eos_tests : enable cli on remote device] **************************************************
  fatal: [veos01]:FAILED! => {"changed": false, "failed": true, "msg": "unable to open shell"}


または


.. code-block:: none

   TASK [ios_system : configure name_servers] *************************************************************
   task path:
   fatal: [ios-csr1000v]: FAILED! => {
       "changed": false,
       "failed": true,
       "msg": "unable to open shell",
   }

解決するためのヒント:

enable_network_logging_ に記載の手順に従います。

ログファイルからエラーメッセージが特定できたら、特定の解決方法は、本ガイドのその他のセクションを参照してください。



Error: "[Errno -2]Name or service not known"
---------------------------------------------

**プラットフォーム:** 任意

接続しようとしているリモートホストに到達できないことを示します。

例:

.. code-block:: yaml

   2017-04-04 11:39:48,147 p=15299 u=fred |  control socket path is /home/fred/.ansible/pc/ca5960d27a
   2017-04-04 11:39:48,147 p=15299 u=fred |  current working directory is /home/fred/git/ansible-inc/stable-2.3/test/integration
   2017-04-04 11:39:48,147 p=15299 u=fred |  using connection plugin network_cli
   2017-04-04 11:39:48,340 p=15299 u=fred |  connecting to host veos01 returned an error
   2017-04-04 11:39:48,340 p=15299 u=fred |  [Errno -2] Name or service not known


解決するためのヒント:

* ``provider:`` オプションを使用している場合は、そのサブオプション ``host:`` が正しく設定されていることを確認してください。
* ``provider:`` またはトップレベルの引数を使用しない場合には、インベントリーファイルが正しいことを確認してください。





Error: "Authentication failed"
------------------------------

**プラットフォーム:** 任意

(``ansible`` または ``ansible-playbook`` を使用して) ``ansible-connection`` に渡される認証情報 (ユーザー名、パスワード、または ssh キー) を使用してリモートデバイスに接続できない場合に発生します。



例:

.. code-block:: yaml

   <ios01> ESTABLISH CONNECTION FOR USER: cisco on PORT 22 TO ios01
   <ios01> Authentication failed.


解決するためのヒント:

(直接または ``provider:`` を使用して) ``password:`` で認証情報を指定する場合や、環境変数の `ANSIBLE_NET_PASSWORD` を指定する場合は、``paramiko`` (Ansible が使用する Python SSH ライブラリー) が ssh キーを使用している可能性があるため、指定する認証情報は無視されます。これを確認するには、「look for keys」を無効にします。これは以下のように実行できます。

.. code-block:: yaml

   export ANSIBLE_PARAMIKO_LOOK_FOR_KEYS=False

これを永続的に変更するには、以下を ``ansible.cfg`` ファイルに追加します。

.. code-block:: ini

   [paramiko_connection]
   look_for_keys = False


Error: "connecting to host <hostname> returned an error" or "Bad address"
-------------------------------------------------------------------------

これは、SSH フィンガープリントが Paramiko の既知のホストファイル (Python SSH ライブラリー) に追加されていない場合に発生する可能性があります。

Paramiko で永続的な接続を使用すると、接続はバックグラウンドプロセスで実行されます。 ホストに有効な SSH キーがない場合は、デフォルトでは Ansible がホストキーの追加を求めるプロンプトを表示します。 これにより、バックグラウンドプロセスで実行している接続が失敗します。

例:

.. code-block:: yaml

   2017-04-04 12:06:03,486 p=17981 u=fred |  using connection plugin network_cli
   2017-04-04 12:06:04,680 p=17981 u=fred |  connecting to host veos01 returned an error
   2017-04-04 12:06:04,682 p=17981 u=fred |  (14, 'Bad address')
   2017-04-04 12:06:33,519 p=17981 u=fred |  number of connection attempts exceeded, unable to connect to control socket
   2017-04-04 12:06:33,520 p=17981 u=fred |  persistent_connect_interval=1, persistent_connect_retries=30


解決するためのヒント:

``ssh-keyscan`` を使用して known_hosts を事前設定します。キーが正しいことを確認する必要があります。

.. code-block:: shell

   ssh-keyscan veos01


または

鍵を自動的に受け入れるように Ansible に設定できます。

環境変数では、以下のようになります::

  export ANSIBLE_PARAMIKO_HOST_KEY_AUTO_ADD=True
  ansible-playbook ...

``ansible.cfg`` メソッド:

ansible.cfg

.. code-block:: ini

  [paramiko_connection]
  host_key_auto_add = True



.. warning:Security warning

   Care should be taken before accepting keys.

Error: "No authentication methods available"
--------------------------------------------

例:

.. code-block:: yaml

   2017-04-04 12:19:05,670 p=18591 u=fred |  creating new control socket for host veos01:None as user admin
   2017-04-04 12:19:05,670 p=18591 u=fred |  control socket path is /home/fred/.ansible/pc/ca5960d27a
   2017-04-04 12:19:05,670 p=18591 u=fred |  current working directory is /home/fred/git/ansible-inc/ansible-workspace-2/test/integration
   2017-04-04 12:19:05,670 p=18591 u=fred |  using connection plugin network_cli
   2017-04-04 12:19:06,606 p=18591 u=fred |  connecting to host veos01 returned an error
   2017-04-04 12:19:06,606 p=18591 u=fred |  No authentication methods available
   2017-04-04 12:19:35,708 p=18591 u=fred |  connect retry timeout expired, unable to connect to control socket
   2017-04-04 12:19:35,709 p=18591 u=fred |  persistent_connect_retry_timeout is 15 secs


解決するためのヒント:

パスワードまたは SSH キーが指定されていない

Clearing Out Persistent Connections
-----------------------------------

**プラットフォーム:** 任意

Ansible 2.3 では、すべてのネットワークデバイスに対する永続的な接続ソケットは ``~/.ansible/pc`` に保存されます。 Ansible Playbook が実行すると、永続ソケット接続は詳細出力が指定されている場合に表示されます。

``<switch> socket_path: /home/fred/.ansible/pc/f64ddfa760``

タイムアウトする前に永続的な接続を消去する (アクティブになっていない場合のデフォルトのタイムアウトは 30 秒) には、
ソケットファイルを削除するだけです。


.. _timeout_issues:

タイムアウトの問題
==============

永続的な接続アイドルタイムアウト
----------------------------------

デフォルトでは、``ANSIBLE_PERSISTENT_CONNECT_TIMEOUT`` は 30 (秒) に設定されます。この値が低すぎると、以下のエラーが発生することがあります。

.. code-block:: yaml

   2017-04-04 12:19:05,670 p=18591 u=fred |  persistent connection idle timeout triggered, timeout value is 30 secs

解決するためのヒント:

永続的な接続アイドルタイムアウトの値を増やします。

.. code-block:: sh

   export ANSIBLE_PERSISTENT_CONNECT_TIMEOUT=60

これを永続的に変更するには、以下を ``ansible.cfg`` ファイルに追加します。

.. code-block:: ini

   [persistent_connection]
   connect_timeout = 60

コマンドタイムアウト
---------------

デフォルトでは、``ANSIBLE_PERSISTENT_COMMAND_TIMEOUT`` は 30 (秒) に設定されます。Ansible の以前のバージョンでは、この値はデフォルトで 10 秒に設定されていました。
この値が低すぎると、以下のエラーが発生することがあります。


.. code-block:: yaml

   2017-04-04 12:19:05,670 p=18591 u=fred |  command timeout triggered, timeout value is 30 secs

解決するためのヒント:

* オプション 1 (グローバルコマンドタイムアウト設定): 
  設定ファイルを使用するか、環境変数を設定して、コマンドのタイムアウトの値を増やします。

  .. code-block:: yaml

     export ANSIBLE_PERSISTENT_COMMAND_TIMEOUT=60

  これを永続的に変更するには、以下を ``ansible.cfg`` ファイルに追加します。

  .. code-block:: ini

     [persistent_connection]
     command_timeout = 60

* オプション 2 (各タスクコマンドのタイムアウト設定):
  タスクごとにコマンドのタイムアウトを増やします。すべてのネットワークモジュールが、
  タスクごとに設定できるタイムアウト値に対応します。
  タイムアウト値は、
  コマンドが返さないと、タスクは失敗する前の時間 (秒) を制御します。

  ローカル接続タイプの場合:

  ..FIXME:Detail error here

  解決するためのヒント:

  .. code-block:: yaml

      - name: save running-config
        ios_command:
          commands: copy running-config startup-config
          provider: "{{ cli }}"
          timeout: 30

  network_cli の場合の netconf 接続タイプ (2.7 以降で適用可能):

  ..FIXME:Detail error here

  解決するためのヒント:

  .. code-block:: yaml

      - name: save running-config
        ios_command:
          commands: copy running-config startup-config
        vars:
          ansible_command_timeout: 60

一部の操作は、完了する時間がデフォルトの 30 秒よりも長くなります。 一例は、
IOS デバイスで現在実行されている設定を起動設定に保存する例です。
この場合は、タイムアウト値をデフォルトの 30 秒から 60 秒に変更すると、
コマンドが完了するまで
タスクが失敗しないようになります。

永続的な接続の再試行タイムアウト
-----------------------------------

デフォルトでは、``ANSIBLE_PERSISTENT_CONNECT_RETRY_TIMEOUT`` は 15 (秒) に設定されます。この値が低すぎると、以下のエラーが発生することがあります。

.. code-block:: yaml

   2017-04-04 12:19:35,708 p=18591 u=fred |  connect retry timeout expired, unable to connect to control socket
   2017-04-04 12:19:35,709 p=18591 u=fred |  persistent_connect_retry_timeout is 15 secs

解決するためのヒント:

永続的な接続のアイドルタイムアウトの値を増やします。
注記: この値は、
SSH タイムアウト値 (設定ファイルのデフォルトセクションにあるタイムアウト値 (connect_timeout)) よりも大きくし、
永続的な設定アイドルタイムアウトの値より小さくする必要があります。

.. code-block:: yaml

   export ANSIBLE_PERSISTENT_CONNECT_RETRY_TIMEOUT=30

これを永続的に変更するには、以下を ``ansible.cfg`` ファイルに追加します。

.. code-block:: ini

   [persistent_connection]
   connect_retry_timeout = 30


``network_cli`` 接続タイプを持つプラットフォーム固有のログインメニューによるタイムアウトの問題
--------------------------------------------------------------------------------------

Ansible 2.9 以降では、プラットフォーム固有のログインメニューを処理するために、
network_cli 接続プラグイン設定オプションが追加されました。これらのオプションは、
グループ/ホストまたはタスク変数として設定できます。

例:ホスト変数を使用した 1 つのログインメニュープロンプトを処理します。

.. code-block:: console

    $cat host_vars/<hostname>.yaml
    ---
    ansible_terminal_initial_prompt:
      - "Connect to a host"
    ansible_terminal_initial_answer:
      - "3"

例:ホスト変数を使用したリモートホストの複数のログインメニュープロンプトを処理します。

.. code-block:: console

    $cat host_vars/<inventory-hostname>.yaml
    ---
    ansible_terminal_initial_prompt:
      - "Press any key to enter main menu"
      - "Connect to a host"
    ansible_terminal_initial_answer:
      - "\\r"
      - "3"
    ansible_terminal_initial_prompt_checkall: True

複数のログインメニュープロンプトを処理するには、以下を行います。

* ``ansible_terminal_initial_prompt`` および ``ansible_terminal_initial_answer`` の値はリストである必要があります。
* プロンプトシーケンスは、応答シーケンスに一致する必要があります。
* ``ansible_terminal_initial_prompt_checkall`` の値は ``True`` に設定する必要があります。

.. note:: 接続の初期化時に、シーケンス内のすべてのプロンプトがリモートホストから受信しないと、タイムアウトが生じます。


Playbook の問題
===============

本セクションでは、Playbook 自体の問題が原因で発生する問題を詳しく説明します。

Error: "Unable to enter configuration mode"
-------------------------------------------

**プラットフォーム：** eos および ios

これは、ユーザーモードシェルで特権モードを必要とするタスクを実行しようとすると発生します。

例:

.. code-block:: console

  TASK [ios_system : configure name_servers] *****************************************************************************
  task path:
  fatal: [ios-csr1000v]: FAILED! => {
      "changed": false,
      "failed": true,
     "msg": "unable to enter configuration mode",
  }

解決するためのヒント:

2.5 よりも前のバージョンの Ansible の場合:
``authorize: yes`` をタスクに追加します。例:

.. code-block:: yaml

  - name: configure hostname
    ios_system:
      provider:
        hostname: foo
        authorize: yes
    register: result

ユーザーが特権モードにパスワードを必要とする場合は、これを ``auth_pass`` で指定できます。``auth_pass`` が設定されていない場合は、代わりに環境変数 `ANSIBLE_NET_AUTHORIZE` が使用されます。


``authorize: yes`` をタスクに追加します。例:

.. code-block:: yaml

  - name: configure hostname
    ios_system:
    provider:
      hostname: foo
      authorize: yes
      auth_pass: "{{ mypasswordvar }}"
  register: result


.. note:: Ansible 2.5 以降では、``connection: network_cli`` および ``become: yes`` を使用することが推奨されます。


プロキシーの問題
============

 .. _network_delegate_to_vs_ProxyCommand:

delegate_to 対 ProxyCommand
---------------------------

``cli`` トランスポートを使用する Ansible 2.3 のネットワークモジュール用の新しい接続フレームワークでは、
``delegate_to`` ディレクティブの使用に対応しなくなりました。
bastion、または中間ジャンプホストを使用して、``cli`` トランスポートでネットワークデバイスに接続するには、
ネットワークモジュールが ``ProxyCommand`` の使用に対応するようになりました。

``ProxyCommand`` を使用するには、Ansible インベントリーファイルでプロキシー設定を指定して、
プロキシーホストを指定します。

.. code-block:: ini

    [nxos]
    nxos01
    nxos02

    [nxos:vars]
    ansible_ssh_common_args='-o ProxyCommand="ssh -W %h:%p -q bastion01"'


上記の設定では、以下のように Playbook を構築し、通常どおりに実行します。
その他の変更は必要ありません。 ネットワークモジュール
が、
``ansible_ssh_common_args`` に指定したホストに最初に接続することで、ネットワークデバイスに接続するようになります。これは、上記の例の ``bastion01`` になります。

環境変数を使用して、すべてのホストのプロキシーターゲットを設定することもできます。

.. code-block:: sh

    export ANSIBLE_SSH_ARGS='-o ProxyCommand="ssh -W %h:%p -q bastion01"'

netconf 接続での bastion/ジャンプホストの使用
-----------------------------------------------

ジャンプホスト設定の有効化
--------------------------


netconf 接続を持つ bastion/ジャンプホストは、以下で有効にできます。
 - Ansible 変数 ``ansible_netconf_ssh_config`` を ``True`` またはカスタムの ssh 設定ファイルパスに設定します。
 - 環境変数 ``ANSIBLE_NETCONF_SSH_CONFIG`` を ``True`` に設定するか、カスタムの ssh 設定ファイルパスを設定します。
 - ``netconf_connection`` セクションの下に、``ssh_config = 1`` または ``ssh_config = <ssh-file-path>`` セクションを設定します。

設定変数が 1 に設定されている場合は、proxycommand およびその他の ssh 変数から、
デフォルトの ssh 設定ファイル (~/.ssh/config) が読み込まれます。

設定変数が proxycommand のファイルパスに設定されていると、
指定したカスタムの ssh ファイルパスから、その他の ssh 変数が読み込まれます。

ssh 設定ファイルの例 (~/.ssh/config)
---------------------------------------

.. code-block:: ini

  Host jumphost
    HostName jumphost.domain.name.com
    User jumphost-user
    IdentityFile "/path/to/ssh-key.pem"
    Port 22

  # Note: Due to the way that Paramiko reads the SSH Config file,
# you need to specify the NETCONF port that the host uses.
# i.e. It does not automatically use ansible_port
# As a result you need either:

  Host junos01
    HostName junos01
    ProxyCommand ssh -W %h:22 jumphost

  # OR

  Host junos01
    HostName junos01
    ProxyCommand ssh -W %h:830 jumphost

  # Depending on the netconf port used.

Ansible インベントリーファイルの例

.. code-block:: ini

    [junos]
    junos01

    [junos:vars]
    ansible_connection=netconf
    ansible_network_os=junos
    ansible_user=myuser
    ansible_password=!vault...


.. note:: 変数によるパスワードを使用した ``ProxyCommand`` の使用

   設計上、SSH は環境変数によるパスワードの提供に対応しません。
   これは、``ps`` 出力などでシークレットのリークを防ぐために行われます。

   SSH 鍵を使用することを推奨します。必要に応じて、可能な場合は、パスワードではなく ssh-agent を使用することが推奨されます。

その他の問題
====================


``network_cli`` 接続タイプの使用時の断続的な失敗
----------------------------------------------------------------

応答で受け取ったコマンドプロンプトは、
``network_cli`` 接続プラグイン内で適切に一致しない場合は、
切り取られた応答、またはエラーメッセージ ``operation requires privilege escalation`` により、タスクが断続的に失敗することがあります。
2.7.1 以降、プロンプトが適切に適合するように、新しいバッファー読み取りタイマーが追加されています。
また、完全な応答が出力で送信されます。タイマーのデフォルト値は 0.2 秒で、
タスクごとに調整することも、秒単位でグローバルに設定することもできます。

タスクタイマーごとの設定例

.. code-block:: yaml

  - name: gather ios facts
    ios_facts:
      gather_subset: all
    register: result
    vars:
      ansible_buffer_read_timeout:2


これをグローバル設定にするには、以下を ``ansible.cfg`` ファイルに追加します。

.. code-block:: ini

   [persistent_connection]
   buffer_read_timeout = 2

リモートホストで実行されるコマンドごとのこのタイマー遅延は、値をゼロに設定すると無効にできます。


``network_cli`` 接続タイプを使用したコマンド応答内のエラー正規表現の不一致によるタスクの失敗
--------------------------------------------------------------------------------------------------------

Ansible 2.9 以降では、
stdout および stderr の正規表現を処理する network_cli 接続プラグイン設定オプションが追加され、
コマンド実行の応答に、通常の応答またはエラーの応答が含まれているかどうかを特定します。これらのオプションは、グループ/ホスト変数の設定や、
タスク変数のように設定できます。

例:不一致のエラー応答の場合

.. code-block:: yaml

  - name: fetch logs from remote host
    ios_command:
      commands:
        - show logging


Playbook の実行の出力:

.. code-block:: console

  TASK [first fetch logs] ********************************************************
  fatal: [ios01]: FAILED! => {
      "changed": false,
      "msg": "RF Name:\r\n\r\n <--nsip-->
             \"IPSEC-3-REPLAY_ERROR: Test log\"\r\n*Aug  1 08:36:18.483: %SYS-7-USERLOG_DEBUG:
              Message from tty578(user id: ansible): test\r\nan-ios-02#"}

解決するためのヒント:

個々のタスクのエラー正規表現を変更します。

.. code-block:: yaml

  - name: fetch logs from remote host
    ios_command:
      commands:
        - show logging
    vars:
      ansible_terminal_stderr_re:
        - pattern: 'connection timed out'
          flags: 're.I'

ターミナルプラグインの正規表現オプション ``ansible_terminal_stderr_re`` および ``ansible_terminal_stdout_re`` には、
``pattern`` キーおよび ``flags`` がキーとして含まれます。``flags`` キーの値は、
python メソッド ``re.compile`` によって許可される値である必要があります。


低速ネットワークまたはリモートターゲットホストによる ``network_cli`` 接続タイプの使用時の断続的な失敗
------------------------------------------------------------------------------------------------------------

Ansible 2.9 以降では、``network_cli`` 接続プラグイン設定オプションが、
リモートホストへの接続試行回数を制御するために追加されます。デフォルトの試行数は 3 です。
再試行のたびに、最大試行回数がなくなるか、
``persistent_command_timeout`` タイマーまたは ``persistent_connect_timeout`` タイマーが発生するまで、再試行間の遅延が 2 の累乗 (秒単位) で増加します。

これをグローバル設定にするには、以下を ``ansible.cfg`` ファイルに追加します。

.. code-block:: ini

   [persistent_connection]
   network_cli_retries = 5
