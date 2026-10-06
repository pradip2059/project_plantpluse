from pathlib import Path
import time, typer, yaml
from rich.console import Console
from rich.table import Table
from .config import load_yaml
from .simulator import SCENARIOS
from .adapters.sim import SimulatorAdapter
from .adapters.uart import UARTAdapter
from .adapters.modbus import ModbusAdapter
from .diagnostics import evaluate,health_score
from .testbench import TestBench,write_report
app=typer.Typer(help="PlantPulse TestBench: hardware-agnostic commissioning and validation CLI."); console=Console()
def adapter_for(target,cfg,scenario="normal",port=None,host=None):
    device=cfg.get("device","pump01")
    if target=="simulator": return SimulatorAdapter(device=device,scenario=scenario)
    if target=="uart": return UARTAdapter(device=device,port=port or cfg.get("uart",{}).get("port"),baud=cfg.get("uart",{}).get("baud",115200))
    if target=="modbus":
        m=cfg.get("modbus",{}).copy(); m["host"]=host or m.get("host","127.0.0.1"); return ModbusAdapter(device=device,**m)
    raise typer.BadParameter("target must be simulator, uart, or modbus")
def show(s,cfg):
    f=evaluate(s,cfg); t=Table(title=f"PlantPulse | {s.device}"); t.add_column("Signal");t.add_column("Reading",justify="right")
    for k,v in [("RPM",f"{s.rpm:.0f}"),("Current",f"{s.current_a:.2f} A"),("Temperature",f"{s.temperature_c:.1f} C"),("Vibration",f"{s.vibration_mm_s:.2f} mm/s"),("Pressure",f"{s.pressure_psi:.1f} psi")]:t.add_row(k,v)
    console.print(t); console.print(f"Health: [bold]{health_score(f)}%[/bold]"); [console.print(f"{x.severity:7} {x.code} {x.message}") for x in f]
@app.command()
def simulate(scenario:str="normal",samples:int=8,config:str=None):
    if scenario not in SCENARIOS: raise typer.BadParameter(f"Choose: {', '.join(sorted(SCENARIOS))}")
    cfg=load_yaml(config); a=SimulatorAdapter(device=cfg["device"],scenario=scenario); a.connect()
    for _ in range(samples): show(a.read(),cfg)
@app.command()
def monitor(target:str=typer.Option("simulator"),scenario:str="normal",config:str=None,port:str=None,host:str=None,samples:int=0):
    cfg=load_yaml(config); a=adapter_for(target,cfg,scenario,port,host); a.connect(); n=0
    try:
        while samples<=0 or n<samples: show(a.read(),cfg); n+=1; time.sleep(.25)
    finally:a.close()
@app.command()
def validate(plan:str="testplans/commissioning.yaml",target:str=typer.Option("simulator"),scenario:str="normal",config:str=None,port:str=None,host:str=None,report:str="reports/latest.json"):
    cfg=load_yaml(config); p=load_yaml(plan); a=adapter_for(target,cfg,scenario,port,host); results=TestBench(a,cfg).run(p)
    table=Table(title=f"PlantPulse Validation | {target}"); table.add_column("Test");table.add_column("Result");table.add_column("Checks")
    for r in results: table.add_row(r.name,"PASS" if r.passed else "FAIL","; ".join(c["detail"] for c in r.checks))
    console.print(table); out=write_report(results,report,target); passed=sum(r.passed for r in results); console.print(f"{passed}/{len(results)} passed | report: {out}")
    if passed!=len(results): raise typer.Exit(1)
if __name__=="__main__": app()
