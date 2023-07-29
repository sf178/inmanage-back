import os

def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def bytes_to_gb(size_in_bytes):
    gb_size = size_in_bytes / (1024**3)
    return gb_size

def main():
    base_path = r'C:/'
    folders = os.listdir(base_path)

    folder_sizes = {}
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            size = get_folder_size(folder_path)
            folder_sizes[folder] = size

    for folder, size in folder_sizes.items():
        size_gb = bytes_to_gb(size)
        if size_gb >= 0.3:
            print(f"{folder}: {size_gb:.2f} GB")

if __name__ == "__main__":
    main()
