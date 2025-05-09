# Agente Inteligente para o Jogo Connect-4 (5x5)

Este projeto implementa um agente inteligente para o jogo **Connect-4 em um tabuleiro 5x5**, onde o objetivo é alinhar 4 peças consecutivas (horizontal, vertical ou diagonal). O agente toma decisões utilizando o algoritmo **Min-Max com poda Alfa-Beta** e uma **função de avaliação otimizada por Algoritmo Genético**.

## Etapas do Projeto

### 1. Min-Max com Poda Alfa-Beta
- Implementação do algoritmo Min-Max com profundidade limitada (3 a 5 jogadas futuras).
- Utiliza poda Alfa-Beta para otimizar a busca e reduzir o número de estados avaliados.

### 2. Função de Avaliação Personalizada
- Baseada em pelo menos 3 características do tabuleiro, como:
  - Número de linhas abertas (sem peças do oponente).
  - Número de trincas formadas (3 peças em sequência).
  - Controle das colunas centrais.
- Cada característica tem um peso ajustável (ex.: `w1`, `w2`, `w3`).

### 3. Algoritmo Genético (AG)
- Evolui os pesos da função de avaliação ao longo de gerações.
- Cada indivíduo representa um conjunto de pesos reais.
- A função de fitness avalia o desempenho dos agentes em partidas contra adversários.
- Utiliza torneio interno entre os indivíduos de cada geração.
