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

def write_long_text(start_block, text):
    block_size = 16
    text_bytes = [ord(c) for c in text]  # Convert text to bytes
    num_blocks = (len(text_bytes) + block_size - 1) // block_size  # Calculate number of blocks needed

    for i in range(num_blocks):
        block_data = text_bytes[i*block_size:(i+1)*block_size]  # Extract block data
        block_data += [0x00] * (block_size - len(block_data))  # Pad with zeros if needed
        status = rdr.write(start_block + i, block_data)
        if status == rdr.OK:
            print(f"Data written to block {start_block + i} successfully")
        else:
            print(f"Failed to write data to block {start_block + i}")

try:
    while True:
        (status, tag_type) = rdr.request(rdr.REQIDL)  # Check if a card is near
        if status == rdr.OK:
            (status, uid) = rdr.SelectTagSN()  # Get the card's UID
            if status == rdr.OK:
                print("Card detected with UID: ", uid)
                
                # Choose the starting block number
                start_block = 8  # Change this to the starting block
                
                # Authenticate for the chosen block
                status = rdr.authKeys(uid, start_block, keyA=key)
                if status == rdr.OK:
                    print("Authentication successful")
                    
                    # Prepare and write the long text
                    text = "Hello this is devraj"  # Change this line to your new text
                    write_long_text(start_block, text)
                    
                    rdr.stop_crypto1()  # End the communication
                else:
                    print("Authentication failed")
            else:
                print("Failed to select tag")
except KeyboardInterrupt:
    print("Stopped by user")
    utime.sleep_ms(500)
