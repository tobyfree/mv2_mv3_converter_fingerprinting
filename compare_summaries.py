#!/usr/bin/env python3
import json


def compare_summaries(malicious_json, general_json, output_json="comparison.json"):
    """
    Compare two summaries (malicious vs. general).  For each column:
      - For each token in either summary
      - Show absolute count difference, ratio difference, etc.
    """
    comparison = {}

    # The JSON structure is: summary[col] = {
    #     "total_tokens": int,
    #     "token_counts": { "some_token": {"count": X, "ratio": Y}, ... },
    #     "total_raw_values": int,
    #     "raw_values": { ... }
    # }
    columns = set(malicious_json.keys()) | set(general_json.keys())

    for col in columns:
        col_mal = malicious_json.get(col, {})
        col_gen = general_json.get(col, {})

        mal_tokens = col_mal.get("token_counts", {})
        gen_tokens = col_gen.get("token_counts", {})

        # We'll combine the keys from both sets of tokens
        all_tokens = set(mal_tokens.keys()) | set(gen_tokens.keys())

        token_diffs = {}
        for token in all_tokens:
            mal_info = mal_tokens.get(token, {"count": 0, "ratio": 0.0})
            gen_info = gen_tokens.get(token, {"count": 0, "ratio": 0.0})

            mal_count = mal_info["count"]
            gen_count = gen_info["count"]
            mal_ratio = mal_info["ratio"]
            gen_ratio = gen_info["ratio"]

            # Differences
            diff_count = mal_count - gen_count
            diff_ratio = mal_ratio - gen_ratio

            token_diffs[token] = {
                "mal_count": mal_count,
                "gen_count": gen_count,
                "diff_count": diff_count,
                "mal_ratio": round(mal_ratio, 6),
                "gen_ratio": round(gen_ratio, 6),
                "diff_ratio": round(diff_ratio, 6)
            }

        comparison[col] = {
            "token_differences": token_diffs
        }

    # Write out a JSON with the differences
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(comparison, f, indent=2)
    print(f"Wrote comparison results to {output_json}")


def main():
    # Load both
    with open("malicious_summary.json", "r", encoding="utf-8") as f:
        malicious_data = json.load(f)
    with open("general_summary.json", "r", encoding="utf-8") as f:
        general_data = json.load(f)

    # Compare
    compare_summaries(malicious_data, general_data, output_json="comparison_results.json")


if __name__ == "__main__":
    main()
