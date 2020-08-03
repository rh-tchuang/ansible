.. _playbooks_environment:

環境の設定 (およびプロキシーの使用)
==================================================

.. versionadded:: 1.1

``environment`` キーワードを使用すると、リモートターゲットで行うアクションの環境変数を設定できます。
たとえば、http 要求を行うタスクのプロキシーの設定が必要になる場合があります。
または、呼び出されるユーティリティーまたはスクリプトも、適切に実行するように特定の環境変数の設定が必要になる場合があります。

以下は例になります。

    - hosts: all
      remote_user: root

      tasks:

        - name: Install cobbler
          package:
            name: cobbler
            state: present
          environment:
            http_proxy: http://proxy.example.com:8080

.. note::
   ``environment:`` は Ansible 自体には影響を与えず、特定のタスクアクションのコンテキストだけでなく、
    Ansible 自体の設定や、lookup や filter などの他のプラグインの実行は含まれません。

環境は変数に保存し、以下のようにアクセスすることもできます。

    - hosts: all
      remote_user: root

      # here we make a variable named "proxy_env" that is a dictionary
      vars:
        proxy_env:
          http_proxy: http://proxy.example.com:8080

      tasks:

        - name: Install cobbler
          package:
            name: cobbler
            state: present
          environment: "{{ proxy_env }}"

これは、プレイレベルでも使用できます。

    - hosts: testhost

      roles:
         - php
         - nginx

      environment:
        http_proxy: http://proxy.example.com:8080

上記のプロキシー設定のみを示していますが、任意の数の設定を指定することができます。 環境ハッシュを定義する最も論理的な場所は、
以下のように group_vars ファイルになる可能性があります。

    ---
    # file: group_vars/boston

    ntp_server: ntp.bos.example.com
    backup: bak.bos.example.com
    proxy_env:
      http_proxy: http://proxy.bos.example.com:8080
      https_proxy: http://proxy.bos.example.com:8080


言語固有のバージョンマネージャーの使用
===============================================

一部の言語固有のバージョンマネージャー (rbenv や NVM など) では、これらのツールを使用している間に環境変数を設定する必要があります。これらのツールを手動で使用する場合は、通常、シェル設定ファイルに追加されたスクリプトまたは行を使用して環境変数の一部を指定する必要があります。Ansible では、代わりに環境ディレクティブを使用できます。

    ---
    ### A playbook demonstrating a common npm workflow:
    # - Check for package.json in the application directory
    # - If package.json exists:
    #   * Run npm prune
    #   * Run npm install

    - hosts: application
      become: false

      vars:
        node_app_dir: /var/local/my_node_app

      environment:
        NVM_DIR: /var/local/nvm
        PATH: /var/local/nvm/versions/node/v4.2.1/bin:{{ ansible_env.PATH }}

      tasks:
      - name: check for package.json
        stat:
          path: '{{ node_app_dir }}/package.json'
        register: packagejson

      - name: npm prune
        command: npm prune
        args:
          chdir: '{{ node_app_dir }}'
        when: packagejson.stat.exists

      - name: npm install
        npm:
          path: '{{ node_app_dir }}'
        when: packagejson.stat.exists

.. note::
   ``ansible_env:`` 通常、ファクト収集 (M(gather_facts)) によって設定され、
   変数の値は収集アクションを実行したユーザーにより異なります。remote_user/become_user を変更すると、それらの変数に誤った値が使用される可能性があります。

また、1 つのタスクに対して環境を指定することも可能です。

    ---
    - name: install ruby 2.3.1
      command: rbenv install {{ rbenv_ruby_version }}
      args:
        creates: '{{ rbenv_root }}/versions/{{ rbenv_ruby_version }}/bin/ruby'
      vars:
        rbenv_root: /usr/local/rbenv
        rbenv_ruby_version: 2.3.1
      environment:
        CONFIGURE_OPTS: '--disable-install-doc'
        RBENV_ROOT: '{{ rbenv_root }}'
        PATH: '{{ rbenv_root }}/bin:{{ rbenv_root }}/shims:{{ rbenv_plugins }}/ruby-build/bin:{{ ansible_env.PATH }}'
    
.. seealso::

   :ref:`playbooks_intro`
       Playbook の概要
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       IRC チャットチャンネル #ansible
