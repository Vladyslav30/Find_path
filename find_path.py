# Import necessary modules
from tkinter import messagebox, ttk
import pygame
import sys
import tkinter as tk
import os
import math

# Initialize the Pygame display module
screen = pygame.display.set_mode((800, 800))

# Define the 'spot' class
class spot:
    # Constructor for spot class
    def __init__(self, x, y):
        self.i = x  # x-coordinate
        self.j = y  # y-coordinate
        self.f = 0  # total cost of the node
        self.g = 0  # distance from the start node to the current node
        self.h = 0  # heuristic estimate of the distance from the current node to the end node
        self.neighbors = []  # list to store the neighbors of the current spot
        self.previous = None  # previous node in the optimal path
        self.obs = False  # boolean to check if the current spot is an obstacle
        self.closed = False  # boolean to check if the current spot has been visited
        self.value = 1  # value associated with the spot (can be used to represent different types of terrain)

    # Function to display the current spot on the screen
    def show(self, color, st):
        if self.closed == False:
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    # Function to show the path on the screen
    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    # Function to add neighbors of the current spot
    def addNeighbors(self, grid):
        # Array of possible movement directions (8 directions)
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1),
                   (-1, -1), (1, -1), (-1, 1)]

        for offset in offsets:
            next_i, next_j = self.i + offset[0], self.j + offset[1]

            # Verify that we are in the grid boundaries
            if 0 <= next_i < cols and 0 <= next_j < row:
                neighbor = grid[next_i][next_j]

                # Add the neighbor if it's not an obstacle
                if not neighbor.obs:
                    self.neighbors.append(neighbor)



cols = 50  # Number of columns in the grid
grid = [0 for i in range(cols)]  # Initialize grid as a list of zeros
row = 50  # Number of rows in the grid
openSet = []  # List for nodes to be evaluated
closedSet = []  # List for nodes already evaluated
red = (255, 0, 0)  # RGB value for color red
green = (0, 255, 0)  # RGB value for color green
blue = (0, 0, 255)  # RGB value for color blue
grey = (220, 220, 220)  # RGB value for color grey
w = 800 / cols  # Width of each spot on the grid
h = 800 / row  # Height of each spot on the grid
cameFrom = []  # List to record the path

# Create 2D array for the grid
for i in range(cols):
    grid[i] = [0 for i in range(row)]

# Create spots and store them in the grid
for i in range(cols):
    for j in range(row):
        grid[i][j] = spot(i, j)

# Display all spots as red on the screen
for i in range(cols):
    for j in range(row):
        grid[i][j].show((255, 0, 0), 1)

# Draw lines to create the grid - Horizontal and Vertical
# Also, set the boundary cells as obstacles
for i in range(0, row):
    grid[0][i].show(grey, 0)
    grid[0][i].obs = True
    grid[cols - 1][i].obs = True
    grid[cols - 1][i].show(grey, 0)
    grid[i][row - 1].show(grey, 0)
    grid[i][0].show(grey, 0)
    grid[i][0].obs = True
    grid[i][row - 1].obs = True

class SetupWindow:
    # Constructor for the SetupWindow class
    def __init__(self):
        self.window = tk.Tk()  # Initialize Tkinter window
        self.setup_interface()  # Setup the interface for the window
        self.window.mainloop()  # Start the Tkinter event loop

    # Method to setup the interface for the window
    def setup_interface(self):
        self.instructions_label = tk.Label(self.window,
                                               text='Input coordinates from (1, 1) to (48, 48)')  # Instruction label
        self.instructions_label.grid(columnspan=2, row=0)  # Place instruction label in grid

        self.start_x_label = tk.Label(self.window, text='Start x: ')  # Label for start x coordinate
        self.start_x_entry = tk.Entry(self.window)  # Text entry for start x coordinate

        self.start_y_label = tk.Label(self.window, text='Start y: ')  # Label for start y coordinate
        self.start_y_entry = tk.Entry(self.window)  # Text entry for start y coordinate

        self.end_x_label = tk.Label(self.window, text='End x: ')  # Label for end x coordinate
        self.end_x_entry = tk.Entry(self.window)  # Text entry for end x coordinate

        self.end_y_label = tk.Label(self.window, text='End y: ')  # Label for end y coordinate
        self.end_y_entry = tk.Entry(self.window)  # Text entry for end y coordinate

        self.var = tk.IntVar()  # Integer variable to hold the state of the checkbutton
        self.showPath = ttk.Checkbutton(self.window, text='Show Steps:', onvalue=1, offvalue=0,
                                            variable=self.var)  # Checkbutton to show path steps

        self.submit = tk.Button(self.window, text='Submit',
                                    command=self.onsubmit)  # Submit button, command to execute on submit needs to be defined

        # Place all the elements in the grid
        self.start_x_label.grid(row=1, column=0)
        self.start_x_entry.grid(row=1, column=1)
        self.start_y_label.grid(row=2, column=0)
        self.start_y_entry.grid(row=2, column=1)
        self.end_x_label.grid(row=3, column=0)
        self.end_x_entry.grid(row=3, column=1)
        self.end_y_label.grid(row=4, column=0)
        self.end_y_entry.grid(row=4, column=1)

        self.showPath.grid(columnspan=2, row=5)
        self.submit.grid(columnspan=2, row=6)

        self.window.update()  # Update the window to reflect the added elements

    # Function to be executed on 'submit' button click
    def onsubmit(self):
        # Access global variables 'start' and 'end'
        global start
        global end
        # Get the x and y coordinates for the start and end points from the Entry fields in the Tkinter window
        start_x = int(self.start_x_entry.get())
        start_y = int(self.start_y_entry.get())
        end_x = int(self.end_x_entry.get())
        end_y = int(self.end_y_entry.get())

        # Assign the 'start' and 'end' spots from the 'grid' based on the user input
        start = grid[start_x][start_y]
        end = grid[end_x][end_y]

        # Close the Tkinter window after the start and end spots have been determined
        self.window.quit()
        self.window.destroy()


