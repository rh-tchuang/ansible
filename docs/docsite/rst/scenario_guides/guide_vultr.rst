Vultr ガイド
===========

Ansible は、`Vultr <https://www.vultr.com>`_ クラウドプラットフォームと対話するためのモジュールセットを提供します。

このモジュールセットは、Vultr クラウドプラットフォームのインフラストラクチャーを簡単に管理および調整できるようにするフレームワークを形成します。


要件
------------

技術的要件はありません。すでに作成されている Vultr アカウントが必要です。


構成
-------------

Vultr モジュールは、構成に関してかなり柔軟な方法を提供します。

設定は、以下の順序で読み込まれます。

- 環境変数 (例: ``VULTR_API_KEY``、``VULTR_API_TIMEOUT``)
- 環境変数 ``VULTR_API_CONFIG`` で指定されるファイル
- 現在の作業ディレクトリーにある ``vultr.ini`` ファイル
- ``$HOME/.vultr.ini``


Ini ファイルは以下のような構成になっています。

.. code-block:: ini

  [default]
  key = MY_API_KEY
  timeout = 60

  [personal_account]
  key = MY_PERSONAL_ACCOUNT_API_KEY
  timeout = 30


``VULTR_API_ACCOUNT`` 環境変数または ``api_account`` モジュールパラメーターが指定されないと、モジュールは「default」という名前のセクションを探します。


認証
--------------

Ansible モジュールを使用して Vultr と対話する前に、API キーが必要になります。
AIP キーを所有していない場合は、`Vultr <https://www.vultr.com>`_ にログインし、アカウント、API の順に移動して API を有効すると、API キーが表示されます。

適切な IP アドレスから API キーを使用できるようにします。

この情報をどこに配置するかは、「構成」セクションを参照してください。

すべてが適切に機能していることを確認するには、次のコマンドを実行します。

.. code-block:: console

  #> VULTR_API_KEY=XXX ansible -m vultr_account_info localhost
localhost | SUCCESS => {
"changed": false,
"vultr_account_info": {
"balance": -8.9,
"last_payment_amount": -10.0,
"last_payment_date": "2018-07-21 11:34:46",
"pending_charges": 6.0
},
"vultr_api": {
"api_account": "default",
"api_endpoint": "https://api.vultr.com",
"api_retries": 5,
"api_timeout": 60
}
}


同様の出力が表示され、すべての設定が適切に行われた場合は、適切な ``VULTR_API_KEY`` が正しく指定されており、Vultr > Account > API ページのアクセス制御が正確であることを確認してください。


使用法
-----

`Vultr <https://www.vultr.com>`_ はパブリック API を提供するため、プラットフォーム上でインフラストラクチャーを管理するモジュールの実行はローカルホストで行われます。これは以下に変換されます。

.. code-block:: yaml

  ---
  - hosts: localhost
    tasks:
      - name:Create a 10G volume
        vultr_block_storage:
          name: my_disk
          size:10
          region:New Jersey


これ以降は、ユーザーの創造性が限界となります。`利用可能なモジュール <https://docs.ansible.com/ansible/latest/modules/list_of_cloud_modules.html#vultr>`_ のドキュメントを参照してください。


動的インベントリー
-----------------

Ansible は、`Vultr <https://www.vultr.com>`_ の動的インベントリープラグインを提供します。
設定プロセスは、モジュールのプロセスと完全に同じです。

これを使用できるようにするには、最初に ``ansible.cfg`` ファイルで以下を指定して有効にする必要があります。

.. code-block:: ini

  [inventory]
  enable_plugins=vultr

また、プラグインで使用する設定ファイルを提供します。最小設定ファイルは以下のようになります。

.. code-block:: yaml

  ---
  plugin: vultr

利用可能なホストを一覧表示するには、以下を実行します。

.. code-block:: console

  #> ansible-inventory -i vultr.yml --list


たとえば、これにより、場所別または OS 名別にグループにまとめたノードでアクションを実行できます。

.. code-block:: yaml

  ---
  - hosts:Amsterdam
    tasks:
      - name:Rebooting the machine
        shell: reboot
        become:True


統合テスト
-----------------

Ansible には、すべての Vultr モジュールの統合テストが含まれます。

このテストは、パブリックの Vultr API に対して実行されることが意図されていますが、これは API にアクセスするために有効なキーを必要とするためです。

テスト設定を準備します。

.. code-block:: shell

  $ cd ansible # location the ansible source is
$ source ./hacking/env-setup

Vultr API キーを設定します。

.. code-block:: shell

  $ cd test/integration
$ cp cloud-config-vultr.ini.template cloud-config-vultr.ini
$ vi cloud-config-vultr.ini

すべての Vultr テストを実行します。

.. code-block:: shell

  $ ansible-test integration cloud/vultr/ -v --diff --allow-unsupported


特定のテスト (例: vultr_account_info) を実行するには、以下を実行します。

.. code-block:: shell

  $ ansible-test integration cloud/vultr/vultr_account_info -v --diff --allow-unsupported
