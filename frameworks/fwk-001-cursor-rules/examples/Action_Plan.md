1) Prerequisites and update main
git checkout main
git pull --ff-only origin main
2) Baseline checks (Progressive OFF, sidecars)
grep -n "progressive_mode" frameworks/fwk-001-cursor-rules/DOCS/changes/routing_override.yaml || true
python3 scripts/validate_sidecars.py | sed -n '1,160p' || true
3) Intelligent selection (dry-run) using your brief
python3 scripts/advanced_rule_integrator.py \
  --text "AI-Driven Memory Bridge with Multi-Agent Orchestration: Knowledge/Memory Bridge (JSON+SQLite) 100k+ tokens; rules-based .mdc routing; constraint-aware deny; cross-machine Docker+Redis/ZMQ (MainPC RTX4090 + PC2 mid-GPU); hybrid inference (local GPU primary, fallback cloud if quality<0.85); auto-recovery; 50+ concurrent tasks; <2m recovery; 100% audit trail." \
  --max-select 12 --risk-budget 6.0 | sed -n '1,200p'
4) Inspect selection artifacts
SELDIR=$(ls -dt frameworks/fwk-001-cursor-rules/DOCS/harvested/selection_* | head -1); echo "$SELDIR"
sed -n '1,200p' "$SELDIR/selection.json"
sed -n '1,160p' "$SELDIR/composite_rule.mdc"
5) Apply integration safely (Progressive OFF + one-shot monitors + append report)
python3 scripts/advanced_rule_integrator.py \
  --text "AI-Driven Memory Bridge with Multi-Agent Orchestration: Knowledge/Memory Bridge (JSON+SQLite) 100k+ tokens; rules-based .mdc routing; constraint-aware deny; cross-machine Docker+Redis/ZMQ (MainPC RTX4090 + PC2 mid-GPU); hybrid inference (local GPU primary, fallback cloud if quality<0.85); auto-recovery; 50+ concurrent tasks; <2m recovery; 100% audit trail." \
  --max-select 12 --risk-budget 6.0 \
  --apply --progressive off --run-monitors --repeat 1 --interval 1 --append-report | sed -n '1,200p'
6) Verify backup, report, and drift (WARN due to Progressive=OFF is OK; ensure drift=0)
ls -t frameworks/fwk-001-cursor-rules/DOCS/changes/routing_override.yaml.bak.*
sed -n '1,200p' frameworks/fwk-001-cursor-rules/DOCS/reports/Latest_Current.md | sed -n '1,200p'
TRIGGERS="/route /status /health /observe /alert /benchmark /analyze /review /validate_docs"
BASE="frameworks/fwk-001-cursor-rules/DOCS/reports/progressive_observability"
for t in $TRIGGERS; do
  f="$BASE/${t#/}/monitoring_dashboard.json"
  if [ -f "$f" ]; then
    python3 - "$f" "$t" <<'PY'
import json,sys; j=json.load(open(sys.argv[1])); t=sys.argv[2]
print(f"{t}: {j.get('status') or j.get('overall_status') or 'UNKNOWN'} (drift={j.get('drift') or j.get('drift_score') or 0})")
PY
  fi
done
7) Phase 1: Minimal Memory Bridge (JSON + SQLite) + audit (save as memory_bridge.py)
import sqlite3, json, time, os, argparse, uuid

DB = os.environ.get("MEMORY_DB", "memory.db")

