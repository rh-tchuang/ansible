.. _playbooks_vault:

Playbook での Vault の使用
========================

.. contents:: トピック

「Vault」は Ansible の機能で、Playbook またはロールで平文テキストとしてではなく、パスワードやキーの保護などの機密データを静止させて維持できます。この vault ファイルは、ソース制御に配布または配置することができます。

vault の内容は 2 種類あり、それぞれに使用法と制限があります。

:Vault で暗号化が行われたファイル:
    * 完全なファイルが vault で暗号化されると、Ansible 変数や他の種類のコンテンツを含めることができます。
    * 読み込み時または参照時には常に復号されるため、復号しない限り、コンテンツが必要かどうかを Ansible が認識できません。
    * これはインベントリー、変数を読み込むすべてのもの (つまり vars_files、group_vars、host_vars、include_vars など) と、
      ファイルを処理する一部のアクション (M(copy)、M(assemble)、M(script) など) に使用できます。

:Single で暗号化された変数:
    * 特定の変数のみが通常の「variable file」内で暗号化されます。
    * 他のコンテンツでは機能しません。変数でのみ有効です。
    * オンデマンドで復号されるため、異なる vault シークレットで vault 処理された変数を指定し、必要な変数のみを使用できます。
    * 再生やロールにインラインがある場合でも、同じファイル内で vault 処理された変数と、行われていな変数を混在させることができます。

.. warning::
    * vault は、データを「静止させて」保護します。 復号すると、プレイおよびプラグインの作成者はシークレットの公開を防ぐことができます。
      出力を非表示にする詳細は、「:ref:`no_log <keep_secret_data>`」を参照してください。

この機能を有効にするには、コマンドラインツール :ref:`ansible-vault` を使用してファイルを編集し、コマンドラインフラグ :option:`--ask-vault-pass <ansible-vault-create --ask-vault-pass>`、:option:`--vault-password-file <ansible-vault-create --vault-password-file>`、または :option:`--vault-id <ansible-playbook --vault-id>` を使用します。``ansible.cfg`` ファイルを変更してパスワードファイルの場所を指定するか、常にパスワードを入力するように Ansible を設定することもできます。このオプションには、コマンドラインフラグの使用は必要ありません。

ベストプラクティスに関するアドバイスは、:ref:`best_practices_for_variables_and_vaults` を参照してください。

vault を使用した Playbook の実行
`````````````````````````````

vault で暗号化されたデータファイルが含まれる Playbook を実行するには、vault パスワードを指定する必要があります。

vault-password をインタラクティブに指定するには、以下を実行します。

    ansible-playbook site.yml --ask-vault-pass

このプロンプトは、アクセスされる、vault で暗号化されたファイルを復号する (インメモリーのみ) ために使用されます。

または、パスワードはファイルまたはスクリプトで指定できます (スクリプトバージョンには Ansible 1.7 以降が必要です)。 このフラグを使用する場合は、ファイルのパーミッションで、他のユーザーが鍵にアクセスできないことを確認し、キーをソースコントロールに追加しないようにします。

    ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt

    ansible-playbook site.yml --vault-password-file ~/.vault_pass.py

パスワードは、ファイル内に単一行として保存される文字列である必要があります。

フラットファイルの代わりにスクリプトを使用している場合は、そのスクリプトを実行ファイルとするマークが付いていて、パスワードが標準出力に出力されていることを確認します。 スクリプトでデータの入力を要求する必要がある場合は、プロンプトを標準エラーに送信できます。

.. note::
   :envvar:`ANSIBLE_VAULT_PASSWORD_FILE` 環境変数 (``ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass.txt`` など) を設定することもできます。Ansible は、このファイル内のパスワードを自動的に検索します。

   これは、Jenkins などの継続的な統合システムから Ansible を使用する場合に行うことができます。

:option:`--vault-password-file <ansible-pull --vault-password-file>` オプションは、必要に応じて :ref:`ansible-pull` コマンドと併用することもできます。ただし、ノードにキーを配布する必要があるため、意図を理解してください。プッシュモードの場合は vault を使用することが意図されています。


複数の vault パスワード
````````````````````````

Ansible 2.4 以降では、異なるパスワードで暗号化される複数の vault の概念に対応します。
異なる vault には、それを区別するためのラベルを指定できます (通常は dev、prod などの値)。

:option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>` オプションおよび 
:option:`--vault-password-file <ansible-playbook --vault-password-file>` オプションは、
任意の実行には、パスワードは 1 つだけ必要になる場合に限り使用できます。

