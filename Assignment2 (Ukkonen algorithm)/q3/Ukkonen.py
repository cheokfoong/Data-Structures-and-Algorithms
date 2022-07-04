"""
Name:Wong Cheok Foong
Std ID: 29801028
"""

class Node:
    """ Class for Node """
    def __init__(self, size = 27):
        # list of edges for alphabet $ + a..z
        self.edges = [None] * size
        for i in range(size):
            self.edges[i] = Edge()

class Edge:
    """ Class for Edge """
    def __init__(self):
        self.content = [None, end_leaf]
        self.next = None
        self.leaf = None # only for leafs and depicts the index correspond to string
        
class End:
    def __init__(self, end_leaf):
        self.end = end_leaf
        
    def increment(self):
        self.end += 1

class Tree:
    """ Class for Tree """
    def __init__(self):
        self.root = Node()
        self.end = End(-1)

    def insert(self, key):
        # begin from root
        N = len(key)
        j = 0

        for i in range(N):
            end_leaf.increment() # increment end_leaf by 1
            while j < i + 1:
                current = self.root
                exist = True
                suffix_len = 0
                suffix = key[j:i+1]
                
                if suffix[0] == "$" or suffix[0] == "#":
                    index = 0
                else:
                    index = ord(suffix[0]) -97 +1

                current_content = current.edges[index].content

                if current_content[0] != None:

                    #rule 3 suffix already exist
                    edge_len = current_content[0] 
                    for k in range(len(suffix)):                   
                        if suffix[k] != key[edge_len]:
                            exist = False
                            break
                        edge_len += 1

                    #rule 2 branch from edge
                    if exist == False:
                        edge_len = current_content[0]
                        while key[edge_len] == suffix[suffix_len]:
                            edge_len += 1
                            suffix_len += 1

                        if current.edges[index].next == None:
                            self.split_children(current, key, index, suffix, edge_len, suffix_len, j)
                            j += 1
                            
                        else:
                            temp = suffix
                            while current.edges[index].next != None:
                                diff = current_content[1] - current_content[0] + 1
                                current = current.edges[index].next
                                temp = temp[diff:]
                                char = temp[0]
                                index = ord(char) -97 +1
                                
                            self.split_children(current, key, index, suffix, edge_len, suffix_len, j)
                            j += 1
                            
                    #Trick 4 show stopper
                    else:
                        break
                        
                #rule 2 branch from node
                else:
                    current.edges[index].content[0] = j
                    current.edges[index].leaf = j
                    j += 1

    def split_children(self, current, key, index, suffix, edge_len, suffix_len, j):
        if current.edges[index].next == None:
            print("char1: " + key[current.edges[index].content[0]])
            # change the current edge's content until where it started spliting and branching out 
            current.edges[index].content[1] = edge_len -1
            leaf = current.edges[index].leaf
            current.edges[index].leaf = None
            # create a new node for where the edge split
            current.edges[index].next = Node()

            current = current.edges[index].next
            # fill the content for the edges of the new node
            # continuation of the content where the previous edge split
            char = key[edge_len]
            index = ord(char) -97 +1
            print("char2: " + char)
            current.edges[index].content[0] = edge_len
            current.edges[index].leaf = leaf
            # newly added content for the other edge
            char = suffix[suffix_len]
            print("char3: " + char)
            index = ord(char) -97 +1
            current.edges[index].content[0] = j+suffix_len

            current.edges[index].leaf = j
            
        else:
            char = suffix[suffix_len]
            index = ord(char) -97 +1
            current.edges[index].content[0] = j+suffix_len

            current.edges[index].leaf = j

    def suffix_array(self, key):
        key += "$"
        N = len(key)
        suffix_array = []
        self.insert(key)
        #suffix_array.append(len(key)-1)

        unique_character = []
        # discover all unique characters
        for i in key:
            if i not in unique_character:
                unique_character.append(i)
        unique_character.sort()

            
        for char in unique_character:
            current = self.root
            if char == "$" or char == "#":
                index = 0
            else:
                index = ord(char) -97 + 1
            if current.edges[index].content[0] != None:
                if current.edges[index].leaf == None:
                        self.traversal(current.edges[index].next, suffix_array, unique_character)
                else:
                    suffix_array.append(current.edges[index].leaf)              
        return suffix_array

    def traversal(self, current_node, arr, unique_char):
        for char in unique_char:
            if char == "$" or char == "#":
                index = 0
            else:
                index = ord(char) -97 + 1
            if current_node.edges[index].content[0] != None:
                if current_node.edges[index].leaf == None:
                        self.traversal(current_node.edges[index].next, arr, unique_char)
                else:
                    arr.append(current_node.edges[index].leaf)

def read_file(filename):
    file = open(filename)
    string = file.readline()

    return string
                                                   
##text = "abcabe"
##text1 = "mississippi"
##text2 = "abccbccbddb$"        
##end_leaf = End(-1)
##t1 = Tree()
#print(t1.suffix_array(text))


