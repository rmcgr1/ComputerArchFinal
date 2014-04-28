#!/usr/bin/python

'''
Implements data mem cache for the EX phase

'''

import pdb

class Mem:

    D_CACHE_DELAY = ''
    MEMORY_DELAY = ''
    memory = {}
    register = {}
    D_Cache = {'0': [('', ['','','','','']), ('', ['','','','',''])], '1': [('', ['','','','','']), ('', ['','','','',''])]}

    LRU = []

    def __init__(self, config, memory, register):    
        self.I_CACHE_DELAY = int(config['D-Cache'][0])
        self.MEMORY_DELAY = int(config['Main memory'][0])
        self.memory = memory
        self.register = register

###
# Helper Functions
###

    # Return addr as a string with 5 digits and binary prefix '0b'
    def get_address(self, addr):
        if addr > 384:
            print "ERROR, addr greater than 384"
            pdb.set_trace()

        padding = 9 - len(bin(addr)[2:])
        return bin(addr)[0:2] + padding * '0' + bin(addr)[2:]
    
    def get_tag(self, addr):
        return (self.get_address(addr))[2:6]

    def get_index(self, addr):
        return (self.get_address(addr))[6]

    def get_offset(self, addr):
        return (self.get_address(addr))[7:9]


    def status(self):
        print '0: ' + str(self.D_Cache['0'])
        print '1: ' + str(self.D_Cache['1'])


###
# Main methods
###

    def access_memory(self, instruction, clock):
        if instruction[0] == 'L.D':
            # TODO: see if this is a valid parsing
            # TODO: LW SW SD, INTOPS

            if instruction[2].find('(') == -1:
                address = self.register[instruction[2]]
            else:
                add = instruction[2][:instruction[2].find('(')]
                reg = instruction[2][instruction[2].find('(')+1:instruction[2].find(')')]
                address = int(add) + int(self.register[reg],2)
                result, clock = self.read_memory(address, clock)
                
            
        return clock

    def read_memory(self, addr, clock):

        pdb.set_trace()

        index = self.get_index(addr)
        tag = self.get_tag(addr)
        offset = self.get_offset(addr)

        #check index to get the set, then check the tag
        if self.D_Cache[index][0][0] == tag:
            # Hit
            pdb.set_trace()
            return self.D_Cache[index][0][1][int('0b' + offset,2)], clock
        if self.D_Cache[index][1][0] == tag:
            # Hit
            pdb.set_trace()
            return self.D_Cache[index][1][1][int('0b' + offset,2)], clock
       
        else:
            # Cache Miss
            pdb.set_trace()

            data = self.move_to_cache(addr)
            if self.D_Cache[index][0][0] == '':
                self.D_Cache[index][0] = (tag, data)
                return self.D_Cache[index][0][1][int('0b' + offset, 2)], clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY)) - 1

            if self.D_Cache[index][1][0] == '':
                self.D_Cache[index][1] = (tag, data)
                return self.D_Cache[index][1][1][int('0b' + offset, 2)], clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY)) - 1

            self.status()


        
    def move_to_cache(self, addr):
        data = []
        
        # Align address to begining offset
        addr = addr[:-2] + '00'

        for i in range(addr, addr + 16,4):
            if i > int('0x180',16) or i < int('0x100',16):
                # TODO: what about fetching at extreme of memory?
                print "ERROR: I cache fetch out of range"
                pdb.set_trace()
            
            data.append(self.memory[i])
            
        return data
                                
