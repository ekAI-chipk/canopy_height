import os
import argparse
import zipfile

def unzip(folder_path, extract_folder_path):
    """Unzips all ZIP files in a folder into specified subfolders.

    Args:
        folder_path (str): Folder that contains the ZIP files.
        extract_folder_path (str): Folder to extract the files into.
    """
    for file in os.listdir(folder_path):
        if file.endswith('.zip'):
            zip_path = os.path.join(folder_path, file)
            
            if 'GEDI' in file or 'gedi' in file:
                extract_folder = os.path.join(extract_folder_path, 'GEDI')
            else: 
                extract_folder = os.path.join(extract_folder_path, 'S2')
                
            os.makedirs(extract_folder, exist_ok=True)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)
            
            print(f'Extracted {file} to {extract_folder}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Unzip zip files")

    # Add arguments
    parser.add_argument('--folder_path', type=str, required=True, help='Folder that contains Zip files')
    parser.add_argument('--extract_folder_path', type=str, required=True, help='Folder to extract files into')
    # Parse the arguments
    args = parser.parse_args()

    folder_path = args.folder_path
    extract_folder_path = args.extract_folder_path
    unzip(folder_path, extract_folder_path)
