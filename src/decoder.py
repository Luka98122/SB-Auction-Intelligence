import base64
import gzip
import io
import re
from nbt import nbt

def print_all_tags(tag, indent=0):
    """
    Recursively prints all NBT tags and their values.
    """
    prefix = "  " * indent
    
    # If it's a Compound tag (like a folder/dictionary)
    if isinstance(tag, nbt.TAG_Compound):
        for key, value in tag.items():
            print(f"{prefix}{key}:")
            print_all_tags(value, indent + 1)
            
    # If it's a List tag
    elif isinstance(tag, nbt.TAG_List):
        print(f"{prefix}[List of {len(tag)} items]")
        for i, item in enumerate(tag):
            print(f"{prefix}  Index {i}:")
            print_all_tags(item, indent + 2)
            
    # If it's a standard Value tag (String, Int, Byte, etc.)
    else:
        # Clean formatting codes if the value is a string
        val = tag.value
        if isinstance(val, str):
            val = re.sub(r'(§[0-9a-fk-or])', '', val)
        print(f"{prefix}{val}")

def decode_and_print_all(raw_base64):
    try:
        # 1. Decode Base64
        decoded_data = base64.b64decode(raw_base64)
        
        # 2. Decompress GZip
        uncompressed_data = gzip.decompress(decoded_data)
        
        # 3. Parse NBT
        buffer = io.BytesIO(uncompressed_data)
        nbt_data = nbt.NBTFile(buffer=buffer)
        
        # 4. Navigate to the first item in the list
        # Skyblock/Minecraft auction data usually wraps items in an 'i' list
        items_list = nbt_data["i"]
        
        for index, item in enumerate(items_list):
            print(f"--- Item #{index} ---")
            print_all_tags(item)
            print("-" * 20)
            
    except Exception as e:
        print(f"Failed to decode NBT: {e}")

# Testing it with your provided string
test_bytes = "H4sIAAAAAAAAAE1SXY/SQBS9wLKWSiT6oD7paNxkCQJtt0jLG7C4NnEBwY9HMrQDTGw77HQq7i/if/DDjLfQNfbl3p575sydk6MDVKDAdQAoFKHIg0K5AOWhSGNV0KGk6LoCZyz2N5B9Jah84gH7GNJ1gr9/dHgU8GQb0ntkfRaSaYg+gVeHffeGUUnmPmI9ctgHVtfF4lx2bLcOr3F+TSO6Ps78hmWax2HD7rgt16lDAwlDyRUZbmjs5yzTvsDqXmZN/cTPOmg+kP+XND/k5O4D98puOc7FSduLFQtDvma5OG2YRq5t5HTLbOEiAB2EvXjFY64Y+ZLyX0yS74i9z/hTzqTP4zXx/iFilxGgiv085ltGPM9Dmbd4az8MxS4h9yIlSpBkI4QiVMoMi1J0+DFyVqlUGybf4JGXuNeUyRXzFbnqGIZB2qcKz1H8sA9n/dmIXH8b34wmYzKY/NDgbEwjBs9wPOP+hhwXkGQgdqBDbfRbSdpXSvJlqliiwdMgjddMxIvkJw/DhWR3UB32v/aHk9vBvGe6JXixpAmbK6oGQiQKl/FZjJFguF1bAy0SAV+hBaBJvG6xFDstixDo87E3Hc0WuJMO1Sw9NFYRHk1KoG1zz7LElaDGc28Xd0dvES2XoLzNbMz7JHvFMXz4wDRF/XfMtVcrt0ObHd/oNm3bt5rOkhlN1wl811na1PIZZhVlo4XiR6VzDSqKRyxRNNpCrdu2jLZlEbdnOqR/C1CE81N+spz/BXrZlOsWAwAA"

if __name__ == "__main__":
    decode_and_print_all(test_bytes)