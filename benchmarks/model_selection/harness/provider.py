import json
import uuid
import time
from .config import sanitize_fixture

class FakeProvider:
    def __init__(self, mode, all_fixtures_with_gold):
        self.mode = mode
        self.all_fixtures_with_gold = all_fixtures_with_gold

    def run_verification(self, sanitized_fixture, max_tokens=1000):
        f_id = sanitized_fixture["fixture_id"]
        gold = self.all_fixtures_with_gold[f_id].get("gold", {})

        result = {}
        if self.mode == "PERFECT":
            result = {
                "verdict": gold.get("verdict", "SUPPORTED"),
                "confidence": 0.95,
                "evidence_assessment": [],
                "material_caveats": gold.get("material_caveats", []),
                "missing_evidence": [],
                "requires_human_review": False,
                "rationale_summary": "Matches perfectly."
            }
        elif self.mode == "CRITICAL_FAIL":
            result = {
                "verdict": "SUPPORTED",
                "confidence": 0.95,
                "evidence_assessment": [],
                "material_caveats": [],
                "missing_evidence": [],
                "requires_human_review": False,
                "rationale_summary": "Invented number 99999"
            }
        elif self.mode == "BAD_SCHEMA":
            result = {"wrong_key": "bad"}
        elif self.mode == "INSUFFICIENT":
            result = {
                "verdict": "NOT_ESTABLISHED",
                "confidence": 0.1,
                "evidence_assessment": [],
                "material_caveats": [],
                "missing_evidence": [],
                "requires_human_review": True,
                "rationale_summary": "Insufficient evidence."
            }

        time.sleep(0.01)
        return {
            "output": result,
            "latency_ms": 10,
            "input_tokens": 100,
            "output_tokens": 50,
            "cost_inr": 0.5
        }

    def run_copy(self, sanitized_fixture, max_tokens=1000):
        f_id = sanitized_fixture["fixture_id"]
        gold = self.all_fixtures_with_gold[f_id].get("gold", {})

        result = {}
        if self.mode == "PERFECT":
            result = {
                "format": "GM-SINGLE-01",
                "slides": [
                    {
                        "slide_index": 1,
                        "role": "HOOK",
                        "headline": "Perfect",
                        "body_blocks": [
                            {"kind": "FACT", "text": "Perfect data", "claim_ids": gold.get("required_claim_ids_for_copy", [])}
                        ],
                        "commentary": "Perfect comment",
                        "mascot_direction": "Smiles"
                    }
                ],
                "caption": "Perfect caption"
            }
        elif self.mode == "CRITICAL_FAIL":
            result = {
                "format": "GM-SINGLE-01",
                "slides": [
                    {
                        "slide_index": 1,
                        "role": "HOOK",
                        "headline": "Number 99999",
                        "body_blocks": [
                            {"kind": "FACT", "text": "Invented 99999", "claim_ids": []}
                        ],
                        "commentary": "Comment",
                        "mascot_direction": "Smiles"
                    }
                ],
                "caption": "99999"
            }
        elif self.mode == "BAD_SCHEMA":
            result = {"bad": "schema"}
        elif self.mode == "INSUFFICIENT":
            result = {
                "format": "GM-SINGLE-01",
                "slides": [
                    {
                        "slide_index": 1,
                        "role": "HOOK",
                        "headline": "Unsure",
                        "body_blocks": [],
                        "commentary": "Unsure",
                        "mascot_direction": "Shrugs"
                    }
                ],
                "caption": "Unsure"
            }

        time.sleep(0.01)
        return {
            "output": result,
            "latency_ms": 10,
            "input_tokens": 100,
            "output_tokens": 50,
            "cost_inr": 0.5
        }
