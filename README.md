# Block Matcher
 A simple color-matching puzzle game, written in Python

# How to Play

You can start a new game by clicking 'File', then 'New Game'. You will be asked to enter your name for the high scores chart, and to select a game mode. The avaliable game modes are as follows:

ENDLESS: Last as long as you can. More colors will be added the longer you last.

MARATHON: Score as many points as you can in 50 or 100 moves.

To earn points, you muct click on a matching set of 2 or more blocks of the same color that are horizontally or vertically connected to each other. When you do, all connected blocks of the same color will vanish, and the blocks above them will fall. The more connected blocks you clear, the more points you get.

Every time you successfully clear a group of blocks, it counts as one 'Move'. In Marathon mode, you only have a limited number of moves, indicated by the 'Moves' counter decreasing. In Endless mode, the number of moves made only determines when new colors are added to the game(every 50 moves, up to 150). The number of moves made is also saved in the high scores table, so if you want to im[ress your friends, go for big combos to get a high score in less moves!

The game ends when you have no more valid moves remaining, or when you run out of moves in Marathon mode. If you got a high score, it will save to the high scores table automatically. You can view the high scores table by clicking 'File', then 'High Scores.'