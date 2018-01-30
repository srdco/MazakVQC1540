#!/usr/bin/env python

# Remap python file
# - used in remapping M codes (adapting behavior from default)
# - from Vismach/VMC_toolchange/remap.py
# - imports stdglue functions (copied into same folder as this file, 
#   & provides default prolog/epilog functions for the standard
#   remaps, e.g. M6)

from stdglue import *
