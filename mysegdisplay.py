''' My MCP23008 based display driver '''

NUM_DIGITS = 4
BASE_ADDR = 0x20

MCP23008_IODIR = 0x00
MCP23008_GPIO = 0x09

# Seems these are backwords from the pinout
# and upside down or something
# LSB = A, MSB = DP
SEGDAT = [
  0b00111111,  # 0
  0b00110000,
  0b01011011,
  0b01111001,
  0b01110100,
  0b01101101,
  0b01101111,
  0b00111000,
  0b01111111,
  0b01111100,  # 9
  0b01111110,  # A
  0b01100111,  # b (other 6)
  0b01000011,  # c
  0b01110011,  # d
  0b01001111,  # E
  0b01001110,  # F
  0b01100011,  # o
  0b00000000,  # Off
  0b11111111,  # TEST
]

SEGDAT2 = [
  0b00111111,  # 0
  0b00000110,  # Flip
  0b01011011,
  0b01001111,  # Flip
  0b01100110,  # Flip
  0b01101101,
  0b01111101,  # Flip
  0b00000111,  # Flip
  0b01111111,
  0b01100111,  # 9 // Flip
  0b01110111,  # A // Flip
  0b01111100,  # b (other 6) // Flip
  0b01011000,  # c // Flip
  0b01011110,  # d // Flip
  0b01111001,  # E // Flip
  0b01110001,  # F // Flip
  0b01011100,  # o // Flip
  0b00000000,  # Off
  0b11111111,  # TEST
]


class MySegDisplay(object):

    def __init__(self, i2c):
        self.i2c = i2c
        self.setasoutput()

    def write(self, idx, regaddr, data):
        self.i2c.writeto(BASE_ADDR + idx, bytearray([regaddr, data]))

    def set_digit(self, digit, data, colon=False):
        if colon:
            dp = 1 << 7
        else:
            dp = 0

        if digit == 3:
            self.write(digit, MCP23008_GPIO, ~SEGDAT2[data])
        elif digit == 2:
            self.write(digit, MCP23008_GPIO, ~(SEGDAT2[data] | dp))
        elif digit == 1:
            self.write(digit, MCP23008_GPIO, ~(SEGDAT[data] | dp))
        elif digit == 0:
            self.write(digit, MCP23008_GPIO, ~SEGDAT[data])

    def setasoutput(self):
        ''' Sets all digits on all displays as output
            Being common-anode, all segments turn on '''
        for idx in range(0, NUM_DIGITS):
            self.write(idx, MCP23008_IODIR, 0x00)

    def set_all(self, data):
        for idx in range(0, NUM_DIGITS):
            self.write(idx, MCP23008_GPIO, ~data)

    def segtest(self):
        ''' Turns on all segments on all displays '''
        self.set_all(0xFF)

    def off(self):
        self.set_all(0x00)

    def display(self, value):
        for digit in range(0, NUM_DIGITS):
            val = int(value / 10 ** digit)
            self.set_digit(digit, val % 10)

    def text(self, value):
        dp = True if len(value.split(':')) > 1 else False
        value = "".join(value.split(':'))

        if len(value) == 3:
            self.set_digit(3, 17)  # Turn off leading digit

        for digit in range(0, len(value)):
            self.set_digit((len(value) - 1) - digit, int(value[digit]), dp)