:orphan:

no-underscore-variable
======================

今後、Ansibleは、識別子 ``_`` を使用して、
メッセージ文字列を国際化することができます。 そのためには、
コードベースで定義されている識別子が競合しないようにする必要があります。

一般的な慣例では、``_`` はダミー変数 (値が役に立たず、
決して使用されない関数から値を受け取る変数) として頻繁に使用されますが、
Ansible では、``dummy`` の識別子はこのために使用しています。

未修正コードの例:

.. code-block:: python

    for _ in range(0, retries):
        success = retry_thing()
        if success:
            break

修正したコードの例:

.. code-block:: python

    for dummy in range(0, retries):
        success = retry_thing()
        if success:
            break
