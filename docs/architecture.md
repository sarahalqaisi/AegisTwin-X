# Architecture

AegisTwin X separates untrusted hints from trusted evidence.

1. **Promise layer:** human-approved YAML contracts describe product-specific security behavior.
2. **Graph layer:** NetworkX creates a living role → endpoint → resource model.
3. **Diff layer:** candidate relationships are compared with the secure baseline.
4. **Verification layer:** suspected regressions become deterministic role-aware checks.
5. **Shadow Lab:** checks run only against synthetic TwinShop data.
6. **Evidence layer:** expected and observed behavior are recorded without secrets.
7. **Decision layer:** verified severity produces PASS, WARN, or BLOCK.

The current MVP deliberately does not allow an LLM to mark a finding as verified. A future LangGraph adapter may draft policies and explanations, but deterministic verification remains authoritative.

## Trust boundaries

- Browser ↔ AegisTwin API
- Policy files ↔ validation engine
- Candidate metadata ↔ graph builder
- Verification engine ↔ isolated TwinShop lab
- Optional future AI provider ↔ redaction gateway

## Persistence

SQLite stores analysis history for the self-contained portfolio release. PostgreSQL is the intended production adapter. Security Promise Contracts remain version-controlled YAML.

