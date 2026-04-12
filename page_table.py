from constants import MAX_FRAMES

class PageTable:
    def __init__(self,max_frames=MAX_FRAMES):
        self.max_frames=max_frames

        self.frames = [[None,0] for _ in range(max_frames)]
        self.time = 0

    # PUBLIC FUNCTION
    def access_page(self,page):
        self.time += 1

        for i in range(self.max_frames):
            if self.frames[i][0] == page:
                self.frames[i][1]=self.time  # update last access time
                return i, "HIT"   # return address

        for i in range(self.max_frames):
            if self.frames[i][0] is None:
                self.frames[i]=[page, self.time]
                return i, "FAULT"

        lru_index = self._find_lru()
        self.frames[lru_index]=[page, self.time]
        return lru_index, "FAULT"

    def _find_lru(self):
        min_time = self.frames[0][1]
        lru_index = 0

        for i in range(1,self.max_frames):
            if self.frames[i][1] <min_time:
                min_time=self.frames[i][1]
                lru_index= i

        return lru_index