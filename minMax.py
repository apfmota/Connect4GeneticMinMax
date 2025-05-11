# não sei se esse código realmente vai ser utilizado,
# escrevi pra ver se eu entendi a lógica do minMax
import copy

class State:
    def __init__(self, board, currentPlayer, lastMove=None):
        self.board = copy.deepcopy(board)
        self.lastPlayer = 1 if currentPlayer == 2 else 2 
        self.currentPlayer = currentPlayer
        self.lastMove = lastMove
        self.moveCount = 0
    
    def getNextStates(self):
        possibleStates = []
        for j in range(5):
            for i in range(4, -1, -1):
                if self.board[i][j] == 0:
                    newState = self.makeMove((i, j))
                    possibleStates.append(newState)
                    break
        return possibleStates
    
    def makeMove(self, move):
        newState = State(self.board, self.lastPlayer, lastMove=move)
        newState.board[move[0]][move[1]] = self.currentPlayer
        newState.moveCount = self.moveCount + 1
        return newState
    
    def printBoard(self):
        for line in self.board:
            print(' '.join(map(str, line)))

def getInitialState():
    return State([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ], 1)    

def minMax(state: State, depth, alfa, beta, weights):
    terminal, winner = isTerminal(state)
    if terminal or depth == 0:
        if terminal:
            if winner == 1:
                return float('inf')
            elif winner == 2:
                return float('-inf')
            else:
                return 0
        else:
            return 0
            #return evaluate(state, weights)
        
    possibleStates = state.getNextStates()

    if state.currentPlayer == 1:
        bestValue = float('-inf')
        for possibleState in possibleStates:
            bestValue = max(bestValue, minMax(possibleState, depth - 1, alfa, beta, weights))
            alfa = max(alfa, bestValue)
            if beta <= alfa:
                break
        return bestValue
    else:
        bestValue = float('inf')
        for possibleState in possibleStates:
            bestValue = min(bestValue, minMax(possibleState, depth - 1, alfa, beta, weights))
            beta = min(beta, bestValue)
            if beta <= alfa:
                break
        return bestValue
        
def isTerminal(state):
    #tabuleiro cheio:
    if state.moveCount == 25:
        return True, 0
    #checa 4 na linha:
    if (state.lastMove == None):
        return False, 0
    line = state.lastMove[0]
    sequentialPieces = 0
    for i in range(5):
        if state.board[line][i] == state.lastPlayer:
            sequentialPieces += 1
            if (sequentialPieces == 4):
                return True, state.lastPlayer
        else:
            sequentialPieces = 0
    #checa 4 na coluna:
    column = state.lastMove[1]
    sequentialPieces = 0
    for i in range(5):
        if state.board[i][column] == state.lastPlayer:
            sequentialPieces += 1
            if (sequentialPieces == 4):
                return True, state.lastPlayer
        else:
            sequentialPieces = 0

    #checa 4 na diagonal topo-esquerda -> baixo-direita:
    row, col = state.lastMove
    sequentialPieces = 0
    startRow, startCol = row, col
    while startRow > 0 and startCol > 0:
        startRow -= 1
        startCol -= 1

    while startRow < 5 and startCol < 5:
        if state.board[startRow][startCol] == state.lastPlayer:
            sequentialPieces += 1
            if sequentialPieces == 4:
                return True, state.lastPlayer
        else:
            sequentialPieces = 0
        startRow += 1
        startCol += 1

    #checa 4 na diagonal topo-direita -> baixo-esquerda:
    sequentialPieces = 0
    startRow, startCol = row, col
    while startRow > 0 and startCol < 4:
        startRow -= 1
        startCol += 1

    while startRow < 5 and startCol >= 0:
        if state.board[startRow][startCol] == state.lastPlayer:
            sequentialPieces += 1
            if sequentialPieces == 4:
                return True, state.lastPlayer
        else:
            sequentialPieces = 0
        startRow += 1
        startCol -= 1
    
    return False, 0

def evaluate(state, weights):
    eval = 0

    metrics = get_metrics(state)
    for i in range(len(metrics)):
        eval += metrics[i] * weights[i]

    return eval

def get_metrics(state):
    pass