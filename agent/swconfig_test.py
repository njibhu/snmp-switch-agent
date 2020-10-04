#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import swconfig


class TestSwconfigModule(unittest.TestCase):

    @patch('swconfig.call_port_map')
    def test_get_port_number(self, mock_call):
        with open("agent/__mocks__/call_port_map.txt", "r") as mock_file:
            mock_call.return_value = "\n".join(mock_file.readlines())
        self.assertEqual(swconfig.get_port_number(), 7)

    @patch('swconfig.call_port_detail')
    def test_get_port_detail(self, mock_call):
        with open("agent/__mocks__/call_port_detail.txt", "r") as mock_file:
            mock_call.return_value = "\n".join(mock_file.readlines())
        port_detail = swconfig.get_port_detail(0)
        self.assertEqual(port_detail["index"], "0")
        self.assertEqual(port_detail["mib"],
                         "MIB counters\nRxGoodByte  : 1798572445 (1.6 GiB)\nTxByte      : 28744747498 (26.7 GiB)")
        self.assertEqual(
            port_detail["link"], "port:0 link:up speed:1000baseT full-duplex txflow rxflow")

    def test_parse_mib_string(self):
        mib_string = "MIB counters\nRxGoodByte  : 1798572445 (1.6 GiB)\nTxByte      : 28744747498 (26.7 GiB)"
        self.assertEqual(swconfig.parse_mib_string(mib_string),
                         {'RxGoodByte': 1798572445, 'TxByte': 28744747498,
                             'description': 'MIB counters'}
                         )

    def test_parse_link(self):
        link_string = "port:0 link:up speed:1000baseT full-duplex txflow rxflow"
        self.assertEqual(swconfig.parse_link(link_string),
                         {'full-duplex': True,
                          'link': 'up',
                          'port': 0,
                          'rxflow': True,
                          'speed': '1000baseT',
                          'txflow': True})

    def test_parse_port(self):
        port_detail = {'index': '0', 'mib': 'MIB counters\nRxGoodByte  : 1798572445 (1.6 GiB)\nTxByte      : 28744747498 (26.7 GiB)', 'enable_eee': '???',
                       'igmp_snooping': '0', 'vlan_prio': '0', 'pvid': '0', 'link': 'port:0 link:up speed:1000baseT full-duplex txflow rxflow'}
        parsed_port = swconfig.parse_port(port_detail)
        self.assertEqual(parsed_port["index"], 0)
        self.assertEqual(parsed_port["enable_eee"], None)
        self.assertEqual(parsed_port["igmp_snooping"], 0)
        self.assertEqual(parsed_port["vlan_prio"], 0)
        self.assertEqual(parsed_port["pvid"], 0)
        self.assertEqual(parsed_port["mib"], {
            "description": "MIB counters",
            "RxGoodByte": 1798572445,
            "TxByte": 28744747498
        })
        self.assertEqual(parsed_port["link"], {
            "port": 0,
            "link": "up",
            "speed": "1000baseT",
            "full-duplex": True,
            "txflow": True,
            "rxflow": True
        })

    @patch('swconfig.call_port_detail')
    def test_get_port_detail_none(self, mock_call):
        with open("agent/__mocks__/call_port_detail_none.txt", "r") as mock_file:
            mock_call.return_value = "\n".join(mock_file.readlines())
        port_detail = swconfig.get_port_detail(0)
        self.assertEqual(port_detail, {'enable_eee': '???',
                                       'igmp_snooping': '???',
                                       'index': '7',
                                       'link': '???',
                                       'mib': '???',
                                       'pvid': '???',
                                       'vlan_prio': '???'})

    @patch('swconfig.call_port_detail')
    def test_parse_port_none(self, mock_call):
        with open("agent/__mocks__/call_port_detail_none.txt", "r") as mock_file:
            mock_call.return_value = "\n".join(mock_file.readlines())
        port_detail = swconfig.get_port_detail(0)
        self.assertEqual(swconfig.parse_port(port_detail), {'enable_eee': None,
                                                            'igmp_snooping': None,
                                                            'index': 7,
                                                            'link': None,
                                                            'mib': None,
                                                            'pvid': None,
                                                            'vlan_prio': None})

    @patch('swconfig.call_port_detail')
    def test_get_port_detail_down(self, mock_call):
        with open("agent/__mocks__/call_port_detail_down.txt", "r") as mock_file:
            mock_call.return_value = "\n".join(mock_file.readlines())
        port_detail = swconfig.get_port_detail(1)
        self.assertEqual(port_detail, {'enable_eee': '???',
                                       'igmp_snooping': '0',
                                       'index': '1',
                                       'link': 'port:1 link:down',
                                       'mib': 'No MIB data',
                                       'pvid': '0',
                                       'vlan_prio': '0'})

    @patch('swconfig.call_port_detail')
    def test_parse_port_down(self, mock_call):
        with open("agent/__mocks__/call_port_detail_down.txt", "r") as mock_file:
            mock_call.return_value = "\n".join(mock_file.readlines())
        port_detail = swconfig.get_port_detail(1)
        self.assertEqual(swconfig.parse_port(port_detail), {'enable_eee': None,
                                                            'igmp_snooping': 0,
                                                            'index': 1,
                                                            'link': {'link': 'down', 'port': 1},
                                                            'mib': {'description': 'No MIB data'},
                                                            'pvid': 0,
                                                            'vlan_prio': 0})


if __name__ == '__main__':
    unittest.main()
