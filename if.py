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

###
# Helper Functions
###

    # Return EIP as a string with 5 digits and binary prefix '0b'
    def get_address(self, EIP):
        if EIP > 32:
            print "ERROR, EIP greater than 32"
            pdb.set_trace()

        padding = 5 - len(bin(EIP)[:2])
        
        return bin(a)[0:2] + padding * '0' + bin(a)[2:]
    
    def get_tag(self, EIP):
        return self.get_address(EIP)[2]

    def get_index(self, EIP):
        return self.get_address(EIP)[3:5]

    def get_offset(self, EIP):
        return self.get_address(EIP)[5:]

    def get_instruction(self, EIP, clock):
        pass
        

        
        


                                
