from collections import defaultdict
from typing import *
import numpy as np
import time
from math import ceil

class Edge:
    def __init__(self, v1, v2, capacity, flow, reverse):
        self.v1 = int(v1)
        self.v2 = int(v2)
        self.capacity = int(capacity)
        self.flow = int(flow)
        self.reverse = reverse
        self.residual_capacity = 0
        self.original_pointer = None
        self.reverse_pointer = None
        
        if reverse:
            self.residual_capacity = self.flow
        else:
            self.residual_capacity = self.capacity - self.flow

    def update(self, bottleneck):
        self.flow += bottleneck
        if self.reverse == True:
            self.residual_capacity = self.flow
        else:
            self.residual_capacity = self.capacity - self.flow
            self.reverse_pointer.update(bottleneck)
    
    def elegible(self, delta):
        if self.residual_capacity >= delta:
            return True
        else:
            return False

class Graph:
    def __init__(self, data, directed = True):
        self.data = data
        self.graph = defaultdict(list) 
        self.load_data(directed)
        
    def load_data(self, directed):
        f = open(self.data, 'r')
        self.size = int(f.readline())
        if directed == True:
            for line in f:  
                split = line.split()
                v1, v2, capacity = int(split[0]), int(split[1]), int(split[2])
                original = self.add_edge(v1, v2, capacity, 0, False)
                reverse = self.add_edge(v2, v1, capacity, 0, True)
                original.reverse_pointer = reverse
                reverse.original_pointer = original
                
        if directed == False:
            for line in f:   
                split = line.split()
                v1, v2, capacity = int(split[0]), int(split[1]), int(split[2])
                self.add_edge(v1, v2, capacity, 0, False)
                self.add_edge(v2, v1, capacity, 0, True)
                self.add_edge(v1, v2, capacity, 0, True)
                self.add_edge(v2, v1, capacity, 0, False)
        f.close

    def add_edge(self, v1, v2, capacity, flow, reverse):
        self.graph[v1].append(Edge(v1, v2, capacity, flow, reverse))
        return self.graph[v1][-1]

    def get_neighboors(self, v):
        neighboors = self.graph[v]
        return neighboors

    def bfs(self, start, end, delta):
        setup = 1
        explored = [0] * (self.size + 1) 
        fathers = [0] * (self.size + 1)
        explored[start] = 1
        fathers[start] = None

        q = [start]
        while q != []:
            current = q.pop()
            neighboors = []
            if setup == 1:
                neighboors = self.get_neighboors(current)
                setup = 0
            else:
                neighboors = self.get_neighboors(current.v2)
            for neighboor in neighboors:
                if explored[neighboor.v2] == 0 and neighboor.elegible(delta):
                    explored[neighboor.v2] = 1
                    fathers[neighboor.v2] = current
                    if neighboor.v2 == end:
                        fathers.append(neighboor)
                        return fathers
                    q.append(neighboor)
        return False

    def get_path(self, start, end, delta = 1):
        fathers = self.bfs(start, end, delta)
        if fathers:
            path = [fathers[-1]]
            current = fathers[end]
            while current != start:
                path.append(current)
                current = fathers[current.v2]
            return path
        else:
            return False

    def get_bottleneck(self, path):
        bottleneck = path[0]
        for edge in path:
            if edge.residual_capacity < bottleneck.residual_capacity:
                bottleneck = edge
        return bottleneck

    def augment(self, path):
        bottleneck = self.get_bottleneck(path)
        bn_value = bottleneck.residual_capacity
        for edge in path:
            edge.update(bn_value)

    def ford_fulkerson(self, start, end, write_path, delta = False, reset = False):
        if reset == True:
            self.reset()

        if delta == False:
            path = self.get_path(start, end)
            while path:
                self.augment(path)
                path = self.get_path(start, end)

        if delta == True:
            capacity = self.get_capacity(start)
            delta = ceil(capacity/2)
            while delta != 1:     
                path = self.get_path(start, end, delta)
                while path:
                    self.augment(path)
                    path = self.get_path(start, end, delta)
                delta = ceil(delta/2)
            path = self.get_path(start, end)
            while path:
                self.augment(path)
                path = self.get_path(start, end)

        flow = self.get_flow(start)
        t = self.flow_alocation(write_path)
        reset = True
        return flow, t

    def get_flow(self, v):
        flow = 0
        neighboors = self.get_neighboors(v)
        for edge in neighboors:
            flow += edge.flow
        return flow

    def get_capacity(self, v):
        capacity = 0
        neighboors = self.get_neighboors(v)
        for edge in neighboors:
            capacity += edge.capacity
        return capacity

    def reset(self):
        self.graph = defaultdict(list) 
        f = open(self.data, 'r')
        self.size = int(f.readline())

        for line in f:
            split = line.split()
            v1, v2, capacity = int(split[0]), int(split[1]), int(split[2])
            self.add_edge(v1, v2, capacity, 0, False)
            self.add_edge(v2, v1, capacity, 0, True)
        f.close

    def flow_alocation(self, write_path):
        f = open(write_path, 'w')
        f.writelines('edge|v1|v2|flow\n')
        graph = self.graph
        count=0
        start = time.time()
        for v in graph:
            for edge in graph[v]:
                if edge.reverse == False:
                    count += 1
                    f.writelines(f'{count}|{edge.v1}|{edge.v2}|{edge.flow} \n')
        end = time.time()
        time = end - start
        f.close()
        return time
