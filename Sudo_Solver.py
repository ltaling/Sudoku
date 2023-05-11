#Imports
import numpy as np
import matplotlib.pyplot as plt
import copy
import tkinter as tk

#----------------------------------------------------------------------------
# All the functions used in the program

def checker(array):
    """Checks if the sudoku is correctly filled"""
    #Checks rows and columns
    for i in range(9):
        if np.sum(array[i]) != 45 or np.sum(array[:,i]) != 45:
            return False
    #Checks boxes
    for i in [[0,3],[3,6],[6,9]]:
        for j in [[0,3],[3,6],[6,9]]:
            if np.sum(array[i[0]:i[1],j[0]:j[1]]) != 45:
                return False
    return True

def position_num(grid):
    """Returns the the positions of all empty grid spaces and their respective possible numbers"""
    x_pos = []
    y_pos = []
    #valid_n = 9
    valid_nums = []
    for i in range(9):
        for j in range(9):
            #temp_n = 0
            temp_nums = []
            if grid[i,j] == 0:
                for k in range(1,10):
                    if valid(grid,j,i,k): # Check if the number fits
                        #temp_n += 1
                        temp_nums.append(k)
                #if temp_n < valid_n:
                #valid_n = temp_n
                valid_nums.append(temp_nums)
                x_pos.append(j)
                y_pos.append(i)
    return y_pos,x_pos,valid_nums

def valid(grid,x,y,n):
    """Determines if the number, n, fits in coordinate (x,y) on grid"""
    # Check row
    for i in range(9):
        if grid[y,i] == n:
            return False
    # Check column
    for i in range(9):
        if grid[i,x] == n:
            return False
    # Check square
    box_x = x//3
    box_y = y//3
    
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if grid[i,j] == n:
                return False
    return True

def solver(array):
    """Finds the solution to a sudoku via the backtracking algorithm, and returns the solved array"""
    grid = np.copy(array)
    #prev_sol = np.zeros([9,9],dtype=int)
    y_pos,x_pos,nums = position_num(grid) #Positions with possible entries
    # Sort the lists so fewest possibilities go first
    zipped = sorted(zip(nums,y_pos,x_pos),key=lambda x: len(x[0]))
    nums,y_pos,x_pos = [list(a) for a in zip(*zipped)]
    nums_clone = copy.deepcopy(nums) # Make a copy of the numbers to be re-added when all possibilities exhausted
    n_index = 0 # Index of possible numbers 
    i = 0
    while i < len(nums) and i > -1: # Loop over every position
        if len(nums[i]) < 1: # When there are no more numbers left to try
            grid[y_pos[i],x_pos[i]] = 0 #Grid element goes back to being empty
            nums[i] = copy.deepcopy(nums_clone[i]) # possible numbers are replaced
            i -= 1 #We go back to previous position
            continue # Don't bother checking the grid
        
        else:
            if not valid(grid,x_pos[i],y_pos[i],nums[i][0]): #If number doesn't fit
                nums[i].pop(0) # Remove it from the possibilities
            else:
                grid[y_pos[i],x_pos[i]] = nums[i][0] # Place number onto grid
                nums[i].pop(0) # Remove it from the possibilities
                i += 1 # Move onto the next set      
      
    # Just to make sure the solution makes sense
    if checker(grid):
        return grid # Return the solved grid

#-----------------------------------------------------------------------------
# User interface

class main_window:
    def __init__(self,input_window):
        self.input_window = input_window
        self.input_window.title('Sudoku Solver')
        self.make_window()
        
    def make_window(self):

        # Create grid
        self.cells = {}
        self.header = tk.Frame(master=self.input_window)
        self.header.grid(column=0,row=0,columnspan=10)
        self.heading = tk.Label(master = self.header, text = 'Please input the known numbers onto the grid and\
 click the "Solve" button on the bottom right when you are done')
        self.heading.pack(pady=3)
        for row in range(1,10):
            for column in range(1,10):
                cell = tk.Frame(master=self.input_window, bg='white', highlightbackground="black",
                             highlightcolor="black", highlightthickness=1,
                             width=70, height=50,  padx=0,  pady=3)
                cell.grid(row=row, column=column)
                self.cells[(row, column)] = cell

        # Allow user input
        for row in range(1,10):
            for column in range(1,10):
                self.cells[(row,column)] = tk.Entry(master=self.input_window,width=4,relief='flat',justify='center',
                                               font=(('Segoe UI'), (20)))
                self.cells[(row,column)].grid(row=row,column=column)

        # Define the 'Solve' button
        self.solve_button = tk.Button(master=self.input_window,text="Solve",width=20,pady=3,
                                 relief='raised',command=self.reader)
        self.solve_button.grid(column=7,row=10,columnspan=3)
        
    def reader(self):
        """This function defines what happens when the Solve button is pressed"""
        puzzle = np.zeros((9,9))
        for row in range(1,10):
            for column in range(1,10):
                if len(self.cells[(row,column)].get()) != 0:
                    puzzle[row-1,column-1] = self.cells[(row,column)].get()

        solution = solver(puzzle)

        self.lbl_cells = {}
        for row in range(1,10):
            for column in range(1,10):
                self.lbl_cells[(row,column)] = tk.Label(master=self.input_window,width=4,relief='flat',
                            justify='center',font=(('Segoe UI'), (20)),text=str(int(solution[row-1,column-1])))
                self.lbl_cells[(row,column)].grid(row=row,column=column)

        self.heading.destroy()
        new_heading = tk.Label(master = self.header, text = "Sudoku solved! Press 'Refresh' to solve another")
        new_heading.pack(pady=3)

        self.solve_button.destroy()
        self.refresh_button = tk.Button(master=self.input_window, text="Refresh",width=20,pady=3,
                                        relief='raised',command=self.refresh)
        self.refresh_button.grid(column=7,row=10,columnspan=3)
        
    def refresh(self):
        """This function defines what happens when the refresh button is pressed"""
        self.make_window()

#-------------------------------------------
# Main program

root = tk.Tk()
app = main_window(root)
root.mainloop()