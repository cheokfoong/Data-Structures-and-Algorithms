import timeit
import csv
import random
random.seed(0)

def numerical_radix_sort(num_list, b):
    """
    Stable sorting for the list of integer values. The input values are num_list which takes in a list of integers and b
    which takes in a base number. The output will be a sorted and stable list if integers
    complexity:O(N+b), where N is the length of num_list and b is the base
    """
    count_array = [None] * b
    for i in range(len(count_array)):
            count_array[i] = []
        
    col = 0
    output = num_list
    
    while (len(count_array[0]) != len(num_list)): #if all items are in count_array[0] means that it has loop through all columns
        for i in range(len(count_array)): #resetting count_array
            count_array[i] = []
        
        for item in output:
            position = (item//(b**col)) % b
            count_array[position].append(item)
        col += 1

        output = [] * len(num_list) #resetting output
        for i in count_array:
            for j in i:
                output.append(j)

    return output
        
##num_list =[123,312,1000,76,594,100]
##
##b = 3
##
##print(numerical_radix_sort(num_list, b))
                        
def test_bases(num_list):
    """
    Using different bases that are the powers of 2 to sort a list of numbers. The input value num_list which takes a list of number
    and the output will return a list of tuples with elements of a base and the number representing
    the time in seconds.
    complexity: O(N+b), where N is the length of num_list and b is the base 
    """
    tuple_list = []
    
    k = 1

    smaller_magnitude = True
    while smaller_magnitude:
        base = 2**k
        
        start_time = timeit.default_timer()
        output = numerical_radix_sort(num_list,base)
        finish_time = timeit.default_timer()
        time_to_sort_list = finish_time - start_time
        
        this_tuple = (k, time_to_sort_list)
        tuple_list.append(this_tuple)
        
        k += 1

        if len(tuple_list) > 1:
            if tuple_list[-1][1] > tuple_list[0][1]:
                smaller_magnitude = False

    return tuple_list
                    

##data1 = [random.randint(0,2**8-1) for _ in range(10**4)]    
##data2 = [random.randint(0,2**8-1) for _ in range(10**5)]
##data3 = [random.randint(0,2**(2**10)-1) for _ in range(10)]
##data4 = [random.randint(0,2**(2**10)-1) for _ in range(20)]

##
##data_list = [data1, data2, data3, data4]
##
##filename = "output_for_datas.csv"
##
##fields = ['Exponent', 'Runtime']
##
##with open (filename, 'w', newline="") as csvfile:
##    writer = csv.writer(csvfile)
##
##    for i in range(len(data_list)):
##        writer.writerow(fields)
##        writer.writerows(test_bases(data_list[i]))
    
def scrabble_helper(word_list, char_set_list):
    """
    Determines which words can be made using a given set of letters. The input values are word_list which takes in a list
    of strings and the char_set_list which also takes in a list of string. The output returns char_set_list which consists
    a list of lists.
    complexity: O(N*M) where N is the length of word_list and M is the maximum number of characters in word_list
    """
    col = 0
    for word in word_list:
        if len(word) > col:
            col = len(word)

    position = -1 #start from first column which is right aligned
    for length in range(col):
        
        max_item = 0
        # getting the largest value of string for the particular column
        for word in word_list:   
            if len(word) > length:
                item = ord(word[position]) - 97
                if item > max_item:
                    max_item = item

        count_array = [None] * (max_item + 1)
        for i in range(len(count_array)):
            count_array[i] = []
        
        for word in word_list:
            if len(word) > length:
                item = ord(word[position]) - 97
                count_array[item].append(word) 
            else:
                count_array[0].append(word) #len of words that are shoter than the len of column are place in the bucket count_array[0]

        index = 0
        #rearranging word_list
        for i in range(len(count_array)):   
            item = i
            inner_list = count_array[i]
            for j in inner_list:
                word_list[index] = j
                index += 1

        position -= 1 #move to next column
    
    count_array = [None] * len(char_set_list)
    for i in range(len(count_array)):
        count_array[i] = []

    for i in range(len(char_set_list)):
        for j in range(len(word_list)):
            if sorted(word_list[j]) == sorted(char_set_list[i]):
                count_array[i].append(word_list[j])

    char_set_list = count_array

    return char_set_list
            
word_list = ['pots', 'pot', 'stop', 'post', 'stops', 'stoop', 'sop', 'pos']
char_set_list = ['sopt', 'otp', 'ppsto']


print(scrabble_helper(word_list, char_set_list))
