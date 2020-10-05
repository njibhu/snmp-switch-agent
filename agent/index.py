#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyagentx
import swconfig
import re


class IfSwitchPorts(pyagentx.Updater):
    def update(self):
        amount = swconfig.get_port_number()
        self.set_INTEGER('1', amount)
        for port_index in range(amount):
            port_detail = swconfig.get_port_detail(port_index)
            parsed_port_detail = swconfig.parse_port(port_detail)
            self.set_INTEGER('2.' + str(port_index) + '.1', port_index)
            port_up = 1 if parsed_port_detail["link"]["link"] == 'up' else 2
            self.set_INTEGER('2.' + str(port_index) + '.2', port_up)
            port_speed = 0
            if "speed" in parsed_port_detail["link"]:
                match_number = re.match(r"\d*", parsed_port_detail["link"]["speed"])
                port_speed = int(match_number.group())
            self.set_GAUGE32('2.' + str(port_index) + '.3', port_speed)
            rx_good_bytes = 0
            if "RxGoodByte" in parsed_port_detail["mib"]:
                rx_good_bytes = parsed_port_detail["mib"]["RxGoodByte"]
            self.set_COUNTER64('2.' + str(port_index) + '.4', int(rx_good_bytes))
            tx_bytes = 0
            if "TxByte" in parsed_port_detail["mib"]:
                tx_bytes = parsed_port_detail["mib"]["TxByte"]
            self.set_COUNTER64('2.' + str(port_index) + '.5', int(tx_bytes))


class MyAgent(pyagentx.Agent):
    def setup(self):
        self.register('1.3.6.1.4.1.999.1', IfSwitchPorts)


def main():
    pyagentx.setup_logging()
    try:
        agent = MyAgent()
        agent.start()
    except Exception as e:
        print("Unhandled exception:", e)
        agent.stop()
    except KeyboardInterrupt:
        agent.stop()


if __name__ == "__main__":
    main()
