#!/usr/bin/env python3
"""Print the routes script (ROUTES_SH) of the given `run`. Usage: extract-routes.py PATH-OF-run"""
import importlib.machinery
import sys
R = importlib.machinery.SourceFileLoader('runmod', sys.argv[1]).load_module()
sys.stdout.write(R.ROUTES_SH)
