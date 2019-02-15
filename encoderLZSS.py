from bitarray import bitarray
import sys
import time
import numpy as np
import os
def getFile(name):
    fileName = name
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
def write(bits,test):
    try:
        file = open("compressedSS/"+str(test)+".bin","wb")
        file.write(bits.tobytes())
        file.close()
    except IOError:
        print ("Couldn't find or write to file")
        

#data for the lz encoder needs to be a string of characters for it to work
def lzEncoder(filename,W,L,test):
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
            output.frombytes(chr(dis).encode('utf-16be'))
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
    #not really necessary
    output.fill()
    write(output,test)     

lzEncoder("testTxt/1.txt",4000,255,"testing2")
'''
data = np.empty((8,5),dtype=np.object)
data[0,] = ["originalSize","compressedSize","Ratio","Window","Running Time"]
for i in range (6):
    filename = 'testTxt/'+str(i+1)+'.txt'
    counter = 1
    for j in [4000,8000,160000,320000,64000,65535,80000]:
        start = time.time()
        lzEncoder(filename,j,255,i+1+j)
        end = time.time()
        data[counter,0] = os.path.getsize('testTxt/'+str(i+1)+'.txt')
        data[counter,1] = os.path.getsize('compressedSS/'+str(i+1+j)+'.bin')
        data[counter,2] = data[counter,1]/data[counter,0]
        data[counter,3] = j
        data[counter,4] = end-start
        counter += 1
    print (i)
    print (data)
    file = open("resSS/"+str(i+1)+".txt","w")
    file.write(",".join([",".join(item) for item in data.astype(str)]))
    file.write("\n")
    file.close() 
    '''
    