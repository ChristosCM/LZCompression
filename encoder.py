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
        print("The size of L will be reduced to ",W," for improved performance")
    
    #encoded is an empty array of arrays. each sub-array is a triple based on LZ77
    encoded=[]
    #done is boolean that signifies that the whole document has been encoded
    done = False 
    # pos is the coding position 
    pos = 0;
    #first element is always going to appear as that so we append it and put pos in the next position
    encoded.append((0,0,data[0]))
    pos = 1;

    while done==False:
        slidingW = []
        for l in range (pos+1,L):
            #check if the l is over the end of the document and close
            if l>len(data):
                done = True;
                break
            #check if the sliding window is over the start of the document and adjust it 
            startWindow = max(0, pos - W)
            
            for i in range(pos-1,pos-newW,-1):
                slidingW.append(data[pos-i])
                print (slidingW)
            pos +=1
        break
        

def match(data,pos,L,W):
    length = -1
    distance = -1
    end = min(pos + L, len(data) + 1)
    for j in range(pos + 1, end):
		
        start = max(0, pos - W)
		substring = data[pos:j]

		for i in range(start, pos):	

            #this only looks at the l sized windows as a bigger one would not make a difference as it wouldn't match and check them
			string = data[i:i+j-pos] 

			if string == substring and len(substring) > length:
				distance = pos - i 
				length = len(substring)		

		if distance > 0 and length > 0:
			return (distance, length)
		return None



lzEncoder(getFile(),6,6)