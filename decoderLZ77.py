from bitarray import bitarray
import time
import os
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='big')
    with open(inp, 'rb') as file:
        data.fromfile(file)
        print (len(data))

    while len(data) >= 1:
        #this is for the lzss algorithm, another format must be used for the lz77
        #utf-16be stands for Big Endian which drops it down to 16 bits and saves space

        distance = ord(data[0:16].tobytes().decode('utf-16be'))
        length = ord(data[16:24].tobytes().decode('utf-8'))
        del data[0:24]
        byte3 = data[0:8].tobytes().decode('utf-8')
        del data[0:8]    
        for i in range(length):
            output_buffer.append(output_buffer[-distance])

        output_buffer.append(byte3)


    out_data =  ''.join(output_buffer)
    print (out_data)

decompress("compressed/testing.bin")
# times = []
# for file in os.listdir("compressed/"):
#     filename = os.fsdecode(file)

#     if filename.endswith(".bin"): 
#         start = time.time()
#         decompress("compressed/"+filename)
#         end = time.time()
#         times.append((end-start)*1000)
# print (times)