.. _playbooks_reuse_roles:

ロール
=====

.. contents:: トピック

.. versionadded:: 1.2

ロールは、既知のファイル構造に基づいて特定の vars_files、タスク、およびハンドラーを自動的に読み込む方法です。 ロールでコンテンツをグループ化すると、他のユーザーとのロールの共有が容易になります。

ロールのディレクトリー構造
````````````````````````

プロジェクト構造の例:

    site.yml
    webservers.yml
    fooservers.yml
    roles/
        common/
            tasks/
            handlers/
            files/
            templates/
            vars/
            defaults/
            meta/
        webservers/
            tasks/
            defaults/
            meta/

ロールは、ファイルが特定のディレクトリー名にあることを想定しています。ロールには上記のディレクトリーのいずれかを含める必要がありますが、使用されていないものは除外しても問題はありません。使用中、それぞれのディレクトリーには、関連するコンテンツが含まれている ``main.yml`` ファイルが含まれている必要があります。

- ``tasks`` - このロールによって実行される主なタスクの一覧が含まれます。
- ``handlers`` - このロールによって使用される可能性のあるハンドラーや、このロールの外でも使用できるハンドラーが含まれます。
- ``defaults`` - ロールのデフォルト変数です (詳細は :ref:`playbooks_variables` を参照)。
- ``vars`` - ロールの他の変数です (詳細は :ref:`playbooks_variables` を参照)。
- ``files`` - このロールでデプロイできるファイルが含まれます。
- ``templates`` - このロールでデプロイできるテンプレートが含まれます。
- ``meta`` - このロールのメタデータを定義します。詳細は、以下を参照してください。

他の YAML ファイルは特定のディレクトリーに追加できます。たとえば、一般的に、``tasks/main.yml`` ファイルからプラットフォーム固有のタスクを指定できます。

    # roles/example/tasks/main.yml
    - name: added in 2.4, previously you used 'include'
      import_tasks: redhat.yml
      when: ansible_facts['os_family']|lower == 'redhat'
    - import_tasks: debian.yml
      when: ansible_facts['os_family']|lower == 'debian'

    # roles/example/tasks/redhat.yml
    - yum:
        name: "httpd"
        state: present

    # roles/example/tasks/debian.yml
    - apt:
        name: "apache2"
        state: present

また、ロールにはモジュールおよびその他のプラグインタイプが含まれる場合があります。詳細は、以下の「:ref:`embedding_modules_and_plugins_in_roles`」セクションを参照してください。

