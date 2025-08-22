## Proposal A: Deprecate Legacy Rules and Fully Adopt the Framework

- **Pros**
  - **Single source of truth**: Policy, states, and gates governed by `frameworks/fwk-001-cursor-rules`.
  - **Zero policy drift**: Docs and runtime align to BLOCK semantics.
  - **Auditable and predictable**: Deterministic gate behavior; easier CI governance.
  - **Lower long-term cost**: One ruleset to maintain; simpler test matrix.

- **Cons**
  - **Short-term disruption**: Existing workflows relying on advisory behavior will break.
  - **Learning curve**: Contributors must adapt to framework phases, transitions, and stricter gates.
  - **Temporary velocity hit**: More upfront analysis to pass gates.

- **High-Level Migration Steps**
  1. Archive legacy rules
     - Move `/.cursor/rules` to `/legacy/.cursor-rules-archived` and leave a `README.md` with pointers to `frameworks/fwk-001-cursor-rules`.
  2. Make framework the canonical policy
     - Set default enforcement to strict (team) everywhere; codify in shell profiles and CI.
     - Remove optional language from any remaining user-facing docs.
  3. Add compatibility guardrails
     - Detect legacy rule usage and emit a clear deprecation error with pointers.
  4. Update CLI and docs
     - Ensure `todo_manager.py` help, logs, and error messages reference framework concepts (Decision Gate, IMPORTANT NOTE).
     - Publish the canonical workflow and examples.
  5. Enforce in CI
     - Block if `AI_ENFORCEMENT_MODE` is not `team` in CI.
     - Add checks for missing Decision Gate/IMPORTANT NOTE in analysis phases.

- **Executable snippets**
  - Enforce strict mode globally (shell/CI):
    export AI_ENFORCEMENT_MODE=team

  - CI guard (bash):
    if [ "${CI:-}" = "true" ] && [ "${AI_ENFORCEMENT_MODE:-team}" != "team" ]; then
      echo "CI must run with AI_ENFORCEMENT_MODE=team (strict)."
      exit 1
    fi

## Proposal B: Integrate Legacy Rules with the New Framework

- **Pros**
  - **Lower disruption**: Gradual transition preserves developer habits.
  - **Mode flexibility**: Advisory for exploration; strict for integration/CI.
  - **Parallel adoption**: Teams can onboard to framework incrementally.

- **Cons**
  - **Increased complexity**: Two layers (legacy + framework) to keep consistent.
  - **Persistent debt risk**: Dual semantics can linger and regrow drift.
  - **Higher maintenance**: Additional tooling to synchronize docs and runtime.

- **High-Level Integration Strategy**
  1. Make `.cursor/rules` a user-facing adapter
     - Update legacy docs to describe two modes explicitly: Advisory vs Strict.
     - Replace “optional” wording with “mode-dependent,” pointing to framework policies.
  2. Centralize policy resolution in code
     - Create a single shared policy module used by `todo_manager.py` and any analyzers. It normalizes env mode, logs consistent messages, and decides WARN vs BLOCK.

      (python)
      # policy/gate_policy.py
      import os
      from enum import Enum

      class Enforcement(Enum):
          BLOCK = "block"
          WARN = "warn"

      def current_enforcement() -> Enforcement:
          mode = os.getenv("AI_ENFORCEMENT_MODE", "team").strip().lower()
          return Enforcement.WARN if mode in {"solo", "optional", "warn", "advisory"} else Enforcement.BLOCK

      def should_block() -> bool:
          return current_enforcement() is Enforcement.BLOCK

      def describe_mode() -> str:
          return f"Deep Analysis Gate enforcement: {current_enforcement().value.upper()} (AI_ENFORCEMENT_MODE={os.getenv('AI_ENFORCEMENT_MODE','team')})"

  3. Unify messages across tools
     - Use `describe_mode()` in CLI outputs so logs always reflect the active policy.
  4. Doc-sync pipeline
     - Introduce a lightweight build step that regenerates `/.cursor/rules/*.mdc` snippets from `frameworks/fwk-001-cursor-rules` (or includes canonical excerpts) to prevent drift.
  5. Master toggle and governance
     - Adopt `frameworks/fwk-001-cursor-rules/system-prompt/rules_master_toggle.mdc` as the control surface. Document `AI_ENFORCEMENT_MODE` clearly:
       - Advisory (WARN): local exploration.
       - Strict (BLOCK): CI, protected branches, release flows.
  6. CI policy
     - CI enforces strict mode and verifies the doc-sync step (diff fails if legacy and framework diverge).
  7. Sunset plan
     - Define a timebox (e.g., 4–8 weeks) after which legacy adapters are removed once usage drops below threshold.

- **Executable snippets**
  - Local advisory toggle:
    export AI_ENFORCEMENT_MODE=solo

  - CI strict guard and doc-sync check:
    export AI_ENFORCEMENT_MODE=team
    git diff --exit-code frameworks/fwk-001-cursor-rules .cursor/rules || { echo "Doc drift detected"; exit 1; }

## Final Recommendation

- **Recommend Proposal A (Deprecate and Replace)** with a short, time-boxed compatibility window. It eliminates long-term policy drift, simplifies governance, and aligns docs with runtime. If immediate disruption is a concern, briefly apply elements of Proposal B (centralized policy module and CI guards) strictly as a transition layer, then fully remove legacy rules on a fixed date.
