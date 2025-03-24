#!/usr/bin/env python3
import json
import argparse
from tqdm import tqdm

# ========================
# Helper Functions
# ========================
def load_summary(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_patterns(general_summary, malicious_summary, field="token_counts"):
    """
    Compare token or raw value patterns between general and malicious summaries.
    Returns a dict mapping each column to its pattern differences.
    """
    diff_summary = {}
    all_columns = set(general_summary.keys()).union(set(malicious_summary.keys()))
    for col in tqdm(all_columns, desc=f"Comparing {field}", unit="col"):
        gen_patterns = general_summary.get(col, {}).get(field, {})
        mal_patterns = malicious_summary.get(col, {}).get(field, {})

        all_keys = set(gen_patterns.keys()).union(set(mal_patterns.keys()))
        col_diff = {}
        for key in all_keys:
            gen_ratio = gen_patterns.get(key, {}).get("ratio", 0.0)
            mal_ratio = mal_patterns.get(key, {}).get("ratio", 0.0)
            abs_diff = abs(mal_ratio - gen_ratio)
            relative_diff = abs_diff / max(mal_ratio, gen_ratio) if max(mal_ratio, gen_ratio) > 0 else 0.0

            col_diff[key] = {
                "general_ratio": gen_ratio,
                "malicious_ratio": mal_ratio,
                "absolute_diff": abs_diff,
                "relative_diff": relative_diff
            }
        diff_summary[col] = col_diff
    return diff_summary

# ========================
# Main Function
# ========================
def main(args=None):
    parser = argparse.ArgumentParser(description="Compare general vs. malicious pattern summaries.")
    parser.add_argument("--general_json", help="Path to general summary JSON", default="general_summary.json")
    parser.add_argument("--malicious_json", help="Path to malicious summary JSON", default="malicious_summary.json")
    parser.add_argument("--output", help="Path to output comparison JSON", default="comparison_summary.json")
    parsed = parser.parse_args(args)

    general_summary = load_summary(parsed.general_json)
    malicious_summary = load_summary(parsed.malicious_json)

    diff_tokens = compare_patterns(general_summary, malicious_summary, field="token_counts")
    diff_raw = compare_patterns(general_summary, malicious_summary, field="raw_values")

    combined_diff = {
        "token_comparison": diff_tokens,
        "raw_value_comparison": diff_raw
    }

    with open(parsed.output, "w", encoding="utf-8") as f:
        json.dump(combined_diff, f, indent=4)
    print(f"✅ Comparison summary written to {parsed.output}")

if __name__ == "__main__":
    main()
