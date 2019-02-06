# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 19:23:53 2019

@author: sualeh

This program prints complete state space graph and the search tree of the ‘Frog Problem’.
Also, counts the number of states while generating them

Encoding:
Each state of the game will be represented in the form of a 7-char string
1 represents green frog
2 represents brown frog

Root Node: 1110222
Goal Node: 2220111

"""

import queue

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


    def __init__(self):
        self.counter = 0
        self.root = Node(self.INITIAL_STATE)

    def isGreenFrog(self,frog):
        return frog is '1'
    def isBrownFrog(self,frog):
        return frog is '2'

    def hasNoFrog(self,frog):
        return frog is '0'

    def getStates(self):
        unexplored_nodes = queue.Queue()
        unexplored_nodes.put(self.root)
        ctr = 0
        while True:
            latest_node = unexplored_nodes.get()
            if latest_node.state is self.FINAL_STATE:
                exit()

            else:
                frogs = latest_node.state
                print("Iteration # " + str(ctr))
                print(str(self.root))
                ctr += 1
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

                    elif self.isBrownFrog(frogs[i]) and i > 0:
                        # Jump to next one
                        if self.hasNoFrog(frogs[i-1]):
                            # .. 0 2 .. --> ... 2 0 ..
                            new_state = list(frogs)
                            new_state[i] = '0'
                            new_state[i-1] = '2'
                            new_state = ''.join(new_state)

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

def main():
    tree = FrogGameSearchTree()
    tree.getStates()

if __name__ == '__main__':
    main()
