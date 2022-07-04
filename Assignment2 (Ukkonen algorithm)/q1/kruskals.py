"""
Name:Wong Cheok Foong
Std ID: 29801028
"""
import sys

def initSet(n):
    parent = [-1] * n
    return parent


def kruskals(V,G):

    def find(a):
        #with path splitting
        while parent[a] >= 0:
            c_parent = parent[a]
            g_parent = parent[c_parent]
            # The child of the root doesn’t have a grandparent
            if g_parent < 0:
                return c_parent
            parent[a] = g_parent
            a = c_parent
        return a

    def union_by_height(a,b):
        root_a = find(a) # find root of tree containing ‘a’
        root_b = find(b) # find root of tree containing ‘b’

        #if a and b are not in the same tree
        if root_a != root_b:

            height_a = -parent[root_a] # height of tree containing ‘a’
            height_b = -parent[root_b] # height of tree containing ‘b’
            
            if height_a > height_b: 
                parent[root_b] = root_a # link shorter tree’s root to taller

            elif height_b > height_a: 
                parent[root_a] = root_b

            #if height_a == height_b
            else:
                parent[root_a] = root_b
                parent[root_b] = -(height_b+1) # update to height
            
    file = open(G)
    graph = []
    for i in file:
        edge = i.strip().split(' ')
        edge = list(map(int, edge)) #change string to int
        graph.append(edge)
    
    sorted_edge = sorted(graph, key = lambda x:(x[2]))
    parent = initSet(V)
    output = []

    for i in sorted_edge:
        #if both vertices does not belong in the same tree
        if find(i[0]) != find(i[1]):
            union_by_height(i[0], i[1])
            output.append(i)
        # once all vertices are connected stop looping
        if len(output) == V -1:
            break

    total_weight = 0
    for i in output:
        total_weight += i[2]

    #create txt file for output
    file = open("output_kruskals.txt","w")
    file.write(str(total_weight) + "\n")
    for i in range(len(output)):
        file.write(str(output[i][0]) + " " + str(output[i][1]) + " " + str(output[i][2]) + "\n")
    file.close   
                    
    return output
    


print(kruskals(7,"G.txt"))

if __name__ == "__main__":

    argument_00 = sys.argv[0]

    argument_01 = sys.argv[1]

    argument_02 = sys.argv[2]

    kruskals(argument_01, argument_02)
