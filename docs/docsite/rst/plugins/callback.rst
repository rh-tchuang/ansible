.. _callback_plugins:

Callback プラグイン
================

.. contents::
   :local:
   :depth: 2

callback プラグインを使用すると、イベントの応答時に、Ansible に新たな動作を追加できます。
デフォルトでは、コールバックプラグインは、コマンドラインプログラムの実行時に表示されるほとんどの出力を制御します。
ただし、出力を追加して他のツールと統合し、イベントをストレージバックエンドにまとめるために使用することもできます。

.. _callback_examples:

Ansible callback プラグイン
------------------------

:ref:`log_plays <log_plays_callback>` コールバックは、Playbook イベントをログファイルに記録する方法の例になります。
:ref:`メール<mail_callback>` コールバックにより、Playbook の失敗時にメールが送信されます。

また、:ref:`say <say_callback>` コールバックは、Playbook のイベントに関連するコンピューターによる音声合成に応答します。

.. _enabling_callbacks:

callback プラグインの有効化
-------------------------

カスタムの callback を有効にするには、カスタムのプラグインを、ロール内の Play の隣りにある ``callback_plugins`` ディレクトリーに配置するか、:ref:`ansible.cfg <ansible_configuration_settings>` で設定した callback ディレクトリーソースの 1 つに配置します。

プラグインは、アルファベット順に読み込まれます。たとえば、`1_first.py` という名前で実装されているプラグインは、`2_second.py` とう名前のプラグインファイルより先に実行されます。

Ansible に同梱されるほとんどの callback プラグインはデフォルトで無効にされており、このプラグインを機能させるには、:ref:`ansible.cfg <ansible_configuration_settings>` ファイルでホワイトリスト化する必要があります。以下に例を示します。

.. code-block:: ini

  #callback_whitelist = timer, mail, profile_roles, collection_namespace.collection_name.custom_callback

``ansible-playbook`` の callback プラグインの設定
--------------------------------------------------

コンソールの出力の主要マネージャーとして指定できるプラグインは 1 つだけです。デフォルトを置き換える場合は、サブクラスに CALLBACK_TYPE = stdout を定義して、:ref:`ansible.cfg <ansible_configuration_settings>` に stdout プラグインを設定する必要があります。以下に例を示します。

.. code-block:: ini

  stdout_callback = dense

または、カスタムのコールバックの場合は以下を実行します。

.. code-block:: ini

  stdout_callback = mycallback

デフォルトでは、この設定は :ref:`ansible-playbook` にだけ影響があります。

ad-hoc コマンドへの callback プラグインの設定
---------------------------------------------

:ref:`ansible` の ad hoc コマンドは、特に標準出力 (stdout) に異なるコールバックプラグインを使用します。
したがって、:ref:`ansible_configuration_settings` には、上記のように定義した標準出力コールバックを使用するように追加の設定が必要です。

.. code-block:: ini

    [defaults]
    bin_ansible_callbacks=True

これを環境変数として設定することもできます。

.. code-block:: shell

    export ANSIBLE_LOAD_CALLBACK_PLUGINS=1


.. _callback_plugin_list:

プラグイン一覧
-----------

``ansible-doc -t callback -l`` を使用すると、利用可能なプラグインの一覧を表示できます。
特定のドキュメントと例を参照する場合には、``ansible-doc -t callback <plugin name>`` を使用してください。

.. toctree:: :maxdepth: 1
    :glob:

    callback/*


.. seealso::

   :ref:`action_plugins`
       Ansible Action プラグイン
   :ref:`cache_plugins`
       Ansible Cache プラグイン
   :ref:`connection_plugins`
       Ansible connection プラグイン
   :ref:`inventory_plugins`
       Ansible inventory プラグインの使用
   :ref:`shell_plugins`
       Ansible Shell プラグイン
   :ref:`strategy_plugins`
       Ansible Strategy プラグイン
   :ref:`vars_plugins`
       Ansible Vars プラグイン
   `ユーザーのメーリングリスト <https://groups.google.com/forum/#!forum/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `webchat.freenode.net <https://webchat.freenode.net>`_
       #ansible IRC chat channel
