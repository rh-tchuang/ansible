assert は使用しない
=========

実稼働用の Ansible python コードで ``assert`` を使用しないでください。Python を最適化して実行すると、
Python は ``assert`` ステートメントを削除し、
Ansible コードベース全体で予期しない動作が発生する可能性があります。

``assert`` を使用する代わりに、単純な ``if`` ステートメントを使用する必要があります。
これにより例外が生じます。``AnsibleError`` および 
``AssertionError`` を継承する 
``AnsibleAssertionError`` という新しい例外があります。可能な場合は、
``AnsibleAssertionError`` よりも具体的な例外を使用します。

モジュールは ``AnsibleAssertionError`` にアクセスできず、
代わりに、より具体的な例外である ``AssertionError`` を発生させるか、
障害点で ``module.fail_json`` を使用する必要があります。
