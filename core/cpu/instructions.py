import numpy as np
from core.cpu.registers import Registers
from core.cpu.config.memory_config import Config


class Cpu(Registers):

    def __init__(self):
        super().__init__()
        self.instructions_table = {}
        self.config_instructions()

    def config_instructions(self):

        self.instructions_table = {
            # Unique OPCODES
            '1': self.jump_to_location,
            '2': self.call_to_location,
            '3': self.skip_instr_register_x_equals_kk,
            '4': self.skip_instr_register_x_not_equal_kk,
            '5': self.skip_instr_register_x_equal_y,
            '6': self.load_value_into_register,
            '7': self.load_value_into_register_add,
            '9': self.skip_instr_register_x_not_equal_y,
            'a': self.store_addr_on_index,
            'b': self.jump_to_location_nnn_plus_register_zero,
            'c': self.store_random_number_on_register_x,
            'd': self.display_bytes_on_screen,
            # Digit 8 on start
            '8': {'0': self.load_register_y_into_register_x,
                  '1': self.cmp_or_x_y_into_register_x,
                  '2': self.cmp_and_x_y_into_register_x,
                  '3': self.cmp_xor_x_y_into_register_x,
                  '4': self.add_x_y_into_register_x,
                  '5': self.sub_x_y_into_register_x,
                  '6': self.div_x_into_register_x,
                  '7': self.sub_y_x_into_register_x,
                  'e': self.mul_x_into_register_x
                  },
            # Digit 0 starters
            '00e0': self.clear_the_display,
            '00ee': self.return_from_subroutine,
            # Digit E start
            'e': {'a1': self.not_skip_instruction_if_key_pressed,
                  '9e': self.skip_instruction_if_key_pressed},
            # Digit F start
            'f': {'07': self.delay_timer_on_register_x,
                  '0a': self.wait_for_key_press,
                  '15': self.register_x_on_delay_timer,
                  '18': self.sound_timer_on_register_x,
                  '1e': self.add_register_x_and_index,
                  '29': self.stores_on_index_hex_sprite,
                  '33': self.load_bcd_on_memory,
                  '55': self.load_registers_onto_memory,
                  '65': self.load_memory_onto_register}
            }

    def clear_the_display(self):
        """
        Completely set the video display to off, setting the array to False

        OP_CODE: 00E0
        """
        self.video_display = np.zeros((128, 32), dtype=np.uint8)

    def return_from_subroutine(self):
        """
        Return back to a subroutine stored on the stack pointer

        OP_CODE: 00EE
        """
        self.stack_pointer -= 1
        self.pc = self.stack[self.stack_pointer]

    def jump_to_location(self):
        """
        Jump to a specific config location without saving current status on the stack

        OP_CODE: 1nnn
        OP_WHAT: 1 - Instruction / nnn - 12 bit address
        OP_description: Sets the program counter (pc) to the 12 bit address specified in the nnn.
        """
        self.pc = self.current_opcode & 0x0FFF

    def call_to_location(self):
        """
        Call to a specific config location saving the current status on the stack

        OP_CODE: 2nnn
        OP_WHAT: 2 - Instruction  / nnn - 12 bit address
        OP_description: Saves the current opcode on the stack and sets the program counter (pc) to the 12 bit config
        address specified in the nnn and
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

    def skip_instr_register_x_not_equal_kk(self):
        """
        Skips the next instructions if the Register[x] is NOT equal to the kk address on the opcode

        OP_CODE: 4xkk
        OP_WHAT: 4 - Instruction / x - 4 bit register address / kk - 8 bit content to compare
        OP_description: Skip the pc if the register[x] is NOT equal to the kk byte content-wise
        """
        x = self.current_opcode & 0x0F00 >> 8
        kk = self.current_opcode & 0x00FF

        if self.registers[x] != kk:
            self.pc += 2

    def skip_instr_register_x_equal_y(self):
        """
        Skips the next instructions if the Register[x] is  equal to the register[y]

        OP_CODE: 5xy0
        OP_WHAT: 5 - Instruction / x - 4 bit register address / 4 - 4 bit register address / 0 - Unused
        OP_description: Skip the pc if the register[x] is equal to the register[y] byte content-wise
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4

        if self.registers[x] == self.registers[y]:
            self.pc += 2

    def load_value_into_register(self):
        """
        Load the value of kk into a register specified in the opcode

        OP_CODE: 6xkk
        OP_WHAT: 6 - Instruction / x - 4 bit register address / kk - 8 bit content to compare
        OP_description: Load the value kk into the register specified by the x
        """
        x = self.current_opcode & 0x0F00 >> 8
        kk = self.current_opcode & 0x00FF
        self.registers[x] = kk

    def load_value_into_register_add(self):
        """
        Load the value of (kk + register[x]) into a register specified in the opcode

        OP_CODE: 7xkk
        OP_WHAT: 7 - Instruction / x - 4 bit register address / kk - 8 bit content to compare
        OP_description: Load the value kk + register[x] into the register specified by the x
        """
        x = self.current_opcode & 0x0F00 >> 8
        kk = self.current_opcode & 0x00FF
        xkk = self.registers[x] + kk
        self.registers[x] = xkk

    def load_register_y_into_register_x(self):
        """
        Stores the value of register[y] into register[x]

        OP_CODE: 8xy0
        OP_WHAT: 8 - Instruction / x - 4 bit register address / y - 4 bit register address / 0 - Instruction
        OP_description: Load the content of register[y] into register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4
        self.registers[x] = self.registers[y]

    def cmp_or_x_y_into_register_x(self):
        """
        Performs a bitwise OR between values of register[x] and register[y]

        OP_CODE: 8xy1
        OP_WHAT: 8 - Instruction / x - 4 bit register address / y - 4 bit register address / 1 - Instruction
        OP_description: Perfoms a bitwise comparasion OR between the values of register[x] and register[y] and stores the
        result into register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4
        self.registers[x] = x | y

    def cmp_and_x_y_into_register_x(self):
        """
        Performs a bitwise AND between values of register[x] and register[y]

        OP_CODE: 8xy2
        OP_WHAT: 8 - Instruction / x - 4 bit register address / y - 4 bit register address / 2 - Instruction
        OP_description: Perfoms a bitwise comparasion between AND the values of register[x] and register[y] and stores the
        result into register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4
        self.registers[x] = x & y

    def cmp_xor_x_y_into_register_x(self):
        """
        Performs a bitwise XOR between values of register[x] and register[y]

        OP_CODE: 8xy3
        OP_WHAT: 8 - Instruction / x - 4 bit register address / y - 4 bit register address / 3 - Instruction
        OP_description: Perfoms a bitwise comparasion between XOR the values of register[x] and register[y] and stores the
        result into register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4
        self.registers[x] = x ^ y

    def add_x_y_into_register_x(self):
        """
        Performs a ADD between the values of register[x] and register[y]

        OP_CODE: 8xy4
        OP_WHAT:  8 - Instruction / x - 4 bit register address / y - 4 bit register address / 4 - Instruction
        OP_description: Perfoms a ADD between register[x] and register[y] and stores the result value into register[x].
        If the result is greater than 255, than the register[0xF] (int(15)) is set to 1.
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4
        add_x_y = x + y
        self.registers[x] = add_x_y & 0x00FF
        if add_x_y > 255:
            self.registers[int(0xF)] = 1
        else:
            self.registers[int(0xF)] = 0

    def sub_x_y_into_register_x(self):
        """
        Performs a SUB between the values of register[x] and register[y]

        OP_CODE: 8xy5
        OP_WHAT:  8 - Instruction / x - 4 bit register address / y - 4 bit register address / 5 - Instruction
        OP_description: Perfoms a SUB between register[x] and register[y] and stores the result value into register[x].
        If the register[x] > register[y], than the register[0xF] (int(15)) is set to 1.
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4

        if x > y:
            self.registers[int(0xF)] = 1
        else:
            self.registers[int(0xF)] = 0
        sub_x_y = x - y
        self.registers[x] = sub_x_y

    def div_x_into_register_x(self):
        """
        Performs a division register[x]

        OP_CODE: 8xy6
        OP_WHAT:  8 - Instruction / x - 4 bit register address / y - 4 bit unused / 6 - Instruction
        OP_description: Perfoms a DIV of register[x] and stores the result value into register[x].
        If the register[x] least significant bit is 1, than the register[0xF] (int(15)) is set to 1.
        """
        x = self.current_opcode & 0x0F00 >> 8

        if (x & 0x1) == 0x1:
            self.registers[int(0xF)] = 1
        else:
            self.registers[int(0xF)] = 0
        div_x = x / 2
        self.registers[x] = div_x

    def sub_y_x_into_register_x(self):
        """
        Performs a SUB between the values of register[y] and register[x]

        OP_CODE: 8xy7
        OP_WHAT:  8 - Instruction / x - 4 bit register address / y - 4 bit register address / 7 - Instruction
        OP_description: Perfoms a SUB between register[y] and register[x] and stores the result value into register[x].
        If the register[x] > register[y], than the register[0xF] (int(15)) is set to 1.
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4

        if x > y:
            self.registers[int(0xF)] = 1
        else:
            self.registers[int(0xF)] = 0
        sub_y_x = y - x
        self.registers[x] = sub_y_x

    def mul_x_into_register_x(self):
        """
        Performs a multiply register[x]

        OP_CODE: 8xyE
        OP_WHAT:  8 - Instruction / x - 4 bit register address / y - 4 bit unused / E - Instruction
        OP_description: Perfoms a MUL of register[x] and stores the result value into register[x].
        If the register[x] most significant bit is 1, than the register[0xF] (int(15)) is set to 1.
        """
        x = self.current_opcode & 0x0F00 >> 8

        if (x & 0x80 >> 7) == 0x1:
            self.registers[int(0xF)] = 1
        else:
            self.registers[int(0xF)] = 0
        mul_x = x * 2
        self.registers[x] = mul_x

    def skip_instr_register_x_not_equal_y(self):
        """
        Skips the next instructions if the Register[x] is  not equal to the register[y]

        OP_CODE: 9xy0
        OP_WHAT: 9 - Instruction / x - 4 bit register address / 4 - 4 bit register address / 0 - Unused
        OP_description: Skip the pc by 2 if the register[x] is not equal to the register[y] byte content-wise
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4

        if self.registers[x] != self.registers[y]:
            self.pc += 2

    def store_addr_on_index(self):
        """
        Set an address on the index register

        OP_CODE: Annn
        OP_WHAT: A - Instruction / nnn - 12 bit register address.
        OP_description: Sets the value of the indes register with the 12 bit nnn address on the operand
        """
        addr = self.current_opcode & 0x0FFF
        self.index = addr

    def jump_to_location_nnn_plus_register_zero(self):
        """
        Jump to the location specified by the sum of the register 0 and the nnn operand

        OP_CODE: Bnnn
        OP_WHAT: B - Instruction / nnn - 12 bit register address.
        OP_description: Sets the program counter with register[0] + nnn
        """
        addr = self.current_opcode & 0x0FFF
        self.pc = addr + self.registers[0]

    def store_random_number_on_register_x(self):
        """
        Generates a random number that is anded with kk abd stored on a register

        OP_CODE: Cxkk
        OP_WHAT: C - Instruction / x - 4 bit register address / kk - 8 bit value
        OP_description: Sets the register[x] a random number anded with the kk value
        """
        # TODO: Implementation of a random number generation is still in working

    # TODO: Change the pixels values from raw to a exported attribute
    def display_bytes_on_screen(self):
        """
        Display n-bytes on screen

        OP_CODE: Dxyn
        OP_WHAT: D - Instruction / x - 4 bit register address / y - 4 bit register address / n - n bytes value
        OP_description: Change n bytes from position stored on register[x] and register[y]
        """
        x = self.current_opcode & 0x0F00 >> 8
        y = self.current_opcode & 0x00F0 >> 4
        num_bytes = self.current_opcode & 0x000F
        readed_bytes = []
        self.registers[0xF] = 0

        for i in range(num_bytes):
            readed_bytes.append([self.memory[self.index + i]])

        readed_array = np.array(readed_bytes, dtype=np.uint8)
        readed_array = np.unpackbits(readed_array, axis=1)

        for i, line in enumerate(readed_array):
            for j, element in enumerate(line):
                x_pos = (j + x) % 64
                y_pos = (i + y) % 32
                pixel_bit = self.video_display[x_pos][y_pos]
                pixel_result = element ^ pixel_bit
                self.video_display[x_pos][y_pos] = pixel_result
                if pixel_bit == 1 and pixel_result == 0:
                    self.registers[0xF] = 1

    def skip_instruction_if_key_pressed(self):
        """
        Skips the next instruction if the keys corresponding on the register x value is equal the value of the key
        OP_CODE: Ex9E
        OP_WHAT: E - Instruction / x - 4 bit register address / 9E - 8 bit instruction
        OP_description: If the register[x] is equal to the key number, than pc += 2
        """
        x = self.current_opcode & 0x0F00 >> 8

        if self.keypad[x]:
            self.pc += 2

    def not_skip_instruction_if_key_pressed(self):
        """
        Not Skips the next instruction if the keys corresponding on the register x value is equal the value of the key
        OP_CODE: ExA1
        OP_WHAT: E - Instruction / x - 4 bit register address / A1 - 8 bit instruction
        OP_description: If the register[x] is equal to the key number, than pc += 2
        """
        x = self.current_opcode & 0x0F00 >> 8

        if not self.keypad[x]:
            self.pc += 2

    def delay_timer_on_register_x(self):
        """
        Stores delay timer on register x

        OP_CODE: Fx07
        OP_WHAT: F - Instruction / x - 4 bit register address / 07 - 8 bit instruction
        OP_description: Stores the value of self.delay_timer on register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8

        self.registers[x] = self.delay_timer

    def wait_for_key_press(self):
        """
        Waits for a key to be pressed and stores value on register x

        OP_CODE: Fx0A
        OP_WHAT: F - Instruction / x - 4 register address / 0A - 8 bit instruction
        OP_description: Waits for a key to be pressed, and than stores the value of the key on register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8
        key_press = False

        while not key_press:
            key_pressed = np.where(self.keypad == 1)
            if key_pressed:
                self.registers[x] = key_pressed[0]
                key_press = True

    def register_x_on_delay_timer(self):
        """
        Stores register x value on the delay timer

        OP_CODE: Fx15
        OP_WHAT: F - Instruction / x - 4 bit register address / 15 - 8 bit instruction
        OP_description: Stores the value of register[x] on self.delay_timer
        """
        x = self.current_opcode & 0x0F00 >> 8

        self.delay_timer = self.registers[x]

    def sound_timer_on_register_x(self):
        """
        Stores sound timer on register x

        OP_CODE: Fx18
        OP_WHAT: F - Instruction / x - 4 bit register address / 18 - 8 bit instruction
        OP_description: Stores the value of self.sound_timer on register[x]
        """
        x = self.current_opcode & 0x0F00 >> 8

        self.registers[x] = self.sound_timer

    def add_register_x_and_index(self):
        """
        Add values of index and register x and stores on index

        OP_CODE: Fx1E
        OP_WHAT: F - Instruction / x - 4 bit register address / 1E - 8 bit instruction
        OP_description: Add values of self.index and register[x] and stores result on self.index
        """
        x = self.current_opcode & 0x0F00 >> 8

        self.index = self.registers[x] + self.index

    def stores_on_index_hex_sprite(self):
        """
        Stores the config address of sprite with register x value

        OP_CODE: Fx29
        OP_WHAT: F - Instruction / x - 4 bit register address / 29 - 8 bit instruction
        """

        x = self.current_opcode & 0x0F00 >> 8

        self.index = Config.FONT_SET_START_ADDRESS + (self.registers[x] * 5)

    def load_bcd_on_memory(self):
        """
        Stores the BCD representation of Vx in config on index locations

        OP_CODE: Fx33
        OP_WHAT:
        """

        x = self.current_opcode & 0x0F00 >> 8

        self.memory[self.index] = int(str(self.registers[x])[-3])
        self.memory[self.index + 1] = int(str(self.registers[x])[-2])
        self.memory[self.index + 2] = int(str(self.registers[x])[-1])

    def load_registers_onto_memory(self):
        """
        Stores the value of a register into the config
        OP_CODE: Fx55
        OP_WHAT:
        """

        x = self.current_opcode & 0x0F00 >> 8

        for i in range(x):
            self.memory[self.index + i] = self.registers[i]

    def load_memory_onto_register(self):
        """
        Stores the value of a register into the config
        OP_CODE: Fx65
        OP_WHAT:
        """

        x = self.current_opcode & 0x0F00 >> 8

        for i in range(x):
            self.registers[i] = self.memory[self.index + i]
