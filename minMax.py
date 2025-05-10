# não sei se esse código realmente vai ser utilizado,
# escrevi pra ver se eu entendi a lógica do minMax

class State:
    def __init__(self, board, player, lastMove=None):
        self.board = board
        self.player = player
        self.lastMove = lastMove
    
    def getNextStates(self, state):
        possivleStates = []
        for i in range(4, -1, -1):
            for j in range(5):
                if state.board[i][j] == 0:
                    newState = State(state.board, 1 if state.player == 2 else 2, lastMove=(i, j))
                    newState.board[i][j] = state.player
                    possivleStates.append(newState)
        return possivleStates

def getInitialState():
    return State([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ], 1)    

def minMax(state: State, depth, alfa, beta):
    terminal, winner = isTerminal(state)
    if terminal or depth == 0:
        if terminal:
            if winner == 1:
                return float('inf')
            elif winner == 2:
                return float('-inf')
        else:
            #if not terminal:
            #    return evaluate(state) --- Falta implementar a funcao de avaliacao
            return 0
    possibleStates = state.getNextStates(state)

    if state.player == 1:
        bestValue = float('-inf')
        for state in possibleStates:
            bestValue = minMax(state, depth - 1, alfa, beta)
            alfa = max(alfa, bestValue)
            if beta <= alfa:
                break
        return bestValue
    else:
        bestValue = float('inf')
        for state in possibleStates:
            bestValue = minMax(state, depth - 1, alfa, beta)
            beta = min(beta, bestValue)
            if beta >= alfa:
                break
        return bestValue
        
def isTerminal(state):
    #checa 4 na linha:
    if (state.lastMove == None):
        return False, 0
    line = state.lastMove[0]
    sequentialPieces = 0
    for i in range(5):
        if state.board[line][i] == state.player:
            sequentialPieces += 1
            if (sequentialPieces == 4):
                return True, state.player
        else:
            sequentialPieces = 0
    #checa 4 na coluna:
    column = state.lastMove[1]
    sequentialPieces = 0
    for i in range(5):
        if state.board[i][column] == state.player:
            sequentialPieces += 1
            if (sequentialPieces == 4):
                return True, state.player
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
        if state.board[startRow][startCol] == state.player:
            sequentialPieces += 1
            if sequentialPieces == 4:
                return True, state.player
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
        if state.board[startRow][startCol] == state.player:
            sequentialPieces += 1
            if sequentialPieces == 4:
                return True, state.player
        else:
            sequentialPieces = 0
        startRow += 1
        startCol -= 1

    return False, 0

def evaluate(state):
    # calcula a funcao de avaliacao (pesos e etc)
    pass

print(minMax(getInitialState(), 10, float('-inf'), float('inf')))