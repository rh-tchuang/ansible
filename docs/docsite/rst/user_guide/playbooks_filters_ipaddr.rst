:orphan:

.. _playbooks_filters_ipaddr:

ipaddr フィルター
`````````````

バージョン 1.9 における新機能

``ipaddr()`` は、Ansible 内から Python パッケージ `netaddr`_ へ、
インターフェースを提供するように設計された Jinja2 フィルターです。文字列やアイテムのリストを操作したり、
さまざまなデータをテストして有効な IP アドレスかどうかを確認したり、入力データを操作して要求された情報を抽出したりできます。
``ipaddr()`` は、
さまざまな形式の IPv4 アドレスと IPv6 アドレスの両方で機能します。IP サブネットと MAC アドレスを操作するために
使用できる追加機能もあります。

このフィルターを Ansible で使用するには、Ansible を使用するコンピューターに Python ライブラリー `netaddr`_ 
をインストールする必要があります (リモートホストでは必要ありません)。
これは通常、
システムパッケージマネージャーまたは ``pip`` を使用してインストールできます::

    pip install netaddr

.. _netaddr: https://pypi.org/project/netaddr/

.. contents:: トピック
   :local:
   :depth: 2
   :backlinks: top

基本的なテスト
^^^^^^^^^^^

``ipaddr()`` は、クエリーが True の場合は入力値を返し、
False の場合は ``False`` を返すように設計されています。このように、
連鎖フィルターで簡単に使用できます。フィルターを使用する場合は、文字列をフィルターに渡します。

.. code-block:: none

    {{ '192.0.2.0' | ipaddr }}

変数として値を渡すこともできます。

    {{ myvar | ipaddr }}

以下は、さまざまな入力文字列のテスト結果の例です。

    # These values are valid IP addresses or network ranges
    '192.168.0.1'       -> 192.168.0.1
    '192.168.32.0/24'   -> 192.168.32.0/24
    'fe80::100/10'      -> fe80::100/10
    45443646733         -> ::a:94a7:50d
    '523454/24'         -> 0.7.252.190/24

    # Values that are not valid IP addresses or network ranges
    'localhost'         -> False
    True                -> False
    'space bar'         -> False
    False               -> False
    ''                  -> False
    ':'                 -> False
    'fe80:/10'          -> False

IPv4 アドレスまたは IPv6 アドレスのいずれかが必要になる場合があります。特定のタイプのみを絞り込むには、
``ipaddr()`` フィルターには、``ipv4()`` と ``ipv6()`` の 2 つの「エイリアス」があります。

IPv4 フィルターの使用例:

    {{ myvar | ipv4 }}

同様の、IPv6 フィルターの使用例::

    {{ myvar | ipv6 }}

以下は、IPv4 アドレスを検索するテスト結果の例です。

    '192.168.0.1'       -> 192.168.0.1
    '192.168.32.0/24'   -> 192.168.32.0/24
    'fe80::100/10'      -> False
    45443646733         -> False
    '523454/24'         -> 0.7.252.190/24

IPv6 アドレスにフィルターが設定されたデータ::

    '192.168.0.1'       -> False
    '192.168.32.0/24'   -> False
    'fe80::100/10'      -> fe80::100/10
    45443646733         -> ::a:94a7:50d
    '523454/24'         -> False


リストへのフィルター設定
^^^^^^^^^^^^^^^

リスト全体に絞り込むことができます。``ipaddr()`` は、
特定のクエリーに有効な値を含むリストを返します::

    # Example list of values
    test_list = ['192.24.2.1', 'host.fqdn', '::1', '192.168.32.0/24', 'fe80::100/10', True, '', '42540766412265424405338506004571095040/64']

    # {{ test_list | ipaddr }}
    ['192.24.2.1', '::1', '192.168.32.0/24', 'fe80::100/10', '2001:db8:32c:faad::/64']

    # {{ test_list | ipv4 }}
    ['192.24.2.1', '192.168.32.0/24']

    # {{ test_list | ipv6 }}
    ['::1', 'fe80::100/10', '2001:db8:32c:faad::/64']
    

[ ] 括弧で IPv6 アドレスのラッピング
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

一部の設定ファイルでは、
IPv6 アドレスを角括弧 (``[ ]``) で「ラップする」必要があります。これを実行するには、``ipwrap()`` フィルターを使用できます。すべての IPv6 アドレスをラップし、
その他の文字列をそのまま残します。

    # {{ test_list | ipwrap }}
    ['192.24.2.1', 'host.fqdn', '[::1]', '192.168.32.0/24', '[fe80::100]/10', True, '', '[2001:db8:32c:faad::]/64']
    
上記のとおり、``ipwrap()`` は非 IP アドレス値をフィルタリングしませんでした。
これは、たとえば、
通常、IP アドレスとホスト名を混在させる場合に必要な値です。それでもすべての非 IP アドレス値をフィルターで除外する場合は、
両方のフィルターを連結できます。

    # {{ test_list | ipaddr | ipwrap }}
    ['192.24.2.1', '[::1]', '192.168.32.0/24', '[fe80::100]/10', '[2001:db8:32c:faad::]/64']
    

基本クエリー
^^^^^^^^^^^^^

各 ``ipaddr()`` フィルターに引数を 1 つ指定できます。その後、フィルターはそれをクエリーとして扱い、
そのクエリーによって変更された値を返します。リストには、
クエリーする値のみが含まれます。

クエリーの種類は次のとおりです。

- 名前によるクエリー: ``ipaddr('address')``、``ipv4('network')``
- CIDR 範囲によるクエリー: ``ipaddr('192.168.0.0/24')``、``ipv6('2001:db8::/32')``
- インデックス番号によるクエリー: ``ipaddr('1')``、``ipaddr('-1')``

クエリータイプが認識されないと、Ansible はエラーを発生させます。


ホストおよびネットワークに関する情報の取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ここでは、テストリストを再度使用します。

    # Example list of values
    test_list = ['192.24.2.1', 'host.fqdn', '::1', '192.168.32.0/24', 'fe80::100/10', True, '', '42540766412265424405338506004571095040/64']
    
上記のリストを使用して、
ネットワーク範囲ではなくホストの IP アドレスである要素のみを取得してみましょう。

    # {{ test_list | ipaddr('address') }}
    ['192.24.2.1', '::1', 'fe80::100']
    
上記のとおり、CIDR プレフィックスを持つホストアドレスがある場合でも、
フィルターによって破棄されました。(IPv6 アドレスでよくあるように) 
正しい CIDR プレフィックスが付いたホスト IP アドレスが必要な場合は、
``ipaddr('host')`` フィルターを使用できます。

    # {{ test_list | ipaddr('host') }}
    ['192.24.2.1/32', '::1/128', 'fe80::100/10']
    
IP アドレスタイプによるフィルタリングも機能します。

    # {{ test_list | ipv4('address') }}
    ['192.24.2.1']

    # {{ test_list | ipv6('address') }}
    ['::1', 'fe80::100']
    
IP アドレスまたはネットワーク範囲にパブリックインターネットでアクセスできるかどうか、
またはプライベートネットワークにあるかどうかを確認できます。

    # {{ test_list | ipaddr('public') }}
    ['192.24.2.1', '2001:db8:32c:faad::/64']

    # {{ test_list | ipaddr('private') }}
    ['192.168.32.0/24', 'fe80::100/10']
    
特定のネットワーク範囲の値を確認できます。

    # {{ test_list | ipaddr('net') }}
    ['192.168.32.0/24', '2001:db8:32c:faad::/64']
    
特定の範囲内にある IP アドレスの数を確認することもできます。

    # {{ test_list | ipaddr('net') | ipaddr('size') }}
    [256, 18446744073709551616L]
    
ネットワーク範囲をクエリーとして指定すると、
指定の値がその範囲に含まれるかどうかを確認できます。

    # {{ test_list | ipaddr('192.0.0.0/8') }}
    ['192.24.2.1', '192.168.32.0/24']
    
正または負の整数をクエリーとして指定すると、``ipaddr()`` はこれをインデックスとして扱い、
ネットワーク範囲から特定のIPアドレスを
「host/prefix」形式で返します。

    # First IP address (network address)
    # {{ test_list | ipaddr('net') | ipaddr('0') }}
    ['192.168.32.0/24', '2001:db8:32c:faad::/64']

    # Second IP address (usually the gateway host)
    # {{ test_list | ipaddr('net') | ipaddr('1') }}
    ['192.168.32.1/24', '2001:db8:32c:faad::1/64']

    # Last IP address (the broadcast address in IPv4 networks)
    # {{ test_list | ipaddr('net') | ipaddr('-1') }}
    ['192.168.32.255/24', '2001:db8:32c:faad:ffff:ffff:ffff:ffff/64']
    
インデックスの範囲、
その開始または終了までの間にある IP アドレスを選択することもできます::

    # Returns from the start of the range
    # {{ test_list | ipaddr('net') | ipaddr('200') }}
    ['192.168.32.200/24', '2001:db8:32c:faad::c8/64']

    # Returns from the end of the range
    # {{ test_list | ipaddr('net') | ipaddr('-200') }}
    ['192.168.32.56/24', '2001:db8:32c:faad:ffff:ffff:ffff:ff38/64']

    # {{ test_list | ipaddr('net') | ipaddr('400') }}
    ['2001:db8:32c:faad::190/64']
    

ホスト/プレフィックスの値からの情報の取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IP アドレスとサブネットプレフィックス ("CIDR") の組み合わせを頻繁に使用しますが、
これは IPv6 ではさらに一般的です。``ipaddr()`` フィルターは、
これらの接頭辞から有用なデータを抽出できます。

以下は、ホストプレフィックス (「制御」の値を含む) の例です。

    host_prefix = ['2001:db8:deaf:be11::ef3/64', '192.0.2.48/24', '127.0.0.1', '192.168.0.0/16']

まず、サブネットや単一の IP アドレスだけでなく、
正しいホスト/プレフィックスの値のみを使用するようにします。

    # {{ host_prefix | ipaddr('host/prefix') }}
['2001:db8:deaf:be11::ef3/64', '192.0.2.48/24']
    
Debian ベースのシステムでは、``/etc/network/interfaces`` ファイルに保存されているネットワーク設定は、IP アドレス、ネットワークアドレス、ネットマスク、およびブロードキャストアドレスの組み合わせを使用して IPv4 ネットワークインターフェースを設定します。これらの値は、単一の「host/prefix」の組み合わせから取得できます。

.. code-block:: jinja

    # Jinja2 template
    {% set ipv4_host = host_prefix | unique | ipv4('host/prefix') | first %}
    iface eth0 inet static
        address   {{ ipv4_host | ipaddr('address') }}
        network   {{ ipv4_host | ipaddr('network') }}
        netmask   {{ ipv4_host | ipaddr('netmask') }}
        broadcast {{ ipv4_host | ipaddr('broadcast') }}

    # Generated configuration file
    iface eth0 inet static
        address   192.0.2.48
        network   192.0.2.0
        netmask   255.255.255.0
        broadcast 192.0.2.255

上記の例では、値がリストに格納されているという事実を処理する必要がありました。
これは、
インターフェイスに 1 つの IP アドレスしか設定できない IPv4 ネットワークでは珍しいことです。ただし、IPv6 ネットワークでは、
インターフェースに複数の IP アドレスを設定できます。

  .. code-block:: jinja

    # Jinja2 template
    iface eth0 inet6 static
      {% set ipv6_list = host_prefix | unique | ipv6('host/prefix') %}
      address {{ ipv6_list[0] }}
      {% if ipv6_list | length > 1 %}
      {% for subnet in ipv6_list[1:] %}
      up   /sbin/ip address add {{ subnet }} dev eth0
      down /sbin/ip address del {{ subnet }} dev eth0
      {% endfor %}
      {% endif %}

    # Generated configuration file
    iface eth0 inet6 static
      address 2001:db8:deaf:be11::ef3/64

必要な場合は、「host/prefix」値からサブネットおよびプレフィックス情報を抽出できます。

    # {{ host_prefix | ipaddr('host/prefix') | ipaddr('subnet') }}
    ['2001:db8:deaf:be11::/64', '192.0.2.0/24']

    # {{ host_prefix | ipaddr('host/prefix') | ipaddr('prefix') }}
    [64, 24]
    
サブネットマスクの CIDR 表記への変換
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ネットワークアドレスおよびサブネットマスクの形式でサブネットを指定すると、``ipaddr()`` フィルターは CIDR 表記に変換できます。 これは、ネットワーク設定に関する Ansible ファクトをサブネットマスクから CIDR 形式に変換する際に便利です。

    ansible_default_ipv4: {
        address:"192.168.0.11",
        alias: "eth0",
        broadcast:"192.168.0.255",
        gateway:"192.168.0.1",
        interface: "eth0",
        macaddress: "fa:16:3e:c4:bd:89",
        mtu:1500,
        netmask:"255.255.255.0",
        network:"192.168.0.0",
        type: "ether"
    }

最初に、ネットワークとネットマスクを連結します。

    net_mask = "{{ ansible_default_ipv4.network }}/{{ ansible_default_ipv4.netmask }}"
    '192.168.0.0/255.255.255.0'

これにより、``ipaddr()`` で正則形式に変換して、CIDR 形式でサブネットを生成できます。

    # {{ net_mask | ipaddr('prefix') }}
    '24'

    # {{ net_mask | ipaddr('net') }}
    '192.168.0.0/24'

CIDR 表記でのネットワーク情報の取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IP アドレスを指定すると、``ipaddr()`` フィルターは CIDR 表記でネットワークアドレスを生成することができます。
これは、CIDR 形式の IP アドレスからネットワークアドレスを取得する場合に便利です。

以下は IP アドレスの例です。

    ip_address = "{{ ansible_default_ipv4.address }}/{{ ansible_default_ipv4.netmask }}"
    '192.168.0.11/255.255.255.0'

これは、CIDR 表記形式でネットワークアドレスを取得するのに使用できます。

    # {{ ip_address | ipaddr('network/prefix') }}
    '192.168.0.0/24'

IP アドレス変換
^^^^^^^^^^^^^^^^^^^^^

ここでは、テストリストを再度使用します。

    # Example list of values
    test_list = ['192.24.2.1', 'host.fqdn', '::1', '192.168.32.0/24', 'fe80::100/10', True, '', '42540766412265424405338506004571095040/64']
    
IPv4 アドレスを IPv6 アドレスに変換できます。

    # {{ test_list | ipv4('ipv6') }}
    ['::ffff:192.24.2.1/128', '::ffff:192.168.32.0/120']
    
IPv6 から IPv4 への変換はほとんど機能しません。

    # {{ test_list | ipv6('ipv4') }}
    ['0.0.0.1/32']
    
ただし、必要に応じて二重変換を行うことができます。

    # {{ test_list | ipaddr('ipv6') | ipaddr('ipv4') }}
    ['192.24.2.1/32', '0.0.0.1/32', '192.168.32.0/24']
    
整数を IP アドレスに変換するのと同じ方法で、
IP アドレスを整数に変換できます。

    # {{ test_list | ipaddr('address') | ipaddr('int') }}
    [3222798849, 1, '3232243712/24', '338288524927261089654018896841347694848/10', '42540766412265424405338506004571095040/64']
    
任意の区切り文字を使用して、IPv4 アドレスを `16 進表記 <https://en.wikipedia.org/wiki/Hexadecimal>`_ に変換できます。

    # {{ '192.168.1.5' | ip4_hex }}
    c0a80105
    # {{ '192.168.1.5' | ip4_hex(':') }}
    c0:a8:01:05

