# os
import os

# pygame
import pygame
from pygame.locals import *

# gameobjects
from gameobjects.gametime import GameClock

# math
from math import *

# mine
from tiles import *
from pygame_helpers import *
import timer

class map(object):

  def __init__(self, s, w=10, h=10):

    # init vars
    self.w = w
    self.h = h
    self.s = s

    self.xo = 0
    self.yo = 200

    self._TILE_H = 64
    self._TILE_W = 128
    self.BLOCK_W = self.BLOCK_H = 5
    self.SENSITIVITY = 5
    self.MAX_NEGITIVE_DIG = 0

    self._sun_pos = 0
    self._last_sun_pos = 0
    self._sun_event = False

    self._mx = 0
    self._my = 0

    # create gametime clock
    self.clock = GameClock()
    self.clock.start()
    self.time = 0

    # create day/night cycles
    self.day_length = 600.0 # 10 minutes
    self._day_phases = 100.0 # how many times to change the light

    # set up events
    self._events = []





    # load images
    self.load_src()


    # tools
    self.tool = None
    self.tools = { "shovel": (self.src.shovel, self.src.shovel_action) }
    self.tool = "shovel"
    self.tool_image = 0

    # create map
    self.flush_map()


  def __del__(self):
    # stop clock
    self.clock.stop()
    pass


  # container for resources
  class src: pass



  # TILE_W Property
  @property
  def TILE_W(self):
    return self._TILE_W

  @TILE_W.setter
  def TILE_W(self, v):
    self._TILE_W = v
    for x in xrange(self.w-1, -1, -1):
      for y in xrange(0, self.h):
        self.tiles[x][y].TILE_W = v


  # TILE_H Property
  @property
  def TILE_H(self):
    return self._TILE_H

  @TILE_H.setter
  def TILE_H(self, v):
    self._TILE_H = v
    for x in xrange(self.w-1, -1, -1):
      for y in xrange(0, self.h):
        self.tiles[x][y].TILE_H = v


  # sun_pos Property
  @property
  def sun_pos(self):
    return self._sun_pos

  @sun_pos.setter
  def sun_pos(self, v):
    # set sun's pos
    self._sun_pos = v
    if self._sun_pos > 1: self._sun_pos = 0
    if self._sun_pos < 0: self._sun_pos = 1

    # update the whole map
    for x in xrange(self.w-1, -1, -1):
      for y in xrange(0, self.h):
        self.tiles[x][y].update()




  def load_src(self):
    # selector
    self.src.selector = pygame.image.load( os.path.join("src", "selector.png") ).convert_alpha()

    # tools
    shovel = pygame.image.load( os.path.join("src", "shovel.png") ).convert_alpha()
    self.src.shovel = pygame.transform.smoothscale( shovel, (32, 32) )
    self.src.shovel_action = pygame.transform.rotate(self.src.shovel, 20)
    
    # mining images
    self.src.mine = []
    self.src.mine.append( pygame.image.load( os.path.join("src", "mine4.png") ).convert_alpha() )
    self.src.mine.append( pygame.image.load( os.path.join("src", "mine3.png") ).convert_alpha() )
    self.src.mine.append( pygame.image.load( os.path.join("src", "mine2.png") ).convert_alpha() )
    self.src.mine.append( pygame.image.load( os.path.join("src", "mine1.png") ).convert_alpha() )
    self.src.mine.append( pygame.image.load( os.path.join("src", "mine0.png") ).convert_alpha() )


  def flush_map(self):

    # create list of map tiles
    self.tiles = []

    # create empty map
    for x in xrange(0, self.w):
      self.tiles.append([])
      for y in xrange(0, self.h):

        # create new tile, set variables
        self.tiles[-1].append( sand( self, x, y, (255,255,255), self.s ) )
        self.tiles[-1][-1].TILE_H = self.TILE_H
        self.tiles[-1][-1].TILE_W = self.TILE_W

        # create the tiles 'block'
        # a block is the tiles around the current tile
        # blocks are BLOCK_W x BLOCK_H
        # [ ][ ][ ][ ][ ]
        # [ ][1][1][1][ ]
        # [ ][1][X][1][ ]
        # [ ][1][1][1][ ]
        # [ ][ ][ ][ ][ ]


    # create blocks
    for x in xrange(0, self.w):
      self.tiles.append([])
      for y in xrange(0, self.h):

        # create block
        self.tiles[x][y].BLOCK = self.create_block(x, y)

        # lastly, update the tile
        self.tiles[x][y].update()


  # flush, but then randomize heights
  def flush_and_randomize_map(self):

    # create list of map tiles
    self.tiles = []

    # create empty map
    for x in xrange(0, self.w):
      self.tiles.append([])
      for y in xrange(0, self.h):

        # create new tile, set variables
        self.tiles[-1].append( tile( self, x, y, (255,255,255), self.s ) )
        self.tiles[-1][-1].TILE_H = self.TILE_H
        self.tiles[-1][-1].TILE_W = self.TILE_W
        self.tiles[-1][-1].h = generate_random_tile_height()

        # create the tiles 'block'
        # a block is the tiles around the current tile
        # blocks are BLOCK_W x BLOCK_H
        # [ ][ ][ ][ ][ ]
        # [ ][1][1][1][ ]
        # [ ][1][X][1][ ]
        # [ ][1][1][1][ ]
        # [ ][ ][ ][ ][ ]


    # create blocks
    for x in xrange(0, self.w):
      self.tiles.append([])
      for y in xrange(0, self.h):

        # create block
        self.tiles[x][y].BLOCK = self.create_block(x, y)

        # lastly, update the tile
        self.tiles[x][y].update()




  # delete events that are tagged with description d
  def flush_events(self, d=""):
    for c,e in enumerate(self._events):
      if e[3] == d:
          a = list(e)
          a[0] = -1
          self._events[c] = tuple(a)


  def increment_time(self, t=0.1):
    # increments time by 1
    self._last_sun_pos = self.sun_pos
    self.sun_pos += t
    self._sun_event = False

  def clear_map(self, color=None):
    # sets all tiles to color, and resets selection

    # create empty map
    for x in xrange(0, self.w):
      for y in xrange(0, self.h):

        # create new tile, set variables
        if color: self.tiles[x][y].color = color
        self.tiles[x][y].selected = False


  # convert tile coords to screen coords
  def to_screen(self, x, y):
    sx = (y+x)*(self.TILE_W/2)
    sy = (y-x)*(self.TILE_H/2)
    return sx+self.xo, sy+self.yo


  # convert screen coords to 2d tile coords
  def to_2d_tile(self, x, y):
    x, y = (x-self.xo)*1.0, (y-self.yo)*1.0

    # now do math
    tx = (y - x/2)/self.TILE_H
    ty = (y + x/2)/self.TILE_H

    return int( floor(-tx) ), int( floor(ty) )


  # version of to_2d_tile that is more precise and handles 3d
  def to_3d_tile(self, mx, my):

    # create some vars
    measures = []

    # start with a 2d comparison
    x, y = self.to_2d_tile(mx, my+self.TILE_H/8)
    #x, y = self.to_2d_tile(mx, my-self.TILE_H)

    # round these inputs first
    x = int(self.SENSITIVITY * round(float(x)/self.SENSITIVITY))
    y = int(self.SENSITIVITY/2 * round(float(y)/(self.SENSITIVITY/2)))

    # filter values
    if x < 0: x = 0
    if y < 0: y = 0
    if x > self.w-1: x = self.w-1
    if y > self.h-1: y = self.h-1

    # look through all tiles in block around our tile
    tile_block = self.tiles[x][y].BLOCK
    for blk in tile_block:
      
      # convert tile coords to screen coords
      sx = blk.centerx
      sy = blk.centery

      # preform a nearest-neighbor analysis
      dx = sx-mx
      dy = sy-my
      distance = sqrt( dx**2 + dy**2 )
      measures.append(distance)



    # get the 3 lowest numbers in the list, (3 closest tiles)
    closest = min(measures)
    index1 = measures.index( closest )
    measures.remove(closest)

    closest = min(measures)
    index2 = measures.index( closest )
    measures.remove(closest)

    closest = min(measures)
    index3 = measures.index( closest )
    


    # now, pick the tile that is the highest

    # 1 is highest
    if tile_block[index1].h > tile_block[index2].h and tile_block[index1].h > tile_block[index3].h:
      return tile_block[index1].x, tile_block[index1].y

    # 2 is highest
    elif tile_block[index2].h > tile_block[index1].h and tile_block[index2].h > tile_block[index3].h:
      return tile_block[index2].x, tile_block[index2].y
    
    # 3 is highest    
    elif tile_block[index3].h > tile_block[index2].h and tile_block[index3].h > tile_block[index1].h:
      return tile_block[index3].x, tile_block[index3].y

    # all == or something else
    else:
      # just return 1 in this case
      return tile_block[index1].x, tile_block[index1].y


  def in_map(self, x, y):
    # see if the tile (x,y) is on the map

    try:
      _ = self.tiles[x][y]
      return True
    except IndexError:
      return False


  def create_block(self, x, y):
    # create a block for the tile, being BLOCK_W wide and BLOCK_H high, centered on (x, y)

    block = []

    # get block half points
    Bx = self.BLOCK_W/2
    By = self.BLOCK_H/2

    # loop
    for i in xrange(x-Bx, x+Bx+1):
      for j in xrange(y-By, y+By+1):
        
        # check bounds
        if i < 0 or j < 0: continue
        if i > self.w-1 or j > self.h-1: continue
        if i == x and j == y: continue
        
        # add to block list
        tile = self.tiles[i][j]
        block.append( tile )



    return block


  def render(self):

    # update game clock
    for g in self.clock.update():
      self.time = g[1]

      # check scheduled times
      for e in self._events:

        # if event should be run, run it
        if e[0] > 0 and e[0] <= g[1]:
          e[1](*e[2])
          # remove from list
          self._events.remove(e)


    # render all tiles
    for x in xrange(self.w-1, -1, -1):
      for y in xrange(0, self.h):
        
        # check tile exists, and that is subclasses tile
        if self.tiles[x][y] and ( isinstance(self.tiles[x][y], tile) or issubclass(self.tiles[x][y], tile) ):

          # render it
          t = self.tiles[x][y]
          t.render()


    # render current tool
    if self.tool:
      self.s.blit(self.tools[self.tool][self.tool_image], (self._mx, self._my))

    # do daylight stuff
    # update the time
    if not self._sun_event and self._last_sun_pos <= self.sun_pos:
      # schedule an update for later
      self.schedule_time(self.time+self.day_length/self._day_phases, self.increment_time, [1/self._day_phases], "time_shift")
      self._sun_event = True


  def send_motion(self, event):

    # clear the map
    self.clear_map()

    # get mx and my
    self._mx, self._my = event.pos

    # get 3d click
    x, y = self.to_3d_tile(self._mx, self._my)

    if x < 0: x = 0
    if y < 0: y = 0

    # color that tile's block
    # for b in self.tiles[x][y].BLOCK:
    #   b.color = (255, 0, 0)

    # self.tiles[x][y].color = (0, 255, 0)

    self.tiles[x][y].selected = True


  # function called to update a tile's mining status
  def set_tile_mine(self, x, y, state, mouse=1):
    
    # get tile
    tile = self.tiles[x][y]

    # update tile
    tile.update()

    # send an update to tiles block
    tile.update_block()

    # check mouse
    # FIXME: OLD UPDATES ARENT DELETED
    if mouse and not pygame.mouse.get_pressed()[0] and self.to_3d_tile(self._mx, self._my) == (x, y): 
      self.tiles[x][y]._mine_state = None
      return

    elif state == 5:
      # finish the mining
      if self.tool: self.tool_image = 0
      tile._mine_state = None
      tile.h -= 1

      # update tila and tiles block
      tile.update()
      tile.update_block()

    else:
      # set mining state
      tile._mine_state = state

      # move tool
      if self.tool:
        if state%2:
          self.tool_image = 1
        else:
          self.tool_image = 0


  # schedule an event for later
  def schedule_time(self, t, event, a=[], desc=""): self._events.append( (t, event, a, desc) )


  # mine a tile at x, y
  def mine_tile(self, x, y):

    # get our tile
    t = self.tiles[x][y]
    h = self.tiles[x][y].hardness/5.0

    # schedule time for each mining change
    for mine_level in xrange(0, 6):
      self.schedule_time(self.time+mine_level*h, self.set_tile_mine, (x, y, mine_level), "mine_block")


  # send a mousebutton event
  def send_mousebutton(self, event, a):
    # get mx and my
    mx, my = event.pos

    # get 3d click
    x, y = self.to_3d_tile(mx, my)

    # round off
    if x < 0: x = 0
    if y < 0: y = 0


    if a == "down" and event.button == 1:
      # mine that tile
      if self.tiles[x][y].h <= self.MAX_NEGITIVE_DIG: return
      self.mine_tile(x, y)

    elif a == "down" and event.button == 3:
      
      # error checking
      if self.tiles[x][y].h > (self.BLOCK_H+self.BLOCK_H)/2: return

      # update tile
      self.tiles[x][y].h += 1
      # send an update to tiles block
      self.tiles[x][y].update()
      self.tiles[x][y].update_block()

    elif a == "up":
      # reset tool
      self.flush_events("mine_block")
      self.tiles[x][y]._mine_state = None
      if self.tool: self.tool_image = 0


  # center the map on the window
  def center_map(self, (w, h)):
    self.xo = w/2-(self.w*self.TILE_W/2)
    self.yo = h/2