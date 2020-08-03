.. _working_with_bsd:

Ansible および BSD
===============

BSD マシンの管理は、Linux/Unix マシンの管理とは異なります。BSD を実行している管理ノードをお持ちの場合は、以下のトピックを確認してください。

.. contents::
   :local:

BSD ノードへの接続
-----------------------

Ansible はデフォルトで OpenSSH を使用して管理ノードに接続します。これは、認証に SSH キーを使用する場合に BSD で機能します。ただし、認証に SSH パスワードを使用する場合、Ansible は sshpass に依存します。sshpass のほとんどのバージョンは BSD ログインプロンプトを適切に処理できないため、
BSD マシンに SSH パスワードを使用する場合は、OpenSSH ではなく ``paramiko`` を使用して接続します。これは、ansible.cfg でグローバルに実行するか、inventory/group/host 変数として設定することもできます。以下に例を示します。

.. code-block:: text

    [freebsd]
    mybsdhost1 ansible_connection=paramiko

.. _bootstrap_bsd:

BSD のブートストラップ
-----------------

Ansible はデフォルトでエージェントレスですが、管理ノードで Python が必要になります。Python を使用しないと、:ref:`raw <raw_module>` モジュールしか動作しません。このモジュールを使用して Ansible をブートストラップし、Python を BSD バリアントにインストールするために使用できます (以下を参照) が、非常に制限されており、Ansible の機能を最大限に活用するには Python を使用する必要があります。

次の例では、Ansible の全機能に必要な json ライブラリーを含む Python 2.7 をインストールします。
コントロールマシンでは、FreeBSD のほとんどのバージョンに対して次のコマンドを実行できます。

.. code-block:: bash

    ansible -m raw -a "pkg install -y python27" mybsdhost1

または、ほとんどのバージョンの OpenBSD の場合は、次のようになります。

.. code-block:: bash

    ansible -m raw -a "pkg_add -z python-2.7"

これが完了すると、``raw`` モジュール以外の他の Ansible モジュールを使用できるようになります。

.. note::
    この例では、FreeBSD で pkg を使用し、OpenBSD で pkg_add を使用する方法を示しましたが、BSD の代わりに適切なパッケージツールを使用できるはずです。パッケージ名が異なる場合もあります。インストールする Python パッケージの正確な名前は、使用している BSD バリアントのパッケージ一覧またはドキュメントを参照してください。

..BSD_python_location:

Python インタープリターの設定
------------------------------

さまざまな Unix/Linux オペレーティングシステムおよびディストリビューションに対応するために、Ansible が常に既存の環境変数 (または ``env`` 変数) を使用して、適切な Python バイナリーを特定することはできません。モジュールは、デフォルトでは、最もよく使用される ``/usr/bin/python`` を参照します。BSD バリアントではこのパスが異なる可能性があるため、``ansible_python_interpreter`` インベントリー変数を使用して、バイナリーの場所を Ansible に通知することが推奨されます。以下に例を示します。

.. code-block:: text

    [freebsd:vars]
    ansible_python_interpreter=/usr/local/bin/python2.7
    [openbsd:vars]
    ansible_python_interpreter=/usr/local/bin/python2.7

Ansible でバンドルされているプラグイン以外のプラグインを使用する場合は、プラグインの記述方法に応じて ``bash``、``perl``、または ``ruby`` に同様の変数を設定できます。以下に例を示します。

.. code-block:: text

    [freebsd:vars]
    ansible_python_interpreter=/usr/local/bin/python
    ansible_perl_interpreter=/usr/bin/perl5


利用可能なモジュール
----------------------------

Ansible のコアモジュールの大半は、Linux/Unix マシンと他の汎用サービスを組み合わせて記述されているため、Linux に限定したテクノロジー (LVG など) を対象とするものを除き、その大半が BSD 上で正常に機能します。

コントロールノードとしての BSD の使用
-----------------------------

BSD をコントロールマシンとして使用することは、BSD バリアントの Ansible パッケージをインストールするか、``pip`` または「from source」の指示に従うのと同じくらい簡単です。

.. _bsd_facts:

BSD ファクト
---------

Ansible は、Linux マシンと同様の方法で BSD からファクトを収集しますが、データ、名前、構造は、ネットワーク、ディスク、およびその他のデバイスにより異なる可能性があるため、BSD 管理者にとっては出力が多少異なるもののまだ馴染みがあることが期待できます。

.. _bsd_contributions:

BSD の取り組みおよび貢献
-----------------------------

Ansible では、BSD サポートが重要になります。貢献者の大半は Linux を使用し、対象としていますが、BSD コミュニティーは活発で、できるだけ BSD が使いやすくなるように努めています。
BSD と検出された問題または非互換性を報告してください。修正を含む pull リクエストもお寄せください。

.. seealso::

   :ref:`intro_adhoc`
       基本コマンドの例
   :ref:`working_with_playbooks`
       Ansible の設定管理言語について
   :ref:`developing_modules`
       モジュールの書き方
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
