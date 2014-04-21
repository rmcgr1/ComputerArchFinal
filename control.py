#!/usr/bin/python

'''
control.py

The controller to kick of all stages of the MIPS processor

'''

import pdb

from setup import Setup
from ex import Ex
from id import Id

###
# Helper Functions
###

def setup():
    setup = Setup()
    inst_list, label_list = setup.parse_instructions('inst.txt')
    register = setup.parse_registers('reg.txt')
    memory = setup.parse_memory('data.txt')
    config = setup.parse_config('config.txt')

    #print inst_list 
    #print lable_list
    #print register
    #print memory
    #print config

    return inst_list, label_list, register, memory, config

def update_state(ins, stage, val):
    if not state.has_key(ins):
        state[ins] = {'IF':'', 'ID':'', 'EX':'', 'WB':'', 'RAW':'','WAR':'','WAW':'','Struct':''}
        state_list.append({ins :state[ins]})
    state[ins][stage] = val


def to_string(ins):
    rv = ''
    for i in ins:
        rv = rv + i + ' '
    return rv.strip()


def status():

    print ""
    print "After Clock: " + str(clock)
    print "IF: {0}  //  ID: {1} ID_RDY: {2}  //  EX: {3} EX_RDY: {4}  //  WB: {5}".format(IF, ID, ID_Ready, EX, EX_Ready, WB)
    print ""
    print "IF_Proceed: " + str(IF_Proceed)
    print execute.status()
    print ""
    print "Instruction\t\tIF\tID\tEX\tWB\tRAW\tWAR\tWAW\tStruct"
    for s in state_list:
        print s.keys()[0] + (21 - len(s.keys()[0])) * ' ' +  "\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(s[s.keys()[0]]['IF'], s[s.keys()[0]]['ID'], s[s.keys()[0]]['EX'], s[s.keys()[0]]['WB'], s[s.keys()[0]]['RAW'], s[s.keys()[0]]['WAR'], s[s.keys()[0]]['WAW'], s[s.keys()[0]]['Struct'])

    

        

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
    global IF_Proceed

    if proceed and (len(IF) != 0 or len(ID) != 0):
        
        # TODO This may be trouble trying to remove from list
        # TODO Is this proper way to prevent more fetches?
        if len(IF) > 0:
            ID.append(IF.pop(0))

        # TODO do jumps/branches first so we don't have to do parsing issues
        # TODO do we also need to check EX_Ready() - I think so
        
        tempID = list(ID)
        for inst in tempID:
            if not execute.unitFree(inst, clock):
                # TODO record hazard here? Waiting on a FU is a structural hazard right?
                update_state(to_string(inst), "Struct", "Y")
                IF_Proceed = False
                continue
            if decode.RAW_Hazard(inst, EX + EX_Ready):
                update_state(to_string(inst), "RAW", "Y")
                IF_Proceed = False
                continue
            # TODO do WAW here?
            if decode.WAW_Hazard(inst, EX + EX_Ready):
                update_state(to_string(inst), "WAW", "Y")
                IF_Proceed = False
                continue


            ID_Ready.append(inst)
            ID.remove(inst)
            update_state(to_string(inst), "ID", clock)

        # TODO this needs to change to if there are no more delayed instructions due to structural hazards
        if len(ID) == 0:
            IF_Proceed = True


def EX_stage():
    global ID_Ready

    if proceed and len(ID_Ready) != 0:
        

        # can we have multiple instructions enter EX, sure!
        for inst in ID_Ready:

            EX.append(inst)

            completion_cycle = execute.start(inst, clock, register)

            if not EX_completion.has_key(completion_cycle):
                EX_completion[completion_cycle] = list()
                EX_completion[completion_cycle].append(inst)
            else:
                EX_completion[completion_cycle].append(inst)

        ID_Ready = []
                 
        # check EX_completion here too to do the status update
        # Need to account for multiple instructions finishing in this cycle

        if EX_completion.has_key(clock):
            inst_list = EX_completion[clock]
            for inst in inst_list:
                # TODO implement MEM here, maybe have to make a MEM_completion and check that each cycle and put it after this block
                if execute.needsMem(inst):
                    
                    completion_cycle, result = execute.Mem(inst, clock)

                    if not MEM_completion.has_key(completion_cycle):
                        MEM_completion[completion_cycle] = list()
                        MEM_completion[completion_cycle].append(inst)
                    else:
                        EX_completion[completion_cycle].append(inst)
                    continue

                update_state(to_string(inst), "EX", clock)
                EX.remove(inst)
                EX_Ready.append(inst)

        if MEM_completion.has_key(clock):
            inst_list = MEM_completion[clock]
            for inst in inst_list:
                update_state(to_string(inst), "EX", clock)
                EX.remove(inst)
                EX_Ready.append(inst)




def WB_stage():
    if proceed and len(EX_Ready) != 0:
        global WB

        WB = []


        # TODO do WAR Hazard here?
        #if decode.WAR_Hazard(inst, EX + EX_Ready):
        #    update_state(to_string(inst), "WAR", "Y")


        # Contention for single WB port
        # TODO Priority given to not pipelined FU that takes most cycles, if tie, earielst issued
        # TODO Record Structural Hazard
        
        if len(EX_Ready) > 1:
            # TODO Change this
            WB.append(EX_Ready.pop())
        elif len(EX_Ready) == 1:
            WB.append(EX_Ready.pop())
        
        inst = WB[0]
        update_state(to_string(inst), "WB", clock)

    
###
# State Variables
###

instruction, labels, register, memory, config = setup()

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
decode = Id()


EX_completion = {}
MEM_completion = {}
state = {}
state_list = []

pdb.set_trace()

while True:
    clock = clock + 1

    if clock == 4:
        pdb.set_trace()

    WB_stage()
        
    EX_stage()
    
    ID_stage()
    
    IF_stage()

    status()




