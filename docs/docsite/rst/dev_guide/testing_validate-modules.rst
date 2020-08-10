:orphan:

.. _testing_validate-modules:

****************
validate-modules
****************

.. contents:: トピック

Ansible モジュールのテストまたは検証に役立つ Python プログラム。

``validate-modules`` は、健全性テスト ``ansible-test`` の 1 つです。詳細は、「:ref:`testing_sanity`」を参照してください。

本プログラムは、元々 Michay Martz(@sivel) 氏により開発されました。


使用法
=====

.. code:: shell

    cd /path/to/ansible/source
    source hacking/env-setup
    ansible-test sanity --test validate-modules

ヘルプ
====

.. code:: shell

    usage: validate-modules [-h] [-w] [--exclude EXCLUDE] [--arg-spec]
                            [--base-branch BASE_BRANCH] [--format {json,plain}]
                            [--output OUTPUT]
                            modules [modules ...]

    positional arguments:
      modules               Path to module or module directory

    optional arguments:
      -h, --help            show this help message and exit
      -w, --warnings        Show warnings
      --exclude EXCLUDE     RegEx exclusion pattern
      --arg-spec            Analyze module argument spec
      --base-branch BASE_BRANCH
                            Used in determining if new options were added
      --format {json,plain}
                            Output format. Default: "plain"
      --output OUTPUT       Output location, use "-" for stdout. Default "-"


validate-modules の拡張
==========================

``validate-modules`` ツールには「`schema.py <https://github.com/ansible/ansible/blob/devel/test/lib/ansible_test/_data/sanity/validate-modules/validate_modules/schema.py>`_」があり、これは ``DOCUMENTATION`` や ``RETURNS`` などの YAML ブロックの検証に使用されます。


コード
=====

============================================================   ==================   ====================   =========================================================================================
  **エラーコード**                                                 **種類**             **レベル**            **サンプルメッセージ**
