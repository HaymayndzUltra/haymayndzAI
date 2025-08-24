#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any

ROOT = Path('/workspace/frameworks/fwk-001-cursor-rules')
INDEX = ROOT / 'tools' / 'rule_index.json'
BACKLOG = ROOT / 'examples' / 'product_backlog.yaml'

TECH_TOKENS = {
  'django','python','go','golang','react','node','express','postgres','mysql','k8s','kubernetes','terraform','aws','gcp','azure'
}

def load_index() -> List[Dict[str, Any]]:
    return json.loads(INDEX.read_text(encoding='utf-8'))

def parse_backlog(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # requires PyYAML
        data = yaml.safe_load(path.read_text(encoding='utf-8'))
        if isinstance(data, list):
            text = "\n".join([json.dumps(x) for x in data])
        else:
            text = json.dumps(data)
    except Exception:
        # fallback: raw text
        text = path.read_text(encoding='utf-8')
    # infer intent (very naive)
    intent = 'codegen'
    m = re.search(r'(plan|architect|design)', text, re.I)
    if m:
        intent = 'planning'
    m = re.search(r'(test|qa|validate)', text, re.I)
    if m:
        intent = 'qa'
    m = re.search(r'(deploy|mlops|serve|scale)', text, re.I)
    if m:
        intent = 'mlops'
    techs = sorted(list({t for t in TECH_TOKENS if re.search(r'\b'+re.escape(t)+r'\b', text, re.I)}))
    return {'raw': text, 'intent': intent, 'techs': techs}

def score(entry: Dict[str, Any], intent: str, techs: List[str]) -> float:
    s = 0.0
    # intent
    if entry.get('intent') == intent:
        s += 1.0
    elif entry.get('intent') in {'planning','codegen','qa','mlops'}:
        s += 0.3
    # tags overlap
    etags = set(entry.get('tags', []))
    overlap = etags.intersection({t.lower() for t in techs})
    if overlap:
        s += 0.7 * (len(overlap) / max(1, len(etags) or 1))
    # keyword hit
    ekeys = set(entry.get('instructions_keywords', []))
    khit = ekeys.intersection({t.lower() for t in techs})
    if khit:
        s += 0.5 * (len(khit) / max(1, len(ekeys) or 1))
    # guardrails bonus
    if entry.get('guardrails_present'):
        s += 0.1
    return s

def select_rule(index: List[Dict[str, Any]], intent: str, techs: List[str]) -> Dict[str, Any]:
    ranked = sorted(index, key=lambda e: score(e, intent, techs), reverse=True)
    best = ranked[0] if ranked else {}
    best['score'] = score(best, intent, techs) if best else 0.0
    return best

def extract_sections(mdctext: str) -> Dict[str,str]:
    # simple extraction for demo
    parts = {}
    current = None
    lines = mdctext.splitlines()
    for line in lines:
        m = re.match(r'^\[([A-Za-z_]+)\]\s*$', line.strip())
        if m:
            current = m.group(1).upper()
            parts[current] = []
        elif current:
            parts[current].append(line)
    return {k: "\n".join(v).strip() for k,v in parts.items()}

def build_persona_payload(rule_path: str, agent: str, intent: str) -> Dict[str, Any]:
    p = Path(rule_path)
    text = p.read_text(encoding='utf-8', errors='ignore')
    secs = extract_sections(text)
    return {
        'agent': agent,
        'intent': intent,
        'instructions': secs.get('INSTRUCTIONS',''),
        'guardrails': secs.get('GUARDRAILS',''),
        'tags': [],
        'hash': '',
        'source_rule': rule_path
    }

def main(argv: List[str]) -> int:
    agent = argv[1] if len(argv) > 1 else 'codegen_ai'
    backlog = parse_backlog(BACKLOG) if BACKLOG.exists() else {'raw':'','intent':'codegen','techs':[]}
    index = load_index()
    best = select_rule(index, backlog['intent'], backlog['techs'])
    persona = build_persona_payload(best.get('path',''), agent, backlog['intent']) if best else {}
    out_path = ROOT / 'tools' / 'persona_payload.json'
    out_path.write_text(json.dumps({'task': backlog, 'selection': best, 'persona': persona}, indent=2), encoding='utf-8')
    print(f"Wrote persona payload: {out_path}")
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))