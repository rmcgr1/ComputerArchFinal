#!/usr/bin/python

'''
control.py

The controller to kick of all stages of the MIPS processor

'''

import pdb
import argparse
import sys

from setup import Setup
from ex import Ex
from id import Id
from instructioncache import If
from memorycache import Mem

###
# Helper Functions
###

def setup():
    setup = Setup()

    parser = argparse.ArgumentParser(description='Useage: simulator inst.txt data.txt reg.txt config.txt result.txt')

    parser.add_argument('inst.txt')
    parser.add_argument('data.txt')
    parser.add_argument('reg.txt')
    parser.add_argument('config.txt')
    parser.add_argument('result.txt')
    
    args = parser.parse_args()
    if len(vars(args)) != 5:
        print "Useage: simulator inst.txt data.txt reg.txt config.txt result.txt"
        sys.exit(0)

    inst_list, label_list = setup.parse_instructions(vars(args)['inst.txt'])
    register = setup.parse_registers(vars(args)['reg.txt'])
    memory = setup.parse_memory(vars(args)['data.txt'])
    config = setup.parse_config(vars(args)['config.txt'])
    priority = setup.return_priority(config)

    #print inst_list 
    #print lable_list
    #print register
    #print memory
    #print config

    return inst_list, label_list, register, memory, config, priority

def update_state(inst, stage, val, flush=False):
    if not state.has_key(inst):
        state[inst] = {'IF':'', 'ID':'', 'EX':'', 'WB':'', 'RAW':'','WAR':'','WAW':'','Struct':''}
        state_list.append({inst :state[inst]})
    state[inst][stage] = val

    if not result.has_key(inst):
        result[inst] = {'IF':' ', 'ID':' ', 'EX':' ', 'WB':' ', 'RAW':'N','WAR':'N','WAW':'N','Struct':'N'}
    result[inst][stage] = val

    # TODO get labels, branches, and HLTs
    if stage == 'WB' or (inst.split()[0] in Branch_Ops and stage == 'ID') or (inst.split()[0] == 'HLT' and stage == 'ID') or flush:
        result_list.append("{0}\t\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}".format(inst, result[inst]['IF'], result[inst]['ID'], result[inst]['EX'], result[inst]['WB'], result[inst]['RAW'], result[inst]['WAR'], result[inst]['WAW'], result[inst]['Struct']))


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
    print "IF_Proceed: " + str(IF_Proceed) + " MEM_BUSY: " + str(MEM_BUSY)
    print execute.status()
    print ""
    print "Instruction\t\tIF\tID\tEX\tWB\tRAW\tWAR\tWAW\tStruct"
    for s in state_list:
        print s.keys()[0] + (21 - len(s.keys()[0])) * ' ' +  "\t{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(s[s.keys()[0]]['IF'], s[s.keys()[0]]['ID'], s[s.keys()[0]]['EX'], s[s.keys()[0]]['WB'], s[s.keys()[0]]['RAW'], s[s.keys()[0]]['WAR'], s[s.keys()[0]]['WAW'], s[s.keys()[0]]['Struct'])

    
def get_issue_cycle(inst):
    for s in state_list:
        if s.keys()[0] == inst[0]:
            return s[s.keys()[0]]['IF']

def FU_type(inst):
    op = inst[0]
    if op in Int_Arithmetic:
        return 'IU'
    if op in Mem_Ops:
        return 'IU'
    if op in Int_Arithmetic:
        return 'IU'
    if op == "ADD.D" or op == "SUB.D":
        return 'FP adder'
    if op == "MUL.D":
        return 'FP Multiplier'
    if op == "DIV.D":
        return 'FP divider'
    
    
Mem_Ops = ['LW', 'SW', 'L.D', 'S.D']
Branch_Ops = ['J', 'BNE', 'BEQ']


