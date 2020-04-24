.. \_platform\_options:

****************
プラットフォームのオプション
****************

一部の Ansible Network プラットフォームは、複数の接続タイプ、権限昇格 (``enable`` モード)、またはその他のオプションに対応します。本セクションのページでは、各ネットワークプラットフォームで利用可能なオプションを理解する標準ガイドが紹介されています。コミュニティーが管理するプラットフォームから、このセクションへの貢献を歓迎いたします。

.. toctree::
   :maxdepth: 2
   :caption: プラットフォームのオプション

   platform\_cnos
   platform\_dellos6
   platform\_dellos9
   platform\_dellos10
   platform\_enos
   platform\_eos
   platform\_eric\_eccli
   platform\_exos
   platform\_icx
   platform\_ios
   platform\_iosxr
   platform\_ironware
   platform\_junos
   platform\_meraki
   platform\_netvisor
   platform\_nos
   platform\_nxos
   platform\_routeros
   platform\_slxos
   platform\_voss
   platform\_vyos
   platform\_netconf\_enabled

.. \_settings\_by\_platform:

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

.. \_`[†]`:

**\[†]** Ansible Network Team が管理しています。
