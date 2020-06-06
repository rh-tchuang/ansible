basestring は使用しない
=============

Python3 ではベースストリングが削除されているため、
``isinstance(s, basestring)`` は使用しないでください。 ``string_types``、``binary_type``、``text_type`` を、
``ansible.module_utils.six`` からインポートして、代わりに ``isinstance(s, string_types)``、
または ``isinstance(s, (binary_type, text_type))`` を使用します。

これが文字列を特定の型に変換するコードの一部である場合、
``ansible.module_utils._text`` には、
``to_text``、``to_bytes``、``to_native`` などの適した関数がいくつか含まれています。
