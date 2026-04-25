from constants import PAGE_SIZE
class File:
    def __init__(self, file_id, size):
        self.file_id = file_id
        self.size = size
        self.pages = [f"{file_id}_p{i}" for i in range(size//PAGE_SIZE)]