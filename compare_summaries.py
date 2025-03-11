#!/usr/bin/env python3
import json

def load_summary(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)

def compare_patterns(general_summary, malicious_summary, field="token_counts"):
    """
    For each column and each token (or raw value) in that field,
    compute:
       - gen_ratio: ratio in the general dataset (or 0 if not present)
       - mal_ratio: ratio in the malicious dataset (or 0 if not present)
       - abs_diff: absolute difference (|mal_ratio - gen_ratio|)
       - relative_diff: abs_diff divided by the larger ratio (or 0 if both are zero)
    Returns a dict with these details.
    """
    diff_summary = {}
    # Iterate over columns present in either summary
    all_columns = set(general_summary.keys()).union(set(malicious_summary.keys()))
    for col in all_columns:
        gen_patterns = general_summary.get(col, {}).get(field, {})
        mal_patterns = malicious_summary.get(col, {}).get(field, {})

        # Get union of all keys in this column (tokens or raw values)
        all_keys = set(gen_patterns.keys()).union(set(mal_patterns.keys()))
        col_diff = {}
        for key in all_keys:
            gen_ratio = gen_patterns.get(key, {}).get("ratio", 0.0)
            mal_ratio = mal_patterns.get(key, {}).get("ratio", 0.0)
            abs_diff = abs(mal_ratio - gen_ratio)
            # Calculate relative difference (avoiding division by zero)
            if max(mal_ratio, gen_ratio) > 0:
                relative_diff = abs_diff / max(mal_ratio, gen_ratio)
            else:
                relative_diff = 0.0

            col_diff[key] = {
                "general_ratio": gen_ratio,
                "malicious_ratio": mal_ratio,
                "absolute_diff": abs_diff,
                "relative_diff": relative_diff
            }
        diff_summary[col] = col_diff
    return diff_summary

def main():
    # Load the two summaries
    general_summary = load_summary("general_summary.json")
    malicious_summary = load_summary("malicious_summary.json")

    # Compare token counts (you could similarly compare "raw_values")
    diff_tokens = compare_patterns(general_summary, malicious_summary, field="token_counts")
    diff_raw = compare_patterns(general_summary, malicious_summary, field="raw_values")

    # Combine into one result
    combined_diff = {
        "token_comparison": diff_tokens,
        "raw_value_comparison": diff_raw
    }

    # Save the comparison result to JSON
    with open("comparison_summary.json", "w", encoding="utf-8") as f:
        json.dump(combined_diff, f, indent=4)
    print("Comparison summary written to comparison_summary.json")

if __name__ == "__main__":
    main()
