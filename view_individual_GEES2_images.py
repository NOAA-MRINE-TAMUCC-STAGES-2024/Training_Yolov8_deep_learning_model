import ee
import pandas as pd

# Authenticate with GEE
ee.Initialize()

# Load the Excel sheet containing image names (image IDs)
excel_file_path = 'Google_Images_Statistically_Likely.xlsx'  # Change to your file path
df = pd.read_excel(excel_file_path)

# Extract image IDs from the 'image_name' column
image_ids = df['image_name'].tolist()

# Function to display the original image and retrieve resolution
def display_original_image(image_id):
    image = ee.Image(image_id)
    resolution = image.select('B4').projection().nominalScale()
    print(f"Resolution (meters) for {image_id}: {resolution.getInfo()}")
    # Add to the map for visualization (optional if using GEE interactive environment)
    Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'Original Image')

# Function to display the enhanced image
def display_enhanced_image(image_id):
    image = ee.Image(image_id)
    enhanced_image = image.visualize({
        'bands': ['B2', 'B3', 'B4'],
        'min': 0,
        'max': 3000,
        'gamma': 1.5
    })
    # Add to the map for visualization (optional if using GEE interactive environment)
    Map.addLayer(enhanced_image, {}, 'Enhanced Image')

# Function to export the image to Google Drive
def export_image(image_id, export_name):
    image = ee.Image(image_id)
    export = ee.batch.Export.image.toDrive(
        image=image,
        description=export_name,
        scale=10,
        region=image.geometry(),
        fileFormat='GeoTIFF',
        folder='GEE_Export_Folder'  # Optional: Specify the Google Drive folder
    )
    export.start()

# Loop through each image ID and process it
for image_id in image_ids:
    print(f"Processing image: {image_id}")
    display_original_image(image_id)
    display_enhanced_image(image_id)
    export_image(image_id, f"Export_{image_id.split('/')[-1]}")  # Export with the image's ID


