from constants import PAGE_SIZE

class File:
    def __init__(self, file_id, size):
        self.file_id = file_id
        self.size = size
        num_pages = (size + PAGE_SIZE - 1) // PAGE_SIZE if size > 0 else 0
        self.pages = [f"{file_id}_p{i}" for i in range(num_pages)]