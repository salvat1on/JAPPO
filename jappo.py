import os
import random
import codecs
import re

# Function to read the content of a file and return it as a string
def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Function to write the transformed payload to a file in the same directory as the script
def write_to_file(file_name, content):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(script_directory, file_name)
    with open(output_file_path, 'w') as file:
        file.write(content)

# Define the file path (update with your file path)
input_file_path = 'your_file.py'
output_file_name = 'payload.py'

# Read the content of the input file
payload = read_file(input_file_path)

# Create random parameters for transform function output spec
random.seed(version=2)
random_key = random.randint(1, 25)
# Extend with random encoding
repl_randchar = (random.choice(['###', 'zzz', 'abcd'])) * random_key


# Separate functions for each transformer
def hextransform(payload):
    hex_payload = payload.encode().hex()
    transformed_payload = f'''#!/usr/bin/env python3
# Transformed payload using hextransform
import codecs

hex_payload = "{hex_payload}"
deobfuscated_payload = bytes.fromhex(hex_payload).decode()
exec(deobfuscated_payload)
'''
    print("Original payload: " + payload)
    print("Transformed payload: " + hex_payload)
    return transformed_payload


def rot13transform(payload):
    rot13_payload = codecs.encode(payload, 'rot_13')
    mutated_rot13_payload = re.sub(r"\s", repl_randchar, rot13_payload)
    transformed_payload = f'''#!/usr/bin/env python3
# Transformed payload using rot13transform
import codecs

rot13_payload = "{mutated_rot13_payload}"
s1_deobfuscated_payload = re.sub("{repl_randchar}", " ", rot13_payload)
s2_deobfuscated_payload = codecs.decode(s1_deobfuscated_payload, "rot_13")
exec(s2_deobfuscated_payload)
'''
    print("Original payload: " + payload)
    print("Transformed payload: " + mutated_rot13_payload)
    return transformed_payload


# Specify main driver
def main():

    # Random transformation selector
    function_list = [hextransform, rot13transform]
    selectedfunction = random.choice(function_list)
    # Ensure repl_randchar was defined earlier
    transformed_payload = selectedfunction(payload)
    
    # Write the transformed payload to the output file in the same directory as the script
    write_to_file(output_file_name, transformed_payload)

    if "rot13transform" in str(selectedfunction):
        print('selected modified rot-13')
    elif "hextransform" in str(selectedfunction):
        print('selected hex')


if __name__ == "__main__":
    main()
