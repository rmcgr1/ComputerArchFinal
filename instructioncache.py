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

    def __init__(self, config, instruction, stats):    
        self.I_CACHE_DELAY = int(config['I-Cache'][0])
        self.MEMORY_DELAY = int(config['Main memory'][0])
        self.instruction = instruction
        self.stats = stats

###
# Helper Functions
###

    # Return EIP as a string with 5 digits and binary prefix '0b'
    def get_address(self, EIP):
        if EIP > int('0x100',16):
            print "ERROR, EIP greater than 0x100"
            pdb.set_trace()

        padding = 8 - len(bin(EIP)[2:])
        return bin(EIP)[0:2] + padding * '0' + bin(EIP)[2:]
    
    def get_tag(self, EIP):
        return (self.get_address(EIP))[2:4]

    def get_index(self, EIP):
        return (self.get_address(EIP))[4:6]

    def get_offset(self, EIP):
        return (self.get_address(EIP))[6:8]


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
        self.stats['IC_REQ'] = self.stats['IC_REQ'] + 1
        
        if self.I_Cache[index][0] == tag:
            # Hit
            self.stats['IC_HITS'] = self.stats['IC_HITS'] + 1
            return self.I_Cache[index][1][int('0b' + offset,2)], clock
        

        else:
            # Cache Miss

            data = self.move_to_cache(EIP)
            self.I_Cache[index] = (tag, data)

#            self.status()
#            pdb.set_trace()

            return self.I_Cache[index][1][int('0b' + offset, 2)], clock + (2 * (self.I_CACHE_DELAY + self.MEMORY_DELAY)) - 1
        
    def move_to_cache(self, EIP):
        data = []
        
        # Align address to begining offset
        addr = self.get_address(EIP)
        EIP = int(addr[:-4] + '0000',2)

        for i in range(EIP, EIP + 16,4):
            if i > 255:
                print "ERROR: I cache fetch out of range"
                pdb.set_trace()
            
            data.append(self.instruction[i])
            
        return data
                                
