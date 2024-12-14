import os
from sys import argv
import matplotlib.pyplot as plt

def analyze_partition(partition):
    extension_count = {}
    extension_size = {}
    total_files = 0
    total_dirs = 0
    for root, dirs, files in os.walk(partition + ":\\"):
        total_dirs += len(dirs)
        total_files += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            file_size = os.path.getsize(file_path)
            if(file_extension not in extension_count):
                extension_count[file_extension] = 1
                extension_size[file_extension] = file_size
            else:
                extension_count[file_extension] += 1
                extension_size[file_extension] += file_size
    plt.figure(figsize=(10, 5))
    plt.pie([total_dirs, total_files], labels=[f'Directories ({total_dirs})', f'Files ({total_files})'], autopct='%1.1f%%', colors=['blue', 'green'])
    plt.title('Directories and Files')
    plt.show()

if __name__ == "__main__":
    partition = argv[1]
    analyze_partition(partition)