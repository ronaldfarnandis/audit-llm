# AuditLLM 🛡️

An offline reliability and testing harness designed to audit downstream LLM outputs and AI agents for structural compliance, performance SLAs, and semantic hallucination rates.

## Why AuditLLM?
Most AI engineering focuses on generation (wrappers, chat UIs). **AuditLLM** focuses on **testing and reliability infrastructure**—acting as a CI/CD quality gate to catch silent regressions, invalid JSON schemas, and ungrounded hallucinations before code reaches production.

## Architecture
AuditLLM uses a dual-layer evaluation pipeline:
1. **Deterministic Gatekeeper:** Fast, local code-based checks using Pydantic v2 schemas and latency SLA boundaries. If an agent breaks its JSON contract, the engine short-circuits to save resources.
2. **Semantic Judge Layer:** Evaluates agent claims against source contexts to detect hallucinations and consistency failures.
3. **Report Exporter:** Automatically generates clean, minimalist Markdown execution reports for PR/CI integration.

## Project Structure
```text
audit-llm/
│
├── core/
│   ├── checker.py      # Structural & latency validation
│   ├── runner.py       # Orchestration & test pipeline
│   └── reporter.py     # Minimalist Markdown report generator
│
├── judges/
│   └── llm_judge.py    # Semantic heuristic hallucination checks
│
├── examples/
│   └── target_agent.py # Mock buggy target agent for test simulations
│
├── reports/            # Generated audit execution logs
├── main.py             # CLI entrypoint
└── requirements.txt
