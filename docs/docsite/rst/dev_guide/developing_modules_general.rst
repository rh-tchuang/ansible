.. _developing_modules_general:
.. _module_dev_tutorial_sample:

*******************************************
Ansible モジュールの開発: はじめに
*******************************************

モジュールは、ローカルまたはリモートで Ansible を実行する再利用可能なスタンドアロンスクリプトです。モジュールは、ローカルマシン、API、またはリモートシステムと対話し、データベースパスワードの変更やクラウドインスタンスの起動などの特定のタスクを実行します。各モジュールは、Ansible API または :command:`ansible` または :command:`ansible-playbook` のプログラムで使用できます。モジュールは定義されたインターフェースを提供し、引数を受け入れ、終了前に JSON 文字列を標準出力 (stdout) に出力して Ansible に情報を返します。Ansible には数千ものモジュールが同梱されているため、簡単に独自のモジュールを作成できます。ローカルで使用するためにモジュールを作成する場合は、任意のプログラミング言語を選択して、独自のルールに従います。このチュートリアルでは、Python で Ansible モジュールの開発を開始する方法を説明します。

.. contents:: トピック
   :local:

.. _environment_setup:

環境の設定
=================

apt (Ubuntu) による前提条件
------------------------------

依存関係のため (例: ansible -> paramiko -> pynacl -> libffi)。

.. code:: bash

    sudo apt update
    sudo apt install build-essential libssl-dev libffi-dev python-dev

一般的な環境設定
------------------------------

