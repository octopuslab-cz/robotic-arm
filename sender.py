from machine import Pin, UART
from time import sleep, ticks_ms

# send delay
delay = 1000
last_send = 0

u2 = UART(2, 115200, tx = 4, rx = 36)

i = 0
while True:
    if ticks_ms() > last_send + delay:
        u2.write("Test {}".format(i))
        last_send = ticks_ms()
        i+=1

    char = u2.read()
    if char:
        print(char)

