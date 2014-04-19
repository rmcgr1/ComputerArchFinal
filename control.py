#!/usr/bin/python

'''
control.py

The controller to kick of all stages of the MIPS processor

'''

import pdb

from setup import Setup
from ex import Ex

###
# Helper Functions
###

def setup():
    setup = Setup()
    inst_list, lable_list = setup.parse_instructions('inst.txt')
    register = setup.parse_registers('reg.txt')
    memory = setup.parse_memory('data.txt')
    config = setup.parse_config('config.txt')

    #print inst_list 
    #print lable_list
    #print register
    #print memory
    #print config

    return inst_list, lable_list, register, memory, config

def update_state(ins, stage, clock):
    if not state.has_key(ins):
        state[ins] = {'IF':'', 'ID':'', 'EX':'', 'WB':'', 'RAW':'','WAR':'','WAW':'','Struct':''}
        state_list.append({ins :state[ins]})
    state[ins][stage] = clock

def to_string(ins):
    rv = ''
    for i in ins:
        rv = rv + i + ' '
    return rv.strip()


def status():

    print "Clock: " + str(clock)
    print "IF: {0} ID: {1} EX: {2} WB: {3}".format(IF, ID, EX, WB)
    print ""
    print "Instruction\t\tIF\tID\tEX\tWB\tRAW\tWAR\tWAW\tStruct"
    for s in state_list:
        print s.keys()[0] + (21 - len(s.keys()[0])) * ' ' +  "\t{0}\t{1}\t{2}\t{3}".format(s[s.keys()[0]]['IF'], s[s.keys()[0]]['ID'], s[s.keys()[0]]['EX'], s[s.keys()[0]]['WB'])

    

        

# List of instructions that are ready to be WB'ed
# Store the calculated cycle that they will exit EX
def ready_instructions():
    pass


def IF_stage():
    global EIP
    if proceed:
        inst = instruction[EIP]
        IF.append(inst)
        EIP = EIP + 4

        update_state(to_string(inst), "IF", clock)
        
    
def ID_stage():
    if proceed and len(IF) != 0:
        
        inst = IF.pop(0)
        ID.append(inst)
        ## Maybe check functional unit availability here and set flags?

        update_state(to_string(inst), "ID", clock)

def EX_stage():
    if proceed and len(ID) != 0:
        
        # can we have multiple instructions enter EX?
        inst = ID.pop(0)
        EX.append(inst)
      
        completion_cycle = execute.start(inst, clock)
        
        
        
        # WORK HERE (check to make sure config is parsed then...) Add to EX_completion, modify for each FU
        if not EX_completion.has_key(completion_cycle):
            EX_completion[completion_cycle] = list()
            EX_completion[completion_cycle].append(inst)
            EX.pop()
        else:
            EX_completion[completion_cycle].append(inst)
            EX.pop()

        
        
        # check EX_completion here too to do the status update
        # Need to account for multiple instructions finishing in this cycle
        if EX_completion.has_key(clock):
            inst_list = EX_completion[clock]
            for inst in inst_list:
                if execute.needsMem(inst):
                    execute.Mem(inst)
                update_state(to_string(inst), "EX", clock)
                WB.append(inst)

            


def WB_stage():
    if proceed and len(WB) != 0:
        
        # Need to account for multiple instructions finishing in this cycle
        inst = WB.pop()
        update_state(to_string(inst), "WB", clock)

    
###
# State Variables
###

instruction, lable, register, memory, config = setup()

instruction.keys().sort()

clock = 0
EIP = 0
proceed = True

IF = []
ID = []
EX = []
WB = []


execute = Ex(config)

EX_completion = {}
state = {}
state_list = []

pdb.set_trace()

while True:
    clock = clock + 1

    WB_stage()
        
    EX_stage()
    
    ID_stage()
    
    IF_stage()

    status()




