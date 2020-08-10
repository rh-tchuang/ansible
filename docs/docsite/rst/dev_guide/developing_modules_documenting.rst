.. _developing_modules_documenting:
.. _module_documenting:

*******************************
モジュールの形式およびドキュメント
*******************************

Ansible にモジュールを投稿したい場合は、Python でモジュールを書き、以下の標準形式に従う必要があります。(Windows モジュールを書いている場合を除きます。Windows モジュールには「:ref:`Windows ガイドライン <developing_modules_general_windows>`」が適用されます)。 この形式に従うことに加え、プル要求を作成する前に、「:ref:`提出チェックリスト <developing_modules_checklist>`」、「:ref:`プログラミングのヒント <developing_modules_best_practices>`」、「:ref:`Python 2 と Python 3 の互換性を維持するための戦略 <developing_python_3>`」および「:ref:`テスト <developing_testing>`」に関する情報を確認してください。

Python で書かれたすべての Ansible モジュールは、特定の順序で 7 つの標準セクションから始まり、その後にコードが続きます。セクションの順番は以下のとおりです。

.. contents::
   :depth: 1
   :local:

.. note:: 最初にインポートが行われないのはなぜですか。

  熱心な Python プログラマーは、PEP 8 のアドバイスに反して、ファイル上部に ``imports`` が入っていないことに気が付くかもしれません。これは、``ANSIBLE_METADATA`` から ``RETURN`` セクションまではモジュールコード自体によって使用されないためです。これらは基本的にファイル用に追加のドキュメント文字列であるためです。インポートは、PEP 8 と同じ理由で、特別な変数の後に挿入されます。これは、入門的なコメントと ドキュメント文字列の後にインポートが加えられます。これにより、コードの能動的な部分は一緒に、純粋に情報的な部分は離れた場所に置かれます。E402 を除外する決定は、読みやすさに基づいています (これが PEP 8 の目的です)。モジュール内のドキュメント文字列は、コードよりもモジュールレベルのドキュメント文字列に似ており、モジュール自体が利用することはありません。インポートをこのドキュメントの下、コードの近くに置くと、関連するすべてのコードが統合されてグループ化され、読みやすさ、デバッグ、理解が向上します。

.. warning:: **古いモジュールは注意してコピーしてください。**

  Ansible Core の古いモジュールの一部は、そのファイルの下に ``imports``、完全な GPL 接頭辞を持つ ``著作権`` 通知、および/または ``ANSIBLE_METADATA`` フィールドが間違った順序で含まれています。これらは、更新が必要なレガシーファイルです。新しいモジュールにはコピーしないでください。しばらく経過すると、古いモジュールを更新して修正します。このページのガイドラインに従ってください。

.. _shebang:

Python シバンと UTF-8 コーディング
===============================

すべての Ansible モジュールは、``#!/usr/bin/python`` で開始する必要があります。この「シバン」を使用すると、``ansible_python_interpreter`` が有効になります。
ファイルが UTF-8 エンコードされていることを明確にするために、これは ``# -*- coding: utf-8 -*-`` のすぐ後に続きます。

.. _copyright:

著作権およびライセンス
=====================

シバンおよび UTF-8 コーディングの後には、元の著作権所有者およびライセンス宣言を含む `著作権の行 <https://www.gnu.org/licenses/gpl-howto.en.html>`_ があるはずです。ライセンス宣言は、完全な GPL 接頭辞ではなく、1 行で記載する必要があります。

.. code-block:: python

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    # Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
    # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

モジュールに重要な追加 (書き直しなど) を追加すると、余分な著作権行が追加されます。法的なレビューにはソース制御の履歴が含まれるので、完全な著作権ヘッダーは必要ありません。重要な機能または書き直しに 2 番目の行を追加する場合は、古い機能の上に新しい行を追加します。

.. code-block:: python

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    # Copyright: (c) 2017, [New Contributor(s)]
    # Copyright: (c) 2015, [Original Contributor(s)]
    # GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

.. _ansible_metadata_block:

ansible_METADATA ブロック
======================

