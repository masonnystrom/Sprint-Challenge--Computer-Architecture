""" CPU Functionality"""

import sys

LDI = 0b10000010 
PRN = 0b01000111 
HLT = 0b00000001
MULT = 0b10100010 
ADD = 0b10100000 
PUSH = 0b01000101
POP = 0b01000110
RET = 0b00010001
CALL = 0b01010000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
SP = 7

class CPU:
    """Main CPU class."""
    def __init__(self):
        """constructs a new CPU"""
        self.reg = [0] * 256
        self.ram = [0] * 128
        self.pc = 0
        self.flags = [0] * 8
    
    def load(self, filename):
        """Loads program into memory"""

        address = 0

        with open(filename, 'r') as fp:
            for line in fp:
                comment_split = line.split("#")
                num = comment_split[0].strip()
                if num == '': # ignore blanks
                    continue
                val = int(num, 2)
                self.ram_write(val, address)
                address += 1
    
    # Stores value in specified address in ram
    def ram_write(self, value, address):
        self.ram[address] = value

    # Returns value in ram stored in address
    def ram_read(self, address):
        return self.ram[address]
    

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] == self.reg[reg_b]
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            self.flags = [0] * 8
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flags[5] = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.flags[6] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flags[7] = 1
            else:
                raise Exception("unsupported operation")
    
    def trace(self):
        """
        Handy Function to print out the CPU state
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    

    def run(self):
        """Run the CPU."""
        while True:
            pc = self.pc
            instruction = self.ram_read(pc)

            if instruction == LDI:
                self.reg[self.ram_read(pc + 1)] = self.ram_read(pc + 2)
                self.pc += 3

            elif instruction == PRN:
                print(self.reg[self.ram_read(pc + 1)])
                self.pc +=2

            elif  instruction == MULT:
                register_a = self.ram_read(pc + 1)
                register_b = self.ram_read(pc + 2)
                self.alu('MUL', register_a, register_b)
                self.pc += 3

            elif instruction == ADD:
                register_a = self.ram_read(pc + 1)
                register_b = self.ram_read(pc + 2)
                self.alu("ADD", register_a, register_b)
                self.pc += 3

            elif instruction == PUSH:
                self.reg[SP] -= 1
                stack_address = self.reg[SP]
                register_number = self.ram_read(pc + 1)
                value = self.reg[register_number]
                self.ram_write(stack_address, value)
                self.pc += 2

            elif instruction == POP:
                stack_value = self.ram_read(self.reg[SP])
                register_number = self.ram_read(pc + 1)
                self.reg[register_number] = stack_value
                self.reg[SP] += 1 
                self.pc += 2

            elif instruction == CALL:
                self.reg[SP] -= 1
                stack_address = self.reg[SP]
                returned_address = pc + 2
                self.ram_write(stack_address, returned_address)
                register_number = self.ram_read(pc + 1)
                self.pc = self.reg[register_number]

            elif instruction == RET:
                self.pc = self.ram_read(self.reg[SP])
                self.reg[SP] += 1  

            elif instruction == CMP:
                register_a = self.ram_read(self.pc + 1)
                register_b = self.ram_read(self.pc + 2)
                value_a = self.reg[register_a]
                value_b = self.reg[register_b]
                if value_a == value_b:
                    self.flags = 0b1
                elif value_a > value_b:
                    self.flags = 0b10
                elif value_b > value_a:
                    self.flags = 0b100
                self.pc += 3

            elif instruction == JMP:
                register_a = self.ram_read(self.pc + 1)
                self.pc = self.reg[register_a]

            elif instruction == JEQ:
                if not self.flags & 0b1:
                    self.pc += 2
                elif self.flags & 0B1:
                    register_a = self.ram_read(self.pc + 1)
                    self.pc = self.reg[register_a]

            elif instruction == JNE:
                if self.flags & 0b1:
                    self.pc += 2
                elif not self.flags & 0b0:
                    register_a = self.ram_read(self.pc + 1)
                    self.pc = self.reg[register_a]

            elif instruction == HLT:
                sys.exit(1)

            else:
                print(f"Error: Unknown input:\t {instruction}")
                sys.exit(1)



