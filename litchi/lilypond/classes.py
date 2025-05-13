from typing import List, Optional
from quickly.dom import lily

class Tempo:
    def __init__(self):
        self.onset: float = 0.0
        self.div: Optional[str] = None
        self.bpm: Optional[int] = None

class Event:
    def __init__(self):
        self.name: Optional[str] = None
        self.pitch: Optional[str] = None
        self.onset: float = 0.0
        self.octave: Optional[int] = 0
        self.articulations: List[lily.Articulations] = []
        self.freq: Optional[float] = None
        self.dyn: Optional[float] = None
        self.env = 0
        self.channels = 2

class Rest:
    def __init__(self):
        self.name: Optional[str] = None
        self.onset: float = 0.0

class Processor:
    def __init__(self, nodes):
        self.nodes = nodes

    def process(self):
        raise NotImplementedError("Subclasses should implement this method.")
