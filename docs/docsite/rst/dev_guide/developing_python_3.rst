.. _developing_python_3:

********************
Ansible および Python 3
********************

.. contents:: トピック
   :local:

Ansible が Python 2 と Python 3 の両方で動作する 1 つのコードベースを維持しているのは、
Ansible が、
多種多様なマシンを管理できるようにしたいからです。 Ansible への貢献者は、
Ansible の他のバージョンと同じバージョンの Python で動作するコードを書けるように、
本ガイドに示されたヒントを意識する必要があります。

作成したコードが Python 2 と同様に Python 3 でも確実に動作するようにするために、
ここで説明されているヒントやコツ、イディオムを学びましょう。これらの考慮事項のほとんどは、3 種類のすべての Ansible コードに適用されます。

1. コントローラーのコード - :command:`/usr/bin/ansible` を呼び出したマシン上で動作するコード。
2. モジュール - 管理マシンに Ansible が送信したり起動したりするコード。
3. 共有されている ``module_utils`` コード - タスクを実行するためにモジュールが使用する一般的なコードで、コントローラーのコードでも使用されることがあります。

ただし、この 3 種類のコードで同じ文字列戦略が使用されているわけではありません。モジュールまたは一部の ``module_utils`` コードを開発している場合は、
必ず文字列戦略のセクションで詳細を確認してください。

Python 3.x および Python 2.x の最小バージョン
============================================

コントローラーでは、Python 3.5 以降、および Python 2.7 以降をサポートしています。 モジュールでは、
Python 3.5 以降、および Python 2.6 以降をサポートしています。

Python 3.5 は、
長期サポート (LTS: Long Term Support) の Linux ディストリビューション (この場合は Ubuntu-16.04) でデフォルトの Python として採用されている最も古い Python 3 のバージョンであるため、最小バージョンとして採用されました。
以前の LTS Linux ディストリビューションでは、Python 3 バージョンの代わりに、
ユーザーが代わりに使用できる Python 2 バージョンが同梱されていました。

Python 2 の場合、デフォルトは、モジュールが Python 2.6 以上で動作するようになっています。 これにより、
Python 2.6 で動かなくなった古いディストリビューションのユーザーが、
マシンを管理できるようになります。 モジュールは、
依存ライブラリーの一つがより新しいバージョンの Python を必要とする場合は、Python 2.6 のサポートを停止することができます。これは、
モジュールを新しいバージョンの Python でのみ使用できるようにするために、
不要な依存ライブラリーを追加することを促すものではありません。
代わりに、
一部のライブラリー (たとえば boto3 や docker-py) は新しいバージョンの Python でしか機能しないことを認めています。

.. note:: Python 2.4 モジュールでのサポート:

    Python 2.4 および Python 2.5 のサポートは Ansible 2.4 で終了しました。 RHEL 5 (および CentOS 5 などのリビルド) は、
    2017 年 4 月までサポートされていました。
    2017 年 4 月にリリースされた Ansible 2.3 は、
    モジュールで Python 2.4 をサポートする最後の Ansible リリースでした。

Python 2 および Python 3 をサポートする Ansible コードの開発
===========================================================

Python 2 と Python 3 の両方をサポートするコードを書くことについて学び始めるのに最適なのは、
`Lennart Regebro 氏の書籍「Porting to Python 3」<http://python3porting.com/>`_ です。
本書では、Python 3 に移植するためのいくつかの戦略が説明されています。私たちが使用しているのは、
「``1 つのコードベースから Python 2 と Python 3 をサポートすること
<http://python3porting.com/strategies.html#python 2-and-python 3-without-conversion>`_」です。

Python 2 および Python 3 の文字列を理解
----------------------------------------------

Python 2 と Python 3 では文字列の扱いが異なるため、
Python 3 をサポートするコードを書くときには、どのような文字列モデルを使用するかを決めなければなりません。 文字列は (C 言語のように) バイトの配列にすることもできますし、
テキストの配列にすることもできます。 ここでの「テキスト」とは、文字、数字 (digit または number)、
その他の出力可能な記号、
そして少数の出力できない「記号」(コントロールコード) を指しています。

