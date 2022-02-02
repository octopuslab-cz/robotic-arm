# Robotic-arm | serial sender test
# octopusLAB 2018-22

from machine import Pin, UART
from time import sleep_ms

ARM_ID = 2

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

loop = 0

while True:
    print(loop)
    for r in range(sweep_from, sweep_to, sweep_step):
        send_servo(u2, ARM_ID, 1, r)
        send_servo(u2, ARM_ID, 3, r//2)
        sleep_ms(sweep_delay)

    send_servo(u2, ARM_ID, 6, 70)
    sleep_ms(2000)
    send_servo(u2, ARM_ID, 6, 130)

    for r in range(sweep_to, sweep_from, -sweep_step):
        send_servo(u2, ARM_ID, 1, r)
        send_servo(u2, ARM_ID, 3, r//2)
        sleep_ms(sweep_delay)

    send_servo(u2, ARM_ID, 6, 70)
    sleep_ms(500)
    send_servo(u2, ARM_ID, 6, 130)
    loop += 1

