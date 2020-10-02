#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import pyagentx

class IfSwitchPorts(pyagentx.Updater):
    def update(self):
        self.set_INTEGER('1', 0)
        # TODO table

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

if __name__=="__main__":
    main()