from machine import Pin, SPI
from mfrc522 import MFRC522
import utime

# Pin numbers for SPI and RFID
sck = 6
mosi = 3
miso = 4
rst = 0
cs = 5

# Initialize the RFID reader
rdr = MFRC522(sck=sck, mosi=mosi, miso=miso, rst=rst, cs=cs)

# Key for authentication (default key for new cards)
key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

print("Place your card near the reader...")

def read_long_text(start_block, num_blocks):
    text_bytes = []
    for i in range(num_blocks):
        status, block_data = rdr.read(start_block + i)
        if status == rdr.OK:
            text_bytes.extend(block_data)
        else:
            print(f"Failed to read data from block {start_block + i}")
            return None
    # Remove padding zeros and convert bytes to string
    text = ''.join([chr(b) for b in text_bytes if b != 0x00])
    return text

try:
    while True:
        (status, tag_type) = rdr.request(rdr.REQIDL)  # Check if a card is near
        if status == rdr.OK:
            (status, uid) = rdr.SelectTagSN()  # Get the card's UID
            if status == rdr.OK:
                print("Card detected with UID: ", uid)
                
                # Choose the starting block number
                start_block = 8  # Change this to the starting block
                num_blocks = 2  # Change this to the number of blocks written
                
                # Authenticate for the chosen block
                status = rdr.authKeys(uid, start_block, keyA=key)
                if status == rdr.OK:
                    print("Authentication successful")
                    
                    # Read the long text
                    text = read_long_text(start_block, num_blocks)
                    if text is not None:
                        print(f"Data read from blocks {start_block} to {start_block + num_blocks - 1}: {text}")
                    
                    rdr.stop_crypto1()  # End the communication
                else:
                    print("Authentication failed")
            else:
                print("Failed to select tag")
except KeyboardInterrupt:
    print("Stopped by user")
    utime.sleep_ms(500)
