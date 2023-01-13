import pygame
from .constants import BLACK, ROWS, RED, WHITE, SQUARE_SIZE, COLS
from .piece import Piece

class Board:
    
    def __init__(self):
        self.board = []
        self.selcted_piece = None
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
        
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
          
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            if piece.color == RED:
                self.red_kings += 1
    
    def check_legal_move(self, piece, row, col, hops, red): 
        if ( piece.row + 1 == row or piece.row - 1 == row) and row%2 != col%2 and (piece.col + 1 == col or piece.col - 1 >= col):
            print(piece)
            if piece.king == True:
                if piece.color == WHITE and red == False:    
                    return True
                elif piece.color == RED and red == True:
                    return True 
            if piece.color == WHITE and piece.row + 1 == row and red == False:
                return True
            if piece.color == RED and piece.row - 1 == row and red == True:
                return True
            else:
                return False
            
        elif hops != None:
            if piece.king == True:
                if piece.color == WHITE and row%2 != col%2 and red == False:
                    for hop in hops:
                        if row == hop.row + 1 and col == hop.col - 1:
                            self.board[hop.row][hop.col] = 0
                            self.red_left -= 1
                            return True
                        elif row == hop.row + 1 and col == hop.col + 1:
                            self.board[hop.row][hop.col] = 0
                            self.red_left -= 1
                            return True
                        elif row == hop.row - 1 and col == hop.col - 1:
                            self.board[hop.row][hop.col] = 0
                            self.white_left -= 1
                            return True
                        elif row == hop.row - 1 and col == hop.col + 1:
                            self.board[hop.row][hop.col] = 0
                            self.white_left -= 1
                            return True
                elif piece.color == RED and row%2 != col%2 and red == True:
                    for hop in hops:
                        if row == hop.row + 1 and col == hop.col - 1:
                            self.board[hop.row][hop.col] = 0
                            self.red_left -= 1
                            return True
                        elif row == hop.row + 1 and col == hop.col + 1:
                            self.board[hop.row][hop.col] = 0
                            self.red_left -= 1
                            return True
                        elif row == hop.row - 1 and col == hop.col - 1:
                            self.board[hop.row][hop.col] = 0
                            self.white_left -= 1
                            return True
                        elif row == hop.row - 1 and col == hop.col + 1:
                            self.board[hop.row][hop.col] = 0
                            self.white_left -= 1
                            return True  
            elif piece.color == WHITE and row%2 != col%2 and red == False:
                for hop in hops:
                    if row == hop.row + 1 and col == hop.col - 1:
                        self.board[hop.row][hop.col] = 0
                        self.red_left -= 1
                        return True
                    elif row == hop.row + 1 and col == hop.col + 1:
                        self.board[hop.row][hop.col] = 0
                        self.red_left -= 1
                        return True
            elif piece.color == RED and row%2 != col%2 and red == True:
                for hop in hops:
                    if row == hop.row - 1 and col == hop.col - 1:
                        self.board[hop.row][hop.col] = 0
                        self.white_left -= 1
                        return True
                    elif row == hop.row - 1 and col == hop.col + 1:
                        self.board[hop.row][hop.col] = 0
                        self.white_left -= 1
                        return True
    
    def check_hop(self, piece):
        hops = [] 
        if piece != 0 and piece.col != COLS - 1:
            print(piece.row, piece.col)
            if piece.king == True:                
                if piece.color == WHITE:
                    if piece.row < ROWS - 2:
                        SOUTHWEST = self.board[piece.row + 1][piece.col - 1]
                        SOUTHEAST = self.board[piece.row + 1][piece.col + 1]
                        if SOUTHEAST != 0 and SOUTHEAST.color == RED and piece.col + 2 <= COLS - 1 and self.board[piece.row + 2][piece.col + 2] == 0:
                            hops.append(SOUTHEAST)
                        if SOUTHWEST != 0 and SOUTHWEST.color == RED  and piece.col - 2 >= 0 and self.board[piece.row + 2][piece.col - 2] == 0:
                            print("hop")
                            hops.append(SOUTHWEST)
                    if piece.row > 1:
                        NORTHWEST = self.board[piece.row - 1][piece.col - 1]
                        NORTHEAST = self.board[piece.row - 1][piece.col + 1]
                        if NORTHEAST != 0 and NORTHEAST.color == RED and piece.col + 2 <= COLS - 1 and self.board[piece.row - 2][piece.col + 2] == 0:
                            print("hop")
                            hops.append(NORTHEAST)
                        if NORTHWEST != 0 and NORTHWEST.color == RED and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                            print("hop")
                            hops.append(NORTHWEST)
                elif piece.color == RED:
                    if piece.row < ROWS - 2:
                        SOUTHWEST = self.board[piece.row + 1][piece.col - 1]
                        SOUTHEAST = self.board[piece.row + 1][piece.col + 1]
                        if SOUTHEAST != 0 and SOUTHEAST.color == WHITE and piece.col + 2 <= COLS - 1 and self.board[piece.row + 2][piece.col + 2] == 0:
                            hops.append(SOUTHEAST)
                        if SOUTHWEST != 0 and SOUTHWEST.color == WHITE  and piece.col - 2 >= 0 and self.board[piece.row + 2][piece.col - 2] == 0:
                            print("hop")
                            hops.append(SOUTHWEST)
                    if piece.row > 1:
                        NORTHWEST = self.board[piece.row - 1][piece.col - 1]
                        NORTHEAST = self.board[piece.row - 1][piece.col + 1]
                        if NORTHEAST != 0 and NORTHEAST.color == WHITE and piece.col + 2 <= COLS - 1 and self.board[piece.row - 2][piece.col + 2] == 0:
                            print("hop")
                            hops.append(NORTHEAST)
                        if NORTHWEST != 0 and NORTHWEST.color == WHITE and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                            print("hop")
                            hops.append(NORTHWEST)
            if piece.color == WHITE and piece.row < ROWS - 2:
                SOUTHWEST = self.board[piece.row + 1][piece.col - 1]
                SOUTHEAST = self.board[piece.row + 1][piece.col + 1]
                if SOUTHEAST != 0 and SOUTHEAST.color == RED and piece.col + 2 <= COLS - 1 and self.board[piece.row + 2][piece.col + 2] == 0:
                    print("hop")
                    hops.append(SOUTHEAST)
                if SOUTHWEST != 0 and SOUTHWEST.color == RED  and piece.col - 2 >= 0 and self.board[piece.row + 2][piece.col - 2] == 0:
                    print("hop")
                    hops.append(SOUTHWEST)

            elif piece.color == RED and piece.row > 1:
                NORTHWEST = self.board[piece.row - 1][piece.col - 1]
                NORTHEAST = self.board[piece.row - 1][piece.col + 1]
                if NORTHEAST != 0 and NORTHEAST.color == WHITE and piece.col + 2 <= COLS - 1 and self.board[piece.row - 2][piece.col + 2] == 0:
                    print("hop")
                    hops.append(NORTHEAST)
                if NORTHWEST != 0 and NORTHWEST.color == WHITE and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                    print("hop")
                    hops.append(NORTHWEST)
                
        elif piece != 0 and piece.col == COLS -1:
            NORTHWEST = self.board[piece.row - 1][piece.col - 1]
            SOUTHWEST = self.board[piece.row + 1][piece.col - 1]
            if piece.king == True:
                if piece.color == WHITE:
                    if NORTHWEST != 0 and NORTHWEST.color == RED and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                        print(piece.row, piece.col)
                        print("hop")
                        hops.append(NORTHWEST)
                    if SOUTHWEST != 0 and SOUTHWEST.color == RED and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                        print(piece.row, piece.col)
                        print("hop")
                        hops.append(SOUTHWEST)
                elif piece.color == RED:
                    if NORTHWEST != 0 and NORTHWEST.color == WHITE and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                        print(piece.row, piece.col)
                        print("hop")
                        hops.append(NORTHWEST)
                    if SOUTHWEST != 0 and SOUTHWEST.color == WHITE and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                        print(piece.row, piece.col)
                        print("hop")
                        hops.append(SOUTHWEST) 
            elif piece.color == RED and NORTHWEST != 0 and NORTHWEST.color == WHITE and piece.col - 2 >= 0 and self.board[piece.row - 2][piece.col - 2] == 0:
                print(piece.row, piece.col)
                print("hop")
                hops.append(NORTHWEST)      
            elif piece.color == WHITE and SOUTHWEST != 0 and SOUTHWEST.color == RED  and piece.col - 2 >= 0 and self.board[piece.row + 2][piece.col - 2] == 0:
                print(piece.row, piece.col)
                print("hop")
                hops.append(SOUTHWEST)
        print(hops)
        return hops

    def get_piece(self, row, col):
        return self.board[row][col] 
    
    def check_win(self):
        if self.white_left == 0 or  self.red_left == 0:
            return False
        else: return True 
           
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
        
                