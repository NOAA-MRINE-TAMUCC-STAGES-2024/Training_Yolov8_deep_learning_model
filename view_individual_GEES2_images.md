# ** This file contains instructions to view individual satellite images in Google Earth Engine, then save images of interest as a GEOTIFF file.

## Google Earth Engine does not allow users to download images from a separate website, so the images have to be individually called upon in the GEE coding platform.

The user should go to the GEE coding platform using this url: https://code.earthengine.google.com/

Then, the user can manually copy and paste the image_name into the following script, and scan the image through the GEE

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


## The user should manually copy and paste the image name of positive identificaitons of the object of interest into a separate excel csv file named "positive_IDs" into a column named "positive_IDs", and download the python file named "positive_IDs.py" found in this branch.


## This script will then download the images you listed in that excel file as a GEOTIFF file in your Google Drive.


