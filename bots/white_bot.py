from copy import deepcopy
from time import time
from checkers.board import *
from checkers.constants import *

# Global Constants
MaxUtility = 1e9
IsPlayerBlack = False
MaxAllowedTimeInSeconds = 9.5
MaxDepth = 100

class CheckersState:
    def __init__(self, grid, blackToMove, moves):
        self.grid = grid
        self.blackToMove = blackToMove
        self.moves = moves  # Hops taken by a disc to reach the current state

  # This just checks for whether or not all pieces of a player have been eliminated.
  # It does not check for whether a player has a move or not. In that case, there will
  # be no successors for that player and alpha beta search will return Min/Max Utility.
    def isTerminalState(self):
        redSeen, whiteSeen = False, False
        for row in self.grid:
            for cell in row:
                if cell.color == RED: redSeen = True
                elif cell.color == WHITE: whiteSeen = True
                if redSeen and whiteSeen: return False
        self.isLoserBlack = whiteSeen
        return True

    def getTerminalUtility(self):
        return MaxUtility if IsPlayerBlack != self.isLoserBlack else -MaxUtility

    def getSuccessors(self):
        def getSteps(cell):
            whiteSteps = [(1, -1), (1, 1)]
            redSteps = [(-1, -1), (-1, 1)]
            steps = []
            if cell.king == True: steps.extend(whiteSteps, redSteps)
            if cell.color == RED and cell.king == False: steps.extend(redSteps)
            if cell.color == WHITE and cell.king == False: steps.extend(whiteSteps)
            return steps

        def generateMoves(board, i, j, successors):
            for step in getSteps(board[i][j]):
                x, y = i + step[0], j + step[1]
                if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] == 0:
                    boardCopy = deepcopy(board)
                    boardCopy[x][y], boardCopy[i][j] = boardCopy[i][j], 0
                    # A pawn is promoted when it reaches the last row
                    if (x == 7 and self.blackToMove) or (x == 0 and not self.blackToMove):
                        boardCopy[x][y] = boardCopy[x][y].upper()
                    successors.append(CheckersState(boardCopy, not self.blackToMove, [(i, j), (x, y)]))

        def generateJumps(board, i, j, moves, successors):
            jumpEnd = True
            for step in getSteps(board[i][j]):
                x, y = i + step[0], j + step[1]
                if x >= 0 and x < 8 and y >= 0 and y < 8 and board[x][y] != 0 and board[i][j] != board[x][y]:
                    xp, yp = x + step[0], y + step[1]
                    if xp >= 0 and xp < 8 and yp >= 0 and yp < 8 and board[xp][yp] == 0:
                        board[xp][yp], save = board[i][j], board[x][y]
                        board[i][j] = board[x][y] = 0
                        previous = board[xp][yp]
                        # A pawn is promoted when it reaches the last row
                        if (xp == 7 and self.blackToMove) or (xp == 0 and not self.blackToMove):
                            board[xp][yp] = board[xp][yp].upper()

                        moves.append((xp, yp))
                        generateJumps(board, xp, yp, moves, successors)
                        moves.pop()
                        board[i][j], board[x][y], board[xp][yp] = previous, save, 0
                        jumpEnd = False
            if jumpEnd and len(moves) > 1:
                successors.append(CheckersState(deepcopy(board), not self.blackToMove, deepcopy(moves)))

        player = RED if self.blackToMove else WHITE
        successors = []

        # generate jumps
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == player:
                    generateJumps(self.grid, i, j, [(i, j)], successors)
        if len(successors) > 0: return successors

        # generate moves
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] == player:
                    generateMoves(self.grid, i, j, successors)
        return successors

class WhiteBot:
    def piecesCount(state):
        # 1 for a normal piece, 1.5 for a king
        red, white = 0, 0
        for row in state.grid:
            for cell in row:
                if cell.color == RED and cell.king == True: red += 1.5
                if cell.color == WHITE and cell.king == True: white += 1.5
                elif cell.color == RED: red += 1.0
                elif cell.color == WHITE: white += 1.0
        return red - white if IsPlayerBlack else white - red

    def iterativeDeepeningAlphaBeta(state, evaluationFunc):
        startTime = time()

        def alphaBetaSearch(state, alpha, beta, depth):
            def maxValue(state, alpha, beta, depth):
                val = -MaxUtility
                for successor in state.getSuccessors():
                    val = max(val, alphaBetaSearch(successor, alpha, beta, depth))
                    if val >= beta: return val
                    alpha = max(alpha, val)
                return val

            def minValue(state, alpha, beta, depth):
                val = MaxUtility
                for successor in state.getSuccessors():
                    val = min(val, alphaBetaSearch(successor, alpha, beta, depth - 1))
                    if val <= alpha: return val
                    beta = min(beta, val)
                return val

            if state.isTerminalState(): return state.getTerminalUtility()
            if depth <= 0 or time() - startTime > MaxAllowedTimeInSeconds: return evaluationFunc(state)
            return maxValue(state, alpha, beta, depth) if state.blackToMove == IsPlayerBlack else minValue(state, alpha, beta, depth)

        bestMove = None
        for depth in range(1, MaxDepth):
            if time() - startTime > MaxAllowedTimeInSeconds: break
            val = -MaxUtility
            for successor in state.getSuccessors():
                score = alphaBetaSearch(successor, -MaxUtility, MaxUtility, depth)
                if score > val:
                    val, bestMove = score, successor.moves
        return bestMove