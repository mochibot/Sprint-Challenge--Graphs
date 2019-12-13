from room import Room
from player import Player
from world import World
from roomGraph import roomGraph
from util import Stack, Queue

import random

# Load world
world = World()


world.loadGraph(roomGraph)
world.printRooms()
player = Player("Name", world.startingRoom)

# FILL THIS IN

def getOpposite(d):
    '''
    return the direction opposite of the input direction
    '''
    obj = {'w': 'e', 'e': 'w', 's': 'n', 'n': 's'}
    return obj[d]

def bfs_mod(start):
    '''
    find the shortest path from start to closest room with 
    '''
    visited_room = set()
    q = Queue()
    q.enqueue([start])

    while q.size() > 0:
        path = q.dequeue()
        v = path[-1]
        if v not in visited_room:
            for e in visited[v]:
                if visited[v][e] == '?':
                    return path
            visited_room.add(v)

            for d in visited[v]:
                neighbor = visited[v][d]
                new_path = path.copy()
                new_path.append(neighbor)
                q.enqueue(new_path)
    return None

def getPath(path):
    '''
    reconstruct the directions based on the input path of rooms
    '''
    route = []
    for room in path:
        for d in visited[path[0]]:
            if room == visited[path[0]][d]:
                route.append(d)
    return route

traversalPath = []
visited = {}

while len(visited) < len(roomGraph):    #run until 500 rooms have been visited
    room = player.currentRoom.id
    exits = player.currentRoom.getExits()

    #if room no visited, add to visited and set all direction to '?'
    if room not in visited:
        visited[room] = {e: '?' for e in exits}

    #get all exits of the room that have not been explored yet     
    unexplored = [d for d in visited[room] if visited[room][d] == '?']
    
    #if there are exits that have not been explored
    if len(unexplored) > 0:
        # just pick the first room for now, move the player there, and add exit to traversalPath
        curr_exit = unexplored[0]   
        player.travel(curr_exit) 
        traversalPath.append(curr_exit) 
        next_room = player.currentRoom.id
        #update visited {} for the old room
        visited[room][curr_exit] = next_room

        if next_room not in visited:
            next_room_exits = player.currentRoom.getExits()
            visited[next_room] = {e: '?' for e in next_room_exits}

        #update visited {} for the new room (direction is opposite)
        opposite = getOpposite(curr_exit)   
        visited[next_room][opposite] = room
    
    #if all exits have been explored, use BFS to find the a room that has unexplored exit ('?')
    else:
        new_path = bfs_mod(room)   
        
        if new_path is not None:
            directions = getPath(new_path)  #get the path to the room
            for direction in directions:
                traversalPath.append(direction)  
                player.travel(direction)        
    
print(traversalPath)

# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
