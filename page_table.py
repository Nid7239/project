import time

class Entry:
    def __init__(self, frame=None):
        self.frame = frame
        self.valid = 1 if frame else 0
        self.reference = 0
        self.last_access = time.time()
    def access(self):
        self.reference += 1
        self.last_access = time.time()
class PageTable:
    def __init__(self):
        self.entries = {}

    def get(self, page):
        return self.entries.get(page)

    def map(self, page, frame):
        if page not in self.entries:
            self.entries[page] = Entry(frame)
        else:
            self.entries[page].frame = frame
            self.entries[page].valid = 1

        self.entries[page].access()

    def unmap(self, page):
        if page in self.entries:
            self.entries[page].valid = 0