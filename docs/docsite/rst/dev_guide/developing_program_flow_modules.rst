.. _flow_modules:
.. _developing_program_flow_modules:

***************************
Ansible モジュールのアーキテクチャー
***************************

以下の詳細な説明は、Ansible の Core コードで作業している、Ansible モジュールを作成している、またはアクションプラグインを開発している場合に、Ansible のプログラムフローの実行方法を理解するのに役立ちます。Playbook で Ansible Modules を使用しているだけの場合、本セクションは必要ありません。

.. contents::
   :local:

.. _flow_types_of_modules:

モジュールの種類
================

Ansible は、コードベースでいくつかのタイプのモジュールをサポートしています。後方互換性のためのものもあれば、
柔軟性を可能にするためのものもあります。

.. _flow_action_plugins:

アクションプラグイン
--------------

アクションプラグインは、Playbook を作成する人にとってはモジュールのように見えます。ほとんどのアクションプラグインの使用方法に関するドキュメントは、同じ名前のモジュール内にあります。アクションプラグインの中には、すべての作業を行なうものもありますが、このモジュールはドキュメントのみを提供します。一部のアクションプラグインはモジュールを実行します。``normal`` アクションプラグインは、特別なアクションプラグインを持たないモジュールを実行します。アクションプラグインは常にコントローラー上で実行されます。

一部のアクションプラグインは、そのすべての作業をコントローラー上で実行します。たとえば、
:ref:`debug <debug_module>` アクションプラグイン (ユーザーに表示するテキストを出力する) と、
:ref:`assert <assert_module>` アクションプラグイン 
(Playbook の値が特定の基準を満たしているかどうかをテストする) は、そのコントローラー上で完全に実行されます。

ほとんどのアクションプラグインは、コントローラーにいくつかの値を設定してから、
これらの値で何かを行う管理ノードで実際のモジュールを呼び出します。たとえば、:ref:`template <template_module>` アクションプラグインは、
Playbook 環境から変数を使用して、
コントローラーの一時的な場所にファイルを作成するユーザーから値を取得します。その後、この一時ファイルを、
リモートシステムの一時ファイルに転送します。その後、
:ref:`copy module <copy_module>` を呼び出します。
その最後の場所にファイルを異動し、ファイルパーミッションの設定を行います。

.. _flow_new_style_modules:

新スタイルのモジュール
-----------------

Ansible に同梱されるモジュールはすべてこのカテゴリーに分類されます。モジュールは任意の言語で記述できますが、(Ansible に同梱されている) 正式なモジュールはすべて Python または PowerShell を使用します。

新しいスタイルのモジュールは、
何らかの方法でモジュールの内部にモジュールの引数が埋め込まれています。古いスタイルのモジュールは、管理ノードで別のファイルをコピーする必要があります。
ネットワークでは、
接続は 1 つではなく 2 つ必要になるため、効率が悪くなります。

.. _flow_python_modules:

Python
^^^^^^

新しいスタイルの Python モジュールは、
モジュールの構築に :ref:`Ansiballz` フレームワークを使用します。これらのモジュールは、:code:`ansible.module_utils` からのインポートを使用して、
引数の解析や、
:term:`JSON` としての戻り値のフォーマット、さまざまなファイル操作などの boilerplate モジュールコードをプルします。

.. note:: Ansible では、バージョン 2.0.x までの公式の Python モジュールで、
    :ref:`module_replacer` フレームワークが使用されます。 モジュール作成者は、
    :ref:`Ansiballz` は主に :ref: `module_replacer` 機能のスーパーセットであるため、
    通常は両方を理解する必要はありません。

.. _flow_powershell_modules:

PowerShell
^^^^^^^^^^

新しいスタイルの PowerShell モジュールは、
:ref: `module_replacer` フレームワークを使用してモジュールを構築します。これらのモジュールは、管理ノードに送られる前に、
PowerShell コードのライブラリーが埋め込まれています。

.. _flow_jsonargs_modules:

JSONARGS モジュール
----------------

このモジュールは、その本文に、
``<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>`` 文字列を含むスクリプトです。
この文字列は、JSON 形式の引数文字列に置き換えられます。通常、これらのモジュールは以下のような変数をその値に設定します。

.. code-block:: python

    json_arguments = """<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>"""

これは以下のように展開されます。

