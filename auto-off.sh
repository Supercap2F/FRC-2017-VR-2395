#!/bin/bash
# This script turns off all the auto features of the microsoft
# lifecam for FRC. It requires that you have 'uvcdynctrl' installed.
# NOTE: This script *must* be run as sudo

echo "Turning off auto exposure ..."
uvcdynctrl -s 'Exposure, Auto' 1
uvcdynctrl -s 'Exposure (Absolute)' 0
uvcdynctrl -g 'Exposure, Auto'


echo "Turning off auto white balance ..."
uvcdynctrl -s 'White Balance Temperature, Auto' 0
uvcdynctrl -g 'White Balance Temperature, Auto'


