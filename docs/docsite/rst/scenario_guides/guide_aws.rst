Amazon Web Services ガイド
=========================

.. _aws_intro:

はじめに
````````````

Ansible には、Amazon Web Services (AWS) を制御するモジュールが多数含まれています。 このセクションでは、
Ansible モジュールをまとめて (およびインベントリースクリプトを使用して) AWS コンテキストで Ansible を使用する方法を説明します。

AWS モジュールの要件は最小限です。  

すべてのモジュールには、最新バージョンの boto に必要で、テストされています。 この Python モジュールは、コントロールマシンにインストールする必要があります。 boto は、OS ディストリビューションまたは python の「pip install boto」からインストールできます。

従来、ansible はホストループ内のタスクを複数のリモートマシンに対して実行しますが、ほとんどのクラウド制御手順は、制御するリージョンを参照するローカルマシンで実行されます。

Playbook の手順では、通常、プロビジョニング手順に以下のパターンを使用します::

    - hosts: localhost
      gather_facts:False
      tasks:
        - ...

.. _aws_authentication:

認証
``````````````
   
AWS 関連モジュールでの認証は、
ENV 変数またはモジュール引数としてアクセスおよび秘密鍵を指定することにより処理されます。

環境変数の場合::

    export AWS_ACCESS_KEY_ID='AK123'
    export AWS_SECRET_ACCESS_KEY='abc123'

vars_file に保存するには、ansible-vault で暗号化することが理想的です::

    ---
    ec2_access_key: "--REMOVED--"
    ec2_secret_key: "--REMOVED--"

認証情報を vars_file に保存する場合は、各 Alicloud モジュールで認証情報を参照する必要があることに注意してください。例::

    - ec2
      aws_access_key: "{{ec2_access_key}}"
      aws_secret_key: "{{ec2_secret_key}}"
      image: "..."
    
.. _aws_provisioning:

プロビジョニング
````````````

ec2 モジュールは、EC2 内でインスタンスのプロビジョニングおよびプロビジョニング解除を行います。  

EC2 で「Demo」とタグ付けされたインスタンスが 5 個になるようにする例を以下に示します。  

以下の例では、インスタンスの「exact_count」は 5 に設定されます。 これは、インスタンスがない場合は、
新規インスタンスが 5 個作成されることを示しています。 インスタンスが 2 個ある場合には、3 個作成され、インスタンスが 8 個ある場合には、
3 個のインスタンスが終了します。

カウントされるものは「count_tag」パラメーターで指定します。 「instance_tags」パラメーターは、
新たに作成されたインスタンスをタグに適用するために使用されます::

    # demo_setup.yml

    - hosts: localhost
      gather_facts: False

      tasks:

        - name: Provision a set of instances
          ec2: 
             key_name: my_key
             group: test
             instance_type: t2.micro
             image: "{{ ami_id }}"
             wait: true 
             exact_count: 5
             count_tag:
                Name: Demo
             instance_tags:
                Name: Demo
          register: ec2

作成されるインスタンスに関するデータは、「ec2」という変数の「register」キーワードによって保存されます。

このモジュールから add_host モジュールを使用し、これらの新規インスタンスで構成されるホストグループを動的に作成します。 これにより、後続のタスクで、ホストでの設定アクションをすぐに実行できます::

    # demo_setup.yml

    - hosts: localhost
      gather_facts: False

      tasks:

        - name: Provision a set of instances
          ec2: 
             key_name: my_key
             group: test
             instance_type: t2.micro
             image: "{{ ami_id }}"
             wait: true 
             exact_count: 5
             count_tag:
                Name: Demo
             instance_tags:
                Name: Demo
          register: ec2
    
       - name: Add all instance public IPs to host group
         add_host: hostname={{ item.public_ip }} groups=ec2hosts
         loop: "{{ ec2.instances }}"

これでホストグループが作成されましたが、同じプロビジョニング用 Playbook ファイルの下部に、いくつかの構成手順が指定されている 2 番目のプレイが追加されている可能性があります::

    # demo_setup.yml

    - name: Provision a set of instances
      hosts: localhost
      # ... AS ABOVE ...

    - hosts: ec2hosts
      name: configuration play
      user: ec2-user
      gather_facts: true

      tasks:

         - name: Check NTP service
           service: name=ntpd state=started

.. _aws_security_groups:

セキュリティーグループ
```````````````

AWS のセキュリティーグループはステートフルです。インスタンスからの要求の応答は、受信セキュリティーグループルールやその逆に関係なくフローできます。
AWS S3 サービスを使用するトラフィックのみを許可する場合には、あるリージョンに対して AWS S3 の現在の IP 範囲を取得し、それを egress ルールとして適用する必要があります::

    - name: fetch raw ip ranges for aws s3
      set_fact:
        raw_s3_ranges: "{{ lookup('aws_service_ip_ranges', region='eu-central-1', service='S3', wantlist=True) }}"

    - name: prepare list structure for ec2_group module
      set_fact:
        s3_ranges: "{{ s3_ranges | default([]) + [{'proto': 'all', 'cidr_ip': item, 'rule_desc': 'S3 Service IP range'}] }}"
      with_items: "{{ raw_s3_ranges }}"

    - name: set S3 IP ranges to egress rules
      ec2_group:
        name: aws_s3_ip_ranges
        description: allow outgoing traffic to aws S3 service
        region: eu-central-1
        state: present
        vpc_id: vpc-123456
        purge_rules: true
        purge_rules_egress: true
        rules: []
        rules_egress: "{{ s3_ranges }}"
        tags:
          Name: aws_s3_ip_ranges

.. _aws_host_inventory:

ホストインベントリー
``````````````

ノードが起動したら、おそらく再度通信するようにしたいでしょう。 クラウド設定では、テキストファイルに、
クラウドホスト名の静的リストを維持しないことが推奨されます。 これを処理する最善の方法は、ec2 動的インベントリースクリプトを使用することです。:ref:`dynamic_inventory` を参照してください。 

これにより、Ansible 外で作成されたノードも動的に選択され、Ansible がノードを管理できるようになります。

これを使用する方法は :ref:`dynamic_inventory` を参照してから、本章に戻ります。

.. _aws_tags_and_groups:

タグ、グループ、および変数
`````````````````````````````

