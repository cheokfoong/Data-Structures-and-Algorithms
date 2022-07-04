"""
Name: Wong Cheok Foong
Std ID: 29801028
"""
import sys
import math

class Node:
    def __init__(self, data = None, size = 2):
        self.link = [None] * size
        # data payload
        self.data = data

class Trie:
    def __init__(self):
         self.root = Node()

    def insert(self, char, code):
        #begin from root
        current = self.root
        for i in code:
            #convert bitstring into integer
            binary = int(i)
            # if path exist
            if current.link[binary] is not None:
                current = current.link[binary]
            # if path don't exist
            else:
                #create new node
                current.link[binary] = Node()
                current = current.link[binary]
        current.data = char

    def search(self, bitstring, index):
        #begin from root
        current = self.root
        while index < len(bitstring):
            #convert bitstring into integer
            binary = int(bitstring[index])
            # if path exist
            if current.link[binary] is not None:
                current = current.link[binary]
                index += 1
                #the last index
                if index == len(bitstring):
                    char = current.data
            # if path don't exist
            else:
                char = current.data
                break

        return char, index

def header_decoder(bitstring):
    header_details = []
    section = ["ascii_code", "len_ass_huff", "state_huff"]
    curr_sec_index = -1 #go through each header part in order from section table
    curr_sec = "no_uniq" #all headers start with this
    num_unique_char = math.inf # to determine when to stop the while loop later which is after header is completely decoded
    index = 0
    
    while index < len(bitstring):
        if curr_sec == "no_uniq" or curr_sec == "len_ass_huff":
            length = 1 # the length of the converted binary + 1
            next_len = 1 # the next minimal binary code to look at from current index
            while index < len(bitstring):
                #if binary is 0 means that it's a length, so convert it to 1
                if bitstring[index] == "0":
                    code = bitstring[index:index+length]
                    code = "1" + code[1:]
                    base_10 = int(code,2) + 1 #convert to integer
                    length = base_10
                    index += next_len
                    next_len = length
                #if binary is 1 means that it's a number
                else:
                    code = bitstring[index:index+length]
                    number = int(code,2)
                    index += next_len
                    # get the len of the huffman statement code
                    if curr_sec == "len_ass_huff":
                        huff_code_len = number
                    else:
                        num_unique_char = number
                    curr_sec_index += 1
                    curr_sec = section[curr_sec_index]
                    break
            
        elif curr_sec == "ascii_code":
            length = 7 #fixed length which is 7 bits
            code = bitstring[index:index+length]
            number = int(code,2)
            char = chr(number) # convert it to character
            header_details.append([char])
            index += length
            curr_sec_index += 1
            curr_sec = section[curr_sec_index]
            
        elif curr_sec == "state_huff":
            #loop for end because each new character decoded is appended to the end. Therefore, the first index
            #will always be the matching character and this reduces time complexity
            for i in range(len(header_details)-1, -1, -1):
                if header_details[i][0] == char:
                    header_details[i].append(bitstring[index:index+huff_code_len])
                    break            
            index += huff_code_len
            curr_sec_index  = 0 #assign it back to 0 to repeat the process
            curr_sec = section[curr_sec_index]
            
            # break when header_details has all the unique chacacters's details stored
            if len(header_details) == num_unique_char:
                break
            
    return header_details,index

def data_decoder(bitstring, header_details, index):
    #insert character details into the Trie 
    t1 = Trie()
    for i in header_details:
        t1.insert(i[0],i[1])

    text = ""
    index = index
    total_num_fields = 0 # the total number of fields
    field_code = True #is the current code part referring to the total number of fields, at the start is true
    while index < len(bitstring):
        if field_code == True:
            length = 1 # the length of the converted binary + 1
            next_len = 1 # the next minimal binary code to look at from current index
            while index < len(bitstring):
                    #if binary is 0 means that it's a length, so convert it to 1
                    if bitstring[index] == "0":
                        code = bitstring[index:index+length]
                        code = "1" + code[1:]
                        base_10 = int(code,2) + 1 #convert to integer
                        length = base_10
                        index += next_len
                        next_len = length
                    #if binary is 1 means that it's a number
                    else:
                        code = bitstring[index:index+length]
                        number = int(code,2)
                        index += next_len
                        if field_code == True:
                            total_num_fields = number
                            field_code = False
                        break
                    
        #outputing text part
        else:
            #if bit is 1-bit
            if bitstring[index] == "1":
                index += 1 # skip the 1-bit and move on to character
                char,index = t1.search(bitstring,index)
                text += char
            #if bit is 0-bit
            else:
                offset_state = True #the sequence is offset first then length
                offset = 0
                matched_len = 0
                index += 1 # skip the 0-bit and move on to offset and matched length
                length = 1 # the length of the converted binary + 1
                next_len = 1
                while offset == 0 or matched_len == 0:
                    #if binary is 0 means that it's a length, so convert it to 1
                    if bitstring[index] == "0":
                        code = bitstring[index:index+length]
                        code = "1" + code[1:]
                        base_10 = int(code,2) + 1 #convert to integer
                        length = base_10
                        index += next_len
                        next_len = length
                    #if binary is 1 means that it's a number
                    else:
                        code = bitstring[index:index+length]
                        number = int(code,2)
                        index += next_len
                        if offset_state == True:
                            offset = number
                            offset_state = False
                            length = 1
                            next_len = 1
                        else:
                            matched_len = number
            
                pointer = len(text) - offset
                for i in range(matched_len):
                    text += text[pointer]
                    pointer += 1
    return text
                
    
def decoder_lzss(binary):
    header_details,index = header_decoder(binary)
    text = data_decoder(binary,header_details,index)

    # create txt file for output
    file = open("output_decoder_lzss.txt", "w")
    file.write(text)
    file.close
    
    return text 

def read_file(filename):
    file = open(filename)
    string = file.readline()

    return string

##binary = "01111000011111000100100011000110100100011111111010011000100100001101111"
##header = "011110000111110001001000110001101001"
##data = "00011111111010011000100100001101111"
##text = "aacaacabcaba"
##header_details = [['a', '1'], ['b', '00'], ['c', '01']]
print(decoder_lzss(read_file("end_of_semester_msg_encoded.txt")))
##print(data_decoder(data,header_details,index))

##if __name__ == "__main__":
##
##    argument_00 =sys.argv[0]
##
##    argument_01 = sys.argv[1]
##
##    decoder_lzss(read_file(argument_01))
