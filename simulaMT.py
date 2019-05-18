#!usr/bin/python
# -*- coding:utf-8 -*-





import sys

from data import not_file
from TuringMachine import TuringMachine

def main():

    # verify input file
    if len(sys.argv) > 1:
        file = sys.argv[-1]
        if not_file(file):
            print('Arquivo {} não reconhecido.'.format(file))
            return
    else:
        print('Arquivo de entrada não encontrado.')
        return


    # get user configurations
    config = None
    if len(sys.argv) >= 3:
        config = sys.argv[1:-1]


    # print header
    header()


    # create turing machine simulator
    tm_sim = TuringMachine(file, config)


    # get the input word
    tm_sim.word = input('Forneça a palavra inicial: ')
    print('\n')


    # execute turing machine simulator
    tm_sim.execute()
    while not tm_sim.finalize:
        config = []
        tm_sim.up_config(input('\nForneça opção (-r,-v,-s): ').split(' '))
        tm_sim.execute()


def header():
    print('\nSimulador de Máquina de Turing ver 1.0')
    print('Desenvolvido como trabalho prático para a disciplina de Teoria da Computação - IFMG, 2019\n')
    print('Lise Arantes')
    print('Rúbia Marques\n')


if __name__ == '__main__':
    main()
