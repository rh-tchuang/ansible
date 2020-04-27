.. _release_and_maintenance:

リリースおよびメンテナンス
=======================

.. contents::
   :local:

.. _release_cycle:

リリースサイクル
\`\`\`\`\`\`\`\`\`\`\`\`\`

Ansible は、柔軟な 6 ヶ月のリリースサイクルで開発、リリースされています。
このサイクルは、大規模な変更を正しく実装して、
テストしてから新しいリリースが公開されるように、延長することが可能です。

Ansible のメンテナンス構造は段階的で、3 つのメジャーリリースまで展開します。
詳細は、「:ref:`development_and_stable_version_maintenance_workflow`」を確認してください。
現行リリースがどの程度維持されているかは、:ref:`release_schedule` の表を参照してください。

メンテナンスされていない Ansible のリリースを使用している場合には、
最新の機能やセキュリティー修正からの恩恵を受けられるように、
できるだけ早くアップグレードすることを強く推奨します。

メンテナンスのない、以前の Ansible バージョンには、
未修正のセキュリティーの脆弱性が含まれている可能性があります (*CVE*)。

Ansible Playbook を更新して新しいバージョンで実行するときのヒントは、「:ref:`移植ガイド<porting_guides>`」
を参照してください。

.. _release_schedule:

リリースのステータス
\`\`\`\`\`\`\`\`\`\`\`\`\`\`
以下の表には、メジャーリリースごとのリリースノートへのリンクが含まれています。このようなリリースノート (changelog) には、各マイナーリリースの日付や、大きな変更が含まれます。

==============================      =================================================
Ansible リリース                     ステータス
==============================      =================================================
devel                               開発中 (未リリースの 2.10 (trunk))
`2.9 リリースノート`_                メンテナンス対象 (セキュリティー **および** 一般的なバグの修正)
`2.8 リリースノート`_                メンテナンス対象 (セキュリティー **および** 重要なバグの修正)
`2.7 リリースノート`_                メンテナンス対象 (セキュリティーの修正)
`2.6 リリースノート`_                メンテナンス対象外 (エンドオフライフ)
`2.5 リリースノート`_                メンテナンス対象外 (エンドオフライフ)
<2.5                                メンテナンス対象外 (エンドオフライフ)
==============================      =================================================

各リリースは、`<https://releases.ansible.com/ansible/>`_ からダウンロードできます。

.. note:: Ansible は、リリース 3 回分、メンテナンスされます。 つまり、最新の Ansible リリースでは、その最新のリリースが最初にリリースされた時はセキュリティーおよび一般的なバグ修正が含まれます。
    その次のバージョンがリリースされるときは、セキュリティーおよび重要なバグ修正が含まれます。
    その次のバージョンがリリースされるときは、セキュリティー修正 **のみ** が提供されます。

..Comment: devel はこちらを参照していましたが、
   現在 changelog プロセスを改定中で devel 用の静的な changelog へのリンクはありません。_2.6: https://github.com/ansible/ansible/blob/devel/CHANGELOG.md
.. _2.9 Release Notes:
.. _2.9: https://github.com/ansible/ansible/blob/stable-2.9/changelogs/CHANGELOG-v2.9.rst
.. _2.8 Release Notes:
.. _2.8: https://github.com/ansible/ansible/blob/stable-2.8/changelogs/CHANGELOG-v2.8.rst
.. _2.7 Release Notes: https://github.com/ansible/ansible/blob/stable-2.7/changelogs/CHANGELOG-v2.7.rst
.. _2.6 Release Notes:
.. _2.6: https://github.com/ansible/ansible/blob/stable-2.6/changelogs/CHANGELOG-v2.6.rst
.. _2.5 Release Notes: https://github.com/ansible/ansible/blob/stable-2.5/changelogs/CHANGELOG-v2.5.rst

.. _support_life:
.. _methods:

.. _development_and_stable_version_maintenance_workflow:

開発版および安定版のメンテナンスワークフロー
\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

Ansible コミュニティーは、GitHub_ で Ansible を開発してメンテナンスしましす。

新しいモジュール、プラグイン、機能、バグ修正は常に、
Ansible の次のメジャーバージョンに統合されます。このような作業内容は ``devel`` git ブランチで追跡されます。

