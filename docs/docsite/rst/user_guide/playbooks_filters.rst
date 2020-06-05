.. _playbooks_filters:

フィルター
-------

.. contents:: トピック


Ansible のフィルターは Jinja2 から取得して、テンプレート式内のデータの変換に使用されます。 Jinja2 には多くのフィルターが同梱されます。公式の Jinja2 テンプレートドキュメントの「`builtin filters`_」を参照してください。

テンプレートは、タスクのターゲットホストでは **なく**、Ansible コントローラーで実行されるため、フィルターはローカルデータを操作するため、コントローラーでも実行されます。

Jinja2 が提供するもののほかに、Ansible には独自のフィルターが同梱され、ユーザーが独自のカスタムフィルターを追加できるようにします。

.. _filters_for_formatting_data:

データフォーマットのフィルター
```````````````````````````

以下のフィルターは、テンプレートのデータ構造を取り、これを若干異なる形式でレンダリングします。 これらは、
時々デバッグに役立ちます::

    {{ some_variable | to_json }}
    {{ some_variable | to_yaml }}
    
人間が判読できる出力には、以下を使用できます::

    {{ some_variable | to_nice_json }}
    {{ some_variable | to_nice_yaml }}
    
両方のインデントを変更することもできます (バージョン 2.2 の新機能)。

    {{ some_variable | to_nice_json(indent=2) }}
    {{ some_variable | to_nice_yaml(indent=8) }}
    

``to_yaml`` フィルターおよび ``to_nice_yaml`` フィルターは、デフォルトの 80 の記号文字列の長さ制限のある `PyYAML library`_ を使用します。これにより、80 番目のシンボルの後に予期しない改行が破損します (80 番目の記号の後に空白がある場合)。
このような動作を回避し、長い行を生成するには、``width`` オプションを使用できます。

    {{ some_variable | to_yaml(indent=8, width=1337) }}
    {{ some_variable | to_nice_yaml(indent=8, width=1337) }}
    
ハードコードされた数値の代わりに ``float("inf")`` のような構造を使用する方が適切かもしれませんが、フィルターは Python 関数のプロキシーをサポートしていません。
また、他の YAML パラメーターのパススルーにも対応していることに注意してください。完全なリストは、`PyYAML ドキュメント`_ を参照してください。


または、すでにフォーマットされている一部のデータで読み取る場合があります。

    {{ some_variable | from_json }}
    {{ some_variable | from_yaml }}
    
例:

  tasks:
    - shell: cat /some/path/to/file.json
      register: result

    - set_fact:
        myvar: "{{ result.stdout | from_json }}"


.. versionadded:: 2.7

複数ドキュメントの yaml 文字列を解析するには、``from_yaml_all`` フィルターが提供されます。
``from_yaml_all`` フィルターは、解析された yaml ドキュメントのジェネレーターを返します。

例:

  tasks:
    - shell: cat /some/path/to/multidoc-file.yaml
      register: result
    - debug:
        msg: '{{ item }}'
      loop: '{{ result.stdout | from_yaml_all | list }}'


.. _forcing_variables_to_be_defined:

定義する変数の強制
```````````````````````````````

Ansible および ansible.cfg のデフォルトの動作は、変数が定義されていない場合に失敗しますが、これをオフにすることができます。

これにより、この機能をオフにすると、この明示的なチェックが可能になります。

    {{ variable | mandatory }}

変数の値はそのまま使用されますが、定義されていない場合は、テンプレートの評価でエラーが発生します。


.. _defaulting_undefined_variables:

未定義変数のデフォルト設定
``````````````````````````````

Jinja2 は、変数が定義されていない場合に失敗するより適切な「デフォルト」フィルターを提供します。

    {{ some_variable | default(5) }}

上記の例では、「some_variable」変数が定義されていない場合、
使用される値はエラーではなく、5 になります。

変数が false または空の文字列に評価されるときにデフォルト値を使用する場合は、
2 番目のパラメーターを ``true`` に設定する必要があります::

    {{ lookup('env', 'MY_USER') | default('admin', true) }}


.. _omitting_undefined_variables:

パラメーターの省略
```````````````````

Ansible 1.8 より、特別な `omit` 変数を使用して、デフォルトのフィルターを使用してモジュールパラメーターを省略できるようになりました。

    - name: touch files with an optional mode
      file:
        dest: "{{ item.path }}"
        state: touch
        mode: "{{ item.mode | default(omit) }}"
      loop:
        - path: /tmp/foo
        - path: /tmp/bar
        - path: /tmp/baz
          mode: "0444"
    
リストの最初の 2 つのファイルの場合、デフォルトのモードはシステムの umask によって決定されます。
これは、最後のファイルが `mode=0444` オプションを受け取る間、`mode=` パラメーターがファイルモジュールに送信されないためです。

.. note:: ``default(omit)`` フィルターの後にフィルターを「チェーン」する場合は、代わりに以下のようなフィルターを実行する必要があります。
      ``"{{ foo | default(None) | some_filter or omit }}"``この例では、デフォルトの ``None`` (Python null) 値により、
      後のフィルターが失敗し、ロジックの ``or omit`` 部分がトリガーされなくなります。この方法で ``omit`` を使用することは、
      連鎖する後のフィルターに非常に固有であるため、これを行う場合は、トライアル・アンド・エラーの準備をしてください。

.. _list_filters:

リストのフィルター
````````````

これらのフィルターはすべて、list 変数で動作します。

.. versionadded:: 1.8

数字リストから最小値を取得するには、以下を実行します。

    {{ list1 | min }}

数字リストから最大値を取得するには、以下を実行します。

    {{ [3, 4, 2] | max }}

.. versionadded:: 2.5

リストをフラット化します (`flatten` フラットルックアップと同等)。

    {{ [3, [4, 2] ] | flatten }}

リストの最初のレベルのみをフラット化します (`items` ルックアップと同等)。

    {{ [3, [4, [2]] ] | flatten(levels=1) }}


.. _set_theory_filters:

集合論フィルター
``````````````````
これらの関数はすべて、セットまたはリストから一意のセットを返します。

.. versionadded:: 1.4

リストから一意のセットを取得するには、以下を指定します。

    {{ list1 | unique }}

2 つのリストを組み合わせて取得するには、以下を指定します。

    {{ list1 | union(list2) }}

2 つのリスト (両方の全項目の一意のリスト) で構成されるものを取得するには、以下を指定します。

    {{ list1 | intersect(list2) }}

2 つのリストの相違点を取得するには (2 に存在しない 1 の項目）、以下を指定します。

    {{ list1 | difference(list2) }}

2 つのリストの対称的な違いを取得する (各リストへの除外) には、以下を指定します。

    {{ list1 | symmetric_difference(list2) }}


.. _dict_filter:

ディクショナリーフィルター
```````````

