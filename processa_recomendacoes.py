from db_connect import *
from string_funcoes import *
import os

#********************************************************************************# 
def opcaoValida(opcao):
    return (opcao in ['0', '1', '2', '3', '4', '5'] )

#********************************************************************************#                             
def lista_generos():
    return  mostra_generos_banco()

#********************************************************************************# 
def nome_genero(genero_numero):
    return lista_generos()[genero_numero-1]
#********************************************************************************# 
def mostra_generos():
    lista = lista_generos()

    string ='|'
    contador = 0
    contador_geral = 0
    print('---------------------------------------------------------------------------------------------' )
    for genero in lista:

        contador_geral += 1
        string += '('+padl(str(contador_geral), 2 , ' ')+ ')' + padr(genero.upper(), 18, ' ') + '|'
        contador += 1
        if contador == 4:
            print(string)
            contador = 0
            string ='|'
    print('---------------------------------------------------------------------------------------------' )

#********************************************************************************#                 
def recomendacoes_genero():
    genero = 99
    while genero != 0:
        mostra_generos()
        genero = input('Selecione um dos generos: ')
        genero_nome = nome_genero(int(genero))
        clrscr()
        print('Gerando recomendações para o gênero: ' + genero_nome)
        filme = carrega_filmes_por_genero( genero_nome )
        if filme:
            print(filme)
        else:
            print('Not Found')
        teste = input('Teste')


#********************************************************************************#     
def recomendacoes_avaliacoes():
    print('Gera recomendações por...')

#********************************************************************************#     
def recomendacoes_elenco():
    print('Gera recomendações por...')

#********************************************************************************#     
def recomendacoes_diretor():
    print('Gera recomendações por...')

#********************************************************************************#     
def recomendacoes_popularidade():
    print('Gera recomendações por...')

#********************************************************************************# 
def clrscr():
    os.system('cls')


    
#********************************************************************************# 
def recomendacoes():

    opcao = 99
    while opcao != '0':
        clrscr()
        print('+--------------------------------------------------+')
        print('+---------  Recomendações de filmes por    --------+')
        print('+--------------------------------------------------+')
        print('+ Selecione:                                       +')
        print('+ 1 - Gênero                                       +')
        print('+ 2 - Avaliação dos usuários                       +')
        print('+ 3 - Elenco                                       +')
        print('+ 4 - Diretor                                      +')
        print('+ 5 - Popularidade                                 +')
        print('+ 0 - Sair                                         +')
        print('+--------------------------------------------------+')
        print('+--------------------------------------------------+\n')
        if opcaoValida(opcao):

            if opcao == '1':
                recomendacoes_genero()
            elif opcao == '2':
                recomendacoes_avaliacoes()
            elif opcao == '3':
                recomendacoes_elenco()
            elif opcao == '4':
                recomendacoes_diretor()
            elif opcao == '5':
                recomendacoes_popularidade()
            else:
                print(" --- Fim do programa ---")
                return

        else:
            print('Opção ',opcao,' invalida!')

#********************************************************************************# 
def main():
    recomendacoes_genero()
    
    


main()    