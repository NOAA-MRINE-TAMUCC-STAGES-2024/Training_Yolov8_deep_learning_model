# All Codes Will Be Run Through Google Colaboratory

## You will need your own statistical information for sightings, and R-Studio
Use tidyverse on R-Studio to determine when and where it is most statistically likely.
This helps us narrow down our images of interest from an otherwise impossible amount of images.
If you already have a specific spatial or temporal range in mind, use that when filling in your parameters. 

## Login to your Google Earth Engine account through your command line

You will need to have a GEE account and Cloud Project Account with billing information set up for this to work.

## Import necessary libraries

```python
!pip install pandas geemap earthengine-api tqdm
import pandas as pd
import geemap
import ee
from tqdm import tqdm
```

## Mount Google Drive

drive.mount('/content/drive')

## Authenticate and initialize Google Earth Engine

```python
project_id = 'your_project_id'  # Example: 'my-cloud-project-123'
ee.Authenticate()
ee.Initialize(project=project_id)
```

## Define your python preferred image parameters

### Date range

Adjust the date range to filter images.

```python
start_date = '2023-01-01'  # Customize the start date (YYYY-MM-DD)
end_date = '2023-12-31'    # Customize the end date (YYYY-MM-DD)
```

### Latitude and longitude coordinates

Set your area of interest (coordinates of a bounding box).

```python
lat_min = 10.0  # Minimum latitude
lat_max = 20.0  # Maximum latitude
lon_min = 30.0  # Minimum longitude
lon_max = 40.0  # Maximum longitude
```

### Maximum cloud cover

Specify the maximum cloud coverage an image is allowed to have.

```python
cloud_coverage_max = 10  # Maximum cloud coverage percentage (e.g., 10%)
```

```python
# Function to mask clouds using the Sentinel-2 QA band
def maskS2clouds(image):
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(qa.bitwiseAnd(cirrusBitMask).eq(0))
    return image.updateMask(mask).divide(10000)

# Define region and date range for Sentinel-2 image collection
region = ee.Geometry.Rectangle([lon_max, lat_max, lon_min, lat_min])
# Load the Sentinel-2 image collection
dataset = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
    .filterDate(start_date, end_date) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_coverage_max)) \
    .filterBounds(region) \
    .map(maskS2clouds)

# Function to extract image metadata
def getImageMetadata(image_info):
    # Extract system:index and system:footprint properties
    index = image_info['properties']['system:index']
    footprint = image_info['properties']['system:footprint']['coordinates']

    # Parse index to get date and time (consider different formats)
    index_parts = index.split('_')[0].split('T')
    date = index_parts[0]

    # Format the date (yyyy-mm-dd)
    date_formatted = f'{date[:4]}-{date[4:6]}-{date[6:8]}'

    return {
        'image name': index,
        'area of interest': 'Cape Canaveral, Florida',  # Example area of interest
        'date': date_formatted,
        'Linear Ring': footprint
    }

# Initialize an empty list to store metadata
metadata_list = []

# Get image information
images_info = dataset.getInfo()['features']

# Check if no images were found and print a message
if not images_info:
    print("No images found for the given parameters.")
else:
    # Add a progress bar with tqdm
    for image_info in tqdm(images_info, desc="Processing images"):
        metadata = getImageMetadata(image_info)
        metadata_list.append(metadata)

    # Convert the list to a pandas DataFrame
    df = pd.DataFrame(metadata_list)

    # Define the file path in Google Drive
    file_path = '/content/drive/MyDrive/Sentinel_2_Images.xlsx'

    # Save the DataFrame to an Excel file
    df.to_excel(file_path, index=False)

    print(f'Saved metadata to {file_path}')
```