Python 2 では、
この 2 つのタイプ (バイトを表す :class:`str <python:str>` とテキストを表す :func:`unicode <python:unicode>`) は、しばしば区別しないで使用されます。 ASCII 文字だけを扱う場合は、
文字列を結合したり、比較したり、
あるタイプから別のタイプに自動的に変換したりできます。 非 ASCII 文字が導入されると、
Python 2 は、
非 ASCII 文字がどのようなエンコーディングであるべきかを知らないために例外を発生し始めます。

Python 3では、バイト (:class:`bytes <python3:bytes>`) とテキスト (:class:`str <python3:str>`) の分離をより厳密にすることで、
この動作を変更しています。 Python 3 は、
2 つの型を結合して比較しようとすると例外が発生します。 プログラマーは、
ある型から別の型に明示的に変換して、それぞれの値を混合させる必要があります。

Python 3 では、プログラマーは、
コードがバイト型とテキスト型を不適切に混合していることがすぐに分かりますが、
Python 2 では、ユーザーが非 ASCII 入力を入力して例外が発生するまでは、これらの型を混合しているコードが動作するかもしれません。
Python 3 では、プログラマーが意図せずにテキスト文字列とバイト文字列を混在させないように、
プログラムの中で文字列を扱うための戦略を積極的に定義することを強制しています。

Ansible では、
コントローラーで :ref: `modules <module_string_strategy>` コード文字列を扱うための戦略と、 :ref:`module_utils <module_utils_string_strategy>` コードで文字列を扱うための戦略は異なります。

.. _controller_string_strategy:

コントローラー文字列戦略: Unicode Sandwich
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

コントローラーでのコードでは、
Unicode Sandwichとして知られる戦略を使用します (Python 2 の :func:`unicode  <python:unicode>` テキストタイプにちなんで命名されました)。 Unicode Sandwich では、
コードと外部の世界 (たとえば、ファイルやネットワークIO、環境変数、
いくつかのライブラリー呼び出しなど) の境界でバイトを受け取ります。
このバイトをテキストに変換し、
コードの内部でそれを使用する必要があります。 この文字列を外の世界に送り返さなければならないときは、
まずテキストをバイトに変換します。
これを視覚化すると、
上下にバイトの層があり、その間に変換の層があり、中央にすべてのテキストタイプがある「サンドイッチ」のようになります。

Unicode Sandwich の共通の境界: コントローラーコードのテキストにバイトを変換する場所
-----------------------------------------------------------------------------------

これは、Unicode Sandwich 文字列戦略を使用する際に、
バイトへの変換とバイトからの変換が必要な場所の部分的なリストです。網羅的ではありませんが、
どこに問題があるかを理解するためのアイデアが得られます。

ファイルの読み取りおよび書き込み
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 2では、ファイルから読み込むとバイトが生成されます。 Python 3 では、テキストを生成できます。
両方に移植性のあるコードを作るために、テキストを生成する Python 3 の機能は利用せず、
代わりに明示的に自分自身で変換を行います。例:

.. code-block:: python

    from ansible.module_utils._text import to_text

    with open('filename-with-utf8-data.txt', 'rb') as my_file:
        b_data = my_file.read()
        try:
            data = to_text(b_data, errors='surrogate_or_strict')
        except UnicodeError:
            # Handle the exception gracefully -- usually by displaying a good
            # user-centric error message that can be traced back to this piece
            # of code.
            pass

.. note:: Ansible の多くは、エンコードされたテキストがすべて UTF-8 であることを想定しています。 他のエンコーディングに対する需要があれば、
    いつかこれが変更されるかもしれませんが、
    今のところはバイトは UTF-8 であると考えて問題ありません。

