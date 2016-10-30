from microbit import *
from math import *
import radio

radio.on()
radio.config(channel=16)
alpha = '[abcdef ghijkl]'
bet = '<Smnopqrstuvwxyz>'  # alphabet
num = ':01234567890.'
operators = 'D,()+-*/="RI'
p = print
d = display.scroll  # make typing easier


def get_char():
    while True:
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        if x == 0:
            theta = 90  # avoid division by zero
        else:
            theta = atan(z / x) * 180 / pi
        if theta < 0:
            theta = 180 + theta
        # map theta to characters on semisphere (in degrees) using calibrated formulae
        if y < -300:
            i = num[min(int(abs(theta - 30) / 120 * len(num)), len(num) - 1)]
        elif y > 700:
            i = operators[
                min(int(abs(theta - 30) / 120 * len(operators)), len(operators) - 1)]
        elif y > 300:
            i = bet[int(theta / 180 * len(bet))]
        else:
            i = alpha[int(theta / 180 * len(alpha))]
        display.show(i)
        radio.send(i)
        if button_b.was_pressed():  # b for execution
            return False
        if button_a.was_pressed():  # a for typing
            display.clear()
            radio.send(' ')
            while button_a.is_pressed():
                pass  # feedback: nothing displayed with a pressed
            display.show(i)
            radio.send(i)
            sleep(500)
            break
        sleep(50)
    return i


def code():
    s = ''
    c = get_char()
    caps_lock = False
    while c:
        if c == 'D':
            # delete
            s = s[:-1]
        elif c == 'S':
            caps_lock = True
        elif caps_lock:
            s += c.upper()
            caps_lock = False
        elif c == 'I':
            # indentation
            s += '    '
        elif c == ' ':
            if s[-1] == ' ':
                # type two spaces for a new line
                s = s[:-1]
                s += '\n'
            else:
                s += ' '
        elif c == 'R':
            s += 'return '
        else:
            s += c
        print('...', s)
        c = get_char()
    try:
        if s[-1] == ' ':
            exec(s)
        else:
            exec("result = " + s)
            exec("print('>>>', result)")
            exec("radio.send(str(result))")
            exec("display.scroll(str(result))")
    except:
        eval("print('error')")
        exec("radio.send('error')")
        eval("display.scroll('error', wait=False, loop=True)")


idle = """\n\nPython 3.5.2 (v3.5.2:4def2a2901a5, Jun 26 2016, 10:47:25)
 [GCC 4.2.1 (Jason Li build 5666) (dot 3)] on BBC micro:bit\n>>> """
print(idle)
while True:
    code()

# for display
'''
from microbit import *
import radio

radio.on()
radio.config(channel=16)

while True:
    incoming = radio.receive()
    if incoming:
        display.show(incoming)
'''