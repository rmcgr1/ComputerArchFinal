#!/usr/bin/python

'''
Implements methods for the IF phase, specfically the instruction cache

'''

import pdb
import sys

class If:

    I_CACHE_DELAY = ''
    MEMORY_DELAY = ''
    instruction = {}
    I_Cache = {'00': ('', ['','','','','']), '01': ('', ['','','','','']), '10': ('', ['','','','','']), '11': ('',['','','','',''])}

    LRU = []

    def __init__(self, config, instruction):    
        self.I_CACHE_DELAY = int(config['I-Cache'][0])
        self.MEMORY_DELAY = int(config['Main memory'][0])
        self.instruction = instruction

###
# Helper Functions
###

    # Return EIP as a string with 5 digits and binary prefix '0b'
    def get_address(self, EIP):
        if EIP > 32:
            print "ERROR, EIP greater than 32"
            pdb.set_trace()

        padding = 5 - len(bin(EIP)[2:])
        return bin(EIP)[0:2] + padding * '0' + bin(EIP)[2:]
    
    def get_tag(self, EIP):
        return (self.get_address(EIP))[2]

    def get_index(self, EIP):
        return (self.get_address(EIP))[3:5]

    def get_offset(self, EIP):
        return (self.get_address(EIP))[5:]


    def status(self):
        print '00: ' + str(self.I_Cache['00'])
        print '01: ' + str(self.I_Cache['01'])
        print '10: ' + str(self.I_Cache['10'])
        print '11: ' + str(self.I_Cache['11'])

###
# Main methods
###


    def get_instruction(self, EIP, clock):

        index = self.get_index(EIP)
        tag = self.get_tag(EIP)
        offset = self.get_offset(EIP)

        #check index to get the set, then check the tag
        if self.I_Cache[index][0] == tag:
            # Hit
            pdb.set_trace()
            return self.I_Cache[index][1][int('0b' + offset,2)], clock

        else:
            if index == '10':
                pdb.set_trace()
            data = self.move_to_cache(EIP)

            self.I_Cache[index] = (tag, data)

            self.status()
            pdb.set_trace()

            return self.I_Cache[index][1][int('0b' + offset, 2)], clock + (2 * (self.I_CACHE_DELAY + self.MEMORY_DELAY)) - 1
        
    def move_to_cache(self, EIP):
        data = []

        for i in range(EIP, 4):
            if i > 32:
                print "ERROR: I cache fetch out of range"
                pdb.set_trace()
            
            data.append(self.instruction[i])
            
        return data
                                
