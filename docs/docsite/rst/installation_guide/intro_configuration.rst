.. \_intro\_configuration:

*******************
Ansible の設定
*******************

.. contents:: トピック


このトピックでは、Ansible の設定を制御する方法について説明します。


.. \_the\_configuration\_file:

設定ファイル
==================

Ansible の一部の設定は、設定ファイル (ansible.cfg) で調整できます。
大半の場合には stock 設定で十分ですが、変更したほうがが合理的な場合もあります。
設定ファイルを検索するパスが :ref:`参照ドキュメント<ansible_configuration_settings_locations>` に一覧表示されます

.. \_getting\_the\_latest\_configuration:

最新設定の取得
--------------------------------

パッケージマネージャーから Ansible をインストールした場合は、最新の ``ansible.cfg`` ファイルが ``/etc/ansible`` に存在しているはずです。
更新の場合には、``.rpmnew`` ファイル (またはその他のファイル) が適切な場合もあります。

pip またはソースから Ansible をインストールした場合には、
このファイルを作成して Ansible のデフォルト設定をオーバーライドすることもできます。

`サンプルファイルは GitHub <https://github.com/ansible/ansible/blob/devel/examples/ansible.cfg>`_ で利用できます。

詳細および利用可能な設定の詳細な一覧は、「:ref:`configuration_settings<ansible_configuration_settings>`」を参照してください。Ansible バージョン 2.4 以降では、:ref:`ansible-config` コマンドラインユーティリティーを使用して、利用可能なオプションを表示し、現在の値を確認できます。

詳細については「:ref:`ansible_configuration_settings`」を参照してください。

.. \_environmental\_configuration:

環境設定
===========================

Ansible では、環境変数を使用した設定も可能です。
これらの環境変数が設定されている場合、設定ファイルから読み込まれる設定よりもこちらのほうが優先されます。

「:ref:`ansible_configuration_settings` 」から利用可能な環境変数の詳細な一覧を取得できます。


.. \_command\_line\_configuration:

コマンドラインオプション
====================

コマンドラインにすべての設定オプションが存在するわけではありません。最も便利で一般的と思われるものだけが存在します。
コマンドラインでの設定は、設定ファイルおよび環境を介して渡される設定よりも優先されます。

利用可能なオプションの詳細な一覧は :ref:`ansible-playbook` および :ref:`ansible` で入手できます。