IP アドレスを PTR レコードに変換できます。

    # {% for address in test_list | ipaddr %}
    # {{ address | ipaddr('revdns') }}
    # {% endfor %}
    1.2.24.192.in-addr.arpa.
    1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.ip6.arpa.
    0.32.168.192.in-addr.arpa.
    0.0.1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.e.f.ip6.arpa.
    0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.d.a.a.f.c.2.3.0.8.b.d.0.1.0.0.2.ip6.arpa.


IPv4 アドレスの 6 から 4 アドレスへの変換
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`6to4`_ トンネルは、IPv4 のみのネットワークから IPv6 インターネットにアクセスする方法です。パブリック
IPv4 アドレスがある場合は、
``2002::/16`` ネットワーク範囲で、IPv6 に相当するものを自動的に構成できます。変換したら、
``2002:xxxx:xxxx::/48`` サブネットにアクセスできます 
(必要に応じて 65535``/64`` サブネットに分割できます)。

IPv4 アドレスを変換するには、単に ``'6to4'`` フィルターを介してこれを送信します。これは、
自動的にルーターアドレスに変換されます (``::1/48`` ホストアドレスを使用)。

    # {{ '193.0.2.0' | ipaddr('6to4') }}
    2002:c100:0200::1/48

.. _6to4: https://en.wikipedia.org/wiki/6to4

