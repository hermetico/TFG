#!/bin/bash - 
#===============================================================================
#
#          FILE: resize-images.sh
# 
#         USAGE: ./resize-images.sh folder
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 12/08/2015 19:16
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

# The first input argument is needed
# This argument should be the base folder for the pictures to be parsed
if [ -z "$1" ]
then
    echo No argument supplied
    echo Usage $0 abs-path-to-execute abs-path-to-move-results
    exit 1
fi


SRCFOLDER="$1"
NOW="$(date)"
SIZE="256x256"

echo
echo "================================================================================"
echo "|                                                                              |"
echo "| This script will launch mogrify                                              |"
echo "|                                                                              |"
echo "================================================================================"
echo
echo "Executed: $NOW"
echo
echo "Executing mogrify recursively in $SRCFOLDER"
echo "This may take some time"
echo


# All the folders recursively only the next type of folder structure
# user/year/month/day
# executes the matlab script for each folder
echo ">> find" '"'"$SRCFOLDER"'"' -mindepth 4 -not -path "*meta*" -not -path "*Meta*" -not -path "*_Crop*" -type d
find "$SRCFOLDER" -mindepth 4 -not -path "*meta*" -not -path "*Meta*" -not -path "*_Crop*" -type d | while read path
do
    
    # executes the script
    command='mogrify -resize' $SIZE "'"$path/*.jpg"'"
    echo ">> $command"
    eval $command
    echo
    
done

echo BYE

