.. _plugin_filtering_config:

プラグインのフィルター設定
===========================

Ansible 2.5 には、
サイト管理者が Ansible で利用できないモジュールをブラックリストに登録する機能が追加されました。これは、yaml 設定ファイル
(デフォルトでは :file:`/etc/ansible/plugin_filters.yml`) を使用して設定されます。``defaults`` のセクションで ``plugin_filters_cfg`` 設定を使用して、
この設定ファイルのパスを変更します。ファイルの形式は以下のとおりです。

.. code-block:: YAML

    ---
    filter_version: '1.0'
    module_blacklist:
      # Deprecated
      - docker
      # We only allow pip, not easy_install
      - easy_install

このファイルには、2 つのフィールドが含まれています。

* 今後の後方互換性を維持しつつ、
  フォーマットを更新できるようにするバージョン。現在のバージョンは文字列 ``"1.0"`` である必要があります。

* ブラックリストに登録するモジュールの一覧。 ここに登録されるモジュールは、
  Ansible でタスクを呼び出すモジュールを検索するときに検出されません。

.. note::

    Ansible を実行するには、``stat`` モジュールが必要です。そのため、このモジュールをブラックリストモジュールリストに追加しないでください。
