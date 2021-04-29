from core.cpu import Cpu
from core.memory_management import MemoryManagement
from core.chip8_config.config import Config
from core.chip8_config.file_reader import FileReader


class Main:

    def __init__(self):
        self.chip8_cpu = Cpu()
        self.memory_management = MemoryManagement(self.chip8_cpu)

    def run(self):
        binary_file = FileReader.file_reader()
        file_buffer_list = FileReader.load_binary_to_buffer(binary_file)
        self.memory_management.load_into_memory(file_buffer_list, Config.MEMORY_START_ADDRESS)
        self.memory_management.load_into_memory(Config.FONT_SET, Config.FONT_SET_START_ADDRESS)
        print(hex(self.chip8_cpu.memory[512]))
        print(hex(self.chip8_cpu.memory[513]))
        print(hex(self.chip8_cpu.memory[0x2b4]))
        print(hex(self.chip8_cpu.memory[0x2b4 + 1]))
        self.chip8_cpu.pc = self.chip8_cpu.memory[512]