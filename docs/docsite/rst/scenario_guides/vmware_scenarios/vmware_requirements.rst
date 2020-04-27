.. _vmware_requirements:

********************
VMware の要件
********************

.. contents::
   :local:

SSL 証明書のインストール
===========================

すべての vCenter サーバーおよび ESXi サーバーでは、セキュアな通信を強制するために、すべての接続で SSL 暗号化が必要です。Ansible の SSL 暗号化は、サーバーの SSL 証明書を Ansible コントールノードまたは委譲ノードにインストールして SSL 証明書を有効にする必要があります。

vCenter サーバーまたは ESXi サーバーの SSL 証明書が Ansible コントロールノードに正しくインストールされていない場合は、Ansible VMware モジュールを使用する際に以下の警告が表示されます。

``Unable to connect to vCenter or ESXi API at xx.xx.xx.xx on TCP/443: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777)``

VMware サーバーの SSL 証明書をインストールし、Ansible VMware モジュールを暗号化モードで実行するには、VMware で実行しているサーバーの手順に従ってください。

Ansible 用の vCenter SSL 証明書のインストール
-----------------------------------------------

* 任意の Web ブラウザーから、``https://vcenter-domain.example.com`` などのポート番号のない vCenter Server のベース URL に移動します。

* 右側の灰色の領域の下部にある「Download trusted root CA certificates (信頼されたルート CA 証明書のダウンロード)」のリンクをクリックして、ファイルをダウンロードします。

* ファイルの拡張子を .zip に変更します。このファイルは、すべてのルート証明書とすべての CRL の ZIP ファイルです。

* zip ファイルの内容を展開します。展開したディレクトリーには、両タイプのファイルが含まれる ``.certs`` ディレクトリーが含まれます。数字が拡張子 (.0、.1 など) になっているファイルは、ルート証明書です。

* 証明書ファイルを、オペレーティングシステムに適したプロセスで信頼されている証明書にインストールします。


Ansible 用の ESXi SSL 証明書のインストール
--------------------------------------------

* Ansible VMware モジュール `vmware_host_service_manager` <https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/cloud/vmware/vmware_host_config_manager.py>_ を使用するか、vSphere Web インターフェースを使用して手動で、ESXi で SSH サービスを有効にします。

* 管理認証情報を使用して ESXi サーバーに SSH 接続し、``/etc/vmware/ssl`` ディレクトリーに移動します。

* ``/etc/vmware/ssl`` ディレクトリーにある SCP (Secure Copy) ``rui.crt`` を Ansible コントロールノードへ置きます。

* オペレーティングシステムに適したプロセスで、証明書ファイルをインストールします。
