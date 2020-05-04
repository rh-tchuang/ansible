.. _yaml_syntax:


YAML 構文
===========

このページでは、Ansible Playbook (Ansible での設定管理言語) の表現方法である、
正しい YAML 構文を概説します。  

XML や JSON などの一般的な他のデータ形式に比べて人間による解読および記述が容易であるため、
YAML を使用します。 さらに、プログラミング言語の多くには、
YAML に対応するライブラリーが提供されています。

:ref:`working_with_playbooks` も合わせて参照し、
実際にどのように使用されているかを確認してください。


YAML の基礎
-----------

Ansible で使用する場合には、YAML ファイルのほぼすべてがリストで開始されます。   
リストの各アイテムは、
「ハッシュ」または「ディクショナリー」と一般的に呼ばれる、キー/値のペアのリストとなっています。 そのため、
YAML でリストとディクショナリーを記述する方法を理解する必要があります。

YAML には、他にも固有の特徴があります。 YAML ファイルはすべて (Ansible との関係の有無に関わらず)、
任意で ``---`` から開始して、``...`` で終わらせることができます。 これは、YAML 形式の一部で、ドキュメントの最初と最後を示します。

リストのメンバーが記載されている行はすべて、同じ幅分インデントして、``"- "`` (ダッシュとスペース) で開始します::

    ---
    # A list of tasty fruits
    - Apple
    - Orange
    - Strawberry
    - Mango
    ...

ディクショナリーは、シンプルな ``key: value`` の形式で表現します (コロンの後にはスペースを挿入します)::

    # An employee record
    martin:
        name: Martin D'vloper
        job: Developer
        skill: Elite

ディクショナリーのリストや、値がリスト場合や、ディクショナリーと値が混合している場合など、より複雑なデータ構造も可能です::

    # Employee records
    -  martin:
        name: Martin D'vloper
        job: Developer
        skills:
          - python
          - perl
          - pascal
    -  tabitha:
        name: Tabitha Bitumen
        job: Developer
        skills:
          - lisp
          - fortran
          - erlang

