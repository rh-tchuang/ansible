.. _playbooks_variables:

***************
変数の使用
***************

.. contents::
   :local:

繰り返し処理を容易にする自動化は存在しますが、すべてのシステムは全く同じではありません。他のシステムとは若干異なる設定が必要になる場合があります。場合によっては、確認済みの動作や状態が他のシステムの設定方法に影響を与える場合があります。たとえば、システムの IP アドレスを見つけ、別のシステムで設定値として使用しないといけない場合があります。

Ansible は、*変数* を使用してシステム間の相違点に対応します。

:ref:`playbooks_conditionals` および :ref:`playbooks_loops` も読み取る変数を理解するには、以下を実行します。
**group_by** モジュールや、
``when`` 条件式などの便利なものを変数とともに使用して、システム間の相違点を管理することもできます。

`ansible-examples github repository <https://github.com/ansible/ansible-examples>`_ には、Ansible で変数がどのように使用されているかの例が記載されています。

.. _valid_variable_names:

有効な変数名の作成
=============================

変数の使用を開始する前に、有効な変数名を知っていることが重要です。

変数名は文字、数字、およびアンダースコアである必要があります。 変数は常に文字で始まる必要があります。

``foo_port`` は優れた変数です。``foo5`` も問題ありません。

``foo-port``、``foo port``、``foo.port``、および ``12`` は有効な変数名ではありません。

YAML は、キーを値にマップするディクショナリーもサポートします。 例::

  foo:
    field1: one
    field2: two

その後、括弧またはドットのいずれかの表記を使用して、
ディクショナリーの特定のフィールドを参照できます::

  foo['field1']
  foo.field1

これらはいずれも同じ値 (「1」) を参照します。 ただし、ドット表記を使用する場合は、一部のキーが Python ディクショナリーの属性やメソッドと競合して問題を引き起こす可能性があることに注意してください。
ドット表記は、一部の鍵が問題を引き起こす可能性があることに注意してください。
Python ディクショナリーの属性とメソッドと併用します。 2 つのアンダースコアで始まるキーと終了するキー (Python で特別に予約されているキー) を使用する場合、
または既知のパブリック属性のいずれかである場合は、
ドット表記ではなく、
括弧表記を使用する必要があります。

``add``, ``append``, ``as_integer_ratio``, ``bit_length``, ``capitalize``, ``center``, ``clear``, ``conjugate``, ``copy``, ``count``, ``decode``, ``denominator``, ``difference``, ``difference_update``, ``discard``, ``encode``, ``endswith``, ``expandtabs``, ``extend``, ``find``, ``format``, ``fromhex``, ``fromkeys``, ``get``, ``has_key``, ``hex``, ``imag``, ``index``, ``insert``, ``intersection``, ``intersection_update``, ``isalnum``, ``isalpha``, ``isdecimal``, ``isdigit``, ``isdisjoint``, ``is_integer``, ``islower``, ``isnumeric``, ``isspace``, ``issubset``, ``issuperset``, ``istitle``, ``isupper``, ``items``, ``iteritems``, ``iterkeys``, ``itervalues``, ``join``, ``keys``, ``ljust``, ``lower``, ``lstrip``, ``numerator``, ``partition``, ``pop``, ``popitem``, ``real``, ``remove``, ``replace``, ``reverse``, ``rfind``, ``rindex``, ``rjust``, ``rpartition``, ``rsplit``, ``rstrip``, ``setdefault``, ``sort``, ``split``, ``splitlines``, ``startswith``, ``strip``, ``swapcase``, ``symmetric_difference``, ``symmetric_difference_update``, ``title``, ``translate``, ``union``, ``update``, ``upper``, ``values``, ``viewitems``, ``viewkeys``, ``viewvalues``, ``zfill``.

.. _variables_in_inventory:

インベントリーでの変数の定義
===============================

多くの場合は、個々のホストまたはインベントリー内のホストのグループに対して変数を設定します。たとえば、ボストンのマシンはすべて、
NTP サーバー (boston.ntp.example.com) として使用する場合があります。:ref:`intro_inventory` ページには、インベントリーに :ref:`host_variables` および :ref:`group_variables` を設定する方法の詳細が記載されています。

.. _playbook_variables:

Playbook での変数の定義
================================

変数は Playbook で直接定義できます。

   - hosts: webservers
     vars:
       http_port:80

これは、Playbook を読んでいるときにすぐそこにあるので便利です。

.. _included_variables:

含まれるファイルおよびロールでの変数の定義
==============================================

:ref:`playbooks_reuse_roles` で説明されているように、
変数は、Ansible ロールの一部である場合とそうでない場合があるインクルードファイルを介して、Playbook に含めることもできます。 適切な組織システムを提供するため、ロールの使用が推奨されます。

.. _about_jinja2:

Jinja2 での変数の使用
===========================

変数を定義したら、Jinja2 テンプレートシステムを使用して Playbook で変数を使用できます。 以下は、Jinja2 の単純なテンプレートです。

    My amp goes to {{ max_amp_value }}

この式は、変数置換の最も基本的な形式を提供します。

Playbook で同じ構文を使用できます。例::

    template: src=foo.cfg.j2 dest={{ remote_install_path }}/foo.cfg

ここで変数は、システム間で異なる可能性のあるファイルの場所を定義します。

テンプレート内では、ホストのスコープにあるすべての変数に自動的にアクセスできます。 実際は、
それだけではありません。他のホストに関する変数を読み取ることもできます。 その方法を少し説明します。

.. note:: Ansible は、テンプレートで Jinja2 ループと条件を許可しますが、Playbook では使用しません。 Ansible の Playbook は、
   純粋にマシンでの解析が可能な YAML です。 これは、ファイルの一部をコード生成したり、
   他のエコシステムツールに Ansible ファイルを読み取らせることができるため、かなり重要な機能です。 誰もがこれを必要とするわけではありませんが、
   選択肢になります。

.. seealso::

    :ref:`playbooks_templating`
        Jinja2 テンプレートの詳細はこちらを参照してください。

.. _jinja2_filters:

Jinja2 フィルターを使用した変数の変換
==========================================

Jinja2 フィルターを使用すると、テンプレート式内で変数の値を変換できます。たとえば、``capitalize`` フィルターは、フィルターに渡される値を大文字にします。``to_yaml`` フィルターおよび ``to_json`` フィルターは変数の値の形式を変更します。Jinja2 には多くの `組み込みフィルター <http://jinja.pocoo.org/docs/templates/#builtin-filters>`_ が含まれ、Ansible は :ref:`より多くのフィルター <playbooks_filters>` を提供します。

.. _yaml_gotchas:

YAML に関する注意点
=======================

YAML 構文では、``{{ foo }}`` で値を開始する場合は、行全体を引用符で囲む必要があります。
これは、YAML ディクショナリーを起動しないようにするためです。 これは、:ref:`yaml_syntax` ドキュメントで説明されています。

これは機能しません::

    - hosts: app_servers
      vars:
          app_path: {{ base_path }}/22

以下のように実行してください。問題ありません。

    - hosts: app_servers
      vars:
           app_path: "{{ base_path }}/22"

.. _vars_and_facts:

システムから検出される変数: Fact (ファクト)
========================================

変数が取得できる他の場所がありますが、これらはユーザーが設定しない、検出される変数のタイプです。

ファクトとは、リモートシステムとの対話から得られる情報です。``ansible_facts`` 変数で完全なセットを見つけることができます。
ほとんどのファクトも、最上位の変数として ``ansible_`` プレフィックスを保持するように「挿入」されますが、競合のために一部削除されます。
これは :ref:`INJECT_FACTS_AS_VARS` 設定で無効にできます。

この例として、リモートホストの IP アドレス、またはオペレーティングシステムなどが挙げられます。

利用可能な情報を確認するには、プレイで以下を実行します。

    - debug: var=ansible_facts

「raw」情報が収集されたものとして表示されるようにするには、以下を実行します。

    ansible hostname -m setup

これにより、Ansible 2.7では次のような大量の変数データが返されます。

