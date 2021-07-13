from core.cpu.instructions import Cpu
from core.cpu.config.memory_starter import MemoryStarter
from core.cpu.config.memory_config import Config
from core.reader.file_reader import FileReader


class Main:

    def __init__(self):
        self.chip8_cpu = Cpu()
        self.memory_management = MemoryStarter(self.chip8_cpu)

    def run(self):
        binary_file = FileReader.file_reader()
        file_buffer_list = FileReader.load_binary_to_buffer(binary_file)
        self.memory_management.load_into_memory(file_buffer_list, Config.MEMORY_START_ADDRESS)
        self.memory_management.load_into_memory(Config.FONT_SET, Config.FONT_SET_START_ADDRESS)
        self.cycle()

    def cycle(self):
        program_counter = self.chip8_cpu.pc
        self.chip8_cpu.current_opcode = self.chip8_cpu.memory[program_counter] << 8 | \
                                        self.chip8_cpu.memory[program_counter + 1]
        self.chip8_cpu.pc += 2
        print(hex(self.chip8_cpu.current_opcode))
