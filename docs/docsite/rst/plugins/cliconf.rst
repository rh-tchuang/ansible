.. \_cliconf\_plugins:

Cliconf プラグイン
===============

.. contents::
   :local:
   :depth: 2

Cliconf プラグインは、ネットワークデバイスに対する CLI インターフェースを抽象化したものです。これらのネットワークデバイスで
Ansible がこれらのネットワークデバイスでタスクを実行する標準インターフェースを提供します。

通常、これらのプラグインはネットワークデバイスプラットフォームに 1 対 1 で対応します。適切な cliconf プラグインは、
``ansible_network_os`` 変数に基づいて自動的に読み込まれます。

.. \_enabling\_cliconf:

cliconf プラグインの追加
-------------------------

``cliconf_plugins`` ディレクトリーにカスタムのプラグインをドロップして、Ansible が他のネットワークデバイスをサポートするように拡張できます。

.. \_using\_cliconf:

cliconf プラグインの使用
------------------------

使用する cliconf プラグインは、``ansible_network_os`` 変数から自動的に判断します。この機能をオーバーライドする理由はありません。

cliconf プラグインの多くは設定なしで動作します。タスクを CLI コマンドに変換する方法を左右する設定が
可能な追加オプションがあります。

プラグインは、自己文書化されており、プラグインごとに、設定オプションについて文書化する必要があります。

.. \_cliconf\_plugin\_list:

プラグイン一覧
-----------

``ansible-doc -t cliconf -l`` を使用すると、利用可能なプラグインの一覧を表示できます。
詳細にわたるドキュメントや例を参照するには、``ansible-doc -t cliconf <plugin name>`` を使用します。


.. toctree:: :maxdepth: 1
    :glob:

    cliconf/*


.. seealso::

   :ref:`ネットワーク自動化での Ansible<network_guide>`
       Ansible を使用したネットワークデバイスの自動化の概要
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       \#ansible-network IRC chat channel