ec2 インベントリースクリプトを使用すると、ホストは EC2 でタグ付けされる方法に基づいて自動的にグループに表示されます。

たとえば、ホストに「webserver」の値で「class」タグが付与される場合は、
以下のように、動的グループを介して自動的に検出されます::

   - hosts: tag_class_webserver
     tasks:
       - ping

この原理を使用すると、実行する機能でシステムを分離することができます。

この例では、「webserver」の「class」でタグ付けされた各マシンに自動的に適用される変数を定義すると、
ansible の「group_vars」が使用できます。 「:ref:`splitting_out_vars`」を参照してください。

同様のグループは、リージョンおよびその他の分類に利用でき、同じメカニズムを使用して同様に変数を割り当てることができます。

.. _aws_pull:

Ansible Pull を使用した自動スケーリング
`````````````````````````````

Amazon Autoscaling 機能は、負荷に応じて容量を自動的に増減します。 また、クラウドドキュメントで説明されるように、
自動スケーリングポリシーを設定する Ansible モジュールがあります。

ノードがオンラインになると、ansible コマンドの次のサイクルが反映されてそのノードを設定するのを待つことができない可能性があります。  

これには、必要な ansible-pull 呼び出しが含まれる事前のマシンイメージが必要です。 Ansible-pull は、git サーバーから Playbook を取得し、ローカルで実行するコマンドラインツールです。  

このアプローチの課題の 1 つとして、pull コマンドの結果に関するデータを自動スケーリングコンテキストに保存する集中的な方法が必要になります。
このため、次のセクションで提供される自動スケーリングソリューションの方が適切です。

pull モードの Playbook の詳細は、「:ref:`ansible-pull`」を参照してください。

.. _aws_autoscale:

Ansible Tower を使用した自動スケーリング
``````````````````````````````

:ref:`ansible_tower` には、自動スケーリングのユースケースに使用する非常に優れた機能も含まれています。 このモードでは、単純な curl スクリプトが定義済みの URL を呼び出すことができ、
サーバーはリクエスターに「ダイヤルアウト」して、起動しているインスタンスを構成します。 これは、
一時ノードを再設定する優れた方法です。 詳細は、Tower のインストールおよび製品のドキュメントを参照してください。

pull モードで Tower のコールバックを使用する利点は、ジョブの結果が引き続き中央で記録され、
リモートホストと共有する必要のある情報が少なくなることです。

.. _aws_cloudformation_example:

CloudFormation を使用した Ansible (Ansible と CloudFormation の比較)
````````````````````````````````````````

CloudFormation は、クラウドスタックを JSON または YAML のドキュメントとして定義する Amazon テクノロジーです。   

Ansible モジュールは、複雑な JSON/YAML ドキュメントを定義せずに、多くの例で CloudFormation よりも簡単にインターフェースを使用できます。
これは、ほとんどのユーザーに推奨されます。

ただし、CloudFormation を使用するユーザーには、
CloudFormation テンプレートを Amazon に適用するのに使用できる Ansible モジュールがあります。

CloudFormation で Ansible を使用する場合は、通常、Ansible を Packer などのツールで使用してイメージを作成し、CloudFormation がそのイメージを起動するか、
イメージがオンラインになると、ユーザーデータを通じて ansible が呼び出されるか、その組み合わせとなります。

詳細は、Ansible CloudFormation モジュールのサンプルを参照してください。

.. _aws_image_build:

Ansible での AWS イメージの構築
```````````````````````````````

多くのユーザーは、イメージをインスタンス化後に完全に設定するのではなく、より完全な設定で起動できます。 これを行うには、
Ansible Playbook で数多くあるプログラムの 1 つを使用してベースイメージを定義し、アップロードすることができます。
これにより、ec2 モジュールや、ec2_asg、cloudformation などの Ansible AWS モジュールで使用する独自の AMI ID を取得します。  利用可能なツールには、Packer、aminator、
および Ansible の ec2_ami モジュールが含まれます。  

一般的には、Packer が使用されます。

Packer ドキュメントの「`Ansible のローカル Packer プロビジョナー <https://www.packer.io/docs/provisioners/ansible-local.html>`_」および「`Ansible リモート Packer プロビジョナー <https://www.packer.io/docs/provisioners/ansible.html>`_」を参照してください。

現時点では、Packer を使用しない場合は、プロビジョニング後に (上記のように) Ansible を使用したベースイメージの設定が可能です。

.. _aws_next_steps:

次のステップ:モジュールの検証
```````````````````````````

Ansible には、幅広い EC2 サービスを設定する多くのモジュールが含まれています。 モジュールドキュメントの「Cloud」カテゴリーを参照してください。
サンプルを含む完全なリストが紹介されています。

.. seealso::

   :ref:`all_modules`
       Ansible モジュールの全ドキュメント
   :ref:`working_with_playbooks`
       Playbook の概要
   :ref:`playbooks_delegation`
       委譲 (ロードバランサー、クラウド、ローカルで実行した手順を使用する際に役に立ちます)
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       #ansible IRC chat channel

