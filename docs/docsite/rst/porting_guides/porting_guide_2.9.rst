
.. _porting_2.9_guide:

*************************
Ansible 2.9 ポーティングガイド
*************************

このセクションでは、Ansible 2.8 と Ansible 2.9 での動作の変更点について説明します。

本書では、このバージョンの Ansible で動作するように、Playbook、プラグイン、その他の Ansible インフラストラクチャーの更新を支援することが目的です。

このページと、`Ansible Changelog for 2.9 <https://github.com/ansible/ansible/blob/stable-2.9/changelogs/CHANGELOG-v2.9.rst>`_ をお読みいただくと、必要な更新を理解できます。

このドキュメントは、ポーティングに関するコレクションの一部です。ポーティングガイドの完全なリストは、『:ref:`ポーティングガイド<porting_guides>`』を参照してください。

.. contents:: トピック


Playbook
========

インベントリー
---------

 * インベントリーソースが ``hash_behaviour`` からの影響を受けるようになりました。Playbook を ``merge`` に設定している場合には、インベントリーから取得するデータが変更される可能性があるため、それに合わせて Playbook を更新する必要があります。デフォルト設定 (``overwrite``) を使用する場合は、変更はありません。以前は、インベントリーは、この設定を無視していました。

ループ
-----

Ansible 2.9 は、「安全でない」データをより確実に処理して、「安全でない」とマークされたデータがテンプレート化されるのを防ぎます。以前の Ansible バージョンでは、``lookup()`` を直接使用して返された全データに、再帰的に「安全でない」というマークを付けていましたが、返される要素が文字列の場合には、``with_X`` のスタイルループを使用してルックアップを間接的に使用して返された構造化データにだけ「安全でない」というマークを付けていました。Ansible 2.9 では、これら 2 つのアプローチを整合的に処理するようになりました。

その結果、``with_dict`` を使用して、テンプレート化できる値とキーが返された場合には、テンプレートは Ansible 2.9 では想定どおりに動作しなくなる可能性があります。

以前と同じ動作を可能にするには、``with_X`` から、:ref:`migrating_to_loop` で説明しているようなフィルターを付けた ``loop`` を使用するように切り替えてください。

コマンドライン
============

* Galaxy トークンファイルの場所が ``~/.ansible_galaxy`` から ``~/.ansible/galaxy_token`` に変更されました。:ref:`galaxy_token_path` 設定を使用して、パスとファイル名の両方を設定できます。


非推奨
==========

主な変更はありません。


コレクションローダーの変更
=========================

コレクションから PowerShell モジュールまたは C# モジュールのユーティリティーをインポートする方法は、Ansible 2.9 リリースで変更になりました。Ansible 2.8 では、ユーティリティーは、以下の構文でインポートされます。

.. code-block:: powershell

    #AnsibleRequires -CSharpUtil AnsibleCollections.namespace_name.collection_name.util_filename
    #AnsibleRequires -PowerShell AnsibleCollections.namespace_name.collection_name.util_filename

Ansible 2.9 では、上記は次のように変更されました。

.. code-block:: powershell

    #AnsibleRequires -CSharpUtil ansible_collections.namespace_name.collection_name.plugins.module_utils.util_filename
    #AnsibleRequires -PowerShell ansible_collections.namespace_name.collection_name.plugins.module_utils.util_filename

コレクションでインポートの名前を変更すると、新しい名前形式で、C# ユーティリティーの名前空間を更新する必要があります。これは、より詳細で、さまざまな種類のプラグインの中で、プラグイン名の競合を回避し、Python モジュールの仕組みでインポートが PowerShell でどのように機能するかを標準化するために作られました。


モジュール
=======

* 今回のリリースでは、``win_get_url`` および ``win_uri`` モジュールは、``ansible-httpget`` のデフォルトの``User-Agent`` でリクエストを送信するようになりました。これは、``http_agent`` キーを使用して変更できます。
* 今回のリリースでは、``apt`` モジュールは、独自の依存関係をインストールする場合に ``update_cache = false`` を尊重してキャッシュの更新をスキップするようになりました。``update_cache = true`` を明示的に設定するか、パラメーター ``update_cache`` を省略すると、独自の依存関係をインストールする場合にキャッシュが更新されるようになります。

``_facts`` から``_info`` への名前変更
--------------------------------------

モジュールにより :ref:`Ansible ファクト<vars_and_facts>` が返されないため、Ansible 2.9 では多くのモジュールの名前が ``<something>_facts`` から ``<something>_info`` に変更になりました。Ansible ファクトは特定のホストに関連しています。たとえば、ネットワークインターフェースの構成、UNIX サーバーのオペレーティングシステム、Windows ボックスにインストールされているパッケージのリストは、すべて Ansible ファクトです。名前が変更されたモジュールが返す値は、ホスト固有ではありません。たとえば、クラウドプロバイダーの地域データまたはアカウント情報などです。これらのモジュール名を変更すると、各モジュールセットが提供する戻り値のタイプが、より明確になります。

モジュールの記述
---------------

* 今回のリリースでは、モジュールおよび module_utils ファイルは、相対インポートを使用して他の module_utils ファイルを含めることができるようになりました。
  これは、特にコレクションで、長いインポート行を短縮するのに役立ちます。

  コレクションで相対インポートを使用する例:

  .. code-block:: python

    # ファイル: ansible_collections/my_namespace/my_collection/plugins/modules/my_module.py
    # 絶対インポートを使用してコレクションから module_utils をインポートする従来の手法:
    from ansible_collections.my_namespace.my_collection.plugins.module_utils import my_util
    # 相対インポートを使用する新しい手法:
    from ..module_utils import my_util

  Ansible に同梱されているモジュールと module_utils では、相対インポートも使用できますが、
  短縮される量は少なくなります。

  .. code-block:: python

    # ファイル: ansible/modules/system/ping.py
    # 絶対インポートを使用してコアから module_utils をインポートする従来の手法:
    from ansible.module_utils.basic import AnsibleModule
    # 相対インポートを使用する新しい手法:
    from ...module_utils.basic import AnsibleModule

  単一ドット (``.``) はそれぞれツリーの 1 レベルを表します (ファイルシステムの相対リンクの``../`` に相当)。

  .. seealso:: `The Python Relative Import Docs <https://www.python.org/dev/peps/pep-0328/#guido-s-decision>`_ では、相対インポートの記述方法をさらに詳しく説明しています。


削除されたモジュール
---------------

次のモジュールはもう存在していません。

* Apstra の ``aos_ *`` モジュール。 新しいモジュールは、`https://github.com/apstra <https://github.com/apstra>`_ を参照してください。
* ec2_ami_find では、代わりに :ref:`ec2_ami_facts <ec2_ami_facts_module>` が使用されます。
* kubernetes では、代わりに :ref:`k8s_raw <k8s_raw_module>` が使用されます。
* nxos_ip_interface では、代わりに :ref:`nxos_l3_interface <nxos_l3_interface_module>` が使用されます。
* nxos_portchannel では、代わりに :ref:`nxos_linkagg <nxos_linkagg_module>` が使用されます。
* nxos_switchport では、代わりに :ref:`nxos_l2_interface <nxos_l2_interface_module>` が使用されます。
* oc では、代わりに :ref:`openshift_raw <openshift_raw_module>` が使用されます。
* panos_nat_policy では、代わりに :ref:`panos_nat_rule <panos_nat_rule_module>` が使用されます。
* panos_security_policy では、代わりに :ref:`panos_security_rule <panos_security_rule_module>` が使用されます。
* vsphere_guest では、代わりに :ref:`vmware_guest <vmware_guest_module>` が使用されます。


