USD_INR_BUDGET_RATE = 100.0

PRICING_CATALOG = {
    "google:gemini-3.7-flash": {
        "input_1m": 0.75,
        "output_1m": 3.75
    },
    # DeepSeek Conservative PEAK and Cache-MISS pricing
    "deepseek:deepseek-v4-flash": {
        "input_1m": 0.44,
        "output_1m": 1.32
    },
    "deepseek:deepseek-v4-pro": {
        "input_1m": 1.32,
        "output_1m": 3.96
    }
}

def estimate_tokens(text: str) -> int:
    """
    Conservative local estimation.
    Deliberately overestimates ordinary English/JSON.
    1 token ~ 3 characters.
    """
    if not text:
        return 0
    return max(1, len(text) // 3)

def calculate_cost_usd(route: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICING_CATALOG.get(route, {"input_1m": 0.0, "output_1m": 0.0})
    cost = (input_tokens / 1_000_000) * rates["input_1m"]
    cost += (output_tokens / 1_000_000) * rates["output_1m"]
    return cost
