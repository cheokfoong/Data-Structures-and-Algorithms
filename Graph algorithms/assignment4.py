import math

class MinHeap:
    def __init__(self, length):
        self.array = [None] * (length + 1)
        self.index_array = [None] * length #stores the vertex index of the heap array
        for i in range(1, len(self.array)):
            self.array[i] = [i-1, math.inf] #vertex starts from 0
            self.index_array[i-1] = i

    def serve(self):
        """
        swap first with last, then pop it
        :complexity: O(1)
        """
        first = self.array[1][0]
        last = self.array[-1][0]
        self.swap(self.array, 1, -1)
        self.swap(self.index_array, first, last)
        vertex = self.array.pop()

        return vertex

    def rise(self, k: int)-> None:
        """
        Rise element at index k to its correct position
        :complexity: O(logN) where N is the length of self.array
        """
        k = self.index_array[k]
        #rise the smaller value to top
        while k > 1 and self.array[k][1] < self.array[k//2][1]: # k//2 is parent
            index_k = self.array[k][0]
            index_parent = self.array[k//2][0]
            self.swap(self.array, k, k//2)
            self.swap(self.index_array, index_k, index_parent)
            k = k//2

        return k

    def swap(self, array, i, j) -> None:
        """
        swaping two elements
        :complexity: O(1)
        """
        tmp = array[i]
        array[i] = array[j]
        array[j] = tmp


    def sink(self) -> None:
        """
        Make the element at first index sink to the correct position
        :complexity: O(logN) where N is the length of self.array
        """
        if len(self.array) > 1:
            k = 1
            while 2*k <= len(self.array)-1:
                if 2*k+1 <= len(self.array)-1:
                    child = self.smallest_child(k)
                else:
                    child = 2*k
                if self.array[k][1] <= self.array[child][1]:
                    break
                
                index_k = self.array[k][0]
                index_child = self.array[child][0]
                self.swap(self.array, child, k)
                self.swap(self.index_array, index_child, index_k)
                k = child

        return k

    def smallest_child(self, k: int) -> int:
        """
        Returns the index of the smallest child of k
        :complexity: O(1)
        """
        if self.array[2*k][1] < self.array[2*k+1][1] or self.array[2*k][1] == self.array[2*k+1][1]:
            return 2*k
        else:
            return 2*k+1

    def update_distance(self, vertex_id, distance):
        """
        Update the distance of the vertex in the heap
        :complexity: O(1)
        """
        index = self.index_array[vertex_id]
        self.array[index][1] = distance

class Graph:
    def __init__(self, V):
        #Representing in adjacency list
        self.vertices = [None] * V
        for i in range(V):
            self.vertices[i] = Vertex(i)

    def reset(self):
        """
        Reset discovered and visited back to False
        :complexity: O(N), where N is the length of self.vertices
        """      
        for vertex in self.vertices:
            vertex.discovered = False
            vertex.visited = False

    def add_edges(self, argv_edges, argv_direct=True):
        """
        Create edge objects and add it to the vertex
        :complexity: O(N), where N is the length of argv_edges
        """
        for edge in argv_edges:
            u = edge[0]
            v = edge[1]
            w = edge[2]
            # add u to v
            current_edge = Edge(u,v,w)
            current_vertex = self.vertices[u]
            current_vertex.add_edge(current_edge)

            #add v to u (only for undirected)
            if not argv_direct:
                current_edge = Edge(v,u,w)
                current_vertex = self.vertices[v]
                current_vertex.add_edge(current_edge)

    def bfs(self, source):
        """
        Function for BFS, starting from source
        Time complexity: O(V+E), where V is the number of vertices in the input graph and E is the number of edges in the input graph.
        """
        self.reset()
        source = self.vertices[source]
        return_bfs = []
        discovered = []
        discovered.append(source)
        source.discovered = True # source is discovered
        s_value = source.value
        captured_chain = True
        
        while len(discovered) > 0:
            # serve from
            u = discovered.pop(0) # pop(0) same as serve
            u.visited = True      # means I have visit u
            return_bfs.append(u)
            
            for edge in u.edges:
                v = edge.v
                v = self.vertices[v]
                if v.discovered == False:
                    if v.value == s_value:
                        discovered.append(v)
                        v.discovered = True # ,means I have discovered v, adding it to queue
                    elif v.value == 0:
                        captured_chain = False
        return (return_bfs, captured_chain)

    def dijkstra(self, source, length, crossing_time, transform_time):
        """
        Function for dijkstra
        Time complexity: O(ElogV),where E is the total number of edges in input graph and V is the total number of vertices in input graph
        """
        self.reset()
        current_vehicle = "wheel" #starting vehicle is wheel

        hours_vehicle = self.optimal_crossing_time(crossing_time, current_vehicle, source.value, transform_time)
        current_vehicle = hours_vehicle[1]
        source.distance = hours_vehicle[0]
        source.vehicle = current_vehicle
        discovered = MinHeap(length)  # discovered is a queue
        discovered.update_distance(source.id, source.distance)
        #discovered.append(source, source.distance) #append(key, data)
        source.discovered = True # source is discovered

        #check if self.array[1] is the source/starting vertex
        if discovered.array[1][0] != source.id:
            discovered.swap(discovered.array, 1, source.id+1) #source.id+1 because the array index in heap starts with 1 not 0
        
        while len(discovered.array) > 1:
            # u = tuple of (vertex.id, distance)
            u = discovered.serve()
            if len(discovered.array) > 1:
                discovered.sink()
            ids = u[0]
            u = self.vertices[ids] # u is now a vertex object
            u.visited = True      # means I have visit u
            current_vehicle = u.vehicle

            #perform edge relaxation on all adjacent vertices
            for edge in u.edges:
                v = edge.v
                v = self.vertices[v]
                if v.discovered == False:  # means distance is still infinity
                    v.discovered = True # means I have discovered v, adding it to queue
                    #get optimal crossing time and vehicle
                    hours_vehicle = self.optimal_crossing_time(crossing_time, current_vehicle, v.value, transform_time)
                    edge.w = hours_vehicle[0]
                    v.vehicle = hours_vehicle[1]
                    v.distance = u.distance + edge.w
                    v.previous = u.id
                    discovered.update_distance(v.id, v.distance) #update the distance of vertex in the heap array
                    discovered.rise(v.id)

                #it is in heap, but not yet finalize
                elif v.visited == False:
                    #get optimal crossing time and vehicle
                    hours_vehicle = self.optimal_crossing_time(crossing_time, current_vehicle, v.value, transform_time)
                    edge.w = hours_vehicle[0]
                    v.vehicle = hours_vehicle[1] 
                    #if i find a shorter route, change it
                    if v.distance > u.distance + edge.w:
                        #update distance
                        v.distance = u.distance + edge.w
                        v.previous = u.id
                        discovered.update_distance(v.id, v.distance)
                        discovered.rise(v.id)
                        

    def optimal_crossing_time(self, crossing_time, vehicle, terrain, transform_time):
        """
        Get the optimal vehicle to cross the terrain of the vertex
        :complexity: O(N), where N is the length of crossing_time
        """
        if terrain == 0:
            terrain = "plain"
        elif terrain == 1:
            terrain = "hill"
        elif terrain == 2:
            terrain = "swamp"
        
        hours = crossing_time[vehicle][terrain]

        current_vehicle = vehicle

        for this_vehicle in crossing_time:
            if hours > crossing_time[this_vehicle][terrain] + transform_time:
                hours = crossing_time[this_vehicle][terrain] + transform_time
                current_vehicle = this_vehicle

        #returns a tuple for total hours and the current vehicle
        return (hours, current_vehicle)

        
class Vertex:
    def __init__(self, ids):
        self.id = ids
        self.edges = []
        # the value that the vertex hold 
        self.value = None
        #for traverse
        self.discovered = False
        self.visited = False
        #distance
        self.distance = math.inf
        #backtracking/ where i was from
        #stores previous vertes id
        self.previous = None
        #for Q2 to track for vehicle type
        self.vehicle = None

    def __str__(self):
        return_string = str(self.id)
        for edge in self.edges:
            return_string += "\n with edges" + str(edge)
        return return_string

    def add_edge(self, edge):
        self.edges.append(edge)

    def added_to_queue(self):
        self.discovered = True

    def visited_node(self):
        self.visited = True

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w

    def __str__(self):
        return_string = str(self.u) + "," + str(self.v) + "," + str(self.w)
        return return_string


def captured_chains(vfile, efile):
    """
    Function which finds all captured chains present in graph
    Input: Two files, vfile and efile
    Output: A list of lists where number of internal lists is equal to the number of captured chains in the input graph
    Time complexity: O(V+E), where V is the number of vertices in the input graph and E is the number of edges in the input graph.
    """
    vertex_file = open(vfile, "r")
    edge_file = open(efile, "r")

    #Assigning vertices to graph_board 
    v_length = int(vertex_file.readline())
    graph_board = Graph(v_length)
    for i in range(len(graph_board.vertices)):
        vline = vertex_file.readline()
        graph_board.vertices[i].value = int(vline[2])

    #Assigning edges to each vertex 
    edges = []
    e_length = int(edge_file.readline())  
    for i in range(e_length):
        eline = edge_file.readline()
        edges.append((int(eline[0]), int(eline[2]), None))

    graph_board.add_edges(edges, False)


    
    index = 0 
    output = []
    checked_vertex = [] #a list of vertices that has been gone through
    while len(checked_vertex) != v_length:
        #A captured_cahin list that is to be appended into output
        internal_list = []
        if index not in checked_vertex:
            current_vertex = graph_board.vertices[index]

            #if current_vertex is not an empty GO piece
            if current_vertex.value != 0:
                #Calls bfs function
                chain = graph_board.bfs(index)
                
                for vertex in chain[0]:
                    if vertex.id not in checked_vertex:
                        checked_vertex.append(vertex.id)
                    #check if the chain is a captured_chain
                    if chain[1] == True:
                        internal_list.append(vertex.id)
            #if current_vertex is an empty GO piece
            else:
                checked_vertex.append(current_vertex.id)

        if len(internal_list) != 0:
            output.append(internal_list)
            
        #Proceed to next vertex    
        index += 1

    return output

def terrain_pathfinding(vfile, efile, crossing_time, transform_cost, start, end):
    """
    Function which finds the quickest path for avehicle through difficult terrain.
    Input: Two files, vfile and efile
    Output: A two element tuple, where the first element is an integer which is number of hours and the second element is a list of tuples
    Time Complexity:O(Elog(V)), where E is the total number of edges in input graph and V is the total number of vertices in input graph
    """
    vertex_file = open(vfile, "r")
    edge_file = open(efile, "r")

    #Assigning vertices to graph_board 
    v_length = int(vertex_file.readline())
    graph_board = Graph(v_length)
    for i in range(len(graph_board.vertices)):
        vline = vertex_file.readline()
        graph_board.vertices[i].value = int(vline[2])

    #Assigning edges to each vertex 
    edges = []
    e_length = int(edge_file.readline())  
    for i in range(e_length):
        eline = edge_file.readline()
        edges.append((int(eline[0]), int(eline[2]), None))

    graph_board.add_edges(edges, False)

    graph_board.dijkstra(graph_board.vertices[start], v_length, crossing_time, transform_cost)

    #the previous vertex stores the total distance travelled from previous to current vertex
    previous = graph_board.vertices[end].previous
    previous_vertex = graph_board.vertices[previous]
    # total number of hours to travel
    total_hours = graph_board.vertices[previous].distance
    
    current_vertex = graph_board.vertices[end]
    current_index = end

    list_of_tuples = []
    list_of_tuples.append((end, previous_vertex.vehicle))

    #backtrack from the end vertex all the way to the start
    while current_index != start:
        # get the previous vertex
        current_index = graph_board.vertices[current_index].previous
        current_vertex = graph_board.vertices[current_index]
        list_of_tuples.append((current_index, current_vertex.vehicle))

    #reverse the list from start to end
    list_of_tuples.reverse()

    return (total_hours, list_of_tuples)
    
if __name__ == "__main__":

    #print(captured_chains("vfile.txt", "efile.txt"))

    crossing_time = {"wheel": {"plain": 1, "hill": 2, "swamp": 3},
    "tank" : {"plain": 3, "hill": 1, "swamp": 2},
    "hover": {"plain": 2, "hill": 3, "swamp": 1}}

    print(terrain_pathfinding("vfile2.txt", "efile2.txt", crossing_time, 0.5, 0, 9))