.. versionadded:: 2.6


ディクショナリーをループに適した項目リストに変更するには、`dict2items` を使用します:

    {{ dict | dict2items }}

以下を、

    tags:
      Application: payment
      Environment: dev

以下のように設定します::

    - key:Application
      value: payment
    - key:Environment
      value: dev

.. versionadded:: 2.8

``dict2items`` は、``key_name`` と ``value_name`` の 2 つのキーワード引数を受け入れ、変換に使用するキー名を設定できます。

    {{ files | dict2items(key_name='file', value_name='path') }}

以下を、

    files:
      users: /etc/passwd
      groups: /etc/group

以下のように設定します::

    - file: users
      path: /etc/passwd
    - file: groups
      path: /etc/group

items2dict filter
`````````````````

.. versionadded:: 2.7

このフィルターは、2 つのキーを持つディクショナリーのリストを 1 つのディクショナリーに変換し、それらのキーの値を ``key: value`` のペアにマッピングします。

    {{ tags | items2dict }}

以下を、

    tags:
      - key:Application
        value: payment
      - key:Environment
        value: dev

以下のように設定します::

    Application: payment
    Environment: dev

これは、``dict2items`` フィルターとは異なります。

``items2dict`` は、``key_name`` と ``value_name`` の 2 つのキーワード引数を受け入れ、変換に使用するキーの名前を設定できます。

    {{ tags | items2dict(key_name='key', value_name='value') }}


.. _zip_filter:

zip フィルターおよび zip_longest フィルター
```````````````````````````

.. versionadded:: 2.3

他のリストの要素を組み合わせるリストを取得するには、``zip`` を使用します::

    - name: give me list combo of two lists
      debug:
       msg: "{{ [1,2,3,4,5] | zip(['a','b','c','d','e','f']) | list }}"

    - name: give me shortest combo of two lists
      debug:
        msg: "{{ [1,2,3] | zip(['a','b','c','d','e','f']) | list }}"

すべてのリストを常に使い切るには、``zip_longest`` を使用します::

    - name: give me longest combo of three lists , fill with X
      debug:
        msg: "{{ [1,2,3] | zip_longest(['a','b','c','d','e','f'], [21, 22, 23], fillvalue='X') | list }}"


上記の ``items2dict`` フィルターの出力と同様に、これらのフィルターを使用して ``dict`` を作成できます。

    {{ dict(keys_list | zip(values_list)) }}

以下を、

    keys_list:
      - one
      - two
    values_list:
      - apple
      - orange

以下のように設定します::

    one: apple
    two: orange

サブ要素フィルター
``````````````````

.. versionadded:: 2.7

``subelements`` のルックアップと同様、オブジェクトとそのオブジェクトのサブ要素の値の積を生成します。

    {{ users | subelements('groups', skip_missing=True) }}

以下を、

    users:
    - name: alice
      authorized:
      - /tmp/alice/onekey.pub
      - /tmp/alice/twokey.pub
      groups:
      - wheel
      - docker
    - name: bob
      authorized:
      - /tmp/bob/id_rsa.pub
      groups:
      - docker

以下のように設定します::

    -
      - name: alice
        groups:
        - wheel
        - docker
        authorized:
        - /tmp/alice/onekey.pub
        - /tmp/alice/twokey.pub
      - wheel
    -
      - name: alice
        groups:
        - wheel
        - docker
        authorized:
        - /tmp/alice/onekey.pub
        - /tmp/alice/twokey.pub
      - docker
    -
      - name: bob
        authorized:
        - /tmp/bob/id_rsa.pub
        groups:
        - docker
      - docker

``loop`` でこのフィルターを使用する例::

    - name:Set authorized ssh key, extracting just that data from 'users'
      authorized_key:
        user: "{{ item.0.name }}"
    key: "{{ lookup('file', item.1) }}"
  loop: "{{ users | subelements('authorized') }}"
    
.. _random_mac_filter:

