from constants import MAX_FRAMES

class PageTable:
    def __init__(self, max_frames=MAX_FRAMES):
        self.max_frames = max_frames #store no of frames


        self.frames = [[None, 0] for _ in range(max_frames)] #memory sructure
        #stores page,time 
        self.time = 0
        self.page_to_file = {}
    # FUNCTION
    def access_page(self, page):
        self.time += 1 #for each page time increases
        # HIT
        for i in range(self.max_frames):
            if self.frames[i][0] == page:
                self.frames[i][1] = self.time
                file = self.page_to_file[page] #store the file address
                return file, "HIT"

        #if empty frame found then  insert page
        for i in range(self.max_frames):
            if self.frames[i][0] is None:
                self.frames[i] = [page,self.time] #if empty insert 
                self.page_to_file[page] = f"/var/data/page_{page}.data" #store file address
                return self.page_to_file[page], "FAULT"
        # LRU
        lru_index = self._find_lru()

        old_page = self.frames[lru_index][0]
        del self.page_to_file[old_page]

        self.frames[lru_index] = [page, self.time]
        self.page_to_file[page] = f"/var/data/page_{page}.data"
        return self.page_to_file[page], "FAULT"

    # INTERNAL FUNCTION
    def _find_lru(self):
        min_time=self.frames[0][1]
        lru_index=0
#check which frame has smaleest access time
        for i in range(1,self.max_frames):
            if self.frames[i][1]<min_time:
                min_time=self.frames[i][1]
                lru_index=i
        return lru_index