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

#import pdb


class Instruction:


    def parse(self, filename):
        
        #TODO There is a inconsistancy between having DADDI and DADD.i

        Data_Instructions_List = ['LW', 'SW', 'L.D', 'S.D']
        Arithmetic_Instructions_List = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI', 'ADD.D', 'MUL.D', 'DIV.D', 'SUB.D']
        Control_Instructions_List = ['J', 'BEQ', 'BNE']

        inst_list = []

        f = open(filename)
        lines = f.readlines()
        for l in lines:
            l = l.strip().split()

            if l[0].upper() in Data_Instructions_List:
                opcode = l[0]
                rs = l[1].strip(',')
                rt = l[2].split('(')[-1].strip(')')
                immediate = l[2].split('(')[0]
                inst_list.append(Data_Instruction(opcode, rs, rt, immediate))
                continue

            if l[0].upper() in Arithmetic_Instructions_List:
                opcode = l[0]
                rd = l[1].strip(',')
                rs = l[2].strip(',')
                rt = l[3].strip(',')
                inst_list.append(Arithmetic_Instruction(opcode, rd, rs, rt))

            if l[0].upper() in Control_Instructions_List:
                opcode = l[0]
                rd = l[1].strip(',')
                rs = l[2].strip(',')
                rt = l[3].strip(',')
                inst_list.append(Control_Instruction(opcode, rd, rs, rt))



        #print inst_list[3].opcode
        #print inst_list[3].rd
        #print inst_list[3].rs
        #print inst_list[3].rt

            
        return inst_list


            


class Data_Instruction:
    def __init__(self, opcode, rs, rt, immediate):
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.immediate = immediate
        self.type = 'data'



class Arithmetic_Instruction:
    def __init__(self, opcode, rd, rs, rt):
        self.opcode = opcode
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.type = 'math'


class Control_Instruction:
    def __init__(self, opcode, rd, rs, rt):
        self.opcode = opcode
        self.rd = rd
        self.rs = rs
        self.rt = rt
        self.type = 'control'



class I_Type:
    def __init__(self, opcode, rs, rt, immediate):
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.immediate = immediate
        self.type = 'i'


class R_Type:
    def __init__(self, opcode, rs, rt, rd, shamt, funct):
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.shamt = shamt, 5
        self.funct = funct, 6
        self.type = 'r'

    
class J_Type:
    def __init__(self, opcode, offset):
        self.opcode = opcode
        self.offset = offset
        self.type = 'j'

