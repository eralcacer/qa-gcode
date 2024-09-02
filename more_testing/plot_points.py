import matplotlib.pyplot as plt
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, 'plot_points.txt')

# Lists to store x, y, and z coordinates
x_coords = []
y_coords = []
z_coords = []

# Read the file and extract coordinates
with open(file_path, 'r') as file:
    for line in file.readlines():
        # Assuming attributes are space-separated, adjust the delimiter accordingly
        line = line.strip('[] \n')
        line_list = [float(value) for value in line.split(',')]
        attributes = line_list
        # Extract the first three attributes as x, y, and z coordinates
        x_coords.append(float(attributes[0]))
        y_coords.append(float(attributes[1]))
        z_coords.append(float(attributes[2]))
# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_coords, y_coords, z_coords)

# Add labels for each point
for i, (x, y, z) in enumerate(zip(x_coords, y_coords, z_coords)):
    label = f'({x:.2f}, {y:.2f}, {z:.2f})'
    #ax.text(x, y, z, label, fontsize=8, ha='right', va='bottom')

# Set axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()
