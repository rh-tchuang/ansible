:orphan:

.. \_implicit\_localhost:

暗黙的な 'localhost'
====================

``localhost`` を参照しようとしたにもかかわらず、インベントリーにその localhost が定義されていない場合には、Ansible により暗黙的 localhost が作成されます。::

    - hosts: all
      tasks:
        - name: check that i have log file for all hosts on my local machine
          stat: path=/var/log/hosts/{{inventory_hostname}}.log
          delegate_to: localhost

上記のような場合 (または ``local_action``) で、Ansible が 'localhost' に問い合わせをする必要があるにもかかわらず、localhost を作成していない場合には、Ansible で localhost が作成されます。このホストは、インベントリーにあるものと同等の特定の接続変数で定義します::

   ...

   hosts:
     localhost:
      vars:
        ansible\_connection: local
        ansible\_python\_interpreter: "{{ansible\_playbook\_python}}"

この設定により、正しい接続および Python が使用してローカルでのタスクが実行されるようになります。
インベントリーに ``localhost`` のホストのエントリーを作成して、組み込まれた暗黙的なホストバージョンを上書きできます。この時点で、すべての暗黙的な動作は無視され、インベントリー内の ``localhost`` は他のホストと同じように処理されます。``ansible_python_interpreter`` などの接続変数を含む、グループおよびホスト変数が適用されます。この設定は、``delegate_to: localhost`` や ``local_action`` にも適用されます。local\_action は、delegate\_to: localhost のエイリアスです。

.. note::
  \- このホストはいずれのグループでもターゲットにすることはできませんが、``host_vars`` と 'all' グループからの vars (変数) を使用します。
  - ``"{{ hostvars['localhost'] }}"`` などの要求がない限り、暗黙的な localhost は ``hostvars`` マジック変数には表示されません。
  \- マジック変数 ``inventory_file`` および ``inventory_dir`` は、**各インベントリーホスト** に依存するため、暗黙的な localhost では利用できません。
  \- この暗黙的ホストは、「localhost」の IPv4 および IPv6 の表現であるため、``127.0.0.1`` または ``::1`` を使用してもトリガーとなります。
  \- 作成する方法は多数ありますが、暗黙的な localhost は 1 つしかありません。これには、最初に作成したときの名前が使用されます。
  - ``connection: local`` があっても暗黙的な localhost のトリガーにならない場合は、``inventory_hostname`` の接続を変更しているだけです。
