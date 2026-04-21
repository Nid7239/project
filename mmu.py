from frame import Frame
from page_table import PageTable

class MMU:
    def __init__(self, num_frames):
        self.frames = [Frame(i) for i in range(num_frames)]
        self.page_table = PageTable()

    def access_page(self, page):
        entry = self.page_table.get_entry(page)

        # HIT
        if entry and entry.valid:
            entry.access()
            return "HIT"

        # FAULT (empty frame)
        for frame in self.frames:
            if frame.page is None:
                frame.page = page
                self.page_table.map(page, frame)
                return "FAULT"

        # LRU Replacement
        lru_entry = min(
            self.page_table.entries.values(),
            key=lambda e: e.last_access
        )

        old_page = lru_entry.page_number
        frame = lru_entry.frame

        self.page_table.unmap(old_page)

        frame.page = page
        self.page_table.map(page, frame)

        return "FAULT"