範囲内の IP アドレスの検索
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

IP 範囲内で使用可能な IP アドレスを見つけるには、以下の ``ipaddr`` フィルターを試行します。

範囲内の次の使用可能な IP アドレスを見つけるには、``next_usable`` を使用します::

    # {{ '192.168.122.1/24' | ipaddr('next_usable') }}
    192.168.122.2

範囲から最後の使用可能な IP アドレスを見つけるには、``last_usable`` を使用します::

    # {{ '192.168.122.1/24' | ipaddr('last_usable') }}
    192.168.122.254

指定したネットワークアドレスから利用可能な IP アドレスの範囲を検索するには、``range_usable`` を使用します。

    # {{ '192.168.122.1/24' | ipaddr('range_usable') }}
    192.168.122.1-192.168.122.254

範囲内で nth が使用可能な次の IP アドレスを見つけるには、``next_nth_usable`` を使用します。

    # {{ '192.168.122.1/24' | next_nth_usable(2) }}
    192.168.122.3

この例では、``next_nth_usable`` は、指定された IP 範囲で使用可能な 2 番目の IP アドレスを返します。


IP 計算
^^^^^^^

バージョン 2.7 における新機能

``ipmath()`` フィルターは、単純な IP 計算/演算をするのに使用できます。

以下は簡単な例です。

    # {{ '192.168.1.5' | ipmath(5) }}
    192.168.1.10

    # {{ '192.168.0.5' | ipmath(-10) }}
    192.167.255.251

    # {{ '192.168.1.1/24' | ipmath(5) }}
    192.168.1.6

    # {{ '192.168.1.6/24' | ipmath(-5) }}
    192.168.1.1

    # {{ '192.168.2.6/24' | ipmath(-10) }}
    192.168.1.252

    # {{ '2001::1' | ipmath(10) }}
    2001::b

    # {{ '2001::5' | ipmath(-10) }}
    2000:ffff:ffff:ffff:ffff:ffff:ffff:fffb



