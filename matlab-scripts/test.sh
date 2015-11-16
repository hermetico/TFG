#!/bin/bash - 
#===============================================================================
#
#          FILE: test.sh
# 
#         USAGE: ./test.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 15/11/15 19:39
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

#SRCFOLDERS=( $(find "$1" -mindepth 4 -not -path "*meta*"  -not -path "*_Crop*" -type d) )
find "$1" -mindepth 4 -not -path "*meta*"  -not -path "*_Crop*" -type d | while read folder
do
    echo Executing Rectimages in folder: "$folder"
done
exit
# executes the matlab script for each folder
for folder in $SRCFOLDERS
do
    #finalfolder="$1/$folder"

    echo Executing Rectimages in folder: "$folder"


done
exit
# executes the matlab script for each folder
for folder in $newfolders
do
    finalfolder="$SRCFOLDER/$folder"
    # executes the script
    echo matlab -nodesktop -nojvm -r "folder='"$finalfolder"';output_size="$MATLAB_PICTURE_OUTPUT_SIZE";"$MATLABSCRIPT""
    echo OK
done


