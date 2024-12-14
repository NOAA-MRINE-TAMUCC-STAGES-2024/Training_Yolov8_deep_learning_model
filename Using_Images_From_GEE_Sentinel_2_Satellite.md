# All Codes Will Be Run Through Google Colaboratory

## You will need your own statistical information for sightings, and R-Studio
Use tidyverse on R-Studio to determine when and where it is most statistically likely.
This helps us narrow down our images of interest from an otherwise impossible amount of images.
If you already have a specific spatial or temporal range in mind, use that when filling in your parameters. 

## Login to your Google Earth Engine account through your command line

You will need to have a GEE account and project already set up for this to work.

## Import necessary libraries


```python
!pip install pandas geemap earthengine-api tqdm
import pandas as pd
import geemap
import ee
from tqdm import tqdm
```

## Authenticate and initialize Google Earth Engine

```python
ee.Authenticate()
ee.Initialize()
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

## Run this code to create an excel file, listing the Sentinel-2 images taken within your parameters

```python
	# Define an area of interest
aoi = ee.Geometry.Rectangle([lon_min, lat_min, lon_max, lat_max])

	# Filter Sentinel-2 images by date, cloud coverage, and area of interest
collection = (ee.ImageCollection('COPERNICUS/S2')
              .filterBounds(aoi)
              .filterDate(start_date, end_date)
              .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_coverage_max)))

	# Get image information and export to a list
def get_image_info(image):
    info = image.getInfo()
    return {
        'id': info['id'],
        'date': info['properties']['GENERATION_TIME'],
        'cloud_coverage': info['properties']['CLOUDY_PIXEL_PERCENTAGE']
    }

	# Map over the collection to extract metadata
images = collection.toList(collection.size())
image_info = [get_image_info(ee.Image(images.get(i))) for i in range(images.size().getInfo())]

	# Convert to a DataFrame and save as Excel
df = pd.DataFrame(image_info)
df.to_excel('Sentinel_2_Images.xlsx', index=False)

print("Excel file 'Sentinel_2_Images.xlsx' created successfully!")
```

## Download the Output Excel File

After running the above script, download the generated Excel file to your local machine:

```python
from google.colab import files

	# Download the file
files.download('Sentinel_2_Images.xlsx')
```
