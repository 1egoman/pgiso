# pygame
import pygame
from pygame.locals import *

# math
from math import *

# random
import random

class tile(object):

  TILE_H = 32
  TILE_W = 64
  BLOCK = None

  OUTLINE_COLOR = (0, 0, 0)
  SELECTION_COLOR = (120, 120, 120)

  def __init__(self, p, x, y, color, s):

    # set color
    self.x = x
    self.parent = p
    self.y = y
    self.color = color
    self.s = s
    self.h = 0

    self.centerx = 0
    self.centery = 0
    self.pts = []

    self.hardness = 0.5
    self._mine_state = None

    self._SHADE = 1

    self.selected = False

    # self.font = pygame.font.SysFont("monospace", 12)

  # calculates the amout to shade a tile
  def calculate_shade(self, s):
    return 1 - abs( self.parent.sun_pos - s )


  # update tiles in block around our tile
  def update_block(self):
    
    # loop through block
    for t in self.BLOCK:
      t.update()

  def update(self):
    # update tile

    #               /\   <------ 1st
    #              /  \
    # 4th ____\   /    \   /_____ 2nd
    #         /   \    /   \
    #              \  /
    #               \/  <----- 3rd


    # do the sloping of tiles
    self.ax=self.bx=self.cx=self.dx=0
    self.ay=self.by=self.cy=self.dy=0
    w=s=e=None
    h2 = self.TILE_H/2

    # get the tiles around our tile (from block)
    for t in self.BLOCK:

      # west
      if not w and t.x == self.x and t.y == self.y-1: w = t

      # south
      if not s and t.x == self.x+1 and t.y == self.y-1: s = t

      # east
      if not e and t.x == self.x+1 and t.y == self.y: e = t


    # reset shading
    if (not self.ay and not self.ax) and (not self.by and not self.bx) and \
    (not self.cy and not self.cx) and (not self.dy and not self.dx):
      if self.h:
        self._SHADE = 1
      else:
        self._SHADE = .9

    # slope northern sides
    if s and s.h > self.h:
      self.ay -= h2*(s.h - self.h)
      self._SHADE = self.calculate_shade(0.5)

    # slope western sides
    elif w and w.h > self.h:
      self.ay -= h2*(w.h - self.h)
      self.dy -= h2*(w.h - self.h)
      self._SHADE = self.calculate_shade(0.8)

    # slope eastern sides
    elif e and e.h > self.h:
      self.ay -= h2*(e.h - self.h)
      self.by -= h2*(e.h - self.h)
      self._SHADE = self.calculate_shade(0.2)


    # slope northern, modified
    if s and s.h > self.h and w and w.h > self.h and e and e.h > self.h:
      self.by -= h2*(e.h - self.h)
      self.dy -= h2*(w.h - self.h)

    # slope east and west, modified
    elif w and w.h > self.h and e and e.h > self.h:
      self.by -= h2*(e.h - self.h)

    # slope east and west, modified
    elif s and s.h > self.h and e and e.h > self.h:
      self.by -= h2*(e.h - self.h)


    # another slope east and west
    elif w and w.h > self.h and s and s.h > self.h:
      self.dy -= h2*(w.h - self.h)


    # shading logic
    if not self._SHADE:
      if w and not w._SHADE:
        self._SHADE == w._SHADE

      elif e and not e._SHADE:
        self._SHADE == e._SHADE




  def render(self):
    # draw tile

    # convert to screen coords
    sx, sy = self.parent.to_screen(self.x, self.y)

    # calculate a list of points to render
    h = (-self.TILE_H/2)*self.h
    self.pts = [
      
      # topmost point
      (self.ax+sx+self.TILE_W/2, self.ay+sy+h),

      # rightmost point
      (self.bx+sx+self.TILE_W, self.by+sy+self.TILE_H/2+h),
      
      # bottommost point
      (self.cx+sx+self.TILE_W/2, self.cy+sy+self.TILE_H+h),
      
      # leftmost point
      (self.dx+sx, self.dy+sy+self.TILE_H/2+h)
    ]

    # calculate the center of the tile
    th = self.pts[0][1] - self.pts[2][1]
    self.centerx = self.pts[3][0]+self.TILE_W/2+self.bx/2
    self.centery = self.pts[0][1]+self.TILE_H/2-self.ay/2



    # draw tile
    c = (self.color[0]*self._SHADE, self.color[1]*self._SHADE, self.color[2]*self._SHADE)
    pygame.draw.polygon(self.s, c, self.pts)



    # draw outline
    if self.OUTLINE_COLOR:
      pygame.draw.aalines(self.s, self.OUTLINE_COLOR, 1, self.pts, 4)

    # draw block's mining status
    if self._mine_state != None: # yes this is nessisary
      self.s.blit(self.parent.src.mine[self._mine_state], (self.pts[3][0], self.pts[0][1]))

    # draw selection
    if self.selected:
      self.s.blit(self.parent.src.selector, (self.pts[3][0], self.pts[0][1]))



    # debug
    # if self.x == 2 and self.y == 2: 
    self.s.set_at((self.centerx, self.centery), (0, 0, 255))


    # label tile
    # r = self.font.render( str(self.x)+","+str(self.y), True, (0,0,0) )
    # self.s.blit(r, (sx+30,sy+10+h))




def generate_random_tile_height():
  a = random.randint(0, 1)
  return a



class sand(tile):

  def __init__(self, *args):
    super(sand, self).__init__(*args)

    # set sand color
    self.color = (233, 201, 175)