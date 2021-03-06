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
    echo "Usage $0 abs-path-to-execute [min-depth]"
    exit 1
fi

if [ -z "$2" ]
then
    echo Using min depth 4
    MIN_DEPTH="4"
else
    echo Using min depth $2
    MIN_DEPTH="$2"

fi

SRCFOLDER="$1"
NOW="$(date)"
# los simbolos \! indican que no es necesario mantener la proporcion de las imagenes
# con lo cual tendremos seguro 256x256 aunque se deformen
SIZE="256x256\!"

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
echo ">> find" '"'"$SRCFOLDER"'"' -mindepth $MIN_DEPTH -not -path "*meta*" -not -path "*Meta*" -not -path "*_Crop*" -type d
find "$SRCFOLDER" -mindepth $MIN_DEPTH -not -path "*meta*" -not -path "*Meta*" -not -path "*_Crop*" -type d | while read path
do
    
    # executes the script
    command="mogrify -resize $SIZE "'"'"$path/*.jpg"'"'
    echo ">> $command"
    eval $command
    echo
    
done

echo BYE

