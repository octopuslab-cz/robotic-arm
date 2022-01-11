from machine import Pin, UART
from time import sleep_ms


class ServoRead():
    def __init__(self, uart):
        self._uart = uart
        self._servo_events = []
        self._data=""


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

        if len(self._data) != 5:
            print("Unknown or malformed data: {}".format(self._data))
            return

        try:
            servo = int(self._data[1])
            degree = int(self._data[2:5])
        except ValueError as e:
            print("Protocol value error! {}".format(e))
            raise e

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

servo_protocol = ServoRead(u2)
servo_protocol.add_servo_event(servo_set)


while True:
    servo_protocol.loop()
