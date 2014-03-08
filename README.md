#Pygame Isometric Engine#

**Requirements**
- Python (I use 2.7, anything above should work)
- Pygame (http://pygame.org)
- GameObjects (It should be included, but otherwise https://code.google.com/p/gameobjects/)

**Examples**

Check main.py for a working example

#*OR*#

Try something along these lines:
```python
import pygame, world

# init
pygame.init()
s = pygame.display.set_mode((500, 500))
w = world.map(s, 3, 3)


while True:
  # make sure it doesn't crash
  for event in pygame.event.get():
    if event.type == pygame.QUIT: break
    
  # render world
  w.render()
  
  pygame.display.flip()
```
