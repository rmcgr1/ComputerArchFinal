#!/usr/bin/python

import pdb

class Ex:

    
    FP_DIV_PIPELINED = ''
    FP_DIV_DELAY = ''
    FP_ADD_PIPELINED = ''
    FP_ADD_DELAY = ''
    FP_MULT_PIPELINED = ''
    FP_MULT_DELAY = ''


    # Make it show the cycle when its free? or just busy or not?
    FP_ADD_BUSY = 1
    FP_MULT_BUSY = 1
    FP_DIV_BUSY = 1
    INT_BUSY = 1



    def __init__(self, config):    
        self.FP_DIV_PIPELINED = self.yesno(config['FP divider'][1])
        self.FP_DIV_DELAY = config['FP divider'][0]
        self.FP_ADD_PIPELINED = self.yesno(config['FP adder'][1])
        self.FP_ADD_DELAY = config['FP adder'][0]
        self.FP_MULT_PIPELINED = self.yesno(config['FP Multiplier'][1])
        self.FP_MULT_DELAY = config['FP Multiplier'][0]

    

    def start(self, inst, clock):
        ex_cycles = self.delay(inst, clock)
        return ex_cycles + clock


    def Mem(self, inst):
        pass



####
# Helper Functions
####

    def delay(self, inst, clock):

        # TODO: Pipelining for MUL and DIV and FP ADD

        Int_Arithmetic = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
        Mem_Ops = ['LW', 'SW', 'L.D', 'S.D']
        

        op = inst[0]
        
        if op in Int_Arithmetic:
            # TODO: What is the deal with the 1 cycle MEM access, guarenteed 1 cycle write? Do I have to track this?
            return 0
        if op in Mem_Ops:
            return 0
        if op == "ADD.D" or op == "SUB.D":
            return int(self.FP_ADD_DELAY)
        if op == "MUL.D":
            return int(self.FP_MULT_DELAY)
        if op == "DIV.D":
            if self.FP_DIV_PIPELINED == "YES":
                self.FP_DIV_BUSY = clock + self.FP_DIV_BUSY
            return int(self.FP_DIV_DELAY)
        if op == 'HLT':
            system.exit(0)


    def needsMem(self, inst):
        return False


    def yesno(self, string):
        if string.upper() == "NO":
            return False
        elif string.upper() == "YES":
            return True
        else:
            pdb.set_trace()