.. code-block:: python

    json_arguments = """{"param1": "test's quotes", "param2": "\"To be or not to be\" - Hamlet"}"""

.. note:: Ansible は、裸の引用符を使用する :term:`JSON` を出力します。二重引用符は文字列値の引用に使用され、
       文字列値の中の二重引用符はバックスラッシュでエスケープされ、
       単一引用符は、
       文字列値の中でエスケープされていない状態で表示されることがあります。JSONARGS を使用するには、
       スクリプト言語が、このタイプの文字列を処理できなければなりません。この例では、
       Python の三重引用符で囲まれた文字列を使用しています。他のスクリプト言語では、
       JSON の引用符と混同されないような類似の引用符文字が使用されているかもしれません。
       または、独自の引用符開始文字と引用符終了文字を定義できるかもしれません。
       もし言語がこれらを提供していない場合は、
       代わりに :ref:`非ネイティブの JSON モジュール` <flow_want_json_modules>、
       または :ref:`古いスタイルのモジュール <flow_old_style_modules>` を作成する必要があります。

これらのモジュールは通常、JSON ライブラリーを使用して ``json_arguments`` のコンテンツを解析し、
次にコード全体でネイティブ変数として使用します。

.. _flow_want_json_modules:

ネイティブ以外の JSON モジュール
----------------------------

モジュールのどこかに ``WANT_JSON`` という文字列が含まれている場合、
Ansible はそのモジュールを、
唯一のコマンドラインパラメーターとしてファイル名を受け入れる非ネイティブモジュールとして扱います。ファイル名は、
モジュールのパラメーターを含む :term:`JSON` 文字列を含む一時ファイル用です。モジュールは、ファイルを開き、パラメーターを読み込んで解析し、
データを操作し、
その戻り値を JSON にエンコードされたディクショナリーとして標準出力 (stdout) に出力してから終了する必要があります。

これらのタイプのモジュールは自己完結型のエンティティーです。Ansible 2.1 の時点では、
シバンの行がある場合は、Ansible はそれだけを変更します。

.. seealso:: Ruby で書かれた非ネイティブモジュールの例は、「`Ansible 
for Rubyists<https://github.com/ansible/ansible-for-rubyists>`_」リポジトリーから入手できます。

.. _flow_binary_modules:

バイナリーモジュール
--------------

Ansible 2.2 以降、モジュールは小規模のバイナリープログラムになる場合があります。Ansible には、
これらを異なるシステムに移植できるようにするな機能がないため、
コンパイルされたシステムに固有のものであったり、
その他のバイナリー実行時の依存関係を必要としたりすることがあります。このような欠点があるにもかかわらず、
特定のリソースにアクセスするための唯一の方法であるならば、
特定のバイナリーライブラリーに対してカスタムモジュールのコンパイルが必要になる場合があります。

バイナリーモジュールは引数を取り、
「:ref:`want JSON モジュール <flow_want_json_modules>`」と同じ方法で Ansible にデータを返します。

.. seealso:: Go で書かれた `バイナリーモジュール
    <https://github.com/ansible/ansible/blob/devel/test/integration/targets/binary_modules/library/helloworld.go>`_ 
の一例

.. _flow_old_style_modules:

古いスタイルのモジュール
-----------------

古いスタイルのモジュールは、
:ref:`want JSON モジュール <flow_want_json_modules>` と似ていますが、
取得するファイルには、
:term:`JSON` の代わりにパラメーターの ``key=value`` ペアが含まれています。Ansible は、モジュールに、他のタイプのいずれかであることを示すマーカーがない場合に、
そのモジュールが古いスタイルであると判断します。

.. _flow_how_modules_are_executed:

モジュールの実行方法
========================

:program:`ansible` または :program:`ansible-playbook` を使用する場合は、
実行するタスクを指定します。タスクは通常、
モジュールの名前と、モジュールに渡すいくつかのパラメーターを指定します。Ansible はこれらの値を受け取り、
さまざまな方法で処理した後、
最終的にリモートマシン上で実行されます。

.. _flow_executor_task_executor:

Executor/task_executor
----------------------