サブネット操作
^^^^^^^^^^^^^^^^^^^

``ipsubnet()`` フィルターは、さまざまな方法でネットワークサブネットを操作するために使用できます。

IP アドレスとサブネットの例を以下に示します。

    address = '192.168.144.5'
    subnet  = '192.168.0.0/16'

特定の文字列がサブネットであるかどうかを確認するには、
引数なしでフィルターを通過させます。指定の文字列が IP アドレスである場合は、
サブネットに変換されます::

    # {{ address | ipsubnet }}
    192.168.144.5/32

    # {{ subnet | ipsubnet }}
    192.168.0.0/16

``ipsubnet()`` フィルターの最初のパラメーターとしてサブネットサイズを指定し、
サブネットのサイズが **現在のものよりも小さい場合** に指定して、
特定のサブネットを分割できるサブネットの数を取得します。

    # {{ subnet | ipsubnet(20) }}
    16

``ipsubnet()`` フィルターの 2 番目の引数はインデックス番号です。
これを指定すると、指定したサイズの新しいサブネットを取得できます::

    # First subnet
    # {{ subnet | ipsubnet(20, 0) }}
    192.168.0.0/20

    # Last subnet
    # {{ subnet | ipsubnet(20, -1) }}
    192.168.240.0/20

    # Fifth subnet
    # {{ subnet | ipsubnet(20, 5) }}
    192.168.80.0/20

    # Fifth to last subnet
    # {{ subnet | ipsubnet(20, -5) }}
    192.168.176.0/20

