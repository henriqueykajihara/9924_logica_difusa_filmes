from db_connect import *
from string_funcoes import *
import os

#********************************************************************************# 
def opcaoValida(opcao):
    return (opcao in ['0', '1', '2', '3', '4', '5'] )

#********************************************************************************#                             
def lista_generos():
    return  mostra_generos_banco(False)

#********************************************************************************# 
def nome_genero(genero_numero):
    return lista_generos()[genero_numero-1]
#********************************************************************************# 
def mostra_filmes(lista_filmes):
    print('\nMostrando filmes:')
    contador = 0
    for filme in lista_filmes:
        print(filme)
        print('\n')
        contador += 1
        if contador == 10:
            return

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
    genero = '99'
    while genero != '0':
        print( 'Recomendações por Gênero (tecle 0 para sair): ')
        mostra_generos()
        genero = input('Selecione um dos generos: ')
        genero_nome = nome_genero(int(genero))
        clrscr()
        print('Gerando recomendações para o gênero: ' + genero_nome)
        lista_filmes = carrega_filmes_por_genero( genero_nome )
        
        mostra_filmes(lista_filmes)    
        teste = input('Teste')

#********************************************************************************#
def avaliacao_valida(avaliacao):
    return (avaliacao in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] )
    
#********************************************************************************#     
def recomendacoes_avaliacoes():

    avaliacao = '99'
    while avaliacao != '0':
        clrscr()
        print( 'Recomendações por Avaliação (tecle 0 para sair): ')
        avaliacao = input( 'Selecione um número de 1 a 9: ')
        clrscr()

        print("Procurando avaliações na faixa: "+ avaliacao)
        if avaliacao_valida(avaliacao):
            lista_filmes = carrega_filmes_por_avaliacao(int(avaliacao))
            mostra_filmes(lista_filmes)
        else:
            print('Escolha um número entre 1 e 9!' )
            
        mostra_filmes(lista_filmes)            
        teste = input('Teste')
        

#********************************************************************************#     
def recomendacoes_elenco():
    ator = ' '
    while ator != '0':
        ator = input( 'Digite o nome do ator/atriz: ' )
        id_ator = 0
        resultado, id_ator = ator_existe(ator)
        if resultado:
            lista_filmes = carrega_filmes_por_elenco(id_ator)
        else:
            print('Ator/Atriz ' + ator+ ' não encontrado!' )

        mostra_filmes(lista_filmes)
        teste = input('Teste')

#********************************************************************************#     
def recomendacoes_diretor():

    diretor  = ' '
    while diretor  != '0':
        diretor  = input( 'Digite o nome do diretor: ' )
        id_diretor  = 0
        resultado, id_diretor = diretor_existe(diretor)
        if resultado:
            lista_filmes = carrega_filmes_por_diretor(id_diretor)
        else:
            print('Diretor ' + diretor + ' não encontrado!' )
            
        mostra_filmes(lista_filmes)
        teste = input('Teste')

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
        opcao = input('Selecione uma opção: ')
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
    recomendacoes()
    
    


main()    