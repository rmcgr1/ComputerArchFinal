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

    print ""
    print "Clock: " + str(clock)
    print "IF: {0} ID: {1} EX: {2} WB: {3}".format(IF, ID, EX, WB)
    print ""
    print execute.status()
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
    if proceed and IF_Proceed:
        inst = instruction[EIP]
        IF.append(inst)
        EIP = EIP + 4

        update_state(to_string(inst), "IF", clock)
        
    
def ID_stage():
    if proceed and len(IF) != 0:
        
        # TODO This may be trouble trying to remove from list
        # TODO Is this proper way to prevent more fetches?

        ID.append(IF.pop(0))
    
        for inst in ID:
            if execute.unitFree(inst, clock):
                ID_Ready.append(inst)
                ID.remove(inst)
                update_state(to_string(inst), "ID", clock)
            else:
                # TODO record hazard here? Waiting on a FU isn't a hazard right?
                IF_Proceed = False
        
        if len(ID) == 0:
            IF_Proceed = True


def EX_stage():
    global ID_Ready

    if proceed and len(ID_Ready) != 0:
        

        # can we have multiple instructions enter EX, sure!
        for inst in ID_Ready:

            EX.append(inst)

            completion_cycle = execute.start(inst, clock)

            if not EX_completion.has_key(completion_cycle):
                EX_completion[completion_cycle] = list()
                EX_completion[completion_cycle].append(inst)
                EX.pop()
            else:
                EX_completion[completion_cycle].append(inst)
                EX.pop()

            ID_Ready = []
                
            # check EX_completion here too to do the status update
            # Need to account for multiple instructions finishing in this cycle
            if EX_completion.has_key(clock):
                inst_list = EX_completion[clock]
                for inst in inst_list:
                    # TODO implement MEM here
                    if execute.needsMem(inst):
                        execute.Mem(inst)
                    update_state(to_string(inst), "EX", clock)
                    EX_Ready.append(inst)
                    
                # Contention for single WB port
                # TODO Priority given to not pipelined FU that takes most cycles, if tie, earielst issued
                # TODO Record Structural Hazard
                if len(EX_Ready) > 1:
                    # TODO Change this
                    WB.append(EX_Ready.pop())
                else:
                    WB.append(EX_Ready.pop())
            


def WB_stage():
    if proceed and len(WB) != 0:
        
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
IF_Proceed = True

IF = []
ID = []
ID_Ready = []
EX = []
EX_Ready = []
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




