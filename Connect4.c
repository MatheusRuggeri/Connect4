/***************************************************************/
/**                                                           **/
/**                  UNIVERSITY OF SAO PAULO                  **/
/**                                                           **/
/**   Joao Matheus Rugeri Murdiga                   7573941   **/
/**   Exercicio-Programa 04                                   **/
/**   Professor: Nina S. T. Hirata                            **/
/**   Turma: 3                                                **/
/**                                                           **/
/***************************************************************/

//This is an old version of the game that I had to make for my programming class, the indentation is really bad but I didn't find the last version

#include <stdio.h>

#define MAXLIN (9+2)
#define MAXCOL (9+2)

#define IMPOSSIVEL 0
#define POSSIVEL   1

#define COMPLETO   2
#define INCOMPLETO 3

#define BRANCO  ' '
#define MOLDURA 'm'
#define XIS     'X'
#define BOLA    'O'
#define VAZIO   'V'
#define EMPATE  'D'
#define ERRO    'E'


#define HUMANO     'h'
#define COMPUTADOR 'c'

/*
 * PARTE I.  P R O T O T I P O S   D A S   F U N C O E S
 */

int carrega_configuracao(char tabuleiro[MAXLIN][MAXCOL], int *k,
                         int *nlin, int *ncol, char *tipo_xis, char *tipo_bola);

void coloca_moldura(char tabuleiro[MAXLIN][MAXCOL], int nlin, int ncol);

void imprime_tabuleiro(char tabuleiro[MAXLIN][MAXCOL], int nlin, int ncol);

void inicializa_tabuleiro(char tabuleiro[MAXLIN][MAXCOL], int *k,
                          int *nlin, int *ncol);

int verifica_tabuleiro_cheio(char tabuleiro[MAXLIN][MAXCOL], int ncol);

char determina_vez(char tabuleiro[MAXLIN][MAXCOL], int nlin, int ncol);

int joga(char tabuleiro[MAXLIN][MAXCOL], int coluna, char marca_jogador);

int conta_ligados(char tabuleiro[MAXLIN][MAXCOL], int coluna);

void salva_configuracao(char tabuleiro[MAXLIN][MAXCOL], int k,
                        int nlin, int ncol, char tipo_xis, char tipo_bola);

int coluna_central(int coluna1, int coluna2, int ncol);

int melhor_jogada(char tabuleiro[MAXLIN][MAXCOL], int k,
                  int ncol, char marca_jogador);

void apagar_ultimo(char tabuleiro[MAXLIN][MAXCOL], int col);

/*
 * PARTE II.   M A I N
 *
 * A secao "Comportamento do programa" do enunciado pode
 * servir como guia para escrever o main.
 *
 */

