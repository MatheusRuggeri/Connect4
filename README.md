# Connect 4
The traditional game made with Python.
There are 2 versions, the Terminal, where you can play in your Terminal or CMD, and the GUI (Graphical User Interface), where you can play with your mouse.
The code that you are downloading was configured with 6 lines, 7 columns and you have to connect 4 pieces to be the winner, this is the traditional Connect4 game, but this was improoved, you can configure this values, set a larger board and maybe 5 pieces connected to win.

# ConnectN

ConnectN is a python based game, it is an improved version of Connect4, it has some features:
  - AI (easy, medium, hard), you can choose between human and AI player, you can play AI vs AI, Player vs Player or Player x AI
  - You can configure the game as you want, the traditional 7x6 board with 4 connections or even bigger, like 10x10 board 
  - The program is Tiled base, so you will be able to see the board even if this is not a traditional size
  - You can choose the language between Brazilian Portuguese, English and German
  - Once you select the language, ConnectN will translate the game to your language, it will also save your preference and never asks for the language again

# New Features!

  - Forget your old and boring Connect4, how about you see if you can beat the AI in a 16x9 Connect5 game?
  - Now you can configure your board as you wish and maybe watch 2 AI fighting

> The software design goal was find a good
> approach to make a fun game with a smart
> AI and keep it's performance.

### Tech

ConnectN uses some Python libraries:

| Library | Information |
| ------ | ------ |
| Pygame | A very HTML powerful pack to game development |
| Pygame.gfxdraw | A pack that can also handle PNG's alpha layer  |
| CSV | A pack to handle the language dictionary file |
| Random | A pack useful to AI's development |
| Sys | A pack to finish the execution |
| Os.path | A pack to check if a file telling the program your language selection exists |

### How to Play

```sh
$ python connectN.py
```

### Todo

 - Improve AI

License
----

MIT
