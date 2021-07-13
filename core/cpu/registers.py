from collections import deque
import numpy as np
from core.cpu.config.memory_config import Config


class Registers:
    def __init__(self):
        self.registers = np.zeros(16, dtype=np.uint8)
        self.memory = np.zeros(4096, dtype=np.uint8)
        self.stack = deque()
        self.keypad = np.zeros(16, dtype=np.uint8)
        self.video_display = np.zeros((128, 32), dtype=np.uint8)
        self.current_opcode = 0
        self.index = 0
        self.pc = Config.MEMORY_START_ADDRESS
        self.stack_pointer = 0
        self.delay_timer = 0
        self.sound_timer = 0
