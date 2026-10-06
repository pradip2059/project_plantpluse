# PlantPulse TestBench

A hardware-agnostic commissioning and automated validation CLI for embedded and industrial control systems. One YAML test plan can target a deterministic simulator, an STM32 over UART, or a PLC/device over Modbus TCP.

## Why this project
Commissioning often involves manually watching telemetry, forcing abnormal conditions, and recording PASS/FAIL results. PlantPulse turns those steps into repeatable test plans with fault injection, timing constraints, diagnostics, and JSON reports.

> **Project status:** The simulator/TestBench path is implemented and software-tested. UART and Modbus adapters are included for integration, but physical STM32/PLC validation must be performed on the target hardware before claiming hardware validation.

## Features
- YAML-defined commissioning tests
- Simulator, UART, and Modbus TCP adapters
- Fault injection hooks
- Threshold diagnostics and fault codes
- Timing-constrained expectations
- JSON test evidence
- GitHub Actions CI
- Example STM32 telemetry protocol/firmware integration guide

## Clone and run
```bash
git clone <YOUR_REPOSITORY_URL>
cd PlantPulse
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .[dev]
pytest -q
plantpulse validate --plan testplans/commissioning.yaml --target simulator
```

## Live monitoring
```bash
plantpulse monitor --target simulator --samples 5
plantpulse monitor --target uart --port COM3 --samples 20
plantpulse monitor --target modbus --host 192.168.1.50 --samples 20
```

## Test-plan example
```yaml
- name: Overcurrent protection
  inject: {current_a: 6.2}
  expect: {fault: PP-CUR-002}
  within_ms: 500
```

## Architecture
```text
YAML Test Plan
      |
      v
 PlantPulse TestBench
      |
  +---+----------------+
  |        |           |
Simulator UART       Modbus TCP
           |           |
         STM32       PLC/device
      |
      v
Diagnostics -> PASS/FAIL -> JSON evidence
```

## Safety
PlantPulse is an educational/engineering validation project, not a certified safety system. Do not use software fault injection on live machinery unless the test setup is isolated and appropriate safeguards are in place.

## License
MIT
