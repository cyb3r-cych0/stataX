# src/statax/artifacts/table.py
from statax.artifacts.base import Artifact

class TableArtifact(Artifact):
    def __init__(self, artifact_id: str, dataframe):
        super().__init__(artifact_id, kind="table")
        self.dataframe = dataframe

    def render(self):
        return self.dataframe
