future-import-boilerplate
=========================

ほとんどの Python ファイルでは、
ファイルの上部、コメントヘッダーの直後に次の boilerplate を含める必要があります。

.. code-block:: python

    from __future__ import (absolute_import, division, print_function)

ここでは、絶対的インポートと相対的インポート、除算、および出力に Python 3 セマンティクスを使用します。 これを実行することで、
Python 3 セマンティクスに従って、Python 2 と Python 3 の間で移植可能なコードを作成できます。


absolute_import
---------------

Python 2 が、``import copy`` など、ファイル内の名前のインポートを検出すると、
ファイルと同じディレクトリーから ``copy.py`` を読み込もうとします。 これは、そのディレクトリーに、その名前の python ファイルがあり、
同じ名前の ``sys.path`` に python モジュールがある場合に問題が発生する場合があります。 このとき、
Python 2 は、同じディレクトリーにあるものは読み込みますが、
``sys.path`` にあるものを読み込む方法はありません。 Python 3 では、デフォルトでインポートを絶対的にすることでこれを修正しています。``import copy`` は、
``sys.path`` から ``copy.py`` を検索します。 同じディレクトリーから ``copy.py`` をインポートする場合は、
コードは、相対的インポート ``from . import copy`` を実行するために変更する必要があります。

.. seealso::

    * `Absolute and relative imports <https://www.python.org/dev/peps/pep-0328>`_

division
--------

Python 2 では、整数で使用すると、除算演算子 (``/``) は整数値を返します。 剰余があると、
この部分は省略されます (別名 `床除算`)。 Python 3では、
除算演算子 (``/``) は常に浮動小数点数を返します。 商の整数部分を計算する必要があるコードは、
代わりに床除算演算子（`//`）を使用する必要があります。

.. seealso::

    * `Changing the division operator <https://www.python.org/dev/peps/pep-0238>`_

print_function
--------------

Python 2 では、:func:`python:print` はキーワードです。 Python 3 では、
:func:`python3:print` は異なるパラメーターを持つ関数です。 この ``__future__`` を使用すると、Python 3 の出力セマンティクスをどこでも使用できます。

.. seealso::

    * `Make print a function <https://www.python.org/dev/peps/pep-3105>`_

