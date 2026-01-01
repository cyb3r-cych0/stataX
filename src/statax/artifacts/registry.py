# src/statax/artifacts/registry.py
class ArtifactRegistry:
    def __init__(self):
        self._artifacts = []

    def add(self, artifact):
        self._artifacts.append(artifact)

    def all(self):
        return list(self._artifacts)