シバンの後に、UTF-8 コーディング、著作権、およびライセンスの後に、モジュールファイルに ``ANSIBLE_METADATA`` セクションが含まれている必要があります。このセクションは、他のツールで使用するためにモジュールに関する情報を提供します。新しいモジュールの場合は、以下のブロックをモジュールに追加するだけです。

.. code-block:: python

   ANSIBLE_METADATA = {'metadata_version': '1.1',
                       'status': ['preview'],
                       'supported_by': 'community'}

.. warning::

   * ``metadata_version`` は、モジュールのバージョンでは *なく*、``ANSIBLE_METADATA`` スキーマのバージョンです。
   * モジュールの ``status`` または ``supported_by`` ステータス`` のプロモートは、Ansible Core Team のメンバーのみが行う必要があります。

Ansible メタデータフィールド
-----------------------

:metadata_version:「X.Y」形式の文字列です。X と Y は、
   メタデータ形式のバージョンを定義する整数です。Ansible と同梱されるモジュールは、
   Ansible のリリースに紐付けられているため、
   メタデータのバージョンは 1 つのものしか出荷されません。既存のフィールドにフィールドや法的な値を追加する場合は、
   Y がインクリメントされます。フィールドや値を削除したり、
   フィールドの型や意味を変更したりすると X がインクリメントされます。
   現在の metadata_versionは「1.1」です。

:supported_by: 誰がモジュールをサポートしますか。
   デフォルト値は ``community`` です。サポートレベルの値の説明は、
   「:ref:`モジュールサポート` <modules_support>」を参照してください。値は次のとおりです。

   * core
   * network
   * certified
   * community
   * curated 
     (*非推奨の値 - このカテゴリーのモジュールは core または certified である必要があります。)

:status: モジュールがどの程度安定しているかを記述した文字列のリスト。「:ref:`module_lifecycle`」も参照してください。
   デフォルト値は単一要素リスト ["preview"] です。以下の文字列は有効なステータスであり、
   以下の意味があります。

   :stableinterface: モジュールのオプション (許可されるパラメーターまたは引数) は安定しています。オプションを削除したり、その意味を変更したりしないように、
      あらゆる努力がなされます。モジュールのコードの品質を評価するものでは**ありません**。
   :preview:このモジュールはテクノロジープレビューです。不安定であったり、
      オプションが変更されたり、
      ライブラリーや Web サービスに互換性のない変更が発生する場合があります。
   :deprecated:モジュールは非推奨となり、今後のリリースで削除されます。
   :removed:このモジュールはリリースには存在しません。ドキュメントを作成できるように、
      スタブが保存されています。ドキュメントは、
      ユーザーが削除されたモジュールから新しいモジュールに移植するのに役立ちます。

.. _documentation_block:

DOCUMENTATION ブロック
===================

シバンの後に、UTF-8 コーディング、著作権行、およびライセンス、``ANSIBLE_METADATA`` セクションの後には、``DOCUMENTATION`` ブロックが続きます。Ansible のオンラインモジュールのドキュメントは、各モジュールのソースコードの ``DOCUMENTATION`` ブロックから生成されます。``DOCUMENTATION`` ブロックは有効な YAML である必要があります。Python ファイルに DOCUMENTATION 文字列を含める前に、:ref:`YAML 構文を強調したエディター <other_tools_and_programs>` で ``DOCUMENTATION`` 文字列を書き始めた方が簡単かもしれません。まず、`サンプルドキュメントの文字列` <https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml>_ をモジュールファイルにコピーし、これを変更することで開始します。YAML の構文の問題を実行する場合は、`YAML Lint` <http://www.yamllint.com/>_ の Web サイトでこれを検証できます。

