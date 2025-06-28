import numpy as np
import matplotlib.pyplot as plt
import cmd
import geopandas as gpd
from shapely.geometry import box
from rasterio import features
from rasterio.plot import show
from rasterio.enums import MergeAlg
from numpy import int16

# === Step 1: Generate synthetic raster and vector data ===
width, height = 100, 100
raster_shape = (height, width)
transform = (1, 0, 0, 0, -1, height)  # Affine-like tuple for simplicity

# Synthetic vector data — 2 rectangles (polygons)
geoms = [
    box(10, 10, 40, 40),  # rectangle 1
    box(50, 50, 90, 90),  # rectangle 2
]

vector = gpd.GeoDataFrame({'geometry': geoms})
vector['id'] = range(len(vector))

# Create (geometry, value) pairs
geom_value = ((geom, val) for geom, val in zip(vector.geometry, vector['id']))

# === Step 2: Rasterize the vector data ===
rasterized = features.rasterize(
    geom_value,
    out_shape=raster_shape,
    transform=transform,
    all_touched=True,
    fill=-1,
    merge_alg=MergeAlg.replace,
    dtype=int16
)

# === Step 3: Visualization helper ===
def render_raster(data, title="Piyo Raster Output"):
    fig, ax = plt.subplots(figsize=(6, 6))
    show(data, ax=ax, title=title)
    ax.invert_yaxis()
    plt.show()

# === Step 4: CLI shell ===
class PiyoShell(cmd.Cmd):
    intro = "Welcome to Piyo vGPU CLI\nType 'help' or 'render' to begin."
    prompt = "(piyo) "

    def do_exit(self, arg):
        "Exit shell."
        print("Shutting down Piyo...")
        return True

    def do_render(self, arg):
        "Render current raster buffer."
        render_raster(rasterized)

    def do_debug(self, arg):
        "Print raster array (for dev debugging)."
        print(rasterized)

if __name__ == "__main__":
    PiyoShell().cmdloop()
