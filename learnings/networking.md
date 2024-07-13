# Networking

- Network layer:
  - IP addressing
    - IP address is a logical address which acts as a partion for broader network. These partitions are called subnet. There are many uses of subnet including access control and security.
    - In the IP header there is a segment called "Quality of Service". This can be used to prioritize network trafic.
    - IPv4 address
      - 4 octet (each 8 bits long, thus octet)
    - in wndows use `ipconfig`, in linux use 'ifconfig'. Additionaly in linux use `ip route` to get the default gateway which is the router.
  - IP trafic type
    - Unicast: These trafic goes to a single destination host
    - broadcast: These trafic goes to all hosts in a subnet. Router doesn't forward broadcast traffic.
    - multicast: These trafic goes to multiple interested host in a subnet
- Trafic
  - If the destination is in the same sub-net, the trafic can go directly
  - If the destination is in different sub-net, it needs to go through a router
