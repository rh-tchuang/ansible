:orphan:

.. _testing_integration:

*****************
統合テスト
*****************

.. contents:: トピック

Ansible 統合テストシステム。

Playbook による Playbook のテスト

テストによっては認証情報が必要になる場合があります。 認証情報は `credentials.yml` で指定できます。

テストによっては root が必要になる場合があります。

クイックスタート
===========

python パッケージ ``argcomplete`` をインストールし、アクティベートすることが強く推奨されます。
これにより、テストランナー ``ansible-test`` に ``bash`` のタブ補完が提供されます。

構成
=============

ansible-test コマンド
--------------------

以下の例では、``bin/`` が ``$PATH`` にあることを前提としています。それを行う簡単な方法は、
``env-setup`` コマンドで環境を初期化します。

    source hacking/env-setup
    ansible-test --help

``ansible-test`` は、完全パスで呼び出すこともできます。

    bin/ansible-test --help

integration_config.yml
----------------------

独自のバージョンの ``integration_config.yml`` を作成すると、
調整可能なパラメーターを設定して、自分の環境でより良いテストを実行する助けとなります。 一部のテスト (例: クラウド) は、
アクセス認証情報が提供されている場合に限り実行します。 サポートされている認証情報の詳細は、
``test/integration/`` ディレクトリーにある、
各種ファイル ``cloud-config-*.template`` を参照してください。

要件
=============

いくつかのテストでは、hg、svn、git のようなものがインストールされていて、パスに入っていることを前提としています。 (Amazon Web Services 用のものなどの) 一部のテストでは、
個別の定義が必要になります。
これは、本ガイドの後半に記載されています。

(完全はリストは後に追加されます)

非破壊テスト
=====================

これらのテストはサブディレクトリー内のファイルを修正しますが、
パッケージやテストのサブディレクトリー以外にあるものをインストールしたり削除したりするようなことはしません。 また、システムサービスの再設定やバウンスも行いません。

.. note:: Docker 内での統合テストの実行

   統合テストによる潜在的な変更からシステムを守り、適切な依存関係セットが利用可能になるようにするには、常に ``--docker`` オプションをつけて統合テストを実行することが推奨されます。オプションについては、「`サポートされる docker イメージの一覧 <https://github.com/ansible/ansible/blob/devel/test/lib/ansible_test/_data/completion/docker.txt>`_」を参照してください。

.. note:: 新規 Docker イメージのプルの回避

   最新のコンテナーイメージをプルしないようにするには、``--docker-no-pull`` オプションを使用します。これは、ダウンロードに利用できないカスタムのローカルイメージを使用する場合に必要です。

CI システムで実行されたすべての POSIX プラットフォームテストに対して、次を実行します。

    ansible-test integration --docker fedora29 -v shippable/

個々のモジュールなど、特定のテストを対象とすることもできます。

    ansible-test integration -v ping

利用可能なターゲットの一覧を表示するには、以下のコマンドを実行します。

    ansible-test integration --list-targets

.. note:: Bash ユーザー

   ``argcomplete`` で ``bash`` を使用する場合は、``ansible-test integration <tab><tab>`` を実行して完全な一覧を取得します。

破壊テスト
=================

これらのテストでは、いくつかの簡単なパッケージのインストールと削除が許可されています。 おそらく、Docker のような仮想環境に、
これらを割り当てたいと考えるでしょう。 ファイルシステムを再フォーマットすることはありません。

    ansible-test integration --docker fedora29 -v destructive/

Windows テスト
=============

これらのテストには、``winrm`` 接続プラグインと Windows モジュールが使用されます。 テストに使用するリモートの Windows 2008 Server、
または Windows 2012 Server でインベントリーを定義して、
PowerShell Remoting を有効にして継続する必要があります。

これらのテストを実行すると、Windows ホストが変更される可能性があるため、
実稼働環境や重要な Windows 環境では実行しないでください。

PowerShell Remoting を有効にします (リモートデスクトップを介して Windows ホストで実行します)::

    Enable-PSRemoting -Force

Windows インベントリーを定義します。

    cp inventory.winrm.template inventory.winrm
    ${EDITOR:-vi} inventory.winrm

CI システムで実行する Windows テストを実行します::

    ansible-test windows-integration -v providepable/

Docker コンテナーでのテスト
==========================

Docker がインストールされた Linux システムをお持ちの場合は、
Ansible の継続的インテグレーション (CI) システムで使用されているものと同じ Docker コンテナーを使用して統合テストを実行することが推奨されます。

.. note:: Linux 以外の Docker

   Docker Engine を使用して (macOS などの) Linux 以外のホストで Docker を実行することは推奨されません。
   テストに使用されるイメージによっては、テストが失敗する場合があります。
   (``network-integration`` または ``windows-integration`` ではなく) ``integration`` の実行時に ``--docker-privileged`` オプションを使用すると、問題が解決する可能性があります。

統合テストの実行
-------------------------

Ubuntu 16.04 コンテナー内の POSIX プラットフォームに CI 統合テストターゲットすべてを実行するには、次のコマンドを実行します。

    ansible-test integration --docker ubuntu1604 -v shippable/

特定のテストを実行することも、別の Linux ディストリビューションを選択することもできます。
たとえば、Ubuntu 14.04 コンテナーで ``ping`` モジュールのテストを実行するには、次を実行します。

    ansible-test integration -v ping --docker ubuntu1404

コンテナーイメージ
----------------

Python 2
````````

