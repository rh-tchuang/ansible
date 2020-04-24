
.. \_developing\_resource\_modules:

***********************************
ネットワークリソースモジュールの開発
***********************************

.. contents::
  :local:

リソースモジュールビルダーは、開発者のスキャフォールディングおよび Ansible ネットワークリソースモジュールの維持に役立つ Ansible Playbook です。

リソースモジュールビルダーには以下の機能があります。

- 定義されたモデルを使用して、リソースモジュールディレクトリーのレイアウトと初期クラスファイルをスキャフォールディングします。
- Ansible ロールまたはコレクションのいずれかをスキャフォールディングします。
- その後にリソースモジュールビルダーを使用すると、モジュール arspec と、モジュール docstring を含むファイルのみが置き換えられます。
- モデルとともに複雑な例を同じディレクトリーに保存できます。
- モジュール用の信頼できるソースとしてモデルを維持し、必要に応じてリソースモジュールビルダーを使用してソースファイルを更新します。
- ``<network_os>_<resource>`` および ``<network_os>_facts`` の両方について作業サンプルモジュールを生成します。

リソースモジュールビルダーへのアクセス
=====================================

リソースモジュールビルダーにアクセスするには、以下を実行します。

1. github リポジトリーのクローンを作成します。

  .. code-block:: bash

    git clone https://github.com/ansible-network/resource\_module\_builder.git

2. 要件をインストールします。

  .. code-block:: bash

    pip install -r requirements.txt

モデルの作成
================

新規リソースのモデルを作成する必要があります。リソースモジュールビルダーはこのモデルを使用して以下を作成します。

* 新しいモジュールのスキャフォールディング
* 新しいモジュールの argspec
* 新しいモジュールの docstring

その後、モデルは argspec と docstring の両方に対する 1 つのソースであり、それらを同期します。リソースモジュールビルダーを使用して、このスキャフォールディングを生成します。モジュールに対する後続の更新の場合は、最初にモデルを更新し、リソースモジュールビルダーを使用してモジュールの argspec および docstring を更新します。

たとえば、リソースモデルビルダーには、以下のように :file:`models` ディレクトリーに ``myos_interfaces.yml`` サンプルが含まれます。

.. code-block:: yaml

  ---
  GENERATOR\_VERSION:'1.0'
  ANSIBLE\_METADATA: |
      {
          'metadata\_version':'1.1',
          'status': \['preview'],
          'supported\_by': '<support\_group>'
      }
  NETWORK\_OS: myos
  RESOURCE: interfaces
  COPYRIGHT:Copyright 2019 Red Hat
  LICENSE: gpl-3.0.txt

  DOCUMENTATION: |
    module: myos\_interfaces
    version\_added:2.9
    short\_description:'Manages <xxxx> attributes of <network\_os> <resource>'
    description:'Manages <xxxx> attributes of <network\_os> <resource>.'
    author:Ansible Network Engineer
   notes:
      \- 'Tested against <network\_os> <version>'
    options:
      config:
        description:The provided configuration
        type: list
        elements: dict
        suboptions:
          name:
            type: str
            description:The name of the <resource>
          some\_string:
            type: str
            description:
            \- The some\_string\_01
            choices:
            \- choice\_a
            \- choice\_b
            \- choice\_c
            default: choice\_a
          some\_bool:
            description:
            \- The some\_bool.
            type: bool
          some\_int:
            description:
            \- The some\_int.
            type: int
            version\_added:'1.1'
          some\_dict:
            type: dict
            description:
            \- The some\_dict.
            suboptions:
              property\_01:
                description:
                \- The property\_01
                type: str
      state:
        description:
        \- The state of the configuration after module completion.
        type: str
        choices:
        \- merged
        \- replaced
        \- overridden
        \- deleted
        default: merged
  EXAMPLES:
    \- deleted\_example\_01.txt
    \- merged\_example\_01.txt
    \- overridden\_example\_01.txt
    \- replaced\_example\_01.txt