TaskExecutor は、
:term:`playbook <playbooks>` 
:command:`/usr/bin/ansible` の場合はコマンドライン) から解析されたモジュール名およびパラメーターを受け取ります。この名前を使用して、
モジュールを見ているのか :ref:`アクションプラグイン <flow_action_plugins>` を見ているのかを判断します。モジュールであれば、
:ref:`normal アクションプラグイン <flow_normal_action_plugin>` を読み込み、
名前や変数、
およびタスクやプレイに関するその他の情報をそのアクションプラグインに渡して、さらに処理を行います。

.. _flow_normal_action_plugin:

``通常`` のアクションプラグイン
----------------------------

``通常`` アクションプラグインはリモートホスト上でモジュールを実行します。これは、
管理マシンで、
モジュールを実際に実行するタスクの多くの作業に対する主要な調整役です。

* タスクに適切な接続プラグインを読み込み、
  そのホストへの接続を作成するために必要に応じて転送や実行を行います。
* モジュールのパラメーターに、
  Ansible の内部プロパティーを追加します (たとえば ``no_log`` をモジュールに渡すものなど)。
* その他のプラグイン (接続、シェル、become、
  その他のアクションプラグイン) と連携してリモートマシン上に一時ファイルを作成し、
  その後のクリーンアップを行います。
* モジュールとモジュールパラメーターをリモートホストにプッシュしますが、
  次のセクションで説明する :ref:`module_common <flow_executor_module_common>` 
  コードが
  どの形式を取るかを判断します。
* モジュールに関する特殊なケースを処理します (たとえば、
  非同期実行や、Python モジュールと同じ名前を持たなければならない Windows モジュールの複雑さなど。これにより、他のアクションプラグインからのモジュールの内部呼び出しが機能します)。

この機能の多くは、
:file:`plugins/action/__init__.py` にある `BaseAction` クラスから来ています。これは、
``Connection`` オブジェクトおよび ``Shell`` オブジェクトを使用して動作します。

.. note::
    :term:`タスク` <tasks>が ``async:`` パラメーターで実行されると、
    Ansible は ``normal`` アクションプラグインではなく、
    ``async`` を使用してタスクを呼び出します。そのプログラムフローは現在のところ文書化されていません。仕組みについては、
    情報源を参照してください。

.. _flow_executor_module_common:

Executor/module_common.py
-------------------------

:file:`executor/module_common.py` のコードは、
管理ノードに出荷されるモジュールを組み立てます。モジュールは最初に読み込まれ、
その後、その型を調べるために検査されます。

* :ref:`PowerShell <flow_powershell_modules>` および :ref:`JSON-args モジュール <flow_jsonargs_modules>` は、:ref:`Module Replacer <module_replacer>` に渡されます。
* 新しいスタイルの :ref:`Python モジュール <flow_python_modules>` は、:ref:`Ansiballz` により組み立てられます。
* :ref:`Non-native-want-JSON <flow_want_json_modules>`、:ref:`バイナリーモジュール <flow_binary_modules>`、および :ref:`古いスタイルのモジュール <flow_old_style_modules>` は、これらのいずれにも触れられず、そのまま通過します。

アセンブルステップの後、
シバン行を持つすべてのモジュールに対して最終的な修正を行います。Ansible は、
シバン行にあるインタープリターが特定のパスを持っているかどうかを、
``ansible_$X_interpreter`` インベントリー変数で確認します。特定のパスが設定されている場合、
Ansible はそのパスをモジュールで指定されたインタープリターのパスに置き換えます。この後、
Ansible はモジュールの完全なデータとモジュールタイプを 
:ref:`Normal Action <flow_normal_action_plugin>` に返し、
モジュールの実行を継続します。

アセンブラーフレームワーク
--------------------

Ansible は、2 つのアセンブラフレームワーク (Ansiballz と古い Module Replacer) をサポートしています。

.. _module_replacer:

Module Replacer フレームワーク
^^^^^^^^^^^^^^^^^^^^^^^^^

Module Replacer フレームワークは、
新しいスタイルのモジュールを実装したオリジナルのフレームワークで、今でも PowerShell モジュールに使用されています。これは、
基本的にはプリプロセッサーです (プログラミング言語に精通している人向けの C プロセッサーのようなもの)。モジュールファイルの中で、
特定の部分文字列パターンの直接の置換を行います。置換には、
2 つの種類があります。

