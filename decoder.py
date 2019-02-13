from bitarray import bitarray
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='big')
    
    with open(inp, 'rb') as file:
        data.fromfile(file)
    print (data)
    while len(data) >= 9:
        print (output_buffer)

        flag = data.pop(0)
        if not flag:
            byte = data[0:8].tobytes()

            output_buffer.append(byte)
            del data[0:8]
        else:
            byte1 = ord(data[0:8].tobytes())
            byte2 = ord(data[8:16].tobytes())
            del data[0:16]
            distance = (byte1 << 4) | (byte2 >> 4)
            length = (byte2 & 0xf)
            
            for i in range(length):
                output_buffer.append(output_buffer[-distance])
    out_data =  ''.join(output_buffer)
    

decompress("compressed.bin")