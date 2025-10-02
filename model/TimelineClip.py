class TimelineClip:
    name: str
    start: float
    end: float
    
    def __init__(self, name: str, start: float, end: float):
        self.name = name
        self.start = start
        self.end = end