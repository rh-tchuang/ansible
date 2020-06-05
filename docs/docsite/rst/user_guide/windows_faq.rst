.. _windows_faq:

Windows に関するよくある質問 (FAQ)
==================================

ここでは、Ansible と Windows に関するよくある質問と、
その回答を紹介します。

.. note:: このドキュメントでは、Microsoft Windows サーバーでの Ansible に管理に関する質問を扱います。
    Ansible Core に関する質問は、
    「:ref:`全般的な FAQ ページ <ansible_faq>`」を参照してください。

Ansible は、Windows XP または Server 2003 で動作しますか
``````````````````````````````````````````````````
Ansible は、Windows XP または Server 2003 ホストでは動作しません。Ansible は、以下の Windows オペレーティングシステムバージョンで動作します。

* Windows Server 2008
* Windows Server 2008 R2
* Windows Server 2012
* Windows Server 2012 R2
* Windows Server 2016
* Windows Server 2019
* Windows 7
* Windows 8.1
* Windows 10

Ansible には、PowerShell バージョンの最小要件もあります。
最新の情報は「:ref:`windows_setup`」を参照してください。

Ansible で Windows Nano Server を管理できますか
``````````````````````````````````````````````
Ansible は現在、Windows Nano Server では動作しません。
これは、Ansible が、
モジュールおよび内部コンポーネントの大部分で使用される完全な .NET Framework にアクセスできないためです。

Ansible は Windows で実行できますか
```````````````````````````
いいえ、Ansible は Windows ホストを管理するだけです。Ansible は、Windows ホストでネイティブに実行することはできませんが、
Linux 用の Windows サブシステム (WSL) では実行できます。

.. note:: Linux 用の Windows サブシステムは、Ansible でサポートされていないため、
    実稼働システムには使用しないでください。

Ansible を WSL にインストールするには、
bash 端末で次のコマンドを実行できます。

.. code-block:: shell

    sudo apt-get update
    sudo apt-get install python-pip git libffi-dev libssl-dev -y
    pip install ansible pywinrm

WSL のリリースではなくソースから Ansible を実行するには、
pip をインストールしたバージョンをアンインストールしてから、git リポジトリーを複製します。

.. code-block:: shell

    pip uninstall ansible -y
    git clone https://github.com/ansible/ansible.git
    source ansible/hacking/env-setup

    # To enable Ansible on login, run the following
    echo ". ~/ansible/hacking/env-setup -q' >> ~/.bashrc

SSH キーを使用して Windows ホストへの認証を行うことはできますか
````````````````````````````````````````````````````
WinRM または PSRP 接続プラグインで SSH キーを使用することはできません。
これらの接続プラグインは、
SSH が使用する SSH キーペアの代わりに X509 証明書を認証に使用します。

X509 証明書が生成されてユーザーにマッピングされる方法は、
SSH 実装とは異なります。
詳細は、「:ref:`windows_winrm`」のドキュメントを参照してください。

Ansible 2.8 には、SSH 接続プラグインを使用するための実験的なオプションが追加されました。
これは、Windows サーバーの認証に SSH キーを使用します。詳細は、「:ref:`こちらの質問 <windows_faq_ssh>`」
を参照してください。

.. _windows_faq_winrm:

Ansible で機能しないコマンドをローカルで実行できるのはなぜですか
`````````````````````````````````````````````````````````````````
Ansible は、WinRM を介してコマンドを実行します。このプロセスは、次の点で、
コマンドをローカルで実行することとは異なります。

* CredSSP や Kerberos などの認証オプションと認証情報の委譲を使用しない限り、
  WinRM プロセスにはユーザーの認証情報をネットワークリソースに委譲する機能がないため、
  ``Access is
Denied`` エラーが発生します。

* WinRM で実行されるすべてのプロセスは、非対話型セッションです。対話型セッションを必要とするアプリケーションは
  機能しません。

* WinRM を介して実行する場合、
  Windows は、
  一部のインストーラーおよびプログラムが使用する Windows Update API や DPAPI などの内部 Windows API へのアクセスを制限します。

これらの制限を回避する方法は次のとおりです。

* ローカルで実行する場合と同様にコマンドを実行する ``become`` を使用します。Windows は、
  ``become`` が使用されたときにプロセスが WinRM で実行されていることを Windows が認識していないため、
  ほとんどの WinRM 制限を回避します。詳細は、
  :ref:`become` のドキュメントを参照してください。

* ``win_scheduled_task`` で作成できるスケジュールされたタスクを使用します。``become`` のように、
  それはすべての WinRM 制限を回避しますが、
  モジュールではなくコマンドを実行するためにのみ使用できます

* ``win_psexec`` を使用して、ホストでコマンドを実行します。PSExec は WinRM を使用しないため、
  すべての制限を回避します。

