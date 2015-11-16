#!/bin/bash - 
#===============================================================================
#
#          FILE: main.sh
# 
#         USAGE: ./main.sh "abs-path-to-execute" "abs-path-to-move-results"
#                           use double quotes if the paths have white spaces
# 
#   DESCRIPTION: Lanza el script de matlab con los parametros de entrada
#                especificados
#                It's mandatory to use double quotes along the script
#                to avoid conflicts with white spaces in paths
#
#        AUTHOR: Juan Marín (), 
#  ORGANIZATION: 
#       CREATED: 14/11/15 17:53
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

MATLABSCRIPT=Rectimages
MATLABSCRIPTFOLDER=matlab
#MATLABSCRIPT=foo
MATLAB_PICTURE_OUTPUT_SIZE=256

cd $MATLABSCRIPTFOLDER

# The first input argument is needed
# This argument should be the base folder for the pictures to be parsed
if [ -z "$1" ]
then
    echo No argument supplied
    echo Usage $0 abs-path-to-execute abs-path-to-move-results
    exit 1
fi

# the second input argument is needed too
# it should be the destionation for the parsed pictures
if [ -z "$2" ]
then
    echo No argument supplied
    echo Usage $0 abs-path-to-execute abs-path-to-move-results
    exit 1
fi


SRCFOLDER="$1"
DSTFOLDER="$2"
echo
echo "================================================================================"
echo "|                                                                              |"
echo "| This script will launch Rectimages, which is a matlab script which rotates   |"
echo "| crops and resized images from a wearable camera, based in the information    |"
echo "| contained in the meta folders.                                               |"
echo "| Folders which don't contain a meta folder inside won't be processed          |"
echo "|                                                                              |"
echo "================================================================================"
echo
echo "Executing Rectimages recursively in $SRCFOLDER"
echo "This may take some time"
echo


# All the folders recursively only the next type of folder structure
# user/year/month/day
# executes the matlab script for each folder

find "$SRCFOLDER" -mindepth 4 -not -path "*meta*"  -not -path "*_Crop*" -type d | while read path
do
    #echo Executing Rectimages in folder: "$path"
    
    # executes the script
    command="matlab -nodesktop -nojvm -r "'"folder='"'$path'"';exit_on_end=1;output_size='"$MATLAB_PICTURE_OUTPUT_SIZE;$MATLABSCRIPT"'" >output.txt 2>&1'
    echo ">> $command"
    eval $command

    echo
    
done

echo
echo "Copying the result images preserving the same folder structure to $DSTFOLDER"
echo "This should be faster"
echo


# Retrieves all the folders, but only with the next structure
find "$SRCFOLDER" -mindepth 4 -not -path "*meta*" -path "*_Crop*" -type d | while read srcfolder
do
    # changes the substring of the source folder to the destiny folder
    dstfolder="${srcfolder/$SRCFOLDER/$DSTFOLDER}"
    # changes the word _Crop for nothing
    dstfolder="${dstfolder/_Crop}"
    #echo Copying images from '"'"$srcfolder"'"' to '"'"$dstfolder"'"'
    
    # creating new folder
    mkcommand="mkdir -p '$dstfolder'"
    echo ">> $mkcommand"
    eval $mkcommand

    # copying images
    copycommand="cp -R '$srcfolder/.' '$dstfolder/'"
    echo ">> $copycommand"
    eval $copycommand
    
    echo
done

echo BYE

