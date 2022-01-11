from machine import Pin, UART
from time import sleep_ms

u2 = UART(2, 115200, tx = 4, rx = 36)
rts = Pin(5)
rts.value(1)

def rjust(instr, num, char):
    if len(instr) >= num:
        return instr

    return "{}{}".format(char*(num-len(instr)), instr)


def send_servo(uart, address, servo, degree):
    data = "S{}{}{}\n".format(address, rjust(str(servo), 2, '0'), rjust(str(degree), 3, '0'))
    uart.write(data)


sweep_from = 20
sweep_to = 130
sweep_step = 3
sweep_delay = 30

while True:
    for r in range(sweep_from, sweep_to, sweep_step):
        send_servo(u2, 3, 1, r)
        send_servo(u2, 3, 3, r//2)
        sleep_ms(sweep_delay)

    for r in range(sweep_to, sweep_from, -sweep_step):
        send_servo(u2, 3, 1, r)
        send_servo(u2, 3, 3, r//2)
        sleep_ms(sweep_delay)