ほとんどのコンテナーイメージは、Python 2 でテストするためのものです。

  - centos6
  - centos7
  - fedora28
  - opensuse15py2
  - ubuntu1404
  - ubuntu1604

Python 3
````````

Python 3 でテストするには、以下のイメージを使用します。

  - fedora29
  - opensuse15
  - ubuntu1604py3
  - ubuntu1804


レガシーのクラウドテスト
==================

一部のクラウドテストは通常の統合テストとして実行され、その他はレガシーテストとして実行されます。
詳細は、「:ref:`testing_integration_legacy`」ページを参照してください。


クラウドテストのその他の設定
===================================

テストを実行するには、
test/integration ディレクトリーに、
``cloud-config-aws.yml`` または ``cloud-config-cs.ini`` という名前のファイルにアクセス認証情報を指定する必要があります。構文ヘルプでは、対応する .template ファイルを利用できます。 新しい AWS テストは、
test/integration/cloud-config-aws.yml ファイルを使用するようになりました。

AWS の IAM ポリシー
====================

AWS アカウントでテストを実行するには、Ansible にはかなり幅広い権限が必要になります。 この権限は専用ユーザーに提供できます。テストを実行する前に設定する必要があります。

testing-policies
----------------

``hacking/aws_config/testing_policies`` には、既存のすべての AWS モジュールテストに必要なポリシーのセットが含まれます。
Playbook ``hacking/aws_config/setup_iam.yml`` を使用すると、これらのポリシーをすべて IAM グループに追加できます。
これには、``-e iam_group=GROUP_NAME`` を使用します。グループの作成が完了したら、ユーザーを作成し、
ユーザーをグループのメンバーにする必要があります。ポリシーは、そのユーザーの権限を最小限に抑えるために設計されています。 このポリシーではユーザーを 1 つのリージョンに制限していますが、
完全にユーザーを制限しているわけではないことに注意してください 
(主に Amazon ARN 表記の制限のため)。ユーザーにはアカウント定義を閲覧するための幅広い権限が与えられ、
テストに関係のない一部のリソースを管理することもできます (例えば、別の名前の AWS ラムダなど)。 どのような場合でも、
本番環境のプライマリーのアカウントでは、テストを実行しないでください。

その他の必要な定義
--------------------------

ポリシーをインストールしてテストを実行しているユーザ ID に付与する以外に、
ラムダの基本実行権限を持つラムダロール `ansible_integration_tests` 
を作成する必要があります。


ネットワークテスト
=============

Ansible 2.4 以降、すべてのネットワークモジュールには、すべての機能をカバーするユニットテストが含まれていなければなりません。新しいネットワークモジュールごと、および追加された機能ごとにユニットテストを追加する必要があります。ユニットテストとコードは 1 つの PR にまとめて提出してください。統合テストも強く推奨されます。

ネットワーク統合テストの作成
---------------------------------

ネットワークテストの記述に関するガイダンスは、「`adding tests for Network modules guide <https://github.com/ansible/community/blob/master/group-network/network_test.rst>`_」を参照してください。


ネットワーク統合テストのローカルでの実行
-----------------------------------------

Ansible では Shippable を使用して、その PR で導入された新しいテストも含め、すべての PR で統合テストスイートを実行します。ネットワークモジュールの問題を見つけて修正するには、PR を提出する前にローカルでネットワーク統合テストを実行します。

ネットワーク統合テストを実行するには、次の形式でコマンドを使用します。

    ansible-test network-integration --inventory /path/to/inventory tests_to_run

まず、ネットワークインベントリーファイルを定義します。

    cd test/integration
    cp inventory.network.template inventory.networking
    ${EDITOR:-vi} inventory.networking
    # Add in machines for the platform(s) you wish to test

特定のプラットフォームでネットワークテストをすべて実行するには、次のコマンドを実行します。

    ansible-test network-integration --inventory  /path/to/ansible/test/integration/inventory.networking vyos_.*

この例では、すべての VyOS モジュールに対して実行されます。``vyos_.*`` は、bash ワイルドカードではなく正規表現の一致であることに注意してください。この例を変更した場合は、`.` を含めます。


特定のモジュールに対してインテグレーションテストを実行するには、次のコマンドを実行します。

    ansible-test network-integration --inventory  /path/to/ansible/test/integration/inventory.networking vyos_vlan

特定のモジュールでテストケースを 1 つ実行するには、次を実行します。

    # Only run vyos_vlan/tests/cli/basic.yaml
    ansible-test network-integration --inventory  /path/to/ansible/test/integration/inventory.networking vyos_vlan --testcase basic

特定のトランスポートでインテグレーションテストを実行するには、次を実行します。

    # Only run nxapi test
    ansible-test network-integration --inventory  /path/to/ansible/test/integration/inventory.networking  --tags="nxapi" nxos_.*

    # Skip any cli tests
    ansible-test network-integration --inventory  /path/to/ansible/test/integration/inventory.networking  --skip-tags="cli" nxos_.*

`テストに実装する方法は、`test/integration/targets/nxos_bgp/tasks/main.yaml <https://github.com/ansible/ansible/blob/devel/test/integration/targets/nxos_bgp/tasks/main.yaml>`_ を参照してください。

その他のオプションは、次のコマンドを実行すれば確認できます。

    ansible-test network-integration --help

本書で示したもの以外にヘルプやフィードバックが必要な場合は、Freenode の ``#ansible-network`` にアクセスしてください。


その他の詳細情報
======================

Ansible テストを改善する詳細な計画を確認したい場合は、「`Testing Working Group <https://github.com/ansible/community/blob/master/meetings/README.md>`_」にご参加ください。
