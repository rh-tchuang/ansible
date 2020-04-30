================
Python 3 サポート
================

Ansible 2.5 以降では、Python 3 を使用しますが、Python 3 を使用する 2.5 よりも前のバージョンは、
テクノロジープレビューとみなされます。 以下のトピックでは、
Python 3 を使用できるようにコントローラーと管理マシンを設定する方法を説明します。

.. note:: Ansible は Python バージョン 3.5 以降でのみ動作します。

コントローラー側
----------------------

Python 3 で :command:`/usr/bin/ansible` を最も簡単に実行するには、pip の Python 3 バージョンをインストールします。 これでデフォルトで、Python 3 を使用して :command:`/usr/bin/ansible` を実行できます。

.. code-block:: shell

    $ pip3 install ansible
    $ ansible --version | grep "python version"
    python version = 3.6.2 (default, Sep 22 2017, 08:28:09) [GCC 7.2.1 20170915 (Red Hat 7.2.1-2)]
    
Ansible :ref:`from_source` を実行していて、ソースのチェックアウトに Python 3 を使用するには、``python3`` でコマンドを実行します。 例:

.. code-block:: shell

    $ source ./hacking/env-setup
    $ python3 $(which ansible) localhost -m ping
    $ python3 $(which ansible-playbook) sample-playbook.yml

.. note:: Python 2 または Python 3 向けに、Linux ディストリビューションパッケージが個別でパッケージされている場合があります。 ディストリビューションパッケージから実行する場合には、
    インストールされている Python のバージョンでのみ、
    Ansible を使用できます。 ディストリビューションによっては、
    複数の Python バージョンをインストールする手段を提供するところもあります (別のパッケージや、インストール後に実行するコマンドなど)。 お客様の状況に該当するかどうかは、
    ディストリビューションの情報を確認してください。


コマンドおよび Playbook を使用した管理マシンでの Python 3 の使用
------------------------------------------------------------------

* Ansible は、多数のプラットフォームに同梱されている Python 3 を自動的に検出して使用します。Python 3 インタープリターを明示的に設定するには、
  グループまたはホストレベルで、:command:`/usr/bin/python3` などのように、
  ``ansible_python_interpreter`` のインベントリー変数を Python 3 インタープリターの場所に指定します。デフォルトのインタープリターパスも、
  ``ansible.cfg`` に設定できます。

.. seealso:: 詳細は「:ref:`interpreter_discovery`」を参照してください。

.. code-block:: ini

    # Example inventory that makes an alias for localhost that uses Python3
    localhost-py3 ansible_host=localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3

    # Example of setting a group of hosts to use Python3
    [py3-hosts]
    ubuntu16
    fedora27

    [py3-hosts:vars]
    ansible_python_interpreter=/usr/bin/python3
    
.. seealso:: 詳細は「:ref:`intro_inventory`」を参照してください。

* コマンドまたは Playbook を実行します。

.. code-block:: shell

    $ ansible localhost-py3 -m ping
    $ ansible-playbook sample-playbook.yml


コマンドの実行時に、`-e` コマンドラインオプションを指定して、
手動で Python インタープリターを設定することもできる点に注意してください。  これは、
Python 3で固有のモジュールや Playbook にバグが発生しているかをテストする場合に便利です。 例:

.. code-block:: shell

    $ ansible localhost -m ping -e 'ansible_python_interpreter=/usr/bin/python3'
    $ ansible-playbook sample-playbook.yml -e 'ansible_python_interpreter=/usr/bin/python3'

非互換性が見つかった場合の対処方法
-----------------------------------------

Python 2 および Python 3 の両方で Ansible でコアとなる機能が実行できるように、
複数リリースにわたってバグ修正や、新規テストが追加されました。 ただし、バグはエッジケースなどでまだ存在する可能性があります。
また、Ansible に同梱されている多くのモジュールは、コミュニティーがメンテナンスを実施しており、
すべてがポーティングされているわけではありません。

Python 3 で実行中にバグを発見した場合には、
`Ansible の GitHub プロジェクト <https://github.com/ansible/ansible/issues/>`_ からバグ報告を提出してください。 適切な担当者が対応できるように、
バグ報告には Python3 と記載するようにしてください。

コードを修正して github へのプルリクエストを送信する場合は、
Ansible コードベースで一般的な Python 3 の互換性の問題を修正する方法について、
:ref:`developing_python_3` を参照してください。
