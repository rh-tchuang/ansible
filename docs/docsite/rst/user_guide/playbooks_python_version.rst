.. _pb-py-compat:

Python のバージョンおよびテンプレート
=============================

Jinja2 テンプレートは、Python データタイプと標準機能を活用します。 これにより、
実行できる豊富な操作セットを作成します。 ただし、
これは、
基礎となる Python の特定の詳細がテンプレート作成者に表示されます。 Ansible Playbook はテンプレートと変数に Jinja2 を使用するため、
Playbook の作者が、
このような詳細に注意する必要があることも意味します。

特に明記しない限り、この違いは、
Python2 と Python3 で Ansible を実行する場合に限り重要です。 Python2 と Python3 内の変更は、
一般に、jinja2 レベルでは表示されないほど小さくなります。

.. _pb-py-compat-dict-views:

ディクショナリービュー
----------------

Python2 では、:meth:`dict.keys`、:meth:`dict.values`、および :meth:`dict.items` 
の各メソッドがリストを返します。 Jinja2 は、
Ansible がリストに戻せる文字列表現で Ansible に返します。 Python3 では、
これらのメソッドは :ref:`ディクショナリービュー <python3:dict-views>` オブジェクトを返します。 Jinja2 がディクショナリービューに対して返す文字列表現は、
Ansible が
解析してリストに戻すことができません。 ただし、
:meth:`dict.keys`、
:meth:`dict.values`、または :meth:`dict.items` を使用する場合は常に :func:`list <jinja2:list>` フィルターを使用することでこの移植性を容易にできます::

    vars:
      hosts:
        testhost1: 127.0.0.2
        testhost2: 127.0.0.3
    tasks:
      - debug:
          msg: '{{ item }}'
        # Only works with Python 2
        #loop: "{{ hosts.keys() }}"
        # Works with both Python 2 and Python 3
        loop: "{{ hosts.keys() | list }}"
    
.. _pb-py-compat-iteritems:

dict.iteritems()
----------------

Python2 では、ディクショナリーには :meth:`~dict.iterkeys`、
:meth:`~dict.itervalues`、および :meth:`~dict.iteritems` の各メソッドがあります。 この方法は、
Python3 で削除されました。 :meth:`dict.keys`、
:meth:`dict.values`、および :meth:`dict.items` を使用して、
Playbook と Jinja2 テンプレートを Python2 と Python3 の両方と互換性を持たせるようにします。

    vars:
      hosts:
        testhost1: 127.0.0.2
        testhost2: 127.0.0.3
    tasks:
      - debug:
          msg: '{{ item }}'
        # Only works with Python 2
        #loop: "{{ hosts.iteritems() }}"
        # Works with both Python 2 and Python 3
        loop: "{{ hosts.items() | list }}"
    
.. seealso::
    * ここで、
      :func:`list filter<jinja2:list>` が必要な理由は、
      :ref:`pb-py-compat-dict-views` エントリーを参照してください。
