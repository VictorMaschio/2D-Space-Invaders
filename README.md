# Space Invader
Victor Maschio Gabriel Paulet-Duprat

In this space invaders game, we can move using 'q' and 'd' and shoot simultaneously with the 'space' key. The enemies are created from a level file and appear infinitely. They shoot randomly at regular intervals, fortunately, the player is protected by asteroids. If an enemy reaches the bottom of the screen or the player's lives drop to zero, the player loses the game. The score increases by 50 for each enemy killed.

The quit button closes the window, and the new game button starts a new game.

Our space invaders are composed of a class file that contains the classes responsible for the execution of most elements of the program, such as the main window, canvas objects, etc. Of a file that contains functions for launching and creating objects, and a main file from which the project is launched.

After is a recursive multi-threaded method used in numerous functions such as shooting, enemy movement, allied movement, etc. There is an implementation of a list with enemy movements as well as the level loading that loops.