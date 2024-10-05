import meshtastic
import time
import meshtastic.serial_interface
from pubsub import pub



interface = meshtastic.serial_interface.SerialInterface()

def on_receive(packet):

    fromId = packet.get('fromId')
    message = packet.get('decoded', '')
    portnum = message.get('portnum')

    if portnum == 'TEXT_MESSAGE_APP':

        print('--------------------------------------------------------')
        print(packet)
        print('--------------------------------------------------------')

        response = message.get("text")
        if response.lower().startswith('ping'):
            response = 'pong'

        interface.sendText(response, fromId, wantAck=False)

        print(f"Received '{message}', responding with {response}")

pub.subscribe(on_receive, "meshtastic.receive")



#
# Main Loop
#

try:

    ourNode = interface.getNode('^local')
    print(f'Our node preferences:{ourNode.localConfig}')
    print("Listening for 'ping'... Press Ctrl+C to stop.")

    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting the script")

interface.close()
