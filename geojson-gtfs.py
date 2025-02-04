import json
import csv

# Specify the path to your GeoJSON file
geojson_file_path = 'geojson/TPUJ_4A_BP05_OUT_NIGHT.geojson'  # Assuming the file is in the same folder

# Load the GeoJSON data
with open(geojson_file_path, 'r') as geojson_file:
    geojson_data = json.load(geojson_file)

# Open the output shapes.csv file for writing (change extension to .csv)
with open('shapes.csv', 'w', newline='') as csvfile:
    fieldnames = ['shape_id', 'shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header to shapes.csv
    writer.writeheader()

    # Define the sequence counter
    sequence = 1

    # Handle multiple routes (if available in GeoJSON)
    if isinstance(geojson_data, dict) and 'geometry' in geojson_data:
        # If it's a single route feature
        shape_id = "TPUJ_4A_BP05"  # Single route with ID JP101 (this will be constant for this route)
        coordinates = geojson_data['geometry']['coordinates']
        for coord in coordinates:
            lon, lat = coord  # GeoJSON is [lon, lat] format
            writer.writerow({
                'shape_id': shape_id,
                'shape_pt_lat': lat,
                'shape_pt_lon': lon,
                'shape_pt_sequence': sequence
            })
            sequence += 1
    elif isinstance(geojson_data, dict) and 'features' in geojson_data:
        # If it's a FeatureCollection (multiple routes)
        for feature in geojson_data['features']:
            shape_id = feature['properties'].get('route_id', 'UNKNOWN_ROUTE')  # Use route_id or any property for shape_id
            coordinates = feature['geometry']['coordinates']
            for coord in coordinates:
                lon, lat = coord
                writer.writerow({
                    'shape_id': shape_id,
                    'shape_pt_lat': lat,
                    'shape_pt_lon': lon,
                    'shape_pt_sequence': sequence
                })
                sequence += 1
    else:
        print("GeoJSON data structure is unexpected.")
