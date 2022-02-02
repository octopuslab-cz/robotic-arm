from machine import Pin, UART, I2C
from time import sleep_ms
from pca9685.servo import Servos
from utils.pinout import set_pinout


# blocking - simple test
def sweep(s, start, stop, delay=5, step=1):
   ang = start
   servo.position(s, ang)
   sleep_ms(delay)

   if start < stop:
      print("a")
      while ang < stop:
         ang = ang + step
         servo.position(s, ang)
         sleep_ms(delay)

   if start > stop:
      print("b")
      while ang > stop:
         ang = ang - step
         servo.position(s, ang)
         sleep_ms(delay)


print("Init I2C")
pins = set_pinout()
if pins.I2C_SDA_PIN is None:
        print("Error: I2C pins are not configured")
        print("Do you set up right board in setup() ?")

i2c = I2C(1, sda = Pin(pins.I2C_SDA_PIN), scl = Pin(pins.I2C_SCL_PIN), freq = 1000000)

print("Init Servo")
servo = Servos(i2c)


def sweeptest():
    sweep(2,30,160)
    sweep(1,30,180)
    sweep(2,160,30)
    sweep(1,180,30)

while True:
    sweeptest()
    sleep_ms(2000)



