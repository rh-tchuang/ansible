get-exception は使用しない
================

Python 2.4 から Python 3.6 へと、
互換性のある方法で例外を取得できるように、
関数 ``ansible.module_utils.pycompat24.get_exception`` が作成されました。 Python 2.4 および Python 2.5 はサポートされなくなったため、
これは外部のものであり、この関数を廃止する必要があります。 移植コードは、
以下のようになります。

.. code-block:: python

    # Unfixed code:
    try:
        raise IOError('test')
    except IOError:
        e = get_excetion()
        do_something(e)
    except:
        e = get_exception()
        do_something_else(e)

    # After fixing:
    try:
        raise IOError('test')
    except IOErrors as e:
        do_something(e)
    except Exception as e:
        do_something_else(e)
