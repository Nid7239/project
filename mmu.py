import time
from frame import Frame
from page_table import PageTable

class MMU:
    def __init__(self,max_frames):
        self.frames=[Frame(i) for i in range(max_frames)]
        self.page_table=PageTable()

    def access_page(self,page):
        current_time =time.time()

        entry =self.page_table.get_entry(page)

        if entry and entry.frame:
            entry.reference=1
            entry.last_used=current_time
            entry.frame.time=current_time
            return entry.frame,"HIT"

        if not entry:
            entry = self.page_table.create_entry(page)

        for frame in self.frames:
            if frame.page is None:
                frame.page=page
                frame.time=current_time
                entry.frame=frame
                entry.valid=1
                entry.reference= 1
                entry.last_used= current_time
                return frame, "FAULT"

        lru_frame =min(self.frames, key=lambda f: f.time)

        old_page =lru_frame.page
        old_entry = self.page_table.get_entry(old_page)

        if old_entry:
            old_entry.valid =0
            old_entry.frame =None

            #for replacing the page in the frame
        lru_frame.page =page
        lru_frame.time =current_time
        entry.frame =lru_frame
        entry.valid =1
        entry.reference =1
        entry.last_used =current_time
        return lru_frame,"FAULT"