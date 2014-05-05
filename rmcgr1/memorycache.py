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
    D_Cache = {'0': [('', ['','','','',''], ''), ('', ['','','','',''], '')], '1': [('', ['','','','',''], ''), ('', ['','','','',''], '')]}

    LRU = {'0': 0, '1' : 0}


    def __init__(self, config, memory, register, stats):    
        self.D_CACHE_DELAY = int(config['D-Cache'][0])
        self.MEMORY_DELAY = int(config['Main memory'][0])
        self.memory = memory
        self.register = register
        self.stats = stats

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
        result = ''

        if instruction[0] == 'L.D':

            if instruction[2].find('(') == -1:
                address = self.register[instruction[2]]
            else:
                add = instruction[2][:instruction[2].find('(')]
                reg = instruction[2][instruction[2].find('(')+1:instruction[2].find(')')]
                address = int(add) + self.register[reg]
                result, hit = self.read_memory(address)
                self.stats['DC_REQ'] = self.stats['DC_REQ'] + 1
                result, hit2 = self.read_memory(address + 4)
                self.stats['DC_REQ'] = self.stats['DC_REQ'] + 1

                if not hit and not hit2:
                    completion_cycle = clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY)) + 1

                elif (not hit and hit2) or (hit and not hit2):
                    completion_cycle = clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY)) + 1
                    self.stats['DC_HITS'] = self.stats['DC_HITS'] + 1
                else:
                    # With hits, two cache delay cycles to read both words
                    completion_cycle = clock + self.D_CACHE_DELAY * 2
                    self.stats['DC_HITS'] = self.stats['DC_HITS'] + 2
                          

        if instruction[0] == 'LW':

            if instruction[2].find('(') == -1:
                address = self.register[instruction[2]]
            else:
                add = instruction[2][:instruction[2].find('(')]
                reg = instruction[2][instruction[2].find('(')+1:instruction[2].find(')')]
                address = int(add) + self.register[reg]
                result, hit = self.read_memory(address)
                self.stats['DC_REQ'] = self.stats['DC_REQ'] + 1

                if not hit:
                    completion_cycle = clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY))
                else:
                    completion_cycle = clock + self.D_CACHE_DELAY
                    self.stats['DC_HITS'] = self.stats['DC_HITS'] + 2

            self.register[instruction[1]] = result

        
        if instruction[0] == 'S.D':

            if instruction[2].find('(') == -1:
                address = self.register[instruction[2]]
            else:
                add = instruction[2][:instruction[2].find('(')]
                reg = instruction[2][instruction[2].find('(')+1:instruction[2].find(')')]
                address = int(add) + self.register[reg]

                hit = self.write_memory(address, self.register[instruction[1]])
                self.stats['DC_REQ'] = self.stats['DC_REQ'] + 1

                hit2 = self.write_memory(address + 4, self.register[instruction[1]]) 
                self.stats['DC_REQ'] = self.stats['DC_REQ'] + 1

                if not hit and not hit2:
                    completion_cycle = clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY)) + 1

                elif (not hit and hit2) or (hit and not hit2):
                    completion_cycle = clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY)) + 1
                    self.stats['DC_HITS'] = self.stats['DC_HITS'] + 1
                else:
                    # With hits, two cache delay cycles to read both words
                    completion_cycle = clock + self.D_CACHE_DELAY * 2
                    self.stats['DC_HITS'] = self.stats['DC_HITS'] + 2

        if instruction[0] == 'SW':

            if instruction[2].find('(') == -1:
                address = self.register[instruction[2]]
            else:
                add = instruction[2][:instruction[2].find('(')]
                reg = instruction[2][instruction[2].find('(')+1:instruction[2].find(')')]
                address = int(add) + self.register[reg]

                hit = self.write_memory(address, self.register[instruction[1]])
                self.stats['DC_REQ'] = self.stats['DC_REQ'] + 1

                if not hit:
                    completion_cycle = clock + (2 * (self.D_CACHE_DELAY + self.MEMORY_DELAY))
                else:
                    completion_cycle = clock + self.D_CACHE_DELAY
                    self.stats['DC_HITS'] = self.stats['DC_HITS'] + 2





        return result, completion_cycle

    def write_memory(self, addr, data):

        index = self.get_index(addr)
        tag = self.get_tag(addr)
        offset = self.get_offset(addr)
        
        pdb.set_trace()
        
        if self.D_Cache[index][0][0] == tag:
            # Hit
            self.LRU[index] = 1
            self.D_Cache[index][0][1][int('0b' + offset,2)] = data
            new_block = self.D_Cache[index][0][1]
            self.D_Cache[index][0] = (tag, new_block, 'D')
            return True
        if self.D_Cache[index][1][0] == tag:
            # Hit
            self.LRU[index] = 0
            self.D_Cache[index][1][1][int('0b' + offset,2)] = data
            new_block = self.D_Cache[index][1][1]
            self.D_Cache[index][1][2] = (tag, new_block, 'D')
            return True
        else:
            # Miss
            if self.D_Cache[index][self.LRU[index]][2] == 'D':
                # Dirty block write to backing store before blowing away
                self.write_to_backing_store(self.D_Cache[index][self.LRU[index]][0], self.D_Cache[index][self.LRU[index]][1])
            new_block = self.move_to_cache(addr)
            self.D_Cache[index][self.LRU[index]] = (tag, new_block, 'D')
            self.D_Cache[index][self.LRU[index]][1][int('0b' + offset,2)] = data
            
            # Flip LRU
            if self.LRU[index] == 0:
                self.LRU[index] = 1
            else:
                self.LRU[index] = 0
            
            return False

    def read_memory(self, addr):

        index = self.get_index(addr)
        tag = self.get_tag(addr)
        offset = self.get_offset(addr)

        #check index to get the set, then check the tag
        if self.D_Cache[index][0][0] == tag:
            # Hit
            self.LRU[index] = 1
            return self.D_Cache[index][0][1][int('0b' + offset,2)], True
        if self.D_Cache[index][1][0] == tag:
            # Hit
            self.LRU[index] = 0
            return self.D_Cache[index][1][1][int('0b' + offset,2)], True
       
        else:
            # Cache Miss
            data = self.move_to_cache(addr)
            if self.D_Cache[index][0][0] == '':
                self.D_Cache[index][0] = (tag, data, '')
                self.LRU[index] = 1
                return self.D_Cache[index][0][1][int('0b' + offset, 2)], False

            elif self.D_Cache[index][1][0] == '':
                self.D_Cache[index][1] = (tag, data, '')
                self.LRU[index] = 0
                return self.D_Cache[index][1][1][int('0b' + offset, 2)], False
            else:
                pdb.set_trace()
                used_index = self.LRU[index]
                self.D_Cache[index][used_index] = (tag, data, '')

                # Flip LRU
                if self.LRU[index] == 0:
                    self.LRU[index] = 1
                else:
                    self.LRU[index] = 0
                
                return self.D_Cache[index][used_index][1][int('0b' + offset, 2)], False

        
    def move_to_cache(self, addr):
        data = []
        
        # Align address to begining offset
        addr = self.get_address(addr)
        addr = int(addr[:-4] + '0000',2)

        for i in range(addr, addr + 16,4):
            if i > int('0x180',16) or i < int('0x100',16):
                # TODO: what about fetching at extreme of memory?
                print "ERROR: I cache fetch out of range"
                pdb.set_trace()
            
            data.append(self.memory[i])
            
        return data
                                
