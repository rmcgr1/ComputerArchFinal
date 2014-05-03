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
    MEM_DELAY = ''

    # Make it show the cycle when its free? or just busy or not?
    FP_ADD_BUSY = 1
    FP_MULT_BUSY = 1
    FP_DIV_BUSY = 1
    INT_BUSY = 1

    Int_Arithmetic = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
    Mem_Ops = ['LW', 'SW', 'L.D', 'S.D']
    Branch_Ops = ['J', 'BNE', 'BEQ']

    register = {}

    def __init__(self, config, register):    
        self.FP_DIV_PIPELINED = self.yesno(config['FP divider'][1])
        self.FP_DIV_DELAY = int(config['FP divider'][0])
        self.FP_ADD_PIPELINED = self.yesno(config['FP adder'][1])
        self.FP_ADD_DELAY = int(config['FP adder'][0])
        self.FP_MULT_PIPELINED = self.yesno(config['FP Multiplier'][1])
        self.FP_MULT_DELAY = int(config['FP Multiplier'][0])
        self.MEM_DELAY = int(config['Main memory'][0])
        self.register = register

    def start(self, inst, clock, register):
        result = ''
        ex_cycles = self.setDelay(inst, clock)
        self.calculateResult(inst, register)
        return ex_cycles + clock


####
# Helper Functions
####

    def setDelay(self, inst, clock):

        # TODO: Test pipelining for MUL and DIV and FP ADD

        op = inst[0]
        
        if op in self.Int_Arithmetic:
            # TODO: What is the deal with the 1 cycle MEM access, guarenteed 1 cycle write? Do I have to track this?
            return 1
        if op in self.Mem_Ops:
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

    def calculateResult(self, inst, register):

        # TODO get the LW/SW address calculation here and use as result
        
        if inst[0] not in self.Int_Arithmetic:
            return ''
        
        if len(inst) != 4:
            print "ERROR: Int_Arithmetic with not 3 operands"
            pdb.set_trace()
        
        if inst[0] == 'DADD':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) + int(register[inst[3]],2)))[2:]

        if inst[0] == 'DADDI':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) + int(inst[3])))[2:]

        if inst[0] == 'DSUB':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) - int(register[inst[3]],2)))[2:]

        if inst[0] == 'DSUBI':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) - int(inst[3])))[2:]

        if inst[0] == 'AND':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) & int(register[inst[3]],2)))[2:]
        
        if inst[0] == 'ANDI':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) & int(inst[3])))[2:]

        if inst[0] == 'OR':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) | int(register[inst[3]],2)))[2:]
        
        if inst[0] == 'ORI':
            self.register[inst[1]] = str(bin(int(register[inst[2]],2) | int(inst[3])))[2:]


    def unitFree(self, inst, clock):

        # TODO: What about two Int/Loads leaving EX at the same time?

        op = inst[0]
        
        if op in self.Int_Arithmetic:
            return True
        if op in self.Mem_Ops:
            return True
        if op in self.Branch_Ops:
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
        if inst[0] in self.Mem_Ops:
            return True
        else:
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
