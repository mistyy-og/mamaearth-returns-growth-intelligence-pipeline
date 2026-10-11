
import json
import os
from pathlib import Path

from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent
FINDINGS_FILE = BASE_DIR / "findings.json"
SAMPLE_FILE = BASE_DIR / "sample_output.txt"

MODEL_NAME = "gemini-3.8-flash"


def generate_scr_narrative_offline(findings: dict) -> dict:
    """Generate a report without calling an AI API."""

    cleaned = findings["cleaned_total_revenue_inr"]
    raw = findings["raw_total_revenue_inr"]
    delta = findings["duplicate_reconciliation_delta_inr"]
    rates = findings["return_rate_by_payment"]
    risk = findings["highest_risk_segment"]
    peak = findings["true_peak_month"]
    outlier = findings["outlier_inflated_month"]

    narrative = f"""
Situation

Cleaned revenue is INR {cleaned:.2f}, compared with raw revenue
of INR {raw:.2f}. Return rates are {rates['COD']:.1f}% for COD,
{rates['CARD']:.1f}% for CARD, and {rates['UPI']:.1f}% for UPI.
The highest-risk segment is {risk['payment_method']}, City Tier
{risk['city_tier']}, with a return rate of
{risk['return_rate_pct']:.1f}%.

Complication

The duplicate reconciliation difference is INR {delta:.2f}.
For {outlier['month']}, apparent revenue is INR
{outlier['apparent_revenue_inr']:.2f}, while corrected revenue
is INR {outlier['corrected_revenue_inr']:.2f}. Using the
apparent figure could distort monthly comparisons.

Resolution

Use cleaned revenue of INR {cleaned:.2f} for reporting and
retain the INR {delta:.2f} reconciliation difference in the
audit trail. Review the {risk['payment_method']}, City Tier
{risk['city_tier']} segment because its return rate is
{risk['return_rate_pct']:.1f}%. The true peak month is
{peak['month']}, with revenue of INR {peak['revenue_inr']:.2f}.
Use the corrected figure for {outlier['month']} when comparing
monthly performance.
""".strip()

    return {
        "status": "success",
        "narrative": narrative,
        "tokens": 0
    }


import os
print(bool(os.getenv("GEMINI_API_KEY")))
def generate_scr_narrative(findings: dict) -> dict:
    """Generate a narrative with Gemini, or fall back offline."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        result = generate_scr_narrative_offline(findings)
        result["mode"] = "offline"
        return result

    system_instruction = """
You are a senior data analyst writing for Mamaearth's regional
operations and finance heads.

Write a concise business report with exactly three labeled sections:
Situation, Complication, and Resolution.

Use only facts and numerical values from the supplied JSON findings.
Do not invent numbers, causes, or unsupported explanations.
Keep all figures accurate and consistent.
Explain the business significance and give practical recommendations.
"""

    prompt = (
        "Write the report using these verified analysis findings:\n\n"
        + json.dumps(findings, indent=2)
    )

    try:
        client = genai.Client(api_key=api_key)

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.0,
                    max_output_tokens=500,
                    http_options=types.HttpOptions(timeout=60000)
                )
            )
        finally:
            client.close()

        narrative = response.text

        if not narrative or not narrative.strip():
            raise ValueError("Gemini returned an empty narrative.")

        token_count = 0
        usage = getattr(response, "usage_metadata", None)

        if usage and usage.total_token_count is not None:
            token_count = usage.total_token_count

        return {
            "status": "success",
            "narrative": narrative.strip(),
            "tokens": token_count,
            "mode": "gemini"
        }

    except Exception as err:
        print("Gemini unavailable; switching to offline mode.")
        print("Reason:", str(err))

        result = generate_scr_narrative_offline(findings)
        result["mode"] = "offline_fallback"
        result["message"] = str(err)
        return result


def check_narrative(narrative: str) -> dict:
    """Check that the report contains the required figures."""

    normalized = narrative.replace(",", "").lower()

    checks = {
        "cleaned_total_revenue": "97358.30" in normalized,
        "cod_return_rate": "44.4" in normalized,
        "highest_risk_return_rate": "54.5" in normalized,
        "reconciliation_delta": "2501.90" in normalized,
        "peak_month_and_revenue": (
            ("march" in normalized or "2026-03" in normalized)
            and "20318.90" in normalized
        )
    }

    return {
        "passed": all(checks.values()),
        "checks": checks
    }

print("Gemini API key detected:", bool(os.getenv("GEMINI_API_KEY")))
def main():
    if not FINDINGS_FILE.exists():
        print("ERROR: findings.json was not found at:")
        print(FINDINGS_FILE)
        return

    with FINDINGS_FILE.open("r", encoding="utf-8") as file:
        findings = json.load(file)

    result = generate_scr_narrative(findings)
    narrative = result["narrative"]

    SAMPLE_FILE.write_text(narrative + "\n", encoding="utf-8")

    print("\n--- GENERATION MODE ---")
    print(result.get("mode", "unknown"))

    print("\n--- SCR NARRATIVE ---\n")
    print(narrative)

    print("\n--- NARRATIVE CHECKER ---")

    check = check_narrative(narrative)

    for name, passed in check["checks"].items():
        status = "PASS" if passed else "FAIL"
        print(f"{name}: {status}")

    print("\nOverall:", "PASS" if check["passed"] else "FAIL")
    print("Saved output to:", SAMPLE_FILE)


if __name__ == "__main__":
    main()
