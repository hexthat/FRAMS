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
    raw_bytes = fram[address : address + 4]
    
    # struct.unpack always returns a tuple, so we grab index [0]
    return struct.unpack('l', raw_bytes)[0]

# store value with 4 bytes of fram
def writenum(x, address):
    # A standard 4-byte signed integer can hold numbers from -2,147,483,648 to 2,147,483,647.
    # Your range of +/- 394,860,500 fits perfectly inside 4 bytes.
    if -394860500 < x < 394860500:
        packed_data = struct.pack('l', x)
        
        print(packed_data)  # show what number is packed as
        print('This will use 4 bytes of space from', address, 'to', (address + 4))
        
        if address <= len(fram) - 4:  # can packed number fit
            if checkfree(4, address):
                fram[address : address + 4] = packed_data
        else:
            print('Not enough space at address.')
    else:
        print('Number outside of (-394860500, 394860500).')

# write text to address if enough space for it
def writetext(strng, address):
    print(strng)  # print the text to be stored
    
    # Calculate exactly how many bytes it will take
    string_len = len(strng)
    end_address = address + string_len
    
    print('This will use', string_len, 'bytes of space from', address, 'to', end_address)
    
    if end_address < len(fram):  # can text fit
        if checkfree(string_len, address):  # check if space isn't already used
            fram[address : end_address] = bytearray(strng, 'ascii')  
            
            print(bytearray(strng, 'ascii'))  # print what was written
    else:
        print('Not enough space at address.')


# return text stored at address with a size of
def readtext(size, address):
    # Read the raw byte array out of the FRAM via slicing
    raw_bytes = fram[address : address + size]
    
    # Cleanly decode the bytes directly into a standard text string
    text = raw_bytes.decode('utf-8')
    
    return text

# erase fram from address to end of size
def erase(size, address):
    for i in range((address + size) - address):
        fram[address + i] = 255  # erase fram at addresses
