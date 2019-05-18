#!usr/bin/python
# -*- coding:utf-8 -*-


from data import read_file, check, new_word, put_head, rm_space
from Block import Block


STEPS_MAX = 500


class TuringMachine():

    def __init__(self, file, config):

        self.exec_type = 'v'
        self.steps = STEPS_MAX
        self.delimiter = ['(', ')']
        if config is not None:
            self.set_config(config)
        self.blocks = {}
        self.build_tm_sim(file)
        self.exec_stack = []
        self.current_block = 'main'
        self.current_state = self.blocks[self.current_block].init_state
        self.word = 'aba'
        self.len_word = len(self.word)
        self.second_tape = '-'
        self.head = 0
        self.reading = ''
        self.finalize = False
        self.break_point = False

    def build_tm_sim(self, file):
        lines = read_file(file)
        i = 0
        while i < len(lines):
            line = lines[i]
            if line[0] == 'bloco' and (len(line) == 3 or len(line) == 4):
                name = line[1]
                init_state = line[2]
                self.blocks[name] = Block(init_state)
                i += 1
                line = lines[i]
                while line[0] != 'fim':
                    if check(line):
                        self.blocks[name].add_state(line)
                    else:
                        self.finalize = True
                        break
                    i += 1
                    line = lines[i]
            else:
                print('Arquivo não está no formato correto.')
                self.finalize = True
            i += 1

    def set_config(self, config):
        self.set_type_execution(config)
        if "-head" in config:
            i = config.index("-head")
            self.delimiter = [config[i+1][0], config[i+1][1]]

    def up_config(self, config):
        if config != []:
            self.set_type_execution(config)

    def set_type_execution(self, config):
        if ('-step' in config) or ('-s' in config):
            if '-step' in config:
                i = config.index('-step')
            else:
                i = config.index('-s')
            try:
                self.steps = int(config[i+1])
            except (ValueError, IndexError):
                pass
            self.exec_type = 's'
        else:
            if ('-resume' in config) or ('-r' in config):
                self.exec_type = 'r'
                self.steps = STEPS_MAX
            elif ('-verbose' in config) or ('-v' in config):
                self.exec_type = 'v'
                self.steps = STEPS_MAX

###############################################################################

    def execute(self):
        for _ in range(self.steps):
            if self.exec_type != 'r':
                print(self.instant_config())
            else:
                self.instant_config()
            self.do_transition()
            if self.break_point:
                self.break_point = False
                break
            if self.finalize:
                return

    def instant_config(self):
        self.word, word = put_head(self.word, self.head, self.delimiter)
        return '{:.>16}'.format(self.current_block) + '.' + \
                '{:0>4}'.format(self.current_state) + ' : ' + \
                '{:_^43}'.format(word) + ' : ' + self.second_tape

    def do_transition(self):
        state = self.blocks[self.current_block].states[self.current_state]
        self.reading = self.word[self.head]

        # executa transição
        if (self.reading in state.transitions) or ('*' in state.transitions):
            if self.reading in state.transitions:
                t = state.transitions[self.reading]
            else:
                t = state.transitions['*']
            self.transition(t)
        else:
            # segunda fita
            st_transitions = {}
            st = False
            for t in state.transitions:
                if t[0] == '[' and t[-1] == ']':
                    st_transitions[t[1:-1]] = state.transitions[t]
            if len(st_transitions) != 0:
                if self.second_tape in st_transitions:
                    sym = '['+self.second_tape+']'
                    st = True
                elif '*' in st_transitions:
                    sym = '[*]'
                    st = True
            if st:
                t = state.transitions[sym]
                self.transition(t)
                st = False
            elif 'copiar' in state.transitions:
                t = state.transitions['copiar']
                self.second_tape = self.reading
                self.current_state = state.transitions['copiar'][0]
            elif 'colar' in state.transitions:
                t = state.transitions['colar']
                self.word = new_word(self.word, self.head, self.second_tape)
                self.current_state = state.transitions['colar'][0]
            # novo bloco
            else:
                for key in state.transitions:
                    if key in self.blocks:
                        t = state.transitions[key]
                        self.exec_stack.append(self.current_block)
                        self.exec_stack.append(state.transitions[key][0])
                        self.current_block = key
                        self.current_state = self.blocks[key].init_state
            if self.current_state == 'retorne':
                self.current_state = self.exec_stack.pop()
                self.current_block = self.exec_stack.pop()

        if t[-1] == '!':
            print('\nBreak Point')
            self.break_point = True

    def transition(self, t):
        new_sym = t[0]
        move = t[1]
        new_state = t[2]
        if new_sym != '*':
            self.word = new_word(self.word, self.head, new_sym)
        self.movement(move)
        if new_state != '*':
            self.current_state = new_state
        if self.current_state == 'aceite':
            self.aceita()
            self.finalize = True
        elif self.current_state == 'rejeite':
            self.rejeita()
            self.finalize = True
        elif self.current_state == 'retorne':
            self.current_state = self.exec_stack.pop()
            self.current_block = self.exec_stack.pop()

    def movement(self, move):
        if move == 'e':
            if self.head == 0:
                self.word = '_' + self.word
            else:
                self.head -= 1
        if move == 'd':
            if self.head == self.len_word - 1:
                self.word = self.word + '_'
            self.head += 1

    def aceita(self):
        _, word = put_head(self.word, self.head, self.delimiter)
        print(self.instant_config())
        print('\nACEITA\n' + '{:->70}'.format('\n') + rm_space(word) + \
            '\n{:->70}'.format('\n') + 'FIM DA SIMULAÇÃO\n')

    def rejeita(self):
        print(self.instant_config())
        _, word = put_head(self.word, self.head, self.delimiter)
        print('\nREJEITA\n' + '{:->70}'.format('\n') + rm_space(word) + \
            '\n{:->70}'.format('\n') + 'FIM DA SIMULAÇÃO\n')
