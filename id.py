#!/usr/bin/python

import pdb
import sys

class Id:

    def RAW_Hazard(self, inst, EX):
        source_registers = self.getSourceRegisters(inst)
        dest_registers = self.getDestinationRegisers(EX)

        for r in source_registers:
            if r in dest_registers:
                return True
        # Check to see if any srcs are destinations

        return False

    def RAW_Hazard_Branch(self, inst, EX):
        source_registers = self.getSourceRegistersBranch(inst)
        dest_registers = self.getDestinationRegisers(EX)

        for r in source_registers:
            if r in dest_registers:
                return True
        # Check to see if any srcs are destinations

        return False
    
    # TODO Implement here
    def WAR_Hazard(self, inst, EX):
        return False

    # TODO Implement here
    def WAW_Hazard(self, inst, EX):
        return False

    def getDestinationRegisers(self, EX):
        l = []
        for inst in EX:
            l.append(inst[1].strip(','))
        return l

    def getSourceRegisters(self, inst):
        l = []

        if len(inst) == 3:
            sec = inst[-1].strip(',()')
            if sec.find('R') != -1:
                l.append(sec[sec.find('R'):])
            if sec.find('F') != -1:
                l.append(sec[sec.find('F'):])

            
        if len(inst) == 4:
            l.append(inst[-2].strip(',()'))
            sec = inst[-1].strip(',()')
            if sec.find('R') != -1:
                l.append(sec[sec.find('R'):])
            if sec.find('F') != -1:
                l.append(sec[sec.find('F'):])
        
        return l

    def getSourceRegistersBranch(self, inst):
        l = []

        l.append(inst[1])
        l.append(inst[2])

        return l
