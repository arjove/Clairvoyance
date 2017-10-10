#!/usr/bin/env python
from parser import parse
from solver import solve
import puzzles
import sys


#TODO: laten werken als een gebied offline is

KML_FILE = "jotihunt-2016.kml"
PUZZLE = puzzles.tokyo_hotel

def banner():
	print("""  _______     _                                     
 / ___/ /__ _(_)____  _____  __ _____ ____  _______ 
/ /__/ / _ `/ / __/ |/ / _ \/ // / _ `/ _ \/ __/ -_)
\___/_/\_,_/_/_/  |___/\___/\_, /\_,_/_//_/\__/\__/ 
                           /___/                    
    """)

def main():
	banner()
	sys.stdout.flush()

	polygons = parse(KML_FILE)
	solve(PUZZLE, polygons)

if __name__ == "__main__":
	main()