int main()
{
    char tabuleiro[MAXLIN][MAXCOL];
    int k, nlin, ncol, bandeira, jogadaboa, ligado, i;
    char tipo_xis, tipo_bola;
    char ini_car;
    char col_joga_char, vez_do, oponente, vencedor;

    vez_do = XIS;
    oponente = BOLA;
    jogadaboa = 0;
    vencedor = VAZIO; /*DECLARA O VENCEDOR, A FALTA DELE, OU O ERRO AO CARREGAR O ARQUIVO DA CONFIGURAÇÃO*/
    ligado = 0;
    i = 0;

    printf("Voce quer (i)niciar uma nova partida ou\n          (c)arregar uma partida salva\n");
    scanf(" %c", &ini_car);

    if (ini_car == 'c') {bandeira = 0;
                        if (carrega_configuracao(tabuleiro, &k, &nlin, &ncol, &tipo_xis, &tipo_bola) == 1){printf ("Problema ao ler o arquivo"); vencedor = ERRO;}
                        }


    if (ini_car == 'i') {inicializa_tabuleiro(tabuleiro, &k, &nlin, &ncol); bandeira = 0;
                        printf("\nEscolha o jogador Xis:  (h)umano ou (c)omputador:\n");
                            scanf (" %c", &tipo_xis);
                        printf("\nEscolha o jogador Bola:  (h)umano ou (c)omputador:\n");
                            scanf (" %c", &tipo_bola);
                        }


if (vencedor != ERRO){ /*SÓ INICIA O LAÇO CASO NÃO HAJA PROBLEMAS EM CARREGAR UM PARTIDA SALVA*/

        imprime_tabuleiro(tabuleiro,nlin,ncol);

  while (verifica_tabuleiro_cheio(tabuleiro, ncol) == INCOMPLETO && vencedor == VAZIO)
  {
    printf("\nLig-%d", k);
    if (determina_vez(tabuleiro, nlin, ncol) == XIS) {vez_do = XIS; oponente = BOLA; printf("\t Vez do jogador Xis\n");}
    if (determina_vez(tabuleiro, nlin, ncol) == BOLA){vez_do = BOLA; oponente = XIS; printf("\t Vez do jogador Bola\n");}


    if (vez_do == XIS){
        if (tipo_xis == HUMANO){
            printf("\nDigite coluna da jogada (ou 's' para salvar a partida):\n");
                scanf(" %c", &col_joga_char);

                    if (col_joga_char == 's') {salva_configuracao(tabuleiro, k, nlin, ncol, tipo_xis, tipo_bola);}
                        else {jogadaboa = col_joga_char - '0'; /*"CONVERTE" CHAR EM INT*/
                            if (joga(tabuleiro, jogadaboa, vez_do) == IMPOSSIVEL){printf("\nErro, voce nao pode jogar ai\n");}} /*SE JOGA RETORNAR ERRO.*/

            imprime_tabuleiro(tabuleiro,nlin,ncol);
            }

        else {jogadaboa = melhor_jogada(tabuleiro, k, ncol, vez_do); /*VERIFICA A MELHOR JOGADA*/
                joga(tabuleiro, jogadaboa, vez_do); /*JOGA*/
                imprime_tabuleiro(tabuleiro,nlin,ncol);}
        }



    if (vez_do == BOLA){ /*LISTA DE CÓDIGOS PRATICAMENTE IGUAL A DE CIMA, ALTERANDO SOMENTE O NECESSÁRIO (DE XIS PARA BOLA)*/
        if (tipo_bola == HUMANO){
            printf("\nDigite coluna da jogada (ou 's' para salvar a partida):\n");
                scanf(" %c", &col_joga_char);

                    if (col_joga_char == 's') {salva_configuracao(tabuleiro, k, nlin, ncol, tipo_xis, tipo_bola);}
                        else {jogadaboa = col_joga_char - '0';
                            if (joga(tabuleiro, jogadaboa, vez_do) == IMPOSSIVEL){printf("\nErro, voce nao pode jogar ai\n");}}


            imprime_tabuleiro(tabuleiro,nlin,ncol);
            }
        else {jogadaboa = melhor_jogada(tabuleiro, k, ncol, vez_do);
                joga(tabuleiro, jogadaboa, vez_do);
                imprime_tabuleiro(tabuleiro,nlin,ncol);}
        }




        for (ligado = 1; ligado < ncol+1; ligado++){
            if (conta_ligados(tabuleiro, ligado) >= k){ /*CONTA OS LIGADOS PARA VER QUEM GANHA*/
                for (i=nlin; tabuleiro[i][ligado] != MOLDURA; i--) /*A FUNÇÃO SERVE PARA VER O ÚLTIMO CARACTERE DA COLUNA LIGADO, ASSIM PODE DAR O RESULTADO DA VITÓRIA MESMO NÃO HAVENDO A JOGADA ACABADO DE OCORRER.*/
                {
                    if (tabuleiro[i][ligado] == XIS) {vencedor = XIS;} /*ALTERA O VENCEDOR, PARA DAR A VITÓRIA AO JOGADOR XIS E SAIR DO LAÇO*/
                    if (tabuleiro[i][ligado] == BOLA) {vencedor = BOLA;} /*ALTERA O VENCEDOR, PARA DAR A VITÓRIA AO JOGADOR BOLA E SAIR DO LAÇO*/
                }
                    if (vencedor == VAZIO && verifica_tabuleiro_cheio(tabuleiro, ncol) == COMPLETO){vencedor = EMPATE;} /*SE ENCHER O TABULEIRO E NEM O XIS NEM A BOLA GANHAR, DÁ EMPATE*/
            }
        }

    } /*TERMINA O LAÇO DO PROGRAMA RODANDO.*/
} /*TERMINA O LAÇO DE VENCEDOR != DE ERRO*/

    if (vencedor == BOLA){printf ("\n\nO jogador Bola ganhou");} /*DÁ O VENCEDOR*/
    else {if (vencedor == XIS){printf ("\n\nO jogador Xis ganhou");}
          else { if (vencedor == ERRO) {printf ("\n");}
                else {printf ("\n\nA partida empatou");}
               }

         }


  return 0;
}


