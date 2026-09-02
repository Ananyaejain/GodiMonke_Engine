import json
import jsonschema

def detect_critical_fail(output_text, input_text):
    if "99999" in str(output_text):
        return True
    return False

def score_verification(output, gold):
    score = 0
    cf = detect_critical_fail(str(output), "")
    if cf:
        return {"score": 0, "critical_fail": True}

    if output.get("verdict") == gold.get("verdict"):
        score += 5
    else:
        score += 0

    return {"score": score, "critical_fail": False}

def score_copy(output, gold):
    score = 0
    cf = detect_critical_fail(str(output), "")
    if cf:
        return {"score": 0, "critical_fail": True}

    return {
        "score": score,
        "critical_fail": False,
        "humour_score": "NEEDS_HUMAN_SCORE",
        "brand_score": "NEEDS_HUMAN_SCORE",
        "clarity_score": "NEEDS_HUMAN_SCORE"
    }

def validate_schema(instance, schema):
    try:
        jsonschema.validate(instance, schema)
        return True
    except jsonschema.ValidationError:
        return False
