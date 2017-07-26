#!/usr/bin/env python
import libtcodpy as libtcod
from game_objects import BaseObject, Map, Tile, Room

# Globals
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45

ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

# Configure libtcod
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Roguelike Game', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
libtcod.sys_set_fps(LIMIT_FPS)

# Handle user keypresses
def handle_keys():

    # Fullscreen and exit
    key = libtcod.console_check_for_keypress()
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(game_map, 0, -1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(game_map, 0, 1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(game_map, -1, 0)

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(game_map, 1, 0)

def render_all():
    #draw all objects in the list
    for obj in objects:
        obj.draw()

    game_map.draw()

    #blit the contents of "con" to the root console and present it
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

player = BaseObject(con, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, '@')
objects = [player]

game_map = Map(con, MAP_WIDTH, MAP_HEIGHT)

rooms = []
for r in range(MAX_ROOMS):
    # Generates the rooms and hallways
    # random width and height
    w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
    # random position without going out of the boundaries of the map
    x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
    y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

    room = Room(x, y, w, h)
    failed = False
    for other_room in rooms:
        if room.intersect(other_room):
            failed = True
            break

    if not failed:
        #this means there are no intersections, so this room is valid
        #"paint" it to the map's tiles
            game_map.create_room(room)

            #center coordinates of new room, will be useful later
            (new_x, new_y) = room.center()

            num_rooms = len(rooms)
            if num_rooms == 0:
                #this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # this isn't the first room
                #connect it to the previous room with a tunnel

                #center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms-1].center()

                #draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    #first move horizontally, then vertically
                    game_map.create_h_tunnel(prev_x, new_x, prev_y)
                    game_map.create_v_tunnel(prev_y, new_y, new_x)
                else:
                    #first move vertically, then horizontally
                    game_map.create_v_tunnel(prev_y, new_y, prev_x)
                    game_map.create_h_tunnel(prev_x, new_x, new_y)

            #finally, append the new room to the list
            rooms.append(room)


while not libtcod.console_is_window_closed():

    render_all()

    #erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear()

    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
