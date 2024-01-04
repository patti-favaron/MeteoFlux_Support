# The MeteoFlux_Support repository

## In general

This repository contains scripts and programs supporting MeteoFlux Core V2 users to check quality of data and, more generally, using MeteoFlux(R) Core V2 to its best posibilities.

The procedures are described in alphabetic order in the next sections.

All procedures are intended to be used under Linux. Use in other operating systems is possible, but it is the responsibility of users to read, understand the code and provide their own adaptations. I'd appreciate they star my repository and fork it, under the same MIT license. -- Patrizia

## 'rawExpand.py' script

The **rawExpand.py** script unzips raw ultrasonic data in place, without any processing.

To run the procedure, the following command is given from terminal in the directory where the script has been copied:

    ./rawExpand.py <Data_Path> <Year>

where

    <Data_Path>

represents the path name of the root data directory, for example

    /mnt/data

on a MeteoFlux Core V2 system. The directory may also reside somewhere else, for example on a USB disk where data have been copied during periodic maintenance.

The parameter

    <Year>

represents the year processing refers to: the procedure operates on a yearly basis, in order to contain computing time (Python is not renowned for speed).

## 'procGen.py' script

The **procGen.py** script aggregates hourly "processed" and "diagnostic" MeteoFlux(R) Core V2 data to individual files, in preparation of diagnostic data analysis, one of the site maintenance activities.

To run the procedure the following command line is used:

    ./procGen.py <Data_Path> <Year> <Processed_File> <Diagnostic_File>

where

    <Data_Path>

represents the path name of the root data directory, for example

    /mnt/data

on a MeteoFlux Core V2 system. The directory may also reside somewhere else, for example on a USB disk where data have been copied during periodic maintenance.

The parameter

    <Year>

represents the year processing refers to: the procedure operates on a yearly basis, in order to contain computing time (Python is not renowned for speed).

The parameters <Processed_File> and <Diagnostic_File> indicate the names of the processed and diagnostic aggregated files. These are distinct CSV text files, suitable to be read into dataframes, and used as input to the **checkSite.py** script.


## 'checkSite.py' script

The **checkSite.py** script gets aggregated MeteoFlux(R) Core V2 sonic processed data, as produced using procedure **procGen.py**, and builds a set of files useful during maintenance.

To run the procedure the following command line is used:

    ./checkSite.py <Processed_Data_File> <Out_Prefix>

where

    <Processed_Data_File>

is the pathname of the a file containing processed sonic data in MeteoFlux(R) Core V2 aggregated format, and

    <Out_Prefix>

a string which, concatenated on left to other strings, allows building actual output file names.

The file produced on successful exit are:

    <Out_Prefix>_BlindSpots.csv
    <Out_Prefix>_ObstructionIndex.csv
    <Out_Prefix>_Availability.txt
    <Out_Prefix>_H0.txt

The meaning and use of these files is given in MeteoFlux(R) Core V2 maintenance manual.
