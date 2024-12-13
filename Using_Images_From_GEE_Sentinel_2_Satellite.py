import os
import pandas as pd
import ee
from datetime import datetime

# Initialize Google Earth Engine
ee.Initialize()

# Define the region of interest (ROI) as a polygon (editable latitude/longitude coordinates)
# Example: define the coordinates for a bounding box (change these to your region of interest)
region = ee.Geometry.Polygon(
    [[[-122.6, 37.6],
      [-122.6, 37.8],
      [-122.4, 37.8],
      [-122.4, 37.6]]])  # Modify the coordinates here

# Define the date range (editable, e.g., March, April, May)
start_date = '2022-03-01'
end_date = '2022-05-31'

# Define the output directory to save the results
output_directory = "/path/to/output/directory"  # Change this to where you want the output file to be saved

# Filter the Sentinel-2 imagery based on the defined region and date range
sentinel_collection = ee.ImageCollection('COPERNICUS/S2') \
    .filterBounds(region) \
    .filterDate(start_date, end_date) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))  # Optionally filter by cloud cover

# Extract metadata from the filtered image collection
image_list = sentinel_collection.toList(sentinel_collection.size())  # Convert to list
image_metadata = []

for i in range(image_list.size().getInfo()):
    image = ee.Image(image_list.get(i))
    date = image.get('system:time_start').getInfo()
    date = datetime.utcfromtimestamp(date / 1000).strftime('%Y-%m-%d')  # Convert from timestamp to date

    # Add the metadata to the list
    image_metadata.append({'Image ID': image.id().getInfo(), 'Date': date})

# Create a DataFrame and save to Excel
google_images_df = pd.DataFrame(image_metadata)

# Save filtered Google images metadata to a new Excel sheet
output_file = os.path.join(output_directory, "google_images_statistically_likely.xlsx")
print(f"Writing output file: {output_file}")

# Write the DataFrame to an Excel file
with pd.ExcelWriter(output_file) as writer:
    google_images_df.to_excel(writer, sheet_name='Google Images Statistically Likely', index=False)

print(f"The new Excel file with the images taken in March, April, and May has been created at {output_file}")

