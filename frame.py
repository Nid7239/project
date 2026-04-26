class Frame:
    def __init__(self, idx):
        self.idx = idx
        self.page = None

    def __str__(self):
        return f"Frame{self.idx}: {self.page}"