または、:option:`--vault-id <ansible-playbook --vault-id>` オプションを使用してパスワードを入力し、
使用する vault ラベルを示します。これは、
複数の vault が 1 つのインベントリー内で使用される場合により明確になります。例:

「dev」パスワードの入力が求められるようにするには、以下を実行します。

.. code-block:: bash

    ansible-playbook site.yml --vault-id dev@prompt

ファイルまたはスクリプトから「dev」パスワードを取得するには、以下を実行します。

.. code-block:: bash

    ansible-playbook site.yml --vault-id dev@~/.vault_pass.txt

    ansible-playbook site.yml --vault-id dev@~/.vault_pass.py

複数の vault パスワードが一回の実行に必要となる場合は、:option:`--vault-id <ansible-playbook --vault-id>` が、
複数回指定して、複数のパスワードを提供する場合に使用されます。 例:

ファイルから「dev」パスワードを読み取り、「prod」パスワードの入力を求められます。

.. code-block:: bash

    ansible-playbook site.yml --vault-id dev@~/.vault_pass.txt --vault-id prod@prompt

:option:`--ask-vault-pass <ansible-playbook --ask-vault-pass>` オプションまたは
:option:`--vault-password-file <ansible-playbook --vault-password-file>` オプションを使用すると、パスワードのいずれかを指定できます。
これらを :option:`--vault-id <ansible-playbook --vault-id>` と混在させないようにする方が一般的には適切です。

.. note::
    デフォルトでは、vault ラベル (dev、prod など）は単なるヒントです。Ansible は、
    指定されたすべてのパスワードで各 vault を復号しようとします。

    設定オプション :ref:`DEFAULT_VAULT_ID_MATCH` を設定すると、
    この動作に変更なり、各パスワードは同じラベルで暗号化されたデータの復号にのみ使用されます。詳細は、「:ref:`specifying_vault_ids`」
    を参照してください。

Vault パスワードクライアントスクリプト
`````````````````````````````

Ansible 2.5以降では、1 つの実行スクリプトを使用して、
vault ラベルに応じて異なるパスワードを取得できます。これらのクライアントスクリプトには、:file:`-client` で終わるファイル名が必要です。例:

:file:`contrib/vault/vault-keyring-client.py` スクリプトを使用してシステムキーリングから dev パスワードを取得するには、以下を実行します。

.. code-block:: bash

    ansible-playbook --vault-id dev@contrib/vault/vault-keyring-client.py

このトピックの詳細は、:ref:`vault_password_client_scripts` を参照してください。


.. _single_encrypted_variable:

単一の暗号化変数
`````````````````````````

バージョン 2.3 以降、Ansible は、それ以外の「平文」の YAML ファイルにある vault 処理された変数を使用できるようになりました。

    notsecret: myvalue
    mysecret: !vault |
              $ANSIBLE_VAULT;1.1;AES256
              66386439653236336462626566653063336164663966303231363934653561363964363833313662
              6431626536303530376336343832656537303632313433360a626438346336353331386135323734
              62656361653630373231613662633962316233633936396165386439616533353965373339616234
              3430613539666330390a313736323265656432366236633330313963326365653937323833366536
              34623731376664623134383463316265643436343438623266623965636363326136
    other_plain_text: othervalue

vault 処理された変数を作成するには、:ref:`ansible-vault encrypt_string <ansible_vault_encrypt_string>` コマンドを使用します。詳細は「:ref:`encrypt_string`」を参照してください。

vault 処理された変数は、提供された vault シークレットで復号化され、通常の変数として使用されます。``ansible-vault`` コマンドラインは、オンザフライでデータの暗号化用に stdin および stdout をサポートします。これは、エディターから使用して、このような vault 処理された変数を作成できます。Ansible と YAML の両方を復号する必要があることを認識できるように、必ず ``!vault`` タグを追加する必要があります。vault の暗号化により複数行の文字列になるため、``|`` も必要になります。

.. note::
   インライン vault は変数でのみ機能し、タスクのオプションで直接使用することはできません。

.. _encrypt_string:

encrypt_string の使用
````````````````````

このコマンドは、YAML ファイルに含めるために上記の形式の文字列を出力します。
暗号化する文字列は、stdin、コマンドライン引数、または対話式プロンプトで指定できます。

「:ref:`encrypt_string_for_use_in_yaml`」を参照してください。
