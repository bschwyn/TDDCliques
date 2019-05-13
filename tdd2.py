#every pair of connected stations has a fare (weight?)

#2 is confusing go through slowly

#find most lowest cost way (path?) from station 1 to N
#input: N stations, E lines of (station1, station2, weight)
#return lowest cost

#bla bla dijkstra's shortest path might be relevant
#need to construct graph
#parse question of how to find total path weight

#high level - take input, parse graph, do stuff to graph, spit out number
#parse graph function
#find cost function

#TDD!
#3 things to test
#test graph good?
#test for find cost
#test for everything (integration test)

from collections import defaultdict
import queue
import itertools
import heapq

class PriorityQueue():

    def __init__(self):
        self.h = []
        self.size = 0
        self.entry_finder = {}
        self.counter = itertools.count()

    def add(self, task, priority):
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.h, entry)
        self.size +=1

    def remove_task(self,task):
        entry = self.entry_finder.pop(task)
        entry[-1] = "removed"
        self.size-=1
        #hopefully this changes the data

    def is_empty(self):
        return self.size ==0


    def pop_task(self):
        while self.h:
            priority, count, task = heapq.heappop(self.h)
            if task is not "removed":
                del self.entry_finder[task]
                self.size -=1
                return task
        raise KeyError('pop from empty pq')


class Graph():

    def __init__(self, N):
        self.nodes = defaultdict(set)
        self.edges = {}
        self.size = N

    def add(self, node1, node2, cost):
        self.edges[(node1, node2)] = cost
        self.edges[(node2,node1)] = cost
        self.nodes[node1].add(node2)
        self.nodes[node2].add(node1)

    def modified_dikstra(self):

        n = self.size
        dists = [10000000]*(n+1)
        parents = [-1]*(n+1)

        dists[1] = 0
        pq = PriorityQueue()
        for i in range(1, n+1):
            pq.add(i, dists[i])

        #dikstra's same for different distance calcs?
        while not pq.is_empty():
            u = pq.pop_task()
            adj = self.nodes[u]
            for v in adj:
                #check for smaller distances?
                new_distance = max(0, self.edges[(u,v)] - dists[u])
                if new_distance + dists[u] < dists[v]:
                    dists[v] = dists[u] + new_distance
                    pq.add(v, new_distance)
                #is the distance metric transitive

        return dists[n]



        #put all nodes into priority queue
        #get min priority node
        #get adj nodes, record distance / parent, change priority


def read_input():
    string = ""
    x = input()
    while x != "":
        string += x
        x = input()
    return string

def make_graph(input_string):
    input_string = input_string.split("\n")
    N,E = input_string.pop(0).strip().split()

    N, E = [int(N), int(E)]

    g = Graph(N)
    for bla in range(E):
        line = input_string.pop(0)
        n1,n2, c = line.strip().split()
        n1, n2, c = [int(n1), int(n2), int(c)]
        g.add(n1, n2, c)
    return g





def smallest_cost(graph):
    #get all paths, then find shortest
    #find shortest path via dijskra and use a different comparison algorithm for finding the distance
    #maybe it is equivalent to the maximum cost, so the lowest cost path is the one with the smallest maximum?

    return graph.modified_dikstra()


def test_parse_graph():
    input_string ="5 5\n1 2 60\n3 5 70\n1 4 120\n4 5 150\n2 3 80"
    g = make_graph(input_string)
    nodes = g.nodes
    edges = g.edges
    nodes_expected = {1:set({2,4}), 3:set({5,2}), 2:set({1,4}), 4:set({5,1}), 5:set({4,3})}
    edges_expected = {(1,2):60, (2,1):60, (2,3):80, (3,2):80, (3,5):70, (5,3):70, (4,5):150, (5,4):150,
                      (1,4):120, (4,1):120}

    #assert dictionary_equals(nodes, {bla bla bla bla})
    #assert dictionary_equals(edges, {bla ba bla})


def test_smallest_cost():
    #test1
    g = make_graph("2 1\n 1 2 1")
    some_number_actual = smallest_cost(g)
    some_number_expected = 1
    print(some_number_expected == some_number_actual)

    #test2 smallest of two paths
    g = make_graph("4 4\n1 2 3\n2 4 4\n1 3 2\n3 4 3")
    actual = smallest_cost(g)
    print(actual == 3)

    #test3
    g = make_graph("3 2\n 1 2 10\n 2 3 5")
    actual = smallest_cost(g)
    print(actual == 10)

    #test4
    g = make_graph("5 3\n1 5 2\n1 2 2\n2 5 3\n")
    actual = smallest_cost(g)
    print(actual == 2)


def test_integration():
    pass

#class graph
#dictionary = {node:set(neighbornode1, neighbornode20, node2:set(nn3, nn1)}
#edges = {(n1,n2) = weight, (n2,n1)=weight, (n5,n8) = weight}

#run
test_parse_graph()
test_smallest_cost()