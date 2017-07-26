import libtcodpy as libtcod

class Room:
    #a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return (center_x, center_y)

    def intersect(self, other):
        #returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Map:
    color_dark_wall = libtcod.Color(0, 0, 100)
    color_dark_ground = libtcod.Color(50, 50, 150)

    def __init__(self, console, width, height):
        self.con = console
        self.width = width
        self.height = height
        #fill map with "blocked" tiles
        self.map = [[ Tile(True)
            for y in range(self.height) ]
                for x in range(self.width) ]

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                wall = self.map[x][y].block_sight
                if wall:
                    libtcod.console_set_char_background(self.con, x, y, self.color_dark_wall, libtcod.BKGND_SET )
                else:
                    libtcod.console_set_char_background(self.con, x, y, self.color_dark_ground, libtcod.BKGND_SET )

    def set_blocked(self, x, y, blocked=True, block_sight=True):
        self.map[x][y].blocked = blocked
        self.map[x][y].block_sight = block_sight

    def is_blocked(self, x, y):
        try:
            return self.map[x][y].blocked
        except:
            return True

    def create_room(self, room):
        #go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.set_blocked(x, y, False, False)

    def create_h_tunnel(self, x1, x2, y):
        # create a horizontal tunnel
        for x in range(min(x1, x2), max(x1, x2) +1):
            self.set_blocked(x, y, False, False)

    def create_v_tunnel(self, y1, y2, x):
        # create a vertical tunnel
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.set_blocked(x, y, False, False)