リソースが対応するそれぞれの状態の例を含める必要があります。リソースモジュールビルダーも、サンプルモデルにこれを追加します。

その他の例は、「`Ansible ネットワークリソースモデル <https://github.com/ansible-network/resource_module_models>`\_」を参照してください。

リソースモジュールビルダーの使用
=================================

リソースモジュールビルダーを使用して、リソースモデルからコレクションのスキャフォールディングを作成するには、以下を実行します。

.. code-block:: bash

  ansible-playbook -e rm\_dest=<destination for modules and module utils>\
                   -e structure=collection \
                   -e collection\_org=<collection\_org> \
                   -e collection\_name=<collection\_name> \
                   -e model=<model>\
                   site.yml

パラメーターは以下のようになります。

- ``rm_dest``: リソースモジュールビルダーがリソースモジュールおよびファクトモジュールのファイルとディレクトリーを置くディレクトリー。
- ``structure``: ディレクトリーレイアウトの種類 (ロールまたはコレクション)

  - ``role``: ロールディレクトリーレイアウトを生成します。
  - ``collection``: コレクションディレクトリーのレイアウトを生成します。

- ``collection_org``: `structure=collection` の場合に必要となるコレクションの組織です。
- ``collection_name``: `structure=collection` の場合に必要となるコレクションの名前。
- ``model``: モデルファイルへのパス。

リソースモジュールビルダーを使用してロールのスキャフォールディングを作成するには、以下を実行します。

.. code-block:: bash

  ansible-playbook -e rm\_dest=<destination for modules and module utils>\
                   -e structure=role \
                   -e model=<model>\
                   site.yml

例
========

コレクションディレクトリーのレイアウト
---------------------------

以下の例では、以下のディレクトリーレイアウトを示しています。

- ``network_os``: myos
- ``resource``: interfaces

.. code-block:: bash

  ansible-playbook -e rm\_dest=~/github/rm\_example \
                   -e structure=collection \
                   -e collection\_org=cidrblock \
                   -e collection\_name=my\_collection \
                   -e model=models/myos/interfaces/myos\_interfaces.yml \
                   site.yml

.. code-block:: text

  ├── docs
  ├── LICENSE.txt
  ├── playbooks
  ├── plugins
  |   ├── action
  |   ├── filter
  |   ├── inventory
  |   ├── modules
  |   |   ├── __init__.py
  |   |   ├── myos\_facts.py
  |   |   └──  myos\_interfaces.py
  |   └──  module\_utils
  |       ├── __init__.py
  |       └──  network
  |           ├── __init__.py
  |           └──  myos
  |               ├── argspec
  |               |   ├── facts
  |               |   |   ├── facts.py
  |               |   |   └──  __init__.py
  |               |   ├── __init__.py
  |               |   └──  interfaces
  |               |       ├── __init__.py
  |               |       └──  interfaces.py
  |               ├── config
  |               |   ├── __init__.py
  |               |   └──  interfaces
  |               |       ├── __init__.py
  |               |       └──  interfaces.py
  |               ├── facts
  |               |   ├── facts.py
  |               |   ├── __init__.py
  |               |   └──  interfaces
  |               |       ├── __init__.py
  |               |       └──  interfaces.py
  |               ├── __init__.py
  |               └──  utils
  |                   ├── __init__.py
  |                   └──  utils.py
  ├── README.md
  └──  roles


ロールディレクトリーのレイアウト
---------------------

この例では、以下のロールのディレクトリーレイアウトを表示しています。

- ``network_os``: myos
- ``resource``: interfaces

.. code-block:: bash

  ansible-playbook -e rm\_dest=~/github/rm\_example/roles/my\_role \
                   -e structure=role \
                   -e model=models/myos/interfaces/myos\_interfaces.yml \
                   site.yml


