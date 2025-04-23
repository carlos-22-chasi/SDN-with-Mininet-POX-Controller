#!/usr/bin/env python

# Spring 2024 CSCI 4211: Introduction to Computer Networks
# This program serves as the SDN controller for the Ethernet-based
# self-learning switches. It was written in Python v3.

from pox.core import core
import pox.openflow.libopenflow_01 as of

# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()

# TODO: Define your global data structures here.
network_topology = {}  # Dictionary to store switch_ID, MAC addresses and corresponding switch ports


flood_counter = 0
packets_received = 0

def _handle_PacketIn(event):
  '''
  Handle an OFPacketIn message that a switch has sent to the controller because
  the switch doesn't have a matching rule for the packet it received.
  '''
  global flood_counter
  global packets_received
  packets_received += 1
  log.info('////////////////////////////////////////////////')
  log.info('Number of packets received so far: {}'.format(packets_received))
  log.info('Number of messages flooded by controller so far: {}'.format(flood_counter))

  # Get the port the packet came in on for the switch that's contacting the
  # controller.
  packet_input_port = event.port

  # Get the number of ports attached to the sending switch except for the
  # packet's input port. This variable should be used when updating your
  # global flood counter.
  other_ports = len(event.connection.ports) - 2

  # Use POX to parse the packet.
  packet = event.parsed

  # Get the packet's source and destination MAC addresses.
  src_mac = str(packet.src)
  dst_mac = str(packet.dst)

  # Get the sending switch's ID.
  switch_ID = str(event.connection.dpid) + str(event.connection.ID)

  # This line of code prints infomation about packets that are sent to the
  # controller.
  log.info('Packet has arrived: SRCMAC:{} DSTMAC:{} from switch:{} in-port:{}'.format(src_mac, dst_mac, switch_ID, packet_input_port))

  # TODO: Update the controller's global data structure that stores the
  # information it learns about the network topology to include an entry for
  # the packet's source host and the sending switch's port that can reach it,
  # if such an entry does not already exist.

  #add the source MAC address to the network topology
  if switch_ID not in network_topology:
    network_topology[switch_ID] = {}  #add entry mapping for switch_ID if not there already
  network_topology[switch_ID][src_mac] = packet_input_port  # Store the source MAc and input port for this switch ID


  # TODO: If the network topology already has an entry for the sending switch
  # and the destination host, then install a new match-action rule or rules
  # in the sending switch and have the original packet be fowarded to the
  # correct output port. This is where you should use the code setting
  # message.match that was provided in Section 2.3 of the Phase 3
  # instructions. Note: You will need to implement more code than the single
  # line that is given to you.

  # Part 4 (commented out)
  # if dst_mac in network_topology[switch_ID]:
  #   output_port = network_topology[switch_ID][dst_mac]
  #   log.info('destination mac in entry, output port: {}'.format(output_port))
  #   if(output_port == packet_input_port):
  #     log.info("input and output port match, dropping packet")
  #     return
  #   else:
  #     message = of.ofp_flow_mod()
  #     message.match = of.ofp_match.from_packet(packet, event.port)
  #     message.actions.append(of.ofp_action_output(port=output_port))
  #     message.data = event.ofp
  #     event.connection.send(message)
  #     log.info('Installed rule in switch {} to forward packet to port {}'.format(switch_ID, output_port))
  #   return

  # checks if destination MAC address is in the netowrk topology for the sending switch
  if dst_mac in network_topology[switch_ID]:
    output_port = network_topology[switch_ID][dst_mac]
    # log.info('destination mac in entry, output port: {}'.format(output_port))
    #drop frame if outport port is the same as inport port
    if(output_port == packet_input_port):
      log.info("input and output port match, dropping packet")
      return
    # forward frame on interface indicated by entry
    else:
      #install first flow table
      message = of.ofp_flow_mod()
      message.match = of.ofp_match(dl_src = packet.src, dl_dst = packet.dst)
      message.actions.append(of.ofp_action_output(port=output_port)) #Set the action’s output port to the one that reaches the destination host
      message.data = event.ofp
      event.connection.send(message)

      #install second flow table
      message2 = of.ofp_flow_mod()
      message2.match = of.ofp_match(dl_src = packet.dst, dl_dst = packet.src)
      message2.actions.append(of.ofp_action_output(port=packet_input_port)) #Set the action’s output port to the one that reaches the source host
      message2.data = event.ofp
      event.connection.send(message2)

      log.info('Installed rule in switch {} to forward packet to port {}'.format(switch_ID, output_port))
      log.info('Installed rule in switch {} to forward packet to port {}'.format(switch_ID, packet_input_port))
    return

  # TODO: Otherwise, have the sending switch flood the original packet to
  # every port except for the one the packet came in from originally. No rules
  # should be installed in the switch in this case. Also, don't forget to
  # update your global counter for the number of flooded messages.

  #destination MAC address not found, so flood
  else:
    log.info("No entry for MAC address: flooding packet")
    message = of.ofp_packet_out()
    message.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))  #set the action to every port except from incoming port
    message.data = event.ofp
    event.connection.send(message)
    flood_counter += other_ports
    log.info('Packet flooded to all ports except input port in switch {}'.format(switch_ID))
  return



def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Pair-Learning switch running.")
