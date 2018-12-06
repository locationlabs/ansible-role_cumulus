# cumulus

## NTP

`cumulus_ntp_servers`: List of ntp servers to use - Default: Cumulus ntp servers
`cumulus_ntp_interface`: Interface to listen on for ntp - Default eth0

## Port Policies

It may be desirable to set a default switch-wide port configuration, such as MTU. This is simply yaml to json.

Example:

```yaml
config:
  port_policy:
    address:
      defaults:
        mtu: 9216
```

For more information, see [Setting a Policy for Global System MTU](https://docs.cumulusnetworks.com/display/DOCS/Layer+1+and+Switch+Port+Attributes#Layer1andSwitchPortAttributes-SettingaPolicyforGlobalSystemMTU)

## 802.1X Port Authentication

**NOTE:** Changing 802.1X settings or port attributes will restart the hostapd daemon, which resets existing authorized sessions

Currently only a single RAIDUS server is supported

Authentication server configuration options:

```yaml
config:
  dot1x:
    server_ip: 'x.x.x.x' # RADIUS server - Required
    authentication_port: 1812 # Default
    shared_secret: 'xxxx' # RADIUS shared secret - Required
    accounting_port: 1813 # Default
    client_source_ip: 'y.y.y.y' # Optional
    mab_activation_delay: 30 # Default - Cumulus only supports a value between 5 and 30
    eap_reauth_period: 0 # Default
    parking_vlan_id: 0000 # Optional
    # To enable dynamic vlan support
    dynamic_vlan:
    # To require dynamic vlan assignment
    # dynamic_vlan: required
```

To enable 802.1X auth on a port, add ONLY one of the following options to the port configuration:

```yaml
config:
  swp1:
    dot1x: # Enable 802.1X
    # dot1x-mab: # Enable MAC address auth bypass
    # dot1x-parking: # Enable parking vlan assignment for failed auth case
```

For more information, see [802.1X Interfaces](https://docs.cumulusnetworks.com/display/DOCS/802.1X+Interfaces)


## ACLs

**NOTE:** Changing these settings will cause `switchd` to restart, which will stop network traffic

**NOTE:** Depending on atomic mode, updating ACLs may interrupt network traffic

* `cumulus_acl_non_atomic_update_mode`: Boolean - control non atomic update mode

Configure ACL rules with the `acl` hash in `config`. Each rule set is written to it's own file,
taking the key as the filename. The digits are important as they are used to control the order that
the rules are loaded. **00** and **99** are reserved by Cumulus.

Example:

```yaml
config:
  acl:
    10_some_rules:
      variables:
        - INGRESS = swp+
        - INPUT_PORT_CHAIN = INPUT,FORWARD
      iptables:
        - -A $INPUT_PORT_CHAIN --in-interface $INGRESS -p tcp --dport 80 -j ACCEPT
      ip6tables:
        - -A $INPUT_PORT_CHAIN --in-interface $INGRESS -p tcp --dport 80 -j ACCEPT
      ebtables:
        - -A INPUT -p IPv4 -j ACCEPT
    20_more_rules:
      ...
```

For more information, See [Netfilter - ACLs](https://docs.cumulusnetworks.com/display/DOCS/Netfilter+-+ACLs)

_Inspired by [mikegleasonjr/ansible-role-firewall](https://github.com/mikegleasonjr/ansible-role-firewall)_

## DOS Protection

**NOTE:** Changing these settings will cause `switchd` to restart, which will stop network traffic.

Cumulus has hardware level DOS protection that is disabled by default. To enable, set `cumulus_dos_enable` to true.

* `cumulus_dos_enable`: Boolean - Set to true to enable DOS protection with the config values from
`defaults/main.yml`
* `cumulus_datapath_conf`: See `defaults/main.yml`, controls the various DOS options.
* `cumulus_datapath_conf_file`: Defaults to the location of the Broadcom config file.

For more information, See [Configuring Hardware-enabled DDOS Protection](https://docs.cumulusnetworks.com/display/DOCS/Configuring+Hardware-enabled+DDOS+Protection) for more information.

## Breakout ports

**NOTE:** Changing these settings will cause `switchd` to restart, which will stop network traffic.

**NOTE:** Beware, removing port from `config.ports` will result in leaving the previous config behind.

100G switches allow you to breakout ports to 4x10G, 4x25G, etc with use of a breakout cable (or use
a different speed than 100G). For example, this will take `swp1` and make `swp1sN`, where N is 0 to
4 or 2, depending on which breakout type configured.

As of this writing, the options available to the Z9100 switch is:
* 4x10G
* 4x25G
* 2x50G
* 40G
* 50G
* 100G
* disabled

Example:

```yaml
config:
  ports:
    1: 4x10G
    2: 4x10G
```

For more information, read [Configuring Breakout Ports](https://docs.cumulusnetworks.com/display/DOCS/Layer+1+and+Switch+Port+Attributes#Layer1andSwitchPortAttributes-breakoutConfiguringBreakoutPorts)

## Administratively Down Interfaces

There may be a need to administratively shutdown interfaces.  This can be accomplished by using down key with a value of yes.

Example:

```yaml
config:
  interfaces:
    swp1:
      link:
        down: yes
```

## Dropping Untagged Frames

On trunk ports by default untagged frames are placed into the native VLAN.  The default native VLAN
is VLAN ID 1.  If there is a desire to prevent untagged frames from being allowed in/out of an
interface you can use `bridge_allow_untagged`.  The behavior changes and any untagged frames will be dropped.

```yaml
config:
  interfaces:
    swp1:
      bridge_allow_untagged: 'no'
```