サブネットの代わりに IP アドレスを指定し、最初の引数としてサブネットサイズを指定すると、
``ipsubnet()`` フィルターは、
代わりに、指定した IP アドレスを含む最大のサブネットを返します。

    # {{ address | ipsubnet(20) }}
    192.168.144.0/20

インデックス番号を 2 番目の引数として指定することにより、
より小さなサブネットを選択できます::

    # First subnet
    # {{ address | ipsubnet(18, 0) }}
    192.168.128.0/18

    # Last subnet
    # {{ address | ipsubnet(18, -1) }}
    192.168.144.4/31

    # Fifth subnet
    # {{ address | ipsubnet(18, 5) }}
    192.168.144.0/23

    # Fifth to last subnet
    # {{ address | ipsubnet(18, -5) }}
    192.168.144.0/27

別のサブネットを 2 番目の引数として指定すると、
2 番目のサブネットに最初のサブネットが含まれる場合は、2 番目のサブネットの最初のサブネットのランクを指定できます::

    # The rank of the IP in the subnet (the IP is the 36870nth /32 of the subnet)
    # {{ address | ipsubnet(subnet) }}
    36870

    # The rank in the /24 that contain the address
    # {{ address | ipsubnet('192.168.144.0/24') }}
    6

    # An IP with the subnet in the first /30 in a /24
    # {{ '192.168.144.1/30' | ipsubnet('192.168.144.0/24') }}
    1

    # The fifth subnet /30 in a /24
    # {{ '192.168.144.16/30' | ipsubnet('192.168.144.0/24') }}
    5

