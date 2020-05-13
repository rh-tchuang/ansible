****************
Online.net ガイド
****************

はじめに
============

Online は、主に Dedibox という名前のベアメタルサーバーを提供するフランス系のホスティング企業です。
詳細は `https://www.online.net/en <https://www.online.net/en>`_ を確認してください。

Online リソースの動的インベントリー
--------------------------------------

Ansible には、リソースを一覧表示できる動的インベントリープラグインがあります。

1. 以下の内容で、``online_inventory.yml`` などの YAML 設定を作成します。

.. code-block:: yaml

    plugin: online

2. トークンを使用して、``ONLINE_TOKEN`` 環境変数を設定します。
    トークンを取得する前にアカウントを作成して、ログインする必要があります。
    トークンは `https://console.online.net/en/api/access <https://console.online.net/en/api/access>`_ ページで確認できます。

3. 以下を実行すると、インベントリーが機能していることをテストできます。

.. code-block:: bash

    $ ansible-inventory -v -i online_inventory.yml --list


4. これで、Playbook またはその他のモジュールをこのインベントリーで実行できます。

.. code-block:: console

    $ ansible all -i online_inventory.yml -m ping
    sd-96735 | SUCCESS => {
        "changed": false,
        "ping": "pong"
    }
