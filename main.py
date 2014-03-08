# pygame
import pygame
from pygame.locals import *

# my files
import world


class app(object):

  BG_COLOR = (180, 180, 180)

  def __init__(self):

    # init vars
    self.w = 800
    self.h = 600
    self.running = True

    # init pygame
    pygame.init()

    # create screen
    self.s = pygame.display.set_mode((self.w, self.h), RESIZABLE)

    # create clock
    self.clock = pygame.time.Clock()

    # create map, center it
    self.wld = world.map(self.s, w=16, h=16)
    # self.wld.flush_and_randomize_map()
    self.wld.center_map((self.w,self.h))

    # loop
    self.loop()


  def loop(self):

    # set mouse invisible
    # pygame.mouse.set_visible(False)

    while self.running:
      
      # tick clock
      self.clock.tick()

      # events
      for event in pygame.event.get():

        if event.type == QUIT:
          # quit program
          self.running = False
          return

        elif event.type == VIDEORESIZE:
          # resize screen
          self.w, self.h = event.size
          self.s = pygame.display.set_mode((self.w, self.h), RESIZABLE)

          # center map on screen
          self.wld.center_map(event.size)


        elif event.type == KEYDOWN:
          if event.unicode == "w": self.wld.yo += 50
          if event.unicode == "s": self.wld.yo -= 50
          if event.unicode == "d": self.wld.xo += 50
          if event.unicode == "a": self.wld.xo -= 50

          # adjust sun position
          if event.unicode == "q": self.wld.sun_pos += 0.1
          if event.unicode == "e": self.wld.sun_pos -= 0.1


        elif event.type == MOUSEMOTION:
          # send mouse motion
          self.wld.send_motion( event )

        elif event.type == MOUSEBUTTONDOWN:
          # send mouse motion
          self.wld.send_mousebutton( event, "down" )

        elif event.type == MOUSEBUTTONUP:
          # send mouse motion
          self.wld.send_mousebutton( event, "up" )



      # draw background
      self.s.fill(self.BG_COLOR)

      # render world
      self.wld.render()

      # flip screen
      pygame.display.flip()


    # make mouse visible again
    pygame.mouse.set_visible(True)


if __name__ == '__main__':
  a = app()