ランダムの MAC アドレスフィルター
`````````````````````````

.. versionadded:: 2.6

このフィルターは、文字列接頭辞からランダムな MAC アドレスを生成するために使用できます。

文字列接頭辞「52:54:00」で始まるランダムな MAC アドレスを取得するには、次のコマンドを実行します。

    "{{ '52:54:00' | random_mac }}"
    # => '52:54:00:ef:1c:03'

接頭辞の文字列で不具合が生じた場合は、フィルターによりエラーが生じることに注意してください。

Ansible バージョン 2.9 では、シードから乱数ジェネレーターを初期化することもできます。これにより、MAC アドレスをランダムで冪等な MAC アドレスを作成できます。

    "{{ '52:54:00' | random_mac(seed=inventory_hostname) }}"

.. _random_filter:

乱数フィルター
````````````````````

.. versionadded:: 1.6

このフィルターは、デフォルトの jinja2 ランダムフィルター (一連のアイテムからランダムなアイテムを返す) と同様に使用できますが、
範囲に基づいて乱数を生成することもできます。

リストからランダムなアイテムを取得するには、以下を指定します。

    "{{ ['a','b','c'] | random }}"
    # => 'c'

0 から指定された数字の間の乱数を取得するには、次のコマンドを実行します。

    "{{ 60 | random }} * * * * root /script/from/cron"
    # => '21 * * * * root /script/from/cron'

0 から 100 までの 10 のステップで乱数を取得します::

    {{ 101 | random(step=10) }}
    # => 70

0 から 100 までの 10 のステップで乱数を取得します::

    {{ 101 | random(1, 10) }}
    # => 31
    {{ 101 | random(start=1, step=10) }}
    # => 51

Ansible バージョン 2.3 では、シードから乱数ジェネレーターを初期化することもできます。これにより、random-but-idempotent (ランダムで冪等な数) を作成することができます。

    "{{ 60 | random(seed=inventory_hostname) }} * * * * root /script/from/cron"


シャッフルフィルター
``````````````

.. versionadded:: 1.8

このフィルターは、既存のリストをランダム化し、呼び出しごとに異なる順序を提供します。

既存の一覧からランダムなリストを取得するには、以下を実行します。

    {{ ['a','b','c'] | shuffle }}
    # => ['c','a','b']
    {{ ['a','b','c'] | shuffle }}
    # => ['b','c','a']

Ansible バージョン 2.3 では、リストを冪等にシャッフルすることもできます。必要なのは、シードだけです::

    {{ ['a','b','c'] | shuffle(seed=inventory_hostname) }}
    # => ['b','a','c']

「リスト可能」ではない項目と併用する場合は、noop であることに注意してください。それ以外の場合は、必ず一覧を返します。


.. _math_stuff:

計算
````

.. versionadded:: 1.9


対数を取得します (デフォルトは e)::

    {{ myvar | log }}

ベース 10 の対数を取得します::

    {{ myvar | log(10) }}

2 の累乗 (または 5)::

    {{ myvar | pow(2) }}
    {{ myvar | pow(5) }}
    
平方根または 5 番目::

    {{ myvar | root }}
    {{ myvar | root(5) }}
    
jinja2 にはすでに abs() や round() があります。

.. json_query_filter:

JSON クエリーフィルター
`````````````````

.. versionadded:: 2.2

場合によっては、JSON 形式の複雑なデータ構造になり、その中の小さなデータセットのみを抽出する必要があります。**json_query** フィルターを使用すると、複雑な JSON 構造をクエリーでき、ループ構造を使用してこれを繰り返すことができます。

.. note:: このフィルターは **jmespath** で構築され、同じ構文を使用できます。たとえば、`jmespath サンプル <http://jmespath.org/examples.html>`_ を参照してください。

ここで、以下のデータ構造を取ります。

    {
        "domain_definition": {
            "domain": {
                "cluster": [
                    {
                        "name": "cluster1"
                    },
                    {
                        "name": "cluster2"
                    }
                ],
                "server": [
                    {
                        "name": "server11",
                        "cluster": "cluster1",
                        "port": "8080"
                    },
                    {
                        "name": "server12",
                        "cluster": "cluster1",
                        "port": "8090"
                    },
                    {
                        "name": "server21",
                        "cluster": "cluster2",
                        "port": "9080"
                    },
                    {
                        "name": "server22",
                        "cluster": "cluster2",
                        "port": "9090"
                    }
                ],
                "library": [
                    {
                        "name": "lib1",
                        "target": "cluster1"
                    },
                    {
                        "name": "lib2",
                        "target": "cluster2"
                    }
                ]
            }
        }
    }
    
この構造からすべてのクラスターを抽出するには、以下のクエリーを使用できます::

    - name:"Display all cluster names"
      debug:
        var: item
      loop: "{{ domain_definition | json_query('domain.cluster[*].name') }}"

すべてのサーバー名に対しても同様です::

    - name:"Display all server names"
      debug:
        var: item
      loop: "{{ domain_definition | json_query('domain.server[*].name') }}"

以下の例では cluster1 からのポートを示しています::

    - name:"Display all ports from cluster1"
      debug:
        var: item
      loop: "{{ domain_definition | json_query(server_name_cluster1_query) }}"
      vars:
        server_name_cluster1_query: "domain.server[?cluster=='cluster1'].port"

.. note:: 変数を使用すると、クエリーの読み取りがより容易になります。

または、ポートをコンマ区切りの文字列で出力します。

    - name:"Display all ports from cluster1 as a string"
      debug:
        msg: "{{ domain_definition | json_query('domain.server[?cluster==`cluster1`].port') | join(', ') }}"

.. note:: ここでは、バッククォートを使用してリテラルを引用符で囲むと、引用符のエスケープが回避され、読みやすさが維持されます。

または、YAML `一重引用符エスケープ <https://yaml.org/spec/current.html#id2534365>`_ を使用します::

    - name:"Display all ports from cluster1"
      debug:
        var: item
      loop: "{{ domain_definition | json_query('domain.server[?cluster==''cluster1''].port') }}"

.. note:: YAML の単一引用符内で単一引用符をエスケープする場合は、単一引用符を 2 倍にします。

この例では、すべてのポートおよびクラスターの名前を持つハッシュマップを取得します。

    - name:"Display all server ports and names from cluster1"
      debug:
        var: item
      loop: "{{ domain_definition | json_query(server_name_cluster1_query) }}"
      vars:
        server_name_cluster1_query: "domain.server[?cluster=='cluster2'].{name: name, port: port}"

.. _ipaddr_filter:

