#!usr/bin/phyton
# -*- coding: utf-8 -*-

MAX_LEN_STATE = 9999
RETORNE = 'retorne'
ACEITE = 'aceite'
REJEITE = 'rejeite'

# verifica arquivo
def not_file(file):
    return file[-3:] != '.mt'


# lê arquivo para lista
def read_file(file):
    with open(file, 'r') as f:
        lines = []
        for line in f:
            if line[0] != ';' and line[0] != '\n':
                lines.append(line[:-1])
    return split_toks(lines)


# string em list separado por espaço
def split_toks(lst):
    _list = []
    for line in lst:
        if ';' in line:
            line = line[:line.index(';')-1]
        tokens = line.split(' ')
        line = [t for t in tokens if t != '']
        if line != []:
            _list.append(line)
    return _list

# verifica se linha de transição está correta
def check(line):

    try:
        if len(line) == 3 or len(line) == 4:
            if int(line[0]) <= MAX_LEN_STATE:
                if len(line) == 4 and line[3] == '!':
                    return True
                return True
        elif len(line) == 6 or len(line) == 7:
            if int(line[0]) <= MAX_LEN_STATE and \
                   line[2] == '--' and \
                   (line[4] == 'e' or line[4] == 'd' or line[4] == 'i') and \
                   (line[5] == RETORNE or line[5] == ACEITE or \
                    line[5] == REJEITE or line[5] == '*' or \
                    int(line[5]) <= MAX_LEN_STATE):
                if len(line) == 7 and line[6] == '!':
                    return True
                return True
    except IOError:
        print('Arquivo não está no formato correto.')

    return False


def to_list(string):
    string = [item for item in string.split(' ') if item != '']
    return string


def new_word(_input, head, new_sym):
    if head == 0:
        ret = new_sym + _input[1:]
    else:
        ret = _input[0:head] + new_sym + _input[head+1:]
    return ret


def put_head(word, head, delim):

    opn_head = delim[0]
    cls_head = delim[1]

    if len(word) == 0:
        word = ' '
        ret = opn_head + word + cls_head
    elif head == 0:
        ret = opn_head + word[0] + cls_head + word[1:]
    else:
        if head == len(word):
            word = word + '_'
            ret = word[0:head] + opn_head + word[head] + cls_head
        else:
            ret = word[0:head] + opn_head + word[head] + cls_head + word[head+1:]
    return word, ret

def rm_space(word):
    i = 0
    j = -1
    while word[i] == '_':
        i = i + 1
    while word[j] == '_':
        j = j - 1
    if j != -1:
        return word[i:j+1]
    else:
        return word[i:]
    return word
