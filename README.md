# **This branch is to be used if the user is intending to use the open access satellite images on Google Earth Engine, from the Sentinel 2 sattellite.**

# *A list of images to view will be created in an excel file, using Google Colaboratory. The codes to view and export these images will be written directly into the terminal in Google Earth Engine. The user will need to have a cloud project set up to do this.*

# Use Case

Best for objects bigger than 10m. It is most commonly used for projects that deal with frequent monitoring, detailed spatial analysis, environmental changes, vegetation and land cover studies, and disaster management.

# Spatial and Temporal Resolution

## Spatial Resolution

### 10 meters per pixel for the following bands

B2 (Blue)
B3 (Green)
B4 (Red)
B8 (Near-Infrared)

The scripts provided in this GitHub use this spatial resolution, but it could be alterred to any of the below.


### 20 meters per pixel for the following bands

B5 (Vegetation Red Edge)
B6 (Vegetation Red Edge)
B7 (Vegetation Red Edge)
B8A (Narrow Near-Infrared)
B11 (Shortwave Infrared)
B12 (Shortwave Infrared)

### 60 meters per pixel for the following bands

B1 (Coastal Aerosol)
B9 (Water Vapor)

## Temporal Resolution

Sentinel-2 has a 5-day revisit cycle at the equator, but th eactual revisit time depends on the latitude, with higher latitudes having shorter revisit times.

# Geographic Range

Sentinel-2 has a global geographic range between the latitudes 82.0 N and 56.0 S

# Swath Width

Sentinel-2 has a 290 km swath width (the area observed during a single pass of the satellite), allowing it to cover large regions in each pass.

# **What order to open the files**

"Using_Images_From_GEE_Sentinel_2_Satellite.md" is the roadmap for using Google Colaboratory to create a list of Sentinel 2 images within the preferred spatial, and temporal ranges, as well as maximum cloud cover.
Next, the user will follow the instructions in "view_and_export_GEES2_Images" to view Sentinel 2 satellite images in Google Earth Engine, and save the images of interest into a folder on the users Google Drive.