IP アドレスフィルター
`````````````````

.. versionadded:: 1.9

文字列が有効な IP アドレスかどうかをテストするには、以下を実行します。

  {{ myvar | ipaddr }}

さらに、特定の IP プロトコルバージョンが必要です。

  {{ myvar | ipv4 }}
  {{ myvar | ipv6 }}

IP アドレスフィルターを使用して、
IP アドレスから特定の情報を抽出することもできます。たとえば、CIDR から IP アドレス自体を取得するには、以下を使用します::

  {{ '192.0.2.1/24' | ipaddr('address') }}

``ipaddr`` フィルターおよび完全な使用方法は、
「:ref:`playbooks_filters_ipaddr`」を参照してください。

.. _network_filters:

ネットワーク CLI フィルター
```````````````````

.. versionadded:: 2.4

ネットワークデバイスの CLI コマンドの出力を構造化された JSON 出力に変換するには、
``parse_cli`` フィルターを使用します::

    {{ output | parse_cli('path/to/spec') }}


``parse_cli`` フィルターは仕様ファイルを読み込み、
それを介してコマンド出力を渡し、JSON 出力を返します。YAML 仕様ファイルは、CLI 出力の解析方法を定義します。

仕様ファイルは有効なフォーマットの YAML である必要があります。 CLI の出力を解析する方法を定義し、
JSON データを返します。 以下は、
``show vlan`` コマンドからの出力を解析する有効な仕様ファイルの例です。

.. code-block:: yaml

   ---
   vars:
     vlan:
       vlan_id: "{{ item.vlan_id }}"
       name: "{{ item.name }}"
       enabled: "{{ item.state != 'act/lshut' }}"
       state: "{{ item.state }}"

   keys:
     vlans:
       value: "{{ vlan }}"
       items: "^(?P<vlan_id>\\d+)\\s+(?P<name>\\w+)\\s+(?P<state>active|act/lshut|suspended)"
     state_static:
       value: present


上記の仕様ファイルは、
解析された VLAN 情報を含むハッシュのリストである JSON データ構造を返します。

キーと値のディレクティブを使用して、
同じコマンドをハッシュに解析できます。 次に、
同じ ``show vlan`` コマンドを使用して出力を解析してハッシュ値にする方法の例を示します。

.. code-block:: yaml

   ---
   vars:
     vlan:
       key: "{{ item.vlan_id }}"
       values:
         vlan_id: "{{ item.vlan_id }}"
         name: "{{ item.name }}"
         enabled: "{{ item.state != 'act/lshut' }}"
         state: "{{ item.state }}"

   keys:
     vlans:
       value: "{{ vlan }}"
       items: "^(?P<vlan_id>\\d+)\\s+(?P<name>\\w+)\\s+(?P<state>active|act/lshut|suspended)"
     state_static:
       value: present


CLI コマンドを解析する別の一般的な使用例は、
大きなコマンドを解析可能なブロックに分割することです。 これは、``start_block`` ディレクティブおよび 
``end_block`` ディレクティブを使用して、コマンドを解析可能なブロックに分割することで実行できます。

.. code-block:: yaml

   ---
   vars:
     interface:
       name: "{{ item[0].match[0] }}"
       state: "{{ item[1].state }}"
       mode: "{{ item[2].match[0] }}"

   keys:
     interfaces:
       value: "{{ interface }}"
       start_block: "^Ethernet.*$"
       end_block: "^$"
       items:
         - "^(?P<name>Ethernet\\d\\/\\d*)"
         - "admin state is (?P<state>.+),"
         - "Port mode is (.+)"


上記の例では、``show interface`` の出力を
解析してハッシュのリストを作成します。

ネットワークフィルターは、
TextFSM ライブラリーを使用した CLI コマンドの出力の解析にも対応しています。 TextFSM で CLI 出力を解析するには、
以下のフィルターを使用します::

  {{ output.stdout[0] | parse_cli_textfsm('path/to/fsm') }}

TextFSM フィルターを使用するには、TextFSM ライブラリーをインストールする必要があります。

ネットワーク XML フィルター
```````````````````

.. versionadded:: 2.5

ネットワークデバイスコマンドの XML 出力を
構造化 JSON 出力に変換するには、``parse_xml`` フィルターを使用します::

  {{ output | parse_xml('path/to/spec') }}

``parse_xml`` フィルターは仕様ファイルを読み込み、
JSON 形式のコマンド出力を渡します。

仕様ファイルは有効なフォーマットの YAML である必要があります。XML 出力を解析して、
JSON データを返す方法を定義します。

以下は、
``show vlan | display xml`` コマンドの出力を解析します。

.. code-block:: yaml

   ---
   vars:
     vlan:
       vlan_id: "{{ item.vlan_id }}"
       name: "{{ item.name }}"
       desc: "{{ item.desc }}"
       enabled: "{{ item.state.get('inactive') != 'inactive' }}"
       state: "{% if item.state.get('inactive') == 'inactive'%} inactive {% else %} active {% endif %}"

   keys:
     vlans:
       value: "{{ vlan }}"
       top: configuration/vlans/vlan
       items:
         vlan_id: vlan-id
         name: name
         desc: description
         state: ".[@inactive='inactive']"


上記の仕様ファイルは、
解析された VLAN 情報を含むハッシュのリストである JSON データ構造を返します。

キーと値のディレクティブを使用して、
同じコマンドをハッシュに解析できます。 同じ ``show vlan | display xml`` コマンドを使用して、
出力をハッシュ値に解析する方法の例を次に示します。

.. code-block:: yaml

   ---
   vars:
     vlan:
       key: "{{ item.vlan_id }}"
       values:
           vlan_id: "{{ item.vlan_id }}"
           name: "{{ item.name }}"
           desc: "{{ item.desc }}"
           enabled: "{{ item.state.get('inactive') != 'inactive' }}"
           state: "{% if item.state.get('inactive') == 'inactive'%} inactive {% else %} active {% endif %}"

   keys:
     vlans:
       value: "{{ vlan }}"
       top: configuration/vlans/vlan
       items:
         vlan_id: vlan-id
         name: name
         desc: description
         state: ".[@inactive='inactive']"


``top`` の値は XML root ノードに対して相対的な値です。
以下の XML 出力例では、``top`` の値は ``configuration/vlans/vlan`` です。
これは root ノード (<rpc-reply>) に関連する XPath 式です。
``top`` 値の ``設定`` は、
最も遠くにあるコンテナノードであり、``vlan`` は最も近くにあるコンテナノードです。

``items`` は、
ユーザー定義の名前から、要素を選択する XPath 式にマップするキーと値のペアのディクショナリーです。Xpath 式は、``top`` に含まれる XPath 値の値を基準にしています。
たとえば、仕様ファイルの ``vlan_id`` はユーザー定義の名前で、その値 ``vlan-id`` は、
``top`` の XPath の値を基準にしています。

XML タグの属性は、XPath 式を使用して抽出できます。仕様の ``state`` の値は、
出力 XML の ``vlan`` タグの属性を取得するために使用される XPath 式です::

    <rpc-reply>
      <configuration>
        <vlans>
          <vlan inactive="inactive">
           <name>vlan-1</name>
           <vlan-id>200</vlan-id>
           <description>This is vlan-1</description>
          </vlan>
        </vlans>
      </configuration>
    </rpc-reply>

.. note:: サポートされる XPath 式の詳細は、`<https://docs.python.org/2/library/xml.etree.elementtree.html#xpath-support>`_ を参照してください。

