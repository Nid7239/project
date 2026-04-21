import math
from constants import PAGE_SIZE
class File:
    def __init__(self,file_id, size):
        self.file_id=file_id
        self.size=size
        self.pages=self.create_pages()
    def create_pages(self):
        #do calculate how much pages each file must have 
        num_pages=math.ceil(self.size/PAGE_SIZE)
        return [f"{self.file_id}_p{i}" for i in range(num_pages)]