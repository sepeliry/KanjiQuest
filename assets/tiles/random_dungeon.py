# -*- coding: utf-8 -*-
"""
@original author: Jani Vuolle (ja.vuolle@gmail.com)

"""

from pprint import pprint
from random import randint
import math

map_width = 50
map_height = 50
min_room_size = 3
max_room_size = 10
max_room_count = 20
levels = []

WALL = [70, 2]
FLOOR = [145, 10]
STAIR_DOWN = [13, 1]
STAIR_UP = [12, 1]

class Room:
    # these values hold grid coordinates for each corner of the room
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0

    # width and height of room in terms of grid
    w = 0
    h = 0

    # center point of the room
    center = [0,0]

    def new_room(self, x_pos, y_pos, width, height): 
        self.x1 = x_pos
        self.x2 = x_pos + width
        self.y1 = y_pos
        self.y2 = y_pos + height
        self.w = width
        self.h = height
        self.center = [math.ceil((self.x1 + self.x2)/ 2),math.ceil((self.y1 + self.y2) / 2)]
    

    # return true if this room intersects provided room
    def intersects(self, other_room):
        return (self.x1 <= other_room.x2 and self.x2 >= other_room.x1 and
            self.y1 <= other_room.y2 and other_room.y2 >= other_room.y1)

def generate_levels(level_count):   
    i = 0
    current_rooms = []
    current_stairs_up = []
    while (i < level_count):
        # create empty map
        current_map = [[WALL for x in range(map_width)] for x in range(map_height)]
        if (i > 0):
            place_stairs_up(current_map,current_stairs_up)
            
        # place some rooms
        current_rooms = place_rooms(current_map, current_stairs_up)
        # place stairs down and get their positions for next level to place stairs up
        current_stairs_up = []
        current_stairs_up = place_stairs_down(current_map,current_rooms)

        levels.append(current_map)
        current_rooms = []

        i += 1

def place_rooms(level_map, stairs_up):
    i = 0
    current_tries = 0
    current_room_center = [0][0]

    rooms = []

    if (len(stairs_up) > 1):
        for stair in stairs_up:
            w = min_room_size + randint(0, max_room_size-min_room_size)
            h = min_room_size + randint(0, max_room_size-min_room_size)
            x = randint(max(0,stair[0]-w), stair[0])
            if (x < 0):
                x = 0
            if (x+w >= map_width):
                x = map_width-w-1
                
            y = randint(max(0,stair[1]-h), stair[1])
            if (y < 0):
                y = 0
            if (y+h >= map_height):
                y = map_height-h-1
            
            # create room with randomized values
            tmp_room = Room()
            tmp_room.new_room(x,y,w,h)

            if(len(rooms) > 0):
                last_room_center = rooms[len(rooms)-1].center
                if (randint(1,2) == 1):
                    hCorridor(level_map,last_room_center[0], tmp_room.center[0], last_room_center[1])
                    vCorridor(level_map,last_room_center[1], tmp_room.center[1], tmp_room.center[0])
                    
                else:
                    vCorridor(level_map,last_room_center[1], tmp_room.center[1], last_room_center[0])
                    hCorridor(level_map,last_room_center[0], tmp_room.center[0], tmp_room.center[1])         

            print (str(tmp_room.x2) + " " + str(tmp_room.y2))
            fill_map_room(level_map,tmp_room.x1,tmp_room.x2,tmp_room.y1,tmp_room.y2)
            rooms.append(tmp_room)
            i += 1
        
        place_stairs_up(level_map,stairs_up) 
    
    while (i < max_room_count):
        w = min_room_size + randint(0, max_room_size-min_room_size)
        h = min_room_size + randint(0, max_room_size-min_room_size)
        x = randint(1, map_width - w - 1)
        y = randint(1, map_height - h - 1)

        # create room with randomized values
        tmp_room = Room()
        tmp_room.new_room(x,y,w,h)

        failed = False
        for otherRoom in rooms:
            if tmp_room.intersects(otherRoom):
                failed = True
                current_tries += 1
        
        if (failed == False): 

            if(len(rooms) > 0):
                last_room_center = rooms[len(rooms)-1].center
                if (randint(1,2) == 1):
                    hCorridor(level_map,last_room_center[0], tmp_room.center[0], last_room_center[1])
                    vCorridor(level_map,last_room_center[1], tmp_room.center[1], tmp_room.center[0])
                    
                else:
                    vCorridor(level_map,last_room_center[1], tmp_room.center[1], last_room_center[0])
                    hCorridor(level_map,last_room_center[0], tmp_room.center[0], tmp_room.center[1])         

            fill_map_room(level_map,tmp_room.x1,tmp_room.x2,tmp_room.y1,tmp_room.y2)
            
            rooms.append(tmp_room)
            i += 1
            
        if(current_tries > 100):
            i += 1
            current_tries = 0


    return rooms