非推奨のお知らせ
-------------------

次のモジュールは、Ansible 2.13 で削除されます。Playbook を随時、更新してください。

* cs_instance_facts では、代わりに :ref:`cs_instance_info <cs_instance_info_module>` が使用されます。

* cs_zone_facts では、代わりに :ref:`cs_zone_info <cs_zone_info_module>` が使用されます。

* digital_ocean_sshkey_facts では、代わりに :ref:`digital_ocean_sshkey_info <digital_ocean_sshkey_info_module>` が使用されます。

* eos_interface では、代わりに :ref:`eos_interfaces <eos_interfaces_module>` が使用されます。

* eos_l2_interface では、代わりに :ref:`eos_l2_interfaces <eos_l2_interfaces_module>` が使用されます。

* eos_l3_interface では、代わりに :ref:`eos_l3_interfaces <eos_l3_interfaces_module>` が使用されます。

* eos_linkagg では、代わりに :ref:`eos_lag_interfaces <eos_lag_interfaces_module>` が使用されます。

* eos_lldp_interface では、代わりに :ref:`eos_lldp_interfaces <eos_lldp_interfaces_module>` が使用されます。

* eos_vlan では、代わりに :ref:`eos_vlans <eos_vlans_module>` が使用されます。

* ios_interface では、代わりに :ref:`ios_interfaces <ios_interfaces_module>` が使用されます。

* ios_l2_interface では、代わりに :ref:`ios_l2_interfaces <ios_l2_interfaces_module>` が使用されます。

* ios_l3_interface では、代わりに :ref:`ios_l3_interfaces <ios_l3_interfaces_module>` が使用されます。

* ios_vlan では、代わりに :ref:`ios_vlans <ios_vlans_module>` が使用されます。

* iosxr_interface では、代わりに :ref:`iosxr_interfaces <iosxr_interfaces_module>` が使用されます。

* junos_interface では、代わりに :ref:`junos_interfaces <junos_interfaces_module>` が使用されます。

* junos_l2_interface では、代わりに :ref:`junos_l2_interfaces <junos_l2_interfaces_module>` が使用されます。

* junos_l3_interface では、代わりに :ref:`junos_l3_interfaces <junos_l3_interfaces_module>` が使用されます。

* junos_linkagg では、代わりに :ref:`junos_lag_interfaces <junos_lag_interfaces_module>` が使用されます。

* junos_lldp では、代わりに :ref:`junos_lldp_global <junos_lldp_global_module>` が使用されます。

* junos_lldp_interface では、代わりに :ref:`junos_lldp_interfaces <junos_lldp_interfaces_module>` が使用されます。

* junos_vlan では、代わりに :ref:`junos_vlans <junos_vlans_module>` が使用されます。

* lambda_facts では、代わりに :ref:`lambda_info <lambda_info_module>` が使用されます。

* na_ontap_gather_facts では、代わりに :ref:`na_ontap_info <na_ontap_info_module>` が使用されます。

* net_banner では、代わりにプラットフォーム固有の [netos]_banner モジュールが使用されます。

* net_interface では、代わりにプラットフォーム固有の新しい [netos]_interfaces モジュールが使用されます。

* net_l2_interface は、代わりにプラットフォーム固有の新しい [netos]_l2_interfacesモジュールが使用されます。

* net_l3_interface では、代わりにプラットフォーム固有の新しい [netos]_l3_interfaces モジュールが使用されます。

* net_linkagg では、代わりにプラットフォーム固有の新しい [netos]_lag モジュールが使用されます。

* net_lldp では、代わりにプラットフォーム固有の新しい [netos]_lldp_global モジュールが使用されます。

* net_lldp_interface では、代わりにプラットフォーム固有の新しい [netos]_lldp_interfaces モジュールが使用されます。

* net_logging では、代わりにプラットフォーム固有の [netos]_logging モジュールが使用されます。

* net_static_route では、代わりにプラットフォーム固有の [netos]_static_route モジュールが使用されます。

* net_system では、代わりにプラットフォーム固有の [netos]_system モジュールが使用されます。

* net_user では、代わりにプラットフォーム固有の [netos]_user モジュールが使用されます。

* net_vlan では、代わりにプラットフォーム固有の新しい [netos]_vlans モジュールが使用されます。

* net_vrf では、代わりにプラットフォーム固有の [netos]_vrf モジュールが使用されます。

* nginx_status_facts では、代わりに :ref:`nginx_status_info <nginx_status_info_module>` が使用されます。

* nxos_interface では、代わりに :ref:`nxos_interfaces <nxos_interfaces_module>` が使用されます。

* nxos_l2_interface では、代わりに :ref:`nxos_l2_interfaces <nxos_l2_interfaces_module>` が使用されます。

* nxos_l3_interface では、代わりに :ref:`nxos_l3_interfaces <nxos_l3_interfaces_module>` が使用されます。

* nxos_linkagg では、代わりに :ref:`nxos_lag_interfaces <nxos_lag_interfaces_module>` が使用されます。

* nxos_vlan では、代わりに :ref:`nxos_vlans <nxos_vlans_module>` が使用されます。

* online_server_facts では、代わりに :ref:`online_server_info <online_server_info_module>` が使用されます。

* online_user_facts では、代わりに :ref:`online_user_info <online_user_info_module>` が使用されます。

* purefa_facts では、代わりに :ref:`purefa_info <purefa_info_module>` が使用されます。

* purefb_facts では、代わりに :ref:`purefb_info <purefb_info_module>` が使用されます。

* scaleway_image_facts では、代わりに :ref:`scaleway_image_info <scaleway_image_info_module>` が使用されます。

* scaleway_ip_facts では、代わりに :ref:`scaleway_ip_info <scaleway_ip_info_module>` が使用されます。

* scaleway_organization_facts では、代わりに :ref:`scaleway_organization_info <scaleway_organization_info_module>` が使用されます。

* scaleway_security_group_facts では、代わりに :ref:`scaleway_security_group_info <scaleway_security_group_info_module>` が使用されます。

* scaleway_server_facts では、代わりに :ref:`scaleway_server_info <scaleway_server_info_module>` が使用されます。

* scaleway_snapshot_facts では、代わりに :ref:`scaleway_snapshot_info <scaleway_snapshot_info_module>` が使用されます。

* scaleway_volume_facts では、代わりに :ref:`scaleway_volume_info <scaleway_volume_info_module>` が使用されます。

* vcenter_extension_facts では、代わりに :ref:`vcenter_extension_info <vcenter_extension_info_module>` が使用されます。

* vmware_about_facts では、代わりに :ref:`vmware_about_info <vmware_about_info_module>` が使用されます。

