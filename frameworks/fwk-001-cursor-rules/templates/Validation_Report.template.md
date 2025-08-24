| Risk ID | Decision (CONFIRM/CHALLENGE) | Rationale | Evidence Ref (Plan + Codebase) |
|---|---|---|---|
| R-001 | CONFIRM |  | `AP:L<line>` & `CB:/path/to/file.py` |

## 3. Contested Findings
- **R-###** — <Why contested>
  - **Evidence**: `AP:L<line>` & `CB:/path/to/file.py`

## 4. New Risks (NEW-RISK-###)
- **NEW-RISK-001 — <Title>**
  - **Severity**: High | Medium | Low
  - **Rationale**: 
  - **Evidence**: `CB:/path/to/file.py`

## 5. Confirmed Alignments
- **A-001 — <Title of Alignment>**
  - **Decision**: CONFIRM
  - **Rationale**: 
  - **Evidence**: `AP:L<line>` & `CB:/path/to/file.py`

## 6. Verdict & Gating Decision
- [CHOOSE ONE OF THE FOLLOWING VERDICTS AND PROVIDE DETAILS]

- **Verdict Option 1: GO**
  - **Decision**: **GO**. Risk report validated. Proceeding to synthesis.
  - **Rationale**: All identified risks are manageable (Low/Medium severity) and have clear mitigation paths.

- **Verdict Option 2: NO-GO**
  - **Decision**: **NO-GO**. Synthesis halted. Plan requires revision.
  - **Blocking Issues**: 
    - [List all High severity risks or major contests that triggered the halt, with their IDs and titles]