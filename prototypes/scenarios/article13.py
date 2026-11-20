"""A bounded, synthetic fact-retention window; no language model is called."""

from __future__ import annotations


def retain_facts(facts: list[str], capacity: int) -> list[str]:
    if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity < 1:
        raise ValueError("capacity must be a positive integer")
    if any(not isinstance(fact, str) for fact in facts):
        raise TypeError("facts must be strings")
    return list(facts[-capacity:])


def run(seed: int = 42, capacity: int = 4) -> dict:
    facts = [f"session-{i:02}: fact-{i:02}" for i in range(12)]
    retained = retain_facts(facts, capacity)
    retained_set = set(retained)
    return {
        "evidence_type": "synthetic",
        "seed": seed,
        "capacity": capacity,
        "total_facts": len(facts),
        "retained_facts": retained,
        "memory_size": len(retained),
        "recall": {
            "oldest_fact_available": facts[0] in retained_set,
            "most_recent_fact_available": facts[-1] in retained_set,
        },
        "limitations": [
            "This is an exact-string sliding window, not an agent, vector store, or semantic memory.",
            "It does not test summaries, contradiction handling, temporal reasoning, or multi-session questions.",
        ],
    }
