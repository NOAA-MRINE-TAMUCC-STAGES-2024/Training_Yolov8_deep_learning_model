# How to view individual Sentinel 2 satellite images in GEE through the command line.


## Install the Necessary Python Libraries
```bash
pip install pandas
pip install geemap
pip install google-auth
pip install google-earth-engine
```

## Download the "view_individual_GEES2_images.py" python file found in this branch.


## Authenticate the Google Earth Engine (GEE) in the comand line
```bash
earthengine authenticate
```

This will guide you through the authentication process in your browser.

## Run the python script through the command line

```bash
#!/bin/bash

# Prompt for the path to the Excel file
echo "Enter the path to your Excel file:"
read excel_file_path

# Run the Python script with the specified Excel file
python process_images.py $excel_file_path
```

# Make the script Executable

```bash
chmod +x run_gee_process.sh
```

# Run the Script

```bash
./run_gee_process.sh
```


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

```bash
python positive_IDs.py "path/to/your/positive_IDs.xlsx"
```
 