* vmware_category_facts では、代わりに :ref:`vmware_category_info <vmware_category_info_module>` が使用されます。

* vmware_drs_group_facts では、代わりに :ref:`vmware_drs_group_info <vmware_drs_group_info_module>` が使用されます。

* vmware_drs_rule_facts では、代わりに :ref:`vmware_drs_rule_info <vmware_drs_rule_info_module>` が使用されます。

* vmware_dvs_portgroup_facts では、代わりに :ref:`vmware_dvs_portgroup_info <vmware_dvs_portgroup_info_module>` が使用されます。

* vmware_guest_boot_facts では、代わりに :ref:`vmware_guest_boot_info <vmware_guest_boot_info_module>` が使用されます。

* vmware_guest_customization_facts では、代わりに :ref:`vmware_guest_customization_info <vmware_guest_customization_info_module>` が使用されます。

* vmware_guest_disk_facts では、代わりに :ref:`vmware_guest_disk_info <vmware_guest_disk_info_module>` が使用されます。

* vmware_host_capability_facts では、代わりに :ref:`vmware_host_capability_info <vmware_host_capability_info_module>` が使用されます。

* vmware_host_config_facts では、代わりに :ref:`vmware_host_config_info <vmware_host_config_info_module>` が使用されます。

* vmware_host_dns_facts では、代わりに :ref:`vmware_host_dns_info <vmware_host_dns_info_module>` が使用されます。

* vmware_host_feature_facts では、代わりに :ref:`vmware_host_feature_info <vmware_host_feature_info_module>` が使用されます。

* vmware_host_firewall_facts では、代わりに :ref:`vmware_host_firewall_info <vmware_host_firewall_info_module>` が使用されます。

* vmware_host_ntp_facts では、代わりに :ref:`vmware_host_ntp_info <vmware_host_ntp_info_module>` が使用されます。

* vmware_host_package_facts では、:ref:`vmware_host_package_info <vmware_host_package_info_module>` が使用されます。

* vmware_host_service_facts では、代わりに :ref:`vmware_host_service_info <vmware_host_service_info_module>` が使用されます。

* vmware_host_ssl_facts では、代わりに :ref:`vmware_host_ssl_info <vmware_host_ssl_info_module>` が使用されます。

* vmware_host_vmhba_facts では、代わりに :ref:`vmware_host_vmhba_info <vmware_host_vmhba_info_module>` が使用されます。

* vmware_host_vmnic_facts では、代わりに :ref:`vmware_host_vmnic_info <vmware_host_vmnic_info_module>` が使用されます。

* vmware_local_role_facts では、代わりに :ref:`vmware_local_role_info <vmware_local_role_info_module>` が使用されます。

* vmware_local_user_facts では、代わりに :ref:`vmware_local_user_info <vmware_local_user_info_module>` が使用されます。

* vmware_portgroup_facts では、代わりに :ref:`vmware_portgroup_info <vmware_portgroup_info_module>` が使用されます。

* vmware_resource_pool_facts では、代わりに :ref:`vmware_resource_pool_info <vmware_resource_pool_info_module>` が使用されます。

* vmware_target_canonical_facts では、代わりに :ref:`vmware_target_canonical_info <vmware_target_canonical_info_module>` が使用されます。

* vmware_vmkernel_facts では、代わりに :ref:`vmware_vmkernel_info <vmware_vmkernel_info_module>` が使用されます。

* vmware_vswitch_facts では、代わりに :ref:`vmware_vswitch_info <vmware_vswitch_info_module>` が使用されます。

* vultr_account_facts では、代わりに :ref:`vultr_account_info <vultr_account_info_module>` が使用されます。

* vultr_block_storage_facts では、代わりに :ref:`vultr_block_storage_info <vultr_block_storage_info_module>` が使用されます。

* vultr_dns_domain_facts では、代わりに :ref:`vultr_dns_domain_info <vultr_dns_domain_info_module>` が使用されます。

* vultr_firewall_group_facts では、代わりに :ref:`vultr_firewall_group_info <vultr_firewall_group_info_module>` が使用されます。

* vultr_network_facts では、代わりに :ref:`vultr_network_info <vultr_network_info_module>` が使用されます。

* vultr_os_facts では、代わりに :ref:`vultr_os_info <vultr_os_info_module>` が使用されます。

* vultr_plan_facts では、代わりに :ref:`vultr_plan_info <vultr_plan_info_module>` が使用されます。

* vultr_region_facts では、代わりに :ref:`vultr_region_info <vultr_region_info_module>` が使用されます。

* vultr_server_facts では、代わりに :ref:`vultr_server_info <vultr_server_info_module>` が使用されます。

* vultr_ssh_key_facts では、代わりに :ref:`vultr_ssh_key_info <vultr_ssh_key_info_module>` が使用されます。

* vultr_startup_script_facts では、代わりに :ref:`vultr_startup_script_info <vultr_startup_script_info_module>` が使用されます。

* vultr_user_facts では、代わりに :ref:`vultr_user_info <vultr_user_info_module>` が使用されます。

* vyos_interface では、代わりに :ref:`vyos_interfaces <vyos_interfaces_module>` が使用されます。

* vyos_l3_interface では、代わりに :ref:`vyos_l3_interfaces <vyos_l3_interfaces_module>` が使用されます。

* vyos_linkagg では、代わりに :ref:`vyos_lag_interfaces <vyos_lag_interfaces_module>` が使用されます。

* vyos_lldp では、代わりに :ref:`vyos_lldp_global <vyos_lldp_global_module>` が使用されます。

* vyos_lldp_interface では、代わりに :ref:`vyos_lldp_interfaces <vyos_lldp_interfaces_module>` が使用されます。


次の機能は、Ansible 2.12 で削除されます。Playbook を随時、更新してください。

* ``vmware_cluster`` DRS、HA、および VSAN の設定では、代わりに :ref:`vmware_cluster_drs <vmware_cluster_drs_module>`、:ref:`vmware_cluster_ha <vmware_cluster_ha_module>`、および :ref:`vmware_cluster_vsan <vmware_cluster_vsan_module>` が使用されます。


次の機能は、Ansible 2.13 で削除されます。Playbook を随時、更新してください。

* ``openssl_certificate`` で ``assertonly`` プロバイダーが廃止されます。
  
  プロバイダーを、:ref:`openssl_certificate_info <openssl_certificate_info_module>` モジュール、
  :ref:`openssl_csr_info <openssl_csr_info_module>` モジュール、:ref:`openssl_privatekey_info <openssl_privatekey_info_module>`
   モジュール、および :ref:`assert <assert_module>` モジュールに置き換える方法は、:ref:`openssl_certificate <openssl_certificate_module>` ドキュメントで紹介されている例を参照してください。


以下のモジュールは、PyOpenSSL ベースのバックエンド ``pyopenssl`` がすでに非推奨になっており、
Ansible 2.13 で削除されます。

* :ref:`get_certificate <get_certificate_module>`
* :ref:`openssl_certificate <openssl_certificate_module>`
* :ref:`openssl_certificate_info <openssl_certificate_info_module>`
* :ref:`openssl_csr <openssl_csr_module>`
* :ref:`openssl_csr_info <openssl_csr_info_module>`
* :ref:`openssl_privatekey <openssl_privatekey_module>`
* :ref:`openssl_privatekey_info <openssl_privatekey_info_module>`
* :ref:`openssl_publickey <openssl_publickey_module>`


