#!/usr/bin/python

'''
control.py

The controller to kick of all stages of the MIPS processor

'''


from instruction import Instruction

inst = Instruction()
inst.parse('sample_code')
