import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_3d_scatter(x_coords, y_coords, z_coords, color_values, title="3D Point Cloud",
                    color_label="Values", cmap='viridis', point_size=50, alpha=0.6):
    """
    Create and display a 3D scatter plot with color-coded values.

    Parameters:
    -----------
    x_coords : list or array
        X coordinates of points
    y_coords : list or array
        Y coordinates of points
    z_coords : list or array
        Z coordinates of points
    color_values : list or array
        Values to use for color mapping
    title : str, optional
        Title of the plot (default: "3D Point Cloud")
    color_label : str, optional
        Label for the colorbar (default: "Values")
    cmap : str, optional
        Matplotlib colormap name (default: 'viridis')
    point_size : int, optional
        Size of points (default: 50)
    alpha : float, optional
        Transparency of points, 0-1 (default: 0.6)
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Convert color values to numeric array (handles string input)
    color_values = np.array(color_values, dtype=float)

    # Create scatter plot with color mapping
    scatter = ax.scatter(x_coords, y_coords, z_coords,
                         c=color_values,
                         cmap=cmap,
                         marker='o',
                         s=point_size,
                         alpha=alpha)

    # Add labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Add colorbar
    colorbar = plt.colorbar(scatter, ax=ax, pad=0.1, shrink=0.8)
    colorbar.set_label(color_label)

    # Display
    plt.show()