------------------------------------------------------------   ------------------   --------------------   -----------------------------------------------------------------------------------------
  ansible-module-not-initialized                               構文               エラー                  モジュールを実行しても、AnsibleModule は初期化されなかった。
  deprecation-mismatch                                         ドキュメント        エラー                  ファイル名、そのメタデータ、ドキュメントの (すべての場所ではなく) いずれかで非推奨または削除されたとマークされたモジュール (非推奨の場合は DOCUMENTATION.deprecated を設定し、削除の場合はすべてのドキュメントを削除)。
  doc-choices-do-not-match-spec                                ドキュメント        エラー                  argument_spec の「choices」の値がドキュメントと一致しない。
  doc-choices-incompatible-type                                ドキュメント        エラー                  argument_spec に定義された型と一致しないドキュメントの chocies 値。
  doc-default-does-not-match-spec                              ドキュメント        エラー                  argument_spec の「default」の値がドキュメントと一致しない。
  doc-default-incompatible-type                                ドキュメント        エラー                  ドキュメントのデフォルト値が、argument_spec に定義された型と一致しない。
  doc-missing-type                                             ドキュメント        エラー                  ドキュメントでは種類を示していないが、``argument_spec`` の引数がデフォルト型 (``str``) を使用している。
  doc-type-does-not-match-spec                                 ドキュメント        エラー                  Argument_spec が、ドキュメントと異なる種類を定義している。
  documentation-error                                          ドキュメント        エラー                  未知の ``DOCUMENTATION`` エラー。
  documentation-syntax-error                                   ドキュメント        エラー                  無効な ``DOCUMENTATION`` スキーマ。
  illegal-future-imports                                       インポート              エラー                   ``from __future__`` インポートは、``absolute_import``、``division``、および ``print_function`` を許可している。
  import-before-documentation                                  インポート              エラー                  ドキュメント変数の前にインポートが見つかった。すべてのインポートは、``DOCUMENTATION``/``EXAMPLES``/``RETURN``/``ANSIBLE_METADATA`` に置かれている必要がある。
  import-error                                                 ドキュメント        エラー                  ``argument_spec`` イントロスペクションのモジュールをインポートしようとしている ``Exception``。
  import-placement                                             場所            警告                レガシーモジュールの場合は、``DOCUMENTATION``/``EXAMPLES``/``RETURN``/``ANSIBLE_METADATA`` の下に置かれている必要がある。
  imports-improper-location                                    インポート              エラー                  インポートが ``DOCUMENTATION``/``EXAMPLES``/``RETURN``/``ANSIBLE_METADATA`` の下に置かれている必要がある。
  incompatible-choices                                         ドキュメント        エラー                  argument_spec の choices 値が argument_spec に定義されていない。
  incompatible-default-type                                    ドキュメント        エラー                  argument_spec のデフォルト値が、argument_spec に定義した型と互換性がない。
  invalid-argument-spec                                        ドキュメント        エラー                  argument_spec の引数を使用する場合は、ディクショナリーまたはハッシュである必要がある。
  invalid-argument-spec-options                                ドキュメント        エラー                  argument_spec のサブオプションが無効になっている。
  invalid-documentation                                        ドキュメント        エラー                  ``DOCUMENTATION`` が有効な YAML ではない。
  invalid-documentation-options                                ドキュメント        エラー                  ``DOCUMENTATION.options`` は、使用時にディクショナリーまたはハッシュである必要がある。
  invalid-examples                                             ドキュメント        エラー                  ``EXAMPLES`` が有効な YAML ではない。
  invalid-extension                                            命名               エラー                  公式の Ansible モジュールでは、python モジュールの拡張子は ``.py`` で、powershell モジュールの拡張子は ``.ps1`` である必要がある。
  invalid-metadata-status                                      ドキュメント        エラー                  非推奨、または削除された ``ANSIBLE_METADATA.status`` には、他のステータスが含まれない。
  invalid-metadata-type                                        ドキュメント        エラー                  ``ANSIBLE_METADATA`` は dic としては提供されず、YAML はサポートされない。無効な ``ANSIBLE_METADATA`` スキーマ。
  invalid-module-schema                                        ドキュメント        エラー                  ``AnsibleModule`` スキーマ検証エラー
  invalid-requires-extension                                   命名               エラー                  モジュール ``#AnsibleRequires -CSharpUtil`` の末尾を .cs にしてはならない。モジュール ``#Requires`` は .psm1 では終わらない。
  last-line-main-call                                          構文               エラー                  最終行以外の ``main()`` の呼出し (または、非推奨およびドキュメントのみのモジュールでは ``removed_module()``)。
  metadata-changed                                             ドキュメント        エラー                  ``ANSIBLE_METADATA`` は、安定板ブランチのポイントリリースでは変更できない。
  missing-doc-fragment                                         ドキュメント        エラー                  ``DOCUMENTATION`` フラグメントがない。
  missing-existing-doc-fragment                                ドキュメント        警告                以前存在していた ``DOCUMENTATION`` フラグメントがない。
  missing-documentation                                        ドキュメント        エラー                  ``DOCUMENTATION`` が提供されていない。
  missing-examples                                             ドキュメント        エラー                  ``EXAMPLES`` が提供されていない。
  missing-gplv3-license                                        ドキュメント        エラー                  GPLv3 ライセンスヘッダーは見つかっていない。
  missing-if-name-main                                         構文               エラー                  最終行の隣に ``if __name__ == "__main__":`` がない。
  missing-main-call                                            構文               エラー                  ``main()`` への呼出が見つからなかった (非推奨またはドキュメントのみのモジュールの場合は ``removed_module()``)。
  missing-metadata                                             ドキュメント        エラー                  ``ANSIBLE_METADATA`` が提供されていない。
  missing-module-utils-basic-import                            インポート              警告                ``ansible.module_utils.basic`` インポートが見つからない。
  missing-module-utils-import-csharp-requirements              インポート              エラー                  ``Ansible.ModuleUtils`` または C# Ansible ユーティリティー要件/インポートが見つからない。
