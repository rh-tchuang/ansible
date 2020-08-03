タグ
====

Playbook が大きい場合は、
Playbook で *すべて* を実行するのではなく、その特定の部分のみを実行できると便利な場合があります。
Ansible は、この理由により「tags:」属性をサポートします。

タグは、Ansible の *多く* の構造に適用できます (下記の「タグの継承」を参照) が、
最も簡単なのは、個別のタスクを使用することです。以下は、
2 つのタスクに異なるタグを付ける例となります::

    tasks:
    - yum:
        name:
        - httpd
        - memcached
        state: present
      tags:
      - packages

    - template:
        src: templates/src.j2
        dest: /etc/foo.conf
      tags:
      - configuration

Playbook を実行する場合は、次の 2 つの方法でタグに基づいてタスクをフィルタリングできます。

- コマンドラインで、``--tags`` オプションまたは ``--skip-tags`` オプション使用
- Ansible 構成設定で、``TAGS_RUN`` オプションおよび 
  ``TAGS_SKIP`` オプションの使用

たとえば、非常に長い Playbook の「構成」と「パッケージ」の部分だけを実行する場合は、
コマンドラインで ``--tags`` オプションを使用できます。

    ansible-playbook example.yml --tags "configuration,packages"

一方、特定のタグ付きタスク *なし* で Playbook を実行する場合は、
``--skip-tags`` コマンドラインオプションを使用できます。

    ansible-playbook example.yml --skip-tags "packages"

``--list-tasks`` と組み合わせることで、
``--tags`` または ``--skip-tags`` で実行するタスクを確認できます。

    ansible-playbook example.yml --tags "configuration,packages" --list-tasks

.. warning::
    * ファクト収集は、デフォルトで「always」でタグ付けされます。タグを適用して、
      ``--tags`` で別のタグを使用するか、
      ``--skip-tags`` で同じタグを使用する場合にのみ省略されます。

.. _tag_reuse:

タグの再使用
```````````````
複数のタスクに同じタグを適用できます。``--tags`` コマンドラインオプションを使用してプレイを実行すると、
そのタグ名を持つすべてのタスクが実行されます。

この例では、タグ「ntp」がある複数のタスクをタグ付けしています::

    ---
    # file: roles/common/tasks/main.yml

    - name: be sure ntp is installed
      yum:
        name: ntp
        state: present
      tags: ntp

    - name: be sure ntp is configured
      template:
        src: ntp.conf.j2
        dest: /etc/ntp.conf
      notify:
      - restart ntpd
      tags: ntp

    - name: be sure ntpd is running and enabled
      service:
        name: ntpd
        state: started
        enabled: yes
      tags: ntp

.. _tag_inheritance:

タグの継承
```````````````

``tags:`` をプレイに追加、または静的にインポートされたタスクおよびロールに追加すると、
含まれているすべてのタスクにそのタグを追加します。これは *タグの継承
* と呼ばれています。タグの継承は、
``include_role`` や ``include_tasks`` などの動的な包含には *適用されません*。

``tags:`` 属性をタスク以外の構造に適用すると、
Ansible はタグ属性を処理して、その属性に含まれるタスクのみに適用します。
タスク以外の場所にタグを付けるのは利便性のためであり、
個別にタスクにタグを付ける必要はありません。

この例では、2 つのプレイのすべてのタスクにタグを付けています。最初のプレイはすべてのタスクに「bar」のタグが付けられており、
2 番目のプレイにはすべてのタスクに「foo」のタグが付けられています::

    - hosts: all
      tags:
      - bar
      tasks:
        ...

    - hosts: all
      tags: [ foo ]
      tasks:
        ...

また、``roles`` でインポートされたタスクにタグを適用することもできます::

    roles:
      - role: webserver
        vars:
          port:5000
        tags: [ web, foo ]

``import_role:`` ステートメントおよび ``import_tasks:`` ステートメントに追加します::

    - import_role:
        name: myrole
      tags: [ web, foo ]

    - import_tasks: foo.yml
      tags: [ web, foo ]


このタグはすべて、指定されたタグをプレイ、インポートされたファイル、またはロール内の「各」タスクに適用するため、
対応するタグを使用して Playbook が呼び出されたときに、
このタスクを選択的に実行できます。

タグは、依存関係チェーン *に* 適用されます。タグを依存ロールのタスクに継承するには、
タグを、ロール内のすべてのタスクではなく、
ロール宣言または静的インポートに適用する必要があります。

「これらのタグのみをインポートする」方法はありません。
このような機能を探している場合は、おそらくより小さなロール/インクルードに分割する必要があります。

上記の情報は、`include_tasks` または他の動的インクルードには適用されません。
インクルードに適用される属性は、
インクルード自体にのみ影響するためです。

``--list-tasks`` オプションを指定して ``ansible-playbook`` を実行すると、
タスク、ロール、および静的インポートに適用されるタグを確認できます。``--list-tags`` オプションで、
使用可能なすべてのタグを表示できます。

.. note::
    上記の情報は、`include_tasks`、`include_roles`、
    またはその他の動的インクルードには適用されません。これらのいずれかに適用されるタグは、
    インクルード自体にのみタグを付けます。

動的包含を目的としたタスクとロールでタグを使用するには、
必要なすべてのタスクにタスクレベルで明示的にタグを付ける必要があります。
または ``block:`` を使用して一度に複数のタスクにタグを付けることができます。インクルード自体にも、
タグを付ける必要があります。

次に、``block`` ステートメントを使用してロールタスクにタグ ``mytag`` を付け、
動的インクルードで使用する例を示します。

Playbook ファイル::

    - hosts: all
      tasks:
      - include_role:
          name: myrole
        tags: mytag

ロールタスクファイル::

    - block:
      - name:First task to run
        ...
      - name:Second task to run
        ...
      tags:
      - mytag


.. _special_tags:

特別なタグ
````````````

特に省略しない限り、常にタスクを実行する特別な ``always`` タグがあります 
(``--skip-tags always``)。

例:

    tasks:
    - debug:
        msg: "Always runs"
      tags:
      - always

    - debug:
        msg: "runs when you use tag1"
      tags:
      - tag1

.. versionadded:: 2.5

他にも、特別なタグとして ``never`` があります。
これは、タグが特に要求されない限り、タスクを実行しないようにします。

例:

    tasks:
      - debug: msg="{{ showmevar }}"
        tags: [ never, debug ]

この例では、タスクは、``debug`` タグまたは ``never`` 
タグが明示的に要求された場合に限り実行されます。


タグには、``タグ付き``、``タグなし``、
``すべて`` の 3 つの特別なキーワードがあります。
これは、それぞれ「タグ付きのみ」、「タグなしのみ」、または「すべてのタスク」を実行します。

デフォルトでは、Ansible は ``--tags all`` が指定されている時のように実行されます。

.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
