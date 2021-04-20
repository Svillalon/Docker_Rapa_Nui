#!/bin/bash

# Download data NCEP-NCAR Reanalysis in format .ARL for hysplit
# Download data from ftp://ftp.arl.noaa.gov/pub/archives/reanalysis/
# between 2 years, yri and yrf, month by month. Every file per month is
# "RP${yr}${mo}.gbl", where yr is year and mo is month.
# Concatenate all files per month in one file .ARL: "RP${yri}-${yrf}.ARL"


# Path that contains .ARL files
ruta_actual=${PWD}
OUT="${ruta_actual}/ARL_data/"

# Set range of years
yri=2019
yrf=2019

# File name that contains all data
fileout="RP${yri}-${yrf}.ARL"

# Enter to folder OUT
cd $OUT
echo "### $0 ###"

# Remove file exists
rm -f $fileout

# Run for year
for yr in $(seq ${yri} ${yrf})
do
	# Run for month
	for mo in {01..12}
	do
	
	# File name to download
	data="RP${yr}${mo}.gbl"
	
	# If doesn't exist file, then download it
	if [ ! -f "$data" ]; then
    		echo "$data does not exist."
    		wget ftp://ftp.arl.noaa.gov/pub/archives/reanalysis/$data
    	else
    		echo "$data exists."
	fi
	
	# Concatenate file to unique file
	cat $data >> $fileout
	
	done
done
