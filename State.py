#!usr/bin/python
# -*- coding:utf-8 -*-

class State():

    def __init__(self, transition):

        self.transitions = {}
        self.add_transition(transition)

    def add_transition(self, transition):

        if len(transition) == 5 or len(transition) == 6:
            self.transitions[transition[0]] = [transition[2], transition[3],
                transition[4]]
            if len(transition) == 6:
                self.transitions[transition[0]].append(transition[5])
        elif len(transition) == 2 or len(transition) == 3:
            if len(transition) == 3:
                self.transitions[transition[0]] = [transition[1], transition[2]]
            else:
                self.transitions[transition[0]] = [transition[1]]
