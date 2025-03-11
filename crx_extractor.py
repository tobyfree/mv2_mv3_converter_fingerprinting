import os
import zipfile

# Set the directory containing the .crx files
crx_directory = "D:\\extensions\\malicious\\malware"
output_directory = "D:\\extensions\\malicious\\extracted"
# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

def get_cropped_name(filename):
    """Extract everything before the first underscore (_)"""
    base_name = os.path.splitext(filename)[0]  # Remove .crx extension
    return base_name.split("_")[0]  # Keep only the part before "_"

def extract_crx_files(crx_directory, output_directory):
    for file in os.listdir(crx_directory):
        if file.endswith(".crx"):
            crx_path = os.path.join(crx_directory, file)
            folder_name = get_cropped_name(file)  # Apply name cropping
            extract_path = os.path.join(output_directory, folder_name)

            os.makedirs(extract_path, exist_ok=True)  # Create folder

            try:
                with zipfile.ZipFile(crx_path, "r") as zip_ref:
                    zip_ref.extractall(extract_path)
                print(f"Extracted {file} to {extract_path}")
            except zipfile.BadZipFile:
                print(f"Skipping {file}: Not a valid ZIP format")

if __name__ == "__main__":
    extract_crx_files(crx_directory, output_directory)
    print("Extraction complete.")
