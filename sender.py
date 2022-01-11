from machine import Pin, UART
from time import sleep, ticks_ms

# send delay
delay = 1000
last_send = 0

u2 = UART(2, 115200, tx = 4, rx = 36)
rts = Pin(5)
rts.value(1)

while True:
    if ticks_ms() > last_send + delay:
        u2.write("S31090\n")
        last_send = ticks_ms()
