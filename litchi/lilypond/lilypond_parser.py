# litchi/lilypond/parser.py
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import quickly
from quickly.dom import lily
from quickly.dom.scope import Scope

@dataclass
class LilyPondFile:
    """Represents a loaded LilyPond file with its DOM tree"""
    path: Path
    tree: lily.Node
    language: str = 'english'

    @classmethod
    def load(cls, file_path: Path, log_path: Path = None) -> 'LilyPondFile':
        """Factory method to load and preprocess a LilyPond file"""
        d = quickly.load(str(file_path))
        tree = d.get_transform(True)
        
        if log_path:
            with open(log_path, 'w') as f:
                tree.dump(file=f)
        
        cls._resolve_includes(d, tree)
        return cls(path=file_path, tree=tree)

    @staticmethod
    def _resolve_includes(d, tree):
        """Replace include references in the tree"""
        scope = Scope(d)
        for identifier in tree // lily.IdentifierRef:
            identifier.replace_with(identifier.get_value(scope))
