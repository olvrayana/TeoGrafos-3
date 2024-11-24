from graph import Graph
import time

f = open('case_studies/times.txt', 'a')
f.write(f"{'Grafo':^5}|{'Mean Exec Time':^14}|{'Max Flow':^8}\n")

for i in range(1, 7):
    path = f'data/grafo_rf_{i}.txt'
    delta = True
    g = Graph(path)
    total_time = 0
    
    for j in range(10):
        t1 = time.time()
        fluxo, writing_time = g.ford_fulkerson(1, 2, f'case_studies/flow_allocation/flow_alocation_{i}.txt', delta = delta)
        t2 = time.time()
        execution_time = t2 - t1

        total_time += execution_time-writing_time
        tt = f"{total_time/10:.4f}"
    f.write(f"{i:^5}|{tt:^14}|{fluxo:^8}\n")
