"""2048"""
import random 
import pygame

# structure of the game is a 2d array; storing values in a 2d grid
# each row is compiled as a list; so four lists is stored in one main list (nested list)
# start of game two random integers (two and two or two and four) is generated
# every time user inputs, a new random integer is added to one of the rows (two or four)

pygame.init()
screen = pygame.display.set_mode((600, 600))
font = pygame.font.Font(None, 60)
clock = pygame.time.Clock()
running_game = True
square_size: int = 125
margin_size: int = 20
color: dict[int, pygame.Color] = {
    0: pygame.Color(204, 192, 179),
    2: pygame.Color(238, 228, 218),
    4: pygame.Color(237, 224, 200),
    8: pygame.Color(242, 177, 121),
    16: pygame.Color(245, 149, 99),
    32: pygame.Color(246, 124, 95),
    64: pygame.Color(246, 94, 59),
    128: pygame.Color(237, 207, 114),
    256: pygame.Color(237, 204, 97),
    512: pygame.Color(237, 200, 80),
    1024: pygame.Color(237, 197, 63),
    2048: pygame.Color(237, 194, 46),
}



def print_grid(grid: list[list[int]]) -> None:
    # prints the grid vertically
    for row in grid:
        print(row)
        # prints row by row (so it's vertical)

def draw_grid(grid: list[list[int]], surface: pygame.Surface) -> None:
    for row in range(0, len(grid)):
        for column in range(0, len(grid)):
            pygame.draw.rect(surface, color[grid[row][column]], pygame.Rect(column * (square_size + margin_size) + margin_size, row * (square_size + margin_size) + margin_size, square_size, square_size))
            if grid[row][column] == 0:
                text_surface: pygame.Surface = font.render(str(""), True, (0,0,0))
            else:
                text_surface: pygame.Surface = font.render(str(grid[row][column]), True, (0,0,0))
            surface.blit(text_surface, (column * (square_size + margin_size) + margin_size + square_size / 2 - len(str(grid[row][column]))*10, row* (square_size + margin_size) + margin_size + square_size / 2 - 12, square_size, square_size))

grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

moved = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]

x: int = random.randint(0, 15)
# finding the position in lists to assign random int
row: int = x // 4 
# finds which row
# there are 4 rows; the first column are multiples of 4, meaning that whatever random integer is generated, it will only range within 0 to 3 (row 0, 1, 2, 3 -> 4 rows)
# // is integer division, where the decimals are just dropped (rounding down technically); notice that 0//4 is 0 and 15//4 is 3 so it works for the amount of rows we have (4)
column: int = (x % 4)
# finds which column
# length of each row is 4, which is why it's moduloed by 4
# modulo determines which column after a row is assigned; column always has to be from 0 to 3, which ensures that it will only range within the randomly chosen row

while True:
    # to prevent the possibility of the first and second random integer, create a while loop that ensures that the two random integers are not in the same position
    y: int = random.randint(0,15)
    if x != y:
        row1: int = y // 4 
        # rename row and column so python doesn't assume that it's the same value; x and y are separate values and row/columns are not functions so variables can't just be swapped
        column1: int = (y % 4)
        break

grid[row][column] = 2
# find the specific square within the grid; find the row (one of the four lists) within the grid and then the column (specific index of list) to identify a specific square
# make it equal to 2 because at least one of the numbers in the squares has to be 2 to ensure that two 4s aren't generated 

if random.random() >= 0.4:
# weighted random; causes the generation of 2 80% more likely than 4
# random.random results in a float between 0 and 1; add () at end since it's a function
    grid[row1][column1] = 2
else:
    grid[row1][column1] = 4

turn: bool = False
dx: int = 0

