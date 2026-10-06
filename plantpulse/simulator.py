import random
from .models import Telemetry
SCENARIOS={"normal","bearing-wear","overheat","pressure-loss","overcurrent","sensor-failure"}
class Simulator:
    def __init__(self, device="pump01", scenario="normal"):
        if scenario not in SCENARIOS: raise ValueError(f"Unknown scenario: {scenario}")
        self.device=device; self.scenario=scenario; self.index=0; self.injected={}
    def inject(self, values): self.injected.update(values or {})
    def read(self):
        i=self.index; self.index+=1; r=random.Random(1000+i)
        d=dict(rpm=r.gauss(1740,15), current_a=r.gauss(2.8,.08), temperature_c=r.gauss(42,.7), vibration_mm_s=max(.1,r.gauss(1.7,.15)), pressure_psi=r.gauss(62,1.2), state="RUNNING", fault_code="NONE")
        if self.scenario=="bearing-wear": d["vibration_mm_s"]+=min(6.5,i*.35); d["temperature_c"]+=min(18,i*.5)
        elif self.scenario=="overheat": d["temperature_c"]+=min(45,i*2)
        elif self.scenario=="pressure-loss": d["pressure_psi"]-=min(45,i*2)
        elif self.scenario=="overcurrent": d["current_a"]+=min(4.5,i*.3)
        elif self.scenario=="sensor-failure": d["pressure_psi"] = 0.0
        d.update(self.injected)
        return Telemetry.now(self.device, **d)
