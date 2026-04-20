import time
class PageEntry:
    def __init__(self, page):
        self.page=page
        self.frame=None
        self.valid=0
        self.protection="RW"
        self.reference=0
        self.caching=True
        self.dirty=0
        self.last_used=time.time()