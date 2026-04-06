"""
app.py - Meeting Transcript Action Item Extractor
--------------------------------------------------
Reads test cases from eval_set.json, sends each transcript to the
Anthropic Claude API, and writes structured results to output.txt.

Usage:
    python app.py

Requirements:
    pip install anthropic python-dotenv

Environment:
    ANTHROPIC_API_KEY  - your Anthropic API key (set in .env or shell)
    SYSTEM_PROMPT      - (optional) override the default system prompt via .env
"""

import json
import os
import sys
from datetime import datetime

import anthropic
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    print("ERROR: ANTHROPIC_API_KEY is not set. Add it to your .env file or shell environment.")
    sys.exit(1)

MODEL = "claude-3-5-haiku-20241022"
EVAL_SET_FILE = "eval_set.json"
OUTPUT_FILE = "output.txt"

# Configurable system prompt — override via SYSTEM_PROMPT in .env
DEFAULT_SYSTEM_PROMPT = (
    "You are an expert meeting assistant. Your job is to read a raw meeting transcript "
    "and extract every confirmed action item. For each action item return exactly three fields:\n"
    "  - Assignee: the person responsible\n"
    "  - Task: a concise description of what needs to be done\n"
    "  - Deadline: when it must be completed (use the exact wording from the transcript; "
    "if no deadline is stated write 'Not specified')\n\n"
    "Important rules:\n"
    "  1. Only include action items that were CONFIRMED. Ignore ideas that were cancelled or walked back.\n"
    "  2. Do not invent deadlines or assignees that are not in the transcript.\n"
    "  3. Format your response as a numbered list. Each item must have all three fields on separate lines."
)

SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)

USER_PROMPT_TEMPLATE = (
    "Please extract all action items from the following meeting transcript:\n\n"
    "---\n"
    "{transcript}\n"
    "---"
)

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def load_eval_set(path: str) -> list[dict]:
    """Load test cases from the JSON eval set."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def call_llm(client: anthropic.Anthropic, transcript: str) -> str:
    """Send a transcript to the Claude API and return the response text."""
    user_message = USER_PROMPT_TEMPLATE.format(transcript=transcript)

    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ],
    )
    return message.content[0].text


def format_output(test_cases: list[dict], results: list[str]) -> str:
    """Build a structured plain-text report from results."""
    lines = []
    lines.append("=" * 70)
    lines.append("MEETING ACTION ITEM EXTRACTOR — EVALUATION RESULTS")
    lines.append(f"Run date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Model    : {MODEL}")
    lines.append("=" * 70)

    for i, (case, result) in enumerate(zip(test_cases, results), start=1):
        lines.append("")
        lines.append(f"TEST CASE {i}: {case['id']}")
        lines.append(f"Description : {case['description']}")
        lines.append("-" * 70)
        lines.append("TRANSCRIPT:")
        lines.append(case["transcript"])
        lines.append("")
        lines.append("LLM OUTPUT:")
        lines.append(result)
        lines.append("")
        lines.append("EXPECTED (grading note):")
        lines.append(case["good_output_note"])
        lines.append("=" * 70)

    return "\n".join(lines)


def main():
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    print(f"Loading eval set from '{EVAL_SET_FILE}'...")
    test_cases = load_eval_set(EVAL_SET_FILE)
    print(f"  Found {len(test_cases)} test case(s).\n")

    results = []
    for i, case in enumerate(test_cases, start=1):
        print(f"[{i}/{len(test_cases)}] Running: {case['id']}...")
        response = call_llm(client, case["transcript"])
        results.append(response)
        print(f"  Done.\n")

    report = format_output(test_cases, results)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Results written to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
