import rasterio
import h5py
import numpy as np
import os
import osgeo
from osgeo import gdal, osr, ogr, gdalconst
import argparse
from tqdm import tqdm

def to_latlon(x, y, ds):
    bag_gtrn = ds.GetGeoTransform()
    bag_proj = ds.GetProjectionRef()
    bag_srs = osr.SpatialReference(bag_proj)
    geo_srs = bag_srs.CloneGeogCS()
    if int(osgeo.__version__[0]) >= 3:
        # GDAL 3 changes axis order: https://github.com/OSGeo/gdal/issues/1546
        bag_srs.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
        geo_srs.SetAxisMappingStrategy(osgeo.osr.OAMS_TRADITIONAL_GIS_ORDER)
    transform = osr.CoordinateTransformation(bag_srs, geo_srs)

    # in a north up image:
    originX = bag_gtrn[0]
    originY = bag_gtrn[3]
    pixelWidth = bag_gtrn[1]
    pixelHeight = bag_gtrn[5]

    easting = originX + pixelWidth * x + bag_gtrn[2] * y
    northing = originY + bag_gtrn[4] * x + pixelHeight * y

    geo_pt = transform.TransformPoint(easting, northing)[:2]
    lon = geo_pt[0]
    lat = geo_pt[1]
    return lat, lon

def create_latlon_mask(height, width, refDataset, out_type=np.float32):
    # compute lat, lon of top-left and bottom-right corners
    lat_topleft, lon_topleft = to_latlon(x=0, y=0, ds=refDataset)
    lat_bottomright, lon_bottomright = to_latlon(x=width-1, y=height-1, ds=refDataset)

    # interpolate between the corners
    lat_col = np.linspace(start=lat_topleft, stop=lat_bottomright, num=height).astype(out_type)
    lon_row = np.linspace(start=lon_topleft, stop=lon_bottomright, num=width).astype(out_type)

    # expand dimensions of row and col vector to repeat
    lat_col = lat_col[:, None]
    lon_row = lon_row[None, :]

    # repeat column and row to get 2d arrays --> lat lon coordinate for every pixel
    lat_mask = np.repeat(lat_col, repeats=width, axis=1)
    lon_mask = np.repeat(lon_row, repeats=height, axis=0)

    # print('lat_mask.shape: ', lat_mask.shape)
    # print('lon_mask.shape: ', lon_mask.shape)

    return lat_mask, lon_mask

def extract_index_date (string):
    tokens = string.strip().split('_')
    tokens.pop(0)
    index = int(tokens[0])
    tokens.pop(0)
    
    date = '_'.join(tokens)
    return index, date

def stack_gedi_lat_lon(gedi_folder):
    gedi_data, lat_data, lon_data = None, None, None
    sub_folders = sorted(os.listdir(gedi_folder))

    # Preallocate lists for data collection
    gedi_data_list = []
    lat_data_list = []
    lon_data_list = []

    for subf in tqdm(sub_folders):
        index, date = extract_index_date(subf)
        subf_path = os.path.join(gedi_folder, subf)
        files = sorted(os.listdir(subf_path))
        
        for file in files:
            file_path = os.path.join(subf_path, file)
            
            with rasterio.open(file_path) as src:
                data = src.read(1)
                gedi_data_list.append(data[np.newaxis, ..., np.newaxis])  # Add new axis directly

            ref_ds = gdal.Open(file_path)
            lat_mask, lon_mask = create_latlon_mask(height=ref_ds.RasterYSize, width=ref_ds.RasterXSize, refDataset=ref_ds)
            
            lat_data_list.append(lat_mask[np.newaxis, ..., np.newaxis])  # Add new axis directly
            lon_data_list.append(lon_mask[np.newaxis, ..., np.newaxis])  # Add new axis directly

    # Convert lists to arrays at once
    gedi_data = np.concatenate(gedi_data_list, axis=0) if gedi_data_list else None
    lat_data = np.concatenate(lat_data_list, axis=0) if lat_data_list else None
    lon_data = np.concatenate(lon_data_list, axis=0) if lon_data_list else None

    return gedi_data, lat_data, lon_data

