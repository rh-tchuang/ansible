dict-itervalues は使用しない
==================

``dict.itervalues`` メソッドは、Python 3 で削除されました。推奨される方法には、以下の 2 つがあります。

.. code-block:: python

    for VALUE in DICT.values():
       pass

.. code-block:: python

    from ansible.module_utils.six import itervalues

    for VALUE in itervalues(DICT):
        pass
