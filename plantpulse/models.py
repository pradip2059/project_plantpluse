from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class Telemetry:
    timestamp: str
    device: str
    rpm: float
    current_a: float
    temperature_c: float
    vibration_mm_s: float
    pressure_psi: float
    state: str = "RUNNING"
    fault_code: str = "NONE"
    def to_dict(self): return asdict(self)
    @classmethod
    def now(cls, device, rpm, current_a, temperature_c, vibration_mm_s, pressure_psi, state="RUNNING", fault_code="NONE"):
        return cls(datetime.now(timezone.utc).isoformat(), device, rpm, current_a, temperature_c, vibration_mm_s, pressure_psi, state, fault_code)
