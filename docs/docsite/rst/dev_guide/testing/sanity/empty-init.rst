empty-init
==========

以下のディレクトリー下の ``__init__.py`` ファイルは空である必要があります。 これらの一部 (モジュールおよびテスト) では、
コードを含む ``__init__.py`` ファイルは使用されません。 その他 (module_utils) では、
空の ``__init__.py`` で許可される Python 名前空間を使用できるようにしたいと考えています。

- ``lib/ansible/modules/``
- ``lib/ansible/module_utils/``
- ``test/units/``
