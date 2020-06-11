# -*- coding: utf-8 -*-
"""
Created on Sat May  9 20:42:18 2020

@author: jomar
"""

import array

nlin = 5
ncol = 7
k = 4

IMPOSSIVEL = 0
POSSIVEL   = 1

BRANCO  = ' '
MOLDURA = 'm'
NULL    = 'n'
XIS     = 'X'
BOLA    = 'O'
EMPATE  = 'E'

HUMANO     = 'h'
COMPUTADOR = 'c'
    
def main():
    tabuleiro = [["m"]*11 for i in range(11)]
    fim = False
    cont = 0
    vez = XIS
    
    coloca_moldura(tabuleiro)
    while (fim != True):
        colNum = 0
        while (joga(tabuleiro, colNum, vez) == IMPOSSIVEL):
            colNum = input("Dê o número da coluna ou (q)uit:\t")
            if (colNum.upper() == 'Q'):
                return 0
            elif not(colNum.isdigit()):
                colNum = 0
            elif (int(colNum) < 1 or int(colNum) > ncol):
                colNum = 0
            else:
                colNum = int(colNum)
        imprime_tabuleiro(tabuleiro)
        cont = conta_ligados(tabuleiro,colNum)
        print(cont)
        if (cont >= k):
            fim = True
            vencedor = vez
        elif (verifica_tabuleiro_cheio(tabuleiro) == True):
            fim = True
            vencedor = EMPATE
        if(vez == XIS):
            vez = BOLA
        elif(vez == BOLA):
            vez = XIS
        
    print("O jogador "+ vencedor + " ganhou!")

# INICIALIZA O TABULEIRO
def coloca_moldura(tabuleiro):
    for i in range(0, nlin+2):
        tabuleiro[i][0] = MOLDURA
        tabuleiro[i][ncol+1] = MOLDURA
    for j in range(0, ncol+2):
        tabuleiro[0][j] = MOLDURA
        tabuleiro[nlin+1][j] = MOLDURA
    for i in range(1,nlin+1):
        for j in range(1,ncol+1):
            tabuleiro[i][j] = BRANCO
    
# IMPRIME O TABULEIRO
def imprime_tabuleiro(tabuleiro): 
    i = 1
    j = 0
    contalin = 1
    contacol = 1

    while (i<nlin+1):
        print("   ", end = '')
        for j in range(1,ncol+1):
             print("+---", end = '')
        print("+\n", end = '')
        print(" ", end = '')
        print(contalin, end = '')
        contalin += 1
        print(" ", end = '')
        for j in range(1,ncol+1):
            print("| ", end = '')
            if(tabuleiro[i][j] == BOLA):
                print("O ", end = '')
            elif(tabuleiro[i][j] == XIS):
                print("X ", end = '')
            elif(tabuleiro[i][j] == MOLDURA):
                print("M ", end = '')
            elif(tabuleiro[i][j] == BRANCO):
                print(". ", end = '')
            else:
                print("  ", end = '')
        i += 1
        print("|\n", end = '')
    if (i == nlin+1):
        print("   ", end = '')
        for j in range(1,ncol+1):
            print("+---", end = '')
        print("+\n", end = '')
        print("   ", end = '')
        for j in range(1,ncol+1):
            print("  "+str(contacol)+" ", end = '')
            contacol += 1
    print("")

def verifica_tabuleiro_cheio(tabuleiro):
    j = 1
    cheio = True
    while (j <= ncol and cheio == True):
        if (tabuleiro[1][j] == BRANCO):
            cheio = False
        j += 1
    return cheio

def determina_vez(tabuleiro):
    num_x = 0; num_b = 0;
    i = 1; j = 1;
    retorno = XIS
    
    for i in range(1,nlin+1):
        for j in range(1,ncol+1):
            if (tabuleiro[i][j] == BOLA):
                num_b += 1
            if (tabuleiro[i][j] == XIS):
                num_x += 1
    if (num_x > num_b):
        retorno = BOLA
    return retorno

def joga(tabuleiro, col, tipo):
    possibilidade = IMPOSSIVEL
    salvo = False
    lin = 9 #Usa o valor máximo
    
    if (tabuleiro[1][col] == BRANCO):
        possibilidade = POSSIVEL
        while (salvo == False and lin > 0):
            if (tabuleiro[lin][col] == BRANCO):
                tabuleiro[lin][col] = tipo
                salvo = 1
            else:
                lin -= 1
    else:
        possibilidade = IMPOSSIVEL
    return possibilidade

def conta_ligados(tabuleiro, coluna):
    nlin = 1
    
    while (tabuleiro[nlin][coluna] == MOLDURA or tabuleiro[nlin][coluna] == BRANCO):
        nlin += 1
    tipo = tabuleiro[nlin][coluna]
    print (tipo)
    
    direct = 1
    i = 1; j = 1;
    lig = 1
    maxLig = 1
    left = True
    right = True
    while (direct <= 4):
        if (right):
            if (tabuleiro[nlin+i][coluna+j] == tipo):
                lig += 1
            else:
                right = False
        if (left):
            if (tabuleiro[nlin-i][coluna-j] == tipo):
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
            
        if (direct == 1): # Diag \
            i += 1
            j += 1
        if (direct == 2): # Diag /
            i -= 1
            j += 1
        if (direct == 3): # Diag |
            i += 1
        if (direct == 4): # Diag -
            j += 1
        
    return maxLig

main()