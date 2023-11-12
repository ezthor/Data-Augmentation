import os
import matplotlib.pyplot as plt

# 统计bbox的size信息和images的size信息，不记得能不能用了，可能有bug


def get_image_sizes(root_dir):
    image_sizes = []
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder, 'images','train')
        if not os.path.isdir(folder_path):
            continue
        for image_file in os.listdir(folder_path):
            image_path = os.path.join(folder_path, image_file)
            try:
                with open(image_path, 'rb') as f:
                    img_data = f.read()
                    width, height = plt.imread(image_path).shape[:2]
                    print(width,height)
                    image_sizes.append((width, height))
            except Exception as e:
                print(f"Error processing {image_path}: {str(e)}")
    return image_sizes

def get_file_sizes(root_dir, extension='.txt'):
    file_sizes = []
    for folder in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder, 'labels','train')
        if not os.path.isdir(folder_path):
            print('1')
            continue
        for file in os.listdir(folder_path):

            if file.endswith(extension):
                file_path = os.path.join(folder_path, file)
                try:
                    file_size = os.path.getsize(file_path)
                    print(file_size)
                    file_sizes.append(file_size)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
    return file_sizes

def plot_scatter(data, title, x_label, y_label):
    if data:
        x, y = zip(*data)
        plt.scatter(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    else:
        print("No data to plot!")

def plot_histogram(data, title, x_label, y_label, bin_count=20):
    plt.hist(data, bins=bin_count, alpha=0.7)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

if __name__ == "__main__":
    datasets_folder = r"G:\Radar_datasets\yolo\second_period\datasets"

    # Get image sizes
    image_sizes = get_image_sizes(datasets_folder)
    plot_scatter(image_sizes, "Image Sizes", "Width", "Height")

    # Get file sizes for labels
    file_sizes = get_file_sizes(datasets_folder)
    plot_histogram(file_sizes, "Label File Sizes", "Size", "Count")

    # Get file sizes for images
    image_folder_sizes = get_file_sizes(datasets_folder, extension='.jpg')
    plot_histogram(image_folder_sizes, "Image File Sizes", "Size", "Count")
