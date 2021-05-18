import numpy as np


class FileReader:

    @staticmethod
    def file_reader(file_path='roms/Tetris.ch8'):
        opened_file = open(file_path, "rb").read()
        return opened_file

    @staticmethod
    def load_binary_to_buffer(binary_file):
        buffer = np.zeros(len(binary_file), dtype=np.uint8)
        for index, value in enumerate(binary_file):
            buffer[index] = value
        return buffer