ロールの使用
```````````

ロールを使用する従来の (元の) 方法は、特定のプレイの ``roles:`` オプションを使用して行います。

    ---
    - hosts: webservers
      roles:
        - common
        - webservers

これにより、各ロールの「x」に以下の動作が指定されます。

- roles/x/tasks/main.yml が存在する場合は、一覧表示されているタスクがプレイに追加されます。
- roles/x/handlers/main.yml が存在する場合は、一覧表示されるハンドラーがプレイに追加されます。
- roles/x/vars/main.yml が存在する場合は、一覧表示される変数がプレイに追加されます。
- roles/x/defaults/main.yml が存在する場合は、一覧表示される変数がプレイに追加されます。
- roles/x/meta/main.yml が存在する場合は、一覧表示されるロールの依存関係はロールのリスト (1.3 以降) に追加されます。
- コピー、スクリプト、テンプレート、またはインクルードタスク (ロール内) は、相対パスや絶対パスを必要とせずに roles/x/{files,templates,tasks}/ (ディレクトリーはタスクに依存します) のファイルを参照できます。

この方法で使用する場合、Playbook の実行順序は以下のようになります。

- プレイで定義されている ``pre_tasks``。
- これまでにトリガーとなったハンドラーはすべて実行されます。
- ``roles`` に一覧表示される各ロールは順番に実行されます。ロールの ``meta/main.yml`` で定義されるロール依存関係は、タグのフィルタリングおよび条件に基づいて最初に実行されます。
- プレイで定義されている ``タスク``。
- これまでにトリガーとなったハンドラーはすべて実行されます。
- プレイで定義されている ``post_tasks``。
- これまでにトリガーとなったハンドラーはすべて実行されます。

.. note::
    ロールの依存関係に関する詳細は、以下を参照してください。

.. note::
    (Playbook の一部のみを実行する手段として後述されている) タスクと共にタグを使用する場合には、pre_tasks、post_tasks、およびロールの依存関係にタグを付け、これらと共に渡すようにしてください。特に、事前または事後のタスクおよびロールの依存関係が停止時のウィンドウ制御または負荷分散の監視に使用される場合に使用します。

Ansible 2.4 では、``import_role`` または ``include_role`` を使用して、他のタスクとインラインでロールを使用できるようになりました。

    ---
    - hosts: webservers
      tasks:
        - debug:
            msg: "before we run our role"
        - import_role:
            name: example
        - include_role:
            name: example
        - debug:
            msg: "after we ran our role"

ロールが従来の方法で定義されている場合、ロールは静的なインポートとして処理され、Playbook の解析中に処理されます。

.. note::
    ``include_role`` オプションは、Ansible 2.3 で導入されました。この使用方法は、インクルード (動的) とインポート (静的) の使用で一致するように、Ansible 2.4 で若干変更になりました。詳細は、:ref:`dynamic_vs_static` を参照してください。

ロールに使用される名前は、単純な名前 (以下の :ref:`role_search_path` を参照)か、完全修飾パスになります。

    ---
    - hosts: webservers
      roles:
        - role: '/path/to/my/roles/common'

ロールは、他のキーワードを受け入れることができます。

    ---
    - hosts: webservers
      roles:
        - common
        - role: foo_app_instance
          vars:
            dir: '/opt/a'
            app_port: 5000
        - role: foo_app_instance
          vars:
            dir: '/opt/b'
            app_port: 5001

または、新しい構文を使用します。

    ---
    - hosts: webservers
      tasks:
        - include_role:
            name: foo_app_instance
          vars:
            dir: '/opt/a'
            app_port: 5000
      ...

ロールを条件付きでインポートし、そのタスクを実行できます::

    ---
    - hosts: webservers
      tasks:
        - include_role:
            name: some_role
          when: "ansible_facts['os_family'] == 'RedHat'"



最後に、指定するロール内のタスクにタグを割り当てる場合があります。以下のことができます。

    ---
    - hosts: webservers
      roles:
        - role: foo
          tags:
            - bar
            - baz
        # using YAML shorthand, this is equivalent to the above:
        - { role: foo, tags: ["bar", "baz"] }
    
または、もう一度、新しい構文を使用します。

    ---
    - hosts: webservers
      tasks:
        - import_role:
            name: foo
          tags:
            - bar
            - baz

.. note::
    これにより、*そのロール内のすべてのタスクに指定タグが付けられ*、ロール内で指定されたタグに追加されます。

一方、ロール自体のインポートをタグ付けする場合があります::

    ---
    - hosts: webservers
      tasks:
        - include_role:
            name: bar
          tags:
            - foo

.. note:: この例のタグは ``include_role`` 内のタスクには *追加されません*。前後の ``block`` ディレクティブを使用して両方を実行できます。

.. note:: 実行するタグのサブセットを指定する際にロールをインポートする機能はありません。複数のタグを持つロールを構築し、ロールのサブセットを異なるタイミングで呼び出す場合には、そのロールを複数のロールに分割することを検討する必要があります。

ロールの複製および実行
``````````````````````````````

Ansible は、ロールに定義されているパラメーターが定義ごとに異ならないときは、ロールが複数回定義されている場合でもロールの実行が許可されるのは 1 回だけです。例::

    ---
    - hosts: webservers
      roles:
        - foo
        - foo

上記の場合、``foo`` ロールは 1 回のみ実行されます。

ロールを複数回実行するには、2 つのオプションがあります。

1. 各ロール定義に異なるパラメーターを渡します。
2. ``allow_duplicates: true`` をロールの ``meta/main.yml`` ファイルに追加します。

例 1 - 異なるパラメーターを渡す場合::

    ---
    - hosts: webservers
      roles:
        - role: foo
          vars:
            message: "first"
        - { role: foo, vars: { message: "second" } }

この例では、各ロール定義には異なるパラメーターがあるため、``foo`` は 2 回実行します。

例 2 - ``allow_duplicates: true:`` の使用::

    # playbook.yml
    ---
    - hosts: webservers
      roles:
        - foo
        - foo

    # roles/foo/meta/main.yml
    ---
    allow_duplicates: true

この例では、明示的に有効にしているため、``foo`` は 2 回実行します。

ロールのデフォルト変数
``````````````````````

.. versionadded:: 1.3

ロールのデフォルト変数を使用すると、含まれるロールまたは依存するロールのデフォルト変数を設定できます (下記参照)。デフォルトを作成するには、
``defaults/main.yml`` ファイルをロールディレクトリーに追加します。これらの変数は、使用可能な変数の中で最も優先順位が低く、
他の変数 (インベントリー変数など) によって簡単に上書きできます。

ロールの依存関係
`````````````````

