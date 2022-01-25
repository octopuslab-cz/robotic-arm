# Robotic arm

## Protocol
Text based protocol 7 chars

 S   - 'S' char, start byte
 A   - '0..9', Arm address, 0 is broadcast
 SSS - '000..999', fixed 3 char number of servo
 DDD - '000..999', fixed 3 char degree
 \n  - 'new line char 0x10'

 example:
 'S3001050\n' - set arm ID 3, Servo 1, 50 degrees
 