* モジュールファイル内でのみ行われる置換。これは、
  モジュールが有用なボイラプレートを取得したり、
  引数にアクセスするために利用できるパブリックな置換文字列です。

  - :code:`from ansible.module_utils.MOD_LIB_NAME import *` は、
    :file:`ansible/module_utils/MOD_LIB_NAME.py` の内容に置き換えられます。
    これは、:ref:`新しいスタイルの Python モジュール <flow_python_modules>` でのみ使用してください。
  - :code:`#<<INCLUDE_ANSIBLE_MODULE_COMMON>>` は、
    :code:`from ansible.module_utils.basic import *` と同等であり、
    新しいスタイルの Python モジュールにのみ適用されます。
  - :code:`# POWERSHELL_COMMON` は、
    :file:`ansible/module_utils/powershell.ps1` の内容を置き換えます。これは、
    :ref:`新しいスタイルの Powershell モジュール <flow_powershell_modules>` でのみ使用してください。

* ``ansible.module_utils`` のコードで使用される置換です。これらは内部的な置換パターンです。これらは内部的には上記のパブリックな置換で使用できますが、モジュールでは直接使用しないでください。

  - :code:`"<<ANSIBLE_VERSION>>"` は Ansible のバージョンで置き換えられます。 :ref:`Ansiballz` フレームワークの
    :ref:`新しいスタイルの Python モジュール <flow_python_modules>` では、
    代わりに 
    `AnsibleModule`をインスタンス化し、
    :attr:``AnsibleModule.ansible_version`` からバージョンにアクセスするのが適切な方法です。
  - :code:`"<<INCLUDE_ANSIBLE_MODULE_COMPLEX_ARGS>>"` は、
    :term:`JSON` エンコードされたモジュールパラメーターの Python ``repr`` 
    である文字列で置き換えられます。JSON 文字列に ``repr`` を使用することで、
    Python ファイルに埋め込むことが安全になります。Ansiballz フレームワークの新しいスタイルの Python モジュールでは、
    `AnsibleModule` のインスタンスを作成し、
    :attr:`AnsibleModule.params` を使用することでアクセスする方が適しています。
  - :code:`<<SELINUX_SPECIAL_FILESYSTEMS>>` は、
    SELinux で、
    ファイルシステム依存のセキュリティーコンテキストを持つファイルシステムのコンマ区切りのリストである文字列に置換します。新しいスタイルの Python モジュールでは、
    これが本当に必要な場合は `AnsibleModule`をインスタンス化して、
    :attr:`AnsibleModule._selinux_special_fs` を使用してください。また、
    この変数は、ファイルシステム名をコンマで区切った文字列から、
    実際の Python のファイルシステム名のリストに変更になりました。
  - :code:`<<INCLUDE_ANSIBLE_MODULE_JSON_ARGS>>` は、
    モジュールのパラメーターを JSON 文字列に置き換えます。JSON データには引用符が含まれている可能性があるため、
    文字列を適切に引用符で囲むように注意する必要があります。新しいスタイルの Python モジュールでは、
    モジュールのパラメーターは別の方法で取得できるため、
    このパターンは代用されません。
  - 文字列 :code:`syslog.LOG_USER` は、
    :file:`ansible.cfg` や、
    ``ansible_syslog_facility`` のインベントリー変数で指定された ``syslog_facility`` に置き換えられます。 新しいスタイルの Paython モジュールでは、
    これは少し変更になっています。本当にアクセスする必要がある場合は、
    `AnsibleModule` をインスタンス化してから、
    :attr:`AnsibleModule._syslog_facility` を使用してアクセスする必要があります。これは実際の syslog ファシリティーではなく、
    その syslog ファシリティの名前になりました。詳細は、
    「:ref:`内部引数のドキュメント <flow_internal_arguments>`」
    を参照してください。

.. _Ansiballz:

Ansiballz フレームワーク
^^^^^^^^^^^^^^^^^^^

