# config.py
"""
Configuration constants for Aeroponic Optimizer
"""

# Default Greenhouse Dimensions
DEFAULT_DIMENSIONS = {
    "length": 20.0,
    "width": 11.0,
    "height": 4.0,
    "tech_zone": 2.5,
    "basin_diameter": 0.77
}

# Spacing & Layout Ranges
SPACING_RANGES = {
    "dist_x": {"min": 0.1, "max": 0.6, "default": 0.33},
    "dist_y": {"min": 0.1, "max": 0.8, "default": 0.5},
    "corridor": {"min": 0.8, "max": 2.0, "default": 1.2}
}

# pH & EC Control Defaults
PH_EC_DEFAULTS = {
    "ph_live": 7.2,
    "ec_live": 0.8,
    "ph_target": (5.9, 6.5),
    "ph_range": {"min": 4.0, "max": 9.0},
    "ec_target": (1.2, 1.6),
    "ec_range": {"min": 0.5, "max": 3.0},
    "tank_volume": 700
}

# UI Color Scheme
COLOR_SCHEME = {
    "active": "#2ecc71",
    "inactive": "#bdc3c7",
    "warning": "#e74c3c",
    "info": "#3498db",
    "success": "#27ae60"
}

# Validation Constraints
VALIDATION = {
    "min_length": 5.0,
    "min_width": 3.0,
    "min_height": 2.0
}

# Plants per Tower
PLANTS_PER_TOWER = 52
