import rasterio as rs
import numpy as np
import os
import shutil
import argparse

def extract_id_month_year(file_path):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    tokens = base_name.split('_')
    tokens.pop(0)
    tokens.pop(0)
    index = tokens[0]
    tokens.pop(0)

    id_month_year = '_'.join(tokens)
    return int(index), id_month_year

def gedi_ratio(gedi):
    return np.sum(~np.isnan(gedi)) / gedi.size

def crop2patches(
    gedi_file_path,
    s2_file_path,
    gedi_crop_folder,
    s2_crop_folder,
    scl_crop_folder,
    threshold=75,
    stride=None,
):
    index, id_month_year = extract_id_month_year(s2_file_path)
    # Create directories once
    image_dir = os.path.join(s2_crop_folder, f"s2_{index:04}_{id_month_year}")
    scl_dir = os.path.join(scl_crop_folder, f"scl_{index:04}_{id_month_year}")
    gedi_dir = os.path.join(gedi_crop_folder, f"gedi_{index:04}_{id_month_year}")
    
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(scl_dir, exist_ok=True)
    os.makedirs(gedi_dir, exist_ok=True)
    
    total_patch = 0
    
    with rs.open(gedi_file_path) as gedi_src, rs.open(s2_file_path) as s2_src:
        image = s2_src.read([i for i in range(1, 13)])
        scl = s2_src.read(13)
        
        patch_size = 15
        stride = patch_size // 2 if stride is None else stride
        
        height, width = gedi_src.shape
        gedi_img = np.expand_dims(gedi_src.read(1), axis=0)  # Expand to C x H x W
        if threshold is not None:
            gedi_img[gedi_img > threshold] = np.nan
            
        patch_count = 0
        
        for i in range(0, height, stride):
            for j in range(0, width, stride):
                if i + patch_size > height or j + patch_size > width:
                    continue
                
                total_patch += 1
                
                crop_gedi = gedi_img[:, i:i + patch_size, j:j + patch_size]
                if gedi_ratio(crop_gedi) == 0:
                    continue
                
                crop_scl = scl[i:i + patch_size, j:j + patch_size]
                if np.isnan(crop_scl).any():
                    continue
                
                crop_scl = np.expand_dims(crop_scl, axis=0)
                crop_image = image[:, i:i + patch_size, j:j + patch_size]
                if np.isnan(crop_image).any():
                    continue
                
                # Prepare output file paths
                output_image_file = os.path.join(image_dir, f"patch_{patch_count:04}.tif")
                output_scl_file = os.path.join(scl_dir, f"patch_{patch_count:04}.tif")
                output_gedi_file = os.path.join(gedi_dir, f"patch_{patch_count:04}.tif")
                
                # Write the cropped patches to files
                with rs.open(output_image_file, "w", driver="GTiff", height=crop_image.shape[1],
                             width=crop_image.shape[2], count=crop_image.shape[0],
                             dtype=crop_image.dtype, crs=s2_src.crs, transform=s2_src.transform) as image_dst:
                    image_dst.write(crop_image)
                    
                with rs.open(output_scl_file, "w", driver="GTiff", height=crop_scl.shape[1],
                             width=crop_scl.shape[2], count=crop_scl.shape[0],
                             dtype=crop_scl.dtype, crs=s2_src.crs, transform=s2_src.transform) as scl_dst:
                    scl_dst.write(crop_scl)
                    
                with rs.open(output_gedi_file, "w", driver="GTiff", height=crop_gedi.shape[1],
                             width=crop_gedi.shape[2], count=crop_gedi.shape[0],
                             dtype=crop_gedi.dtype, crs=gedi_src.crs, transform=gedi_src.transform) as gedi_dst:
                    gedi_dst.write(crop_gedi)
                    
                patch_count += 1
    try:
        return patch_count, total_patch
    except:
        return 0, 0
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Crop files into patches")

    # Add arguments
    parser.add_argument('--data_folder', type=str, required=True, help='Folder that contains S2 and GEDI data')
    parser.add_argument('--crop_folder_path', type=str, required=True, help='Folder to store cropped patches')
    
    # Parse the arguments
    args = parser.parse_args()
    data_folder = args.data_folder
    crop_folder_path = args.crop_folder_path
    
    for subfolder in os.listdir(data_folder):
        if "GEDI" in subfolder:
            gedi_folder_path = os.path.join(data_folder, subfolder)
        else: 
            s2_folder_path = os.path.join(data_folder, subfolder)
            
    gedi_folders = sorted(folder for folder in os.listdir(gedi_folder_path))
    s2_folders = sorted(folder for folder in os.listdir(s2_folder_path))
    
    for gedi_folder, s2_folder in zip(gedi_folders, s2_folders):
        print(f"Crop files in {gedi_folder, s2_folder}")
        number = int(gedi_folder.split('_')[1])
        gedi_subfolder_path = os.path.join(gedi_folder_path, gedi_folder)
        s2_subfolder_path = os.path.join(s2_folder_path, s2_folder)
        
        gedi_files = sorted(file for file in os.listdir(gedi_subfolder_path))
        s2_files = sorted(file for file in os.listdir(s2_subfolder_path))
        
        total_patch = 0
        for gedi_file, s2_file in zip (gedi_files, s2_files):
            patch_count, _ = crop2patches(
                gedi_file_path=os.path.join(gedi_subfolder_path, gedi_file),
                s2_file_path=os.path.join(s2_subfolder_path, s2_file),
                gedi_crop_folder=os.path.join(crop_folder_path, f'data_{number:02}', 'GEDI'),
                s2_crop_folder=os.path.join(crop_folder_path, f'data_{number:02}', 'S2'),
                scl_crop_folder=os.path.join(crop_folder_path, f'data_{number:02}', 'SCL'),
                stride=5 # overlap 2/3
            )
            total_patch += patch_count
        
        print(total_patch)




