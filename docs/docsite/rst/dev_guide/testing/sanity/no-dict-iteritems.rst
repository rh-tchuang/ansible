dict-iteritems は使用しない
=================

``dict.iteritems`` メソッドは、Python 3 で削除されました。推奨される方法には、以下の 2 つがあります。

.. code-block:: python

    for KEY, VALUE in DICT.items():
       pass

.. code-block:: python

    from ansible.module_utils.six import iteritems

    for KEY, VALUE in iteritems(DICT):
        pass
