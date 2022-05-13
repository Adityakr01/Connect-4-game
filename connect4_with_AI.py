import numpy as np
import random
import pygame
import sys
import math

YELLOW = (255,255,0)     #Red Green Blue  value of our UI
ROYAL_BLUE = (65, 105, 225)      #background of the UI
RED = (255,0,0)      #color of ball/player1
BLACK = (0,0,0) #color of ball/player2

ROW_COUNT = 6        #total number of rows
COLUMN_COUNT = 7     #total number of column

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4 

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))  #6 rows 7 columns
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0     #checking wheather  it is valid location or not

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):      #without this function piece is enter from the top of the board but after using this function the piece is located in bottom 
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Checking all the horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Checking all the  vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def evaluate_window(window , piece):
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
	    score += 5 

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 3:
		score -= 80

	return score	


def score_position(board ,piece):

	score = 0
	#adding prefernce for the centre pieces
	centre_array = [int(i) fo i in list(board[:,COLUMN_COUNT//2])]
	centr_count = centre_array.count(piece)
	score += create_board * 6


#AI fill the ball in horizontal to win the game
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window .piece)

	#AI fill the ball in vertical to win the game
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			
			score += evaluate_window(window .piece)

	#score postive slope diagnoal
	
	for r in range (ROW_COUNT - 3):
		for c in range(COLUMN_COUNT -3):
			window = [board[r+i][c+i] for i in range (WINDOW_LENGTH)]
			score += evaluate_window(window .piece)
    
    #score negative slope diagnoal
    
    for r in range(ROW_COUNT-3):
    	for r in range(COLUMN_COUNT -3):
    		window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
    		score += evaluate_window(window .piece)

	return score
def is_terminal_node(board):
	return winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth ,maximixingPlayer):      # minimax algorithm  implementation
	valid_locations = get_valid_locations(board)
	terminal_node = is_terminal_node(board)
	if depth == 0 or is terminal:	      #terminal winning is us winnnigng ,opp winning or draw
		if is_terminal:
		    if winning_move(board , AI_PIECE):
			    return 1000000000000000000
		    elif winning_move(board , PLAYER_PIECE):
			    return -1000000000000000000
		    else:  #game is over,no more valid moves
			    return 0
		else: #depth is zero
			return score_position(board , AI_PIECE)
	if maximixingPlayer:
		value = math.inf
		for col in valid_locations:
			row = get_next_open_row(board,col)
			b_copy = board.copy()
			drop_piece(b_copy ,row, col,)


def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board , col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):            #algorithm
	
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board ,row, col ,piece)
		score = score_position(temp_board ,piece)
		if score > best_score:
			best_score = score
			best_col =col

	return best_col

#here we draw 
def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, YELLOW, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)) #draw a rectangle around a point
			pygame.draw.circle(screen, ROYAL_BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


board = create_board()
print_board(board)
game_over = False


#here we design our UI for the game

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER,AI)  #random is used to change wheather AI go first or Player

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		#this is for the jo upr wala empty bar hai usme player colour represent karne ke liye hai

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, ROYAL_BLUE, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, ROYAL_BLUE, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True
					
					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)


			# # Ask for Player 2 Input
	if turn == AI and not game_over:				
		#col = random.randint(0 , COLUMN_COUNT-1)
		col = pick_best_move(board,AI_PIECE)


		if is_valid_location(board, col):
			pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if winning_move(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, BLACK)
				screen.blit(label, (40,10))
				game_over = True

		print_board(board)
		draw_board(board)

		turn += 1
		turn = turn % 2

	if game_over:
		pygame.time.wait(3000)