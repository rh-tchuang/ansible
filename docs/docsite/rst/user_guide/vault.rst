.. _vault:

Ansible Vault
=============

.. contents:: トピック

Ansible Vault は Ansible の機能で、Playbook またはロールで平文テキストとしてではなく、パスワードやキーの保護などの機密データを暗号化ファイルに維持できます。この vault ファイルは、ソース制御に配布または配置することができます。

この機能を有効にするには、コマンドラインツール :ref:`ansible-vault` を使用してファイルを編集し、コマンドラインフラグ (:option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>`、:option:`--vault-password-file <ansible-playbook --vault-password-file>`、または :option:`--vault-id <ansible-playbook --vault-id>`) を使用します。または、ansible.cfg ファイルを変更してパスワードファイルの場所を指定するか、常にパスワードを入力するように Ansible を設定することもできます。このオプションには、コマンドラインフラグの使用は必要ありません。

ベストプラクティスに関するアドバイスは、:ref:`best_practices_for_variables_and_vaults` を参照してください。

.. _what_can_be_encrypted_with_vault:

Vault で暗号化できるもの
````````````````````````````````

ファイルレベルの暗号化
^^^^^^^^^^^^^^^^^^^^^

Ansible Vault は、Ansible が使用する構造化データファイルを暗号化できます。

これには、「group_vars/」または「host_vars/」インベントリー変数、「include_vars」または「vars_files」により読み込まれた変数、または ``-e @file.yml`` または ``-e @file.json`` を使用して ansible-playbook コマンドラインで渡された変数ファイルを含めることができます。 ロール変数とデフォルトも含まれています。

Ansible タスク、ハンドラーなどもデータであるため、vault で暗号化できます。使用している変数の名前を隠すために、タスクファイル全体を暗号化できます。

Ansible Vault は、バイナリーファイルも含め、任意のファイルを暗号化できます。 vault で暗号化されたファイルが、
``src`` 引数として、:ref:`copy <copy_module>`、:ref:`template <template_module>`
:ref:`unarchive <unarchive_module>`、:ref:`script <script_module>`、または :ref:`assemble
<assemble_module>` モジュールとして指定されていると、ファイルは復号されたターゲットホストの宛先に配置されます 
(プレイの実行時に有効な vault パスワードが提供されている場合)。

.. note::
    ファイルレベルの暗号化の利点は、使いやすく、パスワードのローテーションが :ref:`鍵の変更 <rekeying_files>` で簡単に行えることです。
    欠点は、ファイルのコンテンツへのアクセスと読み取りが容易ではなくなったことです。タスクのリストである場合は、これは問題になる可能性があります (変数ファイルを暗号化するときの :ref:`ベストプラクティス <best_practices_for_variables_and_vaults>` は、これらの変数への参照を暗号化されていないファイルに保持することです)。


変数レベルの暗号化
^^^^^^^^^^^^^^^^^^^^^^^^^

Ansible は、`!vault` タグを使用して YAML ファイル内の単一値の暗号化もサポートし、YAML と Ansible に特別な処理が使用されていることを知らせます。この機能は、:ref:`以下 <encrypt_string_for_use_in_yaml>` で詳しく説明します。

.. note::
    変数レベルの暗号化の利点は、平文の変数と暗号化された変数が混在している場合でも、ファイルが簡単に判読できることです。
    欠点は、パスワードローテーションがファイルレベルの暗号化ほど単純ではないことです。:ref:`rekey <ansible_vault_rekey>` コマンドはこの方法では有効ではありません。


.. _vault_ids:

Vault ID および複数の Vault パスワード
``````````````````````````````````````


vault ID は、1 つ以上の vault シークレットの識別子です。
Ansible は複数の valut パスワードをサポートしています。

Valut IDは、個々の vault パスワードを区別するラベルを提供します。

vaule ID を使用するには、選択した ID *ラベル* とそのパスワードを取得する *source* (``prompt`` またはファイルパスのいずれか) を提供する必要があります。

.. code-block:: bash

   --vault-id label@source

このスイッチは、vault と対話できるすべての Ansible コマンド (:ref:`ansible-vault`、:ref:`ansible-playbook` など) で使用できます。

Vault で暗号化されたコンテンツは、暗号化された vault ID を指定できます。

たとえば、Playbook には、
vault ID の「dev」と「prod」で暗号化された変数ファイルを指定できます。

.. 注記:
    2.4 より前の古いバージョンの Ansible では、一度に 1 つの vault パスワードのみを使用できました。


.. _creating_files:

暗号化されたファイルの作成
````````````````````````

新しい暗号化されたデータファイルを作成するには、次のコマンドを実行します。

.. code-block:: bash

   ansible-vault create foo.yml

まず、パスワードの入力を求められます。パスワードを入力すると、ツールは $EDITOR で定義したエディターを起動します。デフォルトは vi です。 エディターセッションが完了すると、ファイルは暗号化されたデータとして保存されます。

デフォルトの暗号は AES (共有秘密ベース) です。

Vault ID「password1」が割り当てられ、暗号化された新しいデータファイルを作成し、パスワードの入力を求めるには、次を実行します。

.. code-block:: bash

   ansible-vault create --vault-id password1@prompt foo.yml


.. _editing_encrypted_files:

暗号化されたファイルの編集
```````````````````````

暗号化されたファイルをインプレース編集するには、:ref:`ansible-vault edit <ansible_vault_edit>` コマンドを使用します。
このコマンドは、ファイルを一時ファイルに復号し、ファイルを編集し、
完了したら保存して一時ファイルを削除できるようにします。

.. code-block:: bash

   ansible-vault edit foo.yml

「vault2」パスワードファイルで暗号化され、vault ID「pass2」を割り当てたファイルを編集するには、以下を実行します。

.. code-block:: bash

   ansible-vault edit --vault-id pass2@vault2 foo.yml


.. _rekeying_files:

暗号化されたファイルの再入力
````````````````````````

Vaule で暗号化されたファイルのパスワードを変更する場合は、rekey コマンドを使用できます。

.. code-block:: bash

    ansible-vault rekey foo.yml bar.yml baz.yml

このコマンドは、複数のデータファイルのキーを一度に変更できます。
元のパスワードと新しいパスワードが必要になります。

Vault ID の「preprod2」と「ppold」ファイルで暗号化された鍵を変更し、新しいパスワードの入力を求めるには、以下を実行します。

.. code-block:: bash

    ansible-vault rekey --vault-id preprod2@ppold --new-vault-id preprod2@prompt foo.yml bar.yml baz.yml

鍵を変更したファイルを ``--new-vault-id`` に渡して、鍵を変更したファイルに別の ID を設定できます。

.. _encrypting_files:

暗号化されていないファイルの暗号化
````````````````````````````

暗号化する既存のファイルがある場合は、
:ref:`ansible-vault encrypt <ansible_vault_encrypt>` コマンドを使用します。 このコマンドは、複数のファイルを一度に処理できます。

.. code-block:: bash

   ansible-vault encrypt foo.yml bar.yml baz.yml

「プロジェクト」IDで既存のファイルを暗号化し、パスワードの入力を求めるプロンプトを表示するには、以下のようになります。

.. code-block:: bash

   ansible-vault encrypt --vault-id project@prompt foo.yml bar.yml baz.yml

.. note::

   異なるパスワードファイルまたはプロンプトされるパスワードが毎回提供される場合は、*同じ* vault ID で *異なる* パスワードを持つファイルまたは文字列を個別に暗号化することは技術的に可能です。
   これは、(単一のパスワードではなく) パスワードのクラスへの参照として vault ID を使用し、コンテキストで使用する特定のパスワードまたはファイルを常に知っている場合に推奨されることが望ましい場合があります。ただし、これは不要に複雑なユースケースになる可能性があります。
   2 つのファイルが同じ vault IDで暗号化されていますが、誤って異なるパスワードが使用されている場合は、:ref:`rekey <rekeying_files>` コマンドを使用して問題を修正できます。


.. _decrypting_files:

暗号化されたファイルの復号化
``````````````````````````

暗号化が必要なくなった既存のファイルがある場合は、
:ref:`ansible-vault decrypt <ansible_vault_decrypt>` コマンドを実行することで完全に復号できます。 このコマンドはそれらを暗号化せずにディスクに保存するため、
:ref:`ansible-vault edit <ansible_vault_edit>` は使用しないことを確認してください。

.. code-block:: bash

    ansible-vault decrypt foo.yml bar.yml baz.yml


.. _viewing_files:

暗号化されたファイルの表示
```````````````````````

暗号化されたファイルの内容を編集せずに表示する場合は、:ref:`ansible-vault view <ansible_vault_view>` コマンドを使用できます。

.. code-block:: bash

    ansible-vault view foo.yml bar.yml baz.yml


.. _encrypt_string_for_use_in_yaml:

encrypt_string を使用して、yaml に埋め込む暗号化変数を作成します
`````````````````````````````````````````````````````````````````

:ref:`ansible-vault encrypt_string <ansible_vault_encrypt_string>` コマンドは、提供された文字列を暗号化し、
:ref:`ansible-playbook` の YAML ファイルで指定できる形式にフォーマットします。

CLI 引数として提供される文字列を暗号化する場合は、以下のようになります。

.. code-block:: bash

    ansible-vault encrypt_string --vault-password-file a_password_file 'foobar' --name 'the_secret'

結果::

    the_secret: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          62313365396662343061393464336163383764373764613633653634306231386433626436623361
          6134333665353966363534333632666535333761666131620a663537646436643839616531643561
          63396265333966386166373632626539326166353965363262633030333630313338646335303630
          3438626666666137650a353638643435666633633964366338633066623234616432373231333331
          6564

vault-id「dev」に、vault ID ラベルを使用する場合は、以下のようになります。

.. code-block:: bash

    ansible-vault encrypt_string --vault-id dev@a_password_file 'foooodev' --name 'the_dev_secret'

結果::

    the_dev_secret: !vault |
              $ANSIBLE_VAULT;1.2;AES256;dev
              30613233633461343837653833666333643061636561303338373661313838333565653635353162
              3263363434623733343538653462613064333634333464660a663633623939393439316636633863
              61636237636537333938306331383339353265363239643939666639386530626330633337633833
              6664656334373166630a363736393262666465663432613932613036303963343263623137386239
              6330

stdin から読み取った文字列を暗号化し、「db_password」という名前を付けます。

.. code-block:: bash

    echo -n 'letmein' | ansible-vault encrypt_string --vault-id dev@a_password_file --stdin-name 'db_password'

.. warning::

   このメソッドは、シェルの履歴に文字列を残します。テスト以外で使用しないでください。

結果::

    Reading plaintext input from stdin. (ctrl-d to end input)
    db_password: !vault |
              $ANSIBLE_VAULT;1.2;AES256;dev
              61323931353866666336306139373937316366366138656131323863373866376666353364373761
              3539633234313836346435323766306164626134376564330a373530313635343535343133316133
              36643666306434616266376434363239346433643238336464643566386135356334303736353136
              6565633133366366360a326566323363363936613664616364623437336130623133343530333739
              3039

暗号化する文字列の入力を求め、暗号化し、「new_user_password」という名前を付けるようにするには、以下を行います。


.. code-block:: bash

    ansible-vault encrypt_string --vault-id dev@a_password_file --stdin-name 'new_user_password'

出力結果::

    Reading plaintext input from stdin. (ctrl-d to end input)

ユーザーは、「hunter2」と入力して、ctrl-d を押します。

.. warning::

   文字列を指定した後に Enter キーを押さないでください。これにより、暗号化された値に新しい行が追加されます。

結果::

    new_user_password: !vault |
              $ANSIBLE_VAULT;1.2;AES256;dev
              37636561366636643464376336303466613062633537323632306566653533383833366462366662
              6565353063303065303831323539656138653863353230620a653638643639333133306331336365
              62373737623337616130386137373461306535383538373162316263386165376131623631323434
              3866363862363335620a376466656164383032633338306162326639643635663936623939666238
              3161

:ref:`single_encrypted_variable` も参照してください

暗号化された値を変数ファイル (vars.yml) に追加した後、デバッグモジュールを使用して元の値を確認できます。

.. code-block:: console

   ansible localhost -m debug -a var="new_user_password" -e "@vars.yml" --ask-vault-pass
   Vault password:

   localhost | SUCCESS => {
       "new_user_password": "hunter2"
   }


.. _providing_vault_passwords:

Vault パスワードの提供
`````````````````````````

すべてのデータが 1 つのパスワードを使用して暗号化される場合は、CLI オプションの :option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>` 
または :option:`--vault-password-file <ansible-playbook --vault-password-file>` を使用する必要があります。

たとえば、テキストファイル :file:`/path/to/my/vault-password-file` でパスワードストアを使用する場合は、次のようにします。

.. code-block:: bash

    ansible-playbook --vault-password-file /path/to/my/vault-password-file site.yml

パスワードを要求する場合は、次のようにします。

.. code-block:: bash

    ansible-playbook --ask-vault-pass site.yml

パスワード実行スクリプト :file:`my-vault-password.py` からパスワードを取得する場合は、以下のようにします。

.. code-block:: bash

    ansible-playbook --vault-password-file my-vault-password.py

設定オプション :ref:`DEFAULT_VAULT_PASSWORD_FILE` を使用して vault パスワードファイルを指定すると、
CLI オプション :option:`--vault-password-file <ansible-playbook --vault-password-file>` 
を毎回指定する必要がなくなります。


.. _specifying_vault_ids:

ボールトのラベル付け
^^^^^^^^^^^^^^^^

Ansible 2.4 以降、:option:`--vault-id <ansible-playbook --vault-id>` を使用して、
パスワードがどの vault ID (「dev」、「prod」、「cloud」など) のものであるかと、パスワードの取得方法 (プロンプト、ファイルパスなど) を示すことができます。

デフォルトでは、vault-id ラベルはヒントにすぎず、パスワードで暗号化された値はすべて複号されます。
構成オプション :ref:`DEFAULT_VAULT_ID_MATCH` は、vault id が、
値を暗号化したときに使用される valut ID と一致することを要求するように設定できます。
これにより、異なる値が異なるパスワードで暗号化されている場合のエラーを減らすことができます。

たとえば、vault-id「dev」にパスワードファイル :file:`dev-password` を使用する場合は以下のようになります。

.. code-block:: bash

    ansible-playbook --vault-id dev@dev-password site.yml

vault ID 「dev」のパスワードを要求する場合は、次のようになります。

.. code-block:: bash

    ansible-playbook --vault-id dev@prompt site.yml

実行スクリプト :file:`my-vault-password.py` から「dev」vault ID パスワードを取得する場合は次のようになります。

.. code-block:: bash

    ansible-playbook --vault-id dev@my-vault-password.py


設定オプション :ref:`DEFAULT_VAULT_IDENTITY_LIST` を使用してデフォルトの vault ID とパスワードソースを指定できるため、
毎回 CLI オプション :option:`--vault-id <ansible-playbook --vault-id>` を指定する必要はありません。


:option:`--vault-id <ansible-playbook --vault-id>` オプションは、vault-id を指定せずに使用することもできます。
この動作は、:option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>`、
または :option:`--vault-password-file <ansible-playbook --vault-password-file>` に相当するため、ほとんど使用されません。

たとえば、パスワードファイル :file:`dev-password` を使用する場合は、以下のようになります。

.. code-block:: bash

    ansible-playbook --vault-id dev-password site.yml

パスワードを要求する場合は、以下のようになります。

.. code-block:: bash

    ansible-playbook --vault-id @prompt site.yml

実行スクリプト :file:`my-vault-password.py` からパスワードを取得する場合は、以下のようになります。

.. code-block:: bash

    ansible-playbook --vault-id my-vault-password.py

.. note::
    Ansible 2.4 より前のバージョンでは、:option:`--vault-id <ansible-playbook --vault-id>` オプションはサポートされていないため、
    :option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>` または、
    :option:`--vault-password-file <ansible-playbook --vault-password-file>` を使用する必要があります。


複数の vault パスワード
^^^^^^^^^^^^^^^^^^^^^^^^

Ansible 2.4 以降では、複数の Valut パスワードを使用して、
:option:`--vault-id <ansible-playbook --vault-id>` を複数回指定できます。

たとえば、ファイルから読み取った「dev」パスワードを使用し、「prod」パスワードの入力を求めるプロンプトを表示する場合は、次のようにします。

.. code-block:: bash

    ansible-playbook --vault-id dev@dev-password --vault-id prod@prompt site.yml

デフォルトでは、vault ID ラベル (dev、prodなど) はヒントにすぎず、
Ansiblebは、各パスワードで vault コンテンツの復号を試みます。暗号化されたデータと同じラベルのパスワードが最初に試行され、
その後、各 vault シークレットがコマンドラインで指定された順序で試行されます。

暗号化したデータにラベルがない場合や、ラベルが、提供されたどのラベルとも一致しない場合は、
パスワードが指定された順序で試行されます。

上記の場合は、最初に「dev」パスワードが試行され、次に、Ansible が、
暗号化に使用される vault ID を知らない場合は「prod」パスワードが試行されます。

暗号化されたデータに vault ID ラベルを追加するには、データを暗号化するときに、
ラベルを付けて :option:`--vault-id <ansible-vault-create --vault-id>` オプションを使用します

:ref:`DEFAULT_VAULT_ID_MATCH` 構成オプションを設定して、Ansible が、
暗号化されたデータと同じラベルのパスワードのみを使用するようにすることができます。これはより効率的であり、
複数のパスワードが使用されている場合により予測可能になります。

構成オプション:ref:`DEFAULT_VAULT_IDENTITY_LIST` には、複数の CLI オプション :option:`--vault-id <ansible-playbook --vault-id>` に相当する複数の値を含めることができます。

:option:`--vault-id <ansible-playbook --vault-id>` は、:option:`--vault-password-file <ansible-playbook --vault-password-file>` オプションまたは :option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>` オプションの代わりに使用できます。
または、それらを組み合わせて使用できます。

コンテンツを暗号化する :ref:`ansible-vault` コマンド（:ref:`ansible-vault encrypt <ansible_vault_encrypt>`、:ref:`ansible-vault encrypt_string <ansible_vault_encrypt_string>` など）を使用する場合、
使用できる vault-id は 1 つだけです。


.. _vault_password_client_scripts:

Vault パスワードクライアントスクリプト
`````````````````````````````

vault パスワードを取得するスクリプトを実装する場合は、
どの vault ID ラベルが要求されたかを知っておくと便利です。たとえば、シークレットマネージャーからパスワードを読み込むスクリプトでは、
vault ID ラベルを使用して「dev」または「prod」のパスワードを選択できます。

Ansible 2.5以降、これはクライアントスクリプトの使用を通じてサポートされています。クライアントスクリプトは、
名前が ``-client`` で終わる実行スクリプトです。クライアントスクリプトは、
他の実行スクリプトと同じ方法で vault パスワードを取得するために使用されます。例:

.. code-block:: bash

    ansible-playbook --vault-id dev@contrib/vault/vault-keyring-client.py

違いは、スクリプトの実装にあります。クライアントスクリプトは ``--vault-id`` オプションを使用して実行されるため、
どの vault ID ラベルが要求されたかがわかります。したがって、上記の Ansible を実行すると、
クライアントスクリプトが次のように実行されます。

.. code-block:: bash

    contrib/vault/vault-keyring-client.py --vault-id dev

:file:`contrib/vault/vault-keyring-client.py` は、
システムキーリングからパスワードを読み込むするクライアントスクリプトの例です。


.. _speeding_up_vault:

Vault 操作の高速化
````````````````````````````

暗号化されたファイルが多数ある場合は、起動時にそれを復号すると、かなりの遅延が発生する可能性があります。これを高速化するには、cryptography パッケージをインストールします。

.. code-block:: bash

    pip install cryptography


.. _vault_format:

Vault 形式
````````````

vault 暗号化ファイルは、UTF-8 でエンコードされた txt ファイルです。

ファイル形式には、改行で終了するヘッダーが含まれます。

例::

    $ANSIBLE_VAULT;1.1;AES256

または::

    $ANSIBLE_VAULT;1.2;AES256;vault-id-label

ヘッダーには、セミコロン「;」で区切られた vault フォーマット ID、vault フォーマットバージョン、vault 暗号、および vault-id ラベル (フォーマットバージョン1.2) が含まれます。

最初のフィールド ``$ANSIBLE_VAULT`` はフォーマット ID です。現在、``$ANSIBLE_VAULT`` が有効な唯一のファイルフォーマット ID です。これは、(vault.is_encrypted_file() を介して) vault で暗号化されたファイルを識別するために使用されます。

2番目のフィールド (``1.X``) は、vault フォーマットのバージョンです。ラベル付き vault-id が指定されている場合、サポートされている Ansible のすべてのバージョンは、現在デフォルトで「1.1」または「1.2」になります。 

「1.0」フォーマットは、読み取り専用としてサポートされています (書き込み時に「1.1」フォーマットに自動的に変換されます)。現在、フォーマットバージョンは正確な文字列比較のみとして使用されています (バージョン番号は現在「比較」されていません)。

3 番目のフィールド (``AES256``) は、データの暗号化に使用される暗号アルゴリズムを識別します。現在、サポートされている暗号は「AES256」のみです。(vault フォーマット 1.0 は「AES」を使用していましたが、現在のコードは常に「AES256」を使用します。)

4 番目のフィールド (``vault-id-label``) は、データの暗号化に使用される vault-id ラベルを識別します。たとえば、``dev@prompt`` の vault-id を使用すると、「dev」の vault-id-label が使用されます。

注記:ヘッダーは、今後変更する可能性があります。vault ID とバージョンに続くものはすべて、vault フォーマットのバージョンに依存すると考えることができます。これには、暗号 ID、およびその後に続く可能性のある追加フィールドが含まれます。

ファイルの残りのコンテンツは「vaulttext」です。vault テキストは、暗号化された暗号文の text-armor バージョンです。
各行の幅は 80 文字になりますが、最後の行は短くなる場合があります。

Vault ペイロードフォーマット 1.1-1.2
``````````````````````````````

vault テキストは、暗号化テキストと SHA256 ダイジェストを連結したもので、結果は「hexlifyied」です。

「hexlify」は、Python 標準ライブラリーの `binascii <https://docs.python.org/3/library/binascii.html>`_ モジュールの ``hexlify()`` メソッドを指します。

hexlify() が行われた結果:

- hexlify() で編集されたソルトの文字列とそれに続く改行 (``0x0a``)。
- 暗号化された HMAC の、hexlify() で編集された文字列とそれに続く改行。HMAC は次のとおりです。

  - `RFC2104 <https://www.ietf.org/rfc/rfc2104.txt>`_ 型 HMAC

    - 入力は以下のとおりです。

      - AES256 で暗号化した暗号文
      - PBKDF2 キー。このキー、暗号キー、および暗号 IV は、以下から生成されます。

        - バイト単位のソルト
        - 10000 回の繰り返し
        - SHA256() アルゴリズム
        - 最初の 32 バイトは暗号キーです
        - 2 番目の 32 バイトは HMAC キーです
        - 残りの 16 バイトは暗号 IV です

-  暗号文の hexlify() が行われた文字列。暗号文は次のとおりです。

  - AES256 暗号化データ。データは次を使用して暗号化されます。

    - AES-CTR ストリーム暗号
    - 暗号鍵
    - IV
    - 整数 IV からシードされた 128 ビットのカウンターブロック
    - 平文

      - 元の平文
      - AES256 ブロックサイズまでのパディング(パディングに使用されるデータは `RFC5652 <https://tools.ietf.org/html/rfc5652#section-6.3>`_ に基づいています。)