/*
 *  PARTE III. D E T A L H A M E N T O   D A S   F U N C O E S
 */

/*
 * Coloca MOLDURA na matriz tabuleiro de acordo com o enunciado.
 */
void coloca_moldura(char tabuleiro[MAXLIN][MAXCOL], int nlin, int ncol)
{
    int i, j;

    for (i = 0; i<= nlin+1; i++) /*Coloca molura na coluna zero*/
        {
                tabuleiro[i][0] = MOLDURA;
        }

    for (j = 0; j<= ncol+1; j++) /*Coloca molura na linha zero*/
        {
                tabuleiro[0][j] = MOLDURA;
        }

    for (i = 0; i<= nlin+1; i++) /*Coloca molura na última coluna*/
        {
                tabuleiro[i][ncol+1] = MOLDURA;
        }

    for (j = 0; j<= ncol+1; j++) /*Coloca molura na última linha*/
        {
                tabuleiro[nlin+1][j] = MOLDURA;
        }
}

/*
 *  Le do teclado o valor de k, o numero de linhas e colunas;
 *  coloca MOLDURA e BRANCO nas posicoes do tabuleiro.
 *
 *  Observacao.
 *    Deve usar _obrigatoriamente_ a funcao coloca_moldura.
 */
void inicializa_tabuleiro(char tabuleiro[MAXLIN][MAXCOL], int *k,
                          int *nlin, int *ncol)
{
    int i, j;

    printf("Digite o valor de k para o Lig-K:");
    scanf ("%d", &*k);
    printf("\nDigite o numero de linhas e colunas:");
    scanf ("%d %d", &*nlin, &*ncol);


  for(i=0; i<*nlin+1; i++) {
    for(j=0; j<*ncol+1; j++) {
      tabuleiro[i][j] = BRANCO; /*Coloca BRANCO em todo o tabuleiro*/
    }
  }

  coloca_moldura(tabuleiro, *nlin, *ncol); /*Coloca moldura nas bordas*/

}

/*
 * Imprime a configuracao do tabuleiro exatamente igual `a do
 * executavel fornecido.
 */


void imprime_tabuleiro(char tabuleiro[MAXLIN][MAXCOL], int nlin, int ncol)
{
    int i, j, contalin = 1, contacol = 1;
    i = 0; j = 0;

while (i<nlin){ /*Imprime até o máximo de linhas*/
    printf("   ");
    for (j = 0; j<ncol; j++)
     {
         printf ("+---");
     }
    printf("+\n");

    printf (" ");
    printf ("%d", contalin);
    contalin++;

    printf (" ");

i++;
    for (j = 0; j<ncol; )
     {
         j++;
         printf ("| ");
         if(tabuleiro[i][j] == BOLA){printf ("O ");} /*Imprime O*/
         else
            if(tabuleiro[i][j] == XIS){printf ("X ");} /*Imprime X*/

            /*else                                          LINHAS DE TESTE, PARA VERIFICAR O TIPO DE CARACTERE PRESENTE NO TABULEIRO, IGNORAR
            if(tabuleiro[i][j] == MOLDURA){printf ("M ");}  LINHAS DE TESTE, PARA VERIFICAR O TIPO DE CARACTERE PRESENTE NO TABULEIRO, IGNORAR
            else                                            LINHAS DE TESTE, PARA VERIFICAR O TIPO DE CARACTERE PRESENTE NO TABULEIRO, IGNORAR
            if(tabuleiro[i][j] == BRANCO){printf ("B ");}   LINHAS DE TESTE, PARA VERIFICAR O TIPO DE CARACTERE PRESENTE NO TABULEIRO, IGNORAR*/

                      else {{printf ("  ");}} /*Imprime o espaço*/
     }
    printf("|\n");


}

if (i == nlin) /*Imprime a última linha*/
{
        printf("   ");
    for (j = 0; j<ncol; j++)
     {
         printf ("+---");
     }
    printf("+\n");

        printf("   ");
    for (j = 0; j<ncol; j++)
     {
         printf ("  %d ",contacol);
         contacol++;
     }

}

}


