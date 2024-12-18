import os
from sys import argv
import sys
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def quit(event):
    sys.exit()

def next(event):
    plt.close()

def plot_chart(extension_size, extension_count):
    sizes = list(extension_size.items())
    counts = list(extension_count.items())
    for i in range(1, len(sizes), 25):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 10))
        chunk = sizes[i:i + 25]
        keys, values = zip(*chunk)
        values = [v / (1024 * 1024)  for v in values]
        bars = ax1.bar(keys, values, color='sienna')
        ax1.set_title('File Size and Count Comparison by Extension')
        ax1.set_ylabel('Size (MB)')
        ax1.set_xticks(range(len(keys)))
        ax1.set_xticklabels(keys, rotation=25, ha='right')
        for bar, value in zip(bars, values):
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{round(value, 2)}', ha='center', va='bottom')
        chunk = counts[i:i + 25]
        keys, values = zip(*chunk)
        bars = ax2.bar(keys, values, color='royalblue')
        ax2.set_ylabel('Count')
        ax2.set_xticks(range(len(keys)))
        ax2.set_xticklabels(keys, rotation=25, ha='right')
        for bar, value in zip(bars, values):
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{(int)(value)}', ha='center', va='bottom')
        ax_button1 = plt.axes([0.89, 0.01, 0.1, 0.03])
        button1 = Button(ax_button1, 'Next')
        button1.on_clicked(next)
        ax_button2 = plt.axes([0.01, 0.01, 0.1, 0.03])
        button2 = Button(ax_button2, 'Quit')
        button2.on_clicked(quit)
        manager = plt.get_current_fig_manager()
        manager.full_screen_toggle()
        plt.show()

def analyze_partition(partition):
    if not os.path.exists(partition + ":\\"):
        print(f"Error: The partition '{partition}' does not exist")
        exit(1)
    extension_count = {}
    extension_size = {}
    total_files = 0
    total_dirs = 0
    total_size = 0
    for root, dirs, files in os.walk(partition + ":\\"):
        total_dirs += len(dirs)
        total_files += len(files)
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()
            file_size = os.path.getsize(file_path)
            total_size += file_size
            if(file_extension not in extension_count):
                extension_count[file_extension] = 1
                extension_size[file_extension] = file_size
            else:
                extension_count[file_extension] += 1
                extension_size[file_extension] += file_size
    plt.figure(figsize=(10, 5))
    plt.pie([total_dirs, total_files], labels=[f'Directories ({total_dirs})', f'Files ({total_files})'], autopct='%1.1f%%', colors=['thistle', 'wheat'])
    plt.title('Directories and Files')
    ax_button1 = plt.axes([0.89, 0.01, 0.1, 0.03])
    button1 = Button(ax_button1, 'Next')
    button1.on_clicked(next)
    ax_button2 = plt.axes([0.01, 0.01, 0.1, 0.03])
    button2 = Button(ax_button2, 'Quit')
    button2.on_clicked(quit)
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()
    plot_chart(extension_size, extension_count)

if __name__ == "__main__":
    if len(argv) < 2:
        print("Error: Please provide a partition")
        exit(0)
    analyze_partition(argv[1])