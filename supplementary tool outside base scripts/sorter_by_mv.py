import os
import json
import shutil
import multiprocessing

# Directory containing the extensions
directory = "D:\\extensions\\malicious\\combined"

# Output folders
v2_folder = os.path.join(directory, "V2")
v3_folder = os.path.join(directory, "V3")
os.makedirs(v2_folder, exist_ok=True)
os.makedirs(v3_folder, exist_ok=True)


def process_extension(extension):
    extension_path = os.path.join(directory, extension)
    if not os.path.isdir(extension_path):
        return

    manifest_path = os.path.join(extension_path, "manifest.json")
    if not os.path.exists(manifest_path):
        return

    try:
        with open(manifest_path, "r", encoding="utf-8-sig") as f:
            manifest = json.load(f)
            manifest_version = manifest.get("manifest_version")

        if manifest_version == 2:
            shutil.move(extension_path, os.path.join(v2_folder, extension))
            print(f"Moving {extension} to V2")
        elif manifest_version == 3:
            shutil.move(extension_path, os.path.join(v3_folder, extension))
            print(f"Moving {extension} to V3")

    except (json.JSONDecodeError, OSError) as e:
        print(f"Skipping {extension}: Error reading manifest.json - {e}")


def categorize_extensions_parallel():
    extensions = os.listdir(directory)

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(process_extension, extensions)


if __name__ == "__main__":
    categorize_extensions_parallel()
    print("Sorting complete.")
