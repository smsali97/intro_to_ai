import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Node():
  def __init__(self,data):
    self.data = data
    self.edgeList = dict()

class Graph():
  def __init__(self):
    self.nodeList = set()
  
  # Calculates cost of the tour specified by the edges
  def tourCost(self,t=list()):
    tour = t.copy()
    totalCost = 0
    tour.insert(0,"C") # tour starts with C
    for i in range(len(tour)-1):
      source = self.findNode(tour[i])
      dest = self.findNode(tour[i+1])
      
      totalCost += source.edgeList[dest]
    return totalCost
  def addNode(self,data):
    self.nodeList.add(Node(data))
  
  def findNode(self,data):
    for node in self.nodeList:
      if node.data == data:
        return node
    return None 

  def addEdge(self,cost,source,dest):
    a = self.findNode(source)
    b = self.findNode(dest)
    a.edgeList[b] = cost
    b.edgeList[a] = cost

def doCrossover(parent1, parent2, two_pts, size):
    crossover = [None for _ in range(size)]
    # Copy randomly selected set from first parent
    for j in range(two_pts[0],two_pts[1]):
        crossover[j] = parent1[j]
    k = two_pts[1] # ptr for crossover
    l = two_pts[1] # ptr for parent
    while (k != two_pts[0]):
        if k == size: k = 0
        if l == size: l = 0
        if parent2[l] not in crossover:
            crossover[k] = parent2[l]
            k += 1
        l += 1
    return crossover

tsp_graph = Graph()
for node in ["A","B","C","D","E","F"]:
  tsp_graph.addNode(node)
tsp_graph.addEdge(8,"A","B")
tsp_graph.addEdge(10,"A","C")
tsp_graph.addEdge(3,"A","D")
tsp_graph.addEdge(4,"A","E")
tsp_graph.addEdge(6,"A","F")
tsp_graph.addEdge(9,"B","C")
tsp_graph.addEdge(5,"B","D")
tsp_graph.addEdge(8,"B","E")
tsp_graph.addEdge(12,"B","F")
tsp_graph.addEdge(7,"C","D")
tsp_graph.addEdge(6,"C","E")
tsp_graph.addEdge(2,"C","F")
tsp_graph.addEdge(8,"D","E")
tsp_graph.addEdge(11,"D","F")
tsp_graph.addEdge(8,"E","F")

sample_space = ["A","B","D","E","F"]
POP_SIZE = 10 # Population Size
K_TOURNAMENT = 2 # binary tournament
MUTATION_RATE = 0.2
OFFSPRING_POOL = 4
MAX_GEN = 100


populations = []
best_so_far = [] # metric
avg_so_far = [] # metric

# generate initial populations
for i in range(POP_SIZE):
  permutation = sample_space.copy()
  random.shuffle(permutation)
  # add fitness function
  populations.append((permutation,tsp_graph.tourCost(permutation)))

for i in range(MAX_GEN):
  # select parents
  parents = []
  for i in range(OFFSPRING_POOL):
    competitors = random.sample(populations,K_TOURNAMENT) # tournament
    parents.append(max(competitors,key=lambda x: tsp_graph.tourCost(x[0])))
  offsprings = []
  
  # generate offspring
  for i in range(OFFSPRING_POOL-1):
    two_pts = random.sample(range(len(sample_space)+1),2) # 2-point crossover
    two_pts.sort()

    parent1 = parents[i][0]
    parent2 = parents[i+1][0]

    crossover1 = doCrossover(parent1,parent2,two_pts,len(sample_space))
    crossover2 = doCrossover(parent2,parent1,two_pts,len(sample_space))

    # probabilistically insert mutations
    if random.random() <= MUTATION_RATE:
      two_pts = random.sample(range(len(sample_space)),2)
      index1 = two_pts[0]
      index2 = two_pts[1]
      crossover1[index1], crossover1[index2] = crossover1[index2], crossover1[index1]
    if random.random() <= MUTATION_RATE:
      two_pts = random.sample(range(len(sample_space)),2)
      index1 = two_pts[0]
      index2 = two_pts[1]
      crossover2[index1], crossover2[index2] = crossover2[index2], crossover2[index1]
 

    populations.append((crossover1,tsp_graph.tourCost(crossover1)))
    populations.append((crossover2,tsp_graph.tourCost(crossover2)))
  # truncation
  populations.sort(key=lambda x: x[1])
  populations = populations[:POP_SIZE]
  best_so_far.append(populations[0][1])
  avg_so_far.append(np.mean([population[1] for population in populations]))

print("Best path was :",populations[0][0],"with cost: ",populations[0][1])
iterations = [i for i in range(MAX_GEN)]
sns.set()
plt.plot(iterations, best_so_far, label='Best so Far')
plt.plot(iterations, avg_so_far, label='Average so Far')
plt.ylabel('Cost of the Graph')
plt.xlabel('Number of Iterations')
plt.legend(['Best so Far','Average so Far'])
plt.show()