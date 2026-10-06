from ..models import Telemetry
def parse_line(line,device="stm32"):
    vals={}
    for part in line.strip().split(","):
        if "=" in part:
            k,v=part.split("=",1); vals[k.strip().upper()]=v.strip()
    required=["RPM","CURRENT","TEMP","VIB","PRESSURE"]
    if not all(k in vals for k in required): raise ValueError("Telemetry missing required fields")
    return Telemetry.now(device,float(vals["RPM"]),float(vals["CURRENT"]),float(vals["TEMP"]),float(vals["VIB"]),float(vals["PRESSURE"]),vals.get("STATE","RUNNING"),vals.get("FAULT","NONE"))
class UARTAdapter:
    name="uart"
    def __init__(self, device="stm32", port=None, baud=115200, timeout=2, **_): self.device=device; self.port=port; self.baud=baud; self.timeout=timeout; self.ser=None
    def connect(self):
        if not self.port: raise ValueError("UART target requires --port or target.port")
        import serial
        self.ser=serial.Serial(self.port,self.baud,timeout=self.timeout); return True
    def read(self):
        while True:
            line=self.ser.readline().decode(errors="replace").strip()
            if line: return parse_line(line,self.device)
    def inject(self, values):
        # Optional firmware test hook: INJECT key=value,key=value\n
        payload=",".join(f"{k}={v}" for k,v in values.items())
        self.ser.write(("INJECT "+payload+"\n").encode()); self.ser.flush(); return True
    def close(self):
        if self.ser: self.ser.close()