Ansible は、最新のメジャーリリースにバグ修正とセキュリティーの強化機能を提供します。1 つ前のメジャーリリースには、
セキュリティーの問題と重要なバグに対する修正のみが提供されます。Ansible は、
リリース 2 回分に対してのみ、セキュリティー修正が適用されます。このような作業内容は、
``stable-<version>`` git ブランチで追跡されます。

メンテナンス対象の安定版のブランチに保存された修正は、
最終的に必要に応じて新しいバージョンとしてリリースされます。

メンテナンス対象外の Ansible リリースに修正が提供されるという保証はありませんが、
重要な問題については例外対応となる可能性がある点に注意してください。

.. _GitHub: https://github.com/ansible/ansible

.. _release_changelogs:

Changelog
~~~~~~~~~~

Ansible 2.5 以降、フラグメントベースで changelog を生成しています。ここでは、2.9_ 向けに生成された changelog を例として紹介します。新機能や、バグ修正の作成時に、変更内容を記述した changelog フラグメントが作成されます。新しいモジュールまたはプラグインには、changelog のエントリーは必要ありません。このようなアイテムの詳細は、モジュールのドキュメントから生成されます。

コミュニティーガイドに、:ref:`changelog フラグメントの作成例および手順<changelogs_how_to>` が記載されています。

以前のバージョンは、``stable-<version>`` branches at ``stable-<version>/CHANGELOG.md`` ブランチで変更内容が記録されます。たとえば、以下は GitHub の `2.4 <https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md>`_ の changelog です。


Release Candidate (リリースの候補)
~~~~~~~~~~~~~~~~~~

Ansible の新規リリースまたはバージョンを公開する前に、
一般的には Release Candidate プロセスを行います。

このプロセスでは、Ansible コミュニティーは、Ansible をテストして、
今後発生する可能性のあるバグや修正を報告する機会があります。

Ansible は最初の Release Candidate (``RC1``) とタグ付けします。
通常、RC はリリース前の最後の 5 営業日にスケジュールされます。この期間に主要なバグや問題が特定されない場合には、
最終的にリリースされます。

最初の Candidate に主要な問題がある場合には、必要な修正がプッシュされた時点で、
2 番目の Candidate (``RC2``) のタグが付けられます。
2 番目の Candidare は、1 番目よりも期間は短くなります。
2 営業日が経過して問題が報告されない場合には、
最終的にリリースされます。

Ansible の中核となるメンテナーが最終リリース前に修正が必要とみなしたバグが有る場合には、
必要に応じて Release Candidate のタグを
さらに付けることができます。

.. _release_freezing:

機能フリーズ
~~~~~~~~~~~~~~

保留中の Release Candidate がある場合、
中核となる開発者やメンテナーは、Release Candidate に向けた修正に焦点を当てます。

できるだけ早く新規リリースを公開できるように、
Release Candidate に関連のない新機能や修正のマージが遅れる可能性があります。


非推奨サイクル
\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`\`

通常、再実装してジョブ実行の改善を希望する場合に、時には機能を削除する必要があります。
これを実現するために非推奨サイクルがあります。まず、機能を「非推奨」とマークします。これは通常、警告を付けて非推奨とした理由、
切り替え先の機能、
完全に機能を削除するタイミング (バージョン) をユーザーに通知します。

サイクルは通常、4 つの機能リリース (2.x.y (x は機能リリースで、y はバグ修正リリース)) となっており、
通常、非推奨の通知をしてから 4 番目のリリースでその機能は削除されます。
たとえば、2.7 で非推奨になった機能は 2.11 に削除されます (この間にリリースが 3.x にならなかった場合)。
トラッキングは、リリース番号ではなく、リリースの回数と関連があります。

モジュール/プラグインについては、以前のバージョンをご利用の方のために、削除後もドキュメントは保持します。

.. seealso::

   :ref:`community_committer_guidelines`
       Ansible で中核となる貢献者およびメンテナー向けガイドライン
   :ref:`testing_strategies`
       ストラテジーのテスト
   :ref:`ansible_community_guide`
       コミュニティー情報および貢献
   `Ansible リリースの tarball <https://releases.ansible.com/ansible/>`_
       Ansible リリースの tarball
   `開発メーリングリスト <https://groups.google.com/group/ansible-devel>`_
       開発トピックのメーリングリスト
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel
