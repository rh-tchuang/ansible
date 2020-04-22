.. \_vmware\_troubleshooting:

**********************************
Ansible for VMware のトラブルシューティング
**********************************

.. contents:: トピック

本セクションでは、問題が発生する可能性があるものと、その修正方法を紹介します。

Ansible for VMware のデバッグ
============================

新しい問題をデバッグまたは作成する場合は、VMware インフラストラクチャーに関する情報が必要になります。この情報は、
`govc <https://github.com/vmware/govmomi/tree/master/govc>`_ を使用して取得できます。以下に例を示します。


.. code-block:: bash

    $ export GOVC_USERNAME=ESXI_OR_VCENTER_USERNAME
$ export GOVC_PASSWORD=ESXI_OR_VCENTER_PASSWORD
$ export GOVC_URL=https://ESXI_OR_VCENTER_HOSTNAME:443
$ govc find /

Ansible for VMware に関する既知の問題
====================================


Ubuntu 18.04 で vmware\_guest を使用したネットワーク設定
--------------------------------------------------

``open-vm-tools`` に ``netplan`` のサポートがないため、Ubuntu 18.04 で ``vmware_guest`` を使用してネットワークを設定すると破損することが知られています。
この問題は以下で追跡します。

* https://github.com/vmware/open-vm-tools/issues/240
* https://github.com/ansible/ansible/issues/41133

潜在的な回避策
^^^^^^^^^^^^^^^^^^^^^

この問題には、複数の回避策があります。

1) Ubuntu 18.04 イメージを変更し、``sudo apt install ifupdown`` でそのイメージに ``ifupdown`` をインストールします。
   必要な場合は、``sudo apt remove netplan.io`` で ``netplan`` を削除し、``sudo systemctl disable systemctl-networkd`` を使用して ``systemd-networkd`` を停止する必要があります。

2) VMware Ansible ロールでタスクを使用して ``systemd-networkd`` ファイルを生成します。

.. code-block:: yaml

   - name: make sure cache directory exists
     file: path="{{ inventory\_dir }}/cache" state=directory
     delegate\_to: localhost

   - name: generate network templates
     template: src=network.j2 dest="{{ inventory\_dir }}/cache/{{ inventory\_hostname }}.network"
     delegate\_to: localhost

   - name: copy generated files to vm
     vmware\_guest\_file\_operation:
       hostname: "{{ vmware\_general.hostname }}"
username: "{{ vmware\_username }}"
password: "{{ vmware\_password }}"
datacenter: "{{ vmware\_general.datacenter }}"
validate\_certs: "{{ vmware\_general.validate\_certs }}"
vm\_id: "{{ inventory\_hostname }}"
vm\_username: root
vm\_password: "{{ template\_password }}"
       copy:
       src: "{{ inventory\_dir }}/cache/{{ inventory\_hostname }}.network"
       dest: "/etc/systemd/network/ens160.network"
       overwrite:False
       delegate\_to: localhost

   - name: restart systemd-networkd
     vmware\_vm\_shell:
       hostname: "{{ vmware\_general.hostname }}"
username: "{{ vmware\_username }}"
password: "{{ vmware\_password }}"
datacenter: "{{ vmware\_general.datacenter }}"
folder: /vm
vm\_id: "{{ inventory\_hostname}}"
vm\_username: root
vm\_password: "{{ template\_password }}"
       vm\_shell: /bin/systemctl
       vm\_shell\_args: " restart systemd-networkd"
       delegate\_to: localhost

   - name: restart systemd-resolved
     vmware\_vm\_shell:
       hostname: "{{ vmware\_general.hostname }}"
username: "{{ vmware\_username }}"
password: "{{ vmware\_password }}"
datacenter: "{{ vmware\_general.datacenter }}"
folder: /vm
vm\_id: "{{ inventory\_hostname}}"
vm\_username: root
vm\_password: "{{ template\_password }}"
       vm\_shell: /bin/systemctl
       vm\_shell\_args: " restart systemd-resolved"
       delegate\_to: localhost

3) ``open-vm-tools`` で ``netplan`` サポートを待ちます。
