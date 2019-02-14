from bitarray import bitarray
import struct
def decompress(inp):
    output_buffer = []
    data = bitarray(endian='big')
    with open(inp, 'rb') as file:
        data.fromfile(file)
    encoded = []
    while len(data) >= 1:
        print (encoded)

        #this is for the lzss algorithm, another format must be used for the lz77
        flag = data.pop(0)
        if not flag:
            byte = data[0:8].tobytes().decode()
            output_buffer.append(byte)
            encoded.append((0,0,byte))
            del data[0:8]
        else:
            
            byte1 = ord(data[0:8].tobytes().decode())
            byte2 = ord(data[8:16].tobytes().decode())
            del data[0:16]
            byte3 = data[0:8].tobytes().decode()
            distance = byte1
            length = byte2
            
            encoded.append((distance,length,byte3))
            for i in range(length):
                output_buffer.append(output_buffer[-distance])


            output_buffer.append(byte3)
            del data[0:8]


    out_data =  ''.join(output_buffer)
    print (encoded)
    print (out_data)
    

decompress("compressed.bin")