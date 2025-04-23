#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the SDN controller for the IP-based
# self-learning switches. It was written in Python v3.

from pox.core import core
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.packet.ethernet import ethernet
from pox.lib.packet.arp import arp
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.icmp import *
from pox.lib.packet import *
from pox.lib.packet.ipv4 import ipv4

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# TODO: Define your global data structures here.


# TODO: Define any helper functions you decide are useful here.



def _handle_PacketIn(event):
  '''
  Handle an OFPacketIn message that a switch has sent to the controller because
  the router doesn't have a matching rule for the packet it received.
  '''

  # Get the port the packet came in on for the switch that's contacting the 
  # controller.
  packet_input_port = event.port

  # Get the number of ports attached to the sending switch. This variable should
  # be used when updating your global flood counter.
  all_ports = event.connection.ports
  other_ports = len(event.connection.ports) - 2

  # Use POX to parse the packet.
  packet = event.parsed

  # Get the packet's source and destination MAC addresses.
  src_mac = str(packet.src)
  dst_mac = str(packet.dst)

  # Get the sending switch's ID.
  switch_ID = str(event.connection.dpid) + str(event.connection.ID)
  
  log.info('Packet has arrived: SRCMAC:{} DSTMAC:{} from switch:{} in-port:{}'.format(src_mac, dst_mac, switch_ID, packet_input_port))
  
  # TODO: Check the type of packet (if it's an ARP request, Ping (ICMP) packet, 
  # or IPv4 packet) and handle the packet accordingly based on its type.
  
  

def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Pair-Learning switch running.")