.. code-block:: json

    {
        "ansible_all_ipv4_addresses": [
            "REDACTED IP ADDRESS"
        ],
        "ansible_all_ipv6_addresses": [
            "REDACTED IPV6 ADDRESS"
        ],
        "ansible_apparmor": {
            "status": "disabled"
        },
        "ansible_architecture": "x86_64",
        "ansible_bios_date": "11/28/2013",
        "ansible_bios_version": "4.1.5",
        "ansible_cmdline": {
            "BOOT_IMAGE": "/boot/vmlinuz-3.10.0-862.14.4.el7.x86_64",
            "console": "ttyS0,115200",
            "no_timer_check": true,
            "nofb": true,
            "nomodeset": true,
            "ro": true,
            "root": "LABEL=cloudimg-rootfs",
            "vga": "normal"
        },
        "ansible_date_time": {
            "date": "2018-10-25",
            "day": "25",
            "epoch": "1540469324",
            "hour": "12",
            "iso8601": "2018-10-25T12:08:44Z",
            "iso8601_basic": "20181025T120844109754",
            "iso8601_basic_short": "20181025T120844",
            "iso8601_micro": "2018-10-25T12:08:44.109968Z",
            "minute": "08",
            "month": "10",
            "second": "44",
            "time": "12:08:44",
            "tz": "UTC",
            "tz_offset": "+0000",
            "weekday": "Thursday",
            "weekday_number": "4",
            "weeknumber": "43",
            "year": "2018"
        },
        "ansible_default_ipv4": {
            "address": "REDACTED",
            "alias": "eth0",
            "broadcast": "REDACTED",
            "gateway": "REDACTED",
            "interface": "eth0",
            "macaddress": "REDACTED",
            "mtu": 1500,
            "netmask": "255.255.255.0",
            "network": "REDACTED",
            "type": "ether"
        },
        "ansible_default_ipv6": {},
        "ansible_device_links": {
            "ids": {},
            "labels": {
                "xvda1": [
                    "cloudimg-rootfs"
                ],
                "xvdd": [
                    "config-2"
                ]
            },
            "masters": {},
            "uuids": {
                "xvda1": [
                    "cac81d61-d0f8-4b47-84aa-b48798239164"
                ],
                "xvdd": [
                    "2018-10-25-12-05-57-00"
                ]
            }
        },
        "ansible_devices": {
            "xvda": {
                "holders": [],
                "host": "",
                "links": {
                    "ids": [],
                    "labels": [],
                    "masters": [],
                    "uuids": []
                },
                "model": null,
                "partitions": {
                    "xvda1": {
                        "holders": [],
                        "links": {
                            "ids": [],
                            "labels": [
                                "cloudimg-rootfs"
                            ],
                            "masters": [],
                            "uuids": [
                                "cac81d61-d0f8-4b47-84aa-b48798239164"
                            ]
                        },
                        "sectors": "83883999",
                        "sectorsize": 512,
                        "size": "40.00 GB",
                        "start": "2048",
                        "uuid": "cac81d61-d0f8-4b47-84aa-b48798239164"
                    }
                },
                "removable": "0",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "deadline",
                "sectors": "83886080",
                "sectorsize": "512",
                "size": "40.00 GB",
                "support_discard": "0",
                "vendor": null,
                "virtual": 1
            },
            "xvdd": {
                "holders": [],
                "host": "",
                "links": {
                    "ids": [],
                    "labels": [
                        "config-2"
                    ],
                    "masters": [],
                    "uuids": [
                        "2018-10-25-12-05-57-00"
                    ]
                },
                "model": null,
                "partitions": {},
                "removable": "0",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "deadline",
                "sectors": "131072",
                "sectorsize": "512",
                "size": "64.00 MB",
                "support_discard": "0",
                "vendor": null,
                "virtual": 1
            },
            "xvde": {
                "holders": [],
                "host": "",
                "links": {
                    "ids": [],
                    "labels": [],
                    "masters": [],
                    "uuids": []
                },
                "model": null,
                "partitions": {
                    "xvde1": {
                        "holders": [],
                        "links": {
                            "ids": [],
                            "labels": [],
                            "masters": [],
                            "uuids": []
                        },
                        "sectors": "167770112",
                        "sectorsize": 512,
                        "size": "80.00 GB",
                        "start": "2048",
                        "uuid": null
                    }
                },
                "removable": "0",
                "rotational": "0",
                "sas_address": null,
                "sas_device_handle": null,
                "scheduler_mode": "deadline",
                "sectors": "167772160",
                "sectorsize": "512",
                "size": "80.00 GB",
                "support_discard": "0",
                "vendor": null,
                "virtual": 1
            }
        },
        "ansible_distribution": "CentOS",
        "ansible_distribution_file_parsed": true,
        "ansible_distribution_file_path": "/etc/redhat-release",
        "ansible_distribution_file_variety": "RedHat",
        "ansible_distribution_major_version": "7",
        "ansible_distribution_release": "Core",
        "ansible_distribution_version": "7.5.1804",
        "ansible_dns": {
            "nameservers": [
                "127.0.0.1"
            ]
        },
        "ansible_domain": "",
        "ansible_effective_group_id": 1000,
        "ansible_effective_user_id": 1000,
        "ansible_env": {
            "HOME": "/home/zuul",
            "LANG": "en_US.UTF-8",
            "LESSOPEN": "||/usr/bin/lesspipe.sh %s",
            "LOGNAME": "zuul",
            "MAIL": "/var/mail/zuul",
            "PATH": "/usr/local/bin:/usr/bin",
            "PWD": "/home/zuul",
            "SELINUX_LEVEL_REQUESTED": "",
            "SELINUX_ROLE_REQUESTED": "",
            "SELINUX_USE_CURRENT_RANGE": "",
            "SHELL": "/bin/bash",
            "SHLVL": "2",
            "SSH_CLIENT": "REDACTED 55672 22",
            "SSH_CONNECTION": "REDACTED 55672 REDACTED 22",
            "USER": "zuul",
            "XDG_RUNTIME_DIR": "/run/user/1000",
            "XDG_SESSION_ID": "1",
            "_": "/usr/bin/python2"
        },
        "ansible_eth0": {
            "active": true,
            "device": "eth0",
            "ipv4": {
                "address": "REDACTED",
                "broadcast": "REDACTED",
                "netmask": "255.255.255.0",
                "network": "REDACTED"
            },
            "ipv6": [
                {
                    "address": "REDACTED",
                    "prefix": "64",
                    "scope": "link"
                }
            ],
            "macaddress": "REDACTED",
            "module": "xen_netfront",
            "mtu": 1500,
            "pciid": "vif-0",
            "promisc": false,
            "type": "ether"
        },
        "ansible_eth1": {
            "active": true,
            "device": "eth1",
            "ipv4": {
                "address": "REDACTED",
                "broadcast": "REDACTED",
                "netmask": "255.255.224.0",
                "network": "REDACTED"
            },
            "ipv6": [
                {
                    "address": "REDACTED",
                    "prefix": "64",
                    "scope": "link"
                }
            ],
            "macaddress": "REDACTED",
            "module": "xen_netfront",
            "mtu": 1500,
            "pciid": "vif-1",
            "promisc": false,
            "type": "ether"
        },
        "ansible_fips": false,
        "ansible_form_factor": "Other",
        "ansible_fqdn": "centos-7-rax-dfw-0003427354",
        "ansible_hostname": "centos-7-rax-dfw-0003427354",
        "ansible_interfaces": [
            "lo",
            "eth1",
            "eth0"
        ],
        "ansible_is_chroot": false,
        "ansible_kernel": "3.10.0-862.14.4.el7.x86_64",
        "ansible_lo": {
            "active": true,
            "device": "lo",
            "ipv4": {
                "address": "127.0.0.1",
                "broadcast": "host",
                "netmask": "255.0.0.0",
                "network": "127.0.0.0"
            },
            "ipv6": [
                {
                    "address": "::1",
                    "prefix": "128",
                    "scope": "host"
                }
            ],
            "mtu": 65536,
            "promisc": false,
            "type": "loopback"
        },
        "ansible_local": {},
        "ansible_lsb": {
            "codename": "Core",
            "description": "CentOS Linux release 7.5.1804 (Core)",
            "id": "CentOS",
            "major_release": "7",
            "release": "7.5.1804"
        },
        "ansible_machine": "x86_64",
        "ansible_machine_id": "2db133253c984c82aef2fafcce6f2bed",
        "ansible_memfree_mb": 7709,
        "ansible_memory_mb": {
            "nocache": {
                "free": 7804,
                "used": 173
            },
            "real": {
                "free": 7709,
                "total": 7977,
                "used": 268
            },
            "swap": {
                "cached": 0,
                "free": 0,
                "total": 0,
                "used": 0
            }
        },
        "ansible_memtotal_mb": 7977,
        "ansible_mounts": [
            {
                "block_available": 7220998,
                "block_size": 4096,
                "block_total": 9817227,
                "block_used": 2596229,
                "device": "/dev/xvda1",
                "fstype": "ext4",
                "inode_available": 10052341,
                "inode_total": 10419200,
                "inode_used": 366859,
                "mount": "/",
                "options": "rw,seclabel,relatime,data=ordered",
                "size_available": 29577207808,
                "size_total": 40211361792,
                "uuid": "cac81d61-d0f8-4b47-84aa-b48798239164"
            },
            {
                "block_available": 0,
                "block_size": 2048,
                "block_total": 252,
                "block_used": 252,
                "device": "/dev/xvdd",
                "fstype": "iso9660",
                "inode_available": 0,
                "inode_total": 0,
                "inode_used": 0,
                "mount": "/mnt/config",
                "options": "ro,relatime,mode=0700",
                "size_available": 0,
                "size_total": 516096,
                "uuid": "2018-10-25-12-05-57-00"
            }
        ],
        "ansible_nodename": "centos-7-rax-dfw-0003427354",
        "ansible_os_family": "RedHat",
        "ansible_pkg_mgr": "yum",
        "ansible_processor": [
            "0",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "1",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "2",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "3",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "4",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "5",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "6",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz",
            "7",
            "GenuineIntel",
            "Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz"
        ],
        "ansible_processor_cores": 8,
        "ansible_processor_count": 8,
        "ansible_processor_threads_per_core": 1,
        "ansible_processor_vcpus": 8,
        "ansible_product_name": "HVM domU",
        "ansible_product_serial": "REDACTED",
        "ansible_product_uuid": "REDACTED",
        "ansible_product_version": "4.1.5",
        "ansible_python": {
            "executable": "/usr/bin/python2",
            "has_sslcontext": true,
            "type": "CPython",
            "version": {
                "major": 2,
                "micro": 5,
                "minor": 7,
                "releaselevel": "final",
                "serial": 0
            },
            "version_info": [
                2,
                7,
                5,
                "final",
                0
            ]
        },
        "ansible_python_version": "2.7.5",
        "ansible_real_group_id": 1000,
        "ansible_real_user_id": 1000,
        "ansible_selinux": {
            "config_mode": "enforcing",
            "mode": "enforcing",
            "policyvers": 31,
            "status": "enabled",
            "type": "targeted"
        },
        "ansible_selinux_python_present": true,
        "ansible_service_mgr": "systemd",
        "ansible_ssh_host_key_ecdsa_public": "REDACTED KEY VALUE",
        "ansible_ssh_host_key_ed25519_public": "REDACTED KEY VALUE",
        "ansible_ssh_host_key_rsa_public": "REDACTED KEY VALUE",
        "ansible_swapfree_mb": 0,
        "ansible_swaptotal_mb": 0,
        "ansible_system": "Linux",
        "ansible_system_capabilities": [
            ""
        ],
        "ansible_system_capabilities_enforced": "True",
        "ansible_system_vendor": "Xen",
        "ansible_uptime_seconds": 151,
        "ansible_user_dir": "/home/zuul",
        "ansible_user_gecos": "",
        "ansible_user_gid": 1000,
        "ansible_user_id": "zuul",
        "ansible_user_shell": "/bin/bash",
        "ansible_user_uid": 1000,
        "ansible_userspace_architecture": "x86_64",
        "ansible_userspace_bits": "64",
        "ansible_virtualization_role": "guest",
        "ansible_virtualization_type": "xen",
        "gather_subset": [
            "all"
        ],
        "module_setup": true
    }
    
