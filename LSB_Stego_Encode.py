import numpy as np
import PIL.Image

message_to_hide = input("Enter the secret: ")

image = PIL.Image.open('image.png', 'r')
width, height = image.size
img_arr = np.array(list(image.getdata()))


if image.mode == "P":
    print("Not Supported")
    exit()

channels = 4 if image.mode == "RGBA" else 3


pixels = img_arr.size // channels

stop_indicator = "$STEG$"
stop_indicator_length = len(stop_indicator)

message_to_hide += stop_indicator

byte_message = ''.join(f"{ord(v):08b}" for v in message_to_hide)
bits = len(byte_message)

if bits > pixels:
    print("Not Enough Space")
else:
    index = 0
    for i in range(pixels):
        for j in range(0,3):
            if index < bits:
                img_arr[i][j] = int(bin(img_arr[i][j])[2:-1] + byte_message[index], 2)
                index += 1

img_arr = img_arr.reshape(height, width, channels)
result = PIL.Image.fromarray(img_arr.astype('uint8'), image.mode)
result.save('encoded.png')
