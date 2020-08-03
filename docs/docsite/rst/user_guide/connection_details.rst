.. _connections:

******************************
接続方法および詳細
******************************

このセクションでは、Ansible がインベントリーに使用する接続方法を拡張および改良する方法を示します。

ControlPersist および paramiko
---------------------------

デフォルトでは、Ansible はネイティブの OpenSSH を使用します。これは、ControlPersist (パフォーマンス機能)、Kerberos、および Jump Host 設定などの ``〜/ .ssh / configの`` のオプションをサポートしているためです。ControlPersist をサポートしない OpenSSH の古いバージョンを使用している場合、Ansible は、「paramiko」と呼ばれる OpenSSH の Python 実装にフォールバックします。

SSH キーの設定
-------------

デフォルトでは、Ansible は、SSH 鍵を使用してリモートマシンに接続していると想定します。 SSH 鍵が推奨されますが、必要に応じて ``--ask-pass`` オプションでパスワード認証を使用できます。:ref:`特権昇格 <become>` (sudo、pbrun など) のパスワードを提供する必要がある場合は、``--ask-become-pass`` を使用します。

.. include:: shared_snippets/SSH_password_prompt.txt

パスワードを再入力しないように SSH エージェントをセットアップするには、次のようにします。

.. code-block:: bash

   $ ssh-agent bash
   $ ssh-add ~/.ssh/id_rsa

セットアップによっては、代わりに Ansible の ``--private-key`` コマンドラインオプションを使用して pem ファイルを指定することもできます。 秘密鍵ファイルを追加することもできます。

.. code-block:: bash

   $ ssh-agent bash
   $ ssh-add ~/.ssh/keypair.pem

ssh-agent を使用せずに秘密鍵ファイルを追加する別の方法は、:ref:`intro_inventory` で説明するように、インベントリーファイルで ``ansible_ssh_private_key_file`` を使用することです。

ローカルホストに対して実行
-------------------------

サーバー名に「localhost」または「127.0.0.1」を使用して、コントロールノードにコマンドを実行できます。

.. code-block:: bash

    $ ansible localhost -m ping -e 'ansible_python_interpreter="/usr/bin/env python"'

これをインベントリーファイルに追加して、localhost を明示的に指定できます。

.. code-block:: bash

    localhost ansible_connection=local ansible_python_interpreter="/usr/bin/env python"

.. _host_key_checking_on:

ホストキーの確認
-----------------

Ansible は、デフォルトでホストキーチェックを有効にします。ホストキーをチェックすると、サーバーのなりすましや中間者攻撃から保護されますが、メンテナンスが必要です。

ホストが再インストールされ、「known_hosts」に異なるキーがある場合は、修正されるまでエラーメッセージが表示されます。 新しいホストが「known_hosts」にない場合は、コントロールノードから鍵の確認が求められます。これにより、cron などの Ansible を使用している場合は、相互作用が行われる可能性があります。このように動作しないようにしたい場合があります。

この動作を無効にした場合の影響を理解し、無効にする場合は、``/etc/ansible/ansible.cfg`` または ``~/.ansible.cfg`` 編集します。

.. code-block:: text

    [defaults]
    host_key_checking = False

また、これは、:envvar:`ANSIBLE_HOST_KEY_CHECKING` 環境変数により設定できます。

.. code-block:: bash

    $ export ANSIBLE_HOST_KEY_CHECKING=False

また、paramiko モードでのホストキーチェックはかなり遅いため、この機能を使用する場合は「ssh」に切り替えることも推奨されます。

その他の接続方法
------------------------

Ansible では、SSH 以外のさまざまな接続方法を使用できます。ローカルでの管理、chroot、lxc、jail コンテナーの管理など、任意の接続プラグインを選択できます。
「ansible-pull」と呼ばれるモードは、システムを反転させ、予定された git チェックアウトを介してシステムに「phone home」を設定して、中央リポジトリーから設定ディレクティブをプルすることもできます。
