# AgentCompromiseLab: Autonomous LLM Red Team Simulation

## Overview

This project is a **research prototype** demonstrating a **Red Team Framework** for autonomous LLM agents. It simulates a full attack pipeline—from indirect context injection to multi-agent trust exploitation—and provides a testbed for validating defense strategies.

The attack does **not** rely on malware, software vulnerabilities, or direct user prompt manipulation.
Instead, it exploits a common design flaw in modern agent systems: **implicit trust in externally ingested context**.

The framework demonstrates how benign user requests can be weaponized to trigger **unauthorized tool invocations** and **system compromises**.

---

## Problem Statement

Autonomous LLM agents increasingly perform tasks that involve:

* ingesting external content (documents, webpages, API responses),
* reasoning over that content,
* and invoking privileged tools (file access, APIs, network calls).

Most current systems assume that:

* system prompts are authoritative,
* external context is benign,
* and policy definitions alone are sufficient to prevent misuse.

This assumption is incorrect.

An attacker who controls or influences external context can inject hidden instructions that:

* manipulate agent reasoning,
* bypass intended policies,
* and trigger forbidden system actions.

This project proves that risk with a **reproducible attacker PoC**.

---

## Threat Model

**Attacker Capabilities**

* Controls or influences external content consumed by the agent
* Cannot modify agent code or system prompts
* No direct user interaction required

**Attack Vectors Supported**

1.  **Context Injection**: Overriding system instructions via document ingestion.
2.  **Tool Abuse**: Forcing the agent to invoke forbidden APIs (e.g., File I/O).
3.  **Memory Poisoning**: Corrupting the agent's long-term state/session memory.
4.  **Multi-Agent Trust Exploit**: Propagating malicious payloads to peer agents via delegation tools.

---

## Attack Chain Visualization

```mermaid
User Prompt (Benign) --> [Agent Ingestion] --> Context Override (Malicious) --> [LLM Reasoning] --> Tool Invocation (Forbidden) --> System Compromise
```

**Target**

* An autonomous LLM agent with tool invocation privileges

**Attacker goal**

* Trigger a **forbidden tool invocation**
* Cause a **policy violation**
* Achieve a measurable attacker win


---

## Project Structure

```
llm-agent-compromise/
├── agent/                # Autonomous agent logic
├── attacker/             # Malicious external context
├── tools/                # Forbidden tools (simulated)
├── policies/             # Explicit security policy
├── logs/                 # Audit logs
└── README.md
```

---

## Security Policy

The agent operates under an explicit policy that forbids:

* reading sensitive files
* exfiltrating data to external endpoints

These restrictions are defined **before the attack** and enforced via logging, making violations unambiguous.

---

## Demonstrated Impact

* Unauthorized tool invocation
* Explicit security policy violation
* Logged, timestamped audit trail
* No malware or software exploitation required

This moves prompt injection from a **theoretical concern** to a **demonstrable attack class**.

---

## Why This Matters

* Modern AI agents increasingly act with autonomy
* Tool-enabled LLMs blur the line between reasoning and execution
* Trust boundaries between *data* and *instructions* are often undefined

This project shows how that gap can be exploited today.

---

## Scope and Limitations

**In scope**

* Single agent
* Single attack chain
* One forbidden action
* Clear attacker win

**Out of scope**

* Defense or mitigation strategies
* Multi-agent coordination
* Production deployment
* Model fine-tuning

This is an **attack demonstration**, not a defense framework.

---

## Key Takeaway

> Autonomous LLM agents can be compromised through indirect context injection, leading to real system-level policy violations without exploiting code or infrastructure.

---

## Disclaimer

This project is intended for **educational and defensive security research purposes only**.
All sensitive actions are simulated and do not interact with real systems.

---

## Status

✅ Attack successfully demonstrated
✅ Policy violation logged
✅ Reproducible results

---
