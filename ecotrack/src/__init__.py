"""
EcoTrack - Carbon Footprint Calculator and Tracker

An open-source tool to help individuals and organizations measure 
and reduce their carbon emissions.
"""

from .ecotrack import (
    EmissionEntry,
    CarbonCalculator,
    EcoTracker,
)

__version__ = "1.0.0"
__author__ = "EcoTrack Contributors"
__license__ = "MIT"

__all__ = [
    "EmissionEntry",
    "CarbonCalculator",
    "EcoTracker",
]
