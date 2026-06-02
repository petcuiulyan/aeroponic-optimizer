# utils.py
"""
Utility functions for Aeroponic Optimizer
"""
import streamlit as st
import logging
from config import VALIDATION, DEFAULT_DIMENSIONS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def initialize_session_state():
    """Initialize all session state variables with defaults"""
    defaults = {
        'active_auto': False,
        'ph_history': [],
        'ec_history': [],
        'ajustari_manuale': {}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
            logger.info(f"Initialized session state: {key}")


def validate_greenhouse_params(length, width, height):
    """
    Validate greenhouse dimensions against constraints.
    
    Args:
        length: Greenhouse length in meters
        width: Greenhouse width in meters
        height: Greenhouse height in meters
    
    Returns:
        bool: True if valid, False otherwise
    """
    if length <= 0 or width <= 0 or height <= 0:
        st.error("❌ Dimensiunile trebuie să fie pozitive")
        logger.warning(f"Invalid dimensions: L={length}, W={width}, H={height}")
        return False
    
    if length < VALIDATION["min_length"]:
        st.warning(f"⚠️ Lungime seră prea mică (minim {VALIDATION['min_length']}m)")
        logger.warning(f"Length below minimum: {length}")
    
    if width < VALIDATION["min_width"]:
        st.warning(f"⚠️ Lățime seră prea mică (minim {VALIDATION['min_width']}m)")
        logger.warning(f"Width below minimum: {width}")
    
    if height < VALIDATION["min_height"]:
        st.warning(f"⚠️ Înălțime seră prea mică (minim {VALIDATION['min_height']}m)")
        logger.warning(f"Height below minimum: {height}")
    
    return True


def get_default_values(key):
    """
    Get default value for a configuration key.
    
    Args:
        key: Configuration key
    
    Returns:
        Default value or None if not found
    """
    if key in DEFAULT_DIMENSIONS:
        return DEFAULT_DIMENSIONS[key]
    return None


def log_system_event(event_type, message):
    """
    Log system events with timestamp.
    
    Args:
        event_type: Type of event (info, warning, error)
        message: Event message
    """
    if event_type == "info":
        logger.info(message)
    elif event_type == "warning":
        logger.warning(message)
    elif event_type == "error":
        logger.error(message)