.. versionadded:: 1.3

ロールの依存関係により、ロールの使用時に自動的に他のロールをプルできます。ロールの依存関係は、上記のようにロールディレクトリーに含まれる ``meta/main.yml`` ファイルに保存されます。このファイルには、指定されたロールの前に挿入するロールとパラメーターのリストが含まれている必要があります (``roles/myapp/meta/main.yml`` など)::

    ---
    dependencies:
      - role: common
        vars:
          some_parameter: 3
      - role: apache
        vars:
          apache_port: 80
      - role: postgres
        vars:
          dbname: blarg
          other_parameter: 12

.. note::
    ロールの依存関係は、従来のロール定義スタイルを使用する必要があります。

ロールの依存関係は、それらが含まれるロールの前に常に実行され、再帰的である可能性があります。依存関係も、上記で指定した複製ルールに従います。別のロールもこれを依存関係として一覧表示すると、上記のルールに基づいて再実行されることはありません。詳細は、「:ref:`Galaxy ロールの依存関係 <galaxy_dependencies>`」を参照してください。

.. note::
    ``allow_duplicates: true`` を使用する場合は、親ではなく依存するロールの ``meta/main.yml`` にある必要があることに注意してください。

たとえば、``car`` という名前のロールは、以下のように ``wheel`` という名前のロールに依存します。

    ---
    dependencies:
      - role: wheel
        vars:
          n:1
      - role: wheel
        vars:
          n:2
      - role: wheel
        vars:
          n:3
      - role: wheel
        vars:
          n:4

``wheel`` ロールは、``tire`` と ``brake`` の 2 つのロールに依存します。wheel の ``meta/main.yml`` には以下が含まれます。

    ---
    dependencies:
      - role: tire
      - role: brake

さらに、``tire`` および ``brake`` の ``meta/main.yml`` には以下が含まれます。

    ---
    allow_duplicates: true


その結果作成される実行順序は以下のようになります。

    tire(n=1)
    brake(n=1)
    wheel(n=1)
    tire(n=2)
    brake(n=2)
    wheel(n=2)
    ...
    car

``car`` が定義する各インスタンスは異なるパラメーター値を使用するため、``wheel`` には ``allow_duplicates: true`` を使用する必要がないことに注意してください。

.. note::
   変数継承およびスコープは :ref:`playbooks_variables` で詳細に説明されています。

.. _embedding_modules_and_plugins_in_roles:

ロールでのモジュールおよびプラグインの埋め込み
``````````````````````````````````````

これは、ほとんどのユーザーには関係ない高度なトピックです。

カスタムモジュールを作成する場合 (「:ref:`developing_modules`」を参照) またはプラグインを作成する場合 (「:ref:`developing_plugins`」を参照) は、ロールの一部として配布できます。
通常、プロジェクトとしての Ansible は、高品質のモジュールを Ansible コアに組み込むことに非常に関心があるため、これは標準ではないはずですが、実行は非常に簡単です。

