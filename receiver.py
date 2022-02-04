# Robotic-arm | serial - receiver
# octopusLAB 2018-22

from machine import Pin, UART, I2C
from time import sleep_ms
from pca9685.servo import Servos
from utils.pinout import set_pinout
from config import Config
from components.led import Led

led = Led(2)
conf = Config("robotic_arm")
# Default configuration
ARM_ID =  conf.get("arm_id")

# Servo
SERVO1_INIT = conf.get("s1")
SERVO2_INIT = conf.get("s2")
SERVO3_INIT = conf.get("s3")
SERVO4_INIT = conf.get("s4")
SERVO5_INIT = conf.get("s5")
SERVO6_INIT = conf.get("s6")

# Uart
UART_BAUD = 115200
UART_TxD = 4
UART_RxD = 36


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

        for char in self._uart.read():
            char = chr(char)
            if char == 'S':
                self._data = ""

            if char == '\n':
                self._parse()

            self._data += char


    def _parse(self):
        if not self._data:
            return

        if len(self._data) != 7:
            print("Unknown or malformed data: {}".format(self._data))
            return

        try:
            address = int(self._data[1:2])
            servo = int(self._data[2:4])
            degree = int(self._data[4:7])
        except ValueError as e:
            print("Protocol value error! {}".format(e))
            return

        if address not in [0, self._addr]:
            return


        self._on_servo_event(servo, degree)


    def add_servo_event(self, func):
        if func in self._servo_events:
            return

        self._servo_events.append(func)


    def loop(self):
        self._read()


class ServosCallback(Servos):
    def servo_set(self, servonum, degree):
        print("Setting up servo {} to degree {}".format(servonum, degree))
        self.position(servonum, degree)


def main():
    print("Booting")
    print("robotic arm: ",ARM_ID)
    print("Init UART")
    u2 = UART(2, UART_BAUD, tx = UART_TxD, rx = UART_RxD)

    print("Init I2C")
    pins = set_pinout()
    if pins.I2C_SDA_PIN is None:
        print("Error: I2C pins are not configured")
        print("Do you set up right board in setup() ?")
        return

    i2c = I2C(1, sda = Pin(pins.I2C_SDA_PIN), scl = Pin(pins.I2C_SCL_PIN), freq = 1000000)

    print("Init Servo")
    servo = ServosCallback(i2c)

    print("Initial position")
    servo.servo_set(1, SERVO1_INIT)
    servo.servo_set(2, SERVO2_INIT)
    servo.servo_set(3, SERVO3_INIT)
    servo.servo_set(4, SERVO4_INIT)
    servo.servo_set(5, SERVO5_INIT)
    servo.servo_set(6, SERVO6_INIT)

    print("Init protocol reader and callbacks")
    servo_protocol = ServoRead(u2, ARM_ID)
    servo_protocol.add_servo_event(servo.servo_set)

    print("Ready to go")
    led.blink()
    while True:
        servo_protocol.loop()

main()