ファイルへの書き込みは、その逆の処理です。

.. code-block:: python

    from ansible.module_utils._text import to_bytes

    with open('filename.txt', 'wb') as my_file:
        my_file.write(to_bytes(some_text_string))

UTF-8 に変換していて、Python のテスト文字列がすべて UTF-8 に戻されるため、
ここで :exc:`UnicodeError` 
を捕える (キャッチする) 必要はないことに注意してください。

ファイルシステムの相互作用
^^^^^^^^^^^^^^^^^^^^^^

UNIX 系のシステムではファイル名はバイトであるため、
ファイル名を扱う際にはバイトに戻すことがあります。 Python 2 では、
これらの関数にテキスト文字列を渡すと、
関数内ではテキスト文字列がバイト文字列に変換され、非 ASCII 文字が含まれている場合にトレースバックが発生します。 Python 3 では、
テキスト文字列が現在のロケールでデコードできない場合にのみトレースバックが発生しますが、
明示的にして、
両方のバージョンで動作するコードを用意しておくことが推奨されます。

.. code-block:: python

    import os.path

    from ansible.module_utils._text import to_bytes

    filename = u'/var/tmp/くらとみ.txt'
    f = open(to_bytes(filename), 'wb')
    mtime = os.path.getmtime(to_bytes(filename))
    b_filename = os.path.expandvars(to_bytes(filename))
    if os.path.exists(to_bytes(filename)):
        pass

ファイルシステムと対話せずに、
ファイル名を文字列として (あるいはファイルシステムと対話する C ライブラリーとして) 操作しているだけの場合は、
バイトに変換せずに済むことがよくあります。

.. code-block:: python

    import os.path

    os.path.join(u'/var/tmp/café', u'くらとみ')
    os.path.split(u'/var/tmp/café/くらとみ')

一方、コードがファイル名を操作したり、
ファイルシステムと対話したりする必要がある場合は、
すぐにバイトに変換してバイト単位で操作した方が便利な場合があります。

.. warning:: 関数に渡される変数がすべて同じ型であることを確認してください。
    :func:`python3:os.path.join` のように複数の文字列を受け取り、
    それらを組み合わせて使用するような作業をしているのであれば、
    すべての型が同じであることを確認する必要があります (すべてのバイトかすべてのテキスト)。 バイトとテキストを混在させると、
    トレースバックの原因になります。

他のプログラムとの対話
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

他のプログラムとの対話は、
オペレーティングシステムおよび C ライブラリーを経由し、UNIX カーネルが定義しているもので動作します。 これらのインタフェースは、
すべてバイト指向であるため、
Python のインタフェースもバイト指向です。 Python 2 でも Python 3 でも、Python のサブプロセスライブラリーにバイト文字列を与え、
そこからバイト文字列を返すことを期待する必要があります。

Ansible のコントローラーコードの中で、
他のプログラムと対話する主な場所の 1 つは、接続プラグインの ``exec_command`` メソッドです。 これらのメソッドは、
コマンド (およびコマンドへの引数) で受け取ったテキスト文字列をバイトに変換して実行し、
stdout と stderr をバイト文字列として返します。
上位レベルの関数 (アクションプラグインの ``_low_level_execute_command`` のようなもの) は、
出力をテキスト文字列に変換します。

.. _module_string_strategy:

モジュール文字列戦略: ネイティブ文字列
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

モジュールでは、ネイティブ文字列として知られる戦略を使用しています。これにより、
モジュール内の文字列はすべてテキストであることを義務づけ、
境界でテキストとバイトとの間の変換を行うことで、下位互換性を壊さないようにすることで、
Ansible 
のモジュールの多くを保守しているコミュニティーメンバーが作業しやすくなるようにしています。

ネイティブ文字列とは、
素の文字列リテラルを指定したときに Python が使用する型を指します。

.. code-block:: python

    "This is a native string"

