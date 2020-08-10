.. _rebase_guide:

***********************
プル要求のリベース
***********************

プル要求 (PR) が古いため、リベースが必要になる場合があります。これにはいくつかの理由が考えられます。

- PR で変更されたファイルは、すでにマージされている変更と競合しています。
- PR は、自動化されたテストインフラストラクチャーに大きな変更が行われたのに十分なサイズです。

PR を作成するのに使用するブランチを再設定すると、この両方の問題が解決されます。

リモートの設定
========================

PR をリベースする前に、適切なリモートが設定されていることを確認する必要があります。
通常の方法でフォークをクローンしたと仮定すると、``作成元`` のリモートはフォークを指定します。

   $ git remote -v
   origin  git@github.com:YOUR_GITHUB_USERNAME/ansible.git (fetch)
   origin  git@github.com:YOUR_GITHUB_USERNAME/ansible.git (push)

ただし、アップストリームのリポジトリーを参照するリモートを追加する必要もあります。

   $ git remote add upstream https://github.com/ansible/ansible.git

次のリモートを残す必要があります。

   $ git remote -v
   origin  git@github.com:YOUR_GITHUB_USERNAME/ansible.git (fetch)
   origin  git@github.com:YOUR_GITHUB_USERNAME/ansible.git (push)
   upstream        https://github.com/ansible/ansible.git (fetch)
   upstream        https://github.com/ansible/ansible.git (push)

ブランチのステータスを確認すると、``作成元`` のリモートのフォークが最新の状態であることを理解できます。

   $ git status
   On branch YOUR_BRANCH
   Your branch is up-to-date with 'origin/YOUR_BRANCH'.
   nothing to commit, working tree clean

ブランチのリベース
====================

``アップストリーム`` のリモートを設定したら、PR のブランチをリベースできます。

   $ git pull --rebase upstream devel

これにより、アップストリームの ``devel`` ブランチで変更したブランチに変更が再プレイされます。
マージの競合が発生した場合は、続行する前に解決するように求められます。

リベースすると、ブランチのステータスが以下のように変わります。

   $ git status
   On branch YOUR_BRANCH
   Your branch and 'origin/YOUR_BRANCH' have diverged,
   and have 4 and 1 different commits each, respectively.
     (use "git pull" to merge the remote branch into yours)
   nothing to commit, working tree clean

リベースはこれで正常です。``git pull`` を使用するには ``git status`` 命令を無視します。
次のセクションでは、次の作業を説明します。

プル要求の更新
==========================

ブランチをリベースしたら、変更を GitHub にプッシュして、PR を更新する必要があります。

git 履歴を再書き込みするため、強制的にプッシュする必要があります。

   $ git push --force-with-lease

GitHub の PR が更新されました。これにより、変更のテストが自動的にトリガーされます。
テスト完了後に PR のステータスを確認し、さらなる変更が必要であるかどうかを確認する必要があります。

ヘルプの再ベース
=====================

PR またはその他の開発関連の質問を再設定する際には、`freenode.net <https://freenode.net>`_ で #ansible-devel IRC チャットチャンネルに参加します。

.. seealso::

   :ref:`community_development_process`
       ロードマップ、オープン PRS、Ansibullbot などに関する情報
