# não sei se esse código realmente vai ser utilizado,
# escrevi pra ver se eu entendi a lógica do minMax
import copy
import numpy as np
import matplotlib.pyplot as plt

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

    def generateFrame(self, frame, terminal, winner):

        fig, ax = plt.subplots()
        ax.set_xticks(np.arange(-0.5, 5, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 5, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        for i in range(5):
            for j in range(5):
                if self.board[i][j] == 1:
                    ax.text(j, 4 - i, 'O', ha='center', va='center', fontsize=20, color='blue')
                elif self.board[i][j] == 2:
                    ax.text(j, 4 - i, 'O', ha='center', va='center', fontsize=20, color='red')

        ax.set_xlim(-0.5, 4.5)
        ax.set_ylim(-0.5, 4.5)
        ax.set_xticks([])
        ax.set_yticks([])

        if terminal:
            if winner == 1:
                ax.text(2, -0.8, 'Player 1 wins!', ha='center', va='center', fontsize=20, color='blue')
            elif winner == 2:
                ax.text(2, -0.8, 'Player 2 wins!', ha='center', va='center', fontsize=20, color='red')
            else:
                ax.text(2, -0.8, 'Draw!', ha='center', va='center', fontsize=20, color='black')

        filename = f"frame_{frame}.png"
        plt.savefig(filename)
        plt.close(fig)

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
            return evaluate(state, weights)
        
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

    return state.moveCount == 25, 0

def evaluate(state, weights):
    eval = 0

    metrics = get_metrics(state)
    for i in range(len(metrics)):
        eval += metrics[i] * weights[i]

    return eval

def get_metrics(state):
    return [
        getSequences(2, state, 1), # numero de duplas abertas jogador 1
        getSequences(2, state, 2), # numero de duplas abertas jogador 2
        getSequences(3, state, 1), # numero de trincas abertas jogador 1
        getSequences(3, state, 2), # numero de trincas abertas jogador 2
    ]

def getSequences(sequenceSize, state, player):
    triples = 0
    # horizontal
    for i in range(5):
        sequentialPieces = 0
        for j in range(5):
            if state.board[i][j] == player:
                sequentialPieces += 1
            else:
                sequentialPieces = 0
            # 3 em sequencia com um vazio antes ou depois
            if sequentialPieces >= sequenceSize and ((j > sequenceSize -1 and  state.board[i][j - sequenceSize] == 0) or (j < 4 and state.board[i][j + 1] == 0)):
                triples += 1
    # vertical
    for i in range(5):
        sequentialPieces = 0
        for j in range(5):
            if state.board[j][i] == player:
                sequentialPieces += 1
            else:
                sequentialPieces = 0
            # 3 em sequencia com um vazio antes ou depois
            if sequentialPieces >= sequenceSize and ((j > sequenceSize - 1 and state.board[j - sequenceSize][i] == 0) or (j < 4 and state.board[j + 1][i] == 0)):
                triples += 1

    # diagonal esquerda -> direita
    for i in range(5):
        sequentialPieces = 0
        row, col = i, 0
        while row < 5 and col < 5:
            if state.board[row][col] == player:
                sequentialPieces += 1
            else:
                sequentialPieces = 0
            # 3 em sequencia com um vazio antes ou depois
            if sequentialPieces >= sequenceSize and ((row > sequenceSize - 1 and col > sequenceSize - 1 and state.board[row - sequenceSize][col - sequenceSize] == 0) or (row < 4 and col < 4 and state.board[row + 1][col + 1] == 0)):
                triples += 1
            row += 1
            col += 1

    # diagonal topo -> direita
    for i in range(1, 5):
        sequentialPieces = 0
        row, col = 0, i
        while row < 5 and col < 5:
            if state.board[row][col] == player:
                sequentialPieces += 1
            else:
                sequentialPieces = 0
            # 3 em sequencia com um vazio antes ou depois
            if sequentialPieces >= sequenceSize and ((row > sequenceSize - 1 and col > sequenceSize - 1 and state.board[row - sequenceSize][col - sequenceSize] == 0) or (row < 4 and col < 4 and state.board[row + 1][col + 1] == 0)):
                triples += 1
            row += 1
            col += 1

    # diagonal direita -> esquerda
    for i in range(5):
        sequentialPieces = 0
        row, col = i, 4
        while row < 5 and col >= 0:
            if state.board[row][col] == player:
                sequentialPieces += 1
            else:
                sequentialPieces = 0
            # 3 em sequencia com um vazio antes ou depois
            if sequentialPieces >= sequenceSize and ((row > sequenceSize - 1 and col + sequenceSize < 5 and state.board[row - sequenceSize][col + sequenceSize] == 0) or (row < 4 and col > 0 and state.board[row + 1][col - 1] == 0)):
                triples += 1
            row += 1
            col -= 1
    
    # diagonal topo -> esquerda
    for i in range(4):
        sequentialPieces = 0
        row, col = 0, i
        while row < 5 and col >= 0:
            if state.board[row][col] == player:
                sequentialPieces += 1
            else:
                sequentialPieces = 0
            # 3 em sequencia com um vazio antes ou depois
            if sequentialPieces >= sequenceSize and ((row > sequenceSize - 1 and col + sequenceSize < 5 and state.board[row - sequenceSize][col + sequenceSize] == 0) or (row < 4 and col > 0 and state.board[row + 1][col - 1] == 0)):
                triples += 1
            row += 1
            col -= 1

    return triples