ディクショナリーとリストは、必要であれば、略語形式で表現することも可能です::

    ---
    martin: {name:Martin D'vloper, job:Developer, skill:Elite}
    ['Apple', 'Orange', 'Strawberry', 'Mango']

以下は「フローコレクション」と呼ばれます。

.. _truthiness:

Ansible では以下の形式はあまり使用されませんが、ブール型値 (True/False) を複数形式で指定することも可能です::

    create_key: yes
    needs_agent: no
    knows_oop:True
    likes_emacs:TRUE
    uses_cvs: false

値は、 ``|`` または ``>`` を使用して複数行に分けることができます。 「リテラル形式のブロックスカラー」 ``|`` を使用して複数行に分けた場合には、改行と、末尾にあるスペースが含まれます。
「折り返し形式のブロックスカラー」 ``>`` を使用すると、改行を折り返してスペースに置き換えます。この文字を使用して、非常に長い行を簡単に解読し、編集できるようにします。
いずれの場合も、インデントは無視されます。
以下に例を示します::

    include_newlines: |
                exactly as you see
                will appear these three
                lines of poetry

    fold_newlines: >
                this is really a
                single line of text
                despite appearances

上記の ``>`` の例では、改行はすべて折り返されてスペースに変換されますが、改行を強制的に確保させる方法が 2 種類あります::

    fold_some_newlines: >
        a
        b

        c
        d
          e
        f
    same_as: "a b\nc d\n  e\nf\n"

これまでに学習した内容を、任意の YAML 例にまとめてみます。
以下は、Ansible とは関係ありませんが、どのような形式になるかを示しています::

    ---
    # An employee record
    name: Martin D'vloper
    job: Developer
    skill: Elite
    employed: True
    foods:
        - Apple
        - Orange
        - Strawberry
        - Mango
    languages:
        perl: Elite
        python: Elite
        pascal: Lame
    education: |
        4 GCSEs
        3 A-Levels
        BSc in the Internet of Things

`Ansible` Playbook の記述を開始するにあたり、以上が YAML について理解しておく必要のある内容です。

Gotchas
-------

引用符なしのスカラーに何でも挿入できますが、例外がいくつかあります。
コロンの後のスペース (または改行) ``": "`` は、マッピングを示すインジケーターです。
スペースの後にシャープ記号 ``" #"`` を指定すると、その後はコメントになります。

このため、以下のような場合には、YAML 構文のエラーが発生します::

    foo: somebody said I should put a colon here: so I did

    windows_drive: c:

...ただし、これは機能します::

    windows_path: c:\windows

コロンを使用してハッシュ記号を引用し、その後ろにスペースを指定するか、行末にしてください::

    foo: 'somebody said I should put a colon here: so I did'
    
    windows_drive: 'c:'

...そしてコロンが保存されます。

または、二重引用符を使用してください::

    foo: "somebody said I should put a colon here: so I did"
    
    windows_drive: "c:"

二重引用符ではエスケープを使用できる点が、
一重引用符と二重引用符との相違点です::

    foo: "a \t TAB and a \n NEWLINE"

使用可能なエスケープの一覧は、YAML 仕様の「Escape Sequences」 (YAML 1.1) または「Escape Characters」(YAML 1.2) に記載されています。

以下は無効な YAML です。

.. code-block:: text

    foo: "an escaped \' single quote"


さらに、Ansible は変数に "{{ var }}" を使用します。 コロンの後に "{" が指定されている場合には、
YAML はその値がディクショナリーであると認識するため、以下のように引用する必要があります::

    foo: "{{ variable }}"

引用符で開始される値は、値の一部だけでなく、値全体を引用符で囲む必要があります。ただしく値を引用する方法について、以下に追加で例を挙げています::

    foo: "{{ variable }}/additional/string/literal"
    foo2: "{{ variable }}\backslashes\are\also\special\characters"
    foo3: "even if it's just a string literal it must all be quoted"
    
以下は有効ではありません::

    foo:"E:\path\"rest\of\path

``'`` および ``"`` 以外に、
``[] {} > | * & ! % # ` @ ,`` などの特殊文字 (予約文字) が複数あり、引用なしのスカラーの最初の文字として使用できません。

また、``? : -`` にも注意が必要です。YAML では、上記の記号の後にスペース以外の文字が続く場合には、文字列の最初に指定できますが、
YAML プロセッサーの実装は異なるため、引用を使用することが推奨されます。

フローコレクションでは、ルールはもう少し厳密です::

    a scalar in block mapping: this } is [ all , valid

    flow mapping: { key: "you { should [ use , quotes here" }

ブール値の変換は便利ですが、リテラルの `yes` や、文字列として他のブール値を指定する場合など問題になる場合があります。
上記場合には、引用符だけを使用します::

    non_boolean: "yes"
    other_string:"False"


YAML は、
特定の文字列は `1.0` の文字列など、浮動小数点の値に変換します。バージョン番号を指定する必要がある場合には (requirements.yml ファイル内など)、
浮動小数点の値のようであれば、
その値を引用符で囲む必要があります::

  version: "1.0"


.. seealso::

   :ref:`working_with_playbooks`
       Playbook でできることと、Playbook を記述および実行する方法を学びます。
   `YAMLLint <http://yamllint.com/>`_
       YAML ヒント (オンライン) は、問題が発生した場合に YAML 構文のデバッグに役立ちます。
   `GitHub サンプルディレクトリー <https://github.com/ansible/ansible-examples>`_
       Github プロジェクトソースにあるすべての Playbook ファイル
   `Wikipedia YAML 構文の参照 <https://en.wikipedia.org/wiki/YAML>`_
       YAML 構文の適切なガイド
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel and #yaml for YAML specific questions
   `YAML 1.1 仕様 <https://yaml.org/spec/1.1/>`_
       PyYAML および libyaml が、現在実装している YAML 1.1 の仕様
   `YAML 1.2 仕様 <https://yaml.org/spec/1.2/spec.html>`_
        完全を期すため、YAML 1.2 は 1.1 の後継となります。

