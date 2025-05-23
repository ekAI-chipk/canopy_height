import numpy as np
import rasterio as rs
import h5py
import matplotlib.pyplot as plt
import tables
import os

def copy_node(node, h5_file_out, parent_path='/'):
    for child in node:
        child_path = f"{parent_path}{child._v_name}"
        if isinstance(child, tables.Array):
            data = child[:]
            if child._v_name == 'canopy_height':
                data = np.where(data == 0.0, np.nan, data)
            h5_file_out.create_array(parent_path, child._v_name, data)
        elif isinstance(child, tables.Group):
            h5_file_out.create_group(parent_path, child._v_name)
            copy_node(child, h5_file_out, f"{child_path}/")

def replace_zeros(path_in, path_out):
    with tables.open_file(path_in, 'r') as h5_file_in:
        with tables.open_file(path_out, 'w') as h5_file_out:
            copy_node(h5_file_in.root, h5_file_out)
            
if __name__ == "__main__":
    folder_out = "../h5"
    folder_in = "../h5_filter_outlier"
    
    for file in os.listdir(folder_in):
        path_in = os.path.join(folder_in, file)
        path_out = os.path.join(folder_out, file)
        replace_zeros(path_in, path_out)
        break