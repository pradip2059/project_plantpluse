from ..models import Telemetry
class ModbusAdapter:
    name="modbus"
    def __init__(self, device="plc", host="127.0.0.1", port=502, unit=1, registers=None, scale=None, **_):
        self.device=device; self.host=host; self.port=port; self.unit=unit; self.reg=registers or {}; self.scale=scale or {}; self.client=None
    def connect(self):
        from pymodbus.client import ModbusTcpClient
        self.client=ModbusTcpClient(self.host,port=self.port); return bool(self.client.connect())
    def _read(self,key):
        addr=self.reg[key]; rr=self.client.read_holding_registers(address=addr,count=1,device_id=self.unit)
        if rr.isError(): raise RuntimeError(f"Modbus read failed for {key}")
        return rr.registers[0]*float(self.scale.get(key,1.0))
    def read(self):
        return Telemetry.now(self.device,self._read("rpm"),self._read("current_a"),self._read("temperature_c"),self._read("vibration_mm_s"),self._read("pressure_psi"))
    def inject(self, values):
        inject_regs=self.reg.get("inject",{})
        for key,val in values.items():
            if key not in inject_regs: raise ValueError(f"No Modbus injection register configured for {key}")
            scale=float(self.scale.get(key,1.0)); self.client.write_register(inject_regs[key],int(float(val)/scale),device_id=self.unit)
        return True
    def close(self):
        if self.client: self.client.close()
