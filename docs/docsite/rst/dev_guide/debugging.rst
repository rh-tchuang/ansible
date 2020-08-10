.. _debugging:

*****************
モジュールのデバッグ
*****************

デバッグ (ローカル)
=================

``localhost`` で実行中のモジュールに侵入し、デバッガーを使用してステップを実行するには、以下を行います。

- モジュールにブレークポイントを設定します (``import pdb; pdb.set_trace()``)。
- ローカルマシンでモジュールを実行します (``$ python -m pdb ./my_new_test_module.py ./args.json``)。

以下のようになります。
-------

`echo '{"msg": "hello"}' | python ./my_new_test_module.py`

デバッグ (リモート)
==================

リモートターゲット (つまり ``localhost``ではない) で実行しているモジュールをデバッグするには、以下を実行します。

#.  (Ansible を実行している) コントローラーマシンに ``ansible_KEEP_REMOTE_FILES=1`` を設定して、Playbook の実行後にモジュールを削除するのではなく、リモートマシンに送信するモジュールを保持するように Ansible に指示します。
#. リモートマシンをターゲットにした Playbook を実行し、``-vvvv`` (詳細) を指定して、Ansible がモジュールに使用しているリモートの場所を表示します (他にも多数あります)。
#. Ansible がリモートホスト上のモジュールを保存するために使用したディレクトリーを書き留めます。このディレクトリーは、通常、``ansible_user`` のホームディレクトリの下にあり、``~/.ansible/tmp/ansible-tmp-...`` という形式になっています。
#. Playbook の実行後、リモートターゲットに SSH 接続します。
#. 手順 3 で書き留めたディレクトリーに移動します。
#. Ansible がリモートホストに送信した zip ファイルからデバッグするモジュールを展開します (``$ python AnsiballZ_my_test_module.py explode``)。Ansible はモジュールを ``./debug-dir`` に展開します。任意で ``python AnsiballZ_my_test_module.py`` を指定することで、zip ファイルを実行できます。
#. デバッグディレクトリー ``$ cd debug-dir`` に移動します。
#. ``__main__.py`` のブレークポイントを変更または設定します。
#. 展開したモジュールが実行できることを確認します (``$ chmod 755 __main__.py``)。
#. 展開したモジュールを直接実行し、元々渡されたパラメーターを含む ``args`` ファイルを渡します (``$ ./__main__.py args``)。このアプローチは、動作を再現したり、デバッグ用にパラメーターを変更する場合に適しています。


.. _debugging_ansiblemodule_based_modules:

AnsibleModule ベースのモジュールのデバッグ
=====================================

.. tip::

    :file:`hacking/test-module.py` スクリプトを使用している場合、
    この情報のほとんどはユーザー用に処理されています。 モジュールが実際に実行されるリモートマシン上でモジュールのデバッグを行う必要がある場合や、
    モジュールが Playbook で使用されている場合は、
    :file:`test-module.py` に頼るのではなく、
    この情報を使用しないといけない場合があります。

Ansible 2.1 以降、AnsibleModule ベースのモジュールは、
すべてのコードを連結した単一のファイルではなく、
モジュールファイルとラッパースクリプト内のさまざまな python モジュールのボイラプレートからなる 
zip ファイルとしてまとめられます。 モジュール内で実際に何が起こっているのかを見るためには、
ファイルをラッパースクリプトから抽出する必要があるため、
何か助けがないとデバッグが難しくなります。 ただし、ラッパースクリプトには、
それを行うためのヘルパーメソッドが用意されています。

環境変数 :envvar:`ANSIBLE_KEEP_REMOTE_FILES` 
でリモートモジュールファイルを保持している Ansible を使用している場合は、
デバッグセッションがどのように開始するかを説明するサンプルを以下に示します。

