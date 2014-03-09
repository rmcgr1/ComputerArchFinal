#!/usr/bin/python

'''

instruction.py

A template to represent MIPS instructions

Classes of instructions:

Data Transfers
LW, SW, L.D, S.D

Arithmetic/ logical
DADD, DADDI, DSUB, DSUBI, AND, ANDI, OR, ORI,ADD.D, MUL.D, DIV.D, SUB.D

Control
J, BEQ, BNE

Special purpose
HLT (to stop fetching new instructions)

Sample code:

L.D F6, 34(R2)
L.D F2, 45(R3)
MUL.D F0, F2, F4
SUB.D F8, F6, F2
DIV.D F10, F0, F6
ADD.D F6, F8, F2

Registers:
R0 = 0
R1 - R31 integer registers (64 bits)
F0 - F31 FP registers (32/64 bits)


'''

import pdb


class Instruction:

    Data_Instructions = ['LW', 'SW', 'L.D', 'S.D']
    Arithmetic_Instructions = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI', 'ADD.D', 'MUL.D', 'DIV.D', 'SUB.D']
    Control_Instructions = ['J', 'BEQ', 'BNE']


    def parse(self, filename):
        f = open(filename)
        lines = f.readlines()
        for l in lines:
            l = l.strip().strip(',').split(' ')
            
            #From opcode determine type
            #if l[0] in Data_Instructions:
                #inst = I_Type(l[0], l[1]


            #fill out type
            

    
class I_Type:
    def __init__(self, opcode, rs, rt, immediate):
        self.opcode = (opcode,6)
        self.rs = (rs, 5)
        self.rt = (rt, 5)
        self.immediate = (immediate, 16)
        self.type = 'i'


class R_Type:
    def __init__(self, opcode, rs, rt, rd, shamt, funct):
        self.opcode = (opcode, 6)
        self.rs = (rs, 5)
        self.rt = (rt, 5)
        self.rd = (rd, 5)
        self.shamt = (shamt, 5)
        self.funct = (funct, 6)
        self.type = 'r'

    
class J_Type:
    def __init__(self, opcode, offset):
        self.opcode = (opcode, 6)
        self.offset = (offset, 26)
        self.type = 'j'

