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

traversalPath = []
visited = {}

s = Stack()
while len(visited) < len(roomGraph):
    room = player.currentRoom.id
    exits = player.currentRoom.getExits()
    if room not in visited:
        visited[room] = {e: '?' for e in exits}
    
    unexplored = [d for d in visited[room] if visited[room][d] == '?']

    if len(unexplored) > 0:
        curr_exit = unexplored[0]
        player.travel(curr_exit)
        traversalPath.append(curr_exit)
        next_room = player.currentRoom.id
        visited[room][curr_exit] = next_room
        if next_room not in visited:
            next_room_exits = player.currentRoom.getExits()
            visited[next_room] = {e: '?' for e in next_room_exits}
        opposite = getOpposite(curr_exit)
        visited[next_room][opposite] = room
        s.push(opposite) #keep track of reverse direction 
    
    #if no more unexplored exit, go back
    else: 
        prev = s.pop()
        player.travel(prev)
        traversalPath.append(prev)

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
