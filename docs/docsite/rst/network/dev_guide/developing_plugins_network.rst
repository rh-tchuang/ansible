
.. \_developing\_modules\_network:
.. \_developing\_plugins\_network:

**************************
ネットワーク接続プラグイン
**************************

各ネットワーク接続プラグインには、独自のプラグインセットがあります。
これは、特定のデバイスセットの接続の仕様を提供します。使用される特定のプラグインは、
ホストに割り当てられた ``ansible_network_os`` 変数の値に基づいてランタイム時に選択されます。この変数は、
読み込むプラグインの名前と同じ値に設定する必要があります。そのため、``ansible_network_os=nxos`` は、
``nxos.py`` という名前のファイルにプラグインを読み込もうとするため、
ユーザーが適切な方法でプラグインに名前を付けることが重要です。

これらのプラグインのパブリックメソッドは、
接続のプロキシーオブジェクトをその他の接続方法として、モジュールまたは module\_utils から接続で呼び出すことが可能です。以下は、このような呼び出しを module\_utils ファイルで実行する非常に簡単な使用例です。
その他のモジュールと共有できるようにします。

.. code-block:: python

  from ansible.module\_utils.connection import Connection

  def get\_config(module):
      \# module is your AnsibleModule instance.
connection = Connection(module.\_socket\_path)

      # You can now call any method (that doesn't start with '_') of the connection
  # plugin or its platform-specific plugin
  return connection.get_config()

.. contents::
   :local:

.. \_developing\_plugins\_httpapi:

httpapi プラグインの開発
==========================

:ref:`httpapi プラグイン<httpapi_plugins>` は、``httpapi`` 接続プラグインで使用するさまざまな HTTP(S) API のアダプターとして機能します。使用しようとしている API に合わせて調整された最小限の便利なメソッドのセットを実装する必要があります。

具体的には、``httpapi`` 接続プラグインが想定するメソッドがいくつかあります。

要求の作成
---------------

``httpapi`` 接続プラグインには ``send()`` メソッドがありますが、httpapi プラグインには、``send()`` の高レベルラッパーとして ``send_request(self, data, **message_kwargs)`` メソッドが必要です。この方法では、共通のヘッダーや URL ルートパスなどの固定値を追加してリクエストを準備する必要があります。この方法は、データをフォーマットされたペイロードに変換する、または要求するパスまたはメソッドを決定するなど、より複雑な作業を行うことができます。また、呼び出し元により簡単に消費されるように応答を展開することもできます。

.. code-block:: python

   from ansible.module\_utils.six.moves.urllib.error import HTTPError

   def send\_request(self, data, path, method='POST'):
       \# Fixed headers for requests
headers = {'Content-Type': 'application/json'}
try:
response, response\_content = self.connection.send(path, data, method=method, headers=headers)
except HTTPError as exc:
return exc.code, exc.read()

       # handle_response (defined separately) will take the format returned by the device
   # and transform it into something more suitable for use by modules.
   # This may be JSON text to Python dictionaries, for example.
   return handle_response(response_content)

認証
--------------

デフォルトでは、すべての要求は HTTP Basic 認証で認証されます。リクエストが HTTP Basic の代わりにある種のトークンを返す場合は、そのトークンの応答を検証するために ``update_auth(self, response, response_text)`` メソッドを実装する必要があります。トークンが各リクエストのヘッダーに含まれていることを意図している場合は、各リクエストの計算されたヘッダーとマージされるディクショナリーを返すだけで十分です。この方法のデフォルト実装は、クッキーに対して正確にこれを実行します。トークンが別の方法 (クエリー文字列など) で使用される場合は、そのトークンをインスタンス変数に保存して、``send_request()`` メソッド (上記) により各リクエストに追加できるようにします。

.. code-block:: python

   def update\_auth(self, response, response\_text):
       cookie = response.info().get('Set-Cookie')
       if cookie:
           return {'Cookie': cookie}

       return None

代わりに明示的なログインエンドポイントを要求して認証トークンを受け取る必要がある場合は、``login(self, username, password)`` メソッドを実装して、そのエンドポイントを呼び出すことができます。実装すると、このメソッドはサーバーのその他のリソースを要求する前に一度呼び出されます。デフォルトでは、リクエストから HTTP 401 が返されると、一度試行されます。

.. code-block:: python

   def login(self, username, password):
       login\_path = '/my/login/path'
       data = {'user': username, 'password': password}

       response = self.send_request(data, path=login_path)
       try:
           # This is still sent as an HTTP header, so we can set our connection's _auth
       # variable manually. If the token is returned to the device in another way,
       # you will have to keep track of it another way and make sure that it is sent
       # with the rest of the request from send_request()
       self.connection._auth = {'X-api-token': response['token']}
       except KeyError:
           raise AnsibleAuthenticationFailure(message="Failed to acquire login token.")
    
同様に、``logout(self)`` を実装してエンドポイントを呼び出し、そのエンドポイントが存在する場合は現在のトークンを無効化または解放できます。これは、接続を閉じると自動的に呼び出されます (リセット時には拡張で呼び出されます)。

