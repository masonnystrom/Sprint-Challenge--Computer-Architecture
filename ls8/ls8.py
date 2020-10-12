#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) != 2:
    raise TypeError('Enter a filename')
filename = sys.argv[1]

cpu = CPU()
cpu.load(filename)
cpu.run()

# for sctest.ls8
# python ls8/ls8.py sctest.ls8