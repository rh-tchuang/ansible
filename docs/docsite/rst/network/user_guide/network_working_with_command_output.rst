.. \_networking\_working\_with\_command\_output:

**********************************************************
ネットワークモジュールのコマンド出力およびプロンプトの使用
**********************************************************

.. contents::
  :local:

ネットワークモジュールの条件
===================================

Ansible では、条件を使用して Playbook のフローを制御できます。Ansible ネットワークコマンドモジュールは、以下の固有の条件ステートメントを使用します。

* ``eq`` \- 等しい
* ``neq`` \- 等しくない
* ``gt`` \- より大きい
* ``ge`` \- より大きいか等しい
* ``lt`` \- より小さい
* ``le`` \- より小さいか等しい
* ``contains`` \- オブジェクトに指定された項目が含まれる


条件ステートメントは、
デバイスでリモートに実行されたコマンドからの結果を評価します。 タスクがコマンドセットを実行したら、
``wait_for`` 引数を使用して、
Ansible Playbook に制御を返す前に結果を評価できます。

例::

    ---
    - name: wait for interface to be admin enabled
      eos_command:
          commands:
              - show interface Ethernet4 | json
          wait_for:
              - "result[0].interfaces.Ethernet4.interfaceStatus eq connected"

上記の例のタスクでは、:code:`show interface Ethernet4 | json` コマンドが、
リモートデバイスで実行され、結果が評価されます。 パ
ス
:code:`(result[0].interfaces.Ethernet4.interfaceStatus)` が、「connected」と等しくない場合は、
コマンドが再試行されます。 このプロセスは、
条件が満たされるか、
または再試行の回数 (デフォルトでは 1 秒間隔で 10 回試行します) に達するまで継続します。

コマンドモジュールは、
インターフェースにある複数のコマンドセットの結果が表示されます。 例::

    ---
    - name: wait for interfaces to be admin enabled
      eos_command:
          commands:
              - show interface Ethernet4 | json
              - show interface Ethernet5 | json
          wait_for:
              - "result[0].interfaces.Ethernet4.interfaceStatus eq connected"
              - "result[1].interfaces.Ethernet5.interfaceStatus eq connected"

上記の例では、
リモートデバイスで 2 つのコマンドが実行され、結果が評価されます。 結果インデックスの値 (0 または 1) を指定すると、
正しい結果出力が
その条件に対して確認されます。

``wait_for`` 引数は常に結果で始まり、次に、
``[]`` のコマンドインデックス (``0`` がコマンド一覧の最初のコマンドになり、
``1`` が次のコマンド、``2`` がその次のコマンドと続きます) となります。


ネットワークモジュールのプロンプトの処理
===================================

ネットワークデバイスでは、デバイスに変更を加える前に、プロンプトに応答する必要がある場合があります。:ref:`ios_command <ios_command_module>`、:ref:`nxos_command <nxos_command_module>` などの個別のネットワークモジュールは、``prompt`` パラメーターでこれを処理できます。

.. note::

	``prompt`` は Python 正規表現です。``prompt` 値に ``?`` などの特殊文字を追加すると、プロンプトが一致しなくなり、タイムアウトが発生します。これを回避するには、`prompt`` 値が、実際のデバイスプロンプトに一致する Python 正規表現であることを確認します。``prompt`` 正規表現で特殊文字を正しく処理する必要があります。

:ref:`cli_command <cli_command_module>` を使用して複数のプロンプトを処理することもできます。

.. code-block:: yaml

  ---
  - name: multiple prompt, multiple answer (mandatory check for all prompts)
    cli\_command:
      command: "copy sftp sftp://user@host//user/test.img"
      check\_all:True
      prompt:
        \- "Confirm download operation"
        \- "Password"
        \- "Do you want to change that to the standby image"
      answer:
        \- 'y'
        - <password>
        \- 'y'

プロンプトと回答を同じ順序で一覧表示する必要があります (つまり、prompt\[0] は、answer\[0] により応答されます)。

上記の例では、``check_all:True`` にすると、タスクは各プロンプトに対して一致する回答を提供します。この設定がないと、複数のプロンプトがあるタスクは、すべてのプロンプトに最初の回答を提供します。

以下の例では、2 番目の回答は無視され、両方のプロンプトに ``y`` が回答されます。つまり、このタスクは両方の答えが同一である場合に限り機能します。また、``プロンプト`` は Python 正規表現である必要があります。これにより、最初のプロンプトで ``?`` がエスケープされます。

.. code-block:: yaml

  ---
   - name: reboot ios device
     cli\_command:
       command: reload
       prompt:
         \- Save\\?
         \- confirm
       answer:
         \- y
         \- y

.. seealso::

  `Ansible によるネットワークデバイスの再起動 <https://www.ansible.com/blog/rebooting-network-devices-with-ansible>`_
      ネットワークデバイスに ``wait_for``、``wait_for_connection``、および ``prompt`` を使用した例。

  `cli_command の詳細<https://www.ansible.com/blog/deep-dive-on-cli-command-for-network-automation>`_
      ``cli_command`` の使用方法に関する詳細な概要
