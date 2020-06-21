# -*- coding: utf-8 -*-
"""
Created on Sat May  9 20:42:18 2020

@author: Matheus Ruggeri
"""

# Número de linhas, colunas e quantas peças devem ser ligadas Connect4 -> k = 4
nlin = 6
ncol = 7
k = 4

# Estados possíveis para o tabuleiro
VAZIO   = ' '
MOLDURA = 'm'
XIS     = 'X'
BOLA    = 'O'
    
def main():
    tabuleiro = [["m"]*(ncol+2) for i in range(nlin+2)]
    vez = XIS
    inicializa_tabuleiro(tabuleiro)
    while (True):
        colNum = 0
        while (joga(tabuleiro, colNum, vez) == False):
            colNum = input("Dê o número da coluna ou (q)uit:\t")
            if (colNum.upper() == 'Q' or colNum.upper() == 'QUIT'):
                return 0
            elif (not(colNum.isdigit()) or (int(colNum) < 1 or int(colNum) > ncol)):
                colNum = 0
            else:
                colNum = int(colNum)
        imprime_tabuleiro(tabuleiro)
        if (conta_ligados(tabuleiro,colNum) >= k):
            print("O jogador "+ vez + " ganhou!")
            return 0
        elif (verifica_tabuleiro_cheio(tabuleiro) == True):
            print("O jogo terminou empatado")
            return 0
        vez = BOLA if (vez == XIS) else XIS
        
# INICIALIZA O TABULEIRO
def inicializa_tabuleiro(tabuleiro):
    for i in range(0, nlin+2):
        tabuleiro[i][0] = MOLDURA
        tabuleiro[i][ncol+1] = MOLDURA
    for j in range(0, ncol+2):
        tabuleiro[0][j] = MOLDURA
        tabuleiro[nlin+1][j] = MOLDURA
    for i in range(1,nlin+1):
        for j in range(1,ncol+1):
            tabuleiro[i][j] = VAZIO
    
# IMPRIME O TABULEIRO
def imprime_tabuleiro(tabuleiro): 
    i = 1
    j = 0
    lin = 1
    col = 1
    while (i<nlin+1):
        print("   ", end = '')
        for j in range(1,ncol+1):
             print("+---", end = '')
        print("+")
        print(" " + str(lin), end = ' ')
        lin += 1
        for j in range(1,ncol+1):
            print("| " + tabuleiro[i][j], end = ' ')
        i += 1
        print("|\n", end = '')
    if (i == nlin+1):
        print("   ", end = '+')
        for j in range(1,ncol+1):
            print("---+", end = '')
        print("\n     ", end = '')
        for j in range(1,ncol+1):
            print(str(col), end = '   ')
            col += 1
    print("")

def verifica_tabuleiro_cheio(tabuleiro):
    j = 1
    cheio = True
    # Só precisa checar a primeira linha devido a gravidade presente no jogo
    while (j <= ncol and cheio == True):
        if (tabuleiro[1][j] == VAZIO):
            cheio = False
        j += 1
    return cheio

def joga(tabuleiro, col, tipo):
    # Usa o valor máximo da linha e vai decrescendo, retorna se foi possível fazer a jogada
    lin = nlin
    ehpossivel = False
    jogou = False
    if (tabuleiro[1][col] == VAZIO):
        ehpossivel = True
        while (jogou == False and lin > 0):
            if (tabuleiro[lin][col] == VAZIO):
                tabuleiro[lin][col] = tipo
                jogou = True
            else:
                lin -= 1
    return ehpossivel

def conta_ligados(tabuleiro, coluna):
    lin = 1
    direct = 1
    i = 1; j = 1;
    lig = 1
    maxLig = 1
    left = True
    right = True
    while (tabuleiro[lin][coluna] == MOLDURA or tabuleiro[lin][coluna] == VAZIO):
        lin += 1
    tipo = tabuleiro[lin][coluna]
    while (direct <= 4):
        if (right):
            if (tabuleiro[lin+i][coluna+j] == tipo):
                lig += 1
            else:
                right = False
        if (left):
            if (tabuleiro[lin-i][coluna-j] == tipo):
                lig += 1
            else:
                left = False
        if (not left and not right):
            left = True
            right = True
            direct += 1
            i = 0 
            j = 0
            if (lig > maxLig):
                maxLig = lig
            lig = 1            
        if (direct == 1): # Diag -> \ <-
            i += 1
            j += 1
        if (direct == 2): # Diag -> / <-
            i -= 1
            j += 1
        if (direct == 3): # Col  -> | <-
            i += 1
        if (direct == 4): # Lin  -> - <-
            j += 1
    return maxLig

main()
