# This file will walk you through viewing and saving individual images in Google Colaboratory from Google Earth Engine's Sentinel-2 Satellite

# Excel file requirements

Your excel file should be named: "Sentinel_2_Images.xlsx" and it should have a column named: "image_ID"

# Google Drive folder

Ensure the folder name specified in the "folder_name" parameter exists in your Google Drive, or GEE will create it automatically.

## Install the necessary python libraries if you have not already

```python
!pip install pandas geemap google-auth earthengine-api openpyxl
```

## Authenticate and initialize Google Earth Engine

Authenticate and initialize the Google Earth Engine API:

```python
import ee

# Authenticate Google Earth Engine
ee.Authenticate()

# Initialize GEE
project_ID='your-project-ID'
ee.Initialize(project=project_ID)
```

## Mount Google Drive and load the excel file

Mount your Google Drive to access the Excel file and read the "image_ID" column:

```python
from google.colab import drive
import pandas as pd

# Mount Google Drive
drive.mount('/content/drive')

# Path to the Excel file in your Drive
excel_path = '/content/drive/MyDrive/Sentinel_2_Images.xlsx'

# Load the Excel file and get the "image_ID" column
df = pd.read_excel(excel_path, sheet_name=0)  # Adjust sheet_name if needed
image_ids = df['image_ID'].dropna().tolist()  # Ensure no empty rows

print(f"Loaded {len(image_ids)} image IDs from the Excel file.")
```

## Define a function to export images to Google Drive

```python
def export_image(image_id, folder_name="Sentinel2_Exports"):
    """
    Export a Sentinel-2 image to Google Drive.
    Args:
        image_id (str): The ID of the image to export.
        folder_name (str): The folder name in Google Drive where the images will be saved.
    """
    try:
        # Load the image by its ID
        image = ee.Image(image_id)
        
        # Export task parameters
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=f"Export_{image_id.split('/')[-1]}",
            folder=folder_name,
            fileNamePrefix=image_id.split('/')[-1],
            scale=10,  # Adjust resolution if needed
            region=image.geometry().bounds().getInfo()['coordinates'],  # Export the entire image
            maxPixels=1e13  # Set a large limit for pixel exports
        )
        
        # Start the export task
        task.start()
        print(f"Export started for image ID: {image_id}")
    except Exception as e:
        print(f"Error processing image ID {image_id}: {e}")
```

## Process all image IDs

Loop through the list of image_ID values from the excel file and export each image:

```python
# Define the Google Drive folder name where the exports will be saved
export_folder = "Sentinel2_Exports"

# Process each image ID
for image_id in image_ids:
    export_image(image_id, folder_name=export_folder)
```

## Check Export Status

Monitor the status of export tasks directly in the Google Earth Engine Tasks dashboard.

# *Output*

This process will create a folder in the user's Google Drive with all of the images, which they can then scan through to find their object of interest.

# If the user does not want to download ALL of the images to their Google Drive

The user should go to the Google Earth Engine code editor platform using this url: https://code.earthengine.google.com/

Then, the user can manually copy and paste the image_name into the following script, and scan the image through the GEE platform itself.

```javascript
// Function to display the original image and retrieve resolution
function displayOriginalImage(imageID) {
  var image = ee.Image(imageID);
  var resolution = image.select('B4').projection().nominalScale();
  print('Resolution (meters):', resolution.getInfo());
  Map.addLayer(image, {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000}, 'Original Image');
}

// Function to display the enhanced image
function displayEnhancedImage(imageID) {
  // Load the image
  var singleImage = ee.Image(imageID);

  // Visualize the image with bands and adjusted parameters
  var enhancedImage = singleImage.visualize({
    bands: ['B2', 'B3', 'B4'],  // Blue, Green, Red bands
    min: 0,
    max: 3000,  // Adjusted max value for brightness and contrast
    gamma: 1.5  // Adjusted gamma for contrast
  });

  // Display the enhanced image
  Map.addLayer(enhancedImage, {}, 'Enhanced Image');
}

// Function to display the grayscale negative image
function displayGrayscaleNegativeImage(imageID) {
  // Load the image
  var singleImage = ee.Image(imageID);

  // Convert image to grayscale using the NIR band (B8)
  var grayscaleImage = singleImage.select('B8').visualize({
    min: 0,
    max: 3000,
    palette: ['white', 'black']  // Inverted palette for negative effect
  });

  // Display the grayscale image
  Map.addLayer(grayscaleImage, {}, 'Grayscale Negative Image');
}

// Define the image ID
var imageID = '# Enter image_name here';

//put image name here after last "/"

// Call the functions to display the layers and retrieve resolution
displayOriginalImage(imageID);
displayEnhancedImage(imageID);
displayGrayscaleNegativeImage(imageID);

// Center the map on the image
var image = ee.Image(imageID);
Map.centerObject(image, 10);
```

## The user should then manually search each image for their object of interest.
** Unfortunately, our team was unable to find a model that can differentiate between ocean, waves, and clouds from an anomaly. Models such as these may exist, and the user is encouraged to try to find them, as manually searching these large images can take an extensive amount of time.**


## The user should manually copy and paste the image name of positive identificaitons of the object of interest into a separate excel file named "positive_IDs" into a column named "image_ids", and download the python file named "positive_IDs.py" found in this branch.


## This script will then only download the images you listed in that excel file

### Mount Google Drive and load the Excel file

```python
from google.colab import drive
import pandas as pd

# Mount Google Drive
drive.mount('/content/drive')

# Path to the Excel file in your Drive
excel_path = '/content/drive/MyDrive/positive_IDs.xlsx'

# Load the Excel file and get the "image_ID" column
df = pd.read_excel(excel_path, sheet_name=0)  # Adjust sheet_name if needed
image_ids = df['image_ID'].dropna().tolist()  # Ensure no empty rows

print(f"Loaded {len(image_ids)} positive image IDs from the Excel file.")
```

### Define a function to export images

```python
def export_image(image_id, folder_name="Sentinel2_Exports"):
    """
    Export a Sentinel-2 image to Google Drive.
    Args:
        image_id (str): The ID of the image to export.
        folder_name (str): The folder name in Google Drive where the images will be saved.
    """
    try:
        # Load the image by its ID
        image = ee.Image(image_id)
        
        # Export task parameters
        task = ee.batch.Export.image.toDrive(
            image=image,
            description=f"Export_{image_id.split('/')[-1]}",
            folder=folder_name,
            fileNamePrefix=image_id.split('/')[-1],
            scale=10,  # Adjust resolution if needed
            region=image.geometry().bounds().getInfo()['coordinates'],  # Export the entire image
            maxPixels=1e13  # Set a large limit for pixel exports
        )
        
        # Start the export task
        task.start()
        print(f"Export started for image ID: {image_id}")
    except Exception as e:
        print(f"Error processing image ID {image_id}: {e}")
```

### Process all image IDs from the positive_IDs.xlsx

```python
# Define the Google Drive folder name where the exports will be saved
export_folder = "Sentinel2_Exports"

# Process each image ID from positive_IDs.xlsx
for image_id in image_ids:
    export_image(image_id, folder_name=export_folder)
```
