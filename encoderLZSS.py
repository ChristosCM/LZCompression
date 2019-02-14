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
    for j in range (pos+2, end):
        start = max(0, pos - W)
        substring = data[pos:j]
        
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
def lzEncoder(filename,W,L):
    data = getFile(filename)
    if L>W:
        print("Length of look ahead buffer is bigger than the size of the sliding window.")
        print("The size of L will be reduced to ",W," for improved performance")
    
    #encoded is an empty array of arrays. each sub-array is a triple based on LZ77

    output = bitarray(endian='big')
    # pos is the coding position 
    pos = 0;
    #first element is always going to appear as that so we append it and put pos in the next position
    #this is to convert it to bytes
    output.append(False)
    output.frombytes(chr(data[pos]).encode('utf-8'))  
  
    pos = 1;
    while pos<len(data):
        matching = match(data,pos,L,W)
        #this if checks if a match was found or not
        if matching:
            (dis, length) = matching
            #following is inserting the bits in an array to process
            output.append(True)
            output.frombytes(chr(dis).encode('utf-16'))
            output.frombytes(chr(length).encode('utf-8'))
            try:
                output.frombytes(chr(data[pos+length]).encode('utf-8'))
            except:
                output.frombytes(chr(data[pos+length-1]).encode('utf-8'))

            pos +=length+1
                
                
        #since a match was not found, the input will just be by itself with the next character
        else:
            output.append(False)
            output.frombytes(chr(data[pos]).encode('utf-8'))
            
            pos +=1
    output.fill()
    write(output)     

data = np.empty((11,5),dtype=np.object)
data[0,] = ["originalSize","compressedSize","Ratio","Window","Running Time"]
for i in range (10):
    filename = 'testTxt/'+str(i+1)+'.txt'
    counter = 1
    for j in [500,1000,2000,4000,8000,160000,320000,64000,65535,12000]:
        start = time.time()
        lzEncoder(filename,j,255,i+1+j)
        end = time.time()
        data[counter,0] = os.path.getsize('testTxt/'+str(i+1)+'.txt')
        data[counter,1] = os.path.getsize('compressed/'+str(i+1+j)+'.bin')
        data[counter,2] = data[i+1,1]/data[i+1,0]
        data[counter,3] = j
        data[counter,4] = end-start
        counter += 1
        print (data)
    file = open(str(i)+".txt","w")
    file.write(data)
    file.close()