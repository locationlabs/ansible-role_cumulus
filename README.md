# cumulus

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