上記の例では、最初のディスクのモデルはテンプレートまたは Playbook で次のように参照できます。

    {{ ansible_facts['devices']['xvda']['model'] }}

同様に、それを報告するシステムのホスト名は次のとおりです。

    {{ ansible_facts['nodename'] }}

ファクトは、(:ref:`playbooks_conditionals` を参照) およびテンプレートでも頻繁に使用されます。

ファクトは、特定の基準に一致するホストの動的グループを作成するために使用することもできます。詳細は、**group_by** の :ref:`モジュール` ドキュメントを参照してください。また、:ref:`playbooks_conditionals` の章で説明されているように一般的な条件付きステートメントでもあります。

.. _disabling_facts:

ファクトの無効化
---------------

ホストに関するファクトデータが不要であることがわかっており、
システムに関するすべてを一元的に知っている場合は、ファクト収集をオフにできます。 これは、主に、または試験的なプラットフォームで Ansible を使用している場合に、
非常に多くのシステムでプッシュモードで Ansible をスケーリングするのに利点があります。  どのプレイでも、以下を行うだけです。

    - hosts: whatever
      gather_facts: no

.. _local_facts:

ローカルファクト (facts.d)
---------------------

.. versionadded:: 1.3

Playbook の章で説明されているように、Ansible のファクトは Playbook 変数で使用するリモートシステムに関するデータを取得する方法です。

通常、これらは Ansible の ``setup`` モジュールによって自動的に検出されます。ユーザーは、API ガイドで説明されているように、カスタムファクトモジュールを作成することもできます。ただし、ファクトモジュールを作成せずに、Ansible 変数で使用するシステムまたはユーザー指定のデータを簡単に提供する方法にはどんなものがありますか。

「Facts.d」は、ユーザーがシステムの管理方法のいくつかの側面を制御する 1 つのメカニズムです。

.. note:: おそらく、「ローカルファクト」という名称は少し間違っています。これは、「ローカルに提供されたユーザー値」ではなく「集中的にプロビジョニングされたユーザー値」、またはファクトが何であるか、つまり「ローカルで動的に決定される値」を意味します。

リモートで管理されているシステムに ``/etc/ansible/facts.d`` ディレクトリーがある場合には、
``.fact`` で終わるこのディレクトリー内のファイルは、JSON、INI、または JSON を返す実行ファイルであり、そのようなファイルは Ansible でローカルファクトを提供できます。
代替ディレクトリーは、``fact_path`` play キーワードを使用して指定できます。

たとえば、``/etc/ansible/facts.d/preferences.fact`` に以下が含まれるとします。

    [general]
    asdf=1
    bar=2

これにより、``asdf`` および ``bar`` がメンバーとして、``general`` という名前のハッシュ変数ファクトが生成されます。
これを検証するには、以下を実行します。

    ansible <hostname> -m setup -a "filter=ansible_local"

以下のファクトが追加されていることを確認できます。

    "ansible_local": {
            "preferences": {
                "general": {
                    "asdf" : "1",
                    "bar"  : "2"
                }
            }
     }

このデータは、``template/playbook`` で以下のようにアクセスできます。

     {{ ansible_local['preferences']['general']['asdf'] }}

ローカル名前空間は、ユーザーが指定したファクトが Playbook の別の場所で定義されるシステムファクトまたは変数を上書きすることを防ぎます。

.. note:: key=value ペアのキーの部分は、ansible_local 変数内の小文字に変換されます。上記の例では、``[general]`` セクションの ``XYZ=3`` に含まれる ini ファイルが含まれると、これを、``{{ ansible_local['preferences']['general']['XYZ'] }}`` ではなく、``{{ ansible_local['preferences']['general']['xyz'] }}`` としてアクセスすることが予想されます。これは、Ansible が Python の `ConfigParser`_ を使用して、`optionxform`_ メソッドを介してオプション名をすべて渡し、このメソッドのデフォルト実装はオプション名を小文字に変換するためです。

.. _ConfigParser: https://docs.python.org/2/library/configparser.html
.. _optionxform: https://docs.python.org/2/library/configparser.html#ConfigParser.RawConfigParser.optionxform

カスタムファクトをコピーして実行する Playbook がある場合は、セットアップモジュールを再実行する明示的な呼び出しを行うと、
その特定のプレイ中にそのファクトを使用できるようになります。 それ以外の場合は、ファクト情報を収集する次のプレイで利用できます。
以下に、以下のような例を示します。

  - hosts: webservers
    tasks:
      - name: create directory for ansible custom facts
        file: state=directory recurse=yes path=/etc/ansible/facts.d
      - name: install custom ipmi fact
        copy: src=ipmi.fact dest=/etc/ansible/facts.d
      - name: re-read facts after adding custom fact
        setup: filter=ansible_local

ただし、このパターンではファクトモジュールも作成でき、これをオプションとして見なすこともできます。

