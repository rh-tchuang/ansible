Prompt
=======

Playbook を実行するとき、ユーザーに特定の入力を求めることができ、
「vars_prompt」セクションでこれを行います。

これの一般的な用途は、記録したくない機密データを要求することです。

これはセキュリティーを超えた用途があります。たとえば、
すべてのソフトウェアリリースに同じ Playbook と、
プッシュスクリプトで、特定のリリースバージョンの入力が求められます。

以下は最も基本的な例です。

    ---
    - hosts: all
      vars_prompt:

        - name: username
          prompt: "What is your username?"
          private: no

        - name: password
          prompt: "What is your password?"

      tasks:

        - debug:
            msg: 'Logging in as {{ username }}'

ユーザー入力はデフォルトでは表示されませんが、``private: no`` を設定することで表示できます。

.. note::
    個別の ``vars_prompt`` 変数の入力を求めるプロンプトは、コマンドラインの ``--extra-vars`` オプションですでに定義されている変数や、非対話的なセッション (cron や Ansible Tower など) から実行する場合に省略されます。/Variables/ の章の「:ref:`passing_variables_on_the_command_line`」を参照してください。

まれにしか変更しない変数がある場合は、
上書きできるデフォルト値を指定できます。これは、
以下のデフォルトの引数を使用して行います。

   vars_prompt:

     - name: "release_version"
       prompt:"Product release version"
       default:"1.0"

`Passlib <https://passlib.readthedocs.io/en/stable/>`_ がインストールされている場合、
vars_prompt は、入力値を暗号化して、たとえばユーザーモジュールを使用してパスワードを定義できます。

   vars_prompt:

     - name: "my_password2"
       prompt:"Enter password2"
       private: yes
       encrypt: "sha512_crypt"
       confirm: yes
       salt_size:7

「Passlib」がサポートする crypt スキームを使用できます。

- *des_crypt* - DES Crypt
- *bsdi_crypt* - BSDi Crypt
- *bigcrypt* - BigCrypt
- *crypt16* - Crypt16
- *md5_crypt* - MD5 Crypt
- *bcrypt* - BCrypt
- *sha1_crypt* - SHA-1 Crypt
- *sun_md5_crypt* - Sun MD5 Crypt
- *sha256_crypt* - SHA-256 Crypt
- *sha512_crypt* - SHA-512 Crypt
- *apr_md5_crypt* - Apache's MD5-Crypt variant
- *phpass* - PHPass' Portable Hash
- *pbkdf2_digest* - Generic PBKDF2 Hashes
- *cta_pbkdf2_sha1* - Cryptacular's PBKDF2 hash
- *dlitz_pbkdf2_sha1* - Dwayne Litzenberger's PBKDF2 hash
- *scram* - SCRAM Hash
- *bsd_nthash* - FreeBSD's MCF-compatible nthash encoding

ただし、許可されるパラメーターは「salt」または「salt_size」のみです。「salt」を定義するか、または「salt_size」を使用して自動生成して、
独自の「salt」を使用できます。何も指定しないと、
サイズ 8 の「salt」が生成されます。

.. versionadded:: 2.7

Passlib がインストールされていない場合は、`crypt <https://docs.python.org/2/library/crypt.html>`_ ライブラリーがフォールバックとして使用されます。
プラットフォームに応じて、最大で次の暗号化スキームがサポートされます。

- *bcrypt* - BCrypt
- *md5_crypt* - MD5 Crypt
- *sha256_crypt* - SHA-256 Crypt
- *sha512_crypt* - SHA-512 Crypt

.. versionadded:: 2.8

テンプレートエラーを作成する特殊文字 (つまり `{%`) を配置する必要がある場合は、``unsafe`` オプションを使用します。

   vars_prompt:
     - name: "my_password_with_weird_chars"
       prompt:"Enter password"
       unsafe: yes
       private: yes

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_variables`
       変数の詳細
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
