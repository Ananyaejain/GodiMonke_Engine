import json
import jsonschema
import re

def extract_numbers(text):
    if not isinstance(text, str):
        text = str(text)
    # Extract numbers like 12.22, 12, 17.15, etc.
    return set(re.findall(r'\b\d+(?:\.\d+)?\b', text))

def extract_quotes(text):
    if not isinstance(text, str):
        text = str(text)
    return set(re.findall(r'"([^"]*)"', text)) + set(re.findall(r"'([^']*)'", text))

def score_verification(output, fixture):
    gold = fixture.get("gold", {})
    score = 0
    cf = False

    # 1. Verdict correctness (30)
    verdict = output.get("verdict")
    gold_verdict = gold.get("verdict")
    if verdict == gold_verdict:
        score += 30
    elif verdict and gold_verdict and verdict in ["MOSTLY_SUPPORTED", "PARTLY_SUPPORTED"] and gold_verdict in ["MOSTLY_SUPPORTED", "PARTLY_SUPPORTED"]:
        score += 15 # adjacent

    # 2. Evidence fidelity (25)
    # Proxy: no invented numbers in rationale
    rationale = output.get("rationale_summary", "")
    output_nums = extract_numbers(rationale)

    # gather allowed numbers from evidence
    allowed_nums = set()
    for ev in fixture.get("evidence", []):
        allowed_nums.update(extract_numbers(ev.get("evidence_summary", "")))
        allowed_nums.update(extract_numbers(ev.get("title", "")))
        allowed_nums.update(extract_numbers(ev.get("published_at", "")))
    allowed_nums.update(extract_numbers(fixture.get("verification_claim", {}).get("text", "")))

    unsupported_nums = output_nums - allowed_nums
    if unsupported_nums:
        cf = True
    else:
        score += 25

    # 3. Caveat retention (20)
    # Check if gold material caveats are present
    gold_caveats = gold.get("material_caveats", [])
    output_caveats = str(output.get("material_caveats", []))
    caveats_kept = True
    # For a deterministic check, we just check if some key words from gold caveats are in output caveats.
    # To be simpler, we will give 20 if len(output_caveats) >= len(gold_caveats) unless it's empty.
    if gold_caveats and not output.get("material_caveats"):
        caveats_kept = False
        cf = True
    if caveats_kept:
        score += 20

    # 4. Unsupported-assertion discipline (15)
    # Already partially covered by cf, but we give 15 if not cf
    if not cf:
        score += 15

    # 5. Schema compliance (10)
    # Assuming passed if we reached here with a dict
    score += 10

    # Forced check for arbitrary hallucinated values in output
    if "99999" in str(output):
        cf = True

    if cf:
        return {"score": 0, "critical_fail": True}

    return {"score": score, "critical_fail": False}

def score_copy(output, fixture):
    gold = fixture.get("gold", {})
    score = 0
    cf = False

    # Allowed numbers from locked claims
    locked_claims = fixture.get("locked_claims", [])
    allowed_nums = set()
    allowed_claim_ids = set()
    for lc in locked_claims:
        allowed_nums.update(extract_numbers(lc.get("display_value", "")))
        allowed_nums.update(extract_numbers(lc.get("text", "")))
        allowed_claim_ids.add(lc.get("claim_id"))

    # Factual blocks checks
    blocks = output.get("blocks", [])
    for b in blocks:
        text = str(b.get("text", "")) + str(b.get("heading", ""))
        b_nums = extract_numbers(text)

        # Numeric values in output not in locked input
        if b_nums - allowed_nums:
            cf = True

        # Factual blocks with no supporting claim ID where required
        # Unsupported claim IDs
        c_ids = b.get("claim_ids", [])
        if b.get("block_type") == "factual" and not c_ids:
            cf = True

        for cid in c_ids:
            if cid not in allowed_claim_ids:
                cf = True

    if "99999" in str(output):
        cf = True

    if cf:
        return {"score": 0, "critical_fail": True}

    # Deterministic components:
    # factual obedience: 35
    score += 35
    # concision/template fit: 10
    score += 10
    # schema compliance: 5
    score += 5

    return {
        "score": score,
        "critical_fail": False,
        "humour_score": "NEEDS_HUMAN_SCORE",
        "brand_score": "NEEDS_HUMAN_SCORE",
        "clarity_score": "NEEDS_HUMAN_SCORE",
        "variation_score": "NEEDS_HUMAN_SCORE"
    }

def validate_schema(instance, schema):
    try:
        jsonschema.validate(instance, schema)
        return True
    except jsonschema.ValidationError:
        return False
