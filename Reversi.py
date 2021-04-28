N, M = 8, 8
n_players = 2
marks = ['B', 'W']
count_cells = [0,0]
grid = [['.']*(M) for _ in range(N)]
possible_cells = []
#This function prints the grid of Reversi as the game progresses
def print_grid():
    print("Player 1: %c  vs  Player 2: %c" % (marks[0], marks[1]))
    print('--' + '---' * M + '--')
    for i in range(N):
        print(end='|  ')
        for j in range(M):
            print(grid[i][j], end='  ')
        print(end='|')
        print()
        print('--' + '---' * M + '--')
    for i in range(n_players):
        print('Player %c has %d cells'% (marks[i], count_cells[i]))
    print('--' + '------' * (M-1))
#This function checks if the game has a full state or not
def check_full():
    for i in range(N):
      for j in range(M):
        if grid[i][j] == '.':
          return False
    return True
#This function checks if the game has a tie state or not
def check_player_ability():
    for i in range(N):
      for j in range(M):
        if grid[i][j] == '?':
          return True
    return False
#This function checks if given cell is chosen or not
def check_chosen(i, j):
    if grid[i][j] == '?':
      return True
    return False
#This function checks if given cell is empty or not
def check_empty(i, j):
    if grid[i][j] == '?':
      return True
    return False
#This function checks if given position is valid or not
def check_valid_position(i, j):
    if i >= 0 and i < N and j >= 0 and j < M:
        return True
    return False
#This function calculates the total number of cells for each player
def calc_cells():
    count_cells[0] = 0
    count_cells[1] = 0
    for i in range(N):
      for j in range(M):
        if grid[i][j] == 'B':
          count_cells[0]+=1
        elif grid[i][j] == 'W':
         count_cells[1]+=1
#This function sets the given mark to the given cell
def set_cell(i, j, mark):
    grid[i][j] = mark

#This function marks the possible cells in the grid
def mark_possible_cells(i,j):
    grid[i][j] = '?'
#This function gets the most cell in the given direction
def get_most_cell(i, j, dx, dy, player, target_mark):
    cnt = 0
    while check_valid_position(i, j) and grid[i][j] == marks[1-player]:
        i += dx
        j += dy
        cnt += 1
    if (check_valid_position(i, j) and grid[i][j] == '.' and cnt > 0):
        most_i = i
        most_j = j
    elif (check_valid_position(i, j) and grid[i][j] == target_mark and cnt > 0):
        most_i = i
        most_j = j
    else:
        most_i = -1
        most_j = -1
    return most_i,most_j
#This function gets the most cells in the all directions
def get_most_cells(i, j, player, target_mark):
    most_cells = []
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dx, dy in dirs:
        most_i,  most_j = get_most_cell(i+dx, j+dy, dx, dy, player, target_mark)
        if most_i == -1 and most_j == -1:
            continue
        if(grid[most_i][most_j] == '.'):
           mark_possible_cells(most_i,most_j)

#This function switches the neighbor cells of the given cell
def switch_cells(i, j, player):
    most_i = 0
    most_j = 0
    cnt = 0
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for k in range(8):
        dx = dirs[k][0]
        dy = dirs[k][1]
        most_i, most_j = get_most_cell(i+dx, j+dy, dx, dy, player, marks[player])
        if (not most_i == -1 and not most_j == -1 and grid[most_i][most_j] == marks[player]):
            if (i == most_i):
                mini = min(j, most_j)
                maxi = max(j, most_j)
                for h in range(mini,maxi):
                    grid[i][h] = marks[player]
            elif j == most_j:
                mini = min(i, most_i)
                maxi = max(i, most_i)
                for h in range(mini,maxi):
                    grid[h][j] = marks[player]
            elif abs(i - most_i) == abs(j - most_j):
                temp = j
                if (i < most_i and j < most_j):
                    for h in range(i,most_i):
                        grid[h][temp] = marks[player]
                        temp += 1
                elif (i < most_i and j > most_j):
                    for h in range(i,most_i):
                        grid[h][temp] = marks[player]
                        temp -= 1
                elif (i > most_i and j > most_j):
                    temp = most_j
                    for h in range(most_i,i):
                        grid[h][temp] = marks[player]
                        temp += 1
                elif (i > most_i and j < most_j):
                    temp = most_j;
                    for h in range(most_i, i):
                        grid[h][temp] = marks[player]
                        temp -= 1
#This function generates the possible cells to be chosen
def generate_possible_cells(player):
    for i in range(N):
      for j in range(M):
        if grid[i][j] == marks[player]:
          get_most_cells(i,j,player,marks[player])
#This function unmarks the possible cells in the grid
def unmark_possible_cells():
    for i in range(N):
      for j in range(M):
        if grid[i][j] == '?':
          grid[i][j] = '.'
#This function clears the game structures
def grid_clear():
    for i in range(N):
      for j in range(M):
        grid[i][j] = '.'
    count_cells[0] = 0
    count_cells[1] = 0
    grid[3][4] = marks[0];
    grid[4][3] = marks[0];
    grid[3][3] = marks[1];
    grid[4][4] = marks[1];
#This function reads a valid position input
def read_input():
    i, j = map(int, input('Enter the row index and column index: ').split())
    while not check_valid_position(i, j) or not check_empty(i, j) or not check_chosen(i, j):
        i, j = map(int, input('Enter a valid row index and a valid column index: ').split())
    return i, j
#MAIN FUNCTION
def play_game():
    print("Reversi Game!")
    print("Welcome...")
    print("============================")
    player = 0
    while True:
        #Generate the possible cells to be chosen
        generate_possible_cells(player)
        #Prints the grid
        print_grid()
        print('Player %s is playing now' % marks[player])
        #Keep the player if there is not an ability with the other player
        if not check_player_ability():
            print('Sorry, you can not play on this turn!')
            #Player number changes after each turn
            player = 1 - player
            continue
        #Read an input position from the player
        i, j = read_input()
        #Unmark the possible cells
        unmark_possible_cells()
        #Set the player mark in the input position
        set_cell(i, j, marks[player])
        #Switch the neighbor cells of the given cell
        switch_cells(i, j, player)
        #Calculates the total number of cells for each player
        calc_cells()
        #Check if the grid has a full state
        if check_full():
            #Prints the grid
            print_grid()
            #Announcement of the final statement
            if count_cells.count(max(count_cells)) == 1:
                idx_max_player = count_cells.index(max(count_cells))
                print('Congrats, Player %s is won!' % marks[idx_max_player])
            else:
                print("Woah! That's a tie!")
            break
        #Player number changes after each turn
        player = 1 - player
while True:
  grid_clear()
  play_game()
  c = input('Play Again [Y/N] ')
  if c not in 'yY':
    break
