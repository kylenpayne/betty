#!/usr/bin/env

class attr:
    '''
    class for attributes assigned to fighters
    '''
    def __init__(self, attrs):
        self.height = attrs[0]
        self.reach = attrs[1]
        self.record = attrs[2]
        self.division = attrs[3]
        self.name = attrs[4]