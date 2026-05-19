- [x] Enemy collisions with bullets
- [x] Player collisions with enemies
- [ ] health bar for both players and enemies
  - small health bar that floats under the player or enemy. 
  - assuming a seperate surface whose rect's top edge = player or enemy's bottom edge? 

  - I am not getting errors on Player's healthbar but I am also not getting a healthbar so thats great. time to print debug or maybe hop over to vscode and bust out the debugger over there
  - ok so there is a healthbar. its is in the top left of the screen because the position is hard coded to be at 0,0. I changed it to be the Player's rect's topleft position. It starts in the right place but it doesn't follow the player around. Also the health bar is a little thick. Thats an easy fix. I think it also needs to be off the player a little bit.
  - ok now the health bar follows the player around, except when the player loses health it doesnt' change and when the player hit a second enemy, I get this: 

```sh
(galaga-clone) ➜  galaga_clone git:(main) ✗ uv run main.py
pygame-ce 2.5.7 (SDL 2.32.10, Python 3.13.2)
Traceback (most recent call last):
  File "/Users/mason_cotter/dev/galaga_clone/main.py", line 157, in <module>
    main()
    ~~~~^^
  File "/Users/mason_cotter/dev/galaga_clone/main.py", line 144, in main
    draw_window(level, enemies, bullets)
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/mason_cotter/dev/galaga_clone/main.py", line 76, in draw_window
    WINDOW.blit(level.img, (0, 0))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
pygame.error: Surface is not initialized
```

- got the player health bar working!! now onto the enemy health bars