.. code-block:: python

   def logout(self):
       logout\_path = '/my/logout/path'
       self.send\_request(None, path=logout\_path)

       # Clean up tokens
   self.connection._auth = None

エラー処理
--------------

``handle_httperror(self, exception)`` メソッドは、サーバーにより返されるステータスコードを処理できます。戻り値は、プラグインがリクエストをどのように続行するかを示します。

* ``true`` の値は、要求を再試行できることを意味します。これは、一時的なエラーや解決されたエラーを示すために使用されます。たとえば、デフォルトの実装では、401 が提供されると ``login()`` の呼び出しが試行され、成功した場合には ``true`` が返されます。

* ``false`` の値を指定すると、プラグインはこの応答から復旧できません。ステータスコードは例外として呼び出したモジュールに戻ります。その他の値は、リクエストから致命的でない応答として取られます。これは、サーバーが応答のボディーにエラーメッセージを返す場合に役立ちます。通常、HTTPError オブジェクトは、成功した応答と同じインターフェイスを持っているため、この場合は、元の例外を返すだけで十分です。

たとえば、httpapi プラグインの場合は、Ansible Core に含まれる `httpapi プラグインのソースコード<https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/httpapi>`_ を参照してください。



NETCONF プラグインの開発
==========================

:ref:`netconf <netconf_connection>` 接続プラグインは、``SSH NETCONF`` サブシステムを介してリモートデバイスへの接続を提供します。ネットワークデバイスは通常、この接続プラグインを使用して ``NETCONF`` で ``RPC`` 呼び出しを送受信します。

``netconf`` 接続プラグインは、Python ライブラリー ``ncclient`` を使用して、NETCONF が有効なリモートネットワークデバイスで NETCONF セッションを開始します。また、``ncclient`` は NETCONF RPC 要求を実行し、応答を受け取ります。``ncclient`` をローカルの Ansible コントローラーにインストールする必要があります。

``get``、``get-config``、``edit-config`` などの標準 NETCONF (:RFC:`6241`) 操作に対応するネットワークデバイスの ``netconf`` 接続プラグインを使用するには、``ansible_network_os=default`` を設定します。
:ref:`netconf_get <netconf_get_module>` モジュール、:ref:`netconf_config <netconf_config_module>` モジュール、および :ref:`netconf_rpc <netconf_rpc_module>` モジュールを使用して、NETCONF が有効なリモートホストと通信できます。

デバイスが標準の NETCONF に対応している場合は、コントリビューターおよびユーザーとして、``NetconfBase`` クラスのすべてのメソッドを使用できるようにする必要があります。作業しているデバイスにベンダー固有の NETCONF RPC がある場合は、新しいプラグインを利用できます。
ベンダー固有の NETCONF RPC に対応するには、ネットワーク OS 固有の NETCONF プラグインに実装を追加します。

たとえば、Junios の場合は以下のようになります。

* ``plugins/netconf/junos.py`` に実装されたベンダー固有の Junos RPC メソッドを参照してください。
* 今回の例では、``ansible_network_os`` の値を netconf プラグインファイルの名前 (ここでは ``junos``) に設定します。

.. \_developing\_plugins\_network\_cli:

network\_cli プラグインの開発
==============================

接続タイプ :ref:`network_cli <network_cli_connection>` は、コマンドを送信して応答を受け取るための疑似端末を作成するフードの下で、``paramiko_ssh`` を使用します。
``network_cli`` は、``ansible_network_os`` の値に基づいて、プラットフォーム固有のプラグインを読み込みます。

* 端末のプラグイン (例: ``plugins/terminal/ios.py``) - 端末の長さや幅の設定、ページの無効化、権限の昇格など、端末に関連するパラメーターを制御します。また、正規表現を定義して、コマンドプロンプトとエラープロンプトを特定します。

* :ref:`cliconf_plugins` (例: :ref:`ios cliconf <ios_cliconf>`) - 低レベルの送受信操作に抽象化レイヤーを提供します。たとえば、``edit_config()`` メソッドは、設定コマンドを実行する前にプロンプトが ``config`` モードであることを確認します。

``network_cli`` 接続を使用する新しいネットワークオペレーティングシステムを提供するには、そのネットワーク OS の ``cliconf`` プラグインおよび ``terminal`` プラグインを実装します。

このプラグインは以下の場所に置くことができます。

* フォルダー内で Playbook に隣接

  .. code-block:: bash

    cliconf\_plugins/
    terminal\_plugins/

* ロール

  .. code-block:: bash

     myrole/cliconf\_plugins/
     myrole/terminal\_plugins/

* コレクション

  .. code-block:: bash

    myorg/mycollection/plugins/terminal/
    myorg/mycollection/plugins/cliconf/

また、:ref:`DEFAULT_CLICONF_PLUGIN_PATH` を設定して ``cliconf`` プラグインパスを設定することもできます。

予想される場所に``cliconf`` プラグインおよび ``terminal`` プラグインを追加した後、ユーザーは以下を行うことができます。

* :ref:`cli_command <cli_command_module>` を使用して、ネットワークデバイスで任意のコマンドを実行します。
* :ref:`cli_config <cli_config_module>` を使用して、プラットフォーム固有のモジュールを使用しないリモートホストに設定変更を実装します。
