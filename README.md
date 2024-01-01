# The MeteoFlux_Support repository

## In general

This repository contains scripts and programs supporting MeteoFlux Core V2 users to check quality of data and, more generally, using MeteoFlux Core V2 to its best posibilities.

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
