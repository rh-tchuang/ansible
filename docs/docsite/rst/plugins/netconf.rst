.. _netconf_plugins:

Netconf プラグイン
===============

.. contents::
   :local:
   :depth: 2

Netconf プラグインは、ネットワークデバイスに対する Netconf インターフェースを抽象化したものです。Ansible が、これらのネットワークデバイスで、
タスクを実行する標準インターフェースを提供します。

通常、これらのプラグインはネットワークデバイスプラットフォームに 1 対 1 で対応します。そのため、適切な netconf プラグインは、
``ansible_network_os`` 変数に基づいて自動的に読み込まれます。Netconf RFC 仕様で定義されているようにプラットフォームが標準 Netconf 実装に対応している場合は、
``デフォルト`` の netconf プラグインが使用されます。
プラットフォームがプロプライエタリー Netconf RPC 仕様に対応している場合は、
プラットフォーム固有の netconf プラグインに定義されるプロプライエタリー Netconf RPC に対応している場合です。

.. _enabling_netconf:

netconf プラグインの追加
-------------------------

``netconf_plugins`` ディレクトリーにカスタムのプラグインを配置して、Ansible が他のネットワークデバイスに対応するように拡張できます。

.. _using_netconf:

netconf プラグインの使用
------------------------

使用する cliconf プラグインは、``ansible_network_os`` 変数から自動的に判断します。この機能をオーバーライドする理由はありません。

netconf プラグインの多くは設定なしで動作します。netconf プラグインの一部には、
タスクを netconf コマンドに変換する方法を左右する設定が可能な追加オプションがあります。ncclient デバイス固有のハンドラー名は、netconf プラグインで設定できます。
または、ncclient デバイスハンドラーにより、``default`` の値が使用されます。


プラグインは、自己文書化されており、プラグインごとに、設定オプションについて文書化する必要があります。

.. _netconf_plugin_list:

プラグイン一覧
-----------

``ansible-doc -t netconf -l`` を使用すると、利用可能なプラグインの一覧を表示できます。
詳細にわたるドキュメントや例を参照するには、``ansible-doc -t netconf <plugin name>`` を使用します。


.. toctree:: :maxdepth: 1
    :glob:

    netconf/*


.. seealso::

   :ref:`ネットワーク自動化での Ansible<network_guide>`
       Ansible を使用したネットワークデバイスの自動化の概要
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible-network IRC chat channel
