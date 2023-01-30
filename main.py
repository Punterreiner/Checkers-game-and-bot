import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.board import Board
from bots.white_bot import WhiteBot, CheckersState 


FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    selected_piece = None
    red = True
    
    while run:
        clock.tick(FPS)

        #if red == False:
            #state = CheckersState(board.board, True, [])
            #move = WhiteBot.iterativeDeepeningAlphaBeta(state, WhiteBot.piecesCount)
            #print(move)
            #for step in move:
                #print(step[0], step[1])
            
        for event in pygame.event.get():
            
            #print(board.board)
            wl = board.white_left
            rl = board.red_left
            
            run = board.check_win()
            
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                piece = board.get_piece(row, col)
                
                if piece != 0:
                    selected_piece = piece
                    hops = board.check_hop(piece)
                elif piece == 0 and selected_piece != None:
                    if board.check_legal_move(selected_piece, row, col, hops, red):
                        board.move(selected_piece, row, col)
                        if board.check_hop(selected_piece) and (board.red_left < rl or board.white_left < wl):
                            red = red
                        else:
                            red = not red
                            

            board.draw(WIN)
            pygame.display.update()
            
    pygame.quit()
main()