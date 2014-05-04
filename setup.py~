#!/usr/bin/python

'''

setup.py

Load the initial state

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

class Setup:

    def parse_instructions(self, filename):
        
        inst_dict = {}
        lable_dict = {}

        f = open(filename)
        lines = f.readlines()

        location = 0
        for l in lines:
            l = l.strip().replace(',','').split()
            if (l[0])[-1] == ':':
                lable_dict[location] = l[0].replace(':','')
                inst_dict[location] = l[1:]
            else:
                inst_dict[location] = l
            location = location + 4
            
        return inst_dict, lable_dict

    def parse_memory(self, filename):
        mem_dict = {}

        f = open(filename)
        lines = f.readlines()
        
        location = int('0x100',16)
        for l in lines:
            l = l.strip()
            mem_dict[location] = l
            location = location + 4

        return mem_dict

    def parse_registers(self, filename):
        reg_dict = {}

        f = open(filename)
        lines = f.readlines()
        
        register = 0
        for l in lines:
            l = l.strip()
            reg_dict['R' + str(register)] = l
            register = register + 1

        return reg_dict

    def parse_config(self, filename):
        config_dict = {}

        f = open(filename)
        lines = f.readlines()
        
        for l in lines:
            l = l.strip().split(':')
            if len(l[1].split()) == 2:
                config_dict[l[0].strip()] = [l[1].split(',')[0].strip(), l[1].split(',')[1].strip()]
            else:
                config_dict[l[0].strip()] = [l[1].strip()]

        return config_dict

    def return_priority(self,config):
        
        pipelined = list()
        unpipelined = list()
        for k in config.keys():
            if len(config[k]) == 2:
                if config[k][1] == 'no':
                    unpipelined.append([k] + config[k])
        for k in config.keys():
            if len(config[k]) == 2:
                if config[k][1] == 'yes':
                    pipelined.append([k] + config[k])
                    
        unpipelined.sort(key=lambda x: x[1], reverse=True)
        pipelined.sort(key=lambda x: x[1], reverse=True)
        return unpipelined + pipelined + [['IU', 1]]
                                  

    def parse_old(self, filename):
        
        #TODO There is a inconsistancy between having DADDI and DADD.i

        Data_Instructions_List = ['LW', 'SW', 'L.D', 'S.D']
        Arithmetic_Instructions_List = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI', 'ADD.D', 'MUL.D', 'DIV.D', 'SUB.D']
        Control_Instructions_List = ['J', 'BEQ', 'BNE']