.. _ansible_version:

Ansible バージョン
---------------

.. versionadded:: 1.8

Playbook の動作を特定のバージョンの Ansible に適用するには、
以下のように変数 ansible_version が利用できます。

    "ansible_version": {
        "full":"2.0.0.2",
        "major":2,
        "minor":0,
        "revision":0,
        "string":"2.0.0.2"
    }

.. _fact_caching:

ファクトのキャッシュ
-------------

.. versionadded:: 1.8

そのドキュメントの別の場所で示されているように、あるサーバーが別のサーバーの変数を参照することは可能です。例を以下に示します。

    {{ hostvars['asdf.example.com']['ansible_facts']['os_family'] }}

「ファクトキャッシング」が無効になっている場合は、
これを行うため、現在のプレイまたは別の Playbook の上位にあるプレイではすでに「asdf.example.com」と通信している必要があります。 これは、Ansible のデフォルト設定です。

これを回避するために、Ansible 1.8では、Playbook の実行間でファクトを保存できますが、
この機能は手動で有効にする必要があります。 なぜこれが役に立つのでしょうか。

数千のホストを持つ非常に大きなインフラストラクチャーでは、ファクトキャッシュが夜間に実行されるように設定できます。小規模なサーバーセットの構成は、アドホックまたは 1 日を通して定期的に実行できます。ファクトキャッシングを有効にすると、
すべてのサーバーに「到達」して、変数とそれに関する情報を参照する必要がなくなります。

ファクトキャッシュを有効にすると、あるグループのマシンが、現在の /usr/bin/ansible-playbook の実行で通信されていないため、他のグループのマシンに関する変数を参照できるようになります。

キャッシュされたファクトの利点を得るには、``gathering`` 設定を ``smart`` または ``explicit`` に変更するか、ほとんどのプレイで ``gather_facts`` を ``False`` に設定します。

現在、Ansible には redis および jsonfile という永続キャッシュプラグインが同梱されています。

redis を使用してファクトキャッシュを設定するには、以下のように ``ansible.cfg`` で有効にします。

    [defaults]
    gathering = smart
    fact_caching = redis
    fact_caching_timeout = 86400
    # seconds

再実行するには、同等の OS コマンドを実行します。

    yum install redis
    service redis start
    pip install redis

Python redis ライブラリーは pip からインストールする必要があることに注意してください。EPEL でパッケージ化されたバージョンは Ansible で使用するには古すぎることに注意してください。

現在の実施形態では、この機能はベータ版の状態であり、Redis プラグインはポートまたはパスワード設定をサポートしません。これは近い将来、変更される予定です。

jsonfile を使用してファクトキャッシュを設定するには、以下のように ``ansible.cfg`` で有効にします。

    [defaults]
    gathering = smart
    fact_caching = jsonfile
    fact_caching_connection = /path/to/cachedir
    fact_caching_timeout = 86400
    # seconds

``fact_caching_connection`` は、
書き込み可能なディレクトリーへのローカルファイルシステムのパスです (Ansibleは、ディレクトリーが存在しない場合は作成しようとします)。

``fact_caching_timeout`` は、記録されたファクトをキャッシュする秒数です。

.. _registered_variables:

変数の登録
=====================

別の変数の主な使用方法は、コマンドを実行して、そのコマンドの結果を変数として登録することです。タスクを実行し、後続のタスクで使用するために変数に戻り値を保存する場合は、登録した変数を作成します。この例については、
「:ref:`playbooks_conditionals`」の章を参照してください。

例::

   - hosts: web_servers

     tasks:

        - shell: /usr/bin/foo
          register: foo_result
          ignore_errors:True

        - shell: /usr/bin/bar
          when: foo_result.rc == 5

結果はモジュールごとに異なります。各モジュールのドキュメントには、そのモジュールの戻り値を記述する ``RETURN`` セクションが含まれています。特定のタスクの値を表示するには、Playbook に ``-v`` を指定して実行します。

登録される変数はファクトに似ていますが、いくつかの相違点があります。ファクトと同様に、登録される変数はホストレベルの変数です。ただし、登録した変数はメモリーにのみ保存されます。(Ansible のファクトは、設定したキャッシュプラグインによってサポートされます)。 登録済みの変数は、現在の Playbook 実行の残りの部分に対してホスト上でのみ有効です。最後に、登録された変数とファクトには異なる :ref:`優先順位レベル <ansible_variable_precedence>` があります。

ループでタスクに変数を登録すると、登録した変数にはループの各項目の値が含まれます。ループ時に変数に置かれたデータ構造は ``results`` 属性を含みます。これは、モジュールからのすべての応答のリストになります。この機能の仕組みの詳細な例は、ループでのレジスターの使用を説明している「:ref:`playbooks_loops`」セクションを参照してください。

.. note:: タスクが失敗するか、または省略した場合、変数は失敗または省略されたステータスで登録されますが、変数の登録を回避する唯一の方法はタグの使用です。

.. _accessing_complex_variable_data:

複雑な変数データへのアクセス
===============================

このことについては、すでに上述しています。

ネットワーク情報などの指定された一部のファクトは、ネストされたデータ構造として利用できます。 それにアクセスするには、
簡単な ``{{ foo }}`` では十分ではありませんが、それでも簡単に実行できます。  IP アドレスを取得する方法を以下に示します。

    {{ ansible_facts["eth0"]["ipv4"]["address"] }}

または、以下を実行します。

    {{ ansible_facts.eth0.ipv4.address }}

同様に、これはアレイの最初の要素にアクセスする方法になります。

    {{ foo[0] }}

.. _magic_variables_and_hostvars:

マジック変数を使用したその他のホストに関する情報へのアクセス
============================================================

変数を定義するかどうかに関係なく、Ansible が提供する :ref:`special_variables` を使用して、「マジック」変数、ファクト、接続変数など、ホストに関する情報にアクセスできます。この変数名は予約されています。これらの名前で変数を設定しないでください。変数の ``環境`` 変数も予約されています。

最も一般的に使用されるマジック変数は、``hostvars``、``groups``、``group_names``、および ``inventory_hostname`` です。

``hostvars`` を使用すると、別のホストの変数にアクセスできます。これには、そのホストに関するファクトが含まれます。Playbook の任意の時点でホスト変数にアクセスできます。Playbook または Playbook のセットでまだホストに接続していない場合でも、変数は取得できますが、ファクトは表示されません。

