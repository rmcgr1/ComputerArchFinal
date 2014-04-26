#!/usr/bin/python

'''
Implements methods for the IF phase, specfically the instruction cache

'''

import pdb
import sys

class If:

    self.I_CACHE_DELAY = ''
    self.instruction = {}
    self.I_CACHE = [['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    self.LRU = []

    def __init__(self, config, instruction):    
        self.I_CACHE_DELAY = int(config['I-Cache'][0])
        self.instruction = instruction

    def get_instruction(self, EIP):
        pass
        
        


                                
