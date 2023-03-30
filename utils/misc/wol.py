







'''import sys, struct, socket
from wakeonlan import create_magic_packet, send_magic_packet

known_computers = {
    'MyComputer': 'A8:A1:59:25:B8:6A'
}


def wake_on_lan(ethernet_address):
    broadcast = [[f'192.168.{i}.{j}' for j in range(256)] for i in range(256)]
    #broadcast = ['192.168.255.255']
    wol_port = 9

    # Construct 6 byte hardware address
    add_oct = ethernet_address.split(':')
    hwa = struct.pack('BBBBBB', int(add_oct[0], 16),
                      int(add_oct[1], 16),
                      int(add_oct[2], 16),
                      int(add_oct[3], 16),
                      int(add_oct[4], 16),
                      int(add_oct[5], 16))

    # Build magic packet

    msg = b'\xff' * 6 + hwa * 16
    print(msg)
    print(create_magic_packet(ethernet_address))
    # send_magic_packet(ethernet_address)

    # Send packet to broadcast address using UDP port 9

    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    for i in broadcast:
        for j in i:
            soc.sendto(msg, (j, wol_port))
    soc.close()


def wol(computers: dict) -> None:
    for name, value in computers.items():
        wake_on_lan(value)


wol(known_computers)
'''