データベースサーバーが別のノードの「ファクト」の値、または別のノードに割り当てられたインベントリー変数を使用する場合は、
テンプレート内またはアクションライン内で簡単に使用できます。

    {{ hostvars['test.example.com']['ansible_facts']['distribution'] }}

``グループ`` とは、インベントリー内のすべてのグループ (およびホスト) の一覧です。 これは、グループ内のすべてのホストを列挙するために使用できます。例:

.. code-block:: jinja

   {% for host in groups['app_servers'] %}
      # something that applies to all app servers.
   {% endfor %}

頻繁に使用されるイディオムは、そのグループ内のすべての IP アドレスを見つけるグループです。

.. code-block:: jinja

   {% for host in groups['app_servers'] %}
      {{ hostvars[host]['ansible_facts']['eth0']['ipv4']['address'] }}
   {% endfor %}

このイディオムを使用してフロントエンドプロキシーサーバーをすべてのアプリケーションサーバーに指定し、サーバー間で適切なファイアウォールルールなどを設定できます。
ただし、ファクトが最近キャッシュされていない場合 (ファクトキャッシュはAnsible 1.8 で追加されています) に、そのホストのファクトが最近追加されたことを確認する必要があります。

``group_names`` は、現在のホストが置かれているすべてのグループの一覧 (アレイ) です。 これは、テンプレートで Jinja2 構文を使用して、ホストのグループメンバーシップ (またはロール) に応じて異なるテンプレートソースファイルを作成できます。

.. code-block:: jinja

   {% if 'webserver' in group_names %}
      # some part of a configuration file that only applies to webservers
   {% endif %}

``inventory_hostname`` は、Ansible のインベントリーホストファイルで設定されるホスト名です。 これは、
ファクト収集を無効にした場合、または検出されたホスト名 ``ansible_hostname`` に依存したくない場合に役立ちます。 FQDN が長くなると、ドメインの残りの部分なしで、最初の期間までの部分を含む ``inventory_hostname_short`` 
を使用できます。

その他の便利なマジック変数は、次のような現在のプレイまたは Playbook を参照します。

.. versionadded:: 2.2

``ansible_play_hosts`` は、現在のプレイでアクティブなままになっているすべてのホストの完全なリストです。

.. versionadded:: 2.2

``ansible_play_batch`` は、プレイの現在の「batch」の範囲にあるホスト名の一覧として利用できます。バッチサイズは ``serial`` で定義されます。設定されていない場合は、プレイ全体に相当するようになります (``ansible_play_hosts`` と同じになります)。

.. versionadded:: 2.3

``ansible_playbook_python`` は、Ansible コマンドラインツールを起動するために使用される Python 実行ファイルへのパスです。

この変数は、テンプレートに複数のホスト名を付ける場合や、一覧をロードバランサーのルールに挿入する際に便利です。

また、``inventory_dir`` は Ansible のインベントリーホストファイルを保持するディレクトリーのパス名であり、``inventory_file`` は、Ansible のインベントリーホストファイルを参照するパス名とファイル名です。

``playbook_dir`` には Playbook のベースディレクトリーが含まれます。

次に、現在ロールのパス名 (1.8 以降) になる ``role_path`` 名があります。これはロール内でのみ機能します。

最後に、``ansible_check_mode`` (バージョン 2.1 で追加) はブール値のマジック変数で、``--check`` で Ansible を実行する場合は ``True`` に設定されます。

.. _variable_file_separation_details:

ファイルで変数の定義
===========================

Playbook をソースの管理下に置くことは素晴らしい考えですが、
特定の重要な変数を非公開にしながら、
Playbook のソースを公開することもできます。 同様に、
特定の情報をメインの Playbook から離れた
別のファイルに保存する場合があります。

これは、以下のような外部変数ファイル (1 つまたは複数) を使用して実行できます。

    ---

    - hosts: all
      remote_user: root
      vars:
        favcolor: blue
      vars_files:
        - /vars/external_vars.yml

      tasks:

      - name: this is just a placeholder
        command: /bin/echo foo

これにより、Playbook のソースを他の人と共有するときに、
機密データを他の人と共有するリスクがなくなります。

各変数ファイルの内容は、以下のような単純な YAML ディクショナリーです。

    ---
    # in the above example, this would be vars/external_vars.yml
    somevar: somevalue
    password: magic

.. note::
   ホストごとおよびグループごとの変数を非常に類似したファイルに保持することも可能です。
   これは、:ref:`splitting_out_vars` で説明されています。

.. _passing_variables_on_the_command_line:

コマンドラインで変数を渡す
=====================================

``vars_prompt`` および ``vars_files`` の他に、
``--extra-vars`` (または ``-e``) 引数を使用して、コマンドラインで変数を設定することが可能です。 変数は、以下の形式のいずれかを使用して、
単一引用符で囲まれた文字列 (1 つ以上の変数を含む) を使用して定義できます。

key=value format::

    ansible-playbook release.yml --extra-vars "version=1.23.45 other_variable=foo"

.. note:: ``key=value`` 構文を使用して渡された値は、文字列として解釈されます。
          文字列でないもの (ブール値、整数、浮動小数点数、リストなど) を渡す必要がある場合は、JSON 形式を使用します。

JSON 文字列の形式::

    ansible-playbook release.yml --extra-vars '{"version":"1.23.45","other_variable":"foo"}'
    ansible-playbook arcade.yml --extra-vars '{"pacman":"mrs","ghosts":["inky","pinky","clyde","sue"]}'

JSON ファイルまたは YAML ファイルの変数::

    ansible-playbook release.yml --extra-vars "@some_file.json"

これは、特に、Playbook のホストグループまたはユーザーを設定するのに役立ちます。

引用符やその他の特殊文字をエスケープ処理します。

マークアップ (JSON など) と操作しているシェルの両方に対して、
適切に引用符をエスケープしていることを確認してください::

    ansible-playbook arcade.yml --extra-vars "{\"name\":\"Conan O\'Brien\"}"
    ansible-playbook arcade.yml --extra-vars '{"name":"Conan O'\\\''Brien"}'
    ansible-playbook script.yml --extra-vars "{\"dialog\":\"He said \\\"I just can\'t get enough of those single and double-quotes"\!"\\\"\"}"