Ansiballz フレームワークは Ansible 2.1 で採用され、すべての新しいスタイルの Python モジュールで使用されています。Module Replacer とは異なり、Ansiballz は、
単にモジュールを前処理するのではなく、:file:`ansible/module_utils` にあるものを実際の Python インポートして使用します。これは、
モジュールファイル、
モジュールによってインポートされた :file:`ansible/module_utils` 内のファイル、
モジュールのパラメーターを渡す boilerplate を含む zip ファイルを作成することによって行われます。この zipfile は Base64 でエンコードされ、
小規模の Python スクリプトでラップされ、
Base64 エンコードをデコードして管理ノードの temp ディレクトリーに置きます。次に、
zip ファイルから Ansible モジュールのスクリプトだけを抽出し、
それを一時ディレクトリーに置きます。PYTHONPATH を設定して zip ファイル内の Python モジュールを探し、
Ansible モジュールを ``__main__`` という特別な名前でインポートします。
これを ``__main__`` としてインポートすることで、Python は単にモジュールをインポートするのではなく、
スクリプトを実行していると考えるようになります。これにより、Ansible はラッパースクリプトとモジュールコードの両方を、リモートマシンにある Python のコピーで実行できます。

.. note::
    * Ansible が Python スクリプトで zip ファイルをラップするには、以下の 2 つの理由があります。

        * Python の ``-m`` コマンドラインスイッチの機能が少ない 
          Python 2.6 との互換性のため。

        * パイプラインが正しく機能するようにするため。パイプラインは、
          Python モジュールをリモートノードの Python インタープリターにパイプする必要があります。Python
          Python は標準出力 (stdin) 上のスクリプトは理解できますが、zip ファイルは理解できません。

    * Ansible 2.7 より前のバージョンでは、モジュールは同じプロセス内で実行するのではなく、
      2 つ目の Python インタープリターを介して実行していました。この変更は、
      モジュールの実行を高速化するために Python-2.4 のサポートが削除された後に行われました。

Ansiballz では、
:py:mod:`ansible.module_utils` パッケージから Python モジュールをインポートすると、
その Python ファイルが zip ファイルに含まれるようになります。モジュールの :code:`#<<INCLUDE_ANSIBLE_MODULE_COMMON>>` のインスタンスは 
:code:`from ansible.module_utils.basic import *` に変換され、
次に、:file:`ansible/module-utils/basic.py` が zip ファイルにインクルードされます。
:file:`module_utils` に含まれているファイルは、
:file:`module_utils` から他の Python モジュールがインポートされているかどうかをスキャンし、
同様に zip ファイルににインポートされます。

.. warning::
    現在、Ansiballz フレームワークでは、
    インポートが相対インポートの場合に、インポートを含めるべきかどうかを判断することができません。Ansiballz がファイルを含めるべきかどうかを判断できるように、
    :py:mod:`ansible.module_utils` 
    を含む絶対インポートを使用してください。


.. _flow_passing_module_args:

引数を渡す
------------

以下の 2 つのフレームワークでは、引数の渡し方が異なります。

* :ref:`module_replacer` では、モジュールの引数は JSON 化された文字列に変換され、結合されたモジュールファイルに置き換えられます。
* :ref:`Ansiballz` では、JSON 化された文字列は zip ファイルをラップするスクリプトに含まれますが、ラッパースクリプトは Ansible モジュールを ``__main__`` としてインポートする直前に、``basic.py`` のプライベート変数 ``_ANSIBLE_ARGS`` に変数値をモンキーパッチします。:class:`ansible.module_utils.basic.AnsibleModule` がインスタンス化されると、この文字列を解析して :attr:`AnsibleModule.params` に配置し、モジュールの他のコードからアクセスできるようにします。

.. warning::
    モジュールを記述する場合、引数の渡し方は内部的な実装の詳細であることを覚えておいてください。
    過去に変更されていますが、共通の module_utils コードが変更されて Ansible モジュールが :class:`ansible.module_utils.basic.AnsibleModule` の使用を見送ることができるようになると、すぐにまた変更されるでしょう。内部のグローバル変数 ``_ANSIBLE_ARGS`` に使用しないようにしてください。

    ``AnsibleModule`` をインスタンス化する前に引数を解析する必要がある非常に動的なカスタムモジュールでは、
    ``_load_params``を使用してパラメーターを取得することがあります。
    ``_load_params`` はコードの変更に対応するために必要に応じて変更されることがありますが、パラメーターを渡す方法や内部グローバル変数よりも安定している可能性があります。
    サポートが必要な場合は、``_load_params`` が破損した方法で変更する可能性があります。

.. note::
    Ansible 2.7 より前のバージョンでは、Ansible モジュールは 2 番目の Python インタープリターで呼び出され、
    引数はスクリプトの標準入力 (stdin) を介してスクリプトに渡されていました。


