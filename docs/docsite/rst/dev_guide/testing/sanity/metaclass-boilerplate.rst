metaclass-boilerplate
=====================

ほとんどの Python ファイルには、
ファイルの上部、コメントヘッダー、および ``from __future__ import`` の直後に、次の boilerplate を含める必要があります。

.. code-block:: python

    __metaclass__ = type


Python 2 には「新スタイルのクラス」および「旧スタイルのクラス」が使用されますが、Python 3 には新スタイルのクラスのみが使用されます。
また、``__metaclass__ = type`` boilerplate を追加すると、
そのファイルで定義されているすべてのクラスが新しいスタイルのクラスになります。

.. code-block:: python

    from __future__ import absolute_import, division, print_function
    __metaclass__ = type

    class Foo:
        # This is a new-style class even on Python 2 because of the __metaclass__
        pass
