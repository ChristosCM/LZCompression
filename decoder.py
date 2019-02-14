from bitarray import bitarray
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='big')
    with open(inp, 'rb') as file:
        data.fromfile(file)
    while len(data) >= 1:
        flag = data.pop(0)
        if not flag:
            byte = data[0:8].tobytes().decode("utf8")

            output_buffer.append(byte)
            del data[0:8]
        else:
            print (output_buffer)
            byte1 = ord(data[0:8].tobytes().decode("utf8"))
            byte2 = ord(data[8:16].tobytes().decode("utf8","backslashreplace"))
            del data[0:16]
            byte3 = data[0:8].tobytes().decode("utf8")
            distance = (byte1 << 4) | (byte2 >> 4)
            length = (byte2 & 0xf)
            for i in range(length):
                output_buffer.append(output_buffer[-distance])
            output_buffer.append(byte3)
            del data[0:8]


    out_data =  ''.join(output_buffer)
    print (out_data)
    

decompress("compressed.bin")