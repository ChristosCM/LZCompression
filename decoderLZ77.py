from bitarray import bitarray
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='little')
    with open(inp, 'rb') as file:
        data.fromfile(file)
    while len(data) >= 1:
        #this is for the lzss algorithm, another format must be used for the lz77
        distance = ord(data[0:8].tobytes().decode())
        length = ord(data[8:16].tobytes().decode())
        del data[0:16]
        byte3 = data[0:8].tobytes().decode()
        del data[0:8]    
        for i in range(length):
            output_buffer.append(output_buffer[-distance])

        output_buffer.append(byte3)


    out_data =  ''.join(output_buffer)
    print (out_data)
    

decompress("compressed.bin")