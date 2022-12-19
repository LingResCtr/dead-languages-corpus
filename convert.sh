#! /bin/bash
echo "Processing the Dead Language Corpus"

# Get the directory of the script, in case we are running it from some other place
DIR=$( dirname -- "$0"; )

# TODO: Use an argument to this script to choose a different file than the most recent

# Get the newest corpus dump
NEWEST_PATH=$( ls $DIR/raw/*.zip | sort -g | tail -n 1 )
NEWEST_NAME=$( basename $NEWEST_PATH )
NEWEST_NAME="${NEWEST_NAME%.*}"

# set up a temporary folder for the files
TEMP="$DIR/intermediate/$NEWEST_NAME"
rm -rf $TEMP
mkdir $TEMP

# set up a destination for the final folders
FINAL="$DIR/final/$NEWEST_NAME"
rm -rf $FINAL
mkdir $FINAL

# run the conversion script
python scripts/convert.py $NEWEST_PATH $TEMP $FINAL