def place_stairs_up(level_map, stairs):
     for stair in stairs:
        level_map[stair[0]][stair[1]] = STAIR_UP

def place_stairs_down(level_map, rooms):
    stair_count = 3
    stair_in_room = []
    stair_positions = []
    i = 0
    while (i < stair_count):
        stair_in_room.append(randint(0, len(rooms)-1))
        i += 1
        
    #generate some randomized position for stair
    for stair in stair_in_room:
        stair_x = randint(rooms[stair].x1, rooms[stair].x2)
        stair_y = randint(rooms[stair].y1, rooms[stair].y2)
        level_map[stair_x][stair_y] = STAIR_DOWN
        stair_positions.append([stair_x, stair_y])
    
    print (stair_in_room)
    return stair_positions

def hCorridor(level_map, x1, x2, y):
    x = min(x1, x2)
    while (x < ((max(x1, x2)))):
        if(level_map[x][y] == WALL):
            level_map[x][y] = FLOOR

        x += 1
    

def vCorridor(level_map, y1, y2, x):
    y = min(y1, y2)
    while (y < ((max(y1, y2)))):
        if(level_map[x][y] == WALL):
            level_map[x][y] = FLOOR

        y += 1
        
def fill_map_room(level_map, x1,x2,y1,y2):
    x = min(x1, x2)
    y = min(y1, y2)
    while(x <= ((max(x1, x2)))):
        while(y <= ((max(y1, y2)))):
            level_map[x][y] = FLOOR
            y += 1
        y = min(y1, y2)
        x += 1      

#stair = []
#rooms = place_rooms(stair)

#place_stairs_down(rooms)

generate_levels(5)

import gentiles as gt
import pygame as pg

FPS = 60
mainloop = True
clock = pg.time.Clock()
TILE_SIZE = 32

dungeon_surface = pg.Surface((1024,768))

current_pos_x = 0
current_pos_y = 0
current_level = 0

direction = (0,0)

while mainloop:

    events = pg.event.get()
    for event in events:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                mainloop = False
            if event.key == pg.K_LEFT:
                if current_pos_x > 0:
                    direction = (-1,0)
            if event.key == pg.K_RIGHT:
                if current_pos_x+32 < map_width:
                    direction = (1,0)                   
            if event.key == pg.K_UP:
                if current_pos_y > 0:
                    direction = (0,-1)
            if event.key == pg.K_DOWN:
                if current_pos_y+24 < map_height:
                    direction = (0,1)

            if event.key == pg.K_1:
                if (current_level < len(levels)-1):
                    current_level += 1
            if event.key == pg.K_2:
                if (current_level > 0):
                    current_level -= 1

        if event.type == pg.KEYUP:
            direction = (0, 0)

    current_pos_x += direction[0]
    current_pos_y += direction[1]

    if current_pos_x+32 >= map_width:
        current_pos_x = map_width-32
    if current_pos_y+24 >= map_height:
        current_pos_y = map_height-24
    if current_pos_x < 0:
        current_pos_x = 0
    if current_pos_y < 0:
        current_pos_y = 0    
        
    i = 0
    j = 0
    
    while (i+current_pos_x < map_width):
        while (j+current_pos_y < map_height):
            kanji_id = levels[current_level][i+current_pos_x][j+current_pos_y][0]
            color_id = levels[current_level][i+current_pos_x][j+current_pos_y][1]
            dungeon_surface.blit(gt.piirtopinta, (i*TILE_SIZE,j*TILE_SIZE),
            (color_id*TILE_SIZE,kanji_id*TILE_SIZE,i*TILE_SIZE+TILE_SIZE,kanji_id*TILE_SIZE+TILE_SIZE) )
            j+=1
        i+=1
        j=0



    gt.screen.blit(dungeon_surface, (0,0))

    milliseconds = clock.tick(FPS) # do not go faster than this frame rate
    pg.display.set_caption("Frame rate: {:0.2f} frames per second.".format(clock.get_fps()))
    pg.display.update()
    pg.display.flip()

#pg.image.save(gt.piirtopinta, 'kanji_tiles.png')

pg.display.quit()