/*
 * Verifica se a matriz tabuleiro que representa uma partida com ncol
 * colunas esta cheia. Retorna COMPLETO se tabuleiro cheio; e
 * retorna INCOMPLETO em caso contrario.
 */
int verifica_tabuleiro_cheio(char tabuleiro[MAXLIN][MAXCOL], int ncol)
{
    int j, cheio;
    j = 1; /*Como o tabuleiro está sobre a ação da gravidade, é impossível uma peça estar sobre nada, logo, só testaremos na linha 1 (primeira de cima para baixo, ignorando a moldura).*/
    cheio = COMPLETO;

    while (j <= ncol && cheio == COMPLETO){
        if (tabuleiro[1][j] == BRANCO){cheio = INCOMPLETO;} /*Se o primeiro valor de alguma coluna não for branco, está completo*/
        j++;
    }

  return cheio;
}


/*
 * Analisa o tabuleiro da partida que tem nlin linhas e ncol colunas e
 * retorna XIS se a vez e' do jogador Xis e BOLA se a vez e' do jogador
 * Bola.
 */
char determina_vez(char tabuleiro[MAXLIN][MAXCOL], int nlin, int ncol)
{
    int num_x, num_b, i, j;
    char retorno;
    retorno = XIS; /*Caso não se altere, retorna X*/

    num_x = 0; num_b = 0;
    i = 1; j = 1;

    for(i=1; i<=nlin; i++) {
        for(j=1; j<=ncol; j++) {
            if (tabuleiro[i][j] == BOLA) {num_b++;} /*Conta o número de O*/
            if (tabuleiro[i][j] == XIS) {num_x++;} /*Conta o número de X*/
        }
    }

    if (num_x > num_b) {retorno = BOLA;} /*Caso tenha mais X do que O, retorna BOLA*/


  return retorno;
}

/*
 * Coloca a marca do disco do jogador na coluna do tabuleiro. Retorna
 * POSSIVEL se foi possivel fazer a jogada e retorna IMPOSSIVEL se a
 * coluna esta' cheia.
 *
 * Observacao.
 *   O tabuleiro deve ter _obrigatoriamente_ uma moldura como descrito
 *   no enunciado.
 */
int joga(char tabuleiro[MAXLIN][MAXCOL], int coluna, char marca_jogador)
{
  int possibilidade, foi, lin;
  possibilidade = IMPOSSIVEL;
  lin = 9; /*ASSUME 9 COMO O VALOR MÁXIMO PARA FICAR OS DISCOS*/
  foi = 0;

    if (tabuleiro[1][coluna] == BRANCO){
        possibilidade = POSSIVEL;

        while (!foi && lin > 0){
            if (tabuleiro[lin][coluna] == BRANCO) {tabuleiro[lin][coluna] = marca_jogador; foi = 1;}
            else {lin--;}
        }
    }

    else {possibilidade = IMPOSSIVEL;}

  return possibilidade;
}
/*
 * Calcula e retorna o maior numero de discos ligados ao disco no topo
 * da coluna em uma das direcoes. Assim, o valor retornado deve ser o
 * maior dentre os quatro valores abaixo:
 *   - numero de discos ligados verticalmente;
 *   - numero de discos ligados horizontalmente;
 *   - numero de discos ligados na diagonal "principal"; e
 *   - numero de discos ligados na diagonal "secundaria".
 * Esses numeros devem incluir o disco do topo da coluna.
 *
 * Se na coluna nao ha' discos, a funcao deve retornar 0.
 * No exemplo abaixo sao mostrados os resultados de varias chamadas
 * da funcao.

   +---+---+---+---+---+---+---+---+
 1 |   |   |   | X |   |   |   |   |
   +---+---+---+---+---+---+---+---+
 2 | O | X | X | O | O | O | O |   |
   +---+---+---+---+---+---+---+---+
 3 | X | X | X | O | X | O | O |   |
   +---+---+---+---+---+---+---+---+
 4 | O | X | O | X | O | X | O |   |
   +---+---+---+---+---+---+---+---+
 5 | X | O | O | X | X | X | O |   |
   +---+---+---+---+---+---+---+---+
 6 | X | O | X | X | X | O | O |   |
   +---+---+---+---+---+---+---+---+
     1   2   3   4   5   6   7   8

  conta_ligados(tabuleiro,1)=1
  conta_ligados(tabuleiro,2)=4
  conta_ligados(tabuleiro,3)=3
  conta_ligados(tabuleiro,4)=3
  conta_ligados(tabuleiro,5)=4
  conta_ligados(tabuleiro,6)=4
  conta_ligados(tabuleiro,7)=5
  conta_ligados(tabuleiro,8)=0

 * Observacao.
 *   O tabuleiro deve ter _obrigatoriamente_ uma moldura como descrito
 *   no enunciado.
 */

