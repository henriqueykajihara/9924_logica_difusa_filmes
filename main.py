from importa_filmes import download_filmes
from processa_recomendacoes import recomendacoes

#********************************************************************************#
def opcaoValida(opcao):
    return (opcao in ['0', '1', '2'] )
#********************************************************************************#
def main():
    
    opcao = 99
    while opcao != '0':

        print('+--------------------------------------------------+')
        print('+---------     Recomendações de Filmes     --------+')
        print('+--------------------------------------------------+')
        print('+ Selecione:                                       +')
        print('+ 1 - Recomendações                                +')
        print('+ 2 - Importar banco de dados                      +')
        print('+ 0 - Sair                                         +')
        print('+--------------------------------------------------+')
        opcao = input('Selecione uma opção ou digite ZERO para sair: ')
        print('+--------------------------------------------------+\n')
        if opcaoValida(opcao):

            if opcao == '1':
                recomendacoes()
            elif opcao == '2':
                download_filmes()

            else:
                print(" --- Fim do programa ---")
                return

        else:
            print('Opção ',opcao,' invalida!')

#********************************************************************************#
if __name__ == "__main__":
    
    main()