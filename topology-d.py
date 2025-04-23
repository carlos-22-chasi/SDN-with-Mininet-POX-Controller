#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as a script that constructs topology D.
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

        # TODO: Define all of the hosts with subnets.
        
        
        # TODO: Define the IP router.
        

        # TODO: Add links between the hosts and router.
        


if __name__ == '__main__':
    setLogLevel( 'info' )

    topo = AssignmentNetworks()
    # TODO: You can comment in the following code line if you wish to test the
    # construction of your topology without having the controller implemented.
    # You will need to also comment out the subsequent code line.
    #net = Mininet(topo = topo, link = TCLink, autoSetMacs = True, autoStaticArp = True)
    net = Mininet(controller = RemoteController, topo = topo, link = TCLink, autoSetMacs = True, autoStaticArp = True)

    # Run network
    net.start()
    CLI( net )
    net.stop()