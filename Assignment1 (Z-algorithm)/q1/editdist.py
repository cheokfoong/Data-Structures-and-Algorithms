"""
Name:Wong Cheok Foong
Std ID: 29801028
"""

import sys
from Z_algo import *

def read_file(filename):
    file = open(filename)
    string = file.readline()

    return string

def edit_dist(text, pattern):
    """
    determine edit distance between pattern and text given
    :complexity: O(n + m) where n is length of text and m is length of pattern
    """
    combine = pattern + "$" + text
    reverse_combine = text + "$" + pattern
    
    z1 = z_algorithm(combine)
    z2 = reverse_z_algorithm(reverse_combine)
    z1 = z1[len(pattern)+1:]
    z2 = z2[:len(text)]

    index = 0
    output = []
    L_pat = len(pattern)

    while index <= len(z1)- L_pat +1:
        #exact match
        if z1[index] == L_pat:
            output.append([index,0])

        # insertion
        elif z1[index] + z2[index + L_pat - 2] == L_pat - 1:
            output.append([index, 1])

        #substitution
        elif (index + L_pat-1 < len(z1)) and z1[index] + z2[index + L_pat-1] == L_pat-1:
            output.append([index,1])

        #deletion
        elif (index + L_pat < len(z1)) and (z1[index] + z2[index + L_pat] == L_pat):
            output.append([index,1])

        index+=1


    #create txt file for output
    file = open("output_editdist.txt","w")
    for i in range(len(output)):
        file.write(str(output[i][0]) + " " + str(output[i][1]) + "\n")
    file.close
    return output

    

if __name__ == "__main__":

    argument_00 =sys.argv[0]

    argument_01 = sys.argv[1]

    argument_02 = sys.argv[2]

    edit_dist(read_file(argument_01), read_file(argument_02))
