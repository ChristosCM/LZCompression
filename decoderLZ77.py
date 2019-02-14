from bitarray import bitarray
import time
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='big')
    with open(inp, 'rb') as file:
        data.fromfile(file)
    while len(data) >= 1:
        #this is for the lzss algorithm, another format must be used for the lz77
        distance = ord(data[0:32].tobytes().decode('utf-16'))
        length = ord(data[32:40].tobytes().decode('utf-8'))
        del data[0:40]
        byte3 = data[0:8].tobytes().decode('utf-8')
        del data[0:8]    
        for i in range(length):
            output_buffer.append(output_buffer[-distance])

        output_buffer.append(byte3)


    out_data =  ''.join(output_buffer)
    print (out_data)
    

decompress("compressed/2001.bin")