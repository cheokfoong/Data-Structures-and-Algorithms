"""
Name: Wong Cheok Foong
Std ID: 29801028
"""
import sys

class Heap:
    def __init__(self, text):
        self.length = 0
        self.the_array = []
        
    def swap(self, i, j):
        tmp = self.the_array[i]
        self.the_array[i] = self.the_array[j]
        self.the_array[j] = tmp
    
    #swap root with last element then pop the last element
    def serve(self, k):
        last_element = self.length
        self.swap(k, last_element)
        smallest = self.the_array.pop(last_element)
        self.length -= 1
        return smallest[0]

    #Rise element at index k to its correct position
    def rise(self, k):
        arr = self.the_array
        while k > 1:
            if arr[k][1] < arr[k//2][1] or (arr[k][1] == arr[k//2][1] and len(arr[k][0]) < len(arr[k//2][0])):
                self.swap(k, k//2)
                k = k//2
            else:
                break

    #Returns the index of the smallest child of k.
    def smallest_child(self, k):
        arr = self.the_array
        if 2*k == self.length or arr[2*k][1]< arr[2*k+1][1] or (arr[2*k][1] == arr[2*k+1][1] and len(arr[2*k][0]) < len(arr[2*k+1][0])):
            return 2*k
        else:
            return 2*k+1

    #Make the element at index k sink to the correct position
    def sink(self, k):
        arr = self.the_array
        while 2*k <= self.length:
            child = self.smallest_child(k)
            if arr[k][1] < arr[child][1] or (arr[k][1] == arr[child][1] and len(arr[k][0]) == len(arr[child][0])):
                break
            self.swap(child,k)
            k = child
            
def Huffman(text):
    heap = Heap(text)
    heap.the_array.append(None) #heap root should start from index 1

    num_unique = 0 #number of unique characters
    #get unique characters
    for z in text:
        if z not in heap.the_array:
            heap.the_array.append(z)
            num_unique += 1

    #count frequencies for each unique characters
    for z in range(1, len(heap.the_array)):
        count = 0
        for x in text:
            if x == heap.the_array[z]:
                count += 1
        heap.the_array[z] = [heap.the_array[z], count]
        
    heap.length = len(heap.the_array) - 1 #store the length
    
    #to store binaries for encoding
    encoding = [None] * (heap.length + 1)
    for z in range(1, heap.length + 1):
        encoding[z] = [heap.the_array[z][0], ""]
    
    #create a min heap by performing sinking
    current = heap.length//2 
    while current >0:
        heap.sink(current)
        current = current//2
        
    #start encoding
    while heap.length > 0:
        binary = "0"
        sum_of_freq = 0 # sum of frequency of next two characters
        combined_char = "" # combination of next two characters
        for z in range(2): # serve two per time to determine which is left(0) and right(1)
            min_root = heap.the_array[1]
            characters = heap.serve(1) #1 indicates the root of the heap
            heap.sink(1)
            sum_of_freq += min_root[1] 
            combined_char += characters 

            #update binary encoding
            for char in characters:
                index = 1
                while True:
                    if encoding[index][0] == char:
                        encoding[index][1] += binary
                        break
                    else:
                        index += 1
            binary = "1"

        #append the new combined_char
        if heap.length > 0:
            heap.the_array.append([combined_char, sum_of_freq])
            heap.length += 1
            heap.rise(heap.length)

    encoding.pop(0)
    #reverse the binary encoding to prepend
    for i in range(len(encoding)):
        encoding[i][1] = encoding[i][1][::-1]
    
        
    return encoding, num_unique

def convert_binary(number):
    binary = ""
    while number > 0:
        binary += str(number%2)
        number >>= 1
    binary = binary[::-1] #flip it to make it prepend
    return binary

def Elias(number):
    binary = convert_binary(number) 
    encode = binary
    temp = len(binary) - 1 #length component to encode

    #stop when length of modified binary has reached 1
    while temp > 0:
        binary = convert_binary(temp)
        #convert binary to base 10 and shift it by length of current encode for prepending later
        prepend_binary = int(binary,2) << len(encode)
        #conduct OR operation on the current encode number which has been converted to base 10
        #and the prepend_binary
        base_10 = int(encode,2) | prepend_binary
        #convert it back to binary
        encode = convert_binary(base_10)
        #change leading 1 of its minimal binary code to 0
        encode = "0" + encode[1:]
            
        temp = len(binary) - 1
        
    return encode
    

def header(string):
    huffman_code, num_of_unique = Huffman(string)
    #perform elias opeartion on the number of unique character
    elias_num_of_unique = Elias(num_of_unique)

    output = [None] * len(huffman_code)
    for i in range(len(huffman_code)):
        output[i] = huffman_code[i]
        current = huffman_code[i]
        ascii_code = convert_binary(ord(current[0])) #binary form for the ascii of the unique character
        len_huffman_code = Elias(len(current[1])) #perform elias on the length of assigned huffman codeword

        output[i].append(ascii_code)
        output[i].append(len_huffman_code)

    #compute bitstring for header
    bitstring = ""
    bitstring += elias_num_of_unique
    for char in output:
        bitstring += char[2]
        bitstring += char[3]
        bitstring += char[1]

    # create txt file for output
    file = open("output_header.txt", "w")
    file.write(bitstring)
    file.close
    
    return bitstring

def read_file(filename):
    file = open(filename)
    string = file.readline()

    return string

#print(header(read_file("string.txt")))
#print(header("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"))

if __name__ == "__main__":

    argument_00 =sys.argv[0]

    argument_01 = sys.argv[1]

    header(read_file(argument_01))
