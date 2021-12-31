import numpy as np
from PIL import Image

def Encode(src, message, dest):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    message += "@l1"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1
        array=array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")

def Decode(src):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-3:] == "@l1":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "@l1" in message:
        print("Hidden Message:", message[:-3])
    else:
        print("No Hidden Message Found")

def Stego():
    while True:
        print("--Welcome--")
        print("1: Encode")
        print("2: Decode")
        print("3: Exit")

        func = input("insert your selection: ")

        if func == '1':
            print("Enter Source Image Path")
            src = input()
            print("Enter Message to Hide")
            message = input()
            print("Enter Destination Image Path")
            dest = input()
            print("Encoding...")
            Encode(src, message, dest)

        elif func == '2':
            print("Enter Source Image Path")
            src = input()
            print("Decoding...")
            Decode(src)

        elif func == '3':
            break
        #elif func == '4':#
            #break#
        else:
            print("ERROR: Invalid option chosen")

if __name__ == '__main__':
    Stego()