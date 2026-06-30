import sys
import os

# Normalize paths and filter out the directory containing the bad pip.py
bad_dir = os.path.normpath("C:/Users/SAMIR AKHTAR/AppData/Local/Programs/Python/Python311")
sys.path = [p for p in sys.path if os.path.normpath(p) != bad_dir]

from pip._internal.cli.main import main
sys.argv = ['pip', 'install', '-r', 'requirements.txt']
sys.exit(main())
