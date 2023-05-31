import numpy as np
from stl import mesh
import csv
import os
import glob

data = []

# Iterate over all directories in the specified path
for dir in glob.glob('models/ycb/*/'):
    # Extract the * part from the directory name
    file_part = os.path.split(dir[:-1])[1]  # The [:-1] removes the trailing '/'

    # Try to find the STL file in the google_16k directory
    filename_google = os.path.join(dir, 'google_16k/nontextured.stl')
    filename_poisson = os.path.join(dir, 'poisson/nontextured.stl')

    if os.path.isfile(filename_google):
        filename = filename_google
    elif os.path.isfile(filename_poisson):
        filename = filename_poisson
    else:
        continue  # Skip this directory if neither file exists

    # Load the STL file
    stlFile = mesh.Mesh.from_file(filename)

    # Find the min and max points for x, y, z
    minx, maxx = np.min(stlFile.v0[:, 0]), np.max(stlFile.v0[:, 0])
    miny, maxy = np.min(stlFile.v0[:, 1]), np.max(stlFile.v0[:, 1])
    minz, maxz = np.min(stlFile.v0[:, 2]), np.max(stlFile.v0[:, 2])

    width = maxx - minx
    depth = maxy - miny
    height = maxz - minz

    # Extract the * part from the filename
    file_part = os.path.split(os.path.split(os.path.split(filename)[0])[0])[1]

    data.append({'File': file_part, 'Width (m)': width, 'Height (m)': height, 'Depth (m)': depth})

# Sort the data by the 'File' field
data_sorted = sorted(data, key=lambda row: row['File'])

# Write the dimensions to a CSV file
with open('dimensions.csv', 'w', newline='') as csvfile:
    fieldnames = ['File', 'Width (m)', 'Height (m)', 'Depth (m)']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in data_sorted:
        writer.writerow(row)