モジュールのドキュメントでは、各モジュールとオプションの動作について簡単かつ正確に定義し、基礎となるシステムで他のモジュールとどのように連携するかを説明します。ドキュメントは、専門家と非専門家の両方が読むことができるように、幅広い読者に向けて作成する必要があります。
    *説明は常に大文字で始め、完全に終了する必要があります。一貫性は常に役立ちます。
    * ドキュメントの引数と、モジュール仕様のディクショナリーが同じであることを確認します。
    * パスワード/シークレットの引数 ``no_log=True`` を設定する必要があります。
    * 機密情報が含まれているように見えても「password_length」などのシークレットが **含まれていない** ように表示される引数には、``no_log=False`` を設定して警告メッセージを無効にします。
    * オプションが必要となるだけの場合は、条件を記述してください。たとえば、「Required when I(state=present)」のようになります。
    * モジュールで ``check_mode`` が許可されている場合は、これをドキュメントに反映させます。

各ドキュメントフィールドの説明は次のとおりです。モジュールのドキュメントをコミットする前に、コマンドラインおよび HTML でテストしてください。

* モジュールファイルが :ref:`ローカルで使用できる限り <local_modules>`、``ansible-doc -t module my_module_name`` を使用してコマンドラインでモジュールのドキュメンテーションを表示できます。構文解析エラーは明確になります。コマンドに ``-vvv`` を追加すると、詳細を表示できます。
* モジュールドキュメントの :ref:`HTML 出力をテスト <testing_module_documentation>` する必要もあります。

ドキュメントフィールド
--------------------

``DOCUMENTATION`` ブロックのフィールドはすべて小文字になります。特に明記されていない限り、すべてのフィールドが必須です。

:module:

  * モジュールの名前。
  * ファイル名と同じ (``.py`` 拡張子なし) である必要があります。

:short_description:

  * :ref:`all_modules` ページと ``ansible-doc -l`` に表示される簡単な説明です。
  * ``short_description`` は、``ansible-doc -l`` で表示されます (カテゴリーでのグループなし)。
    そのため、モジュールが存在するディレクトリー構造のコンテキストなしでモジュールの目的を説明するのに十分な詳細が必要です。
  * ``description:`` とは異なり、``short_description`` には末尾のピリオド (完全な停止) は使わないでください。

:description:

  * 詳細な説明 (通常は 2 文以上)。
  * 文章の形 (冒頭の大文字なピリオドなどを使用) 完全な文章で記述する必要があります。
  * モジュール名について言及すべきではありません。
  * 1 つの長い段落にせず、複数の文章に分けます。
  * YAML で必要な場合を除き、完全な値を引用符で囲まないでください。

:version_added:

  * モジュールが追加された Ansible のバージョン。
  * これは浮動小数点ではなく文字列です (つまり ``version_added: '2.1'`` )。

:author:

  * ``First Last (@GitHubID)`` 形式のモジュール作成者の名前。
  * 作成者が複数になる場合は、複数行のリストを使用します。
  * YAML では必要ないため、引用符は使用しないでください。

:deprecated:

  * 将来のリリースで削除されるモジュールにマークを付けします。「:ref:`module_lifecycle`」も参照してください。