このような場合は、
変数の定義が含まれる JSON ファイルまたは YAML ファイルを使用することが推奨されます。

.. _ansible_variable_precedence:

変数の優先度: 変数をどこに置くべきか
===================================================

変数が別の変数をオーバーライドする方法について疑問をもたれるかもしれません。 最終的に Ansible の哲学が優れています。
変数をどこに配置すればいいかが分かったら、それについて考える必要はほとんどなくなります。

47 か所で変数「x」を定義せず、「どの x が使用されるか」を尋ねます。
なぜですか。 なぜなら、これは、Ansible の Zen (禅) 哲学ではないからです。

エンパイア・ステート・ビルは 1 つしかありません。モナリザも 1 つしかありません。 変数を定義する場所を把握し、
複雑にしないでください。

ただし、次に進んで、優先順位を下げます。 これは存在します。 それは実際のもので、
あなたはそれを使用するかもしれません。

同じ名前の複数の変数が異なる場所に定義されている場合、それらは特定の順序で上書きされます。

以下は、最も少ないものから大きいものへの優先度の順序です (最後に一覧表示される変数が優先されます)。

  #. command line values (eg "-u user")
  #. role defaults [1]_
  #. inventory file or script group vars [2]_
  #. inventory group_vars/all [3]_
  #. playbook group_vars/all [3]_
  #. inventory group_vars/* [3]_
  #. playbook group_vars/* [3]_
  #. inventory file or script host vars [2]_
  #. inventory host_vars/* [3]_
  #. playbook host_vars/* [3]_
  #. host facts / cached set_facts [4]_
  #. play vars
  #. play vars_prompt
  #. play vars_files
  #. role vars (defined in role/vars/main.yml)
  #. block vars (only for tasks in block)
  #. task vars (only for the task)
  #. include_vars
  #. set_facts / registered vars
  #. role (and include_role) params
  #. include params
  #. extra vars (always win precedence)

基本的に、「ロールのデフォルト」となるもの (ロール内のデフォルトディレクトリー) は、最も柔軟で、簡単に上書きできます。ロールの vars ディレクトリーにある内容はすべて、名前空間内のその変数の以前のバージョンを上書きします。 ここで説明する概念は、範囲をより明確にするほど、コマンドラインの優先順位がより高くなることです。追加変数 ``-e`` は常に優先されることです。 ホスト、またはインベントリー変数は、ロールのデフォルトよりも優先されますが、vars ディレクトリーや ``include_vars`` タスクなどの明示的な機能はありません。

.. rubric:: 注記

.. [1] 各ロールのタスクには、独自のロールのデフォルトが表示されます。ロールの外部で定義されたタスクには、最後のロールのデフォルトが表示されます。
.. [2] インベントリーファイルで定義される変数、または動的インベントリーで指定される変数。
.. [3] 「vars plugins」および Ansible に同梱されるデフォルトの vars プラグインにより追加される host_vars および group_vars が含まれます。
.. [4] set_facts のキャッシュ可能なオプションを使用して作成すると、変数がプレイで優先されます。
       ただし、キャッシュからのホストのファクトと同様に優先されます。

.. note:: 任意のセクションで、変数を再定義すると、以前のインスタンスが上書きされます。
          複数のグループに同じ変数がある場合は、最後に読み込まれたグループが優先されます。
          プレイの ``vars:`` セクションで変数を 2 回定義すると、2 つ目の変数が優先されます。
.. note::以前は、デフォルトの設定 ``hash_behaviour=replace`` を説明し、``merge`` に切り替えてを部分的に上書きします。
.. note::グループの読み込みは、親子関係に従います。同じ「親/子」レベルのグループは、アルファベット順に従ってマージされます。
          この最後のものは、ユーザーが ``ansible_group_priority`` を使用して置き換えることができます。デフォルトでは、すべてのグループで ``1`` になります。
          この ``ansible_group_priority`` 変数は、group_vars の読み込みで使用されるため、この変数は、group_vars/ ではなくインベントリーソースでのみ設定できます。

(すべてのバージョンで) 考慮すべきもう 1 つの重要なことは、接続変数が、設定やコマンドライン、ならびにプレイ、ロール、およびタスクに固有のオプションおよびキーワードを上書きすることです。詳細は「:ref:`general_precedence_rules`」を参照してください。たとえば、インベントリーで ``ansible_user: ramon`` が指定されている場合は、以下を実行します。

    ansible -u lola myhost

変数の値が優先されるため、これは引き続き ``ramon`` として接続されます (この場合は、変数がインベントリーから取得されますが、変数が定義されている場所に関係なく、同じことが当てはまります)。

プレイまたはタスクの場合、これは ``remote_user`` にも当てはまります。インベントリー設定が同じ場合、プレイは以下のようになります::

 - hosts: myhost
   tasks:
    - command:I'll connect as ramon still
      remote_user: lola

``remote_user`` の値はインベントリーの ``ansible_user`` によって上書きされます。

これは、ホスト固有の設定が一般的な設定をオーバーライドできるように行われます。これらの変数は通常、インベントリーのホストまたはグループごとに定義されますが、
他の変数のように動作します。

リモートユーザーをグローバルに上書きする必要がある場合 (インベントリーでも) は、追加の変数を使用できます。たとえば、以下を実行した場合::

    ansible... -e "ansible_user=maria" -u lola

``lola`` の値は無視されますが、``ansible_user=maria`` は ``ansible_user`` (または ``remote_user``) が設定されているその他のすべての場所よりも優先されます。

変数の接続固有のバージョンは、
より一般的なバージョンよりも優先されます。 たとえば、group_var として指定された ``ansible_ssh_user`` は、
host_var として指定される ``ansible_user`` よりも優先されます。

また、プレイで通常の変数として上書きすることもできます。

    - hosts: all
      vars:
        ansible_user: lola
      tasks:
        - command:I'll connect as lola!

.. _variable_scopes:

変数のスコープ設定
-----------------

その値に設定するスコープに基づいて、変数を設定する場所を決定できます。Ansible には以下の主要なスコープが 3 つあります。

 * グローバル: これは、設定、環境変数、およびコマンドラインで設定されます。
 * プレイ: 各プレイおよび含まれる構造、変数エントリー (vars、vars_files、vars_prompt)、ロールのデフォルト、および変数
 * ホスト: インベントリー、include_vars、ファクト、または登録されたタスク出力などのホストに直接関連付けられる変数

