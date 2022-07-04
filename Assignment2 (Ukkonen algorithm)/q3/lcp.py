"""
Name:Wong Cheok Foong
Std ID: 29801028
"""

import sys
from Ukkonen import *

def lcp(text1, text2, indices):
    file = open(indices)
    pairs = []
    for i in file:
        edge = i.strip().split(' ')
        edge = list(map(int, edge)) #change string to int
        pairs.append(edge)
    print(pairs)
    
    # generating lcp with suffix array
    # in the suffix_array method the key will add "$" terminal instead
    text = text1 + "#" + text2
    t1 = Tree()
    suffix_array = t1.suffix_array(text)

    output = pairs
    for k in range(len(pairs)):
        # stores all the index that starts with the same first character according to the current tuple (i,j)
        temp = []
        if text1[index[k][0]] == text2[index[k][1]]:
            char = text1[index[0]]
            for i in suffix_array:
                if text[i] == char:
                    temp.append(i)

        max_lcp = 0
        for j in range(len(temp)):
            # if j+1 is out of bound then can't compare j with j+1
            if j+1 <= len(temp):
                a = temp[j]
                b = temp[j+1]
                same = True
                lcp = 0
                while same:
                    if text[a] == text[b]:
                        lcp += 1
                        a += 1
                        b += 1
                    else:
                        same = False
                if lcp > max_lcp:
                    max_lcp = lcp
                    
        output[k].append(max_lcp)

    return output

    #create txt file for output
    file = open("output_lcp.txt","w")
    for i in range(len(output)):
        file.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
    file.close   
                    
    return output
            
def read_file(filename):
    file = open(filename)
    string = file.readline()

    return string

##text1 = "abcd"
##text2 = "dabc"
##indices = (0,1)
##print(lcp(text1, text2, "index.txt"))

if __name__ == "__main__":

    argument_00 = sys.argv[0]

    argument_01 = sys.argv[1]

    argument_02 = sys.argv[2]

    argument_03 = sys.argv[3]

    lcp(read_file(argument_01), read_file(argument_02), argument_03)
