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


## The user should manually copy and paste the image name of positive identificaitons of the object of interest into a separate excel csv file named "positive_IDs" into a column named "image_ID".

Only have the 1 column in this csv file. Open the csv file in a notepad app to make sure there are no hidden characters (usually commas).

## Upload "positive_IDs.csv" as an asset in Google Earth Engine.

1. Open your project in GEE code editor.
2. Click on the "Assets" tab on the left-hand side.
3. Click on "New".
4. Click on "CSV file .csv".
5. Upload "positive_IDs.csv"
6. Click on the "Task" tab on the righ-hand side to make sure the upload is successful.

## Enter this code into the middle script terminal to export the images as GEOTIFFS into a folder named "Sentinel2_Exports_Positive":

```javascript
// Step 1: Load the uploaded table (positive_IDs) as a FeatureCollection
var imageIdsTable = ee.FeatureCollection('projects/YOUR USERNAME/assets/positive_IDs');  // ENTER YOUR USER NAME

// Step 2: Define the export function for each image ID
function exportImage(imageId) {
  // Load the image using the image ID (Assuming it's from Sentinel-2 Surface Reflectance)
  var image = ee.Image('COPERNICUS/S2_SR/' + imageId);  // Replace with the correct image collection if needed

  // Ensure all bands have a consistent data type (e.g., casting to UInt16)
  image = image.toInt16();  // Cast all bands to Int16 (or use toByte() if you prefer Byte)

  // Define export parameters
  Export.image.toDrive({
    image: image,
    description: imageId,
    folder: 'Sentinel2_Exports_Positive',  // The folder in Google Drive
    fileNamePrefix: imageId,  // Set the file name prefix for the GeoTIFF
    scale: 10,  // Resolution (in meters), adjust according to your dataset
    crs: 'EPSG:4326',  // Coordinate Reference System
    fileFormat: 'GeoTIFF',  // Output format
    maxPixels: 1000000000  // Set a higher maxPixels value (1 billion pixels in this case)
  });
}

// Step 3: Iterate over the image IDs in the FeatureCollection and export the images
imageIdsTable.aggregate_array('image_ID').evaluate(function(imageIds) {
  imageIds.forEach(function(imageId) {
    // Call the export function for each image ID
    exportImage(imageId);
  });
});
```

You will then need to open the "Tasks" tab on the right-hand side and click "RUN" next to each image. This will take several hours to complete.