これの良い例は、AcmeWidgets という名前の会社で働いていて、社内ソフトウェアの設定を支援する内部モジュールを作成していて、
組織内の他の人がこのモジュールを簡単に使用できるようにする一方で、Ansible ライブラリーパスの設定方法は全員には教えたくない場合です。

ロールの「tasks」および「handlers」の構造と共に、「library」という名前のディレクトリーを追加します。 この「library」ディレクトリーに、モジュールを直接含めます。

以下があるとします。

    roles/
        my_custom_modules/
            library/
                module1
                module2

モジュールはロール自体で使用でき、以下のようにこのロールの *後* に呼び出されるロールも利用可能になります。

    ---
    - hosts: webservers
      roles:
        - my_custom_modules
        - some_other_role_using_my_custom_modules
        - yet_another_role_using_my_custom_modules

これは、いくつかの制限はありますが、Ansible のコアディストリビューションのモジュールを修正するために使用することもできます。たとえば、実稼働リリースで、リリースされる前にモジュールの開発版を使用するなどです。 ただし、コアコンポーネントで API 署名が変更される可能性があるため、これが常に推奨されるわけではなく、常に機能するとは限りません。 これは、コアモジュールに対してパッチを運ぶのに便利な方法ですが、正当な理由がある場合に限ります。 必然的に、プロジェクトでは、プルリクエストを介して、可能な場合はいつでもコントリビューションを github にリダイレクトすることが推奨されます。

同じスキーマを使用して、同じメカニズムを使用してロールにプラグインを埋め込み、配布できます。たとえば、フィルタープラグインの場合は、以下のようになります。

    roles/
        my_custom_filter/
            filter_plugins
                filter1
                filter2

これらは「my_custom_filter」の後に呼び出される任意のロールのテンプレートまたは jinja テンプレートで使用できます。

.. _role_search_path:

ロール検索パス
````````````````

Ansible は、以下の方法でロールを検索します。

- Playbook ファイルへの相対的な ``roles/`` ディレクトリー。
- デフォルトでは、``/etc/ansible/roles`` にあります。

Ansible 1.4 以降では、ロールを検索するために追加の roles_path を設定できます。 これを使用して、共通のロールをすべて 1 つの場所にチェックアウトし、複数の Playbook プロジェクト間で簡単に共有します。 ansible.cfg でこの設定を行う方法は、「:ref:`intro_configuration`」を参照してください。

Ansible Galaxy
``````````````

`Ansible Galaxy <https://galaxy.ansible.com>`_ は、コミュニティーで開発されたあらゆる種類の Ansible ロールを検索、ダウンロード、評価、およびレビューする無料サイトで、ここで自動化プロジェクトのきっかけを得ることができます。

クライアントの ``ansible-galaxy`` は Ansible に含まれています。Galaxy クライアントを使用すると、Ansible Galaxy からロールをダウンロードでき、独自のロールを作成する優れたデフォルトフレームワークも提供します。 

詳細は、「`Ansible Galaxy ドキュメンテーション <https://galaxy.ansible.com/docs/>`_」ページを参照してください。

.. seealso::

   :ref:`ansible_galaxy`
       新規ロールの作成方法、Galaxy でのロールの共有、ロールの管理
   :ref:`yaml_syntax`
       YAML 構文について
   :ref:`working_with_playbooks`
       基本的な Playbook 言語機能を確認します。
   :ref:`playbooks_best_practices`
       実際の Playbook の管理に関するさまざまなヒント
   :ref:`playbooks_variables`
       Playbook の変数の詳細
   :ref:`playbooks_conditionals`
       Playbook の条件
   :ref:`playbooks_loops`
       Playbook のループ
   :ref:`all_modules`
       利用可能なモジュールについて
   :ref:`developing_modules`
       独自のモジュールを作成して Ansible を拡張する方法について
   `GitHub Ansible examples <https://github.com/ansible/ansible-examples>`_
       Github プロジェクトソースにあるすべての Playbook ファイル
   `メーリングリスト <https://groups.google.com/group/ansible-project>`_
       ご質問はございますか。サポートが必要ですか。ご提案はございますか。 Google グループの一覧をご覧ください。
