import pygame

SCREEN_HEIGHT = 598
SCREEN_WIDTH = 598
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sudoku')

pygame.font.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

class Sudoku :
    def __init__(self, grid) :
        self.n = len(grid)
        self.grid = [[grid[i][j] for j in range(self.n)] for i in range(self.n)]
        self.visited = [[False for j in range(self.n)] for i in range(self.n)]
        self.color = [[BLACK for j in range(self.n)] for i in range(self.n)]

        for i in range(self.n) :
            for j in range(self.n) :
                if self.grid[i][j] != 0 :
                    self.visited[i][j] = True

        dim = min(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.w = (dim - dim % self.n) // self.n

    def show(self, grid = None) :
        
        if grid is None :
            grid = self.grid

        for i in range(self.n) :
            for j in range(self.n) :
                if grid[i][j] == 0 and self.visited[i][j]:
                    pygame.draw.rect(win, RED, (j * self.w, i * self.w, self.w, self.w), 4)
                else :
                    if self.color[i][j] == BLACK :
                        w = 1
                    else :
                        w = 4
                    pygame.draw.rect(win, self.color[i][j], (j * self.w, i * self.w, self.w, self.w), w)
                
                if self.visited[i][j] :
                    font = pygame.font.SysFont('Consolas', 50)
                    text = font.render(str(grid[i][j]), True, BLACK)
                    win.blit(text, (j * self.w + self.w // 2 - 15, i * self.w + self.w // 2 - 20))

        sep = int(self.n ** 0.5)
        for i in range(sep + 1) :
            pygame.draw.line(win, BLACK, (i * sep * self.w, 0), (i * sep * self.w, self.n * self.w), 4)
        
        for j in range(sep + 1) :
            pygame.draw.line(win, BLACK, (0, j * sep * self.w), (self.n * self.w, j * sep * self.w), 4)

    def solveSudokuHelper(self, actual_grid, custom_grid, row = 0, col = 0) : 
        
        win.fill(WHITE)
        self.visited[row][col - 1] = True
        self.show(custom_grid)
        pygame.display.update()
        pygame.time.delay(5)
        
        # Checking if filled the last box
        if row == 8 and col == 9 :
            return True
        
        # Checking if the current column is within the range or not
        if col == 9 :
            col = 0
            row += 1

        # Checking if the current box is filled or not
        if actual_grid[row][col] != 0 :
            return self.solveSudokuHelper(actual_grid, custom_grid, row, col + 1)

        # Making options as True for all the numbers from 1 to 9 initially
        options = [True for i in range(10)]

        # Eliminating numbers present in the current 3*3 box from options
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for i in range(row_start, row_start + 3) :
            for j in range(col_start, col_start + 3) :
                options[custom_grid[i][j]] = False

        # Eliminating numbers present in the current row from options
        for j in range(9) :
            options[custom_grid[row][j]] = False

        # Eliminating numbers present in the current column from options
        for i in range(9) :
            options[custom_grid[i][col]] = False

        # Try to fit in all the options in the current box 
        for num in range(1, 10) :
            if not options[num]:
                continue
            custom_grid[row][col] = num 
            self.color[row][col] = GREEN
            ans = self.solveSudokuHelper(actual_grid, custom_grid, row, col + 1)
            if ans == True :
                return True
            custom_grid[row][col] = 0

        win.fill(WHITE)
        self.visited[row][col - 1] = True
        self.show(custom_grid)
        pygame.display.update()
        pygame.time.delay(5)

        return False

    def solveSudoku(self):

        actual_grid = self.grid.copy()
        custom_grid = self.grid.copy()
        ans = self.solveSudokuHelper(actual_grid, custom_grid)
        return

grid = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]]

sudoku = Sudoku(grid)

solved = False
run = True
play = False
while run :

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] :
        quit()
    elif keys[pygame.K_SPACE] :
        play = True

    win.fill(WHITE)

    sudoku.show()

    if play :
        pygame.display.update()
        pygame.time.delay(1000)

        if not solved :
            sudoku.solveSudoku()
            solved = True

        pygame.display.update()

pygame.quit()