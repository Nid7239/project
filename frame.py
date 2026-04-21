class Frame:
    def __init__(self, frame_id):
        self.frame_id = frame_id
        self.page = None

    def __repr__(self):
        return f"Frame{self.frame_id}: {self.page}"