名前が変更されたモジュール
^^^^^^^^^^^^^^^

次のモジュールの名前が変更されました。以前の名前は非推奨となり、
Ansible 2.13 で削除されます。Playbook を随時、更新してください。

* ``ali_instance_facts`` モジュールの名前が :ref:`ali_instance_info <ali_instance_info_module>` に変更されました。
* ``aws_acm_facts`` モジュールの名前が :ref:`aws_acm_info <aws_acm_info_module>` に変更されました。
* ``aws_az_facts`` モジュールの名前が :ref:`aws_az_info <aws_az_info_module>` に変更されました。
* ``aws_caller_facts`` モジュールの名前が :ref:`aws_caller_info <aws_caller_info_module>` に変更されました。
* ``aws_kms_facts`` モジュールの名前が :ref:`aws_kms_info <aws_kms_info_module>` に変更されました。
* ``aws_region_facts`` モジュールの名前が :ref:`aws_region_info <aws_region_info_module>` に変更されました。
* ``aws_s3_bucket_facts`` モジュールの名前が :ref:`aws_s3_bucket_info <aws_s3_bucket_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``aws_sgw_facts`` モジュールの名前が :ref:`aws_sgw_info <aws_sgw_info_module>` に変更されました。
* ``aws_waf_facts`` モジュールの名前が :ref:`aws_waf_info <aws_waf_info_module>` に変更されました。
* ``azure_rm_aks_facts`` モジュールの名前が :ref:`azure_rm_aks_info <azure_rm_aks_info_module>` に変更されました。
* ``azure_rm_aksversion_facts`` モジュールの名前が :ref:`azure_rm_aksversion_info <azure_rm_aksversion_info_module>` に変更されました。
* ``azure_rm_applicationsecuritygroup_facts`` モジュールの名前が :ref:`azure_rm_applicationsecuritygroup_info <azure_rm_applicationsecuritygroup_info_module>` に変更されました。
* ``azure_rm_appserviceplan_facts`` モジュールの名前が :ref:`azure_rm_appserviceplan_info <azure_rm_appserviceplan_info_module>` に変更されました。
* ``azure_rm_automationaccount_facts`` モジュールの名前が :ref:`azure_rm_automationaccount_info <azure_rm_automationaccount_info_module>` に変更されました。
* ``azure_rm_autoscale_facts`` モジュールの名前が :ref:`azure_rm_autoscale_info <azure_rm_autoscale_info_module>` に変更されました。
* ``azure_rm_availabilityset_facts`` モジュールの名前が :ref:`azure_rm_availabilityset_info <azure_rm_availabilityset_info_module>` に変更されました。
* ``azure_rm_cdnendpoint_facts`` モジュールの名前が :ref:`azure_rm_cdnendpoint_info <azure_rm_cdnendpoint_info_module>` に変更されました。
* ``azure_rm_cdnprofile_facts`` モジュールの名前が :ref:`azure_rm_cdnprofile_info <azure_rm_cdnprofile_info_module>` に変更されました。
* ``azure_rm_containerinstance_facts`` モジュールの名前が :ref:`azure_rm_containerinstance_info <azure_rm_containerinstance_info_module>` に変更されました。
* ``azure_rm_containerregistry_facts`` モジュールの名前が :ref:`azure_rm_containerregistry_info <azure_rm_containerregistry_info_module>` に変更されました。
* ``azure_rm_cosmosdbaccount_facts`` モジュールの名前が :ref:`azure_rm_cosmosdbaccount_info <azure_rm_cosmosdbaccount_info_module>` に変更されました。
* ``azure_rm_deployment_facts`` モジュールの名前が :ref:`azure_rm_deployment_info <azure_rm_deployment_info_module>` に変更されました。
* ``azure_rm_resourcegroup_facts`` モジュールの名前が :ref:`azure_rm_resourcegroup_info <azure_rm_resourcegroup_info_module>` に変更されました。
* ``bigip_device_facts`` モジュールの名前が :ref:`bigip_device_info <bigip_device_info_module>` に変更されました。
* ``bigiq_device_facts`` モジュールの名前が :ref:`bigiq_device_info <bigiq_device_info_module>` に変更されました。
* ``cloudformation_facts`` モジュールの名前が :ref:`cloudformation_info <cloudformation_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``cloudfront_facts`` モジュールの名前が :ref:`cloudfront_info <cloudfront_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``cloudwatchlogs_log_group_facts`` モジュールの名前が :ref:`cloudwatchlogs_log_group_info <cloudwatchlogs_log_group_info_module>` に変更されました。
* ``digital_ocean_account_facts`` モジュールの名前が :ref:`digital_ocean_account_info <digital_ocean_account_info_module>` に変更されました。
* ``digital_ocean_certificate_facts`` モジュールの名前が :ref:`digital_ocean_certificate_info <digital_ocean_certificate_info_module>` に変更されました。
* ``digital_ocean_domain_facts`` モジュールの名前が :ref:`digital_ocean_domain_info <digital_ocean_domain_info_module>` に変更されました。
* ``digital_ocean_firewall_facts`` モジュールの名前が :ref:`digital_ocean_firewall_info <digital_ocean_firewall_info_module>` に変更されました。
* ``digital_ocean_floating_ip_facts`` モジュールの名前が :ref:`digital_ocean_floating_ip_info <digital_ocean_floating_ip_info_module>` に変更されました。
* ``digital_ocean_image_facts`` モジュールの名前が :ref:`digital_ocean_image_info <digital_ocean_image_info_module>` に変更されました。
* ``digital_ocean_load_balancer_facts`` モジュールの名前が :ref:`digital_ocean_load_balancer_info <digital_ocean_load_balancer_info_module>` に変更されました。
* ``digital_ocean_region_facts`` モジュールの名前が :ref:`digital_ocean_region_info <digital_ocean_region_info_module>` に変更されました。
* ``digital_ocean_size_facts`` モジュールの名前が :ref:`digital_ocean_size_info <digital_ocean_size_info_module>` に変更されました。
* ``digital_ocean_snapshot_facts`` モジュールの名前が :ref:`digital_ocean_snapshot_info <digital_ocean_snapshot_info_module>` に変更されました。
* ``digital_ocean_tag_facts`` モジュールの名前が :ref:`digital_ocean_tag_info <digital_ocean_tag_info_module>` に変更されました。
* ``digital_ocean_volume_facts`` モジュールの名前が :ref:`digital_ocean_volume_info <digital_ocean_volume_info_module>` に変更されました。
* ``ec2_ami_facts`` モジュールの名前が :ref:`ec2_ami_info <ec2_ami_info_module>` に変更されました。
* ``ec2_asg_facts`` モジュールの名前が :ref:`ec2_asg_info <ec2_asg_info_module>` に変更されました。
* ``ec2_customer_gateway_facts`` モジュールの名前が :ref:`ec2_customer_gateway_info <ec2_customer_gateway_info_module>` に変更されました。
* ``ec2_eip_facts`` モジュールの名前が :ref:`ec2_eip_info <ec2_eip_info_module>` に変更されました。
* ``ec2_elb_facts`` モジュールの名前が :ref:`ec2_elb_info <ec2_elb_info_module>` に変更されました。
* ``ec2_eni_facts`` モジュールの名前が :ref:`ec2_eni_info <ec2_eni_info_module>` に変更されました。
* ``ec2_group_facts`` モジュールの名前が :ref:`ec2_group_info <ec2_group_info_module>` に変更されました。
* ``ec2_instance_facts`` モジュールの名前が :ref:`ec2_instance_info <ec2_instance_info_module>` に変更されました。
* ``ec2_lc_facts`` モジュールの名前が :ref:`ec2_lc_info <ec2_lc_info_module>` に変更されました。
* ``ec2_placement_group_facts`` モジュールの名前が :ref:`ec2_placement_group_info <ec2_placement_group_info_module>` に変更されました。
* ``ec2_snapshot_facts`` モジュールの名前が :ref:`ec2_snapshot_info <ec2_snapshot_info_module>` に変更されました。
* ``ec2_vol_facts`` モジュールの名前が :ref:`ec2_vol_info <ec2_vol_info_module>` に変更されました。
* ``ec2_vpc_dhcp_option_facts`` モジュールの名前が :ref:`ec2_vpc_dhcp_option_info <ec2_vpc_dhcp_option_info_module>` に変更されました。
* ``ec2_vpc_endpoint_facts`` モジュールの名前が :ref:`ec2_vpc_endpoint_info <ec2_vpc_endpoint_info_module>` に変更されました。
* ``ec2_vpc_igw_facts`` モジュールの名前が :ref:`ec2_vpc_igw_info <ec2_vpc_igw_info_module>` に変更されました。
* ``ec2_vpc_nacl_facts`` モジュールの名前が :ref:`ec2_vpc_nacl_info <ec2_vpc_nacl_info_module>` に変更されました。
* ``ec2_vpc_nat_gateway_facts`` モジュールの名前が :ref:`ec2_vpc_nat_gateway_info <ec2_vpc_nat_gateway_info_module>` に変更されました。
* ``ec2_vpc_net_facts`` モジュールの名前が :ref:`ec2_vpc_net_info <ec2_vpc_net_info_module>` に変更されました。
* ``ec2_vpc_peering_facts`` モジュールの名前が :ref:`ec2_vpc_peering_info <ec2_vpc_peering_info_module>` に変更されました。
* ``ec2_vpc_route_table_facts`` モジュールの名前が :ref:`ec2_vpc_route_table_info <ec2_vpc_route_table_info_module>` に変更されました。
* ``ec2_vpc_subnet_facts`` モジュールの名前が :ref:`ec2_vpc_subnet_info <ec2_vpc_subnet_info_module>` に変更されました。
* ``ec2_vpc_vgw_facts`` モジュールの名前が :ref:`ec2_vpc_vgw_info <ec2_vpc_vgw_info_module>` に変更されました。
* ``ec2_vpc_vpn_facts`` モジュールの名前が :ref:`ec2_vpc_vpn_info <ec2_vpc_vpn_info_module>` に変更されました。
* ``ecs_service_facts`` モジュールの名前が :ref:`ecs_service_info <ecs_service_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ecs_taskdefinition_facts`` モジュールの名前が :ref:`ecs_taskdefinition_info <ecs_taskdefinition_info_module>` に変更されました。
* ``efs_facts`` モジュールの名前が :ref:`efs_info <efs_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``elasticache_facts`` モジュールの名前が :ref:`elasticache_info <elasticache_info_module>` に変更されました。
* ``elb_application_lb_facts`` モジュールの名前が :ref:`elb_application_lb_info <elb_application_lb_info_module>` に変更されました。
* ``elb_classic_lb_facts`` モジュールの名前が :ref:`elb_classic_lb_info <elb_classic_lb_info_module>` に変更されました。
* ``elb_target_facts`` モジュールの名前が :ref:`elb_target_info <elb_target_info_module>` に変更されました。
* ``elb_target_group_facts`` モジュールの名前が :ref:`elb_target_group_info <elb_target_group_info_module>` に変更されました。
* ``gcp_bigquery_dataset_facts`` モジュールの名前が :ref:`gcp_bigquery_dataset_info <gcp_bigquery_dataset_info_module>` に変更されました。
* ``gcp_bigquery_table_facts`` モジュールの名前が :ref:`gcp_bigquery_table_info <gcp_bigquery_table_info_module>` に変更されました。
* ``gcp_cloudbuild_trigger_facts`` モジュールの名前が :ref:`gcp_cloudbuild_trigger_info <gcp_cloudbuild_trigger_info_module>` に変更されました。
* ``gcp_compute_address_facts`` モジュールの名前が :ref:`gcp_compute_address_info <gcp_compute_address_info_module>` に変更されました。
* ``gcp_compute_backend_bucket_facts`` モジュールの名前が :ref:`gcp_compute_backend_bucket_info <gcp_compute_backend_bucket_info_module>` に変更されました。
* ``gcp_compute_backend_service_facts`` モジュールの名前が :ref:`gcp_compute_backend_service_info <gcp_compute_backend_service_info_module>` に変更されました。
* ``gcp_compute_disk_facts`` モジュールの名前が :ref:`gcp_compute_disk_info <gcp_compute_disk_info_module>` に変更されました。
* ``gcp_compute_firewall_facts`` モジュールの名前が :ref:`gcp_compute_firewall_info <gcp_compute_firewall_info_module>` に変更されました。
* ``gcp_compute_forwarding_rule_facts`` モジュールの名前が :ref:`gcp_compute_forwarding_rule_info <gcp_compute_forwarding_rule_info_module>` に変更されました。
* ``gcp_compute_global_address_facts`` モジュールの名前が :ref:`gcp_compute_global_address_info <gcp_compute_global_address_info_module>` に変更されました。
* ``gcp_compute_global_forwarding_rule_facts`` モジュールの名前が :ref:`gcp_compute_global_forwarding_rule_info <gcp_compute_global_forwarding_rule_info_module>` に変更されました。
* ``gcp_compute_health_check_facts`` モジュールの名前が :ref:`gcp_compute_health_check_info <gcp_compute_health_check_info_module>` に変更されました。
* ``gcp_compute_http_health_check_facts`` モジュールの名前が :ref:`gcp_compute_http_health_check_info <gcp_compute_http_health_check_info_module>` に変更されました。
* ``gcp_compute_https_health_check_facts`` モジュールの名前が :ref:`gcp_compute_https_health_check_info <gcp_compute_https_health_check_info_module>` に変更されました。
* ``gcp_compute_image_facts`` モジュールの名前が :ref:`gcp_compute_image_info <gcp_compute_image_info_module>` に変更されました。
* ``gcp_compute_instance_facts`` モジュールの名前が:ref:`gcp_compute_instance_info <gcp_compute_instance_info_module>` に変更されました。
* ``gcp_compute_instance_group_facts`` モジュールの名前が :ref:`gcp_compute_instance_group_info <gcp_compute_instance_group_info_module>` に変更されました。
* ``gcp_compute_instance_group_manager_facts`` モジュールの名前が :ref:`gcp_compute_instance_group_manager_info <gcp_compute_instance_group_manager_info_module>` に変更されました。
* ``gcp_compute_instance_template_facts`` モジュールの名前が :ref:`gcp_compute_instance_template_info <gcp_compute_instance_template_info_module>` に変更されました。
* ``gcp_compute_interconnect_attachment_facts`` モジュールの名前が:ref: `gcp_compute_interconnect_attachment_info <gcp_compute_interconnect_attachment_info_module>` に変更されました。
* ``gcp_compute_network_facts`` モジュールの名前が :ref:`gcp_compute_network_info <gcp_compute_network_info_module>` に変更されました。
* ``gcp_compute_region_disk_facts`` モジュールの名前が :ref:`gcp_compute_region_disk_info <gcp_compute_region_disk_info_module>` に変更されました。
* ``gcp_compute_route_facts`` モジュールの名前が :ref:`gcp_compute_route_info <gcp_compute_route_info_module>` に変更されました。
* ``gcp_compute_router_facts`` モジュールの名前が :ref:`gcp_compute_router_info <gcp_compute_router_info_module>` に変更されました。
* ``gcp_compute_ssl_certificate_facts`` モジュールの名前が :ref:`gcp_compute_ssl_certificate_info <gcp_compute_ssl_certificate_info_module>` に変更されました。
* ``gcp_compute_ssl_policy_facts`` モジュールの名前が :ref:`gcp_compute_ssl_policy_info <gcp_compute_ssl_policy_info_module>` に変更されました。
* ``gcp_compute_subnetwork_facts`` モジュールの名前が :ref:`gcp_compute_subnetwork_info <gcp_compute_subnetwork_info_module>` に変更されました。
* ``gcp_compute_target_http_proxy_facts`` モジュールの名前が :ref:`gcp_compute_target_http_proxy_info <gcp_compute_target_http_proxy_info_module>` に変更されました。
* ``gcp_compute_target_https_proxy_facts`` モジュールの名前が :ref:`gcp_compute_target_https_proxy_info <gcp_compute_target_https_proxy_info_module>` に変更されました。
* ``gcp_compute_target_pool_facts`` モジュールの名前が :ref:`gcp_compute_target_pool_info <gcp_compute_target_pool_info_module>` に変更されました。
* ``gcp_compute_target_ssl_proxy_facts`` モジュールの名前が :ref:`gcp_compute_target_ssl_proxy_info <gcp_compute_target_ssl_proxy_info_module>` に変更されました。
* ``gcp_compute_target_tcp_proxy_facts`` モジュールの名前が :ref:`gcp_compute_target_tcp_proxy_info <gcp_compute_target_tcp_proxy_info_module>` に変更されました。
* ``gcp_compute_target_vpn_gateway_facts`` モジュールの名前が :ref:`gcp_compute_target_vpn_gateway_info <gcp_compute_target_vpn_gateway_info_module>` に変更されました。
* ``gcp_compute_url_map_facts`` モジュールの名前が :ref:`gcp_compute_url_map_info <gcp_compute_url_map_info_module>` に変更されました。
* ``gcp_compute_vpn_tunnel_facts`` モジュールの名前が :ref:`gcp_compute_vpn_tunnel_info <gcp_compute_vpn_tunnel_info_module>` に変更されました。
* ``gcp_container_cluster_facts`` モジュールの名前が :ref:`gcp_container_cluster_info <gcp_container_cluster_info_module>` に変更されました。
* ``gcp_container_node_pool_facts`` モジュールの名前が :ref:`gcp_container_node_pool_info <gcp_container_node_pool_info_module>` に変更されました。
* ``gcp_dns_managed_zone_facts`` モジュールの名前が :ref:`gcp_dns_managed_zone_info <gcp_dns_managed_zone_info_module>` に変更されました。
* ``gcp_dns_resource_record_set_facts`` モジュールの名前が :ref:`gcp_dns_resource_record_set_info <gcp_dns_resource_record_set_info_module>` に変更されました。
* ``gcp_iam_role_facts`` モジュールの名前が :ref:`gcp_iam_role_info <gcp_iam_role_info_module>` に変更されました。
* ``gcp_iam_service_account_facts`` モジュールの名前が :ref:`gcp_iam_service_account_info <gcp_iam_service_account_info_module>` に変更されました。
* ``gcp_pubsub_subscription_facts`` モジュールの名前が :ref:`gcp_pubsub_subscription_info <gcp_pubsub_subscription_info_module>` に変更されました。
* ``gcp_pubsub_topic_facts`` モジュールの名前が :ref:`gcp_pubsub_topic_info <gcp_pubsub_topic_info_module>` に変更されました。
* ``gcp_redis_instance_facts`` モジュールの名前が :ref:`gcp_redis_instance_info <gcp_redis_instance_info_module>` に変更されました。
* ``gcp_resourcemanager_project_facts`` モジュールの名前が :ref:`gcp_resourcemanager_project_info <gcp_resourcemanager_project_info_module>` に変更されました。
* ``gcp_sourcerepo_repository_facts`` モジュールの名前が :ref:`gcp_sourcerepo_repository_info <gcp_sourcerepo_repository_info_module>` に変更されました。
* ``gcp_spanner_database_facts`` モジュールの名前が :ref:`gcp_spanner_database_info <gcp_spanner_database_info_module>` に変更されました。
* ``gcp_spanner_instance_facts`` モジュールの名前が :ref:`gcp_spanner_instance_info <gcp_spanner_instance_info_module>` に変更されました。
* ``gcp_sql_database_facts`` モジュールの名前が :ref:`gcp_sql_database_info <gcp_sql_database_info_module>` に変更されました。
* ``gcp_sql_instance_facts`` モジュールの名前が :ref:`gcp_sql_instance_info <gcp_sql_instance_info_module>` に変更されました。
* ``gcp_sql_user_facts`` モジュールの名前が :ref:`gcp_sql_user_info <gcp_sql_user_info_module>` に変更されました。
* ``gcp_tpu_node_facts`` モジュールの名前が :ref:`gcp_tpu_node_info <gcp_tpu_node_info_module>` に変更されました。
* ``gcpubsub_facts`` モジュールの名前が :ref:`gcpubsub_info <gcpubsub_info_module>` に変更されました。
* ``github_webhook_facts`` モジュールの名前が :ref:`github_webhook_info <github_webhook_info_module>` に変更されました。
* ``gluster_heal_facts`` モジュールの名前が :ref:`gluster_heal_info <gluster_heal_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_datacenter_facts`` モジュールの名前が :ref:`hcloud_datacenter_info <hcloud_datacenter_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_floating_ip_facts`` モジュールの名前が :ref:`hcloud_floating_ip_info <hcloud_floating_ip_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_image_facts`` モジュールの名前が :ref:`hcloud_image_info <hcloud_image_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_location_facts`` モジュールの名前が :ref:`hcloud_location_info <hcloud_location_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_server_facts`` モジュールの名前が :ref:`hcloud_server_info <hcloud_server_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_server_type_facts`` モジュールの名前が :ref:`hcloud_server_type_info <hcloud_server_type_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_ssh_key_facts`` モジュールの名前が :ref:`hcloud_ssh_key_info <hcloud_ssh_key_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hcloud_volume_facts`` モジュールの名前が :ref:`hcloud_volume_info <hcloud_volume_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``hpilo_facts`` モジュールの名前が :ref:`hpilo_info <hpilo_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``iam_mfa_device_facts`` モジュールの名前が :ref:`iam_mfa_device_info <iam_mfa_device_info_module>` に変更されました。
* ``iam_role_facts`` モジュールの名前が :ref:`iam_role_info <iam_role_info_module>` に変更されました。
* ``iam_server_certificate_facts`` モジュールの名前が :ref:`iam_server_certificate_info <iam_server_certificate_info_module>` に変更されました。
* ``idrac_redfish_facts`` モジュールの名前が :ref:`idrac_redfish_info <idrac_redfish_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``intersight_facts`` モジュールの名前が :ref:`intersight_info <intersight_info_module>` に変更されました。
* ``jenkins_job_facts`` モジュールの名前が :ref:`jenkins_job_info <jenkins_job_info_module>` に変更されました。
* ``k8s_facts`` モジュールの名前が :ref:`k8s_info <k8s_info_module>` に変更されました。
* ``memset_memstore_facts`` モジュールの名前が :ref:`memset_memstore_info <memset_memstore_info_module>` に変更されました。
* ``memset_server_facts`` モジュールの名前が :ref:`memset_server_info <memset_server_info_module>` に変更されました。
* ``one_image_facts`` モジュールの名前が :ref:`one_image_info <one_image_info_module>` に変更されました。
* ``onepassword_facts`` モジュールの名前が :ref:`onepassword_info <onepassword_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_datacenter_facts`` モジュールの名前が :ref:`oneview_datacenter_info <oneview_datacenter_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_enclosure_facts`` モジュールの名前が :ref:`oneview_enclosure_info <oneview_enclosure_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_ethernet_network_facts`` モジュールの名前が :ref:`oneview_ethernet_network_info <oneview_ethernet_network_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_fc_network_facts`` モジュールの名前が :ref:`oneview_fc_network_info <oneview_fc_network_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_fcoe_network_facts`` モジュールの名前が :ref:`oneview_fcoe_network_info <oneview_fcoe_network_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_logical_interconnect_group_facts`` モジュールの名前が :ref:`oneview_logical_interconnect_group_info <oneview_logical_interconnect_group_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_network_set_facts`` モジュールの名前が :ref:`oneview_network_set_info <oneview_network_set_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``oneview_san_manager_facts`` モジュールの名前が :ref:`oneview_san_manager_info <oneview_san_manager_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_flavor_facts`` モジュールの名前が :ref:`os_flavor_info <os_flavor_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_image_facts`` モジュールの名前が :ref:`os_image_info <os_image_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_keystone_domain_facts`` モジュールの名前が :ref:`os_keystone_domain_info <os_keystone_domain_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_networks_facts`` モジュールの名前が :ref:`os_networks_info <os_networks_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_port_facts`` モジュールの名前が :ref:`os_port_info <os_port_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_project_facts`` モジュールの名前が :ref:`os_project_info <os_project_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_server_facts`` モジュールの名前が :ref:`os_server_info <os_server_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_subnets_facts`` モジュールの名前が :ref:`os_subnets_info <os_subnets_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``os_user_facts`` モジュールの名前が :ref:`os_user_info <os_user_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_affinity_label_facts`` モジュールの名前が :ref:`ovirt_affinity_label_info <ovirt_affinity_label_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_api_facts`` モジュールの名前が :ref:`ovirt_api_info <ovirt_api_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_cluster_facts`` モジュールの名前が :ref:`ovirt_cluster_info <ovirt_cluster_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_datacenter_facts`` モジュールの名前が :ref:`ovirt_datacenter_info <ovirt_datacenter_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_disk_facts`` モジュールの名前が :ref:`ovirt_disk_info <ovirt_disk_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_event_facts`` モジュールの名前が :ref:`ovirt_event_info <ovirt_event_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_external_provider_facts`` モジュールの名前が :ref:`ovirt_external_provider_info <ovirt_external_provider_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_group_facts`` モジュールの名前が :ref:`ovirt_group_info <ovirt_group_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_host_facts`` モジュールの名前が :ref:`ovirt_host_info <ovirt_host_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_host_storage_facts`` モジュールの名前が :ref:`ovirt_host_storage_info <ovirt_host_storage_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_network_facts`` モジュールの名前が :ref:`ovirt_network_info <ovirt_network_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_nic_facts`` モジュールの名前が :ref:`ovirt_nic_info <ovirt_nic_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_permission_facts`` モジュールの名前が :ref:`ovirt_permission_info <ovirt_permission_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_quota_facts`` モジュールの名前が :ref:`ovirt_quota_info <ovirt_quota_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_scheduling_policy_facts`` モジュールの名前が :ref:`ovirt_scheduling_policy_info <ovirt_scheduling_policy_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_snapshot_facts`` モジュールの名前が :ref:`ovirt_snapshot_info <ovirt_snapshot_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_storage_domain_facts`` モジュールの名前が :ref:`ovirt_storage_domain_info <ovirt_storage_domain_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_storage_template_facts`` モジュールの名前が :ref:`ovirt_storage_template_info <ovirt_storage_template_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_storage_vm_facts`` モジュールの名前が :ref:`ovirt_storage_vm_info <ovirt_storage_vm_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_tag_facts`` モジュールの名前が :ref:`ovirt_tag_info <ovirt_tag_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_template_facts`` モジュールの名前が :ref:`ovirt_template_info <ovirt_template_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_user_facts`` モジュールの名前が :ref:`ovirt_user_info <ovirt_user_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_vm_facts`` モジュールの名前が :ref:`ovirt_vm_info <ovirt_vm_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``ovirt_vmpool_facts`` モジュールの名前が :ref:`ovirt_vmpool_info <ovirt_vmpool_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``python_requirements_facts`` モジュールの名前が :ref:`python_requirements_info <python_requirements_info_module>` に変更されました。
* ``rds_instance_facts`` モジュールの名前が :ref:`rds_instance_info <rds_instance_info_module>` に変更されました。
* ``rds_snapshot_facts`` モジュールの名前が :ref:`rds_snapshot_info <rds_snapshot_info_module>` に変更されました。
* ``redfish_facts`` モジュールの名前が :ref:`redfish_info <redfish_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``redshift_facts`` モジュールの名前が :ref:`redshift_info <redshift_info_module>` に変更されました。
* ``route53_facts`` モジュールの名前が :ref:`route53_info <route53_info_module>` に変更されました。
* ``smartos_image_facts`` モジュールの名前が :ref:`smartos_image_info <ali_instance_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``vertica_facts`` モジュールの名前が :ref:`vertica_info <vertica_info_module>` に変更されました。
  このモジュールでは、新しい名前で呼び出されると、``ansible_facts`` が返されなくなります。
  戻り値を使用するには、:ref:`変数 <registered_variables>` を登録します。
