# Pacman game created using Pygame
Pacman game is a project I've decided to do for  my Programming with Python (CITB331) course in New Bulgarian University (NBU)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [Pygame](https://www.pygame.org) on your local machine. Pip comes with Python on installation

```bash
pip install pygame
```

## Information about the game
It is designed to look similar to the original game from 1980. Includes only player, ghosts and coins.

The game is happening over one of the most popular background images for Pacman games. 
A custom grid is being built over it (check ***map.txt***), based on which the logic for all in-game events happen.

Mappings for easier understand of the map file:
- W - location of a wall
- 1, 2, 3, 4 - enemies location
- C - location of coin
- E - center exit

[Link to background image](https://www.codeproject.com/KB/game/520783/background.png)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)