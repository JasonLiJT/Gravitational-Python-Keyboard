from microbit import *
import radio

radio.on()
radio.config(channel=16)

while True:
    incoming = radio.receive()
    if incoming:
        if incoming[0] == '$':
            # Scroll output
            display.scroll(incoming[1:])
        else:
            # Sync keyboard display
            display.show(incoming)
