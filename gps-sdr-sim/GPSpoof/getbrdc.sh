#!/bin/sh
day=$(date -d -1day +%j)
year=$(date +%Y)
yr=$(date +%y)

wget "ftp://cddis.gsfc.nasa.gov/gnss/data/daily/$year""/brdc/brdc""$day""0.$yr""n.Z"

uncompress "brdc""$day""0.$yr""n.Z"
echo "brdc""$day""0.$yr""n.Z"

