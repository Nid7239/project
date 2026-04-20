from page_entry import PageEntry

class PageTable:
    def __init__(self):
        self.entries = {}
    def get_entry(self, page):
        return self.entries.get(page)
    def create_entry(self, page):
        entry=PageEntry(page)
        self.entries[page] =entry
        return entry