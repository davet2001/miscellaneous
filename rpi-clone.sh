#!/bin/bash
# Helper script for running rpi clone
# Works out where the SD_MMC is, and targets rpi-clone there.
#
# I always want to write my clone to the SD card connected via USB.  
# I never want to accidentally clone to (and therefore overwrite) data 
# storage drives e.g /dev/sda1, /dev/sda2.
# I want to run rpi-clone regularly without worrying that random
# drive letter reassignment one day causes loss of important data.
#
# Dave Thompson 14/6/2020 

echo "Looking for SD_MMC amongst connected /dev/sd* devices..."
for entry in /dev/sd?
do
  echo " trying $entry..."
  if udevadm info $entry | grep -q ID_MODEL=SD_MMC; then
    sdcard=$entry
  fi
done 	

echo SD card found at $sdcard.

sudo rpi-clone $sdcard