* ``vmware_cluster_facts`` モジュールの名前が :ref:`vmware_cluster_info <vmware_cluster_info_module>` に変更されました。
* ``vmware_datastore_facts`` モジュールの名前が :ref:`vmware_datastore_info <vmware_datastore_info_module>` に変更されました。
* ``vmware_guest_facts`` モジュールの名前が :ref:`vmware_guest_info <vmware_guest_info_module>` に変更されました。
* ``vmware_guest_snapshot_facts`` モジュールの名前が :ref:`vmware_guest_snapshot_info <vmware_guest_snapshot_info_module>` に変更されました。
* ``vmware_tag_facts`` モジュールの名前が :ref:`vmware_tag_info <vmware_tag_info_module>` に変更されました。
* ``vmware_vm_facts`` モジュールの名前が :ref:`vmware_vm_info <vmware_vm_info_module>` に変更されました。
* ``xenserver_guest_facts`` モジュールの名前が :ref:`xenserver_guest_info <xenserver_guest_info_module>` に変更されました。
* ``zabbix_group_facts`` モジュールの名前が :ref:`zabbix_group_info <zabbix_group_info_module>` に変更されました。
* ``zabbix_host_facts`` モジュールの名前が :ref:`zabbix_host_info <zabbix_host_info_module>` に変更されました。