Python 2 では、これらはバイト文字列です。Python 3 では、これらはテキスト文字列です。モジュールは、
Python 2 ではバイト、Python 3 ではテキストを期待するようにコード化されている必要があります。

.. _module_utils_string_strategy:

Module_utils 文字列戦略: ハイブリッド
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``module_utils`` のコードでは、ハイブリッド文字列戦略を使用しています。Ansible の ``module_utils`` コードは、
大部分はモジュールコードに似ていますが、
その一部はコントローラーでも使用されています。そのため、モジュールとコントローラーの前提条件、
特に文字列戦略との互換性が必要となります。
module_utils コードは、ネイティブ文字列を関数の入力として受け入れ、
ネイティブ文字列を出力として出力しようとします。

``module_utils`` コードで以下を行います。

* 関数は、文字列パラメーターをテキスト文字列かバイト文字列のいずれかで使用できるようにする **必要があります**。
* 関数は、提供された文字列と同じタイプの文字列を返すか、実行している Python のバージョンに合わせたネイティブの文字列タイプを返すことができます。
* 文字列を返す関数は、指定の文字列と同じ型の文字列を返すのか、ネイティブの文字列を返すのかを文書化 **する必要があります**。

そのため、module-utils 関数はその性質上、非常に保守的であることが多くなります。
彼らは、関数の最初に文字列パラメーターをテキストに変換し (``ansible.module_utils._text.to_text``)、
その後、
戻り値をネイティブの文字列型に変換し (``ansible.module_utils._text.to_native`` を使用)、
あるいはパラメーターが受け取った文字列型に戻します。

Python 2/Python 3 互換のためのヒント、トリック、イディオム
------------------------------------------------------------

前方互換性のあるボイラープレートの使用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 2 と Python 3 で特定の構成要素が同じように動作するようにするために、
すべての python ファイルの先頭に以下のボイラプレートコードを使用してください。

.. code-block:: python

    # Make coding more python3-ish
    from __future__ import (absolute_import, division, print_function)
    __metaclass__ = type

``__metaclass__ = type`` は、
ファイルで定義されているすべてのクラスを :class:`object <python3:object>` から明示的に継承することなく、新しいスタイルのクラスにします。

``__future__`` のインポートは以下のようになります。

:absolute_import: インポートは、
    インポートするモジュールが存在するディレクトリーを飛ばして、
    インポートされるモジュールのために :data:`sys.path <python3:sys.path>` を探します。 コードがインポートを行うモジュールが存在するディレクトリーを使用したい場合は、
    そのための新しいドット表記があります。
:division:整数の除算が常に浮動小数点を返すようになります。 商を見つける必要がある場合は、
   ``x / y`` の代わりに ``x // y`` を使用します。
:print_function::func:`print <python3:print>` をキーワードから関数に変更しました。

.. seealso::
    * `PEP 0328: Absolute Imports <https://www.python.org/dev/peps/pep-0328/#guido-s-decision>`_
    * `PEP 0238: Division <https://www.python.org/dev/peps/pep-0238>`_
    * `PEP 3105: Print function <https://www.python.org/dev/peps/pep-3105>`_

バイト文字列の接頭辞 ``b_``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

テキスト型とバイト型が混在するとトレースバックが発生するため、
どの変数がテキストを保持していて、どの変数がバイトを保持しているかを明確にします。 これを行うには、
バイトを保持する変数の前に ``b_`` を付けます。 たとえば、以下のようになります。

.. code-block:: python

    filename = u'/var/tmp/café.txt'
    b_filename = to_bytes(filename)
    with open(b_filename) as f:
        data = f.read()

代わりにテキスト文字列に接頭辞を付けていないのは、
境界のバイト文字列だけを操作しているためで、
テキストよりもバイトを必要とする変数が少ないためです。

Ansible に同梱されている ``python-six`` ライブラリーをインポート
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

