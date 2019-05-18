#!usr/bin/python
# -*- coding:utf-8 -*-

from State import State

class Block():

    def __init__(self, init_state):
        self.states = {}
        self.init_state = init_state


    def add_state(self, args):
        name = args[0]

        transition = args[1:]
        if name in self.states:
            self.states[name].add_transition(transition)
        else:
            self.states[name] = State(transition)
