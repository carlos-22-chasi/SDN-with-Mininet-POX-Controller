#!/usr/bin/env python

# Do NOT modify this file beyond commenting out line 65 and commenting in 
# line 68 in Phase 3.

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as as a script that constructs topology A.
# It was written in Python v3.

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import RemoteController

class AssignmentNetworks(Topo):
    def __init__(self, **opts):
        Topo.__init__(self, **opts)

	    # Define all of the hosts.
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')

	    # Define the switch.
        s1 = self.addSwitch('s1')

	    # Add links between each host and the switches.
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        

if (__name__ == '__main__'):
    setLogLevel( 'info' )
        
    # Create data network.
    topo = AssignmentNetworks()
    net = Mininet(controller = RemoteController, topo = topo, link = TCLink, autoSetMacs = True, autoStaticArp = True)

    # Run the network.
    net.start()
    CLI( net )
    net.stop()