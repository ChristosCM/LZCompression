from bitarray import bitarray
import sys
def getFile():
    fileName = input("Please provide the name of the file you wish to compress: ")
    try:
        file = open(fileName, "rb")
    except IOError:
        print("File was not found")
    data = file.read()
    data.strip()
    file.close()
    return data

def match(data,pos,L,W):
    length = -1
    distance = -1
    end = min(pos + L, len(data) + 1)
    for j in range (pos+1, end):
        start = max(0, pos - W)
        substring = data[pos:j]
        #this is another implementation that uses rfind, doesnt work as of now but can use it to make the program faster
        # string = data.rfind(substring,start,end)
        # if (string!=-1 and len(substring) >length):
        #     distance = string
        #     length = len(substring)
        for i in range(start, pos):	
            #this only looks at the l sized windows as a bigger one would not make a difference as it wouldn't match and check them
            string = data[i:i+j-pos]
            if (string == substring and len(substring) >=length):
                distance = pos -i
                length = len(substring)
    if (distance > 0 and length >0):
        return (distance, length)
    return None
def write(bits):
    try:
        file = open("compressed.bin","wb")
        #file.write(bits.tobytes())
        #file.close()
        bits.tofile(file)
    except IOError:
        print ("Couldn't find or write to file")

#data for the lz encoder needs to be a string of characters for it to work
def lzEncoder(data,W,L):
    if L>W:
        print("Length of look ahead buffer is bigger than the size of the sliding window.")
        print("The size of L will be reduced to ",W," for improved performance")
    
    #encoded is an empty array of arrays. each sub-array is a triple based on LZ77
    encoded=[]

    output = bitarray(endian='big')
    # pos is the coding position 
    pos = 0;
    #first element is always going to appear as that so we append it and put pos in the next position
    encoded.append((0,0,data[0]))
    #this is to convert it to bytes
    output.append(False)
    output.frombytes(chr(data[pos]).encode("ISO-8859-1"))
    pos = 1;
    while pos<len(data):
        matching = match(data,pos,L,W)
        #this if checks if a match was found or not
        if matching:
            (dis, length) = matching
            encoded.append((dis,length,data[pos+length]))
            #following is inserting the bits in an array to process
            output.append(True)
            output.frombytes(chr(dis>>4).encode("ISO-8859-1"))
            output.frombytes(chr(((dis & 0xf) << 4) | length).encode("ISO-8859-1"))
            output.frombytes(chr(data[pos+length]).encode("ISO-8859-1"))
            pos +=length+1
                
                
        #since a match was not found, the input will just be by itself with the next character
        else:
            encoded.append((0,0,data[pos]))
            output.append(False)
            output.frombytes(chr(data[pos]).encode("ISO-8859-1"))
            
            
            pos +=1
    output.fill()
    write(output)     
    print (output)

lzEncoder(getFile(),400,80)