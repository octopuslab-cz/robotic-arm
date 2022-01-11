from machine import Pin, UART
from time import sleep_ms


class ServoRead():
    def __init__(self, uart, address = 0):
        self._uart = uart
        self._addr = address
        self._servo_events = []
        self._data = ""


    def _on_servo_event(self, servo, degree):
        for f in self._servo_events:
            f(servo, degree)


    def _read(self):
        if not self._uart.any():
            return

        char = self._uart.read(1)

        if char == b'S':
            self._data = ""

        if char == b'\n':
            self._parse()

        self._data += char.decode()


    def _parse(self):
        if not self._data:
            return

        if len(self._data) != 6:
            print("Unknown or malformed data: {}".format(self._data))
            return

        try:
            address = int(self._data[1:2])
            servo = int(self._data[2:3])
            degree = int(self._data[3:6])
        except ValueError as e:
            print("Protocol value error! {}".format(e))
            raise e


        if address not in [0, self._addr]:
            return


        self._on_servo_event(servo, degree)


    def add_servo_event(self, func):
        if func in self._servo_events:
            return

        self._servo_events.append(func)


    def loop(self):
        self._read()


def servo_set(servo, degree):
    print("Setting up servo {} to degree {}".format(servo, degree))


u2 = UART(2, 115200, tx = 4, rx = 36)
rts = Pin(5)
rts.value(0)

servo_protocol = ServoRead(u2, 3)
servo_protocol.add_servo_event(servo_set)


while True:
    servo_protocol.loop()
