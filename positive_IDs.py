import openpyxl
import ee
import sys

# Initialize Earth Engine API
ee.Initialize()

# Function to read image IDs from the provided Excel file
def read_image_ids(excel_file, sheet_name='images_of_interest'):
    # Open the Excel file
    wb = openpyxl.load_workbook(excel_file)
    
    # Select the desired sheet
    sheet = wb[sheet_name]
    
    # Extract image IDs from the "image_name" column (assuming it's in the first column)
    image_ids = []
    for row in sheet.iter_rows(min_row=2, max_col=1, values_only=True):
        image_ids.append(row[0])
    
    return image_ids

# Function to display and export images from GEE
def process_images(image_ids):
    for image_id in image_ids:
        try:
            print(f"Processing image: {image_id}")

            # Load the image from GEE
            image = ee.Image(image_id)
            
            # Get the resolution of the image (example with B4 band for resolution)
            resolution = image.select('B4').projection().nominalScale().getInfo()
            print(f"Resolution (meters) for {image_id}: {resolution}")
            
            # Display the original image
            Map.addLayer(image, {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}, 'Original Image')
            
            # Export the image to Google Drive
            export_task = ee.batch.Export.image.toDrive(
                image=image,
                description=f"Export_{image_id}",
                fileNamePrefix=f"{image_id}",
                scale=10,  # Change this based on desired resolution
                region=image.geometry(),  # Use the image's geometry as the region
                fileFormat='GeoTIFF'
            )
            export_task.start()  # Start the export task
            print(f"Exporting {image_id} to Google Drive...")

        except Exception as e:
            print(f"Error processing {image_id}: {e}")

# Main function to orchestrate the process
def main():
    # Check if the user passed the file path as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_excel_file>")
        sys.exit(1)

    # Get the file path from the command line argument
    excel_file = sys.argv[1]
    
    # Read the image IDs from the Excel file
    image_ids = read_image_ids(excel_file)
    
    # Process and download images from GEE
    process_images(image_ids)

# Run the main function
if __name__ == "__main__":
    main()