while running_game:
    dx += 1
    if dx == 1000000:
        dx = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False



        # this while True ensures that the game itself is running, not verifying the user input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            # shifts all the integers upward
            turn = True
            while True:
                grid_copy = []
                for row in grid:
                    grid_copy.append(list(row))
                # grid_copy = [list(row) for row in grid] -> cleaner way of doing the same thing just in one line
                # creating a literal (or deep) copy of grid (so every time grid is modified, it doesn't affect grid_copy)
                # new global variable (grid_copy) and assign it with a COPY of the values (grid_copy does not = grid because then, whenever grid is modified, grid_copy would also be modified)
                for row in range(len(grid)):
                # accessing the index of the lists
                    if row == 0:
                        continue
                        # "continue" skips its iteration
                        # this ensures that in the case that the integer is at the edge of the list (first row), it doesn't go out of range 
                    for column in range(len(grid)):
                    # the integers shift up 1 row but stays within the same column
                        if grid[row-1][column] == 0:
                        # checks to see if the row above integer is empty
                            grid[row-1][column] = grid[row][column]
                            moved[row-1][column] = moved[row][column]
                            # replaces empty space with integer
                            grid[row][column] = 0
                            moved[row][column] = False
                            # resets the space that the integer was in before shifting up
                        else:
                            if grid[row][column] == grid[row-1][column] and moved[row][column] == moved[row-1][column] == False:
                            # multiplies two of the same integers together if "smashed"
                                grid[row-1][column] *= 2
                                moved[row-1][column] = True
                                grid[row][column] = 0
                                moved[row][column] = False
                if grid_copy == grid:
                # continues to loop until there are no more modifications needed
                # if modified grid isn't the same as original grid, then it breaks out of the loop because it's done modifying and we don't want the modified grid to be the same as the orignal grid
                # if no modifcation is needed, then it wouldn't even enter the loop and return same grid
                    break

        if keys[pygame.K_a]:
            # shifts all the integers left
            turn = True
            while True:
                grid_copy = []
                for row in grid:
                    grid_copy.append(list(row))
                for row in range(len(grid)):
                    for column in range(len(grid)):
                        if column == 0:
                            continue
                        if grid[row][column-1] == 0:
                            grid[row][column-1] = grid[row][column]
                            moved[row][column-1] = moved[row][column]
                            grid[row][column] = 0
                            moved[row][column] = False
                        else:
                            if grid[row][column] == grid[row][column-1] and moved[row][column] == moved[row][column-1] == False:
                                grid[row][column-1] *= 2
                                moved[row][column-1] = True
                                grid[row][column] = 0
                                moved[row][column] = False
                if grid_copy == grid:
                    break
        
        if keys[pygame.K_s]:
            # shifts all the integers downward
            turn = True
            while True:
                grid_copy = []
                for row in grid:
                    grid_copy.append(list(row))
                for row in range(len(grid)):
                    if row == len(grid)-1:
                        continue
                    for column in range(len(grid)-1, -1, -1):
                    # this ensures that it checks from down up (not up down) so that it shifts before it combines
                    # this is so that in a case that there are three rows of the same integer, let's say 2, it would result in 2, 4 instead of 4,2 but obviously verticaly
                        if grid[row+1][column] == 0:
                            grid[row+1][column] = grid[row][column]
                            moved[row+1][column] = moved[row][column]
                            grid[row][column] = 0
                            moved[row][column] = False
                        else:
                            if grid[row][column] == grid[row+1][column] and moved[row][column] == moved[row+1][column] == False:
                                grid[row+1][column] *= 2
                                moved[row+1][column] = True
                                grid[row][column] = 0
                                moved[row][column] = False
                if grid_copy == grid:
                    break
        
        if keys[pygame.K_d]:
            # shifts all the integers right
            turn = True
            while True:
                grid_copy = []
                for row in grid:
                    grid_copy.append(list(row))
                for row in range(len(grid)-1, -1, -1):
                    for column in range(len(grid)):
                        if column == len(grid[row])-1:
                            # len(grid[row]) means the length of the rows in the grid
                            # technically, len(grid)-1 is allowed but only because this specific grid is symmetrical 
                            continue
                        if grid[row][column+1] == 0:
                            grid[row][column+1] = grid[row][column]
                            moved[row][column+1] = moved[row][column]
                            grid[row][column] = 0
                            moved[row][column] = False
                        else:
                            if grid[row][column] == grid[row][column+1] and moved[row][column] == moved[row][column+1] == False:
                                grid[row][column+1] *= 2
                                moved[row][column+1] = True
                                grid[row][column] = 0
                                moved[row][column] = False
                if grid_copy == grid:
                    break
        
        moved = [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]

        if turn:
            # 1 of 2 ways of ending game: the grid is filled and none of the adjacent integers are the same (so they aren't addable)
            zeros = False
            for row in grid:
            # checks if there are any zeros in grid; if there isn't, the game proceeds
                if 0 in row:
                    zeros = True
                    break
            
            # checks if the integers next to each other are the same (addable)
            adjacent = False
            for row in range(len(grid)):
                for column in range(len(grid)):
                    if row != 0:
                        if grid[row][column] == grid[row-1][column]:
                            adjacent = True
                            break
                    if column != 0:
                        if grid[row][column] == grid[row][column-1]:
                            adjacent = True
                            break
                    if row != len(grid)-1:
                        if grid[row][column] == grid[row+1][column]:
                            adjacent = True
                            break
                    if column != len(grid[row])-1:
                        if grid[row][column] == grid[row][column+1]:
                            adjacent = True
                            break
            if adjacent == False:
                print("Game over.")
                break

            while zeros:
                z: int = random.randint(0,15)
                # new global variable that randomly generates in a vacate spot after every turn
                row: int = z // 4 
                column: int = (z % 4)
                if grid[row][column] == 0:
                # new random integer is generated after every turn in a vacate space
                    if random.random() >= 0.1:
                        grid[row][column] = 2
                    else:
                        grid[row][column] = 4
                    break
            
            
            # 2 of 2 ways of ending game: if 2048 is calculated
            for row in grid:
            # goes through the lists of the list (since grid is a nested list)
                if 2048 in row:
                    running_game = False
                    break
            turn = False

        draw_grid(grid, screen)
        pygame.display.flip()
        clock.tick(60)


pygame.quit()
