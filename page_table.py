class Entry:
    def __init__(self, frame, timestamp):
        self.frame = frame
        self.valid = True
        self.last_access = timestamp
    def access(self, timestamp):
        self.last_access = timestamp
class PageTable:
    def __init__(self):
        self.entries = {}
    def get(self, page):
        return self.entries.get(page)
    def map(self, page, frame, timestamp):
        self.entries[page] = Entry(frame, timestamp)
    def unmap(self, page):
        """Destructive unmap: Clears the frame and removes the entry entirely."""
        if page in self.entries:
            entry = self.entries[page]
            if entry.frame:
                entry.frame.page = None  # Reclaim the physical frame
            del self.entries[page]       # Prevent table from growing infinitely