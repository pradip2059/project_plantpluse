from ..simulator import Simulator
class SimulatorAdapter:
    name="simulator"
    def __init__(self, device="pump01", scenario="normal", **_): self.sim=Simulator(device,scenario)
    def connect(self): return True
    def read(self): return self.sim.read()
    def inject(self, values): self.sim.inject(values); return True
    def close(self): pass
