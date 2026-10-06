from plantpulse.simulator import Simulator
from plantpulse.diagnostics import evaluate
from plantpulse.adapters.uart import parse_line
from plantpulse.testbench import TestBench
import yaml
CFG=yaml.safe_load(open("configs/pump01.yaml"))
def test_normal_ok(): assert evaluate(Simulator().read(),CFG)[0].severity=="OK"
def test_uart_parser(): assert parse_line("RPM=1700,CURRENT=2.5,TEMP=40,VIB=1.2,PRESSURE=60").rpm==1700
def test_fault_injection():
    from plantpulse.adapters.sim import SimulatorAdapter
    a=SimulatorAdapter(); plan={"tests":[{"name":"oc","inject":{"current_a":6.2},"expect":{"fault":"PP-CUR-002"},"within_ms":100}]}
    assert TestBench(a,CFG).run(plan)[0].passed
