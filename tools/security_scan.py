#!/usr/bin/env python3
from __future__ import annotations
import argparse, os, re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
SUPPORTED_EXTS={".py",".js",".jsx",".ts",".tsx",".go",".php",".html"}
EXCLUDE_DIRS={".git","node_modules",".venv","venv","dist","build",".cursor",".obsidian","VERIFICATION"}
@dataclass
class Finding: severity:str; rule:str; path:str; line:int; context:str
PATTERNS=[
  ("HIGH",r"(exec\(|eval\(|subprocess\.Popen\()", "Dangerous execution (RCE potential)"),
  ("MEDIUM",r"(\bSELECT\b\s+.*\+\s*\w+|f\"SELECT.*\{|format\(.*\bSELECT\b|\%s.*\bSELECT\b)","Possible SQL query string concatenation"),
  ("MEDIUM",r"request\.(args|get|POST)\[.*\]","Direct use of request params without validation"),
  ("MEDIUM",r"innerHTML\s*=","Potential XSS sink via innerHTML assignment"),
  ("LOW",r"AKIA[0-9A-Z]{16}","AWS access key pattern leaked"),
]
def iter_files(root:Path)->Iterable[Path]:
  for dp, dns, fns in os.walk(root):
    dns[:]=[d for d in dns if d not in EXCLUDE_DIRS]
    for n in fns:
      p=Path(dp)/n
      if p.suffix.lower() in SUPPORTED_EXTS and p.stat().st_size<1_500_000: yield p
def scan_file(path:Path)->List[Finding]:
  out:List[Finding]=[]
  try: txt=path.read_text(encoding="utf-8",errors="ignore")
  except Exception: return out
  for sev,pat,rule in PATTERNS:
    rx=re.compile(pat,re.IGNORECASE)
    for i,line in enumerate(txt.splitlines(),start=1):
      if rx.search(line):
        if any(s in line for s in ["os.system('clear'","os.system(\"clear\"", "os.system('cls'","os.system(\"cls\""]): continue
        out.append(Finding(severity=sev,rule=rule,path=str(path),line=i,context=line.strip()[:200]))
  return out
def render(findings:List[Finding])->str:
  high=sum(1 for f in findings if f.severity.upper()=="HIGH")
  med=sum(1 for f in findings if f.severity.upper()=="MEDIUM")
  low=sum(1 for f in findings if f.severity.upper()=="LOW")
  lines=["# Security Report","","## Summary",f"- High: {high}",f"- Medium: {med}",f"- Low: {low}","",
         "## Dependency Audit (stub)","- N/A (lockfile not found or audit tool not integrated in baseline)","",
         "## Findings"]
  if not findings: lines.append("- None")
  else:
    for f in findings[:1000]:
      lines.append(f"- [{f.severity}] {f.rule} — {f.path}:{f.line} — {f.context}")
  lines.append("")
  return "\n".join(lines)
def main()->int:
  ap=argparse.ArgumentParser(description="Baseline security scanner")
  ap.add_argument("--root",default=str(Path.cwd()))
  ap.add_argument("--output",default="security_report.md")
  args=ap.parse_args()
  root=Path(args.root); findings=[]
  for p in iter_files(root): findings.extend(scan_file(p))
  out=Path(args.output); out.write_text(render(findings),encoding="utf-8")
  print(f"✅ Wrote {out}"); return 0
if __name__=="__main__": raise SystemExit(main())
