import os
import shutil
import re

# Define source folder
source_folder = "../h5"

# Define destination folders inside "parts_shuffle"
base_folder = "../data/parts_shuffled"
train_folder = os.path.join(base_folder, "train")
test_folder = os.path.join(base_folder, "test")
val_folder = os.path.join(base_folder, "val")

# Create destination folders if they don't exist
os.makedirs(train_folder, exist_ok=True)
os.makedirs(test_folder, exist_ok=True)
os.makedirs(val_folder, exist_ok=True)

# Define file classification rules
test_numbers = {0, 26, 33}
val_numbers = {29, 3, 4}

# Iterate over files in source folder
for file_name in os.listdir(source_folder):
    match = re.search(r"h5_(\d+)\.h5", file_name)  # Extract number from filename
    if match:
        file_number = int(match.group(1))
        source_path = os.path.join(source_folder, file_name)

        # Determine destination folder
        if file_number in test_numbers:
            destination_folder = test_folder
        elif file_number in val_numbers:
            destination_folder = val_folder
        else:
            destination_folder = train_folder

        # Copy file to the selected folder
        shutil.copy(source_path, os.path.join(destination_folder, file_name))
        print(f"Copied {file_name} to {destination_folder}")