# Initialize your application
window = SetupWindow()

# Your pygame code here
pygame.init()
openSet.append(start)




# This function changes the status of a spot in the grid when a mouse press event occurs
def mousePress(x):
    t = x[0]  # x-coordinate of the mouse press event
    w = x[1]  # y-coordinate of the mouse press event
    g1 = t // (800 // cols)  # Convert screen coordinate to grid coordinate
    g2 = w // (800 // row)  # Convert screen coordinate to grid coordinate
    acess = grid[g1][g2]  # Access the corresponding spot on the grid
    # If the spot isn't the start or the end, make it an obstacle
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show((255, 255, 255), 0)  # Show the obstacle spot in white

# Show the end spot in pink
end.show((255, 8, 127), 0)
# Show the start spot in pink
start.show((255, 8, 127), 0)

# Game loop
loop = True
while loop:
    # Event handling
    for event in pygame.event.get():
        # Quit event (closing the window)
        if event.type == pygame.QUIT:
            pygame.quit()
        # Mouse press event
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()  # Get the position of the mouse
                mousePress(pos)  # Call the function to handle the mouse press event
            except AttributeError:
                pass
        # Key press event
        elif event.type == pygame.KEYDOWN:
            # If the Space key is pressed, end the loop
            if event.key == pygame.K_SPACE:
                loop = False
                break
    ev = pygame.event.get()

# Add the neighbors of each spot to its neighbors list
for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)

# Heuristic function for A* (distance between two points)
def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)  # Euclidean distance
    return d



def main():
    global running  # Add this at the top of the main function to use the global variable "running"
    end.show((255, 8, 127), 0)  # Show the end spot in pink
    start.show((255, 8, 127), 0)  # Show the start spot in pink
    if len(openSet) > 0:  # If there are still spots to be evaluated in the open set
        lowestIndex = 0  # Index of the spot with the lowest f score
        # Find the spot in the open set with the lowest f score
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i

        current = openSet[lowestIndex]  # The current spot is the one with the lowest f score
        if current == end:  # If the current spot is the end spot, the path has been found
            start.show((255,8,127),0)  # Show the start spot in pink
            temp = current.f  # Save the f score of the current spot (the length of the path)
            # Trace back the path from the end to the start
            for i in range(round(current.f)):
                current.closed = False  # The spots on the path are not considered closed anymore
                current.show((0,0,255), 0)  # Show the spots on the path in blue
                current = current.previous  # Go to the previous spot on the path
            end.show((255, 8, 127), 0)  # Show the end spot in pink

            tk.Tk().wm_withdraw()
            # Display a message box indicating the program has finished and showing the shortest distance
            result = messagebox.askokcancel('Program Finished', (f'The program finished, the shortest distance \n to the path is {int(temp)} blocks away'))
            if result == True:
                # If the user presses 'OK', restart the program
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                # If the user presses 'Cancel', wait for a key press to end the program
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        # If the current spot is not the end spot
        # Remove the current spot from the open set and add it to the closed set
        openSet.pop(lowestIndex)
        closedSet.append(current)

        # Evaluate the neighbors of the current spot
        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            # If the neighbor has not been evaluated yet
            if neighbor not in closedSet:
                tempG = current.g + current.value
                # If the neighbor is in the open set and its g score is higher than the current g score
                # Update the g score
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                # If the neighbor is not in the open set, set its g score and add it to the open set
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            # Update the h and f scores of the neighbor
            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            # If the neighbor has no previous spot, set its previous spot to the current spot
            if neighbor.previous == None:
                neighbor.previous = current
    else:  # There's no path
        tk.Tk().wm_withdraw()
        # Display a message box indicating there's no solution
        result = messagebox.askokcancel('No Solution', 'There was no solution')
        if result:
            running = False  # Set running to False to stop the game loop
            pygame.quit()  # End the pygame
    # If the 'Show Steps' option is checked, show the spots in the open set in green
    if window.var.get():
        for i in range(len(openSet)):
            openSet[i].show(green, 0)

running = True  # The game loop will keep running while this variable is True
while running:
    ev = pygame.event.poll()  # Get the most recent event
    # If the event is a QUIT event, stop the game loop and end pygame
    if ev.type == pygame.QUIT:
        running = False
        pygame.quit()
    pygame.display.update()  # Update the display
    main()  # Call the main function