missing-powershell-interpreter                               構文               エラー                  インタープリター行が ``#!powershell`` ではない。
  missing-python-doc                                           命名               エラー                  python ドキュメントファイルが見つからない。
  missing-python-interpreter                                   構文               エラー                  インタープリター行が ``#!/usr/bin/python`` ではない。
  missing-return                                               ドキュメント        エラー                  ``RETURN`` ドキュメントが提供されなかった。
  missing-return-legacy                                        ドキュメント        警告                レガシーモジュールの ``RETURN`` ドキュメントが提供されていない。
  missing-suboption-docs                                       ドキュメント        エラー                  argument_spec の引数にはサブオプションョンがあるが、ドキュメントではサブオプションが定義されていない。
  module-incorrect-version-added                               ドキュメント        エラー                  モジュールレベル ``version_added`` が正確ではない。
  module-invalid-version-added                                 ドキュメント        エラー                  モジュールレベル ``version_added`` が有効なバージョン番号ではない。
  module-utils-specific-import                                 インポート              エラー                  ``module_utils`` インポートは、``*`` ではなく、特定のコンポーネントをインポートする必要がある。
  multiple-utils-per-requires                                  インポート              エラー                  ``Ansible.ModuleUtils`` 要件は、ステートメントごとに複数のモジュールをサポートしない。
  multiple-csharp-utils-per-requires                           インポート              エラー                  Ansible C# ユーティリティー要件が 1 つのステートメントに対して複数のユーティリティーをサポートしない。
no-default-for-required-parameter                            ドキュメント        エラー                  オプションは必須とマークされているが、デフォルトを指定している。デフォルトのある引数は必須とマークしないようにする必要がある。
nonexistent-parameter-documented                             ドキュメント        エラー                  DOCUMENTATION.options に引数が記載され、モジュールにより受け入れられない。
option-incorrect-version-added                               ドキュメント        エラー                   新しいオプションの ``version_added`` が正確ではない。
  option-invalid-version-added                                 ドキュメント        エラー                  新しいオプションの ``version_added`` は有効なバージョン番号ではない。
  parameter-invalid                                            ドキュメント        エラー                  argument_spec の引数が、有効な python 識別子ではない。
  parameter-invalid-elements                                   ドキュメント        エラー                  「elements」の値は、「type」の値が ``list`` である場合に限り有効である。
  implied-parameter-type-mismatch                              ドキュメント        エラー                  Argument_spec には ``type="str"`` の意が含まれるが、ドキュメントでは、別のデータ型として指定されている。
  parameter-type-not-in-doc                                    ドキュメント        エラー                  type 値が ``argument_spec`` に定義されているが、ドキュメントが型を指定していない。
  python-syntax-error                                          構文               エラー                  モジュールの解析時に Python の ``SyntaxError``。
  return-syntax-error                                          ドキュメント        エラー                  ``RETURN`` が有効な YAML ではない。``RETURN`` フラグメントがないが、無効である。
  subdirectory-missing-init                                    命名               エラー                  Ansible モジュールのサブディレクトリーには、``__init__.py`` が含まれている必要がある。
  try-except-missing-has                                       インポート              警告                Try/Except に ``HAS_`` がない。
  undocumented-parameter                                       ドキュメント        エラー                  引数が argument_spec に記載されているが、このモジュールでは文書化されていない。
  unidiomatic-typecheck                                        構文               エラー                  ``type()`` を使用する型比較が見つかった。代わりに ``isinstance()`` を使用してください。
  unknown-doc-fragment                                         ドキュメント        警告                以前から存在する未知の ``DOCUMENTATION`` エラー。
  use-boto3                                                    インポート              エラー                  ``boto`` インポートが見つかったが、新しいモジュールは ``boto3`` を使用する必要がある。
  use-fail-json-not-sys-exit                                   インポート              エラー                  ``sys.exit()`` 呼び出しが検出された。``exit_json``/``fail_json`` である必要がある。
  use-module-utils-urls                                        インポート              エラー                  ``requests`` インポートが検出されたが、代わりに ``ansible.module_utils.urls`` を使用する必要がある。
  use-run-command-not-os-call                                  インポート              エラー                  ``module.run_command`` の代わりに ``os.call`` が使用されている。
  use-run-command-not-popen                                    インポート              エラー                  ``module.run_command`` の代わりに ``subprocess.Popen`` が使用されている。
  use-short-gplv3-license                                      ドキュメント        エラー                  新しいモジュールの GPLv3 ライセンスヘッダーは :ref:`short form <copyright>` である必要がある。
  ============================================================   ==================   ====================   =========================================================================================
