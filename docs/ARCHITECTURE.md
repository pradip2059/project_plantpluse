# Architecture

`cli.py` selects a transport adapter. `TestBench` executes transport-independent YAML cases. Adapters normalize target data into `Telemetry`. `diagnostics.py` applies configured engineering limits. Results are emitted as structured JSON for traceability and CI.

The adapter boundary is intentional: the same acceptance criteria can be exercised first in simulation, then against firmware over UART, then against an industrial Modbus endpoint.