ネットワーク VLAN フィルター
````````````````````

.. versionadded:: 2.8

``vlan_parser`` フィルターを使用して、
IOS のような VLAN リストルールに従って、ソートされていない VLAN 整数のリストを、整数のソートされた文字列リストに操作します。このリストには以下のプロパティーがあります。

* VLAN は昇順でリストされます。
* 3 つ以上の連続した VLAN はダッシュ付きでリストされます。
* リストの最初の行は、first_line_len 文字の長さになります。
* 後続のリスト行は、other_line_len 文字になります。

VLAN リストをソートするには、以下を実行します。

    {{ [3003, 3004, 3005, 100, 1688, 3002, 3999] | vlan_parser }}

この例では、以下のソートリストを示しています。

    ['100,1688,3002-3005,3999']


Jinja テンプレートの他の例:

    {% set parsed_vlans = vlans | vlan_parser %}
    switchport trunk allowed vlan {{ parsed_vlans[0] }}
    {% for i in range (1, parsed_vlans | count) %}
    switchport trunk allowed vlan add {{ parsed_vlans[i] }}

これにより、Cisco IOS タグ付けインターフェースで VLAN のリストを動的に生成できます。インターフェースに必要となる正確な VLAN リストを保存し、そのリストを設定用に実際に生成される解析された IOS 出力と比較できます。


.. _hash_filters:

ハッシュフィルター
```````````````

.. versionadded:: 1.9

文字列の sha1 ハッシュを取得するには、次のようになります。

    {{ 'test1' | hash('sha1') }}

文字列の md5 ハッシュを取得するには、次のようになります。

    {{ 'test1' | hash('md5') }}

文字列のチェックサムを取得します。

    {{ 'test2' | checksum }}

その他のハッシュ (プラットフォームに依存)::

    {{ 'test2' | hash('blowfish') }}

sha512 パスワードハッシュ (任意の salt) を取得するには、次のようになります。

    {{ 'passwordsaresecret' | password_hash('sha512') }}

特定の salt を持つ sha256 パスワードハッシュを取得するには、次のようになります。

    {{ 'secretpassword' | password_hash('sha256', 'mysecretsalt') }}

システムごとに一意のハッシュを生成する冪等な方法は、実行間で一貫性のある salt を使用することです。

    {{ 'secretpassword' | password_hash('sha512', 65534 | random(seed=inventory_hostname) | string) }}

使用可能なハッシュタイプは、ansible を実行しているマスターシステムに依存し、
「ハッシュ」は hashlib に依存し、password_hash は passlib に依存します (https://passlib.readthedocs.io/en/stable/lib/passlib.hash.html)。

.. versionadded:: 2.7

ハッシュタイプによっては、rounds パラメーターを指定できるものもあります。

    {{ 'secretpassword' | password_hash('sha256', 'mysecretsalt', rounds=10000) }}

.. _combine_filter:

ハッシュ/ディクショナリーの統合
`````````````````````````````

.. versionadded:: 2.0

`combine` フィルターにより、ハッシュをマージできます。たとえば、
次は 1 つのハッシュ内のキーをオーバーライドします。

    {{ {'a':1, 'b':2} | combine({'b':3}) }}

生成されるハッシュは、以下のようになります::

    {'a':1, 'b':3}

フィルターは、オプションの `recursive=True` パラメーターも受け入れ、
最初のハッシュのキーをオーバーライドするだけでなく、
ネストされたハッシュに再帰し、それらのキーもマージします。

.. code-block:: jinja

    {{ {'a':{'foo':1, 'bar':2}, 'b':2} | combine({'a':{'bar':3, 'baz':4}}, recursive=True) }}

これにより、以下のようになります::

    {'a':{'foo':1, 'bar':3, 'baz':4}, 'b':2}

フィルターは複数の引数を使用してマージすることもできます::

    {{ a | combine(b, c, d) }}

この場合、`d` のキーは `c` のキーをオーバーライドし、
`b` のキーをオーバーライドします。

この動作は、
`ansible.cfg` の `hash_behaviour` 設定の値に依存しません。

.. _extract_filter:

