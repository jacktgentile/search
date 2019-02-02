# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

from collections import deque
import heapq

#compute and return the Manhattan distance between two positions
def manhattan(pos1, pos2):
    xdist = abs(pos1[0]-pos2[0]);
    ydist = abs(pos1[1]-pos2[1]);
    return xdist + ydist

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)

# return path, num_states_explored
def bfs(maze):
    num_states_explored = 0
    frontier = deque([maze.getStart()])
    backtrack = {maze.getStart() : (-1, -1)}

    current = maze.getStart()
    while len(frontier) != 0:
        if maze.isObjective(current[0], current[1]):
            break
        current = frontier.popleft()
        neighbors = maze.getNeighbors(current[0], current[1])
        for neighbor in neighbors:
            if neighbor not in backtrack:       # make sure only add unexplored nodes
                backtrack[neighbor] = current
                frontier.append(neighbor)

    path = []
    while current != (-1, -1):
        path.append(current)
        current = backtrack[current]

    return path[::-1], len(backtrack)

# return path, num_states_explored
def dfs(maze):
    frontier = [maze.getStart()]
    backtrack = {maze.getStart() : (-1, -1)}

    current = maze.getStart()
    while len(frontier) != 0:
        if maze.isObjective(current[0], current[1]):
            break
        current = frontier.pop()
        neighbors = maze.getNeighbors(current[0], current[1])
        for neighbor in neighbors:
            if neighbor not in backtrack:       # make sure only add unexplored nodes
                backtrack[neighbor] = current
                frontier.append(neighbor)

    path = []
    while current != (-1, -1):
        path.append(current)
        current = backtrack[current]

    return path[::-1], len(backtrack)

# return path, num_states_explored
def greedy(maze):
    #use heapq, make frontier a priority queue based on estimated path cost
    #stores tuple (g+h, [position])
    frontier = []
    #backtrack is dictionary, stores position, previous position, and distance along path
    current = maze.getStart()
    backtrack = {current : ((-1,-1),0)}
    #inserts tuple in frontier
    current_tup = (manhattan(current,maze.getObjectives()[0]), current)
    heapq.heappush(frontier, (manhattan(current,maze.getObjectives()[0]), current));

    while len(frontier) != 0:
        if maze.isObjective(current_tup[1][0], current_tup[1][1]):
            break
        current_tup = heapq.heappop(frontier)
        neighbors = maze.getNeighbors(current_tup[1][0], current_tup[1][1])
        for neighbor in neighbors:
            if neighbor not in backtrack:       # make sure only add unexplored nodes
                backtrack[neighbor] = (current_tup[1],backtrack[current_tup[1]][1]+1)
                heapq.heappush(frontier, (backtrack[neighbor][1]+manhattan(neighbor,maze.getObjectives()[0]),neighbor))

    path = []
    current = current_tup[1]
    while current != (-1, -1):
        path.append(current)
        current = backtrack[current][0]

    return path[::-1], len(backtrack)


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0
