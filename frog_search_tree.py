# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:23:53 2019

@author: sualeh

This program prints complete state space graph and the search tree of the ‘Frog Problem’.
Goal Node: 2220111
Also, counts the number of states while generating them

Encoding:
Each state of the game will be represented in the form of a 7-char string
1 represents green frog
2 represents brown frog

Root Node: 1110222

"""

import queue
import networkx as nx
import matplotlib.pyplot as plt


class Node():
    def __init__(self,state):
        self.children = []
        self.state = state
    def __str__(self, level=0):
            ret = "\t"*level+repr(self.state)+"\n"
            for child in self.children:
                ret += child.__str__(level+1)
            return ret

    def __repr__(self):
        return '<tree node representation>'




class FrogGameSearchTree():
    INITIAL_STATE = '1110222'
    FINAL_STATE = '2220111'

    # Returns string representation of the Frog Search Tree
    def __str__(self):
        return str(self.root)

    # Constructor
    def __init__(self):
        self.G = nx.DiGraph()
        self.root = Node(self.INITIAL_STATE)

    '''
    Is the frog at that position green?
    '''
    def isGreenFrog(self,frog):
        return frog is '1'
    '''
    Is the frog at that position brown?
    '''
    def isBrownFrog(self,frog):
        return frog is '2'

    '''
    Is there no frog at that position?
    '''
    def hasNoFrog(self,frog):
        return frog is '0'

    '''
    Constructs the search tree of the graph and calls add_edge
    to create the search graph
    '''
    def getStates(self):

        unexplored_nodes = queue.Queue()
        unexplored_nodes.put(self.root)

        # Add starting Node
        self.G.add_node(self.root.state)

        while True:
            latest_node = unexplored_nodes.get()

            if latest_node.state is self.FINAL_STATE:
                exit()

            else:
                frogs = latest_node.state


                for i in range(len(frogs)):

                    if self.isGreenFrog(frogs[i]) and i < len(frogs) - 1:

                        # Jump to next one
                        if self.hasNoFrog(frogs[i+1]):
                            # .. 1 0 ... --> .. 0 1 ...
                            new_state = list(frogs)

                            new_state[i] = '0'
                            new_state[i+1] = '1'
                            new_state = ''.join(new_state)

                            # add children
                            new_node = Node(new_state)
                            latest_node.children.append(new_node)
                            unexplored_nodes.put(new_node)

                            self.add_edge(frogs,new_state)



                        # Jump over the next one
                        if i < len(frogs) - 2 and not self.hasNoFrog(frogs[i+1]) and self.hasNoFrog(frogs[i+2]):
                            new_state = list(frogs)
                            new_state[i] = '0'
                            new_state[i+2] = '1'
                            new_state = ''.join(new_state)
                            # add children
                            new_node = Node(new_state)
                            latest_node.children.append(new_node)
                            unexplored_nodes.put(new_node)

                            self.add_edge(frogs,new_state)


                    elif self.isBrownFrog(frogs[i]) and i > 0:
                        # Jump to next one

                        if self.hasNoFrog(frogs[i-1]):
                            # .. 0 2 .. --> ... 2 0 ..
                            new_state = list(frogs)
                            new_state[i] = '0'
                            new_state[i-1] = '2'
                            new_state = ''.join(new_state)


                            # add children
                            new_node = Node(new_state)
                            latest_node.children.append(new_node)
                            unexplored_nodes.put(new_node)

                            self.add_edge(frogs,new_state)


                        # Jump over the next one
                        if i > 1 and not self.hasNoFrog(frogs[i-1]) and self.hasNoFrog(frogs[i-2]):
                            new_state = list(frogs)
                            new_state[i] = '0'
                            new_state[i-2] = '2'
                            new_state = ''.join(new_state)

                            # add children
                            new_node = Node(new_state)
                            latest_node.children.append(new_node)
                            unexplored_nodes.put(new_node)

                            self.add_edge(frogs,new_state)


            if unexplored_nodes.empty():
                print("Bye\n")
                return

    '''Creates an edge between old_state and new_state and creates a new node
       if necessary '''
    def add_edge(self,old_state,new_state):

        if not self.G.has_edge(old_state,new_state):
            self.G.add_edge(old_state,new_state)



def main():
    tree = FrogGameSearchTree()
    tree.getStates()
    print('Search Tree of Frog Problem\n' + '-'*75 + '\n')
    print(tree)
    print('Number of States in Frog Problem: {} \n'.format( len(tree.G) ))
    nx.draw_spectral(tree.G,with_labels = True,node_size=130,font_size=10,node_color=range(72),cmap=plt.cm.Pastel2,arrowsize=7,alpha=0.7,style='dashed')
    plt.savefig("simple_path.png") # save as png
    plt.show() # display

if __name__ == '__main__':
    main()
