#!/usr/bin/env python
import libtcodpy as libtcod
from game_objects import BaseObject, Map, Tile, Room

# Globals
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

MAP_WIDTH = 80
MAP_HEIGHT = 45

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
npc = BaseObject(con, SCREEN_WIDTH//2 - 5, SCREEN_HEIGHT//2, '@', libtcod.yellow)
objects = [npc, player]

game_map = Map(con, MAP_WIDTH, MAP_HEIGHT)

#create two rooms
room1 = Room(20, 15, 10, 15)
room2 = Room(50, 15, 10, 15)

game_map.create_room(room1)
game_map.create_room(room2)
game_map.create_h_tunnel(25, 55, 23)

player.x = 25
player.y = 23

while not libtcod.console_is_window_closed():

    render_all()

    #erase all objects at their old locations, before they move
    for obj in objects:
        obj.clear()

    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
