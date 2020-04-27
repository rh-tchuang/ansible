.. _lookup_plugins:

Lookup プラグイン
==============

.. contents::
   :local:
   :depth: 2

Lookup プラグインを使用すると、外部をソースとするデータに Ansible がアクセスできるようになります。
たとえば、外部データソースおよびサービスの問い合わせだけでなく、ファイルシステムの読み取りも含まれます。
このようなプラグインは、全テンプレート作成などのように、ターゲット/リモートマシンではなく、Ansible のコントロールマシンで評価されます。

Lookup プラグインにより返されるデータは、Ansible で標準のテンプレートシステムを使用して利用できるようになります。
このデータは、通常、そのシステムからの情報で変数またはテンプレートを読み込むために使用されます。

Lookup は、Jinja2 テンプレート化言語に対する Ansible 固有の拡張です。

.. note::
   - Lookup は、実行したスクリプトに基づいて実行されるローカルタスクとは異なり、
     ロールまたはプレイに関連して作業ディレクトリーで実行されます。
   - Ansible バージョン 1.9 以降、wantlist=True を lookup に渡して、Jinja2 テンプレート「for」ループで使用できます。
   - Lookup プラグインは高度な機能です。Ansible Play の使用方法に関する適切な知識が必要です。

.. warning::
   - lookup によってはシェルに引数を渡します。リモート/信頼されていないソースから変数を使用する場合には、`|quote` フィルターで、安全に使用できるようにします。


.. _enabling_lookup:

Lookup プラグインの有効化
-----------------------

カスタムの lookup を有効にするには、カスタムの lookup を、ロール内の Play の隣りにある ``lookup_plugins`` ディレクトリーに配置するか、:ref:`ansible.cfg <ansible_configuration_settings>` で設定した lookup ディレクトリーソースの 1 つに配置します。


.. _using_lookup:

lookup プラグインの使用
--------------------

Lookup プラグインは、Ansible でテンプレートを使用できる場所で使用できます。これは Play、変数ファイル、または :ref:`テンプレート<template_module>` モジュールの Jinja2 テンプレートで使用できます。

.. code-block:: YAML+Jinja

  vars:
    file_contents: "{{lookup('file', 'path/to/file.txt')}}"

Lookup は、ループで必要付加欠な部分となっています。``with_`` がある場合には、アンダースコアの後の部分はルックアップの名前になります。
これが、ほとんどの lookup がリストを出力し、そのリストを入力として扱う理由です。``with_items`` が :ref:`items <items_lookup>` lookup を使用します::

  tasks:
    - name: count to 3
      debug: msg={{item}}
      with_items: [1, 2, 3]

Lookup と :ref:`playbooks_filters`、:ref:`playbooks_tests`、またはそれぞれを組み合わせて複雑なデータ生成やデータ操作が可能です。例::

  tasks:
    - name: valid but useless and over complicated chained lookups and filters
      debug: msg="find the answer here:\n{{ lookup('url', 'https://google.com/search/?q=' + item|urlencode)|join(' ') }}"
      with_nested:
        - "{{lookup('consul_kv', 'bcs/' + lookup('file', '/the/question') + ', host=localhost, port=2000')|shuffle}}"
        - "{{lookup('sequence', 'end=42 start=2 step=2')|map('log', 4)|list)}}"
        - ['a', 'c', 'd', 'c']

.. versionadded:: 2.6

Lookup プラグインのエラーの動作を制御するには、``errors`` を ``ignore``、``warn`` または ``strict`` に設定します。デフォルト設定は ``strict`` で、(エラーがある場合に) タスクが失敗します。以下に例を示します。

エラーを無視するには、以下のコマンドを実行します。

    - name: file doesnt exist, but i dont care .. file plugin itself warns anyways ...
      debug: msg="{{ lookup('file', '/idontexist', errors='ignore') }}"

.. code-block:: ansible-output

    [WARNING]: Unable to find '/idontexist' in expected paths (use -vvvvv to see paths)

    ok: [localhost] => {
        "msg": ""
    }


失敗させるのではなく警告を出すには、以下を実行します。

    - name: file doesnt exist, let me know, but continue
      debug: msg="{{ lookup('file', '/idontexist', errors='warn') }}"

.. code-block:: ansible-output

    [WARNING]:Unable to find '/idontexist' in expected paths (use -vvvvv to see paths)

    [WARNING]:An unhandled exception occurred while running the lookup plugin 'file'.Error was a <class 'ansible.errors.AnsibleError'>, original message: could not locate file in lookup: /idontexist

    ok: [localhost] => {
        "msg": ""
    }


致命的なエラー (デフォルト)::

    - name: file doesnt exist, FAIL (this is the default)
      debug: msg="{{ lookup('file', '/idontexist', errors='strict') }}"

.. code-block:: ansible-output

    [WARNING]:Unable to find '/idontexist' in expected paths (use -vvvvv to see paths)

    fatal: [localhost]:FAILED! => {"msg":"An unhandled exception occurred while running the lookup plugin 'file'.Error was a <class 'ansible.errors.AnsibleError'>, original message: could not locate file in lookup: /idontexist"}


.. _query:

``query`` を指定した Lookup プラグインの呼び出し
--------------------------------------

.. versionadded:: 2.5

Ansible 2.5 で、lookup プラグインを呼び出す ``query`` と言う jinja2 関数が新たに追加されました。``lookup`` と ``query`` の相違点は主に、``query`` は常にリストを返す点です。
``lookup`` の動作は、デフォルトではコンマ区切りの文字列値を返します。``lookup`` は、 ``wantlist=True`` を使用して、リストを返すように明示的に設定することができます。

これが追加されたのは主に、他の ``lookup`` を使用できるように後方互換性を保ちつつ、より簡単で一貫性を保つことのできる、``loop`` キーワードとの対話インターフェースを新たに提供するためです。

以下の例はどちらも同等の操作ができます。

.. code-block:: jinja

    lookup('dict', dict_variable, wantlist=True)

    query('dict', dict_variable)

上記の例のように、``query`` を使用する場合には ``wantlist=True`` の動作は暗黙的になります。

また、 ``query`` の略式となる ``q`` が導入されました。

.. code-block:: jinja

    q('dict', dict_variable)


.. _lookup_plugins_list:

プラグイン一覧
-----------

``ansible-doc -t lookup -l`` を使用すると、利用可能なプラグインの一覧を表示できます。特定のドキュメントと例を参照する場合には、``ansible-doc -t lookup <plugin name>`` を使用してください。


.. toctree:: :maxdepth: 1
    :glob:

    lookup/*

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`inventory_plugins`
       Ansible inventory プラグインの使用
   :ref:`callback_plugins`
       Ansible callback プラグイン
   :ref:`playbooks_filters`
       Jinja2 filter プラグイン
   :ref:`playbooks_tests`
       Jinja2 test プラグイン
   :ref:`playbooks_lookups`
       Jinja2 lookup プラグイン
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
