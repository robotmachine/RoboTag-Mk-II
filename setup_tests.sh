#!/bin/bash

# Creates empty mp3 files to use for testing

create_file() {
  ffmpeg -f lavfi -i anullsrc=r=44100:cl=mono -t 3 -q:a 9 -acodec libmp3lame "$1".mp3
}

track_names=("01 Tom's Diner" "02 Luka" "03 Ironbound Fancy Poultry" "04 In the Eye" "05 Night Vision" "06 Solitude Standing" "07 Calypso" "08 Language" "09 Gypsy" "10 Wooden Horse (Caspar Hauser's Song)" "11 Tom's Diner (Reprise)")

# Create directories
full_path=("Music" "Susanne Vega" "1987 Solitude Standing")
mkdir "${full_path[0]}"
mkdir "${full_path[0]}/${full_path[1]}"
mkdir "${full_path[0]}/${full_path[1]}/${full_path[2]}"

# Create tracks
for track_name in "${track_names[@]}"
do
  create_file "${full_path[0]}/${full_path[1]}/${full_path[2]}/$track_name"
done