コンテナーからの値の抽出
`````````````````````````````````

.. versionadded:: 2.1

`extract` フィルターは、インデックスリストから、
コンテナーの値リスト (ハッシュまたはアレイ) へマップするために使用されます。

    {{ [0,2] | map('extract', ['x','y','z']) | list }}
    {{ ['x','y'] | map('extract', {'x':42, 'y':31}) | list }}

上記の式の結果は、以下のようになります::

    ['x', 'z']
    [42, 31]

フィルターは別の引数を取ることができます::

    {{ groups['x'] | map('extract', hostvars, 'ec2_ip_address') | list }}

これは、グループ「x」のホストのリストを取得し、`hostvars` でそれを検索してから、
結果の `ec2_ip_address` を検索します。最終結果は、
グループの「x」にあるホストの IP アドレスリストです。

フィルター内の 3 番目の引数は、
コンテナー内の再帰的な検索のためのリストでもあります。

    {{ ['a'] | map('extract', b, ['x','y']) | list }}

これにより、`b['a']['x']['y']` の値が含まれるリストが返されます。

.. _comment_filter:

コメントフィルター
``````````````

.. versionadded:: 2.0

`comment` フィルターにより、
選択したコメントのスタイルでテキストを飾ることができます。たとえば、次のものが、

    {{ "Plain style (default)" | comment }}

次の出力を生成します。

.. code-block:: text

    #
    # Plain style (default)
    #

同様の方法で、C (``//...``)、
C ブロック (``/*...*/``)、Erlang (``%...``) および XML (``<!--...-->``) にスタイルを適用できます。

    {{ "C style" | comment('c') }}
    {{ "C block style" | comment('cblock') }}
    {{ "Erlang style" | comment('erlang') }}
    {{ "XML style" | comment('xml') }}
    
上記のいずれにも含まれていない特定のコメント文字が必要な場合は、
次のようにカスタマイズできます::

  {{ "My Special Case" | comment(decoration="! ") }}

次を生成します。

.. code-block:: text

  !
  !My Special Case
  !

コメントスタイルを完全にカスタマイズすることもできます::

    {{ "Custom style" | comment('plain', prefix='#######\n#', postfix='#\n#######\n   ###\n    #') }}

これにより、以下の出力が作成されます。

.. code-block:: text

    #######
    #
    # Custom style
    #
    #######
       ###
        #

フィルターは、任意の Ansible 変数に適用することもできます。たとえば、
``ansible_managed`` 変数の出力をより読みやすいものにするには、
``ansible.cfg`` ファイルの定義を以下のように変更します。

.. code-block:: jinja

    [defaults]

    ansible_managed = This file is managed by Ansible.%n
      template: {file}
      date: %Y-%m-%d %H:%M:%S
      user: {uid}
      host: {host}

次に、`comment` フィルターで変数を使用します。

    {{ ansible_managed | comment }}

これは、次の出力を生成します。

.. code-block:: sh

    #
    # This file is managed by Ansible.
    #
    # template: /home/ansible/env/dev/ansible_managed/roles/role1/templates/test.j2
    # date: 2015-09-10 11:02:58
    # user: ansible
    # host: myhost
    #


.. _other_useful_filters:

URL Split フィルター
`````````````````

.. versionadded:: 2.4

``urlsplit`` フィルターは、フラグメント、ホスト名、netloc、パスワード、パス、ポート、クエリー、スキーム、およびユーザー名を URL から抽出します。引数なしでは、すべてのフィールドのディクショナリーを返します::

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('hostname') }}
    # => 'www.acme.com'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('netloc') }}
    # => 'user:password@www.acme.com:9000'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('username') }}
    # => 'user'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('password') }}
    # => 'password'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('path') }}
    # => '/dir/index.html'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('port') }}
    # => '9000'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('scheme') }}
    # => 'http'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('query') }}
    # => 'query=term'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit('fragment') }}
    # => 'fragment'

    {{ "http://user:password@www.acme.com:9000/dir/index.html?query=term#fragment" | urlsplit }}
    # =>
    #   {
    #       "fragment": "fragment",
    #       "hostname": "www.acme.com",
    #       "netloc": "user:password@www.acme.com:9000",
    #       "password": "password",
    #       "path": "/dir/index.html",
    #       "port": 9000,
    #       "query": "query=term",
    #       "scheme": "http",
    #       "username": "user"
    #   }


正規表現フィルター
``````````````````````````

正規表現で文字列を検索するには、「regex_search」フィルターを使用します::

    # search for "foo" in "foobar"
    {{ 'foobar' | regex_search('(foo)') }}

    # will return empty if it cannot find a match
    {{ 'ansible' | regex_search('(foobar)') }}

    # case insensitive search in multiline mode
    {{ 'foo\nBAR' | regex_search("^bar", multiline=True, ignorecase=True) }}


正規表現のすべてのマッチを検索するには、「regex_findall」フィルターを使用します。

    # Return a list of all IPv4 addresses in the string
    {{ 'Some DNS servers are 8.8.8.8 and 8.8.4.4' | regex_findall('\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b') }}
    

文字列のテキストを正規表現に置き換えるには、「regex_replace」フィルターを使用します。

    # convert "ansible" to "able"
    {{ 'ansible' | regex_replace('^a.*i(.*)$', 'a\\1') }}

    # convert "foobar" to "bar"
    {{ 'foobar' | regex_replace('^f.*o(.*)$', '\\1') }}

    # convert "localhost:80" to "localhost, 80" using named groups
    {{ 'localhost:80' | regex_replace('^(?P<host>.+):(?P<port>\\d+)$', '\\g<host>, \\g<port>') }}

    # convert "localhost:80" to "localhost"
    {{ 'localhost:80' | regex_replace(':80') }}

.. note:: 文字列全体と一致させるために ``*`` を使用している場合は、必ず正規表現を開始/終了アンカーでラップアラウンドしてください。
   たとえば、``^(.*)$`` で一致する結果は常に 1 つだけで、一部の Python バージョンでは、``(.*)`` は文字列全体と最後の空の文字列に一致します。
   つまり、2つの置換が行われます。

    # add "https://" prefix to each item in a list
    GOOD:
    {{ hosts | map('regex_replace', '^(.*)$', 'https://\\1') | list }}
    {{ hosts | map('regex_replace', '(.+)', 'https://\\1') | list }}
    {{ hosts | map('regex_replace', '^', 'https://') | list }}

    BAD:
    {{ hosts | map('regex_replace', '(.*)', 'https://\\1') | list }}

    # append ':80' to each item in a list
    GOOD:
    {{ hosts | map('regex_replace', '^(.*)$', '\\1:80') | list }}
    {{ hosts | map('regex_replace', '(.+)', '\\1:80') | list }}
    {{ hosts | map('regex_replace', '$', ':80') | list }}

    BAD:
    {{ hosts | map('regex_replace', '(.*)', '\\1:80') | list }}

