main-display は使用しない
===============

Ansible 2.8 では、``Display`` は、``__main__`` からインポートされなくなりました。

``Display`` はシングルトンで、以下のように使用する必要があります。

   from ansible.utils.display import Display
   display = Display()

``try/except`` ブロック内の ``from __main__ import display`` 
から試行する必要がなくなりました。