:options:

  * オプションは、多くの場合、`パラメーター` または `引数` と呼ばれます。ドキュメンテーションフィールドは `オプション` と呼ばれているため、この用語を使用します。
  * モジュールにオプションがない場合 (例: ``_facts`` モジュール)、必要なのは 1 行だけ (``options: {}``) です。
  * モジュールにオプションがある (つまり引数を受け入れる) 場合、各オプションは詳細に文書化される必要があります。各モジュールオプションについて、以下を記載します。

  :option-name:

    * (CRUD ではなく) 宣言操作は、「is_online:」ではなく、「online:」などの最終状態に焦点をあてます。
    *オプションの名前は、そのモジュールの残りの部分、および同じカテゴリーの他のモジュールと一貫性を持たせる必要があります。
    * 不明な場合は、他のモジュールを探して、同じ目的で使用されているオプション名を見つけてください。ユーザーに一貫性を提供できるようにしています。

  :description:

    *このオプションの機能の詳細な説明。これは、完全な文章で記述する必要があります。
    * 最初のエントリーは、オプションそのものの説明です。後続のエントリーは、その使用、依存関係、または使用できる値の形式の詳細を説明します。
    * 可能な値を列挙しないでください (``choices:`` はそのためにあります。値が明らかでない場合は、その値が何を示すのかを説明してください)。
    * オプションのみが必要な場合は、条件を記述してください。たとえば、「Required when I(state=present)」のようになります。
    *相互に排他的なオプションは、各オプションの最後の文で文書化する必要があります。

  :required:

    * ``true`` の場合にのみ必要です。
    * 見つからない場合は、オプションが不要であると仮定します。

  :default:

    * ``required`` が false もしくは指定されていない場合は、``default`` を指定できます (見つからない場合は「null」と見なされます)。
    *ドキュメントのデフォルト値が、コードのデフォルト値と一致していることを確認してください。
    * 追加の情報や条件が必要な場合を除き、デフォルトのフィールドは、説明の一部として記載しないでください。
    * オプションがブール値の場合は、
      Ansible が認識する任意のブール値 (true/false、yes/no など) を使用できます。 オプションのコンテキストで読み取りが適切であればこれを選択します。

  :choices:

    * オプション値のリスト。
    * 空欄の場合は指定なしになります。

  :type:

    * オプションで使用できるデータ型を指定します。``argspec`` と一致させる必要があります。
    * 引数が ``type='bool'`` の場合、このフィールドは ``type: bool` に設定してください。``choices`` は指定しないでください。
    * 引数が ``type='list'`` の場合は、``elements`` を指定する必要があります。

  :elements:

    * ``type='list'`` の場合に list 要素のデータ型を指定します。

  :aliases:
    * オプションの名前エイリアスのリスト。
    * 一般的には必要ありません。

  :version_added:

    * Ansible の初回リリース後にこのオプションが拡張された場合にのみ必要です。たとえば、トップレベルの `version_added` フィールドよりも大きくなります。
    これは浮動小数点ではなく文字列です (つまり ``version_added: '2.3'``)。

  :suboptions:

    * このオプションがディクショナリーまたはディクショナリーの一覧を取る場合は、ここで構造を定義できます。
    * 例は、「:ref:`azure_rm_securitygroup_module`」、「:ref:`azure_rm_azurefirewall_module`」、および「:ref:`os_ironic_node_module`」を参照してください。

:requirements:

  * 要件のリスト (該当する場合)。
  * 最小バージョンを指定します。

:seealso:

  * その他のモジュール、ドキュメント、またはインターネットリソースへの参照の一覧。
  * 参照には、以下の形式のいずれかを使用できます。


    .. code-block:: yaml+jinja

        seealso:

        # Reference by module name
        - module: aci_tenant

        # Reference by module name, including description
        - module: aci_tenant
          description: ACI module to create tenants on a Cisco ACI fabric.

        # Reference by rST documentation anchor
        - ref: aci_guide
          description: Detailed information on how to manage your ACI infrastructure using Ansible.

        # Reference by Internet resource
        - name: APIC Management Information Model reference
          description: Complete reference of the APIC object model.
          link: https://developer.cisco.com/docs/apic-mim-ref/

:notes:

  * 上記のセクションのいずれかに該当しない重要な情報の詳細。
  * たとえば、``check_mode`` がサポートされているかどうかです。


モジュールドキュメント内のリンク
-----------------------------------

モジュールドキュメントからその他のモジュールドキュメント、doccs.ansible.com 内のその他のリソース、インターネット上の他のリソースにリンクできます。これらのリンクの正しい形式は以下のとおりです。

* ``L()`` (見出しとリンク)。たとえば、``See L(IOS Platform Options guide,../network/user_guide/platform_ios.html).`` です。
* ``U()`` (URL)。たとえば、``See U(https://www.ansible.com/products/tower) for an overview.`` です。
* ``I()`` (オプション名)。たとえば、``Required if I(state=present).`` です。
* ``C()`` (ファイルおよびオプションの値)。たとえば、``If not set the environment variable C(ACME_PASSWORD) will be used.`` です。
* ``M()`` (モジュール名)。たとえば、``See also M(win_copy) or M(win_template).`` です。

.. note::

  コレクションのモジュールでは、そのコレクション内のコンテンツに使用できるのは ``L()`` および ``M()`` に限定されます。``U()`` を使用して、別のコレクションのコンテンツを参照します。

.. note::

    - モジュールのグループを参照するには、``C(..)`` を使用します。たとえば ``Refer to the C(win_*) modules.`` です。
    - ``seealso`` の方が目立つため、一般的な参照にはノートの使用や説明へのリンクよりも、``seealso`` の使用が推奨されます。

.. _module_docs_fragments:

ドキュメントフラグメント
-----------------------

複数の関連モジュールを作成している場合は、認証の詳細、ファイルモードの設定、``notes:`` や ``seealso:`` のエントリーなど、共通のドキュメントを共有している場合があります。そのような情報を各モジュールの ``DOCUMENTATION`` ブロックに重複させるのではなく、doc_fragment プラグインとして一度保存しておき、各モジュールのドキュメントで使用することができます。Ansible では、共有されるドキュメントフラグメントは `lib/ansible/plugins/doc_fragments/ <https://github.com/ansible/ansible/tree/devel/lib/ansible/plugins/doc_fragments>`_ にある ``ModuleDocFragment`` クラスに含まれています。ドキュメントフラグメントを含めるには ``extends_documentation_fragment: FRAGMENT_NAME`` をモジュールのドキュメントに追加します。