def init():
    c = sqlite3.connect(DB); cur = c.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS memory(id TEXT PRIMARY KEY, ts REAL, session TEXT, key TEXT, value TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS audit(id TEXT PRIMARY KEY, ts REAL, actor TEXT, action TEXT, payload TEXT)")
    c.commit(); c.close()

def log(actor, action, payload):
    c = sqlite3.connect(DB); cur = c.cursor()
    cur.execute("INSERT INTO audit VALUES(?,?,?,?,?)", (str(uuid.uuid4()), time.time(), actor, action, json.dumps(payload)[:200000]))
    c.commit(); c.close()

def put(session, key, value):
    c = sqlite3.connect(DB); cur = c.cursor()
    cur.execute("INSERT OR REPLACE INTO memory VALUES(?,?,?,?,?)", (f"{session}:{key}", time.time(), session, key, json.dumps(value)[:200000]))
    c.commit(); c.close()

def get(session, key):
    c = sqlite3.connect(DB); cur = c.cursor()
    cur.execute("SELECT value FROM memory WHERE id=?", (f"{session}:{key}",))
    row = cur.fetchone(); c.close()
    return json.loads(row[0]) if row else None

def history(limit=1000):
    c = sqlite3.connect(DB); cur = c.cursor()
    cur.execute("SELECT ts,actor,action,payload FROM audit ORDER BY ts DESC LIMIT ?", (limit,))
    rows = [{"ts": ts, "actor": actor, "action": action, "payload": json.loads(payload)} for ts,actor,action,payload in cur.fetchall()]
    c.close(); return rows

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("init")
    p2 = sub.add_parser("put"); p2.add_argument("--session"); p2.add_argument("--key"); p2.add_argument("--value")
    p3 = sub.add_parser("get"); p3.add_argument("--session"); p3.add_argument("--key")
    p4 = sub.add_parser("log"); p4.add_argument("--actor"); p4.add_argument("--action"); p4.add_argument("--payload")
    p5 = sub.add_parser("history"); p5.add_argument("--limit", type=int, default=100)
    args = ap.parse_args(); init()
    if args.cmd == "put":
        val = json.loads(args.value); put(args.session, args.key, val); log("memory_bridge", "put", {"session": args.session, "key": args.key})
    elif args.cmd == "get":
        out = get(args.session, args.key); print(json.dumps(out, indent=2)); log("memory_bridge", "get", {"session": args.session, "key": args.key, "hit": out is not None})
    elif args.cmd == "log":
        log(args.actor, args.action, json.loads(args.payload))
    elif args.cmd == "history":
        print(json.dumps(history(args.limit), indent=2))
8) Phase 1 quick test (Memory Bridge)
python3 memory_bridge.py init
python3 memory_bridge.py put --session S1 --key plan --value '{"steps":["ingest","route","execute"]}'
python3 memory_bridge.py get --session S1 --key plan | sed -n '1,80p'
python3 memory_bridge.py log --actor orchestrator --action route --payload '{"trigger":"/plan","target":"planning_ai"}'
python3 memory_bridge.py history --limit 10 | sed -n '1,160p'
9) Phase 2: Simulate rule-driven routing audit
python3 memory_bridge.py log --actor execution_orchestrator --action "route" \
  --payload '{"trigger":"/plan","route_to":"planning_ai","session":"S1"}'
10) Phase 3: Minimal Docker Compose (save as docker-compose.yml)
version: "3.9"
services:
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
    healthcheck:
      test: ["CMD","redis-cli","ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  orchestrator:
    build: .
    command: python3 orchestrator.py
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      redis:
        condition: service_healthy
    restart: always
    healthcheck:
      test: ["CMD","python3","-c","import socket;s=socket.socket();s.settimeout(2);s.connect(('localhost',8080));print('ok')"]
      interval: 10s
      timeout: 3s
      retries: 5

  worker:
    build: .
    command: python3 worker.py
    environment:
      - REDIS_URL=redis://redis:6379/0
      - QUALITY_FALLBACK=0.85
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: ["gpu"]
    restart: always
11) Phase 3 bring-up (single machine; Redis + services)
docker compose up -d
docker compose ps
12) Cross-machine setup
# On MainPC (Redis host): ensure 6379/tcp open (firewall)
# On PC2 (worker): point to MainPC IP
export REDIS_URL="redis://MAIN_PC_IP:6379/0"
docker compose up -d worker
13) Hybrid inference quality fallback (pseudo-logic to use in worker)
# inside worker.py
quality = score(output)  # float 0..1
if quality < 0.85:
    output = call_cloud_llm(prompt, model="gpt-4o-mini", temperature=0.2)
14) Concurrency and resilience checks
# scale workers to reach 50+ concurrent tasks (example if implemented)
# docker compose up -d --scale worker=4
# simulate failure
docker compose restart worker
# verify orchestrator requeues tasks and recovery < 2 minutes
15) Observability quick sweep (drift; expect WARN on Progressive=OFF)
for t in /route /status /health /observe /alert /benchmark /analyze /review /validate_docs; do
  python3 scripts/progressive_monitor.py --trigger $t --repeat 1 --interval 1 | sed -n '1,80p'
done
16) Rollback (restore last known-good routing_override.yaml)
ls -t frameworks/fwk-001-cursor-rules/DOCS/changes/routing_override.yaml.bak.* | head -1 | \
  xargs -I{} cp {} frameworks/fwk-001-cursor-rules/DOCS/changes/routing_override.yaml
17) Git hygiene (feature branch and PR; Progressive OFF in PR)
git checkout -b chore/project-memory-bridge
git add -A
git commit -m "AI Memory Bridge: selection + integration (Progressive=OFF)"
git push -u origin chore/project-memory-bridge
# Open PR on GitHub; keep Progressive=OFF