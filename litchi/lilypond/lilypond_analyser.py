# litchi/lilypond/parser.py
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import quickly
from quickly.dom import lily
from quickly.dom.scope import Scope


import litchi.lilypond.processor.node as node
import litchi.lilypond.processor.param as param
import litchi.lilypond.processor.articulation as articulation

# litchi/lilypond/analyzer.py
class LilyPondAnalyzer:
    """Handles musical analysis of a LilyPond tree"""
    
    def __init__(self, processors=None):
        self.processors = processors or [
            param.Duration,
            param.Dynamic,
            param.Frequency,
            articulation.Tie,
            articulation.Glissando
        ]
        self.metric_staff = None
        self.instrument_staves = []

    def find_staves(self, tree: lily.Node):
        """Identify different staff types in the score"""
        self.instrument_staves = []
        
        for context in tree // lily.Context:
            for token in context.descendants():
                if isinstance(token, lily.String) and token.head == 'MetricStaff':
                    self.metric_staff = context
                    break
                elif isinstance(token, lily.Symbol):
                    if token.head == 'Score':
                        break
                    elif token.head in ('Staff', 'PianoStaff', 'StaffGroup'):
                        self.instrument_staves.append(context)
                        break

    def process_events(self, events):
        """Apply all registered processors to events"""
        for processor_class in self.processors:
            processor = processor_class(events)
            processor.process()
        return events

    def normalize_timing(self, events, tempi):
        """Convert musical time to absolute time"""
        for tempo in tempi:
            tempo.onset *= 4
            tempo.bpm *= 4 * tempo.div
            
        for event_group in events:
            for event in event_group:
                event.onset *= 4
                event.dur *= 4
        return events, tempi

    def analyze(self, tree: lily.Node) -> Tuple[List, List]:
        """Main analysis pipeline"""
        self.find_staves(tree)
        
        tempi = node.TempoStaff(self.metric_staff).process()
        events = node.InstrumentStaff(self.instrument_staves).process()
        
        self.process_events(events)
        self.validate_events(events)
        
        return self.normalize_timing(events, tempi)

    def validate_events(self, events):
        """Ensure all events have required parameters"""
        for event_group in events:
            for event in event_group:
                for param in ['name', 'dur', 'dyn', 'env', 'freq']:
                    if not hasattr(event, param) or getattr(event, param) is None:
                        raise ValueError(f'Missing {param} in event: {event.name} at {event.onset}')