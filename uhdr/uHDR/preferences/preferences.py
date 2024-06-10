# uHDR: HDR image editing software
#   Copyright (C) 2021  remi cozot 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# hdrCore project 2020
# author: remi.cozot@univ-littoral.fr

# -----------------------------------------------------------------------------
# --- Package preferences -----------------------------------------------------
# -----------------------------------------------------------------------------
"""
Package preferences contains all global variables that setup the preferences.
"""

# -----------------------------------------------------------------------------
# --- Import ------------------------------------------------------------------
# -----------------------------------------------------------------------------
import numpy as np
import json
import os
from pathlib import Path

# -----------------------------------------------------------------------------
# --- Preferences -------------------------------------------------------------
# -----------------------------------------------------------------------------
target = ['python', 'numba', 'cuda']
computation = target[0]
# verbose mode: print function call 
# useful for debug
verbose = True
# list of HDR displays taken into account
# read from prefs.json file
# display info:
# "vesaDisplayHDR1000": << display tag name
# {
# "shape": [2160, 3840], << display shape (4K)
# "scaling": 12, << color space scaling to max
# "post": "_vesa_DISPLAY_HDR_1000", << postfix add when exporting file
# "tag": "vesaDisplayHDR1000" << tag name
# }
HDRdisplays = None
# current HDR display: tag name in above list
HDRdisplay = None
# image size when editing image: 
# small size = quick computation, no memory issues
maxWorking = 1200
# last image directory path
imagePath = "."
# keep all metadata
keepAllMeta = False

# -----------------------------------------------------------------------------
# --- Functions preferences --------------------------------------------------
# -----------------------------------------------------------------------------
def loadPref(): 
    """Load preferences file: prefs.json

    Args:

    Returns (Dict)
    """
    prefs_path = Path('./prefs.json').resolve()
    if prefs_path.is_file():
        with prefs_path.open() as f:
            return json.load(f)
    else:
        print(f"Preferences file not found: {prefs_path}")
        return None

def savePref():
    global HDRdisplays
    global HDRdisplay
    global imagePath
    pUpdate = {
        "HDRdisplays": HDRdisplays,
        "HDRdisplay": HDRdisplay,
        "imagePath": imagePath
    }
    if verbose:
        print(" [PREF] >> savePref(", pUpdate, ")")
    prefs_path = Path('./prefs.json').resolve()
    with prefs_path.open("w") as f:
        json.dump(pUpdate, f)

# -----------------------------------------------------------------------------
# --- Loading preferences -----------------------------------------------------
# -----------------------------------------------------------------------------
print("uHDRv6: loading preferences")
p = loadPref()
if p:
    HDRdisplays = p["HDRdisplays"]
    HDRdisplay = p["HDRdisplay"]
    imagePath = p["imagePath"]
else:
    HDRdisplays = {
        'none': {'shape': (2160, 3840), 'scaling': 1, 'post': '', 'tag': "none"},
        'vesaDisplayHDR1000': {'shape': (2160, 3840), 'scaling': 12, 'post': '_vesa_DISPLAY_HDR_1000', 'tag': 'vesaDisplayHDR1000'},
        'vesaDisplayHDR400': {'shape': (2160, 3840), 'scaling': 4.8, 'post': '_vesa_DISPLAY_HDR_400', 'tag': 'vesaDisplayHDR400'},
        'HLG1': {'shape': (2160, 3840), 'scaling': 1, 'post': '_HLG_1', 'tag': 'HLG1'}
    }
    # current display
    HDRdisplay = 'vesaDisplayHDR1000'
    imagePath = '.'
print(f"       target display: {HDRdisplay}")
print(f"       image path: {imagePath}")

# -----------------------------------------------------------------------------
# --- Functions computation ---------------------------------------------------
# -----------------------------------------------------------------------------
def getComputationMode():
    """Returns the preference computation mode: python, numba, cuda, ...

    Args:

    Returns (str)
    """
    return computation

# -----------------------------------------------------------------------------
# --- Functions HDR display ---------------------------------------------------
# -----------------------------------------------------------------------------
def getHDRdisplays():
    """Returns the current display model

    Args:

    Returns (Dict)
    """
    return HDRdisplays

def getHDRdisplay():
    """Returns the current display model

    Args:

    Returns (Dict)
    """
    return HDRdisplays[HDRdisplay]

def setHDRdisplay(tag):
    """Set the HDR display

    Args:
        tag (str): tag of HDR display, must be a key of HDRdisplays

    Returns:
    """
    global HDRdisplay
    if tag in HDRdisplays:
        HDRdisplay = tag
    savePref()

def getDisplayScaling():
    return getHDRdisplay()['scaling']

def getDisplayShape():
    return getHDRdisplay()['shape']

# -----------------------------------------------------------------------------
# --- Functions path ----------------------------------------------------------
# -----------------------------------------------------------------------------
def getImagePath():
    return imagePath if os.path.isdir(imagePath) else '.'

def setImagePath(path):
    global imagePath
    imagePath = path
    if verbose:
        print(" [PREF] >> setImagePath(", path, "):", imagePath)
    savePref()
