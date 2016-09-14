# Source Server Query
# Command-line tool by Giggybyte for LGSM
# Shoutouts to Mom

# Imports
import socket # Sending and receiving UDP packets
import re     # Regex
import sys    # Argument parsing

# Packets
A2S_INFO = b"\xFF\xFF\xFF\xFF\x54\x53\x6F\x75\x72\x63\x65\x20\x45\x6E\x67\x69\x6E\x65\x20\x51\x75\x65\x72\x79\x00"
A2S_CHALL = b"\xFF\xFF\xFF\xFF\x55\xFF\xFF\xFF\xFF"
A2S_CHALL_PREFIX = b"\xFF\xFF\xFF\xFF\x55"

# Methods. The querying happens here.
def infoQuery(ip, port):                                    # Used for grabbing the server title and mapname
    port = int(port)                                        # Converts the port argument to an integer
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Open the socket
    sock.sendto(A2S_INFO, (ip, port))                       # Send A2S_INFO
    recv, server = sock.recvfrom(1024)                      # Receive reply
    recv = recv[6:]                                         # Remove header
    recv = recv.split(b"\x00")                              # Split by 0x00
    return recv                                             # Return the new array

def playerQuery(ip, port):                                  # Used for grabbing the list of players
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Open the socket
    sock.sendto(A2S_CHALL, (ip, port))                      # Send challenge request
    recv, server = sock.recvfrom(1024)                      # Receive challenge reply
    recv = recv[-4:]                                        # Grab last four bytes of reply (this is the challenge number we need)
    sock.sendto(A2S_CHALL_PREFIX+recv, (ip, port))          # Send new challenge packet, with challenge number obtained earlier
    recv, server = sock.recvfrom(1024)                      # Get the reply (a list of players)
    recv = recv[7:]                                         # Remove header
    recv = re.sub(b"\x00+", b"\x00", recv)                  # Remove extra 0x00's
    recv = re.sub(b"[^a-zA-Z0-9\\s\x00]", b"", recv)        # Remove anything non-alphanumeric, non-whitespace, non-0x00
    recv = recv.split(b"\x00")                              # Split by 0x00
    recv = [item for item in recv if len(item) > 2]         # Allows items only if at least 3 bytes long (helps remove junk data)
    return recv                                             # Return array of players

# Parsing the arguments given by the command line. 
if len(sys.argv) == 3: # If we're given IP and port (== 3 because the filename is considered the first arg)
    print("")                                                # Blank line
    print("[*] Querying " + sys.argv[1] + ":" + sys.argv[2]) # Letting you know the server you just typed...
    recv = infoQuery(sys.argv[1], sys.argv[2])               # Run the args through the infoQuery function
    result = []                                              # Prepare a blank list
    for r in recv:                                           # Converts the items from bytes to a string
        if len(r) > 1:                                       # while also getting rid of blank items
            result.append(r.decode("cp437"))
    print("[*]     Name: " + result[0])                      # Printing...
    print("[*]      Map: " + result[1])                      # Printing...
    print("[*] Gamemode: " + result[3])                      # Printing...
    print("[*]     Game: " + result[2])                      # Printing... (hey mom)
    recv = playerQuery(sys.argv[1], int(sys.argv[2]))        # Run the args through the playerQuery function
    print("[*]  Players: " + str(len(recv)))
    print("")
elif len(sys.argv) == 2:
    print("")
    print("[*] Port not given, assuming 27015...")                                             
    print("[*] Querying " + sys.argv[1] + ":" + "27015") 
    recv = infoQuery(sys.argv[1], 27015) 
    result = [] 
    for r in recv: 
        if len(r) > 1: 
            result.append(r.decode("cp437"))
    print("[*]     Name: " + result[0]) 
    print("[*]      Map: " + result[1]) 
    print("[*] Gamemode: " + result[3]) 
    print("[*]     Game: " + result[2]) 
    recv = playerQuery(sys.argv[1], 27015) 
    print("[*]  Players: " + str(len(recv)))
    print("")
else:
    print("")
    print("Source Server Query (SSQ) by giggybyte for LGSM")
    print("  Usage: ssq.py <ip> <port>")
    print("Example: ssq.py tf2.gameserver.com 27015")
    print("If no port is given, 27015 is assumed")
    print("")