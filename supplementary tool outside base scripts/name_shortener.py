import os

def shorten_directory_names(base_path):
    for entry in os.scandir(base_path):
        if entry.is_dir():
            new_name = entry.name.split('_', 1)[0]  # Get the part before the first underscore
            new_path = os.path.join(base_path, new_name)

            if new_name != entry.name and not os.path.exists(new_path):  # Avoid conflicts
                os.rename(entry.path, new_path)
                print(f'Renamed: {entry.name} -> {new_name}')
            elif new_name == entry.name:
                print(f'Skipped (no change needed): {entry.name}')
            else:
                print(f'Skipped (name conflict): {entry.name}')

# Example usage
directory_to_crawl = "D:\\extensions\\malicious\\Kapravelos\\V3"
shorten_directory_names(directory_to_crawl)
