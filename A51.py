import re
import copy
import sys

X_LENGTH = 19
Y_LENGTH = 22
Z_LENGTH = 23 


x = []
y = []
z = []
key = ""
def loading_registers(key):
    global x, y, z
    x = [int(bit) for bit in key[:X_LENGTH]]
    y = [int(bit) for bit in key[X_LENGTH: X_LENGTH + Y_LENGTH]]
    z = [int(bit) for bit in key[X_LENGTH + Y_LENGTH:]]
  
def set_key(input):
    global key_one
    if len(input) == 64 and re.match("^([01])+", input):
        key = input
        loading_registers(input)
        return True
    return False


def to_binary(plain):
    binary_values = []
    for char in plain:
        binary = format(ord(char), '08b')  # Convert each character to 8-bit binary
        binary_values.extend([int(bit) for bit in binary])
    return binary_values

def get_majority(x, y, z):
    if x + y + z > 1:
        return 1
    return 0

def get_keystream(length):
    x_temp, y_temp, z_temp = copy.deepcopy(x), copy.deepcopy(y), copy.deepcopy(z)
    keystream = []
    
    for i in range(length):
        majority = get_majority(x_temp[8], y_temp[10], z_temp[10])

        if x_temp[8] == majority:
            new = x_temp[13] ^ x_temp[16] ^ x_temp[17] ^ x_temp[18]
            x_temp[1:] = x_temp[:-1]
            x_temp[0] = new

        if y_temp[10] == majority:
            new_one = y_temp[20] ^ y_temp[21]
            y_temp[1:] = y_temp[:-1]
            y_temp[0] = new_one

        if z_temp[10] == majority:
            new_two = z_temp[7] ^ z_temp[20] ^ z_temp[21] ^ z_temp[22]
            z_temp[1:] = z_temp[:-1]
            z_temp[0] = new_two

        keystream.append(x_temp[18] ^ y_temp[21] ^ z_temp[22])

    return keystream

def convert_binary_to_str(binary):
    return ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])

def encrypt(plain):
    binary = to_binary(plain)
    keystream = get_keystream(len(binary))
    return ''.join([str(binary[i] ^ keystream[i]) for i in range(len(binary))])

def decrypt(cipher):
    binary = [int(bit) for bit in cipher]
    keystream = get_keystream(len(cipher))
    return convert_binary_to_str(''.join([str(binary[i] ^ keystream[i]) for i in range(len(binary))]))

def input_key():
    tha_key = input('Enter a 64-bit key: ')
    while len(tha_key) != 64 or not re.match("^([01])+", tha_key):
        tha_key = input('Enter a valid 64-bit key: ')
    return tha_key

def menu():
    some_in = input('[0]: Quit\n[1]: Encrypt\n[2]: Decrypt\nPress 0, 1, or 2: ')
    while some_in not in {'0', '1', '2'}:
        some_in = input('Invalid input. Press 0, 1, or 2: ')
    return some_in

def input_plaintext():
    return input('Enter the plaintext: ')

def input_ciphertext():
    ciphertext = input('Enter a ciphertext: ')
    while not re.match("^([01])+", ciphertext):
        ciphertext = input('Enter a valid ciphertext: ')
    return ciphertext

def main():
    set_key(input_key())
    first_choice = menu()

    if first_choice == '0':
        sys.exit(0)
    elif first_choice == '1':   
        print(encrypt(input_plaintext()))
    elif first_choice == '2':
        print(decrypt(input_ciphertext()))

# Example of a 64-bit key: 1000100110110110100110010101101010001010100001111001011000110110
main()
