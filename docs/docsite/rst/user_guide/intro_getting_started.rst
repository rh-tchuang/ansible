.. _intro_getting_started:

***************
はじめに
***************

:ref:`インストールガイド<installation_guide>` を読み、コントロールノードに Ansible をインストールしたら、Ansible の仕組みを学ぶ準備ができました。基本的な Ansible コマンドまたはプレイブックは以下のようになります。
  * インベントリーから実行するマシンを選択する
  * 通常は SSH 経由で、このマシン (もしくはネットワークデバイスまたはその他の管理対象ノード) に接続する
  * 1 つ以上のモジュールをリモートマシンにコピーし、そこで実行を開始する

Ansible はさらに多くのことができますが、Ansible の強力な設定、デプロイメント、オーケストレーションの機能をすべて試す前に最も一般的なユースケースを理解しておく必要があります。このページでは、簡単なインベントリーとアドホックコマンドを使用した基本的なプロセスを説明します。Ansible の仕組みを理解したら、:ref:`アドホックコマンド<intro_adhoc>` の詳細を読み、:ref:`インベントリー<intro_inventory>` でインフラストラクチャーを整理し、:ref:`Playbook<playbooks_intro>` で Ansible の全機能を活用できます。

.. contents::
   :local:

インベントリーからのマシンの選択
=================================

Ansible は、インベントリーから管理するマシンの情報を読み取ります。IP アドレスをアドホックコマンドに渡すことはできますが、Ansible の柔軟性と再現性を完全に活用するにはインベントリーが必要です。

アクション: 基本的なインベントリーの作成
--------------------------------
この基本的なインベントリーでは、``/etc/ansible/hosts`` を編集 (または作成) し、リモートシステムをいくつか追加します。この例では、IP アドレスまたは FQDN を使用します。

.. code-block:: text

   192.0.2.50
   aserver.example.org
   bserver.example.org

中級編
-----------------
インベントリーは IP や FQDN よりも多くのものを保存できます。:ref:`エイリアス<inventory_aliases>` を作成し、:ref:`host 変数<host_variables>` で 1 台のホストに変数値を設定し、:ref:`group 変数<group_variables>` で複数のホストに変数値を設定できます。

.. _remote_connection_information:

リモートノードへの接続
==========================

Ansible は、`SSH プロトコル <https://www.ssh.com/ssh/protocol/>`_ でリモートマシンと通信します。デフォルトでは、Ansible はネイティブの OpenSSH を使用し、SSH のように、現在のユーザー名を使用してリモートマシンに接続します。

アクション: SSH 接続の確認
----------------------------------
同じユーザー名で、SSH を使用してインベントリー内のすべてのノードに接続できることを確認します。必要に応じて、公開 SSH キーを、システムの ``authorized_keys`` ファイルに追加します。

中級編
-----------------
次のようないくつかの方法で、デフォルトのリモートユーザー名を上書きできます。
* コマンドラインで ``-u`` パラメーターを渡します。
* インベントリーファイルにユーザー情報を設定します。
* 設定ファイルにユーザー情報を設定します。
* 追加の環境変数を設定します。

ユーザー情報を渡す各方法の優先順位 (意図しない場合もあります) の詳細は、:ref:`general_precedence_rules` を参照してください。接続の詳細は、:ref:`connections` を参照してください。

モジュールのコピーおよび実行
=============================

接続後、Ansible はコマンドまたは Playbook が必要とするモジュールを、リモートマシンに転送して実行します。

アクション: 最初の Ansible コマンドの実行
---------------------------------------
ping モジュールを使用して、インベントリー内のすべてのノードに対して ping を実行します。

.. code-block:: bash

   $ ansible all -m ping

全ノードでライブコマンドを実行します。

.. code-block:: bash

   $ ansible all -a "/bin/echo hello"

次のようなインベントリー内の各ホストの出力が表示されます。

.. code-block:: ansible-output

   aserver.example.org | SUCCESS => {
       "ansible_facts": {
           "discovered_interpreter_python": "/usr/bin/python"
       },
       "changed": false,
       "ping": "pong"
   }

中級編
-----------------
デフォルトでは、Ansible は SFTP を使用してファイルを転送します。管理するマシンまたはデバイスが SFTP に対応していない場合は、:ref:`intro_configuration` で SCP モードに切り替えることができます。ファイルは一時ディレクトリーに置かれ、そこから実行されます。

コマンドを実行する権限昇格 (sudo など) が必要な場合は、``become`` フラグを渡します。

.. code-block:: bash

    # as bruce
    $ ansible all -m ping -u bruce
    # as bruce, sudoing to root (sudo is default method)
    $ ansible all -m ping -u bruce --become
    # as bruce, sudoing to batman
    $ ansible all -m ping -u bruce --become --become-user batman

権限の昇格の詳細は、:ref:`become` を参照してください。

おめでとうございます。Ansible を使用してノードに接続しました。基本的なインベントリーファイルとアドホックコマンドを使用して、Ansible が特定のリモートノードに接続し、そこでモジュールファイルをコピーして実行し、出力を返すように指定しました。完全に機能するインフラストラクチャーがあります。

次のステップ
==========
次に、:ref:`intro_adhoc` で実際のケースについて読むか、
さまざまなモジュールで実行できることを調べるか、
Ansible の :ref:`working_with_playbooks` 言語に関する情報を確認できます。 Ansible は、コマンドの実行だけでなく、
強力な設定管理およびデプロイメント機能があります。

.. seealso::

   :ref:`intro_inventory`
       インベントリーの詳細情報
   :ref:`intro_adhoc`
       基本コマンドの例
   :ref:`working_with_playbooks`
       Ansible の設定管理言語について
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