* これらの回避策なしでネットワークリソースにアクセスするには、
  認証情報の委譲を有効にして CredSSP または Kerberos を使用できます。

become を使用する方法の詳細は、「:ref:`become`」を参照してください。「:ref:`windows_winrm`」の制限セクションには、
WinRM の制限に関する詳細があります。

このプログラムは、Ansible がインストールされている Windows にはインストールされません
``````````````````````````````````````````````````
WinRMの制限の詳細は、「:ref:`こちらの質問 <windows_faq_winrm>`」を参照してください。

どのような Windows モジュールが利用できますか
```````````````````````````````````
Ansible Core のほとんどの Ansible モジュールは、
Linux/Unix マシンと任意の Web サービスを組み合わせて使用するように作成されています。これらのモジュールは Python で作成されており、
そのほとんどは Windows では動作しません。

このため、PowerShell で記述され、
Windows ホストで実行することを目的とした専用の Windows モジュールがあります。このようなモジュールの一覧は、
「:ref:`こちら<windows_modules>`」を参照してください。

次の Ansible Core モジュールおよびアクションプラグインは、Windows で動作します。

* add_host
* assert
* async_status
* debug
* fail
* fetch
* group_by
* include
* include_role
* include_vars
* meta
* pause
* raw
* script
* set_fact
* set_stats
* setup
* slurp
* template (also: win_template)
* wait_for_connection

Windows ホストで Python モジュールを実行できますか
``````````````````````````````````````````
いいえ、WinRM 接続プロトコルは PowerShell モジュールを使用するように設定されているため、
Python モジュールは機能しません。この問題を回避するには、
``delegate_to: localhost`` を使用して、Ansible コントローラーで Python モジュールを実行します。
これは、Playbook の実行時に外部サービスに連絡する必要があり、
利用可能な同等の Windows モジュールがない場合に役に立ちます。

.. _windows_faq_ssh:

SSH 経由で Windows ホストに接続できますか
````````````````````````````````````````
Ansible 2.8 には、
SSH 接続プラグインを使用して、Windows ホストを管理するための実験的なオプションが追加されました。SSH 経由で Windows ホストに接続するには、
Windows ホストに、
Microsoft 社と開発している `Win32-OpenSSH <https://github.com/PowerShell/Win32-OpenSSH>`_ をインストールして設定する必要があります。ほとんどの基本動作は SSH で有効なはずですが、
``Win32-OpenSSH`` は急速に変化しており、
新しい機能が追加され、すべてのリリースでバグが修正されています。Windows ホストで Ansible を使用する場合は、
GitHub のリリースページから、
``Win32-OpenSSH`` の最新リリースを `インストール <https://github.com/PowerShell/Win32-OpenSSH/wiki/Install-Win32-OpenSSH>`_ することが強く推奨されます。

Windows ホストへの接続として SSH を使用するには、
インベントリーで次の変数を設定します。

    ansible_connection=ssh

    # Set either cmd or powershell not both
    ansible_shell_type=cmd
    # ansible_shell_type=powershell

``ansible_shell_type`` の値は、``cmd`` または ``powershell`` のいずれかである必要があります。
``DefaultShell`` が SSH サービスで構成されていない場合は ``cmd`` を使用し、
``DefaultShell`` として設定されている場合は ``powershell`` を使用します。

SSH 経由で Windows ホストに接続できないのはなぜですか
````````````````````````````````````````````````````
上記のように ``Win32-OpenSSH`` を使用している場合を除き、
:ref:`windows_winrm` を使用して Windows ホストに接続する必要があります。Ansible の出力に SSH が使用されたことが示されている場合は、
接続変数を適切に設定していないか、ホストが接続変数を正しく継承していません。

``ansible_connection: winrm`` が、
Windows ホストのインベントリーに設定されていることを確認してください。

認証情報が拒否されるのはなぜですか
``````````````````````````````````````
これは、誤った認証情報とは無関係の、多種多様なものが原因である可能性があります。

この問題に関する詳細なガイドは、「:ref:`windows_setup`」の
「HTTP 401/認証情報の拒否」を参照してください。

SSL CERTIFICATE_VERIFY_FAILED エラーが発生するのはなぜですか
````````````````````````````````````````````````````````
Python 2.7.9 以降、または SSLContext をバックポートした古いバージョンの Python (RHEL 7 上の Python 2.7.5 など) で Ansible コントローラーを実行している場合は、
コントローラーが、
WinRM が HTTPS 接続に使用している証明書を検証しようとします。証明書を検証できない場合 
(自己署名証明書の場合など) は、
検証プロセスに失敗します。

証明書の検証を無効にするには、
Windows ホストのインベントリーに、
``ansible_winrm_server_cert_validation: ignore`` を追加します。

.. seealso::

   :ref:`windows`
       Windows ドキュメントの目次
   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_best_practices`
       ベストプラクティスのアドバイス
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
