import operator,time,json
from dataclasses import dataclass,asdict
from pathlib import Path
from .diagnostics import evaluate
OPS={"eq":operator.eq,"ne":operator.ne,"gt":operator.gt,"gte":operator.ge,"lt":operator.lt,"lte":operator.le}
ALIASES={"temperature":"temperature_c","temp":"temperature_c","current":"current_a","vibration":"vibration_mm_s","pressure":"pressure_psi"}
@dataclass
class CheckResult:
    name:str; passed:bool; detail:str; latency_ms:float=0.0
@dataclass
class CaseResult:
    name:str; passed:bool; checks:list; sample:dict
class TestBench:
    def __init__(self,adapter,cfg): self.adapter=adapter; self.cfg=cfg
    def _check(self,sample,expect,findings):
        out=[]; codes={f.code for f in findings}; severities={f.severity for f in findings}
        for raw,rule in expect.items():
            key=ALIASES.get(raw,raw)
            if key=="fault": ok=str(rule) in codes or sample.fault_code==str(rule); detail=f"fault={rule}; observed={sorted(codes)} controller={sample.fault_code}"
            elif key=="severity": ok=str(rule) in severities; detail=f"severity={rule}; observed={sorted(severities)}"
            elif key=="state": ok=sample.state==str(rule); detail=f"state expected={rule}, actual={sample.state}"
            else:
                val=getattr(sample,key)
                if isinstance(rule,dict):
                    opname,nextval=next(iter(rule.items())); ok=OPS[opname](val,float(nextval)); detail=f"{key} {val:.3f} {opname} {nextval}"
                elif isinstance(rule,list) and len(rule)==2: ok=float(rule[0])<=val<=float(rule[1]); detail=f"{key}={val:.3f} in [{rule[0]}, {rule[1]}]"
                else: ok=val==rule; detail=f"{key} expected={rule}, actual={val}"
            out.append(CheckResult(raw,bool(ok),detail))
        return out
    def run_case(self,case):
        if case.get("inject"): self.adapter.inject(case["inject"])
        settle=float(case.get("settle_ms",0))/1000; time.sleep(settle)
        deadline=float(case.get("within_ms",1000)); start=time.perf_counter(); sample=None; checks=[]
        while (time.perf_counter()-start)*1000 <= deadline:
            sample=self.adapter.read(); findings=evaluate(sample,self.cfg); checks=self._check(sample,case.get("expect",{}),findings)
            if all(c.passed for c in checks): break
            time.sleep(.02)
        latency=(time.perf_counter()-start)*1000
        for c in checks: c.latency_ms=latency
        return CaseResult(case["name"],all(c.passed for c in checks),[asdict(c) for c in checks],sample.to_dict())
    def run(self,plan):
        self.adapter.connect(); results=[]
        try:
            for case in plan["tests"]: results.append(self.run_case(case))
        finally: self.adapter.close()
        return results
def write_report(results,path,target):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); payload={"target":target,"passed":all(r.passed for r in results),"summary":{"passed":sum(r.passed for r in results),"total":len(results)},"tests":[asdict(r) for r in results]}; p.write_text(json.dumps(payload,indent=2)); return p
