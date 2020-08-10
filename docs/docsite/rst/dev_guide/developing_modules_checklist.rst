.. _developing_modules_checklist:
.. _module_contribution:

***********************************
Ansible へのモジュールの貢献
***********************************

モジュールを Ansible に提供する場合は、客観的および主観的な要件を満たしている必要があります。以下の詳細をお読みください。また、:ref:`モジュール開発のヒント <developing_modules_best_practices>` も確認してください。

`メインプロジェクトリポジトリー` <https://github.com/ansible/ansible>_ に受け入れられたモジュールは、すべての Ansible インストールに同梱されます。ただし、メインプロジェクトへの貢献は、モジュールを配信する唯一の方法ではありません。Galaxy のロールにモジュールを埋めこむか、:ref:`ローカルで使用するためにモジュールコードのコピーを単純に共有できます。

Ansible への貢献: 客観的な要件
===============================================

モジュールを Ansible に提供するには、以下を行う必要があります。

* Windows 用の Python または Powershell のいずれかでモジュールを書き込みます。
* ``AnsibleModule`` 共通コードを使用します。
* モジュールが Python 2.7 をサポートできない場合は、``DOCUMENTATION`` の要件セクションで、最低限必要な Python バージョンと根拠を説明します。
* 適切な :ref:`Python 3 構文 <developing_python_3>` を使用します。
* `PEP 8 <https://www.python.org/dev/peps/pep-0008/>`_ Python スタイルの規則に従います。詳細は、:ref:`testing_pep8` を参照してください。
* GPL ライセンス (GPLv3 以降) でモジュールにライセンスを付与します。
* すべての貢献に適用される :ref:`ライセンス契約 <contributor_license_agreement>` を理解します。
* Ansible の :ref:`フォーマットおよびドキュメント <developing_modules_documenting>` の標準仕様に準拠します。
* モジュールの包括的な :ref:`テスト <developing_testing>` が含まれます。
* モジュール依存関係を最小限に抑えます。
* 可能な場合は :ref:`check_mode <check_mode_dry>` をサポートします。
* コードが読み取り可能であることを確認します。
* モジュールが ``<something>_facts`` である場合、その主な目的は ``ansible_facts`` を返すことになります。これを行わないモジュールには ``_facts`` を付けないでください。``ansible_facts`` は、ネットワークインターフェースとその構成、インストールされているオペレーティングシステム、プログラムなど、ホストマシンに固有の情報にのみ使用してください。
* (``ansible_facts`` ではなく) 一般情報をクエリーまたは返すモジュールは、``_info`` という名前にする必要があります。一般情報は、ホストに固有ではない情報です。たとえば、オンラインサービスまたはクラウドサービスに関する情報 (同じホストから同じオンラインサービスで異なるアカウントにアクセス可能)、またはマシンからアクセスできる仮想マシンおよびコンテナーに関する情報などです。

PR または提案を送信する前に、モジュールがこれらの要件を満たしていることを確認してください。質問がある場合は、`Ansible の IRC チャットチャンネル <http://irc.freenode.net>`_ または `Ansible 開発メーリングリスト <https://groups.google.com/group/ansible-devel>`_ をご利用ください。

Ansibleへの貢献: 主観的な要件
================================================

モジュールが目的の要件を満たしている場合には、コードを確認して、明確で簡潔で安全で、保守可能であるかを確認します。モジュールが適切なユーザーエクスペリエンス、役に立つエラーメッセージ、妥当なデフォルトなどを提供するかどうかを検討します。このプロセスは主観的であり、正確な受け入れ基準を記載することはできません。モジュールが Ansible リポジトリーに受け入れられる可能性を高めるには、:ref:`モジュール開発のヒント <developing_modules_best_practices>` に従ってください。

その他のチェックリスト
================

* :ref:`モジュール開発のヒント` <developing_modules_best_practices>
* `Amazon Development checklist` <https://github.com/ansible/ansible/blob/devel/lib/ansible/modules/cloud/amazon/GUIDELINES.md>_
* :ref:`Windows 開発のチェックリスト` <developing_modules_general_windows>