def stack_scl(scl_folder):
    scl_data_list = []
    sub_folders = sorted(os.listdir(scl_folder))

    for subf in tqdm(sub_folders):
        index, date = extract_index_date(subf)
        subf_path = os.path.join(scl_folder, subf)
        files = sorted(os.listdir(subf_path))
        
        for file in files:
            file_path = os.path.join(subf_path, file)
            with rasterio.open(file_path) as src:
                data = src.read(1)
                scl_data_list.append(data[np.newaxis, ..., np.newaxis])  # Reshape and add to list
                
    # Concatenate all data at once
    scl_data = np.concatenate(scl_data_list, axis=0) if scl_data_list else None

    return scl_data

def stack_s2(s2_folder):
    s2_data_list = []
    sub_folders = sorted(os.listdir(s2_folder))

    for subf in tqdm(sub_folders):
        index, date = extract_index_date(subf)
        
        subf_path = os.path.join(s2_folder, subf)
        files = sorted(os.listdir(subf_path))
        
        for file in files:
            file_path = os.path.join(subf_path, file)
            with rasterio.open(file_path) as src:
                data = src.read([i for i in range(1, 13)]).transpose(1, 2, 0)  # Read and transpose directly
                s2_data_list.append(data[np.newaxis, ...])  # Reshape and append to the list

    # Concatenate all data at once
    s2_data = np.concatenate(s2_data_list, axis=0) if s2_data_list else None

    return s2_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create h5 files from patches")

    # Add arguments
    parser.add_argument('--data_folder', type=str, required=True, help='Data folder')
    parser.add_argument('--output_folder', type=str, required=True, help='Data folder')
    
    # Parse the arguments
    args = parser.parse_args()
    
    data_folder = args.data_folder
    output_folder = args.output_folder
    
    for subfolder in os.listdir(data_folder):
        gedi_folder_path = os.path.join(data_folder, subfolder, 'GEDI')
        scl_folder_path = os.path.join(data_folder, subfolder, 'SCL')
        s2_folder_path = os.path.join(data_folder, subfolder, 'S2')
        
        gedi_data, lat_data, lon_data = stack_gedi_lat_lon(gedi_folder=gedi_folder_path)
        # gedi_data = np.nan_to_num(gedi_data)
        
        scl_data = stack_scl(scl_folder=scl_folder_path)
        s2_data = stack_s2(s2_folder=s2_folder_path)
        
        print("S2 images shape (Bands, Rows, Columns):", s2_data.shape, "Data type:", s2_data.dtype)
        print("SCL shape (Rows, Columns):", scl_data.shape, "Data type:", scl_data.dtype)
        print("GEDI shape (Rows, Columns):", gedi_data.shape, "Data type:", gedi_data.dtype)
        print("lat shape (Rows, Columns):", lat_data.shape, "Data type:", lat_data.dtype)
        print("lon shape (Rows, Columns):", lon_data.shape, "Data type:", lon_data.dtype)
        
        if s2_data.shape == 0:
            continue 
        
        number = int(subfolder.split("_")[1])
        h5_file_path = f'{output_folder}/h5_{number:02}.h5'

        # Write the datasets to an HDF5 file
        with h5py.File(h5_file_path, "w") as h5_file:
            h5_file.create_dataset("images", data=s2_data, dtype='u2')
            h5_file.create_dataset("scl", data=scl_data, dtype='u1')
            h5_file.create_dataset("canopy_height", data=gedi_data, dtype='f4')
            h5_file.create_dataset("lat", data=lat_data, dtype='f4')
            h5_file.create_dataset("lon", data=lon_data, dtype='f4')
            
        print(f"Created an h5 file at {h5_file_path}")