.. _flow_internal_arguments:

内部引数
------------------

:ref:`module_replacer` および :ref:`Ansiballz` は両方とも、
Playbook でユーザーが指定した以上の追加引数をモジュールに送ります。これらの追加引数は、
Ansible 
のグローバルな機能を実装するのに役立つ内部パラメータです。機能は :py:mod:`ansible.module_utils.basic` で実装されているため、
モジュールはこれらを明示的に知る必要はないことは少なくありませんが、
特定の機能にはモジュールのサポートが必要になるため、知ることは良いことです。

ここに記載されている内部引数はグローバルです。カスタムモジュールにローカルの内部引数を追加する必要がある場合は、その特定のモジュール用のアクションプラグインを作成してください。例は、「`copy action plugin <https://github.com/ansible/ansible/blob/devel/lib/ansible/plugins/action/copy.py#L329>`_」の「``_original_basename``」を参照してください。

_ansible_no_log
^^^^^^^^^^^^^^^

ブール値です。タスクやプレイのパラメーターで ``no_log`` が指定されている場合は常に True に設定します。:py:meth:`AnsibleModule.log` を呼び出すモジュールがこれを自動的に処理します。モジュールが独自のロギングを実装している場合は、
この値を確認する必要があります。モジュール内でアクセスするには、
``AnsibleModule`` をインスタンス化してから :attr:`AnsibleModule.no_log` の値をチェックします。

.. note::
    モジュールの argument_spec で指定された ``no_log`` は別のメカニズムで処理されます。

_ansible_debug
^^^^^^^^^^^^^^^

ブール値です。より詳細なログをオンまたはオフにし、
モジュールが実行する外部コマンドのログをオンにします。モジュールが 
:py:meth:`AnsibleModule.log` ではなく :py:meth:`AnsibleModule.debug` を使用している場合は、
``_ansible_debug`` が ``True`` に設定されている場合にのみメッセージがログに記録されます。
設定するには、``debug: True`` を :file:`ansible.cfg` に追加するか、
環境変数 :envvar:`ANSIBLE_DEBUG` を設定してください。モジュール内でアクセスするには、
``AnsibleModule`` をインスタンス化して :attr:`AnsibleModule._debug` にアクセスします。

_ansible_diff
^^^^^^^^^^^^^^^

ブール値です。モジュールがこれをサポートしている場合は、
テンプレート化されたファイルに加えられる変更の統一された diff を表示するようにモジュールに指示します。これを設定するには、
コマンドラインオプション ``--diff`` を渡します。モジュール内でアクセスするには、`AnsibleModule` をインスタンス化して、
:attr:`AnsibleModule._diff` にアクセスします。

_ansible_verbosity
^^^^^^^^^^^^^^^^^^

使用されていません。この値は、ログをより細かく制御するために使用できます。

_ansible_selinux_special_fs
^^^^^^^^^^^^^^^^^^^^^^^^^^^

リストです。特別な SELinux 
コンテキストを持つべきファイルシステムの名前。これは、ファイルを操作する `AnsibleModule` メソッド 
(属性の変更、移動、およびコピー) で使用されます。これを設定するには、:file:`ansible.cfg` にファイルシステム名のコンマ区切りの文字列を追加します。

  # ansible.cfg
  [selinux]
  special_context_filesystems=nfs,vboxsf,fuse,ramfs,vfat

ほとんどのモジュールでは、
組み込みの ``AnsibleModule`` メソッドを使用してファイルを操作することができます。この特殊なコンテキストファイルシステムについて知る必要があるモジュールでアクセスするには、``AnsibleModule`` をインスタンス化して、
:attr:`AnsibleModule._selinux_special_fs` のリストを調べます。

これは、
:ref:`module_replacer` の :attr:`ansible.module_utils.basic.SELINUX_SPECIAL_FS` を置き換えたものです。モジュールリプレッサーでは、
これは、ファイルシステム名をコンマで区切った文字列でした。Ansiballz では実際のリストになります。

.. versionadded:: 2.1

_ansible_syslog_facility
^^^^^^^^^^^^^^^^^^^^^^^^

