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
        print(hex(self.chip8_cpu.memory[512]))
        print(hex(self.chip8_cpu.memory[513]))
        print(hex(self.chip8_cpu.memory[0x2b4]))
        print(hex(self.chip8_cpu.memory[0x2b4 + 1]))

    def cycle(self):
        # self.chip8_cpu.current_opcode = self.chip8_cpu.config
        pass