モジュールがドキュメントフラグメントのアイテムを使用するのは、そのフラグメントをインポートする既存のモジュールと動作する方法で、ドキュメント化されたすべてのインターフェースをモジュールが実装する場合のみです。目標は、ドキュメントフラグメントからインポートされたアイテムが、ドキュメントフラグメントをインポートする別のモジュールで使用された場合と同じように動作することです。

デフォルトでは、ドキュメントフラグメントからの ``DOCUMENTATION`` プロパティーのみがモジュールのドキュメントに挿入されます。ドキュメントフラグメントの特定の部分だけをインポートするために、ドキュメントフラグメントに追加のプロパティーを定義したり、必要に応じて組み合わせて使用したりすることができます。ドキュメントフラグメントとモジュールの両方でプロパティーが定義されている場合は、モジュールの値がドキュメントフラグメントよりも優先されます。

以下は、``example_fragment.py`` という名前のドキュメントフラグメントの例です。

.. code-block:: python

    class ModuleDocFragment(object):
        # Standard documentation
        DOCUMENTATION = r'''
        options:
          # options here
        '''

        # Additional section
        OTHER = r'''
        options:
          # other options here
        '''


``OTHER`` の内容をモジュールに挿入するには、次を実行します。

.. code-block:: yaml+jinja

    extends_documentation_fragment: example_fragment.other

または、以下の両方を使用してください。

.. code-block:: yaml+jinja

    extends_documentation_fragment:
      - example_fragment
      - example_fragment.other

.. _note:
* Prior to Ansible 2.8, documentation fragments were kept in ``lib/ansible/utils/module_docs_fragments``.

バージョン 2.8 における新機能

Ansible 2.8 以降、その他のプラグインと同様に、プレイやロールに隣接する ``doc_fragments`` ディレクトリーを使用することで、ユーザーが提供する doc_fragments を設定できます。

たとえば、すべての AWS モジュールには以下を含める必要があります。

.. code-block:: yaml+jinja

    extends_documentation_fragment:
    - aws
    - ec2

「:ref:`docfragments_collections`」では、コレクションにドキュメントのフラグメントを組み込む方法について説明します。

.. _examples_block:

EXAMPLES ブロック
==============

``EXAMPLES`` ブロックは、シバン、UTF-8 コーディング、著作権行、ライセンス、``ANSIBLE_METADATA`` セクション、そして ``DOCUMENTATION`` ブロックの後に続きます。ここでは、複数行のプレーンテキストである YAML 形式の実例を使用して、モジュールがどのように機能するかをユーザーに示します。最適な例は、ユーザーが Playbook にコピーして貼り付ける準備が整っていることです。モジュールが変更されるたびに、サンプルをレビューして更新してください。

