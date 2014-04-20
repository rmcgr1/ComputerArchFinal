#!/usr/bin/python

import pdb
import sys

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
        self.FP_DIV_DELAY = int(config['FP divider'][0])
        self.FP_ADD_PIPELINED = self.yesno(config['FP adder'][1])
        self.FP_ADD_DELAY = int(config['FP adder'][0])
        self.FP_MULT_PIPELINED = self.yesno(config['FP Multiplier'][1])
        self.FP_MULT_DELAY = int(config['FP Multiplier'][0])

    

    def start(self, inst, clock):
        ex_cycles = self.setDelay(inst, clock)
        return ex_cycles + clock


    def Mem(self, inst):
        pass



####
# Helper Functions
####

    def setDelay(self, inst, clock):

        # TODO: Test pipelining for MUL and DIV and FP ADD

        Int_Arithmetic = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
        Mem_Ops = ['LW', 'SW', 'L.D', 'S.D']

        op = inst[0]
        
        if op in Int_Arithmetic:
            # TODO: What is the deal with the 1 cycle MEM access, guarenteed 1 cycle write? Do I have to track this?
            return 0
        if op in Mem_Ops:
            return 0
        if op == "ADD.D" or op == "SUB.D":
            if not self.FP_ADD_PIPELINED:
                self.FP_ADD_BUSY = clock + self.FP_ADD_DELAY - 1
            return self.FP_ADD_DELAY - 1
        if op == "MUL.D":
            if not self.FP_MULT_PIPELINED:
                self.FP_MULT_BUSY = clock + self.FP_MULT_DELAY - 1 
            return self.FP_MULT_DELAY - 1
        if op == "DIV.D":
            if not self.FP_DIV_PIPELINED:
                self.FP_DIV_BUSY = clock + self.FP_DIV_DELAY - 1 
            return self.FP_DIV_DELAY - 1
        if op == 'HLT':
            sys.exit(0)



    def unitFree(self, inst, clock):

        # TODO: What about two Int/Loads leaving EX at the same time?

        Int_Arithmetic = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
        Mem_Ops = ['LW', 'SW', 'L.D', 'S.D']
        

        op = inst[0]
        
        if op in Int_Arithmetic:
            return True
        if op in Mem_Ops:
            return True
        if op == "ADD.D" or op == "SUB.D":
            if self.FP_ADD_BUSY < clock:
                return True
            else:
                return False
        if op == "MUL.D":
            if self.FP_MULT_BUSY < clock:
                return True
            else:
                return False
        if op == "DIV.D":
            if self.FP_DIV_BUSY < clock:
                return True
            else:
                return False
        if op == 'HLT':
            sys.exit(0)



    def needsMem(self, inst):
        return False


    def yesno(self, string):
        if string.upper() == "NO":
            return False
        elif string.upper() == "YES":
            return True
        else:
            pdb.set_trace()

    def status(self):
        return "FP_ADD:{0} FP_MULT:{1} FP_DIV:{2}".format(str(self.FP_ADD_BUSY), str(self.FP_MULT_BUSY), str(self.FP_DIV_BUSY))
