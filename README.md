#Pygame Isometric Engine#

*Requirements*
- Python (I use 2.7, anything above should work)
- Pygame (http://pygame.org)
- GameObjects (It should be included, but otherwise https://code.google.com/p/gameobjects/)

*Examples*
1. Check main.py for a working example

Try something along these lines:
```python
import pygame, world

# init
pygame.init()
s = pygame.display.set_mode((self.w, self.h), RESIZABLE)
w = world.map(s, 10, 10)


while True:
  # make sure it doesn't crash
  for event in pygame.events.get():
    if event.type == QUIT: break
    
  # render world
  w.render()
  
  pygame.display.flip()
```
