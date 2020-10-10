# snmp-switch-agent

Implement an agent for snmpd to monitor switches managed using the `swconfig` openwrt utility.
It currently targets only one device.

### Working:
- Monitoring of each port on the switch (up/down, link speed, bytes received, bytes transmitted)

### Future work:
- Add routing and vlan table.

### Support currently targets:

- Atheros AR8337

### Tested on:

- TPLink Archer C7

### Requirements

`pip3 install git+https://github.com/hosthvo/pyagentx@python3`

### Notes

This should become useless whenever openwrt will support these switches using DSA (Distributed Switch Architecture)
