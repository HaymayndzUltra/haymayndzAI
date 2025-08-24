# Performance Measurement Methodology

## Scope
- Applies to schema validation (synthetic vs real), routing, hydration, and pipeline steps.

## Hardware Profile
- CPU: 4 vCPU minimum
- RAM: 8 GB minimum
- Storage: SSD
- OS: Linux kernel >= 6.x

## Sampling & Statistics
- Warmup: 3 runs (discarded)
- Measurement runs: N = 30
- Report: mean, median, p95, stddev
- Confidence: 95% CI on mean

## Thresholds
- Synthetic validators: mean < 2 ms, p95 < 5 ms
- Real validators (repo I/O): mean < 5 ms, p95 < 15 ms
- Noise budget: +/-15% on shared CI runners

## Procedure
1) Pin toolchain versions (see `constraints/toolchain.json`).
2) Run on isolated runner; disable turbo/boost if possible.
3) Use time.monotonic_ns; aggregate in CSV/JSON.
4) Fail if p95 exceeds thresholds beyond noise budget.

## Reporting
- Emit JSON with fields: { "mean_ms", "p95_ms", "stddev_ms", "n" }.
- Attach environment metadata: { cpu, ram, os, python, node }.

## Reproducibility
- Same commit, same constraints; require 3 consecutive green runs.

