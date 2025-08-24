from typing import List, Dict, Any

def select_candidate(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not candidates:
        return {}
    status_rank = {"approved": 0, "review": 1, "draft": 2}
    # Choose best status first
    best = min((status_rank.get(c.get("status"), 99) for c in candidates))
    pool = [c for c in candidates if status_rank.get(c.get("status"), 99) == best]
    # Within best status: pick max updatedAt then max path
    return max(pool, key=lambda c: (c.get("updatedAt", ""), c.get("path", "")))


