.. _platform_options:

****************
プラットフォームのオプション
****************

一部の Ansible Network プラットフォームは、複数の接続タイプ、権限昇格 (``enable`` モード)、またはその他のオプションに対応します。本セクションのページでは、各ネットワークプラットフォームで利用可能なオプションを理解する標準ガイドが紹介されています。コミュニティーが管理するプラットフォームから、このセクションへの貢献を歓迎いたします。

.. toctree::
   :maxdepth: 2
   :caption: プラットフォームのオプション

   platform_cnos
   platform_dellos6
   platform_dellos9
   platform_dellos10
   platform_enos
   platform_eos
   platform_eric_eccli
   platform_exos
   platform_icx
   platform_ios
   platform_iosxr
   platform_ironware
   platform_junos
   platform_meraki
   platform_netvisor
   platform_nos
   platform_nxos
   platform_routeros
   platform_slxos
   platform_voss
   platform_vyos
   platform_netconf_enabled

.. _settings_by_platform:

プラットフォーム別の設定
================================

.. raw:: html

    <style>
    /* この 1 つの表に関するスタイル。 ヘッダー列の間に区切り文字を追加します。 */
    table#network-platform-table thead tr th.head {
  border-left-width: 1px;
  border-left-color: rgb(225, 228, 229);
  border-left-style: solid;
}
</style>

.. table::
    :name: network-platform-table

    ===============================  =======================  ===========  =======  =======  ===========
    ..                                                        ``ansible_connection:`` settings available
    --------------------------------------------------------  ------------------------------------------
    Network OS                       ``ansible_network_os:``  network_cli  netconf  httpapi  local
    ===============================  =======================  ===========  =======  =======  ===========
    Arista EOS `[†]`_                ``eos``                  ✓                     ✓        ✓
    Cisco ASA                        ``asa``                  ✓                              ✓
    Cisco IOS `[†]`_                 ``ios``                  ✓                              ✓
    Cisco IOS XR `[†]`_              ``iosxr``                ✓                              ✓
    Cisco NX-OS `[†]`_               ``nxos``                 ✓                     ✓        ✓
    Dell OS6                         ``dellos6``              ✓                              ✓
    Dell OS9                         ``dellos9``              ✓                              ✓
    Dell OS10                        ``dellos10``             ✓                              ✓
    Ericsson ECCLI                   ``eric_eccli``           ✓                              ✓
    Extreme EXOS                     ``exos``                 ✓                     ✓
    Extreme IronWare                 ``ironware``             ✓                              ✓
    Extreme NOS                      ``nos``                  ✓
    Extreme SLX-OS                   ``slxos``                ✓
    Extreme VOSS                     ``voss``                 ✓
    F5 BIG-IP                                                                                ✓
    F5 BIG-IQ                                                                                ✓
    Junos OS `[†]`_                  ``junos``                ✓            ✓                 ✓
    Lenovo CNOS                      ``cnos``                 ✓                              ✓
    Lenovo ENOS                      ``enos``                 ✓                              ✓
    Meraki                           ``meraki``                                              ✓
    MikroTik RouterOS                ``routeros``             ✓
    Nokia SR OS                      ``sros``                 ✓                              ✓
    Pluribus Netvisor                ``netvisor``             ✓
    Ruckus ICX `[†]`_                ``icx``                  ✓
    VyOS `[†]`_                      ``vyos``                 ✓                              ✓
    Netconf に対応する OS `[†]`_  ``<network-os>``                      ✓                 ✓
    ===============================  =======================  ===========  =======  =======  ===========

.. _`[†]`:

**[†]** Ansible Network Team が管理しています。
