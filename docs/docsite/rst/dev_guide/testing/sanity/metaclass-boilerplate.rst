metaclass-boilerplate
=====================

ほとんどの Python ファイルには、
ファイルの上部、コメントヘッダーの直後、および ``from __future__ import`` からの次の boilerplate を含める必要があります。

.. code-block:: python

    __metaclass__ = type


Python 2 には「新スタイルのクラス」および「旧スタイルのクラス」がありますが、Python 3 には新スタイルのクラスのみがあります。
boilerplate ``__metaclass__ = type`` を追加すると、
そのファイルで定義されているすべてのクラスも新しいスタイルのクラスになります。

.. code-block:: python

    from __future__ import absolute_import, division, print_function
    __metaclass__ = type

    class Foo:
        # This is a new-style class even on Python 2 because of the __metaclass__
    pass
