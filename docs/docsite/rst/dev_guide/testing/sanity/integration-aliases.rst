integration-aliases
===================

統合テストは ``ansible-test`` によって実行され、``test/integration/targets/`` 配下のディレクトリーに置かれます。
各テストには、テストの実行を制御する ``aliases`` ファイルが必要です。

エイリアスについては、以下のセクションで説明します。各エイリアスは、``aliases`` ファイルの別々の行に指定する必要があります。

グループ
------

テストは、必ず 1 つのグループで実行するように設定する必要があります。これは、``aliases`` ファイルに適切なグループを追加することによって行います。

利用可能な一部のグループの例を以下に示します。

- ``shippable/posix/group1``
- ``shippable/windows/group2``
- ``shippable/azure/group3``
- ``shippable/aws/group1``
- ``shippable/cloud/group1``

グループは、複数の CI ジョブ間でテストのバランスを取り、テストのランタイムを最小限にするために使用します。
同様の要件が一緒に実行されるテストを維持することで、効率性も向上します。

新規テスト用にグループを選択する場合は、追加するテストと同様のグループを使用します。
複数のグループが利用可能な場合は、ランダムに 1 つのグループを選択します。

設定
-----

エイリアスは、テストを実行する前に設定ターゲットを実行するのに使用できます。

- ``setup/once/TARGET`` - ターゲット ``TARGET`` を必要とする最初のターゲットの前に実行します。
- ``setup/always/TARGET`` - 必要な各ターゲットの前にターゲット ``TARGET`` を実行します。

要件
------------

エイリアスを使用すると、一部のテスト要件を表現することができます。

- ``needs/privileged`` - ``--docker`` を使用したテストの実行時に ``--docker-privileged`` を必要とします。
- ``needs/root`` - ``root`` または ``--docker`` でテストを実行する必要があります。
- ``needs/ssh`` - パスワードなしで localhost (または ``--docker`` を使用したテストコンテナー) への SSH 接続を必要とします。
- ``needs/httptester`` - テストを実行するために http-test-container を使用する必要があります。

依存関係
------------

一部のテスト依存関係は自動的に検出されます。

- ``meta/main.yml`` ファイルで定義される Ansible ロールの依存関係。
- ``setup/*`` エイリアスで定義されたターゲットのセットアップ。
- あるターゲットから別のターゲットのファイルへのシンボリックリンク。

エイリアスを使用すると、自動的に処理されない依存関係を宣言できます。

- ``needs/target/TARGET`` - テストターゲット ``TARGET`` を使用する必要があります。
- ``needs/file/PATH`` - git root に対して相対的なファイル ``PATH`` を使用する必要があります。

スキップ
--------

エイリアスを使用すると、以下のいずれかを使用してプラットフォームをスキップできます。

- ``skip/freebsd`` - FreeBSD でのテストをスキップ。
- ``skip/osx`` - macOS でのテストをスキップ。
- ``skip/rhel`` - RHEL でのテストをスキップ。
- ``skip/docker`` - Docker コンテナーで実行される場合のテストをスキップ。

``--remote`` オプションで ``/`` を削除して指定したプラットフォームバージョンもスキップできます。

- ``skip/FreeBSD11.1`` - FreeBSD 11.1 でのテストをスキップ。
- ``skip/rhel7.6`` - RHEL 7.6 でのテストをスキップ。

``--windows`` オプションを使用して指定する Windows バージョンもスキップできます。

- ``skip/windows/2008`` - Windows Server 2008 でのテストをスキップ。
- ``skip/windows/2012-R2`` - Windows Server 2012 R2 でのテストをスキップ。

エイリアスを使用すると、以下のいずれかを使用して Python のメジャーバージョンをスキップできます。

- ``skip/python2`` - Python 2.x でのテストをスキップ。
- ``skip/python3`` - Python 3.x でのテストをスキップ。

より詳細なスキップを行うには、インテグレーションテストの Playbook で条件を使用します。以下に例を示します。

.. code-block:: yaml

   when: ansible_distribution in ('Ubuntu')


その他
-------------

その他にも利用できるエイリアスがあります。

- ``destructive`` - ``--docker`` または ``--remote`` なしで実行するには ``--allow-destructive`` が必要です。
- ``hidden`` - 対象は無視されます。依存関係として使用できます。``setup_`` および ``prepare_`` の接頭辞が付いた場合は自動です。

Unstable
--------

安定性が修正されるまで、``unstable`` エイリアスのマークが付けられる必要があるテスト。
これらのテストは、そのテストの下にあるテストまたはモジュールを変更するプル要求に対して実行を継続します。

これにより、他のプル要求に対する不要なテストの失敗や、マージの実行および毎夜の CI ジョブのテストも回避されます。

不安定なテストを手動で実行する方法は 2 つあります。

- ``ansible-test`` に ``--allow-unstable`` オプションを使用します。
- テストを ``ansible-test`` に渡す際に、テスト名の前に ``unstable/`` を付けます。

テストは、Ansible Core Team のメンバーによって不安定としてマークされます。
GitHub issue_ が作成され、それぞれの不安定なテストを追跡します。

Disabled
--------

常に失敗するテストでは、修正されるまで、``disabled`` なエイリアスでマークされる必要があります。

無効にされたテストは自動的に省略されます。

無効にされたテストを手動で実行する方法は 2 つあります。

- ``ansible-test`` に ``--allow-disabled`` オプションを使用します。
- テストを ``ansible-test`` に渡す際に、テスト名の前に ``disabled/`` を付けます。

テストは、Ansible Core Team のメンバーによって無効とマークされます。
GitHub issue_ が作成され、無効にされた各テストを追跡します。

Unsupported
-----------

CI で実行できないテストには、``unsupported`` エイリアスのマークを付ける必要があります。
ほとんどのテストはシミュレーターやクラウドプラグインを使用することでサポートされます。

ただし、テストが使用できない場合は、サポート対象外としてテストをマークすると、CI でテストを実行できなくなります。

サポートされないテストを手動で実行する方法は 2 つあります。

* ``ansible-test`` に ``--allow-unsupported`` オプションを使用します。
* テストを ``ansible-test`` に渡す際に、テスト名の前に ``unsupported/`` を付けます。

テストは、テストの貢献者によって unsupported とマークされます。

クラウド
-----

通常、外部 API へのアクセスを必要とするクラウドサービスおよびその他のモジュールのテストには、CI でのテストに特別なサポートが必要です。

これらには、必要なテストプラグインを指定するために追加のエイリアスが必要です。

利用可能なエイリアスには、以下のものがあります。

- ``cloud/aws``
- ``cloud/azure``
- ``cloud/cs``
- ``cloud/foreman``
- ``cloud/openshift``
- ``cloud/tower``
- ``cloud/vcenter``

未テスト
--------

テストを CI で実行できない場合でも、すべてのモジュールおよびプラグインにインテグレーションテストが含まれる必要があります。

問題
------

unstable_ または disabled_ としてマークされているテストには、テストのステータスを追跡する問題が作成されます。
それぞれの問題は以下のプロジェクトのいずれかに割り当てられます。

- `AWS <https://github.com/ansible/ansible/projects/21>`_
- `Azure <https://github.com/ansible/ansible/projects/22>`_
- `Windows <https://github.com/ansible/ansible/projects/23>`_
- `General <https://github.com/ansible/ansible/projects/25>`_

ご質問はございますか。
---------

インテグレーションテストに関する質問は、GitHub で @mattclay または @gundalow 、または IRC で ``#ansible-devel`` にお問い合わせください。