このパラメーターは、Ansible モジュールがどの syslog ファシリティーにログを記録するかを制御します。これを設定するには、:file:`ansible.cfg` の ``syslog_facility`` の値を変更します。ほとんどのモジュールは、
:meth:`AnsibleModule.log` を使用するだけで、
これを使用するようになります。モジュールが独自にこれを使用しなければならない場合は、
`AnsibleModule` をインスタンス化し、
:attr:`AnsibleModule._syslog_facility` から syslog ファシリティーの名前を取得する必要があります。Ansiballz のコードは、:ref:`module_replacer` コードよりも洗練されています。

.. code-block:: python

        # Old module_replacer way
        import syslog
        syslog.openlog(NAME, 0, syslog.LOG_USER)

        # New Ansiballz way
        import syslog
        facility_name = module._syslog_facility
        facility = getattr(syslog, facility_name, syslog.LOG_USER)
        syslog.openlog(NAME, 0, facility)

.. versionadded:: 2.1

_ansible_version
^^^^^^^^^^^^^^^^

このパラメーターには、モジュールを実行する Ansible のバージョンを渡します。これにアクセスするために、
モジュールは `AnsibleModule` をインスタンス化してから、
それを :attr:`AnsibleModule.ansible_version` から取得する必要があります。これは、
:ref:`module_replacer` の 
:attr:`ansible.module_utils.basic.ANSIBLE_VERSION` を置き換えるものです。

.. versionadded:: 2.1


.. _flow_module_return_values:

モジュール戻り値と安全でない文字列
-------------------------------------

モジュールの実行の最後に、返したいデータを JSON 文字列としてフォーマットし、その文字列を標準出力 (stdout) に出力します。normal アクションプラグインは JSON 文字列を受け取り、Python ディクショナリーに解析してエクゼキューターに返します。

Ansible がすべての文字列の戻り値をテンプレート化した場合は、管理ノードにアクセスできるユーザーからの攻撃に対して脆弱になります。悪意のあるユーザーが悪意のあるコードを Ansible の戻り値の文字列として偽装し、それらの文字列がコントローラー上でテンプレート化されると、Ansible が任意のコードを実行する可能性があります。このシナリオを防ぐために、Ansible では、返されたデータ内のすべての文字列を ``Unsafe`` としてマークし、文字列内の Jinja2 テンプレートをすべてそのまま出力し、Jinja2 によって展開されないようにしています

``ActionPlugin._execute_module()`` を介してモジュールを呼び出して返された文字列には、normal アクションプラグインによって自動的に ``Unsafe`` というマークが付きます。別のアクションプラグインが他の方法でモジュールから情報を取得した場合は、そのアクションプラグイン自身がその戻り値に ``Unsafe`` マークを付ける必要があります。

コード化が不十分なアクションプラグインが結果を「安全でない」とすることに失敗すると、
Ansible は結果がエクゼキューターに返されたときに結果を再監査し、すべての文字列に ``Unsafe`` マークを付けます。normal アクションプラグインは、自分自身と、結果データをパラメーターとして呼び出す他のコードを保護します。エクゼキューター内のチェックは、他のすべてのアクションプラグインの出力を保護し、Ansible によって実行された後続のタスクがこれらの結果から何かをテンプレート化することがないようにします。

.. _flow_special_considerations:

特別な考慮事項
----------------------

.. _flow_pipelining:

パイプライン
^^^^^^^^^^

Ansible は、以下のいずれかの方法で、モジュールをリモートマシンに転送できます。

* リモートホスト上の一時ファイルにモジュールを書き出し、
  リモートホストへの第二の接続を使用して、
  モジュールが必要とするインタープリターで実行する方法です。
* あるいは、
  リモートインタープリターの標準入力 (stdin) にパイプしてモジュールを実行する、パイプライン化と呼ばれる方法を使用することもできます。

パイプラインは現時点では Python で書かれたモジュールでしか動作しません。
これは、Python のみがこの操作モードをサポートしていると Ansible が認識しているためです。パイプラインをサポートしているということは、
モジュールのペイロードがどのような形式であっても、
stdin を介して Python で実行できなければならないということを意味します。

.. _flow_args_over_stdin:

標準入力 (stdin) で引数を渡す理由
^^^^^^^^^^^^^^^^^^^^^^^^^

以下の理由により、stdin で引数を渡すことが選択されました。

* :ref:`ANSIBLE_PIPELINING` と組み合わせることで、
  モジュールの引数が一時的にリモートマシンのディスクに保存されることを防ぎます。これにより、
  リモートマシン上で悪意のあるユーザーが、
  引数に存在する可能性のある機密情報を盗むことが難しくなります (ただし不可能ではありません)。
