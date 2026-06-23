"""
Configuration constants for Aeroponic Optimizer
"""

DEFAULT_DIMENSIONS = {
    "length": 20.0,
    "width": 11.0,
    "tech_zone": 2.5,
    "basin_diameter": 0.77
}

SPACING_RANGES = {
    "dist_x": {"min": 0.1, "max": 0.6, "default": 0.33},
    "dist_y": {"min": 0.1, "max": 0.8, "default": 0.5},
    "corridor": {"min": 0.8, "max": 2.0, "default": 1.2}
}
