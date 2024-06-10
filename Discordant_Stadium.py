from dataclasses import dataclass, field
from typing import Any

@dataclass
class Stadium:
    name: str = field(default='Habitat')
    effects: Any = field(default=None)
    resonance1: Any = field(default=0)
    resonance2: Any = field(default=0)

