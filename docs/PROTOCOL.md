# STM32 UART protocol

PlantPulse expects newline-delimited ASCII telemetry:
`RPM=1740,CURRENT=2.80,TEMP=42.0,VIB=1.70,PRESSURE=62.0,STATE=RUNNING,FAULT=NONE`

For bench-only fault injection the UART adapter sends:
`INJECT current_a=6.2,pressure_psi=20\n`

The controller firmware may implement this command only in a compile-time TEST_MODE. Never expose test injection in production firmware.