.. code-block:: text

    roles
    └── my_role
        ├── library
        │   ├── __init__.py
        │   ├── myos_facts.py
        │   └── myos_interfaces.py
        ├── LICENSE.txt
        ├── module_utils
        │   ├── __init__.py
        │   └── network
        │       ├── __init__.py
        │       └── myos
        │           ├── argspec
        │           │   ├── facts
        │           │   │   ├── facts.py
        │           │   │   └── __init__.py
        │           │   ├── __init__.py
        │           │   └── interfaces
        │           │       ├── __init__.py
        │           │       └── interfaces.py
        │           ├── config
        │           │   ├── __init__.py
        │           │   └── interfaces
        │           │       ├── __init__.py
        │           │       └── interfaces.py
        │           ├── facts
        │           │   ├── facts.py
        │           │   ├── __init__.py
        │           │   └── interfaces
        │           │       ├── __init__.py
        │           │       └── interfaces.py
        │           ├── __init__.py
        │           └── utils
        │               ├── __init__.py
        │               └── utils.py
        └── README.md


コレクションの使用
--------------------

以下の例は、生成されたコレクションを Playbook で使用する方法を示しています。

 .. code-block:: yaml

     ----
     - hosts: myos101
       gather_facts:False
       tasks:
       - cidrblock.my_collection.myos_interfaces:
         register: result
       - debug:
           var: result
       - cidrblock.my_collection.myos_facts:
       - debug:
           var: ansible_network_resources


ロールの使用
--------------

以下の例は、生成されたロールを Playbook で使用する方法を示しています。

.. code-block:: yaml

    - hosts: myos101
      gather_facts:False
      roles:
      - my_role

    - hosts: myos101
      gather_facts:False
      tasks:
      - myos_interfaces:
        register: result
      - debug:
          var: result
      - myos_facts:
      - debug:
          var: ansible_network_resources


リソースモジュール構造およびワークフロー
======================================

リソースモジュール構造には、以下のコンポーネントが含まれます。

モジュール
    * ``library/<ansible_network_os>_<resource>.py``.
    * ``module_utils`` リソースパッケージをインポートし、``execute_module`` API を呼び出します。

    .. code-block:: python

      def main():
          result = <resource_package>(module).execute_module()

argspec モジュール
    * ``module_utils/<ansible_network_os>/argspec/<resource>/``.
    \* リソース用の argspec

ファクト
    * ``module_utils/<ansible_network_os>/facts/<resource>/``.
    \* リソースのファクトを入力します。
    ``get_facts`` API が全サブセットを同期するリソースモジュールに対して ``<ansible_network_os>_facts`` モジュールおよびファクトを維持するための ``module_utils/<ansible_network_os>/facts/facts.py`` のエントリー
    \* Facts コレクションを機能させるには、``module_utils/<ansible_network_os>/facts/facts.py`` の FACTS\_RESOURCE\_SUBSETS 一覧にあるリソースサブセットのエントリー

module\_utils のモジュールパッケージ
    * ``module_utils/<ansible_network_os>/<config>/<resource>/``.
    \* 設定をデバイスに読み込み、鍵の ``changed``、``commands``、``before``、および ``after`` を使用して、デバイスへの設定を読み込み、結果を生成する ``execute_module`` API を実装します。
    * ``<resource>`` 設定のファクトを返す ``get_facts`` API を呼び出すか、デバイスに onbox diff サポートがある場合はその相違点を返します。
    \* diff がサポートされていない場合は、収集されるファクトと、指定される鍵/値を比較します。
    \* 最後の設定を生成します。

ユーティリティー
    * ``module_utils/<ansible_network_os>/utils``.
    * ``<ansible_network_os>`` プラットフォームのユーティリティー

開発者ノート
===============

このテストは、リソースモジュールビルダーが生成したロールに依存します。リソースモジュールビルダーに変更を加えた後には、ロールを再生成し、必要に応じてテストを変更して実行します。変更後にロールを生成するには、以下を実行します。

.. code-block:: bash

  rm -rf rmb\_tests/roles/my\_role
  ansible-playbook -e rm\_dest=./rmb\_tests/roles/my\_role \
                   -e structure=role \
                   -e model=models/myos/interfaces/myos\_interfaces.yml \
                   site.yml