モジュール変更に関する注目点
-------------------------

* :ref:`vmware_cluster <vmware_cluster_module>` がリファクタリングされ、メンテナンス/バグ修正が容易になりました。クラスターの構成には、新しい 3 つの特殊なモジュールを使用します。DRS は :ref:`vmware_cluster_drs <vmware_cluster_drs_module>` で設定し、HA は :ref:`vmware_cluster_ha <vmware_cluster_ha_module>` で設定し、vSAN は :ref:`vmware_cluster_vsan <vmware_cluster_vsan_module>` で設定します。
* :ref:`vmware_dvswitch <vmware_dvswitch_module>` は、``folder`` パラメーターを受け入れて dvswitch をユーザー定義のフォルダーに配置します。このオプションには、オプションパラメーター ``datacenter`` があります。
* :ref:`vmware_datastore_cluster <vmware_datastore_cluster_module>` は、``folder`` パラメーターを受け入れてデータストアクラスターをユーザー定義のフォルダーに配置します。このオプションには、オプションパラメーター ``datacenter`` があります。
* :ref:`mysql_db <mysql_db_module>` は、``db`` パラメーターに加えて新しい ``db_list`` パラメーターを返します。この ``db_list`` パラメーターはデータベース名のリストを参照します。``db`` パラメーターはバージョン 2.13 で非推奨になります。
* :ref:`snow_record <snow_record_module>` および :ref:`snow_record_find <snow_record_find_module>` が、``instance`` パラメーター、``username`` パラメーター、および ``password`` パラメーターの環境変数を取得するようになりました。この変更により、これらのパラメーターはオプションとしてマークされます。
* 非推奨となっていた ``win_firewall_rule`` の ``force`` オプションは削除されました。
* :ref:`openssl_certificate <openssl_certificate_module>` の ``ownca`` プロバイダーは、``ownca_create_authority_key_identifier: no`` で明示的に無効にされていない限り、認証局キー識別子を作成します。これが当てはまるのは ``cryptography`` バックエンドの場合のみです (``cryptography`` ライブラリーが使用可能になっているときには、これがデフォルトで選択されています)。
* :ref:`openssl_certificate <openssl_certificate_module>` の ``ownca`` プロバイダーおよび ``selfsigned`` プロバイダーは、それぞれ ``ownca_create_subject_key_identifier: never_create`` および ``selfsigned_create_subject_key_identifier: never_create`` で明示的に無効にされていない限り、サブジェクトキー識別子を作成します。CSR でサブジェクトキー識別子を指定している場合にはその識別子が取得され、指定されていない場合は公開鍵から作成されます。これが当てはまるのは ``cryptography`` バックエンドの場合のみです (``cryptography`` ライブラリーが使用可能になっているときには、これがデフォルトで選択されています)。
* このバージョンでは、:ref:`openssh_keypair <openssh_keypair_module>` は、公開鍵と秘密鍵の両方に、同じファイルパーミッションと所有権を適用するようになりました (両方とも同じ ``mode``、``owner``、``group`` などを取得します)。1 つの鍵のパーミッション/所有権を変更する必要がある場合は、:ref:`file <file_module>` を使用して、作成後に変更を行います。