2 番目のサブネットに最初のサブネットが含まれていない場合には、``ipsubnet()`` フィルターによりエラーが発生します。


``ipaddr()`` フィルターと一緒に ``ipsubnet()`` フィルターを使用できます。
たとえば、``/48`` プレフィックスをより小さい ``/64`` サブネットに分割できます。

    # {{ '193.0.2.0' | ipaddr('6to4') | ipsubnet(64, 58820) | ipaddr('1') }}
    2002:c100:200:e5c4::1/64

IPv6 サブネットのサイズのため、
サブネット間のサイズの違いによっては、
低速のコンピューターではすべてのサブネットを繰り返すため、正しいサブネットを見つけるのに時間がかかる場合があります。

サブネットのマージ
^^^^^^^^^^^^^^

バージョン 2.6 における新機能

``cidr_merge()`` フィルターを使用して、
サブネットまたは個々のアドレスを最小限の表現にマージし、
重複するサブネットを折りたたみ、可能な限り隣接するサブネットをマージできます。

    {{ ['192.168.0.0/17', '192.168.128.0/17', '192.168.128.1' ] | cidr_merge }}
    # => ['192.168.0.0/16']

    {{ ['192.168.0.0/24', '192.168.1.0/24', '192.168.3.0/24'] | cidr_merge }}
    # => ['192.168.0.0/23', '192.168.3.0/24']

アクションを「マージ」から「スパン」に変更すると、
代わりにすべての入力を含む最小のサブネットが返されます。

    {{ ['192.168.0.0/24', '192.168.3.0/24'] | cidr_merge('span') }}
    # => '192.168.0.0/22'

    {{ ['192.168.1.42', '192.168.42.1'] | cidr_merge('span') }}
    # => '192.168.0.0/18'

MAC アドレスフィルター
^^^^^^^^^^^^^^^^^^

``hwaddr()`` フィルターを使用して、
特定の文字列が MAC アドレスであるかどうかを確認したり、さまざまな形式に変換したりできます。例::

    # Example MAC address
    macaddress = '1a:2b:3c:4d:5e:6f'

    # Check if given string is a MAC address
    # {{ macaddress | hwaddr }}
    1a:2b:3c:4d:5e:6f

    # Convert MAC address to PostgreSQL format
    # {{ macaddress | hwaddr('pgsql') }}
    1a2b3c:4d5e6f

    # Convert MAC address to Cisco format
    # {{ macaddress | hwaddr('cisco') }}
    1a2b.3c4d.5e6f

サポートされる形式により、以下の変換で、MAC アドレス ``1a:2b:3c:4d:5e:6f`` が作成されます。

    bare:1A2B3C4D5E6F
    bool:True
    int:28772997619311
    cisco:1a2b.3c4d.5e6f
    eui48 or win:1A-2B-3C-4D-5E-6F
    linux or unix:1a:2b:3c:4d:5e:6f:
    pgsql, postgresql, or psql:1a2b3c:4d5e6f

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_filters`
       Jinja2 フィルターの概要およびその用途
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
