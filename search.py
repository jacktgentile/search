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
#import pdb; pdb.set_trace()

#compute and return the Manhattan distance between two positions
def manhattan(pos1, pos2):
    xdist = abs(pos1[0]-pos2[0]);
    ydist = abs(pos1[1]-pos2[1]);
    return xdist + ydist

def min_manhattan(pos, objective_list):
    min = float("inf")
    for objective in objective_list:
        curr_man = manhattan(pos, objective)
        if curr_man < min:
            min = curr_man
    return min


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)

# return path, num_states_explored
def bfs(maze):
    current = maze.getStart()
    frontier = deque([current])
    backtrack = {current : (-1, -1)}

    if len(maze.getObjectives()) == 1:
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
    else:
        objective_list = maze.getObjectives()
        path = []
        num_states_explored = 0
        while len(objective_list) != 0:
            while len(frontier) != 0:
                current = frontier.popleft()
                if current in objective_list:
                    objective_list.remove(current)
                    break
                neighbors = maze.getNeighbors(current[0],current[1])
                for neighbor in neighbors:
                    if neighbor not in backtrack:
                        backtrack[neighbor] = current
                        num_states_explored += 1
                        frontier.append(neighbor)
            offset = len(path)
            current_obj = current
            while current != (-1,-1):
                path.insert(offset,current)
                current = backtrack[current]
            path.pop()
            current = current_obj
            frontier = deque([current])
            backtrack.clear()
            backtrack[current] = (-1,-1)
        path.append(current)
        return path, num_states_explored


# return path, num_states_explored
def dfs(maze):
    frontier = [maze.getStart()]
    backtrack = {maze.getStart() : (-1, -1)}

    if len(maze.getObjectives()) == 1:
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
    else:
        objective_list = maze.getObjectives()
        path = []
        num_states_explored = 0
        while len(objective_list) != 0:
            while len(frontier) != 0:
                current = frontier.pop()
                if current in objective_list:
                    objective_list.remove(current)
                    break
                neighbors = maze.getNeighbors(current[0],current[1])
                for neighbor in neighbors:
                    if neighbor not in backtrack:
                        num_states_explored += 1
                        backtrack[neighbor] = current
                        frontier.append(neighbor)
            current_obj = current
            offset = len(path)
            while current != (-1, -1):
                # print("current:" + str(current))
                path.insert(offset, current)
                current = backtrack[current]
            path.pop()
            current = current_obj
            frontier = [current]
            backtrack.clear()
            backtrack = {current : (-1, -1)}
        path.append(current)
        return path, num_states_explored

                


# return path, num_states_explored
def astar(maze):
    if len(maze.getObjectives()) == 1:
        #use heapq, make frontier a priority queue based on estimated path cost
        #stores tuple (g+h, [position])
        frontier = []
        #backtrack is dictionary, stores position, previous position, and distance along path
        current = maze.getStart()
        backtrack = {current : ((-1,-1),0)}
        #inserts tuple in frontier
        current_tup = (manhattan(current,maze.getObjectives()[0]), current)
        heapq.heappush(frontier, (manhattan(current,maze.getObjectives()[0]), current))
        goal = maze.getObjectives()[0]
        while len(frontier) != 0:
            if maze.isObjective(current_tup[1][0], current_tup[1][1]):
                break
            current_tup = heapq.heappop(frontier)
            current_pos = current_tup[1]
            neighbors = maze.getNeighbors(current_pos[0], current_pos[1])
            for neighbor in neighbors:
                if neighbor not in backtrack:       # make sure only add unexplored nodes
                    backtrack[neighbor] = (current_pos, backtrack[current_pos][1]+1)
                    heapq.heappush(frontier, (backtrack[neighbor][1] + manhattan(neighbor,goal) ,neighbor))
        path = []
        current = current_tup[1]
        while current != (-1, -1):
            path.append(current)
            current = backtrack[current][0]
        return path[::-1], len(backtrack)
    #end if
    else: # multi objective
        objective_list = maze.getObjectives()
        num_states_explored = 0
        frontier = []   # maintains priority queue of tuples (float for g+h, tuple for pos)
        current = maze.getStart()
        backtrack = {current : ((-1,-1), 0)}
        current_tup = (min_manhattan(current, objective_list), current)
        heapq.heappush(frontier, (min_manhattan(current, objective_list), current))
        path = []
        while len(objective_list) != 0:
            # print ("frontier len: " + str(len(frontier)))
            while len(frontier) != 0:
                current_tup = heapq.heappop(frontier)
                current_pos = current_tup[1]
                if current_pos in objective_list:
                    print("found obj: " + str(current_pos))
                    objective_list.remove(current_pos)
                    break
                neighbors = maze.getNeighbors(current_pos[0], current_pos[1])
                for neighbor in neighbors:
                    if neighbor not in backtrack:
                        num_states_explored += 1
                        backtrack[neighbor] = (current_pos, backtrack[current_pos][1] + 1)
                        # print("adding " + str(neighbor) + " to frontier")
                        heapq.heappush(frontier, (backtrack[neighbor][1] + min_manhattan(neighbor, objective_list), neighbor))

            # out of inner while loop now
            offset = len(path)
            ct = current_tup
            current = current_tup[1]
            while current != (-1, -1):
                print("inserting " + str(current) + " into path")
                path.insert(offset, current)
                current = backtrack[current][0]
            print("popping from path of len " + str(len(path)))
            path.pop()
            # current_tup shouldn't have changed through while loop
            # but i'll do it anyway
            current_tup = ct
            frontier = [(manhattan(current,maze.getObjectives()[0]), current)]
            # print("after new set, frontier len is now " + str(len(frontier)))
            backtrack.clear()
            backtrack = {current_tup[1] : ((-1,-1), 0)}
        path.append(current_tup[1])
        return path, num_states_explored





# return path, num_states_explored
def greedy(maze):
    #use heapq, make frontier a priority queue based on heuristic function h
    #stores tuple (h, [position])
    frontier = []
    current = maze.getStart()
    #backtrack is dictionary, stores position, previous position, and distance along path
    backtrack = {current : (-1,-1)}
    #inserts tuple in frontier
    current_tup = (manhattan(current,goal), current)
    heapq.heappush(frontier, (manhattan(current,goal), current));

    if len(maze.getObjectives()) == 1:
        goal = maze.getObjectives()[0]
        while len(frontier) != 0:
            if maze.isObjective(current_tup[1][0], current_tup[1][1]):
                break
            current_tup = heapq.heappop(frontier)
            current_pos = current_tup[1]
            neighbors = maze.getNeighbors(current_pos[0], current_pos[1])
            for neighbor in neighbors:
                if neighbor not in backtrack:       # make sure only add unexplored nodes
                    backtrack[neighbor] = current_pos
                    heapq.heappush(frontier, (manhattan(neighbor,goal) ,neighbor))
        path = []
        current = current_tup[1]
        while current != (-1, -1):
            path.append(current)
            current = backtrack[current]
        return path[::-1], len(backtrack)
    #end if
    return [],0
