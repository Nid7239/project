import time
class PageEntry:
    def __init__(self,page_number):
        self.page_number=page_number
        self.frame=None
        self.valid =0
        self.reference=0
        self.dirty=0
        self.last_access=None
    def access(self):
        self.reference=1
        self.last_access=time.time()