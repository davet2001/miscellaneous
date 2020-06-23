#!/bin/bash
#
# Simple script/one-liner to drive energenie 433MHz wirelss sockets.
# Dave T 23/6/2020
# 
# Problem:
# I wanted a wireless controlled socket that was reliable, and with a physical
# on/off button.  I'm not too bothered about someone malicious controlling it.
# (I know most of my neighbours, and I don't intend to use the sockets for 
# anything dangerous or sensitive).
# Energenie wireless sockets seem to be one of the cheapest in the UK
# that fits the bill.
# I had been using various other tools to drive them including ener314-RT
# connected to a raspberry pi. This is great except:
# - it uses lots of RPi pins
# - it doesn't fit inside a normal case
# - it's not very reliable (mqtt service that goes offline).
#
# Some of the newer (purple button) sockets allow connection to a MiHome
# hub and let you monitor on/off status and power consumption.
#
# Solution:
# I reverse engineered the energenie protocol using the excellent Universal
# Radio Hacker (URH) along with a <£5 RTL-SDR DVB receiver, and figured a 
# bash oneliner that can command the sockets without needing any extra 
# software/configs other than rpi-rf_send, connected to the cheapest (<£2) 
# 433MHz RF transmitter available from aliexpress.
#
# Protocol Description:
# Physical layer is 433.92MHz PWM encoded.  
# Each bit is encoded as 4 equal time slices about 230us:
# 1000 = 0
# 1110 = 1
# so 0xF0 appears as 1110 1110 1110 1110 1000 1000 1000 1000 (8 bits)
# Sockets have a 'house code' which is unique to the wireless remote.
# You can decode this using URH.
# Any socket can be reprogrammed to respond to a specific house code by 
# holding the button.
# There are 4 normal addresses that you can write send to (buttons 1-4 on the
# remote).
# Address 5 is a special one that means 'all on' or 'all off'
# Addresses 6-8 are usable and respond to 'all on/off' but there are no
# remote buttons so they can only be used programmatically.
#
# Code is 24 bits + 1 stop bit.
# bits 0-19 (20 bits) :  Preabmble + house code.  example 0xfd160
# bits 20-22 (3 bits) :  Channel.  To convert from a button number
#                        to a code you need to: 
#                        - subtract 1
#                        - invert the bits
#                        - reverse the bit order
# bit 23 (1 bit):        New state (1=on, 0=0ff)
# bit 24 (1 bit):        Stop bit (always 0)
#
# 
housecode=0xfd160
channel=3
newstate=1
rpi-rf_send -g 19 $(($housecode*16+16#$(echo $((channel)) | tr '12345678' 'e6a2c480')+$newstate))

# One-liner version:
housecode=0xfd160; channel=3; newstate=1; rpi-rf_send -g 19 $(($housecode*16+16#$(echo $((channel)) | tr '12345678' 'e6a2c480')+$newstate))



