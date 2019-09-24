#!/bin/sh
# Read a TMP101 sensor
#Blake Emmert
#hw03
#9/24/19

temp1=`i2cget -y 2 0x48`
temp2=`i2cget -y 2 0x4a`

temp1F=$(($temp1 *9 /5 +32))
temp2F=$(($temp2 *9 /5 +32))


echo "Temperature 1:"
echo "$temp1F"
echo "Temperature 2:"
echo "$temp2F"
