from dataclasses import dataclass, asdict
@dataclass
class Diagnostic:
    severity:str; code:str; message:str; recommendation:str
    def to_dict(self): return asdict(self)
def evaluate(t,cfg):
    L=cfg["limits"]; out=[]
    rules=[("temperature_c","PP-TEMP-001","Temperature","C",True,"warning","fault"),("vibration_mm_s","PP-VIB-003","Vibration","mm/s",True,"warning","fault"),("current_a","PP-CUR-002","Current","A",True,"warning","fault"),("pressure_psi","PP-PRS-004","Pressure","psi",False,"warning_low","fault_low")]
    for attr,code,label,unit,high,wk,fk in rules:
        v=getattr(t,attr); w=L[attr][wk]; f=L[attr][fk]; fh=v>=f if high else v<=f; wh=v>=w if high else v<=w
        if fh: out.append(Diagnostic("FAULT",code,f"{label} {v:.2f} {unit} crossed fault limit {f}",f"Inspect {label.lower()} source and isolate equipment if required."))
        elif wh: out.append(Diagnostic("WARNING",code,f"{label} {v:.2f} {unit} crossed warning limit {w}",f"Inspect {label.lower()} trend."))
    if not out: out=[Diagnostic("OK","PP-OK-000","All monitored values are within configured limits.","Continue operation and trending.")]
    return out
def health_score(findings): return max(0,100-sum({"OK":0,"WARNING":18,"FAULT":45}[f.severity] for f in findings))
