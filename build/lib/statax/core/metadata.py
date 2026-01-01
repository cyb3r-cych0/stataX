import platform
import sys
from datetime import datetime
from dataclasses import asdict, is_dataclass

def _to_serializable(obj):
    if is_dataclass(obj):
        return asdict(obj)
    return obj

def build_metadata(config):
    return {
        "timestamp": datetime.now().isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "config": _to_serializable(config),
    }
