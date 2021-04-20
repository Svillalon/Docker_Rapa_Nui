#!/bin/bash

# Run backtrayectory simulations in hysplit for Rapa Nui
# For each sounding launched in rapa nui between 1995 and 2019, 
# backtrajectories are simulated at the date and time of the 
# survey launch. The backtrajectories are calculated for 7 days
# at 3 heights: 4000, 8000 and 12000 m relative mean sea level.
# NCEP/NCAR reanalysis are used to run hysplit.
# One file per sounding and height is created.
# This requires RapaNui_DatesStr_hysplit.csv, that contains sounding
# datetimes.
# This code requires that hysplit is installed in Linux.
# https://www.ready.noaa.gov/HYSPLIT.php

  # Set directories in that works
  path_rapanui="${PWD}"
  path_hysplit="${HOME}/hysplit.v5.0.0_Ubuntu"
  path_work="${path_hysplit}/working"
  file_dates="${path_rapanui}/RapaNui_DatesStr_hysplit.csv"
  
  # Enter to working directory
  cd ${path_work}



  # Set model simulation variables 
  # Range of year to simulate. Initial year(yri), Final year (yrf)
  yri=2019
  yrf=2019
    
  # Latitude and longitude of origin
  olat=-27.17
  olon=-109.42
  
  # Number of trayectories
  ntraj=1
  
  # Hours of simulation
  run=-168
  
  # Vertical movement that hysplit use
  vertmov=0
  
  # Highest height in hysplit
  ztop=20000.0
  
  # Meteorology files to use. 
  # Number of files
  nmet=1
  # Folder that contains the files
  fold_met="${path_rapanui}/ARL_data"
  # File name
  file_met="RP${yri}-${yrf}.ARL"
  
  # Output folder where to save the trajectories
  path_out="${path_rapanui}/Trajec"
  
  
  # Make SETUP.CFG in working directory. Set height unit input (kmsl)
  # and output (kagl) to meters relative to mean sea level
  kmsl=1
  kagl=0
  
  # Make SETUP.CFG
  echo "&SETUP              "  >SETUP.CFG
  echo "kmsl = ${kmsl},     " >>SETUP.CFG
  echo "kagl = ${kagl},     " >>SETUP.CFG
  echo "/                   " >>SETUP.CFG
  

  # Run backtrayectory simulation
  # Calculate number of soundings
  n=`cat $file_dates | awk '{print NR}' | tail -1`
  for i in $(seq 1 $n)
  do
	# Read RapaNui_DatesStr_hysplit.csv and read year(y), month(m),
	# day(d) and hour(h) for every sounding
	y=`cat $file_dates | awk '{if (NR=='$i') print $1}'`
	m=`cat $file_dates | awk '{if (NR=='$i') print $2}'`
	d=`cat $file_dates | awk '{if (NR=='$i') print $3}'`
	h=`cat $file_dates | awk '{if (NR=='$i') print $4}'`


	# Create year in format #YYYY
	if [[ $((10#$y)) -ge 50 && $((10#$y)) -lt 100 ]]; then
		yy=$(( $((10#$y)) + 1900 ))
	else
		yy=$(( $((10#$y)) + 2000 ))
	fi


	# Run simulation if sounding date is between years yri and yrf
	if (( $yy >= $yri && $yy <= $yrf )); then	
		
		# Run for every height
		for lvl in 4000.0 8000.0 12000.0; do
		
			# Output file name
			file_out="RN_bt_${y}${m}${d}${h}_${lvl}"
			
			# Remove preexisting backtrayectory file
			rm -f ${path_out}/${file_out}
			
			# Make CONTROL.CFG. Namelist file for hysplit
			echo "$y $m $d $h         " >CONTROL
			echo "$ntraj              ">>CONTROL
			echo "$olat $olon $lvl    ">>CONTROL
			echo "$run                ">>CONTROL
			echo "$vertmov            ">>CONTROL
			echo "$ztop               ">>CONTROL
			echo "$nmet               ">>CONTROL
			echo "${fold_met}/        ">>CONTROL
			echo "$file_met           ">>CONTROL
			echo "${path_out}/        ">>CONTROL
			echo "$file_out           ">>CONTROL
			
			
			# Run hysplit with CONTROL and SETUP files
			echo "Z0 ${lvl}, T0 ${y}/${m}/${d}T${h}"
			${path_hysplit}/exec/hyts_std
		
		done
	fi
  done