.. _variable_examples:

変数を設定する場所の例
-----------------------------------

 例と、値よりも便利なコントロールの種類に基づいて配置する場所を示します。

まず、グループ変数は強力なものになります。

サイト全体のデフォルトは、``group_vars/all`` 設定として定義する必要があります。 通常、グループ変数は、
インベントリファイルと一緒に配置されます。 これらは動的インベントリースクリプトによって返されるか (:ref:`intro_dynamic_inventory` を参照)、
UI または API からの :ref:`ansible_tower` などで定義できます。

    ---
    # file: /etc/ansible/group_vars/all
    # this is the site wide default
    ntp_server: default-time.example.com

地域情報は ``group_vars/region`` 変数で定義できます。 このグループが ``all`` グループの子である場合 (つまりすべてのグループが子であるため)、より上位でより一般的なグループをオーバーライドします。

    ---
    # file: /etc/ansible/group_vars/boston
    ntp_server: boston-time.example.com

何らかの理由で特定のホストが特定の NTP サーバーを使用するように指示する場合は、グループ変数をオーバーライドします。

    ---
    # file: /etc/ansible/host_vars/xyz.boston.example.com
    ntp_server: override.example.com

そのため、インベントリーと、通常設定されている内容に対応します。 これは、地理的や動作に対処する際の適切な場所です。 グループは頻繁にホストにロールをマップするエンティティーであるため、ロールに変数を定義する代わりに、グループに変数を設定するショートカットが設定されることがあります。 どちらの方法でも実施できます。

以下に留意してください。 子グループは親グループを上書きし、ホストは常にそのグループを上書きします。

次に、ロール変数の優先順位を説明しています。

この時点でロールを使用していると仮定します。 確実にロールを使用する必要があります。 ロールは優れています。 詳細な
使用方法については、 以下がヒントになります。

適切なデフォルト値で再配布可能なロールを作成する場合は、それらのロールを ``roles/x/defaults/main.yml`` ファイルに配置します。 これは、
ロールはデフォルト値にしますが、Ansible のすべての値はこれを上書きします。
詳細は、:ref:`playbooks_reuse_roles` を参照してください。

    ---
    # file: roles/x/defaults/main.yml
    # if not overridden in inventory or as a parameter, this is the value that will be used
    http_port: 80

ロールを作成していて、ロールの値がそのロールで絶対的に使用され、インベントリーによって上書きされないようにしたい場合は、
それを ``roles/x/vars/main.yml`` に配置する必要があります。インベントリーの値はそれを上書きできません。ただし、``-e`` は次のようになります。

    ---
    # file: roles/x/vars/main.yml
    # this will absolutely be used in this role
    http_port: 80

これは、常に true となるロールの定数をプラグインする方法です。 ロールを他のユーザーと共有していない場合、
ポートなどの特定の動作は、ここで十分です。 しかし、他の人とロールを共有している場合は、
ここに変数を入れるのは適切できない場合があります。インベントリーでそれを上書きすることはできませんが、引き続きパラメーターをロールに渡すことで可能になります。

パラメーター化されたロールは便利です。

ロールを使用し、デフォルトを上書きする場合は、以下のようにパラメーターとしてロールに渡します。

    roles:
       - role: apache
         vars:
            http_port:8080

これにより、Playbook リーダーは、ロールのデフォルトをオーバーライドするか、
ロールがそれ自体では想定できない構成を渡すことを意識的に選択したことを明確にします。 また、他の人と共有しているロールの一部ではない、
サイト固有の何かを渡すこともできます。

これは、多くの場合は、一部のホストに複数回適用される可能性があります。例::

    roles:
       - role: app_user
         vars:
            myname:Ian
       - role: app_user
         vars:
           myname:Terry
       - role: app_user
         vars:
           myname:Graham
       - role: app_user
         vars:
           myname:John

この例では、同じロールが複数回呼び出されています。 指定している 
``name`` デフォルトがまったくなかった可能性が非常に高いです。 Ansible は、変数が定義されていない場合に警告できます。これは実際にはデフォルトの動作です。

ロールに関して他のいくつかのことを扱います。

一般的には、あるロールで設定される変数が他のロールでも利用できます。 これは、``roles/common/vars/main.yml`` がある場合に、
そこに変数を設定し、それを他のロールや Playbook の他の場所で使用できることを意味します::

     roles:
        - role: common_settings
        - role: something
          vars:
            foo:12
        - role: something_else

.. note:: namespace 変数を使用しなくてもいいように、いくつかの保護機能が導入されます。
          上記では、common_settings で定義された変数が、「something」タスクおよび「something_else」タスクに対して確実に使用できますが、
          「something」で、foo を 12 に設定していることが保証されている場合でも、foo を 20 に設定している場合があります。

そのため、それが優先事項であり、より直接的な方法で説明されています。 優先順位を気にする必要はありません。
自分のロールがデフォルトの変数を定義しているか、または確実に使用する「ライブ」変数を定義しているかを考えてください。 インベントリーの優先順位はちょうど真ん中にあり、
強制的に何かを上書きする場合は、``-e`` を使用します。

理解が困難な場合は、GitHub の `ansible-examples <https://github.com/ansible/ansible-examples>`_ リポジトリーでこれらすべての機能をどのように連携できるかについて確認してください。

高度な変数構文の使用
==============================

変数を宣言するために使用される高度な YAML 構文、および Ansible により使用される YAML ファイルにあるデータに対する制御の詳細は、「:ref:`playbooks_advanced_syntax`」を参照してください。

.. seealso::

   :ref:`about_playbooks`
       Playbook の概要
   :ref:`playbooks_conditionals`
       Playbook の条件付きステートメント
   :ref:`playbooks_filters`
       Jinja2 フィルターとそれらの使用
   :ref:`playbooks_loops`
       Playbook でのループ
   :ref:`playbooks_reuse_roles`
       ロール別の Playbook の組織
   :ref:`playbooks_best_practices`
       Playbook のベストプラクティス
   :ref:`special_variables`
       特殊な変数の一覧
   `ユーザーメーリングリスト <https://groups.google.com/group/ansible-devel>`_
       ご質問はございますか。 Google Group をご覧ください。
   `irc.freenode.net <http://irc.freenode.net>`_
       \#ansible IRC chat channel
