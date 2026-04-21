from page_entry import PageEntry

class PageTable:
    def __init__(self):
        self.entries ={}
    def get_entry(self,page):
        return self.entries.get(page)
    def map(self,page,frame):
        entry =PageEntry(page)
        entry.frame=frame
        entry.valid=1
        entry.access()
        self.entries[page]=entry
        return entry
    def unmap(self,page):
        if page in self.entries:
            self.entries[page].valid=0
            self.entries[page].frame=None