#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import re

switch_id = "switch0"
indent = "\t"


def call_port_map():
    return subprocess.getoutput("/sbin/swconfig dev {} portmap".format(switch_id))


def call_port_detail(port_index):
    return subprocess.getoutput(
        "/sbin/swconfig dev {} port {} show".format(switch_id, port_index)
    )


def get_port_number():
    output = call_port_map()
    port_amount = 0
    for line in output.splitlines():
        if line.startswith("port"):
            port_amount += 1

    return port_amount


def get_port_detail(port_index):
    output = call_port_detail(port_index)
    port_detail = {}
    multiline = {
        "active": False,
        "buffer": "",
        "name": ""
    }
    for line_number, line in enumerate(output.split('\n')):
        if line_number == 0:
            port_detail["index"] = re.match(r"Port (\d*):", line).group(1)
            continue

        if multiline["active"]:
            if line == "":
                multiline["active"] = False
                port_detail[multiline["name"]] = multiline["buffer"]
            else:
                multiline["buffer"] += "\n" + line
            continue

        if line.startswith(indent) == False and line != "":
            multiline["active"] = True
            multiline["buffer"] += "\n" + line
        elif line.startswith(indent) == True:
            name, value = line.strip().split(": ", 1)
            multiline["name"] = name
            multiline["buffer"] = value
            port_detail[name] = value
        else:
            continue

    return port_detail


def parse_mib_string(input):
    mib_dict = {}
    for line_number, line in enumerate(input.splitlines()):
        if line_number == 0:
            mib_dict["description"] = line
            continue
        if line.find(":") > -1:
            name, value = line.split(":", 1)
            match_size = re.match(r"(\d*) \(.*\)", value.strip())
            if match_size:
                mib_dict[name.strip()] = int(match_size.group(1))
            else:
                mib_dict[name.strip()] = value.strip()

    return mib_dict


def parse_link(input):
    link_dict = {}
    for value in input.split(" "):
        if value.find(":") > -1:
            key, sub_value = value.split(":", 1)
            if sub_value.strip() == "???":
                link_dict[key.strip()] = None
            else:
                link_dict[key.strip()] = to_int(sub_value.strip())
        else:
            link_dict[value.strip()] = True
    return link_dict


def parse_port(dict_input):
    port_dict = {}
    for key, value in dict_input.items():
        if value == "???":
            port_dict[key] = None
        elif key == "mib":
            port_dict[key] = parse_mib_string(value)
        elif key == "link":
            port_dict[key] = parse_link(value)
        else:
            port_dict[key] = to_int(value)
    return port_dict


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return s
