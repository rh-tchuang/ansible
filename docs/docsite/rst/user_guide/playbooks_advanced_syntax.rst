.. _playbooks_advanced_syntax:

***************
高度な構文
***************

このページの高度な yaml 構文の例では、Ansible で使用される yaml ファイルに置かれるデータをさらに制御できます。Python 固有の yaml に関する追加情報は、公式の `PyYAML ドキュメント <https://pyyaml.org/wiki/PyYAMLDocumentation#YAMLtagsandPythontypes>`_ を参照してください。

.. contents::
   :local:

.. _unsafe_strings:

安全でない文字列または raw 文字列
=====================

Ansible は、変数値を「安全ではない」として宣言する内部データタイプを提供します。つまり、変数値内に保持されるデータは安全ではない状態で処理される必要があり、安全ではない文字置換や情報の公開を防ぎます。

Jinja2 にはエスケープの機能が含まれ、``{% raw %} ... {% endraw %}`` などの機能を使用してデータをテンプレート化しないように Jinja2 に指示しますが、これにより、より包括的な実装を使用して値がテンプレート化されないようにします。

YAML タグを使用して、以下のように ``!unsafe`` タグを使用して値を「安全ではない」としてマークすることもできます。

.. code-block:: yaml

    ---
    my_unsafe_variable: !unsafe 'this variable has {{ characters that should not be treated as a jinja2 template'

Playbook では、以下のようになります。

    ---
    hosts: all
    vars:
        my_unsafe_variable: !unsafe 'unsafe value'
    tasks:
        ...

ハッシュやアレイなどの複雑な変数の場合は、個々の要素で以下のような ``!unsafe`` を使用します。

    ---
    my_unsafe_array:
        - !unsafe 'unsafe element'
        - 'safe element'

    my_unsafe_hash:
        unsafe_key: !unsafe 'unsafe value'

.. _anchors_and_aliases:

yaml アンカーおよびエイリアス: 変数値の共有
=================================================

`yaml アンカーおよびエイリアス <https://yaml.org/spec/1.2/spec.html#id2765878>`_ は、柔軟な方法で共有変数の値を定義、維持、および使用するのに役立ちます。
アンカーは ``&`` で定義してから、``*`` で示されるエイリアスを使用して参照します。アンカーで 3 つの値を設定し、エイリアスでこれらの値のうち 2 つを使用し、3 番目の値を上書きする例を次に示します。

    ---
    ...
    vars:
        app1:
            jvm: &jvm_opts
                opts: '-Xms1G -Xmx2G'
                port: 1000
                path: /usr/lib/app1
        app2:
            jvm:
                <<: *jvm_opts
                path: /usr/lib/app2
    ...

ここでは、``app1`` および ``app2`` は、アンカー ``&jvm_opts`` およびエイリアス ``*jvm_opts`` を使用して、``opts`` および ``port`` の値を共有します。
``path`` の値は、``<<`` または `マージオペレーター<https://yaml.org/type/merge.html>`_ でマージされます。

アンカーとエイリアスを使用すると、ネストされた変数を含む変数値の複雑なセットを共有することもできます。別の変数の値が含まれる変数値がある場合は、個別に定義できます。

      vars:
        webapp_version:1.0
        webapp_custom_name:ToDo_App-1.0

これは非効率的であり、大規模になると、より多くの維持が必要になります。名前にバージョン値を組み込むには、``app_version`` のアンカーと、``custom_name`` のエイリアスを使用できます。

      vars:
        webapp:
            version: &my_version 1.0
            custom_name:
                - "ToDo_App"
                - *my_version

これで、``custom_name`` の値の ``app_version`` の値を再利用し、テンプレートで出力を使用できます::

    ---
    - name: Using values nested inside dictionary
      hosts: localhost
      vars:
        webapp:
            version: &my_version 1.0
            custom_name:
                - "ToDo_App"
                - *my_version
      tasks:
      - name: Using Anchor value
        debug:
            msg: My app is called "{{ webapp.custom_name | join('-') }}".

``version`` の値に ``&my_version`` アンカーを付けてアンカーを作成し、``*my_version`` エイリアスで再利用しました。アンカーとエイリアスを使用すると、ディクショナリー内のネストされた値にアクセスできます。

.. seealso::

   :ref:`playbooks_variables`
       変数の詳細
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
