import json
import jsonschema
import re

SOURCE_ROLE_MAPPING = {
    "SUPPORTS": "SUPPORTS",
    "QUALIFIES": "QUALIFIES",
    "CONTEXT": "CONTEXT",
    "CONTRADICTS": "CONTRADICTS",
    "COUNTER_EVIDENCE": "CONTRADICTS",
    "CORROBORATION": "SUPPORTS",
    "ORIGINAL_STATEMENT": "CONTEXT"
}

def extract_numbers(text):
    if not isinstance(text, str):
        text = str(text)
    text = text.replace(",", "")
    nums = re.findall(r'\b\d+(?:\.\d+)?\b', text)
    return {float(n) for n in nums}

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

def get_allowed_facts(sanitized_fixture):
    """
    Extracts allowed factual values from strictly model-visible fixture data.
    Must never be passed unsanitized fixture containing 'gold'.
    """
    allowed_nums = set()
    allowed_dates = set()
    allowed_quotes = set()
    allowed_claim_ids = set()
    valid_source_roles = {}

    # 1. Verification track fields
    v_claim = sanitized_fixture.get("verification_claim", {}).get("text", "")
    allowed_nums.update(extract_numbers(v_claim))
    allowed_dates.update(extract_dates(v_claim))
    allowed_quotes.update(extract_quotes(v_claim))

    for ev in sanitized_fixture.get("evidence", []):
        text_block = str(ev.get("evidence_summary", "")) + " " + str(ev.get("title", ""))
        allowed_nums.update(extract_numbers(text_block))
        allowed_dates.update(extract_dates(text_block))
        allowed_quotes.update(extract_quotes(text_block))
        valid_source_roles[ev.get("source_id")] = SOURCE_ROLE_MAPPING.get(ev.get("role", "SUPPORTS"), "SUPPORTS")

    for defn in sanitized_fixture.get("definitions", []):
        defn = str(defn)
        allowed_nums.update(extract_numbers(defn))
        allowed_dates.update(extract_dates(defn))
        allowed_quotes.update(extract_quotes(defn))

    # 2. Copy track fields
    rs = str(sanitized_fixture.get("research_summary", ""))
    allowed_nums.update(extract_numbers(rs))
    allowed_dates.update(extract_dates(rs))
    allowed_quotes.update(extract_quotes(rs))

    for lc in sanitized_fixture.get("locked_claims", []):
        text = str(lc.get("display_value", "")) + " " + str(lc.get("text", ""))
        allowed_nums.update(extract_numbers(text))
        allowed_dates.update(extract_dates(text))
        allowed_quotes.update(extract_quotes(text))
        allowed_claim_ids.add(lc.get("claim_id"))

    return allowed_nums, allowed_dates, allowed_quotes, valid_source_roles, allowed_claim_ids

def get_sanitized_for_extractor(fixture):
    # Ensure gold is not in the object we pass to get_allowed_facts
    sanitized = {k: v for k, v in fixture.items() if k not in ["gold", "prohibited_claims", "human_gold_status"]}
    return sanitized

def score_verification(output, fixture, schema_valid):
    gold = fixture.get("gold", {})
    sanitized = get_sanitized_for_extractor(fixture)
    allowed_nums, allowed_dates, allowed_quotes, valid_source_roles, _ = get_allowed_facts(sanitized)

    components = {
        "verdict_correctness": 0,
        "evidence_integrity": 0,
        "semantic_evidence_fidelity": "NEEDS_HUMAN_SCORE",
        "caveat_retention": 0,
        "unsupported_assertion_discipline": 0,
        "schema_compliance": 0,
        "deterministic_subtotal": 0,
        "final_score": "NEEDS_HUMAN_SCORE",
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

    certainty_flags = ["confirmed fact", "assured", "100% certain"]
    if any(cf in rationale.lower() for cf in certainty_flags):
        components["critical_fail"] = True

    output_nums = extract_numbers(rationale)
    output_dates = extract_dates(rationale)
    output_quotes = extract_quotes(rationale)

    for cav in output.get("material_caveats", []):
        cav = str(cav)
        output_nums.update(extract_numbers(cav))
        output_dates.update(extract_dates(cav))
        output_quotes.update(extract_quotes(cav))

    if (output_nums - allowed_nums) or (output_dates - allowed_dates) or (output_quotes - allowed_quotes):
        components["critical_fail"] = True
    else:
        components["unsupported_assertion_discipline"] = 15

    ev_assmts = output.get("evidence_assessment", [])
    has_invalid_source = False
    has_wrong_role = False
    for ea in ev_assmts:
        sid = ea.get("source_id")
        assmt = ea.get("assessment")
        if sid not in valid_source_roles:
            components["critical_fail"] = True
            has_invalid_source = True
        elif valid_source_roles[sid] != assmt:
            has_wrong_role = True

    if not has_invalid_source:
        if not has_wrong_role and len(ev_assmts) == len(valid_source_roles):
            components["evidence_integrity"] = 15

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
    else:
        components["caveat_retention"] = 20

    if schema_valid:
        components["schema_compliance"] = 10

    if components["critical_fail"]:
        components["verdict_correctness"] = 0
        components["evidence_integrity"] = 0
        components["caveat_retention"] = 0
        components["unsupported_assertion_discipline"] = 0
        if not schema_valid:
            components["schema_compliance"] = 0

    components["deterministic_subtotal"] = sum(v for k, v in components.items() if isinstance(v, int) and not isinstance(v, bool))
    return components

def score_copy(output, fixture, schema_valid):
    gold = fixture.get("gold", {})
    sanitized = get_sanitized_for_extractor(fixture)
    allowed_nums, allowed_dates, allowed_quotes, _, allowed_claim_ids = get_allowed_facts(sanitized)

    components = {
        "deterministic_factual_safety": 0,
        "semantic_factual_fidelity": "NEEDS_HUMAN_SCORE",
        "clarity_information_hierarchy": "NEEDS_HUMAN_SCORE",
        "godi_monke_voice": "NEEDS_HUMAN_SCORE",
        "humour_hinglish": "NEEDS_HUMAN_SCORE",
        "concision_template_fit": 0,
        "variation_non_generic": "NEEDS_HUMAN_SCORE",
        "schema_compliance": 0,
        "deterministic_subtotal": 0,
        "final_score": "NEEDS_HUMAN_SCORE",
        "critical_fail": False
    }

    if not isinstance(output, dict):
        components["critical_fail"] = True
        return components

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

    components["deterministic_factual_safety"] = 20

    req_format = fixture.get("copy_format", "GM-SINGLE-01")
    if output.get("format") == req_format:
        n_slides = len(slides)
        if req_format in ["GM-SINGLE-01", "GM-COMPARE-01"]:
            if n_slides == 1:
                components["concision_template_fit"] = 10
        elif req_format == "GM-CAROUSEL-01":
            if 3 <= n_slides <= 5:
                components["concision_template_fit"] = 10

    if schema_valid:
        components["schema_compliance"] = 5

    components["deterministic_subtotal"] = sum(v for k, v in components.items() if isinstance(v, int) and not isinstance(v, bool))

    return components

def validate_schema(instance, schema):
    try:
        jsonschema.validate(instance, schema)
        return True
    except jsonschema.ValidationError:
        return False