.. code-block:: shell-session

    $ ANSIBLE_KEEP_REMOTE_FILES=1 ansible localhost -m ping -a 'data=debugging_session' -vvv
    <127.0.0.1> ESTABLISH LOCAL CONNECTION FOR USER: badger
    <127.0.0.1> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo $HOME/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595 `" && echo "` echo $HOME/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595 `" )'
    <127.0.0.1> PUT /var/tmp/tmpjdbJ1w TO /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/ping
    <127.0.0.1> EXEC /bin/sh -c 'LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LC_MESSAGES=en_US.UTF-8 /usr/bin/python /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/ping'
    localhost | SUCCESS => {
        "changed": false,
        "invocation": {
            "module_args": {
                "data": "debugging_session"
            },
            "module_name": "ping"
        },
        "ping": "debugging_session"
    }

:envvar:`ANSIBLE_KEEP_REMOTE_FILES` を ``1`` に設定すると、
モジュールの実行終了後に削除するのではなく、
リモートモジュールのファイルを保持するように Ansible に指示します。 Ansible に ``-vvv`` オプションを指定すると、Ansible がより詳細になります。
これにより、一時モジュールファイルのファイル名が出力されます。

ラッパーファイルを検査することもできます。 小規模な python スクリプトと、
大規模で、base64 でエンコードされた文字列を含むスクリプトが表示されます。 この文字列には、
実行されるモジュールが含まれています。 wrapper の explode コマンドを実行して、
この文字列を作業可能な python ファイルに変換してください。

.. code-block:: shell-session

    $ python /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/ping explode
    Module expanded into:
    /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/debug_dir

debug_dir は、以下のようなディレクトリー構造になります。

    ├── ansible_module_ping.py
    ├── args
    └── ansible
        ├── __init__.py
        └── module_utils
            ├── basic.py
            └── __init__.py

* :file:`ansible_module_ping.py` は、モジュール自体のコードです。 名前は、
  他の python モジュール名と競合しないように、
  接頭辞をつけたモジュール名をベースにしています。 このコードを修正して、
  お使いのモジュールにどのような効果があるかを確認できます。

* :file:`args` ファイルには、JSON 文字列が含まれます。 この文字列は、
  モジュールの引数やその他の変数を含む辞書で、
  Ansible がモジュールの挙動を変更するためにモジュールに渡すものです。 モジュールに渡されるパラメーターを変更する場合は、
  このファイルを使用します。

* :file:`ansible` ディレクトリーには、
  モジュールが使用する :mod:`ansible.module_utils` のコードが含まれています。 Ansible には、
  モジュールにインポートされた :mod:`ansible.module_utils` のファイルはすべて含まれますが、
  他のモジュールのファイルは含まれません。 つまり、
  モジュールが :mod:`ansible.module_utils.url` を使用している場合は Ansible に含まれますが、
  モジュールが `requests <http://docs.python-requests.org/en/master/api/>`_ を含んでいる場合は、
  モジュールを実行する前に、python の `requests ライブラリー <https://pypi.org/project/requests/>`_ 
  がシステムにインストールされていることを確認する必要があります。 モジュールが問題を抱えているのは、自身が作成したモジュールのコードではなく、
  このボイラプレートコードの一部であることを疑っている場合は、
  このディレクトリーのファイルを修正できます。

コードや引数を編集したら、
それを実行する方法が必要になります。 これには、別のラッパーサブコマンドがあります。

.. code-block:: shell-session

    $ python /home/badger/.ansible/tmp/ansible-tmp-1461434734.35-235318071810595/ping execute
    {"invocation": {"module_args": {"data": "debugging_session"}}, "changed": false, "ping": "debugging_session"}

このサブコマンドは、
開いた :file:`debug_dir/ansible/module_utils` ディレクトリーを使用するように設定し、
:file:`args` ファイルの引数を使用してスクリプトを起動する処理を行います。 問題が理解できるまで、
このように実行し続けることができます。 その後、このスクリプトを実際のモジュールファイルにコピーして、
実際のモジュールが、:command:`ansible` や、
:command:`ansible-playbook` で動作するかどうかをテストしてください。

.. note::

    ラッパーには、もう一つのサブコマンドである ``excommunicate` が用意されています。 このサブコマンドは、
    :file:`args` に含まれる引数で開いたモジュールを呼び出すという点で、
    ``execute`` と非常によく似ています。 ``excommunicate`` は、
    モジュールから ``main`` 関数をインポートし、
    それを呼び出します。 これにより、
    excommunicate はラッパーのプロセスでモジュールを実行します。 これは、
    いくつかのグラフィカルデバッガの下でモジュールを実行するのに便利かもしれませんが、
    Ansible 自体がモジュールを実行する方法とは大きく異なります。 一部のモジュールは、
    ``excommunicate`` で動作しなかったり、
    Ansible で普通に使用したときとは異なる動作をすることがあります。 これらはモジュールのバグではなく、
    ``excommunicate`` の制限です。 ご自身の責任で使用してください。
