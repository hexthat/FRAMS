"""`frams`
FRAM stuff
"""
import board
import busio
import adafruit_fram
import struct

__version__ = "beta"

i2c = busio.I2C(board.SCL, board.SDA)
fram = adafruit_fram.FRAM_I2C(i2c, address=0x50)

# check if addresses are free to use
def checkfree(size, address):
    for i in range(size):
        if size < 4:
            return True
            break
        # check address is free
        if fram[address + i] != bytearray(b'\xff'):
            # show first address in use
            print('Address', (address + i), 'first to fail checkfree')
            print('Use "frams.erase({},'.format(size - i), '{})""'.format(address + i))
            return False
            break
    print('Addresses needed are free to write.')
    return True

# read value stored in fram
def readnum(address):
    # unpack stored number at address
    return struct.unpack('lb', fram[address:(address + 5)])[0]

# store value with 4 bytes of fram
def writenum(x, address):
    # check if number can be stored in 4 bytes
    if x < 394860500 and x > -394860500:
        print(struct.pack('lb', x))  # show what number is packed as
        print('This will use 4 bytes of space from', address, 'to', (address + 4))
        if address < len(fram) - 4:  # can packed number fit
            if checkfree(4, address):
                # write packed number at address
                fram[address] = bytearray(struct.pack('lb', x))
        else:
            print('Not enough space at address.')
    else:
        print('Number outside of (-394860500, 394860500).')

# write text to address if enough space for it
def writetext(strng, address):
    print(strng)  # print the text to be stored
    # print how many bytes it will take
    print('This will use', len(strng), 'bytes of space from', address, 'to', (address + len(strng)))
    if address + len(strng) < len(fram):  # can text fit
        if checkfree(len(strng), address):  # check if space isnt already used
            fram[address] = bytearray(strng)  # write text to fram
            print(bytearray(strng))  # print what was writen
    else:
        print('Not enough space at address.')

# return text stored at address with a size of
def readtext(size, address, text=None):
    text = str(bytes(fram[address:(address + size)]))
    text = text[2:-1]
    return text
    del text

# erase fram from address to end of size
def erase(size, address):
    for i in range((address + size) - address):
        fram[address + i] = 255  # erase fram at addresses
