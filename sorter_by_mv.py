import os
import json
import shutil


def categorize_extensions(directory):
    v2_folder = os.path.join(directory, "V2")
    v3_folder = os.path.join(directory, "V3")
    os.makedirs(v2_folder, exist_ok=True)
    os.makedirs(v3_folder, exist_ok=True)

    for extension in os.listdir(directory):
        extension_path = os.path.join(directory, extension)
        if not os.path.isdir(extension_path):
            continue

        manifest_path = os.path.join(extension_path, "manifest.json")
        if not os.path.exists(manifest_path):
            continue

        try:
            with open(manifest_path, "r", encoding="utf-8-sig") as f:
                manifest = json.load(f)
                manifest_version = manifest.get("manifest_version")

                if manifest_version == 2:
                    shutil.move(extension_path, os.path.join(v2_folder, extension))
                elif manifest_version == 3:
                    shutil.move(extension_path, os.path.join(v3_folder, extension))
        except (json.JSONDecodeError, OSError) as e:
            print(f"Skipping {extension}: Error reading manifest.json - {e}")


if __name__ == "__main__":
    directory = "/home/tobias/extension-data"
    if os.path.exists(directory) and os.path.isdir(directory):
        categorize_extensions(directory)
        print("Sorting complete.")
    else:
        print("Invalid directory path.")
