import os
import json
import csv


PARENT_DIR = "D:\\extensions\\large-dataset\\V2"
OUTPUT_CSV = "manifest_differences_general.csv"


def compare_manifests(manifest_v2, manifest_v3):
    """
    Compare two manifest dictionaries and return a dict with differences.
    Ignores changes in 'manifest_version' and 'version'.
    Returns:
      - 'added': keys present only in V3 with their values.
      - 'removed': keys present only in V2 with their values.
      - 'modified': keys present in both with different values.
          For modified keys, stores a dict with separate V2 and V3 values.
    """
    ignore_keys = {'manifest_version', 'version'}
    diff_result = {
        'added': {},
        'removed': {},
        'modified': {},
    }

    keys_v2 = set(manifest_v2.keys()) - ignore_keys
    keys_v3 = set(manifest_v3.keys()) - ignore_keys

    # Keys added in V3
    for key in keys_v3 - keys_v2:
        diff_result['added'][key] = manifest_v3[key]

    # Keys removed in V3 (present in V2 but not in V3)
    for key in keys_v2 - keys_v3:
        diff_result['removed'][key] = manifest_v2[key]

    # For keys present in both, compare values
    for key in keys_v2.intersection(keys_v3):
        if manifest_v2[key] != manifest_v3[key]:
            diff_result['modified'][key] = {"v2": manifest_v2[key], "v3": manifest_v3[key]}

    return diff_result


def process_extensions(parent_dir):
    """
    Process each extension folder in the main folder.
    V2 manifest is expected in:
      path/to/extensions/ext-id/manifest.json
    V3 manifest is expected in:
      path/to/extensions/converted/ext-id_mv3/manifest.json
    Returns a list of dictionaries with diff information.
    """
    results = []

    # List all items in the parent directory; ignore the "converted" folder.
    for ext_name in os.listdir(parent_dir):
        ext_folder = os.path.join(parent_dir, ext_name)
        if os.path.isdir(ext_folder) and ext_name != "converted":
            manifest_v2_path = os.path.join(ext_folder, "manifest.json")
            manifest_v3_path = os.path.join(parent_dir, "converted", ext_name + "_mv3", "manifest.json")

            if os.path.exists(manifest_v2_path) and os.path.exists(manifest_v3_path):
                try:
                    with open(manifest_v2_path, 'r', encoding='utf-8') as f:
                        manifest_v2 = json.load(f)
                    with open(manifest_v3_path, 'r', encoding='utf-8') as f:
                        manifest_v3 = json.load(f)
                except Exception as e:
                    print(f"Error reading manifest files for '{ext_name}': {e}")
                    continue

                diff = compare_manifests(manifest_v2, manifest_v3)
                # Separate modified details for v2 and v3 values
                modified_details_v2 = {key: diff['modified'][key]["v2"] for key in diff['modified']}
                modified_details_v3 = {key: diff['modified'][key]["v3"] for key in diff['modified']}

                result = {
                    'extension': ext_name,
                    'added_keys': ";".join(diff['added'].keys()),
                    'added_details': json.dumps(diff['added'], ensure_ascii=False),
                    'removed_keys': ";".join(diff['removed'].keys()),
                    'removed_details': json.dumps(diff['removed'], ensure_ascii=False),
                    'modified_keys': ";".join(diff['modified'].keys()),
                    'modified_details_v2': json.dumps(modified_details_v2, ensure_ascii=False),
                    'modified_details_v3': json.dumps(modified_details_v3, ensure_ascii=False),
                    'count_added': len(diff['added']),
                    'count_removed': len(diff['removed']),
                    'count_modified': len(diff['modified'])
                }
                results.append(result)
            else:
                print(f"Skipping '{ext_name}': Missing V2 or V3 manifest file.")
    return results


def save_to_csv(results, output_csv):
    """
    Save the results to a CSV file with the appropriate columns.
    """
    fieldnames = [
        'extension',
        'added_keys', 'added_details',
        'removed_keys', 'removed_details',
        'modified_keys', 'modified_details_v2', 'modified_details_v3',
        'count_added', 'count_removed', 'count_modified'
    ]
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for res in results:
                writer.writerow(res)
        print(f"Results successfully saved to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")


def main():
    results = process_extensions(PARENT_DIR)
    if results:
        save_to_csv(results, OUTPUT_CSV)
    else:
        print("No valid extensions found or no differences detected.")


if __name__ == "__main__":
    main()