use-argspec-type-path
=====================

AnsibleModule の argument_spec は、標準の python タイプ以外のタイプを認識します。 そのうちの 1 つは
``path`` です。 使用する際は、``path`` と入力すると、
引数が文字列になり、シェル変数とチルド文字が展開されます。

このテストは、モジュールの :func:`os.path.expanduser <python:os.path.expanduser>` の使用を検索します。 検出された場合は、モジュールの argument_spec で ``type='path'`` に置き換えるか、
テストで誤検出としてリストするように、
ユーザーに指示します。
