import libtcodpy as libtcod

class BaseObject:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.
    def __init__(self, console, x, y, char, color=libtcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.con = console

    def move(self, game_map, dx, dy):
        if not game_map.is_blocked(self.x + dx, self.y + dy):
            #move by the given amount
            self.x += dx
            self.y += dy

    def draw(self):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(self.con, self.color)
        libtcod.console_put_char(self.con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(self.con, self.x, self.y, ' ', libtcod.BKGND_NONE)