プラグイン
=======

削除されたルックアッププラグイン
----------------------

* ``redis_kv`` では、代わりに :ref:`redis <redis_lookup>` が使用されます。


カスタムスクリプトのポーティング
======================

主な変更はありません。


ネットワーキング
==========

ネットワークリソースモジュール
------------------------

Ansible 2.9 で、ネットワークリソースモジュールの最初のバッチが導入されました。ネットワークデバイスの構成のセクションは、そのネットワークデバイスが提供するリソースと考えることができます。ネットワークリソースモジュールは、単一のリソースを構成するように意図的にスコープされています。このモジュールをビルディングブロックとして組み合わせることで、複雑なネットワークサービスを構成できます。従来のモジュールは Ansible 2.9 で非推奨となり、Ansible 2.13 で削除される予定です。上記の非推奨になったモジュールのリストに目を通して、Playbook で新しいネットワークリソースモジュールに置き換えてください。詳細は、「`Ansible Network Features in 2.9 <https://www.ansible.com/blog/network-features-coming-soon-in-ansible-engine-2.9>`_」を参照してください。

ネットワークデバイスの ``gather_facts`` サポートの改善
-----------------------------------------------------

Ansible 2.9 では、``gather_facts`` キーワードが、標準化された鍵と値のペアでネットワークデバイスファクトの収集に対応するようになりました。これらのネットワークファクトをさらにタスクに送信して、ネットワークデバイスを管理できます。また、新しい ``gather_network_resources`` パラメーターを、ネットワークの ``*_facts`` モジュール (:ref:`eos_facts <eos_facts_module>` など) とともに使用すると、デバイス設定のサブセットのみを返すことができます。 この例は、:ref:`network_gather_facts` を参照してください。

2.9 で削除された最上位の接続引数
---------------------------------------------

``username``、``host``、``password`` といった最上位の接続引数は、バージョン 2.9 で削除されています。

Ansible 2.4 以前の **引数**

.. code-block:: yaml

    - name: 接続プロパティーの最上位オプションの使用例
      ios_command:
        commands: show version
        host: "{{ inventory_hostname }}"
        username: cisco
        password: cisco
        authorize: yes
        auth_pass: cisco


標準の Ansible 接続プロパティーを使用し、この接続プロパティーをグループごとにインベントリーに設定して、Playbook を接続タイプ ``network_cli`` および ``netconf`` に変更してください。Playbook とインベントリーファイルの更新時に、``become`` を簡単に変更して権限を昇格させることができます (この操作がサポートされているプラットフォームの場合)。詳細は、「:ref:`ネットワークモジュールで become を使用<become_network>`」ガイドおよび :ref:`プラットフォームのドキュメント<platform_options>` を参照してください。
