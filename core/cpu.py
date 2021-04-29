import numpy as np
from collections import deque


class Cpu:

    def __init__(self):
        self.registers = np.zeros(16, dtype=np.uint8)
        self.memory = np.zeros(4096, dtype=np.uint8)
        self.stack = deque()
        self.keypad = np.zeros(16, dtype=np.uint8)
        self.video_display = np.zeros((64, 32), dtype=np.bool_)
        self.current_opcode = 0
        self.index = 0
        self.pc = 0
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0

    def clear_the_display(self):
        """
        Completely set the video display to off, setting the array to False

        OP_CODE: 00E0
        """
        self.video_display = np.zeros((64, 32), dtype=np.bool_)

    def return_from_subroutine(self):
        """
        Return back to a subroutine stored on the stack pointer

        OP_CODE: 00EE
        """
        self.stack_pointer -= 1
        self.pc = self.stack[self.stack_pointer]

    def jump_to_location(self):
        """
        Jump to a specific memory location without saving current status on the stack

        OP_CODE: 1nnn
        OP_WHAT: 1 - Instruction / nnn - 12 bit address
        OP_description: Sets the program counter (pc) to the 12 bit address specified in the nnn.
        """
        self.pc = self.current_opcode & 0x0FFF

    def call_to_location(self):
        """
        Call to a specific memory location saving the current status on the stack

        OP_CODE: 2nnn
        OP_WHAT: 2 - Instruction  / nnn - 12 bit address
        OP_description: Saves the current opcode on the stack and   sets the program counter (pc) to the 12 bit address
        specified in the nnn and
        """
        self.stack_pointer += 1
        self.stack.append(self.pc)
        self.pc = self.current_opcode & 0x0FFF

    def skip_instr_register_x_equals_kk(self):
        """
        Skips the next instructions if the Register[x] is equal to the kk address on the opcode

        OP_CODE: 3xkk
        OP_WHAT: 3 - Instruction / x - 4 bit register address / kk - 8 bit content to compare
        OP_description: Skip the pc if the register[x] is equal to the kk byte content-wise
        """
        x = self.current_opcode & 0x0F00 >> 8
        kk = self.current_opcode & 0x00FF

        if self.registers[x] == kk:
            self.pc += 2
