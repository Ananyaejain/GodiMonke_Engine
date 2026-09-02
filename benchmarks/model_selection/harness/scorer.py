import json
import jsonschema
import re

def extract_numbers(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.replace(",", "")
    return set(re.findall(r'\b\d+(?:\.\d+)?\b', text))

def extract_quotes(text):
    if not isinstance(text, str):
        text = str(text)
    return set(re.findall(r'"([^"]*)"', text)) | set(re.findall(r"'([^']*)'", text))

def extract_dates(text):
    if not isinstance(text, str):
        text = str(text)
    return set(re.findall(r'\b\d{4}-\d{2,4}\b', text)) | set(re.findall(r'\b\d{4}\b', text))

def normalize_caveat(text):
    words = re.findall(r'\w+', str(text).lower())
    return set(words)

def score_verification(output, fixture, schema_valid):
    gold = fixture.get("gold", {})

    components = {
        "verdict_correctness": 0,
        "evidence_fidelity": 0,
        "caveat_retention": 0,
        "unsupported_assertion_discipline": 0,
        "schema_compliance": 0,
        "deterministic_total": 0,
        "critical_fail": False
    }

    if not isinstance(output, dict):
        components["critical_fail"] = True
        return components

    verdict = output.get("verdict")
    gold_verdict = gold.get("verdict")
    if verdict == gold_verdict:
        components["verdict_correctness"] = 30
    elif verdict and gold_verdict and verdict in ["MOSTLY_SUPPORTED", "PARTLY_SUPPORTED"] and gold_verdict in ["MOSTLY_SUPPORTED", "PARTLY_SUPPORTED"]:
        components["verdict_correctness"] = 15

    rationale = str(output.get("rationale_summary", ""))
    output_nums = extract_numbers(rationale)
    output_dates = extract_dates(rationale)
    output_quotes = extract_quotes(rationale)

    allowed_nums = set()
    allowed_dates = set()
    allowed_quotes = set()
    valid_source_ids = set()

    for ev in fixture.get("evidence", []):
        text_block = ev.get("evidence_summary", "") + " " + ev.get("title", "")
        allowed_nums.update(extract_numbers(text_block))
        allowed_dates.update(extract_dates(text_block))
        allowed_quotes.update(extract_quotes(text_block))
        valid_source_ids.add(ev.get("source_id"))

    v_claim = fixture.get("verification_claim", {}).get("text", "")
    allowed_nums.update(extract_numbers(v_claim))
    allowed_dates.update(extract_dates(v_claim))
    allowed_quotes.update(extract_quotes(v_claim))

    if (output_nums - allowed_nums) or (output_dates - allowed_dates) or (output_quotes - allowed_quotes):
        components["critical_fail"] = True
    else:
        components["unsupported_assertion_discipline"] = 15

    ev_assmts = output.get("evidence_assessment", [])
    has_invalid_source = False
    for ea in ev_assmts:
        sid = ea.get("source_id")
        if sid not in valid_source_ids:
            components["critical_fail"] = True
            has_invalid_source = True

    if not has_invalid_source and not components["critical_fail"]:
        components["evidence_fidelity"] = 25

    gold_caveats = gold.get("material_caveats", [])
    out_caveats = output.get("material_caveats", [])
    if gold_caveats:
        matched = 0
        for gc in gold_caveats:
            gc_set = normalize_caveat(gc)
            if not gc_set:
                continue
            for oc in out_caveats:
                oc_set = normalize_caveat(oc)
                if len(gc_set & oc_set) >= max(1, len(gc_set)//3):
                    matched += 1
                    break
        if matched == len(gold_caveats):
            components["caveat_retention"] = 20
        elif matched > 0:
            components["caveat_retention"] = 10
        else:
            components["critical_fail"] = True
    else:
        components["caveat_retention"] = 20

    if schema_valid:
        components["schema_compliance"] = 10

    if components["critical_fail"]:
        components["verdict_correctness"] = 0
        components["evidence_fidelity"] = 0
        components["caveat_retention"] = 0
        components["unsupported_assertion_discipline"] = 0
        if not schema_valid:
            components["schema_compliance"] = 0

    components["deterministic_total"] = sum(v for k, v in components.items() if k != "critical_fail" and k != "deterministic_total")
    return components

def score_copy(output, fixture, schema_valid):
    components = {
        "factual_obedience": 0,
        "concision_template_fit": 0,
        "schema_compliance": 0,
        "deterministic_subtotal": 0,
        "clarity_information_hierarchy": "NEEDS_HUMAN_SCORE",
        "godi_monke_voice": "NEEDS_HUMAN_SCORE",
        "humour_hinglish": "NEEDS_HUMAN_SCORE",
        "variation_non_generic": "NEEDS_HUMAN_SCORE",
        "critical_fail": False
    }

    if not isinstance(output, dict):
        components["critical_fail"] = True
        return components

    gold = fixture.get("gold", {})
    locked_claims = fixture.get("locked_claims", [])

    allowed_nums = set()
    allowed_dates = set()
    allowed_quotes = set()
    allowed_claim_ids = set()

    for lc in locked_claims:
        text = lc.get("display_value", "") + " " + lc.get("text", "")
        allowed_nums.update(extract_numbers(text))
        allowed_dates.update(extract_dates(text))
        allowed_quotes.update(extract_quotes(text))
        allowed_claim_ids.add(lc.get("claim_id"))

    def check_text(text):
        if not text:
            return False
        if (extract_numbers(text) - allowed_nums) or (extract_dates(text) - allowed_dates) or (extract_quotes(text) - allowed_quotes):
            return True
        return False

    cf = False

    if check_text(output.get("caption")):
        cf = True

    slides = output.get("slides", [])
    for slide in slides:
        if check_text(slide.get("headline")):
            cf = True

        blocks = slide.get("body_blocks", [])
        for b in blocks:
            text = str(b.get("text", ""))
            if check_text(text):
                cf = True

            c_ids = b.get("claim_ids", [])
            if b.get("kind") == "FACT" and not c_ids:
                cf = True

            for cid in c_ids:
                if cid not in allowed_claim_ids:
                    cf = True

    if cf:
        components["critical_fail"] = True
        if schema_valid:
            components["schema_compliance"] = 5
        return components

    components["factual_obedience"] = 35
    components["concision_template_fit"] = 10

    if schema_valid:
        components["schema_compliance"] = 5

    components["deterministic_subtotal"] = components["factual_obedience"] + components["concision_template_fit"] + components["schema_compliance"]

    return components

def validate_schema(instance, schema):
    try:
        jsonschema.validate(instance, schema)
        return True
    except jsonschema.ValidationError:
        return False
