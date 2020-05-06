Kubernetes および OpenShift ガイド
==============================

Kubernetes (K8s) および OpenShift API と対話するためのモジュールは開発中であり、プレビューモードで使用できます。このモジュールを使用するには、要件を確認し、インストールを行い、その他の手順に従います。

要件
------------

モジュールを使用するには、以下が必要になります。

- ソースから Ansible を実行します。手順は、「`ソースからの実行 <./intro_installation.html/#running-from-source>`_」を参照してください。
- モジュールを実行するホストに `OpenShift Rest Client` <https://github.com/openshift/openshift-restclient-python>_ がインストールされています。


インストールと使用
--------------------

このページの作成時点では、個々のモジュールは Ansible リポジトリーの一部ではありませんが、ロール `ansible.kubernetes-modules <https://galaxy.ansible.com/ansible/kubernetes-modules/>`_ をインストールし、それを Playbook に含めることでアクセスできます。

インストールするには、以下を実行します。

.. code-block:: bash

    $ ansible-galaxy install ansible.kubernetes-modules

次に、以下のように Playbook に追加します。

.. code-block:: bash

    ---
    - hosts: localhost
      remote_user: root
      roles:
        - role: ansible.kubernetes-modules
        - role: hello-world

ロールは参照されるため、``hello-world`` はモジュールにアクセスでき、そのモジュールを使用してアプリケーションをデプロイできます。

モジュールは、ロールの ``library`` ディレクトリーにあります。各ディレクトリーは、パラメーターの詳細なドキュメンテーションと、返されるデータ構造が含まれます。ただし、すべてのモジュールにサンプルが含まれているわけではなく、`テストデータ <https://github.com/openshift/openshift-restclient-python/tree/master/openshift/ansiblegen/examples>`_ が作成されているモジュールのみが作成されます。

API での認証
---------------------------

デフォルトで、OpenShift Rest Client は ``~/.kube/config`` を検索し、それが存在する場合は、アクティブなコンテキストを使用して接続します。``context`` パラメーターを使用すると、``kubeconfig`` パラメーターおよびコンテキストを使用してファイルの場所を上書きできます。

基本認証は、``username`` オプションおよび ``password`` オプションを使用してもサポートされます。``host`` パラメーターを使用して URL を上書きできます。証明書認証は、``ssl_ca_cert`` パラメーター、``cert_file`` パラメーター、および ``key_file`` パラメーターで機能し、トークン認証には ``api_key`` パラメーターを使用します。

SSL 証明書の検証を無効にするには、``verify_ssl`` を false に設定します。

問題の報告
`````````````

バグが見つかった場合や、個々のモジュールまたはロールに関する提案をお寄せいただける場合は、`OpenShift Rest Client issues <https://github.com/openshift/openshift-restclient-python/issues>`_ で問題を報告してください。

また、`Ansible <https://github.com/ansible/ansible>`_ リポジトリーに含まれる k8s_common.py ユーティリティーモジュールもあります。バグが見つかった場合や製品に関する提案をお寄せいただける場合は、`Ansible issues <https://github.com/ansible/ansible/issues>`_ で問題を報告してください。
