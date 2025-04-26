Overview

This project implements a Software-Defined Networking (SDN) environment using Mininet and a custom POX controller to emulate an Ethernet-based self-learning switch. It demonstrates dynamic packet forwarding, topology learning, and flow rule installation using the OpenFlow protocol. The controller mimics real-world switch behavior by learning MAC address-to-port mappings and managing switch flow tables accordingly.

Features
- POX-Based Controller: Written in Python, the controller reacts to PacketIn events and dynamically updates forwarding rules.

- Self-Learning Switch Logic: Learns and maps MAC addresses to switch ports to reduce unnecessary flooding.

- Flow Rule Installation: Adds, updates, and removes flow entries in real-time based on learned topology.

 - Mininet Integration: Simulates realistic network topologies and host-switch communication.

Code Execution:

When you start your topology (using Python) it will connect to this controller, so run your
controller first in one terminal, and then run the target topology in another terminal. Also,
in the main() function of topology-a.py and topology-b.py, you will need to comment
out and comment in the code lines that have been indicated in the provided TODO
comments so that your controller is used instead of the default controller. However, in
topology-c.py, you don’t need to change the code at all.

Running Your Controller with POX
Copy the ethernet-learning.py file into the /home/mininet/pox/pox/samples directory.
You will then run the controller module using the following commands:

● you@yourmachine:~$ cd pox

● you@yourmachine:~/pox$ ./pox.py samples.ethernet-learning

Note: Do not include the .py file extension when running ethernet-learning.py