.. note:: Ansible 2.0 よりも前のバージョンでは、(「key=value」の引数を簡単にするのではなく)「regex_replace」フィルターが YAML 引数内の変数で使用された場合は、
   次に、2 つの (````) ではなく、4 つのバックスラッシュ (``\``) で逆参照 (``\1`` など) をエスケープする必要があります。

.. versionadded:: 2.0

標準の Python 正規表現内で特殊文字をエスケープするには、「regex_escape」フィルターを使用します (デフォルトの re_type='python' オプションを使用)。

    # convert '^f.*o(.*)$' to '\^f\.\*o\(\.\*\)\$'
    {{ '^f.*o(.*)$' | regex_escape() }}

.. versionadded:: 2.8

POSIX 基本正規表現内で特殊文字をエスケープするには、re_type='posix_basic' オプションで「regex_escape」フィルターを使用します。

    # convert '^f.*o(.*)$' to '\^f\.\*o(\.\*)\$'
    {{ '^f.*o(.*)$' | regex_escape('posix_basic') }}


Kubernetes フィルター
``````````````````

「k8s_config_resource_name」フィルターを使用して、
Kubernetes ConfigMap または Secret の名前を取得します。

    {{ configmap_resource_definition | k8s_config_resource_name }}

これは、Pod 仕様のハッシュを参照するために使用できます。

    my_secret:
      kind: Secret
      name: my_secret_name

    deployment_resource:
      kind: Deployment
      spec:
        template:
          spec:
            containers:
            - envFrom:
                - secretRef:
                    name: {{ my_secret | k8s_config_resource_name }}

.. versionadded:: 2.8

他の有用なフィルター
````````````````````

シェルの使用に引用符を追加するには、以下を行います。

    - shell: echo {{ string_value | quote }}

true で 1 つの値を使用し、false で別の値を使用するには、以下を指定します (バージョン1.9の新機能)::

    {{ (name == "John") | ternary('Mr','Ms') }}

true で 1 つの値、false で 1 つの値、null で 3 番目の値を使用するには、以下を指定します (バージョン 2.8 の新機能)::

   {{ enabled | ternary('no shutdown', 'shutdown', omit) }}

リストを文字列に連結するには、以下を指定します::

    {{ list | join(" ") }}

「/etc/asdf/foo.txt」から「foo.txt」のように、ファイルパスの最後の名前を取得するには、以下を指定します::

    {{ path | basename }}

ウィンドウスタイルのファイルパスの最後の名前を取得するには、以下を指定します (バージョン 2.0 の新機能)::

    {{ path | win_basename }}

Windows ドライブの文字を残りのファイルパスから分離するには、以下を指定します (バージョン 2.0 の新機能)。

    {{ path | win_splitdrive }}

Windows ドライブの文字のみを取得するには、以下を指定します::

    {{ path | win_splitdrive | first }}

ドライブ文字なしで残りのパスを取得するには、以下を指定します::

    {{ path | win_splitdrive | last }}

ディレクトリーをパスから取得するには、以下を指定します::

    {{ path | dirname }}

Windows パスからディレクトリーを取得するには、以下を指定します (バージョン 2.0 の新機能)::

    {{ path | win_dirname }}

チルド (`~`) 文字を含むパスを拡張するには、以下を指定します (バージョン 1.5 の新機能)::

    {{ path | expanduser }}

環境変数を含むパスを拡張するには、以下を指定します::

    {{ path | expandvars }}

.. note:: `expandvars` は、ローカル変数を拡張します。リモートパスで使用するとエラーが発生する可能性があります。

.. versionadded:: 2.6

リンクの実際のパスを取得するには、以下を指定します (バージョン 1.8 の新機能)::

    {{ path | realpath }}

リンクの相対パスを取得するには、開始点から以下を行います (バージョン 1.7 の新機能)::

    {{ path | relpath('/etc') }}

パスまたはファイル名のルートおよび拡張を取得するには、以下を指定します (バージョン 2.0 の新機能)::

    # with path == 'nginx.conf' the return would be ('nginx', '.conf')
    {{ path | splitext }}

Base64 でエンコードされた文字列を使用するには、以下を指定します::

    {{ encoded | b64decode }}
    {{ decoded | string | b64encode }}
    
バージョン 2.6 では、使用するエンコーディングのタイプを定義できます。デフォルトは ``utf-8`` です::

    {{ encoded | b64decode(encoding='utf-16-le') }}
    {{ decoded | string | b64encode(encoding='utf-16-le') }}
    
.. note:: ``文字列`` フィルターは Python 2 にのみ必要で、エンコードするテキストがユニコード文字列であることを確認します。
    b64encode より前のフィルターを使用しないと、間違った値がエンコードされます。

.. versionadded:: 2.6

文字列から UUID を作成するには、以下を指定します (バージョン 1.9 の新機能)::

    {{ hostname | to_uuid }}

vars_prompt から文字列を「True」として入力し、
システムがそれがブール値であることを認識していない場合など、特定の型として値をキャストするには、以下を指定します。

   - debug:
       msg: test
     when: some_string_value | bool

.. versionadded:: 1.6

複雑な変数のリストで、各項目から 1 つの属性を使用するには、「map」フィルターを使用します (詳細は `Jinja2 map() docs`_ を参照してください)。

    # get a comma-separated list of the mount points (e.g. "/,/mnt/stuff") on a host
    {{ ansible_mounts | map(attribute='mount') | join(',') }}

