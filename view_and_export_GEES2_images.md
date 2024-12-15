# **This file contains instructions to view individual satellite images in Google Earth Engine, then save images of interest as a GEOTIFF file.**

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

## The user should then scan the image for their object of interest.

If there is an object of interest within the picture, use the geometry tools on GEE, and draw a shape around your object. Make sure there is a sufficient amount of background around the object, so that the AI model and differentiate the object from its environment.

An import tab will then pop up at the top of the terminal. Click on the icon next to it that looks like a document.

A tab will open listing the code affiliated with your polygon, copy it.

## The user should then open a new file in GEE and copy the following code.

The user will need to paste the geometry code to replace the part of the below code containing "var roi = ", and the image name where it says "positive_ID = "

This code will save the clipped image within the polygon the user drew around the object of interest into a folder in their Google Drive named "Sentinel2_Exports_Positive"

```javascript
// Assuming you've drawn the ROI and it's saved as `geometry` in Earth Engine
var roi = 
    ee.Geometry.Polygon(
        [[[-81.20831835725136, 28.510943136677486],
          [-81.20831835725136, 28.494650801415403],
          [-81.17613184907265, 28.494650801415403],
          [-81.17613184907265, 28.510943136677486]]], null, false);  // Use the variable containing your drawn region

Positive_ID = 20200324T155911_20200324T160549_T17RMM //  Input your image_ID

// Function to display the original image and retrieve resolution
function displayOriginalImage(imageID) {
  var image = ee.Image(imageID);
  var resolution = image.select('B4').projection().nominalScale();
  print('Resolution (meters):', resolution.getInfo());

  // Clip the image to the ROI (Region of Interest)
  var clippedImage = image.clip(roi); // Clip using the drawn ROI

  // Cast all bands to UInt16 to ensure consistent data type
  clippedImage = clippedImage.select(['B4', 'B3', 'B2']).toUint16();

  // Add the clipped image to the map for visualization
  Map.addLayer(clippedImage, {bands: ['B4', 'B3', 'B2'], min: 0, max: 3000}, 'Original Image (Clipped)');

  // Export the clipped image as GeoTIFF
  Export.image.toDrive({
    image: clippedImage,
    description: 'Positive_ID',
    folder: 'Sentinel2_Exports_Positive',  // Folder name in Google Drive
    fileNamePrefix: 'Positive_ID',
    scale: 10,  // Resolution (in meters)
    crs: 'EPSG:4326',  // Coordinate Reference System
    fileFormat: 'GeoTIFF',  // Output format
    maxPixels: 1000000000  // Set a higher maxPixels value (1 billion pixels in this case)
  });
}

// Define the image ID
var imageID = 'COPERNICUS/S2_SR/20200324T155911_20200324T160549_T17RMM';

// Call the function to display and export the original image
displayOriginalImage(imageID);

// Center the map on the ROI (Region of Interest)
Map.centerObject(roi, 10);  // Centering the map on the ROI

```