サードパーティーの `python-six <https://pythonhosted.org/six/>`_ ライブラリーは、
Python 2 と Python 3 の両方で動作するコードを作成するプロジェクトを支援するために存在します。 Ansible には module_utils にライブラリーのバージョンが含まれているため、
リモートシステムにインストールしなくても、
他のモジュールが使用できるようになっています。 これを利用するには、
次のようにインポートします。

.. code-block:: python

    from ansible.module_utils import six

.. note:: Ansible は、six のシステムコピーを使用することもできます。

    Ansible は、システムコピーが、
    Ansible がバンドルしているものよりも後のバージョンのものであれば、six のシステムコピーを使用します。

``as`` で例外を処理します。
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 2.6 以降および Python 3 でコードが機能するには、
``as`` キーワードを使用する新しい例外キャッチ構文を使用してください。

.. code-block:: python

    try:
        a = 2/0
    except ValueError as e:
        module.fail_json(msg="Tried to divide by zero: %s" % e)

以下の構文は、Python 3 のすべてのバージョンで失敗するため、**使用しないでください**。

..Python2 は認識されないため、このコードブロックは強調表示されません。これは、Python 3 でテストに合格するために必要です。
.. code-block:: none

    try:
        a = 2/0
    except ValueError, e:
        module.fail_json(msg="Tried to divide by zero: %s" % e)

8 進数の更新
^^^^^^^^^^^^^^^^^^^^

Python 2.xでは、8 進数リテラルは ``0755`` と指定できました。 Python 3 では、
8進数は ``0o755`` と指定しなければなりません。

コントローラーコードの文字列形式
-------------------------------------

Python 2.6 との互換性のために ``str.format()`` を使用してください。
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 2.6 以降、
文字列は ``format()`` というメソッドで文字列をまとめることができるようになりました。 ただし、よく使用される ``format()`` の機能は Python 2.7 までは追加されていなかったため、
Ansible のコードでは使用しないようにしてください。

.. code-block:: python

    # Does not work in Python 2.6!
    new_string = "Dear {}, Welcome to {}".format(username, location)

    # Use this instead
    new_string = "Dear {0}, Welcome to {1}".format(username, location)

上記の書式文字列は、
どちらも ``format()`` メソッドにおける場所の引数を文字列にマッピングしています。 ただし、
最初のバージョンは Python 2.6 では動作しません。 このコードに Python 2.6 との互換性をもたせるように、
プレースホルダに数字を入れることを忘れないようにしてください。

.. seealso::
    Python ドキュメント `書式文字列 <https://docs.python.org/2/library/string.html#formatstrings>`_

バイト文字列でのパーセント書式の使用
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python 3.xでは、バイト文字列には ``format()`` メソッドがありません。 ただし、
以前の、パーセント書式に対するサポートがあります。

.. code-block:: python

    b_command_line = b'ansible-playbook --become-user %s -K %s' % (user, playbook_file)

.. note:: Python 3.5 で追加されたパーセント書式

    バイト文字列のパーセント書式が Python 3.5で追加されました。
    Python 3.5 は最小バージョンであるため、これは問題ではありません。
    ただし、Python 3.4 以前のバージョンで Ansible のコードをテストしている場合は、
    ここでのバイト文字列の書式設定が適切に処理されないことがあります。
    その場合は、Python 3.5 にアップグレードしてテストしてください。

.. seealso::
    Python ドキュメンテーション「`percent formatting <https://docs.python.org/2/library/stdtypes.html#string-formatting>`_」

.. _testing_modules_python_3:

Python 3 でのモジュールのテスト
===================================

Ansible モジュールでは、Python 3 をサポートするためのコーディングが、
他のプロジェクトの通常のコードよりもやや難しくなっています。Ansible モジュールのユニットテストには多くのモック処理が必要で、
変更がすべて修正されているかどうかをテストしたり、
後続のコミットで Python 3 のサポートにレグレッションが起きていないことを確認したりするのが難しくなります。詳細は、「:ref:`テスト` <developing_testing>」
ページを参照してください。
