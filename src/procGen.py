#!/usr/bin/python3

# procGen.py - Script, collecting processed and diagnostic data to CSV files
#
# Copyright 2023 Patrizia Favaron
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import glob

if __name__ == "__main__":

    # Read command-line parameters
    if len(sys.argv) != 5:
        print("procGen.py - Program for collecting sonic processed data\n")
        print("Usage:\n")
        print("  ./procGen.py <Data_Path> <Year> <Processed_File> <Diagnostic_File>\n")
        print("Copyright 2024 by Servizi Territorio srl")
        print("                  All rights reserved\n")
        print("Written by: Patrizia Favaron\n")
        sys.exit(1)
    path_name = sys.argv[1]
    try:
        year  = int(sys.argv[2])
    except:
        print("Invalid year: " + sys.argv[2])
        sys.exit(2)
    proc_file = sys.argv[3]
    diag_file = sys.argv[4]

    # Iterate over sub-directories, searching for this year's subdirs
    search_mask = os.path.join(path_name, "processed", "*")
    possible_dirs = sorted(glob.glob(search_mask))
    plausible_dirs = []
    for dir in possible_dirs:
        if os.path.isdir(dir):
            base_dir = os.path.basename(dir)
            if len(base_dir) == 6:
                try:
                    year_dir = int(base_dir[0:4])
                    month_dir = int(base_dir[4:])
                    if year_dir == year:
                        plausible_dirs.append(dir)
                except:
                    Pass

    # Check some subdir exists
    if len(plausible_dirs) <= 0:
        print("No data to cope with")
        sys.exit(3)

    # Search for processed data, and process them
    print("About to load processed data")
    is_first = True
    processed = []
    for dir in plausible_dirs:
        search_mask = os.path.join(dir, "*p")
        processed_files = sorted(glob.glob(search_mask))
        for in_file in processed_files:
            print(in_file)
            f = open(in_file, "r")
            lines = f.readlines()
            f.close()
            if is_first:
                for line in lines:
                    processed.append(line)
                is_first = False
            else:
                for line_idx in range(1, len(lines)):
                    processed.append(lines[line_idx])

    # Iterate over sub-directories, searching for this year's subdirs
    search_mask = os.path.join(path_name, "diagnostic", "*")
    possible_dirs = sorted(glob.glob(search_mask))
    plausible_dirs = []
    for dir in possible_dirs:
        if os.path.isdir(dir):
            base_dir = os.path.basename(dir)
            if len(base_dir) == 6:
                try:
                    year_dir = int(base_dir[0:4])
                    month_dir = int(base_dir[4:])
                    if year_dir == year:
                        plausible_dirs.append(dir)
                except:
                    Pass

    # Check some subdir exists
    if len(plausible_dirs) <= 0:
        print("No data to cope with")
        sys.exit(4)

    # Search for processed data, and process them
    print("About to load diagnostic data")
    is_first = True
    diagnostic = []
    for dir in plausible_dirs:
        search_mask = os.path.join(dir, "*d")
        diagnostic_files = sorted(glob.glob(search_mask))
        for in_file in diagnostic_files:
            print(in_file)
            f = open(in_file, "r")
            lines = f.readlines()
            f.close()
            if is_first:
                for line in lines:
                    diagnostic.append(line)
                is_first = False
            else:
                for line_idx in range(1, len(lines)):
                    diagnostic.append(lines[line_idx])

    # Store data
    print("Store data")
    f = open(proc_file, "w")
    for line in processed:
        f.write(line)
    f.close()
    f = open(diag_file, "w")
    for line in diagnostic:
        f.write(line)
    f.close()