文字列から日付オブジェクトを取得するには、`to_datetime` フィルターを使用します (2.2 の新しいバージョン)。

    # Get total amount of seconds between two dates. Default date format is %Y-%m-%d %H:%M:%S but you can pass your own format
    {{ (("2016-08-14 20:00:12" | to_datetime) - ("2015-12-25" | to_datetime('%Y-%m-%d'))).total_seconds()  }}

# Get remaining seconds after delta has been calculated. NOTE: This does NOT convert years, days, hours, etc to seconds. For that, use total_seconds()
    {{ (("2016-08-14 20:00:12" | to_datetime) - ("2016-08-14 18:00:00" | to_datetime)).seconds  }}
    # This expression evaluates to "12" and not "132". Delta is 2 hours, 12 seconds

    # get amount of days between two dates. This returns only number of days and discards remaining hours, minutes, and seconds
    {{ (("2016-08-14 20:00:12" | to_datetime) - ("2015-12-25" | to_datetime('%Y-%m-%d'))).days  }}

.. versionadded:: 2.4

文字列 (shell date コマンドの場合のように) を使用して日付をフォーマットするには、「strftime」フィルターを使用します::

    # Display year-month-day
    {{ '%Y-%m-%d' | strftime }}

    # Display hour:min:sec
    {{ '%H:%M:%S' | strftime }}

    # Use ansible_date_time.epoch fact
    {{ '%Y-%m-%d %H:%M:%S' | strftime(ansible_date_time.epoch) }}

    # Use arbitrary epoch value
    {{ '%Y-%m-%d' | strftime(0) }}          # => 1970-01-01
    {{ '%Y-%m-%d' | strftime(1441357287) }} # => 2015-09-04

.. note:: 文字列のすべての可能性を取得するには、https://docs.python.org/2/library/time.html#time.strftime を確認します。

組み合わせフィルター
````````````````````

.. versionadded:: 2.3

このフィルターセットは、組み合わせたリストを返します。
リストの順列を取得するには、以下を実行します。

    - name: give me largest permutations (order matters)
      debug:
        msg: "{{ [1,2,3,4,5] | permutations | list }}"

    - name: give me permutations of sets of three
      debug:
        msg: "{{ [1,2,3,4,5] | permutations(3) | list }}"

Combinations always require a set size::

    - name: give me combinations for sets of two
      debug:
        msg: "{{ [1,2,3,4,5] | combinations(2) | list }}"


:ref:`zip_filter` も参照してください。

製品フィルター
```````````````

製品フィルターは、入力反復可能な `デカルト製品 <https://docs.python.org/3/library/itertools.html#itertools.product>`_ を返します。

これはジェネレーター式のネストされた for-loops とほぼ同等です。

例::

  - name: generate multiple hostnames
    debug:
      msg: "{{ ['foo', 'bar'] | product(['com']) | map('join', '.') | join(',') }}"

これにより、以下のようになります::

    { "msg": "foo.com,bar.com" }


デバッグフィルター
`````````````````

.. versionadded:: 2.3

``type_debug`` フィルターを使用して、変数の基礎となる Python タイプを表示します。
これは、
変数の正確なタイプを知る必要がある状況でのデバッグに役立ちます。

    {{ myvar | type_debug }}


コンピューター理論のアサーション
```````````````````````````

``human_readable`` 関数および ``human_to_bytes`` 関数を使用すると、
Playbook をテストして、タスクで適切なサイズ形式を使用していることを確認できます。
コンピューターにバイト形式を提供し、人が読める形式を提供していることを確認してください。

人間が読み取り可能
``````````````

指定の文字列が人が判読できるかどうかをアサートします。

例::

  - name: "Human Readable"
    assert:
      that:
        - '"1.00 Bytes" == 1|human_readable'
        - '"1.00 bits" == 1|human_readable(isbits=True)'
        - '"10.00 KB" == 10240|human_readable'
        - '"97.66 MB" == 102400000|human_readable'
        - '"0.10 GB" == 102400000|human_readable(unit="G")'
        - '"0.10 Gb" == 102400000|human_readable(isbits=True, unit="G")'

これにより、以下のようになります::

    { "changed": false, "msg":"All assertions passed" }

人間からバイト
``````````````

指定した文字列をバイト形式で返します。

例::

  - name: "Human to Bytes"
    assert:
      that:
        - "{{'0'|human_to_bytes}}        == 0"
        - "{{'0.1'|human_to_bytes}}      == 0"
        - "{{'0.9'|human_to_bytes}}      == 1"
        - "{{'1'|human_to_bytes}}        == 1"
        - "{{'10.00 KB'|human_to_bytes}} == 10240"
        - "{{   '11 MB'|human_to_bytes}} == 11534336"
        - "{{  '1.1 GB'|human_to_bytes}} == 1181116006"
        - "{{'10.00 Kb'|human_to_bytes(isbits=True)}} == 10240"

これにより、以下のようになります::

    { "changed": false, "msg":"All assertions passed" }


通常、便利なフィルターは、新しい Ansible リリースごとに追加されます。 開発ドキュメントには、
独自のプラグインを作成して Ansibleフィルターを拡張する方法が示されていますが、
一般的には、新しいフィルターをコアに追加して、誰でも使用できるようにすることが推奨されます。

.. _Jinja2 map() docs: http://jinja.pocoo.org/docs/dev/templates/#map

.. _builtin filters: http://jinja.pocoo.org/docs/templates/#builtin-filters

.. _PyYAML library: https://pyyaml.org/

.. _PyYAML documentation: https://pyyaml.org/wiki/PyYAMLDocumentation


.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_variables`
       変数の詳細
   :ref:`playbooks_loops`
       Playbook でのループ
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   :ref:`playbooks_best_practices`
       Playbook のベストプラクティス
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