def IF_stage():
    global EIP
    global IF_Flush
    global IF_Cache_Proceed
    global IF_New_EIP

    inst = ''

    if proceed and IF_Proceed:
        completion_cycle = 0
        if IF_Cache_Proceed:
            # TODO record ICache miss to stall DCache
            inst, completion_cycle = fetch.get_instruction(EIP, clock)

            #if not IF_completion.has_key(completion_cycle):
            IF_completion[completion_cycle] = inst
            
            EIP = EIP + 4
        
        if completion_cycle != clock:
            IF_Cache_Proceed = False

        if IF_completion.has_key(clock):
            inst = IF_completion[clock]
            IF.append(inst)
            update_state(to_string(inst), "IF", clock)
            IF_Cache_Proceed = True
            IF_completion.pop(clock)

    if IF_Flush:
        if not STOPPING:
            IF_Flush = False
        update_state(to_string(inst), "IF", clock, True)
        if inst != '':
            IF.remove(inst)
        if STOPPING:
            clean_up()

    if IF_New_EIP != -1:
        EIP = IF_New_EIP
        IF_New_EIP = -1



        
def ID_stage():
    global IF_Proceed
    global IF_Flush
    global EIP
    global IF_New_EIP
    global STOPPING

    if proceed and (len(IF) != 0 or len(ID) != 0):
        
        # TODO This may be trouble trying to remove from list
        # TODO Is this proper way to prevent more fetches?
        if len(IF) > 0:
            ID.append(IF.pop(0))

        
        # Check for jumps or branches, and flush IF if taken
        
        tempID = list(ID)
        for inst in tempID:

            # TODO: do a clean exit
            if inst[0] == 'HLT':
                pdb.set_trace()
                ID.remove(inst)
                update_state(to_string(inst), "ID", clock)
                IF_Flush = True
                STOPPING = True
                # TODO stop cleaner,
                clean_up()
                return


            if inst[0] == 'J':
                update_state(to_string(inst), "ID", clock)
                ID.remove(inst)
                for k in labels.keys():
                    if labels[k] == inst[1]:
                        IF_New_EIP = k 
                        IF_Flush = True
                        return

            elif inst[0] == 'BEQ':
                if decode.RAW_Hazard_Branch(inst, EX + EX_Ready):
                    update_state(to_string(inst), "RAW", "Y")
                    IF_Proceed = False
                    continue
                IF_Proceed = True
                update_state(to_string(inst), "ID", clock)
                ID.remove(inst)
                if register[inst[1]] == register[inst[2]]:
                    for k in labels.keys():
                        if labels[k] == inst[3]:
                            IF_New_EIP = k 
                            IF_Flush = True
                            return
                else:
                    return

            elif inst[0] == 'BNE':
                if decode.RAW_Hazard_Branch(inst, EX + EX_Ready):
                    update_state(to_string(inst), "RAW", "Y")
                    IF_Proceed = False
                    continue
                IF_Proceed = True
                update_state(to_string(inst), "ID", clock)
                ID.remove(inst)
                if register[inst[1]] != register[inst[2]]:
                    for k in labels.keys():
                        if labels[k] == inst[3]:
                            IF_New_EIP = k 
                            IF_Flush = True
                            return
                else:
                    return
            if not execute.unitFree(inst, clock):
                # TODO record hazard here? Waiting on a FU is a structural hazard right?
                update_state(to_string(inst), "Struct", "Y")
                IF_Proceed = False
                continue
            if inst[0] in Mem_Ops and clock >= MEM_BUSY:
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
    global MEM_BUSY

    if proceed and (len(ID_Ready) != 0 or len(EX) != 0):
        

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
        
        if MEM_completion.has_key(clock):
            MEM_BUSY = 10000000
            inst_list = MEM_completion[clock]
            for inst in inst_list:
                # TODO resolve WB contension before getting to WB/Recording leaving EX
                update_state(to_string(inst), "EX", clock)
                EX.remove(inst)
                EX_Ready.append(inst)
            MEM_completion.pop(clock)

        if EX_completion.has_key(clock):
            inst_list = EX_completion[clock]
            for inst in inst_list:
                if execute.needsMem(inst):
                    
                    if clock >= MEM_BUSY:
                        update_state(to_string(inst), "Struct", 'Y')
                        if not EX_completion.has_key(clock + 1 ):
                            EX_completion[clock + 1] = list()
                            EX_completion[clock + 1].append(inst)
                        else:
                            EX_completion[clock + 1].append(inst)
                        continue


                    result, completion_cycle = mem.access_memory(inst, clock)
                    MEM_BUSY = clock + 1

                    if not MEM_completion.has_key(completion_cycle):
                        MEM_completion[completion_cycle] = list()
                        MEM_completion[completion_cycle].append(inst)
                    else:
                        MEM_completion[completion_cycle].append(inst)
                else:
                    # Non memory using instruction finishing EX
                    # TODO resolve WB contension before getting to WB/Recording leaving EX
                    update_state(to_string(inst), "EX", clock)
                    EX.remove(inst)
                    EX_Ready.append(inst)
            EX_completion.pop(clock)




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
        # TODO keep FU busy for stalled instruction
        # TODO what about MEM Ops?
        
        if len(EX_Ready) > 1:
            order = []

            # Go through each priority, and if only one hit for each priority issue and move on, else break tie by figuring out issue cycle
            for p in priority:
                FU = p[0]
                tempEX_Ready = list(EX_Ready)

                for inst in tempEX_Ready:
                    if FU_type(inst) == FU:
                        order.append(inst)

                if len(order) == 1:
                    # Issue
                    inst = order[0]
                    WB.append(inst)
                    EX_Ready.remove(inst)
                    update_state(to_string(inst), "WB", clock)

                    # Give all other instructions Structural Hazards
                    for i in EX_Ready:
                        if i != inst:
                            update_state(to_string(i), "Struct", 'Y')
                    break

                elif len(order) > 1:
                    # TODO test this

                    order.sort(key=lambda x: get_issue_cycle(x), reverse=True)
                    EX_Ready.remove(order[0])
                    update_state(to_string(order[0]), "WB", clock)
                    
                    # Give all other instructions Structural Hazards
                    for i in EX_Ready:
                        if i != inst:
                            update_state(to_string(i), "Struct", 'Y')
                    break

        elif len(EX_Ready) == 1:
            inst = EX_Ready.pop()
            update_state(to_string(inst), "WB", clock)


