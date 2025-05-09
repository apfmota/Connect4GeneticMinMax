# não sei se esse código realmente vai ser utilizado,
# escrevi pra ver se eu entendi a lógica do minMax

# nao ta implementado poda
def minMax(state, depth, player):
    if isTerminal(state) or depth == 0:
        return evaluate(state)
    possibleStates = getPossibleStates(state)
    if player == 1:
        bestValue = float('-inf')
        for state in possibleStates:
            value = minMax(state, depth - 1, 2)
            if value > bestValue:
                bestValue = value
        return bestValue
    else:
        bestValue = float('inf')
        for state in possibleStates:
            value = minMax(state, depth - 1, 1)
            if value < bestValue:
                bestValue = value
        return bestValue
        
def isTerminal(state):
    # testa se acabou o jogo
    pass

def evaluate(state):
    # calcula a funcao de avaliacao (pesos e etc)
    pass

def getPossibleStates(state):
    # retorna os estados possiveis a partir do estado atual
    pass