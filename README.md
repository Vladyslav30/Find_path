# Path Finding Visualizer

This project is a simple implementation of the A* path finding algorithm, which is used to find the shortest path between two points on a grid. The grid can have obstacles, and the path cannot go through them. The algorithm works by assigning a score to each spot (or cell) on the grid and constantly picking the spot with the lowest score as the next spot to move to.

# Installation
1.Clone this repository using git:
``` shell
git clone https://github.com/Vladyslav30/Find_path.git
```

2.This project requires pygame to run. You can install these packages using pip:
``` shell
pip install pygame
```
# Running the Program
To run the program, you can use the following command:
``` shell
python find_path.py
```

# Usage
Once you run the program, a window will appear asking for the coordinates of the start and end spots. Input the coordinates as integers between 1 and 48. You also have the option to show steps of the path finding process by checking the 'Show Steps' box.

After submitting the coordinates, a grid will appear. You can draw obstacles by clicking on the cells. To start the path finding process, press the space key.

If a path is found, it will be displayed in blue, and a message box will appear showing the shortest distance to the path. If there's no solution, a message box will inform you that there's no solution.


