import
======

すべての Python は、``lib/ansible/modules/`` および ``lib/ansible/module_utils/`` にインポートされます。
これは、Python 標準ライブラリーからのものではなく、try/except ImportError ブロックにインポートする必要があります。