int conta_ligados(char tabuleiro[MAXLIN][MAXCOL], int coluna)
{
    int lin, band1, band2, max, lig, nl, cima, nlin, para, diferente;
    char tipo;
    tipo = 'Q';
    lin = 1;
    band1 = 1; band2 = 1;
    max = 0; lig = 0;
    nl = 1;
    cima = 0;
    nlin = 10;
    para = 0;
    diferente = 1;

    while (tabuleiro[lin][coluna] != MOLDURA && !para){ /*Verifica qual é o de cima da coluna*/
        if (tabuleiro[lin][coluna] ==  XIS){tipo = XIS; max = 1; lig = 1; para = 1; diferente = 0;} /*Já adiciona um ao número de ligados (ele mesmo)*/
        else {if (tabuleiro[lin][coluna] ==  BOLA){tipo = BOLA; max = 1; lig = 1; para = 1; diferente = 0;}
                else{diferente = 1;} }
        lin++;
    }

    /*TESTA LINHA DE CIMA*/
        while (!cima && nlin > 0){
            if (tabuleiro[nlin][coluna] == BRANCO && nlin) {cima = 1;
                        if (nlin != 10) {nlin = nlin+1; /*COLOCA O TOPO COMO O ANTERIOR AO BRANCO*/}}
            else {nlin--;}
        }
        if (nlin == 0){nlin = 1;} /*CORRIGE O VALOR, CASO A LINHA DESOCUPADA SEJA A DE CIMA.*/

        while (band1 || band2){ /*TESTA A DIAGONAL PRIMÁRIA*/
            if (tabuleiro[nlin-nl][coluna-nl] == tipo && band1){lig++;} /*TESTA A PARTE DE BAIXO DA DIAGONA PRIMÁRIA*/
                else {band1 = 0;}
            if (tabuleiro[nlin+nl][coluna+nl] == tipo && band2){lig++;} /*TESTA A PARTE DE CIMA DA DIAGONAL PRIMÁRIA*/
                else {band2 = 0;}
            nl++;
        }

        if (lig > max){max = lig;}



    lig = 0; band1 = 1; band2 = 1; nl = 1;

    if (diferente != 1) {lig = 1;}

        while (band1 || band2){ /*TESTA A DIAGONAL SECUNDÁRIA*/
            if (tabuleiro[nlin+nl][coluna-nl] == tipo && band1){lig++;} /*TESTA A PARTE DE BAIXO DA DIAGONA SECUNDÁRIA*/
                else {band1 = 0;}
            if (tabuleiro[nlin-nl][coluna+nl] == tipo && band2){lig++;} /*TESTA A PARTE DE CIMA DA DIAGONAL SECUNDÁRIA*/
                else {band2 = 0;}
            nl++;
        }

        if (lig > max){max = lig;}



    lig = 0; band1 = 1; band2 = 1; nl = 1;

    if (diferente != 1) {lig = 1;}

        while (band1 || band2){ /*TESTA A COLUNA*/
            if (tabuleiro[nlin-nl][coluna] == tipo && band1){lig++;} /*TESTA A PARTE DE BAIXO DA COLUNA*/
                else {band1 = 0;}
            if (tabuleiro[nlin+nl][coluna] == tipo && band2){lig++;} /*TESTA A PARTE DE CIMA DA COLUNA*/
                else {band2 = 0;}
            nl++;
        }

        if (lig > max){max = lig;}



    lig = 0; band1 = 1; band2 = 1; nl = 1;

    if (diferente != 1) {lig = 1;}

        while (band1 || band2){ /*TESTA A LINHA*/
            if (tabuleiro[nlin][coluna-nl] == tipo && band1){lig++;} /*TESTA A PARTE DE BAIXO DA LINHA*/
                else {band1 = 0;}
            if (tabuleiro[nlin][coluna+nl] == tipo && band2){lig++;} /*TESTA A PARTE DE CIMA DA LINHA*/
                else {band2 = 0;}
            nl++;
        }

        if (lig > max){max = lig;}


  return max;
}