* ほとんどのシステムでは、
  権限のないユーザーがプロセスのコマンドライン全体を読むことを許可されているため、コマンドライン引数は安全ではありません。
* 通常、環境変数は、コマンドラインよりも安全ですが、
  システムによっては環境の合計サイズを制限しています。その制限を超えると、
  パラメーターが切り捨てられてしまう可能性があります。


.. _flow_ansiblemodule:

AnsibleModule
-------------

.. _argument_spec:

引数の仕様
^^^^^^^^^^^^^

``AnsibleModule`` に提供される ``argument_spec`` は、モジュールでサポートされる引数、その型、デフォルトなどを定義します。

``argument_spec`` の例：

.. code-block:: python

    module = AnsibleModule(argument_spec=dict(
        top_level=dict(
            type='dict',
            options=dict(
                second_level=dict(
                    default=True,
                    type='bool',
                )
            )
        )
    ))

本セクションでは、引数の動作属性を説明します。

type
""""

``type`` では、引数に受け入れられる値の型を定義できます。``type`` のデフォルト値は ``str`` です。以下の値が使用できます。

* str
* list
* dict
* bool
* int
* float
* path
* raw
* jsonarg
* json
* bytes
* bits

``raw`` 型で、型の検証や型のケーシングを行わず、渡された値の型を保持します。

elements
""""""""

``elements`` は、``type='list'`` の時に ``type`` と組み合わせて動作します。``elements`` は ``elements='int'`` などの型で定義することができ、指定されたリストの各要素がその型であることを示します。

default
"""""""

``default`` オプションは、引数がモジュールに提供されていない場合のシナリオの引数のデフォルト値を設定します。指定されていない場合、デフォルト値は ``None`` です。

fallback
""""""""

``fallback`` は、第 1 引数に、第 2 引数に基づいて検索を実行するために使用される callable (関数) の ``タプル`` を受け入れます。2 つ目の引数は、呼び出し可能な値のリストを指定します。

最も一般的に使用されている callable は ``env_fallback`` で、これは引数に環境変数が与えられていない場合に任意で環境変数を使用できるようにします。

例:

    username=dict(fallback=(env_fallback, ['ANSIBLE_NET_USERNAME']))

choices
"""""""

``choice`` は、引数が受け入れる選択肢のリストを受け入れます。``choices`` の型は、``type`` と一致している必要があります。

required
""""""""

``required`` には、引数が必要であることを示すブール値 (``True`` または ``False``) を使用できます。これは ``default`` と組み合わせて使用しないでください。

no_log
""""""

``no_log`` には、引数の値がログや出力でマスクされるべきかどうかを明示的に示すブール値 (``True`` または ``False``) を使用できます。

.. note::
   ``no_log`` がない場合は、パラメーター名が、引数の値がパスワードやパスフレーズであることを示しているように見える場合 (「admin_password」など)、警告が表示され、値はログでマスクされますが、**出力されません**。機密情報を含まないパラメーターの警告とマスクを無効にするには、``no_log`` を ``False`` に設定します。

aliases
"""""""

``aliases`` では、引数の代替引数名のリストが使用できます。たとえば、引数が ``name`` ですが、モジュールが ``aliases=['pkg']`` を受け付けて、``pkg`` を ``name`` と互換性を持たせるようにしています。

options
"""""""

``options`` では、トップレベル引数のサブオプションもこのセクションで説明した属性を使用して検証される sub-argument_spec を作成する機能を実装しています。このセクションの先頭にある例は、``options`` の使用を示しています。ここでは、``type`` または ``elements`` は ``dict`` である必要があります。

apply_defaults
""""""""""""""

``apply_defaults`` は ``options`` と並んで動作し、トップレベルの引数が指定されていない場合でもサブオプションの ``デフォルト`` を適用できるようにします。

このセクションの先頭にある ``argument_spec`` の例では、ユーザーがモジュールを呼び出すときに ``top_level`` を指定しなかった場合でも、``module.params['top_level']['second_level']`` を定義できるようにします。

removed_in_version
""""""""""""""""""

``removed_in_version`` は、非推奨の引数が削除される Ansible のバージョンを示します。