1. Ansible リポジトリーのクローンを作成します 
   (``$ git clone https://github.com/ansible/ansible.git``)。
2. ディレクトリーをリポジトリーの root ディレクトリーに変更します (``$ cd ansible``)。
3. 仮想環境を作成します (``$ python3 -m venv venv`` 
   (または Python 2 ``$ virtualenv venv`` の場合))。注記: これには、
   virtualenv パッケージインストール (``$ pip install virtualenv``) する必要がある点に注意してください。
4. 仮想環境をアクティベートします (``$ . venv/bin/activate``)。
5. 開発要件をインストールします 
   (``$ pip install -r requirements.txt``)。
6. 新規 dev シェルプロセスごとに環境設定スクリプトを実行します 
   (``$ . hacking/env-setup``)。

.. note:: 上記の初期設定後、
   Ansible の開発を開始する準備ができるたびに、
   Ansibleリポジトリのルートから次のコマンドを実行できるようになります 
   (``$ . venv/bin/activate && . hacking/env-setup``)。


新規モジュールの起動
=====================

新しいモジュールを作成するには、以下を行います。

1. 新しいモジュールの適切なディレクトリーに移動します (``$ cd lib/ansible/modules/cloud/azure/``)。
2. 新しいモジュールファイルを作成します (``$ touch my_test.py``)。
3. 以下の内容を新しいモジュールファイルに貼り付けます。:ref:`必要な Ansible 形式およびドキュメント <developing_modules_documenting>` と、いくつかのサンプルコードが含まれます。
4. コードを変更および拡張して、新しいモジュールで実行すべきことを実行します。適切で簡潔なモジュールコードを記述するヒントは、「:ref:`プログラミングのヒント <developing_modules_best_practices>`」および「:ref:`Python 3 の互換性 <developing_python_3>`」を参照してください。

.. code-block:: python

    #!/usr/bin/python

    # Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
    # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

    ANSIBLE_METADATA = {
        'metadata_version': '1.1',
        'status': ['preview'],
        'supported_by': 'community'
    }

    DOCUMENTATION = '''
    ---
    module: my_test

    short_description: This is my test module

    version_added: "2.4"

    description:
        - "This is my longer description explaining my test module"

    options:
        name:
            description:
                - This is the message to send to the test module
            required: true
        new:
            description:
                - Control to demo if the result of this module is changed or not
            required: false

    extends_documentation_fragment:
        - azure

    author:
        - Your Name (@yourhandle)
    '''

    EXAMPLES = '''
    # Pass in a message
    - name: Test with a message
      my_test:
        name: hello world

    # pass in a message and have changed true
    - name: Test with a message and changed output
      my_test:
        name: hello world
        new: true

    # fail the module
    - name: Test failure of the module
      my_test:
        name: fail me
    '''

    RETURN = '''
    original_message:
        description: The original name param that was passed in
        type: str
        returned: always
    message:
        description: The output message that the test module generates
        type: str
        returned: always
    '''

    from ansible.module_utils.basic import AnsibleModule

    def run_module():
        # define available arguments/parameters a user can pass to the module
        module_args = dict(
            name=dict(type='str', required=True),
            new=dict(type='bool', required=False, default=False)
        )

        # seed the result dict in the object
        # we primarily care about changed and state
        # change is if this module effectively modified the target
        # state will include any data that you want your module to pass back
        # for consumption, for example, in a subsequent task
        result = dict(
            changed=False,
            original_message='',
            message=''
        )

        # the AnsibleModule object will be our abstraction working with Ansible
        # this includes instantiation, a couple of common attr would be the
        # args/params passed to the execution, as well as if the module
        # supports check mode
        module = AnsibleModule(
            argument_spec=module_args,
            supports_check_mode=True
        )

        # if the user is working with this module in only check mode we do not
        # want to make any changes to the environment, just return the current
        # state with no modifications
        if module.check_mode:
            module.exit_json(**result)

        # manipulate or modify the state as needed (this is going to be the
        # part where your module will do what it needs to do)
        result['original_message'] = module.params['name']
        result['message'] = 'goodbye'

        # use whatever logic you need to determine whether or not this module
        # made any modifications to your target
        if module.params['new']:
            result['changed'] = True

        # during the execution of the module, if there is an exception or a
        # conditional state that effectively causes a failure, run
        # AnsibleModule.fail_json() to pass in the message and the result
        if module.params['name'] == 'fail me':
            module.fail_json(msg='You requested this to fail', **result)

        # in the event of a successful module execution, you will want to
        # simple AnsibleModule.exit_json(), passing the key/value results
        module.exit_json(**result)

    def main():
        run_module()

    if __name__ == '__main__':
        main()


モジュールコードを試す
===========================

上記のサンプルコードを修正したら、モジュールを試すことができます。
:ref:`デバッグのヒント<debugging>` は、モジュールコードを実行中にバグが発生した場合に役立ちます。

モジュールコードをローカルで試す
------------------------------

モジュールがリモートホストを対象にする必要がない場合は、以下のようにコードをローカルで簡単に使用できます。

-  パラメーターをモジュールに渡す基本的な JSON 設定ファイルである引数ファイルを作成して、これを実行できます。引数ファイル ``/tmp/args.json`` に名前を付け、以下の内容を追加します。

.. code:: json

    {
        "ANSIBLE_MODULE_ARGS": {
            "name": "hello",
            "new": true
        }
    }

-  仮想環境を使用している場合 (開発には強く推奨されます) は、
   それをアクティブにします。(``$ . venv/bin/activate``)。
-  開発用の環境を設定します (``$ . hacking/env-setup``)。
-  テストモジュールをローカルで直接実行します。
   ``$ python -m ansible.modules.cloud.azure.my_test /tmp/args.json``

これにより、以下のような出力が返されます。

.. code:: json

    {"changed": true, "state": {"original_message": "hello", "new_message": "goodbye"}, "invocation": {"module_args": {"name": "hello", "new": true}}}


Playbook でのモジュールコードを試す
------------------------------------

新規モジュールをテストする次のステップは、Ansible Playbook で使用します。

-  任意のディレクトリーに Playbook を作成します (``$ touch testmod.yml``)。
-  以下を新しい Playbook ファイルに追加します。

    - name: test my new module
      hosts: localhost
      tasks:
      - name: run the new module
        my_test:
          name: 'hello'
          new: true
        register: testout
      - name: dump test output
        debug:
          msg: '{{ testout }}'

- Playbook を実行し、出力を分析します (``$ ansible-playbook ./testmod.yml``)。

基本テスト
====================

これら 2 つの例では、モジュールコードのテストを開始します。:ref:`モジュールドキュメントのテスト <testing_module_documentation>`、:ref:`統合テスト <testing_integration>` の追加などの詳細は、
「:ref:`testing <developing_testing>`」セクションを参照してください。

健全性テスト
------------

Ansible の健全性チェックをコンテナーで実行できます。

``$ ansible-test sanity -v --docker --python 2.7 MODULE_NAME``

この例では Docker をインストールし、実行している必要があることに注意してください。コンテナーを使用しない場合は、
``--docker`` の代わりに ``--tox`` を使用できます。

ユニットテスト
----------

モジュールのユニットテストは、``./test/units/modules`` に追加できます。最初にテスト環境を設定する必要があります。この例では、Python 3.5 を使用しています。

- (仮想環境外に) 要件をインストールします (``$ pip3 install -r ./test/lib/ansible_test/_data/requirements/units.txt``)。
- すべてのテストを実行するには、$ ansible-test units --python 3.5`` を実行します (この前に ``. hacking/env-setup`` を実行する必要があります)。

.. note:: Ansible はユニットテストに pytest を使用します。

1 つのテストモジュールに対して pytest を実行するには、以下を行います (テストモジュールへのパスを適切に提供します)。

``$ pytest -r a --cov=. --cov-report=html --fulltrace --color yes
test/units/modules/.../test/my_test.py``

Ansible への貢献
============================

新しい機能の追加や、バグの修正など、メインの Ansible リポジトリーに貢献する場合は、
Ansible リポジトリーの `フォークを作成 <https://help.github.com/articles/fork-a-repo/>`_ し、
新機能に対して開発します。
``devel`` ブランチを出発点として新しい機能ブランチに対して開発します。
正常に機能するコードを変更したら、
機能ブランチをソースとして、
および Ansible devel ブランチをターゲットとして選択して、
プル要求を Ansible リポジトリーに送信できます。

モジュールをアップストリームの Ansible リポジトリーに提供するには、プル要求を作成する前に、
「:ref:`提出のチェックリスト <developing_modules_checklist>`」、「:ref:`プログラミングのヒント <developing_modules_best_practices>`」、
「:ref:`Python 2 および Python 3 の互換性を維持するための戦略 <developing_python_3>`」、
および「:ref:`テスト <developing_testing>`」を確認します。
:ref:`コミュニティーガイド <ansible_community_guide>` では、プル要求を作成する方法と、作成した後のプロセスを説明します。


通信および開発のサポート
=====================================

Ansible 開発に関するディスカッションは、freenode の IRCチャネル ``#ansible-devel`` 
に参加してください。

Ansible 製品の使用に関する質問とディスカッションは、
``#ansible`` チャンネルを使用してください。

謝辞
======

このトピックの元となる資料を提供していただいた Thomas Stringer (`@trstringer <https://github.com/trstringer>`_) 
氏に感謝の意を示します。
