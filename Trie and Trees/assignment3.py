class Node:
    """ Class for Node """
    def __init__(self, data = None, level = None, size = 27):
        self.link = [None] * size
        # data payload
        self.data = data
        # ranking is used to allocate the index of different suffixes in a string with same first characters
        self.rank = 0
        # the current level of the node
        self.level = level

class Trie:
    """ class for Trie """
    def __init__(self):
         self.root = Node(level = 0)

    def insert_recur(self, key, data = None):
        """
        Function to call insert_recur_aux()
        Time complexity: O(1)
        """
        current = self.root
        self.insert_recur_aux(current, key, 0, 0, data)

    def insert_recur_aux(self, current, key, count_level, rank, data=None):
        """
        Insert a new node into the Trie.
        Time complexity: O(N) where N is the length of key
        """

        #check if current is the first alphabet
        if current.level == 1: #and current.link[index] is not None:
                #increment rank by 1
                current.rank += 1
                rank = current.rank
        
        # After going through all the alphabet in key
        if len(key) == count_level:
            #index 0 to indicate leaf 
            index = 0
            if current.link[index] is not None:
                current = current.link[index]
            else:
                count_level +=1
                current.rank = rank
                current.link[index] = Node(level = count_level)
                current = current.link[index]
                # data stored in leaf node
            current.data = data
            
        else:

            #calculate index
            index = ord(key[count_level]) - 97 + 1
                
            # if following path exist
            if current.link[index] is not None:
                #the rank of the this alphabet follows the rank of the previous node
                current.rank = rank
                current = current.link[index]
                #recurse it
                self.insert_recur_aux(current, key, current.level, rank, data)
            
                
            # if following path does not exist
            else:
                #create a new node
                count_level +=1
                current.link[index] = Node(level = count_level)
                current.rank = rank
                current = current.link[index]
                #recurse it
                self.insert_recur_aux(current, key, count_level, rank, data)


    def search_substring(self, key, index):
        """
        Search for substring of key in Trie
        Time complexity:
            worst case: O(N) where N is the length of key
        """
        #The length of the substring
        length = -1
        
        #begin from root
        current = self.root
        #go through key 1 by 1
        for i in range(index, len(key)):
            char = key[i]
            #calculate index
            index = ord(char) - 97 + 1
            # check if the substring exist
            if current == self.root and current.link[index] is None:
                return False
            # if path exist
            elif current.link[index] is not None:
                current = current.link[index]
                length += 1
            # if path dont exist
            else:
                return (length, current.rank)

        return (length, current.rank)
    

    def search_smaller(self, key, text):
        """
        Checks if a string is smaller than another string. The input key is a string and the input text is a list of strings.
        The output is an integer determining how many string in text is smaller than key.
        Time complexity: O(N + M) where N is the length of text and M is the length of key
        """
        
        #begin from root
        current = self.root
        #value of index 0 for key
        first_key_index = ord(key[0]) - 97 + 1                

        #number of words in text smaller than key
        smaller_texts = 0
        
        for i in range(len(text)):
            current = self.root
            current_level = current.level

            #if index 0 of word is smaller than first_key_index
            if (ord(text[i][0]) - 97 + 1) < first_key_index:
                smaller_texts += 1

            #if index 0 of word is equal to first_key_index     
            elif (ord(text[i][0]) - 97 + 1) == first_key_index:

                for j in range(len(key)):
                    char = key[j]
                    index = ord(char) - 97 + 1

                    #if path exist
                    if current.link[index] is not None:
                        current = current.link[index]
                        current_level = current.level

                    #if path don't exist
                    else:
                        #compare the current index value of key with same index for word
                        if (ord(text[i][current_level]) - 97 + 1) < index:
                            smaller_texts += 1
                            break
                    
        return smaller_texts
        
    
def build_from_substrings(S, T):
    """
    Given a string S and another string T, we want to find a set of substrings of S which, when
    concatenated, equal T. The inputs S and T are strings  consist only of lowercase a-z characters.
    The output is a list of tuples, where each tuple represents a substring.
    Time complexity: O(N^2+M) where N is the number of characters in S and M is the number of characters in T
    """
    #list of lists where each list contains the index number and the suffix
    suffix_array = [0] * len(S)

    for i in range(len(S)):
        suffix_array[i] = []

    #create suffixes for S
    index = 0
    for i in range(len(S)):
        suffix = ''
        for j in range(i, len(S)):
            suffix += S[j]
        suffix_array[i].append(index)
        suffix_array[i].append(suffix)
        index += 1
        

    x = Trie()
    output = []

    #insert all of the suffixes from S into trie
    for i in range(len(suffix_array)):
        x.insert_recur(suffix_array[i][1])

    #the current index of T that has been build so far from substrings of S
    index = 0
    
    while index != len(T):
        # to determine the ranking of recurring character from suffixes of S
        rank = 0
        
        #position is a tuple where first element is length of substrings formed from current index
        #and second element is the rank of the suffix from trie
        position = x.search_substring(T, index)
        if position != False:
            for i in range(len(suffix_array)):
                #if the first character of the suffix is same as the character as index T
                if suffix_array[i][1][0] == T[index]:
                    #for each recurring character increment rank by 1
                    rank += 1
                    #if rank matches the rank of the character gotten from trie
                    if rank == position[1]:
                        output.append((suffix_array[i][0], suffix_array[i][0] + position[0]))
            index += position[0] + 1
        else:
            return position

    return output
        
##print(build_from_substrings("abbcc", "bccabcca"))
##print(build_from_substrings("abbcc", "bccdabcca"))
##print(build_from_substrings('abceebaaabda', 'cbcabdcacdecde'))

                                        
def alpha_pos(text, query_list):
    """
    Given a text and a query word, we need to find the number of words in the text which are alphabetically less than the query.
    The input text and query_list is a lists of strings. The output is a list of integers where the ith integer is the number of words in text which are alphabetically
    less than query_list[i].
    Time complexity: O(C+Q) where C is the total number of characters in text and Q is the total number of characters in query_list
    """
    output = []
    
    y = Trie()
    for i in range(len(text)):
        y.insert_recur(text[i])

    for i in range(len(query_list)):
        count = y.search_smaller(query_list[i], text)
        output.append(count)

    return output

##print(alpha_pos(["bac","aaa","baa","aac"],
##["ba", "aab", "zaa", "aa", "baa", "b"]))       

        
