# cumulus

## DOS Protection

**NOTE:** Changing these settings will cause `switchd` to restart, which will stop network traffic.

Cumulus has hardware level DOS protection that is disabled by default. To enable, set `cumulus_dos_enable` to true.

* `cumulus_dos_enable`: Boolean - Set to true to enable DOS protection with the config values from
`defaults/main.yml`
* `cumulus_datapath_conf`: See `defaults/main.yml`, controls the various DOS options.
* `cumulus_datapath_conf_file`: Defaults to the location of the Broadcom config file.

For more information, See [Configuring Hardware-enabled DDOS Protection](https://docs.cumulusnetworks.com/display/DOCS/Configuring+Hardware-enabled+DDOS+Protection) for more information.
