from bitarray import bitarray
import time
import os
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='big')
    with open(inp, 'rb') as file:
        data.fromfile(file)
    while len(data) >= 1:

        #this is for the lzss algorithm, another format must be used for the lz77
        flag = data.pop(0)
        if not flag:
            byte = data[0:8].tobytes().decode('utf-8')
            output_buffer.append(byte)
            del data[0:8]
        else:
            distance = ord(data[0:16].tobytes().decode('utf-16be'))
            length = ord(data[16:24].tobytes().decode('utf-8'))
            del data[0:24]
            symbol = data[0:8].tobytes().decode('utf-8')
            
            #maybe change this to make it more efficient
            for i in range(length):
                output_buffer.append(output_buffer[-distance])

            output_buffer.append(symbol)
            del data[0:8]


    out_data =  ''.join(output_buffer)
    print (out_data)

decompress("compressedSS/testing2.bin")
# times = []
# for file in os.listdir("compressedSS/"):
#     filename = os.fsdecode(file)

#     if filename.endswith(".bin"): 
#         start = time.time()
#         decompress("compressedSS/"+filename)
#         end = time.time()
#         times.append((end-start)*1000)
# print (times)