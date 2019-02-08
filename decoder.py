def getFile():
    fileName = input("Please provide the name of the file you wish to compress: ")
    try:
        file = open(fileName, "r")
    except IOError:
        print("File was not found")
    data = file.read()
    file.close()
    return data

#data for the lz encoder needs to be a string of characters for it to work
def lzEncoder(data,W,L):
    if L>W:
        print("Length of look ahead buffer is bigger than the size of the sliding window.")
    
    #encoded is an empty array of arrays. each sub-array is a triple based on LZ77
    encoded=[]
    #done is boolean that signifies that the whole document has been encoded
    done = False 
    #pos is the coding position 
    pos = 0
    while done==False:
        slidingW = []
        for l in range (pos,L):
            #check if the l is over the end of the document and close
            if l>len(data):
                done = True;
                break
            #check if the sliding window is over the start of the document and adjust it 
            if pos<=W:
                newW = pos
            else: 
                newW = W
            print(newW)
            print(pos)
            newW = 2
            for i in range(newW,0,-1):
                slidingW.append(data[pos-i])
                print (slidingW)
            pos +=1



lzEncoder(getFile(),2,1)