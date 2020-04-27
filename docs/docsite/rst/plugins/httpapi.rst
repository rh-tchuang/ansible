.. _httpapi_plugins:

Httpapi プラグイン
===============

.. contents::
   :local:
   :depth: 2

Httpapi プラグインは、Ansible に対して、リモートデバイスの HTTP ベースの API と対話して、
そのデバイスでタスクを実行する方法を指示します。

プラグインごとに、特定の API の方言を表します。プラットフォーム固有のもの (Arista eAPI、Cisco NXAPI) があります。
さまざまなプラットフォーム (RESTCONF) で利用できるものもあります。

.. _enabling_httpapi:

httpapi プラグインの追加
-------------------------

``httpapi_plugins`` ディレクトリーにカスタムのプラグインをドロップして、Ansible が他の API をサポートするように拡張できます。詳細は、:ref:`developing_plugins_httpapi` を参照してください。

.. _using_httpapi:

httpapi プラグインの使用
------------------------

使用する httpapi プラグインは、``ansible_network_os`` 変数から自動的に判断します。

多くの httpapi プラグインは設定なしで動作します。追加のオプションは、プラグインごとに定義できます。

プラグインは、自己文書化されており、プラグインごとに、設定オプションについて文書化する必要があります。


.. _httpapi_plugin_list:

プラグイン一覧
-----------

``ansible-doc -t httpapi -l`` を使用すると、利用可能なプラグインの一覧を表示できます。
詳細にわたるドキュメントや例を参照するには、``ansible-doc -t httpapi <plugin name>`` を使用します。


.. toctree:: :maxdepth: 1
    :glob:

    httpapi/*


.. seealso::

   :ref:`ネットワーク自動化での Ansible<network_guide>`
       Ansible を使用したネットワークデバイスの自動化の概要
   :ref:`ネットワークモジュールの開発<developing_modules_network>`
       ネットワークモジュールの開発方法
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible-network IRC chat channel
