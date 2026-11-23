# -*- coding: utf-8 -*-

"""Top-level package for ROTLA."""

__author__ = """Christopher Andrew Lavender, Adam Burkholder"""
__email__ = 'c.andrew.lavender@gmail.com, adam.burkholder@nih.gov'
__version__ = '2.0.1'

import configparser
import os


def blat_path() -> str:
    """BLAT executable: $ROTLA_BLAT, then [paths] blat in paths.cfg (package or ../config), then "blat" on PATH."""
    if os.environ.get("ROTLA_BLAT"):
        return os.environ["ROTLA_BLAT"]
    here = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read([os.path.join(here, "..", "config", "paths.cfg"), os.path.join(here, "..", "paths.cfg")])
    return config.get("paths", "blat", fallback="blat")
