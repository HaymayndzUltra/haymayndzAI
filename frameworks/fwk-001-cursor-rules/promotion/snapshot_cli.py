#!/usr/bin/env python3
import argparse, hashlib, json, os, sys, glob

ROOT = os.path.dirname(__file__)
INDEX = os.path.abspath(os.path.join(ROOT, "..", "sync", "artifacts_index.json"))
SNAP_DIR = os.path.join(ROOT, "snapshots")

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def create(args):
    os.makedirs(SNAP_DIR, exist_ok=True)
    data = open(INDEX, "rb").read()
    digest = sha256_bytes(data)
    out = os.path.join(SNAP_DIR, f"{digest}.json")
    with open(out, "wb") as f:
        f.write(data)
    print("CREATED:", out)

def verify(args):
    ok = True
    for path in glob.glob(os.path.join(SNAP_DIR, "*.json")):
        b = open(path, "rb").read()
        expect = os.path.splitext(os.path.basename(path))[0]
        got = sha256_bytes(b)
        if got != expect:
            ok = False
            print("BAD:", path)
    print("OK" if ok else "FAIL")
    return 0 if ok else 1

def lst(args):
    for path in sorted(glob.glob(os.path.join(SNAP_DIR, "*.json"))):
        print(path)

def rollback(args):
    target = os.path.join(SNAP_DIR, f"{args.digest}.json")
    if not os.path.exists(target):
        print("Not found:", target)
        return 1
    data = open(target, "rb").read()
    with open(INDEX, "wb") as f:
        f.write(data)
    print("RESTORED index from", target)
    return 0

def prune(args):
    keep = int(args.keep)
    snaps = sorted(glob.glob(os.path.join(SNAP_DIR, "*.json")), key=os.path.getmtime, reverse=True)
    for path in snaps[keep:]:
        os.unlink(path)
        print("DELETED:", path)

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("create").set_defaults(func=create)
    sub.add_parser("verify").set_defaults(func=verify)
    sub.add_parser("list").set_defaults(func=lst)
    rb = sub.add_parser("rollback"); rb.add_argument("digest"); rb.set_defaults(func=rollback)
    pr = sub.add_parser("prune"); pr.add_argument("keep"); pr.set_defaults(func=prune)
    args = ap.parse_args()
    code = args.func(args)
    if code is None: code = 0
    sys.exit(code)

if __name__ == "__main__":
    main()


