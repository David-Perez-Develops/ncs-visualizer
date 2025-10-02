from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EnvelopeFollower:
    attack: float = 0.01
    release: float = 0.1
    value: float = 0.0

    def feed(self, sample: float) -> float:
        if sample > self.value:
            coeff = self.attack
        else:
            coeff = self.release
        self.value += coeff * (sample - self.value)
        return self.value