def clean_up():

    print ""
    print ""
    print ""
    for r in result_list:
        if r.startswith('HLT'):
            print 'HLT\t' + r[3:]
        else:
            print r
    print ''
    print "Total number of access requests for instruction cache: " + str(stats['IC_REQ'])
    print ''
    print "Number of instruction cache hits: " + str(stats['IC_HITS'])
    print ''
    print "Total number of access requests for data cache: " + str(stats['DC_REQ'])
    print ''
    print "Number of data cache hits: " + str(stats['DC_HITS'])

    sys.exit(0)
    


    
###
# State Variables
###

instruction, labels, register, memory, config, priority = setup()

instruction.keys().sort()

clock = 0
EIP = 0

proceed = True
IF_Proceed = True
IF_Flush = False
IF_Cache_Proceed = True
IF_New_EIP = -1

STOPPING = False

MEM_BUSY = 10000000

IF = []
ID = []
ID_Ready = []
EX = []
EX_Ready = []
WB = []

result = {}
result_list = []
result_list.append('instruction\t\tIF\tID\tEX\tWB\tRAW\tWAR\tWAW\tStruct')
stats = {'IC_REQ' : 0, 'IC_HITS' : 0, 'DC_REQ' : 0, 'DC_HITS' : 0}

execute = Ex(config, register)
decode = Id()
fetch = If(config, instruction, stats)
mem = Mem(config, memory, register, stats)

EX_completion = {}
IF_completion = {}
MEM_completion = {}
state = {}
state_list = []


Int_Arithmetic = ['DADD', 'DADDI', 'DSUB', 'DSUBI', 'AND', 'ANDI', 'OR', 'ORI']
Mem_Ops = ['LW', 'SW', 'L.D', 'S.D']
Branch_Ops = ['J', 'BNE', 'BEQ']


pdb.set_trace()

while True:
    clock = clock + 1

    if clock == 6:
        pdb.set_trace()

    WB_stage()
        
    EX_stage()
    
    ID_stage()
    
    IF_stage()

    status()

#    if len(IF) == 0 and len(IF_completion) == 0 and len(ID) == 0 and len(ID_Ready) == 0 and len(EX) == 0 and len(EX_completion) == 0 and len(MEM_completion) == 0 and len(EX_Ready) == 0 and len(WB) == 0:
#       clean_up()