/*
 * Salva em um arquivo a codificacao de uma partida, como descrito
 * no enunciado; o nome do arquivo, que nao deve conter espacos, e'
 * digitado pelo usuario.  O parametro tipo_xis contem o caractere 'h'
 * se o jogador Xis for humano ou 'c' se for computador. O parametro
 * tipo_bola tem um papel semelhante ao tipo_xis.
 *
 * A funcao deve imprimir uma mensagem indicando se a partida foi ou
 * nao salva com sucesso.
 */

 void salva_configuracao(char tabuleiro[MAXLIN][MAXCOL], int k,
                        int nlin, int ncol, char tipo_xis, char tipo_bola)
{
      FILE *arq_partida;
  char nome[80];
  int i, j;

  printf("Digite nome do arquivo sem espacos para salvar a partida: ");
  scanf("%s", nome);

  /* abre o arquivo para leitura */
  arq_partida = fopen(nome, "w"); /*Troca o Read por Write*/

  /* verifica se ocorreu erro na abertura do arquivo */
  if (arq_partida == NULL) {
    printf("ERRO: arquivo %s nao pode ser salvo.\n", nome);
  }

  fprintf(arq_partida, "%d %d %d %c %c ", k, nlin, ncol, tipo_xis, tipo_bola);

  for (i = 1; i <= nlin; i++) {
    for (j = 1; j <= ncol; j++) {
        fprintf(arq_partida, " %c ", tabuleiro[i][j]);
        if (tabuleiro[i][j] == BRANCO) {fprintf(arq_partida, " V ");}
    }
  }

  fclose(arq_partida);
}


/*
 * Retorna o indice de uma coluna mais central do tabuleiro dentre
 * coluna1 e coluna2. Por exemplo
 *    coluna_central(1,3,4) = 3,
 *    coluna_central(2,3,4) = 2 ou 3,
 *    coluna_central(2,3,5) = 3, e
 *    coluna_central(3,5,7) = 3 ou 5.
 */
int coluna_central(int coluna1, int coluna2, int ncol)
{
    float meio;
    int ret;
    ret = coluna2;

    meio = (ncol + 1)/2; /*Acha o meio*/

    if ((coluna1 - meio)* (coluna1 - meio) < (coluna2 - meio)* (coluna2 - meio)) {ret = coluna1;} /*Para evitar valores negativos, o programa eleva ambos ao quadrado e verifica qual está mais perto do centro*/

  return ret;
}
/*
 * Quando esta funcao e chamada o tipo do jogador da vez e' computador
 * e sua marca ('X' ou 'O') esta no parametro marca_jogador.
 * A funcao escolhe e retorna o indice da "melhor coluna" para jogar
 * de acordo com a seguinte estrategia. A "melhor coluna" e'
 *   - uma na qual o jogador venca;
 *   - se nao houver tal coluna e' uma que impeca que o adversario
 *     venca caso fosse a vez do adversario;
 *   - se nao houverem tais colunas  e' uma que maximiza o numero de discos
 *     ligados do jogador; havendo varias dessas colunas, uma mais central
 *     possivel e' escolhida.
 *
 * Observacoes.
 *   1. O tabuleiro deve ter _obrigatoriamente_ uma moldura como descrito
 *      no enunciado.
 *
 *   2. Deve usar _obrigatoriamente_ a funcao coluna_central.
 *
 *   3. Sugerimos que nesta funcao sejam tambem usadas as funcoes
 *         joga e conta_ligados.
 */

