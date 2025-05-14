import minMax

class Game:
    def __init__(self, player1, player2, depth, printResults=False):
        self.depth = depth
        self.player1 = player1
        self.player2 = player2
        self.state = minMax.getInitialState()
        self.printResults = printResults
    
    def play(self):
        while True:
            if self.state.currentPlayer == 1:
                move = self.findBestMove()
            else:
                move = self.findBestMove()
            
            self.state = self.state.makeMove(move)
            if self.printResults:
                print(f"Jogador {self.state.lastPlayer} jogou: {move}")
                self.state.printBoard()
            
            terminal, winner = minMax.isTerminal(self.state)
            if terminal:
                if self.printResults:
                    if winner == 0:
                        print("Empate!")
                    else:
                        print(f"Jogador {winner} venceu!")
                return winner
    
    def findBestMove(self):
        if self.state.currentPlayer == 1:
            bestValue = float('-inf')
            bestMove = None
            for possibleState in self.state.getNextStates():
                value = minMax.minMax(possibleState, self.depth, float('-inf'), float('inf'), self.player1)
                if value > bestValue or bestMove is None:
                    bestValue = max(bestValue, value)
                    bestMove = possibleState.lastMove
            return bestMove
        else:
            bestValue = float('inf')
            bestMove = None
            for possibleState in self.state.getNextStates():
                value = minMax.minMax(possibleState, self.depth, float('-inf'), float('inf'), self.player2)
                if value < bestValue or bestMove is None:
                    bestValue = min(bestValue, value)
                    bestMove = possibleState.lastMove
            return bestMove
    

game = Game([1, -1, 1, -1], [1, -1, 1, -1], 4, printResults=True)
print(game.play())