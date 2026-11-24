#!/usr/bin/env python3
"""Complete the integration power-cut row after an earlier comparison failure."""
import pathlib,subprocess,sys
r=pathlib.Path(__file__).resolve().parent.parent
lab=[sys.executable,str(r/'lab.py')]
try:
    subprocess.run(lab+['new','bc1-integration-cut','stand'],check=True)
    subprocess.run([sys.executable,str(r/'build/powercut.py'),'bc1-integration-cut'],check=True)
finally:
    subprocess.run(lab+['destroy','bc1-integration-cut'],check=True)