int melhor_jogada(char tabuleiro[MAXLIN][MAXCOL], int k, int ncol,
                  char marca_jogador)
{
    int i, j, ganhou, ret, maiorateagora, coluna;
    char marca_contraria;
    ganhou = 0;
    i = 1;
    ret = 0;
    maiorateagora = 0;
    coluna = 0;

    marca_contraria = XIS;
    if (marca_jogador == XIS) {marca_contraria = BOLA;} /*Pega a marca do oponente*/


    for (j = 1; tabuleiro[1][j] != MOLDURA; j++){ /*Verifica se o computador consegue ganhar em alguma coluna*/
        if (ganhou == 0) {
            if (joga(tabuleiro, j, marca_jogador) == POSSIVEL){
                if (conta_ligados(tabuleiro, j) >= k) {ganhou = 1; ret = j;}
                apagar_ultimo(tabuleiro, j);
            }
        }
    }



    if (ganhou == 0){ /*Caso o computador não ganhe em alguma coluna, mas possa impedir o oponente de vencer será jogado em tal coluna*/
        for (j = 1; tabuleiro[1][j] != MOLDURA; j++){
            if (ganhou == 0) {
                if (joga(tabuleiro, j, marca_contraria) == POSSIVEL){
                    if (conta_ligados(tabuleiro, j) >= k) {ganhou = 1; ret = j;}
                    apagar_ultimo(tabuleiro, j);
                }
            }
        }
    }


    if (ganhou == 0){ /*Caso não tenha como vencer nem o oponente está a um disco de vencer*/
        for (j = 1; tabuleiro[1][j] != MOLDURA; j++){
           if (joga(tabuleiro, j, marca_jogador) == POSSIVEL){ /*Se for possível jogar*/
                if (conta_ligados(tabuleiro, j) > maiorateagora) {ret = j; maiorateagora = conta_ligados(tabuleiro, j); coluna = j;} /*Testa quanto é o maior número de ligantes possíveis*/
                else {if (conta_ligados(tabuleiro, j) == maiorateagora) /*Sendo o mesmo número de ligantes, testa qual é o mais próximo do centro*/
                            {if (j == coluna_central(coluna, j, ncol)){ret = j; coluna = j;}}
                     }
                apagar_ultimo(tabuleiro, j);
            }
        }
    }

  return ret;
}

/*
 * F U N C A O   D A D A
 */

/*
 * Le de um arquivo a codificacao de uma partida; a matriz tabuleiro
 * e' entao preenchida, incluindo a moldura. No parametro *tipo_xis
 * teremos o caractere 'h' se o jogador Xis for humano ou 'c' se for
 * computador. O parametro *tipo_bola tem um papel semelhante ao
 * *tipo_xis.
 *
 * Se nao houver problema na leitura do arquivo, a funcao retorna 0;
 * caso contrario, retorna 1.
 *
 *  Observacao.
 *    Usa a funcao coloca_moldura.
 */
int carrega_configuracao(char tabuleiro[MAXLIN][MAXCOL], int *k,
                         int *nlin, int *ncol, char *tipo_xis, char *tipo_bola)
{
  FILE *arq_partida;
  char nome[80];
  int i, j;

  printf("Digite nome do arquivo com a partida: ");
  scanf("%s", nome);

  /* abre o arquivo para leitura */
  arq_partida = fopen(nome, "r");

  /* verifica se ocorreu erro na abertura do arquivo */
  if (arq_partida == NULL) {
    printf("ERRO: arquivo %s nao pode ser aberto.\n", nome);
    return 1;
  }

  fscanf(arq_partida, "%d %d %d %c %c ", &*k, &*nlin, &*ncol, &*tipo_xis, &*tipo_bola);

  for (i = 1; i <= *nlin; i++) {
    for (j = 1; j <= *ncol; j++) {
        fscanf(arq_partida, " %c ", &tabuleiro[i][j]);
        if (tabuleiro[i][j] == VAZIO)
          tabuleiro[i][j] = BRANCO;
    }
  }

  fclose(arq_partida);

  coloca_moldura(tabuleiro, *nlin, *ncol);

  return 0;
}



/*FUNÇÃO ADICIONAL

Utilidade: apagar o úlitimo caractere de cada coluna, útil para testar a melhor jogada*/

void apagar_ultimo(char tabuleiro[MAXLIN][MAXCOL], int col)
{
    int i, band;
    band = 1;

    for (i=1; tabuleiro[i][1] != MOLDURA; i++) /*A FUNÇÃO SERVE PARA APAGAR O ÚLTIMO CARACTERE COLOCADO NA COLUNA, ASSIM VERIFICA ATÉ QUANDO É MOLDURA.*/
    {
        if (band){
            if (tabuleiro[i][col] == XIS){tabuleiro[i][col] = BRANCO; band = 0;}
            else
                if (tabuleiro[i][col] == BOLA){tabuleiro[i][col] = BRANCO; band = 0;}
        }
    }
}
