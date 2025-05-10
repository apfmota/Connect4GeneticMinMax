# não sei se esse código realmente vai ser utilizado,
# escrevi pra ver se eu entendi a lógica do minMax
import copy

class State:
    def __init__(self, board, lastPlayer, lastMove=None):
        self.board = copy.deepcopy(board)
        self.lastPlayer = lastPlayer
        self.currentPlayer = 2 if lastPlayer == 1 else 1
        self.lastMove = lastMove
    
    def getNextStates(self, state):
        possibleStates = []
        for j in range(5):
            for i in range(4, -1, -1):
                if state.board[i][j] == 0:
                    newState = State(state.board, state.currentPlayer, lastMove=(i, j))
                    newState.board[i][j] = state.currentPlayer
                    possibleStates.append(newState)
                    break
        return possibleStates

def getInitialState():
    return State([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ], 2)    

def minMax(state: State, depth, alfa, beta):
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
            #return evaluate(state) --- Falta implementar a funcao de avaliacao
            return 0
    possibleStates = state.getNextStates(state)

    if state.currentPlayer == 1:
        bestValue = float('-inf')
        for possibleState in possibleStates:
            bestValue = max(bestValue, minMax(possibleState, depth - 1, alfa, beta))
            alfa = max(alfa, bestValue)
            if beta <= alfa:
                break
        return bestValue
    else:
        bestValue = float('inf')
        for possibleState in possibleStates:
            bestValue = min(bestValue, minMax(possibleState, depth - 1, alfa, beta))
            beta = min(beta, bestValue)
            if beta <= alfa:
                break
        return bestValue
        
def isTerminal(state):
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

def evaluate(state):
    # calcula a funcao de avaliacao (pesos e etc)
    pass

# testando o minMax
print(minMax(getInitialState(), 10, float('-inf'), float('inf')))