# You will need your own statistical information for sightings, and R-Studio
Use tidyverse on R-Studio to determine when and where it is most statistica>
This helps us narrow down our images of interest from an otherwise impossib>
If you already have a specific spatial or temporal range in mind, use that >

# **Install necessary dependencies in Ubuntu**

```bash
sudo apt update
sudo apt install python3 python3-pip git
pip3 install pandas geemap
pip3 install earthengine-api
```
# **Login to your Google account through your command line**

```bash
earthengine authenticate
```

# **First, we need to create an excel file listing the satellite images within our preferred date, location, and cloud cover ranges.**

## Save the python script titled "Using_Images_From_GEE_Sentinel_2_Satellite.py" from this repository branch onto your computer.

### Update the script for the following criteria

#### Date range 

```start_date = '2023-01-01'  # Customize the start date (YYYY-MM-DD)
end_date = '2023-12-31'    # Customize the end date (YYYY-MM-DD)
```

#### Latitude and Longitude Coordinates

```# Set your area of interest (coordinates of a bounding box)
lat_min = 10.0  # Minimum latitude
lat_max = 20.0  # Maximum latitude
lon_min = 30.0  # Minimum longitude
lon_max = 40.0  # Maximum longitude
```

#### Adjust for maximum cloud coverage that an image can have to be considered.

```cloud_coverage_max = 10  # Maximum cloud coverage percentage (e.g., 10 means images with less than 10% cloud cover)
cloud_coverage_max = 10  # Maximum cloud coverage percentage (e.g., 10 means images with less than 10% cloud cover)
```
### Navigate to the directory where you saved this script

```bash
cd /path/to/your/script
python3 Using_Images_From_GEE_Sentinel_2_Satellite.py
```

### This script will query Google Earth Engine for Sentinel-2 images within the specified region and date range, filter the images based on cloud cover, and save the metadata (Image ID, Date, Linear Ring) of the GEE Sentinel 2 images into an excel file as a list.

## Verify the output of your new excel file listing the GEE Sentinel 2 satellite images within your given parameters.

