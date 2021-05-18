

class MemoryStarter:

    def __init__(self, chip8_cpu):
        self.chip8_cpu = chip8_cpu

    def load_into_memory(self, list_values, starting_address):
        ending_address = len(list_values) + starting_address
        self.chip8_cpu.memory[starting_address:ending_address] = list_values