Playbook のベストプラクティスに基づき、各例には ``name:`` 行が必要です。

    EXAMPLES = r'''
    - name: Ensure foo is installed
      modulename:
        name: foo
        state: present
    '''

``name:`` の行は大文字にし、末尾のドットは含めないでください。

サンプルでブール値オプションを使用する場合は、yes/no の値を使用します。ドキュメントによりブール値が yes/no として生成されるため、このサンプルではこれらの値が使用されており、モジュールドキュメントの一貫性が保たれます。

モジュールが必要なファクトを返すと、その使用方法の例が便利です。

.. _return_block:

RETURN ブロック
============

``RETURN`` ブロックは、シバン、UTF-8 コーディング、著作権行、ライセンス、``ANSIBLE_METADATA`` セクション、``DOCUMENTATION`` ブロック、そして ``EXAMPLES`` ブロックの後に続きます。本セクションでは、他のモジュールによって使用されるためにモジュールが返す情報を説明します。

モジュールが何も返さない場合は (標準の戻り値とは異なり)、モジュールのこのセクションは「``RETURN = r''' # '''``」を読み取る必要があります。
それ以外の場合は、返された各値に以下のフィールドを指定します。特に指定がない場合はすべてのフィールドが必要になります。

:return name:
  返されるフィールドの名前。

  :description:
    この値の意味の詳細な説明。大文字、および末尾のドットを使用します。
  :returned:
    ``always``、``on success`` など、この値が返される場合。
  :type:
    データ型。
  :elements:
    ``type='list'`` の場合は、リストの要素のデータ型を指定します。
  :sample:
    1 つ以上の例。
  :version_added:
    この戻りは Ansible の初回リリース後に拡張された場合にのみ必要です。たとえば、これはトップレベルの `version_added` フィールドよりも大きくなります。
    これは浮動小数点ではなく文字列です(つまり ``version_added: '2.3'``)。
  :contains:
    任意です。ネストされた戻り値を説明するには、``type: complex``、``type: dict``、または ``type: list``/``elements: dict`` を設定し、各サブフィールドに対して上記を繰り返します。

以下の例は、``RETURN`` セクションを 3 つの単純なフィールドと、複雑なネストされたフィールドを持つ 2 つのセクションです。

    RETURN = r'''
    dest:
        description: Destination file/path.
        returned: success
        type: str
        sample: /path/to/file.txt
    src:
        description: Source file used for the copy on the target machine.
        returned: changed
        type: str
        sample: /home/httpd/.ansible/tmp/ansible-tmp-1423796390.97-147729857856000/source
    md5sum:
        description: MD5 checksum of the file after running copy.
        returned: when supported
        type: str
        sample: 2a5aeecc61dc98c4d780b14b330e3282
    '''

    RETURN = r'''
    packages:
        description: Information about package requirements
        returned: On success
        type: complex
        contains:
            missing:
                description: Packages that are missing from the system
                returned: success
                type: list
                sample:
                    - libmysqlclient-dev
                    - libxml2-dev
            badversion:
                description: Packages that are installed but at bad versions.
                returned: success
                type: list
                sample:
                    - package: libxml2-dev
                      version: 2.9.4+dfsg1-2
                      constraint: ">= 3.0"
    '''

.. _python_imports:

Python のインポート
==============

シバンの後に、UTF-8 コーディング、著作権の行、ライセンス、および ``ANSIBLE_METADATA``、``DOCUMENTATION``、``EXAMPLES``、および ``RETURN`` のセクションの後に、python インポートを追加できます。すべてのモジュールは、以下の形式で Python インポートを使用する必要があります。

.. code-block:: python

   from module_utils.basic import AnsibleModule

``from module_utils.basic import *`` などの「ワイルドカード」インポートが使用できなくなりました。

.. _dev_testing_module_documentation:

モジュールドキュメンテーションのテスト
============================

Ansible ドキュメントをローカルでテストするには、「:ref:`こちらの手順<testing_module_documentation>`」を参照してください。
