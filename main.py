from flask import Flask, request, jsonify
from luminosidade import controla_luminosidade

app = Flask(__name__)
#********************************************************************************#
def opcao_manual_valida(opcao):
    return (opcao in ['0', '1', '2', '3'] )

#********************************************************************************#
def main():
    opcao = '99'
    while opcao != '0':

        print('+--------------------------------------------------+')
        print('+---------    Controle de Luminosidade     --------+')
        print('+--------------------------------------------------+')
        print('+ Selecione:                                       +')
        print('+ 1 - Baixa                                        +')
        print('+ 2 - Média                                        +')
        print('+ 3 - Alta                                         +')
        print('+ 0 - Sair                                         +')
        print('+--------------------------------------------------+')
        opcao = input('Selecione uma opção ou digite ZERO para sair: ')
        print('+--------------------------------------------------+\n')
        if opcao_manual_valida(opcao):

            if opcao == '1':
                print( 'Definindo nível de intensidade para: ' )
                intensidade, nivel = controla_luminosidade(80, 0, 10, 0 )
                print(nivel, intensidade)

            elif opcao == '2':
                print( 'Definindo nível de intensidade para: ' )
                intensidade, nivel = controla_luminosidade(50, 50, 10, 0.2 )
                print(nivel, intensidade)
                
            elif opcao == '3':
                print( 'Definindo nível de intensidade para: ' )
                intensidade, nivel = controla_luminosidade(10, 90, 30, 50)
                print(nivel, intensidade)

            else:
                print(" --- Fim do programa ---")
                return

        else:
            print('Opção ',opcao,' invalida!')

#********************************************************************************#
if __name__ == "__main__":
    main()