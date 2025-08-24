#!/usr/bin/env python3
import argparse, os, sys, json, time, hashlib
from pathlib import Path
import orjson
import yaml

try:
    import faiss                   # type: ignore
except Exception as e:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except Exception as e:
    SentenceTransformer = None

CONFIG_PATH = Path(__file__).with_name("pro_config.yaml")


def load_cfg():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    # Portability override
    root_override = os.getenv("MEMORY_STORAGE_ROOT")
    if root_override:
        cfg.setdefault("storage", {})["root"] = str(Path(root_override).resolve())
    return cfg


def ensure_dirs(root: Path):
    root.mkdir(parents=True, exist_ok=True)


def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def entry_id(text: str) -> str:
    # Non-security identifier; use SHA-256 for modern hashing
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:10]
    return f"kb_{time.strftime('%Y%m%d_%H%M%S')}_{h}"


def load_model(cfg):
    device_pref = cfg.get("device", "auto")
    device = "cpu"
    if device_pref == "auto":
        device = "cuda" if os.environ.get("CUDA_VISIBLE_DEVICES", "") != "" else ("cuda" if faiss and faiss.get_num_gpus() > 0 else "cpu")
    elif device_pref in ("cuda", "cpu"):
        device = device_pref
    if SentenceTransformer is None:
        raise SystemExit("sentence-transformers not installed")
    model_name = cfg["embedding"]["model"]
    model = SentenceTransformer(model_name, device=device)
    return model, device


def ltm_paths(cfg):
    root = Path(cfg["storage"]["root"]).resolve()
    ensure_dirs(root)
    return {
        "ltm": root / cfg["storage"]["ltm_file"],
        "decisions": root / cfg["storage"]["decision_log"],
        "snapshot": root / cfg["storage"]["snapshot_file"],
        "index": root / cfg["storage"]["index_file"],
        "meta": root / cfg["storage"]["meta_file"],
    }


def append_jsonl(path: Path, obj: dict):
    with open(path, "ab") as f:
        f.write(orjson.dumps(obj) + b"\n")


def cmd_save(args):
    cfg = load_cfg()
    p = ltm_paths(cfg)
    text = args.text.strip()
    if not text:
        print("Nothing to save.")
        return
    obj = {
        "id": entry_id(text),
        "type": args.type,
        "text": text,
        "tags": args.tags or [],
        "confidence": args.confidence,
        "source": args.source,
        "ts": now_ts(),
    }
    append_jsonl(p["ltm"], obj)
    print(obj["id"])


def build_or_load_index(cfg, p, model):
    dim = cfg["embedding"]["dim"]
    flat_threshold = int(cfg["index"].get("flatip_threshold", 200000))
    if faiss is None:
        raise SystemExit("faiss not available")
    idx_path = p["index"]
    meta_path = p["meta"]
    if idx_path.exists() and meta_path.exists():
        idx = faiss.read_index(str(idx_path))
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return idx, meta
    # create empty flat index
    idx = faiss.IndexFlatIP(dim)
    meta = {"type": "flatip", "dim": dim, "ids": []}
    return idx, meta


def embed_batch(model, texts):
    return model.encode(texts, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)


def iter_jsonl(path: Path):
    if not path.exists():
        return []
    with open(path, "rb") as f:
        for line in f:
            if not line.strip():
                continue
            yield orjson.loads(line)


def cmd_reindex(args):
    cfg = load_cfg()
    p = ltm_paths(cfg)
    model, device = load_model(cfg)
    entries = list(iter_jsonl(p["ltm"]))
    texts = [e.get("text", "") for e in entries]
    if not texts:
        print("No entries to index.")
        return
    embs = embed_batch(model, texts)
    dim = embs.shape[1]
    if faiss is None:
        raise SystemExit("faiss not available")
    idx = faiss.IndexFlatIP(dim)
    idx.add(embs)
    faiss.write_index(idx, str(p["index"]))
    with open(p["meta"], "w", encoding="utf-8") as f:
        json.dump({"type": "flatip", "dim": dim, "ids": [e["id"] for e in entries]}, f)
    print(f"Indexed {len(entries)} entries → {p['index']}")


def cmd_recall(args):
    cfg = load_cfg()
    p = ltm_paths(cfg)
    query = args.query.strip()
    if not query:
        print("Empty query.")
        return
    semantic_ready = (
        faiss is not None and p["index"].exists() and p["meta"].exists() and SentenceTransformer is not None
    )
    if not semantic_ready:
        # fallback: naive tag/substring search
        hits = []
        for e in iter_jsonl(p["ltm"]):
            if query.lower() in e.get("text", "").lower() or any(query.lower() in t.lower() for t in e.get("tags", [])):
                hits.append(e)
        for e in hits[: args.topk]:
            print(orjson.dumps(e).decode())
        return
    # semantic path (load model only when needed)
    model, device = load_model(cfg)
    qv = embed_batch(model, [query])
    idx = faiss.read_index(str(p["index"]))
    with open(p["meta"], "r", encoding="utf-8") as f:
        meta = json.load(f)
    D, I = idx.search(qv, args.topk)
    ids = [meta["ids"][i] for i in I[0] if i >= 0]
    idset = set(ids)
    for e in iter_jsonl(p["ltm"]):
        if e["id"] in idset:
            print(orjson.dumps(e).decode())


def cmd_snapshot(args):
    cfg = load_cfg()
    p = ltm_paths(cfg)
    snap = {
        "ts": now_ts(),
        "summary": args.summary or "",
        "open_questions": args.open or [],
        "next_steps": args.next or [],
        "tags": args.tags or [],
    }
    with open(p["snapshot"], "w", encoding="utf-8") as f:
        yaml.safe_dump(snap, f, sort_keys=False)
    print(f"Snapshot written → {p['snapshot']}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("save")
    sp.add_argument("text", type=str)
    sp.add_argument("--type", default="fact")
    sp.add_argument("--tags", nargs="*", default=[])
    sp.add_argument("--confidence", type=float, default=0.9)
    sp.add_argument("--source", default="user")
    sp.set_defaults(func=cmd_save)

    rp = sub.add_parser("recall")
    rp.add_argument("query", type=str)
    rp.add_argument("--topk", type=int, default=5)
    rp.set_defaults(func=cmd_recall)

    ip = sub.add_parser("reindex")
    ip.set_defaults(func=cmd_reindex)

    sn = sub.add_parser("snapshot")
    sn.add_argument("--summary", default="")
    sn.add_argument("--open", nargs="*", default=[])
    sn.add_argument("--next", nargs="*", default=[])
    sn.add_argument("--tags", nargs="*", default=[])
    sn.set_defaults(func=cmd_snapshot)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()