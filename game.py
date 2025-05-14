import minMax
import os
import glob
from PIL import Image

class Game:
    def __init__(self, player1, player2, depth, generateGif=False):
        self.depth = depth
        self.player1 = player1
        self.player2 = player2
        self.state = minMax.getInitialState()
        self.generateGif = generateGif
    
    def play(self):
        frame = 0
        while True:
            if self.state.currentPlayer == 1:
                move = self.findBestMove()
            else:
                move = self.findBestMove()
            
            self.state = self.state.makeMove(move)

            terminal, winner = minMax.isTerminal(self.state)    
            if (self.generateGif):
                self.state.generateFrame(frame, terminal, winner)
            frame += 1
            
            if terminal:
                if self.generateGif:
                    makeGif()
                    cleanupFrames()
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
    
def cleanupFrames():
    for f in glob.glob("frame_*.png"):
        os.remove(f)

def makeGif(output_filename="output.gif", duration=500):
    frames = sorted(glob.glob("frame_*.png"), key=lambda x: int(x.split('_')[1].split('.')[0]))
    images = [Image.open(f).convert('RGBA') for f in frames]

    if images:
        images[0].save(output_filename,
                       save_all=True,
                       append_images=images[1:],
                       duration=duration,
                       loop=0)

game = Game([1, -1, 1, -1], [1, -1, 1, -1], 4, generateGif=True)
print(game.play())