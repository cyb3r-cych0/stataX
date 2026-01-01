# src/statax/artifacts/base.py
from abc import ABC, abstractmethod

class Artifact(ABC):
    def __init__(self, artifact_id: str, kind: str):
        self.id = artifact_id
        self.kind = kind

    @abstractmethod
    def render(self):
        """Produce a renderable object (table, figure, text)."""
        raise NotImplementedError
