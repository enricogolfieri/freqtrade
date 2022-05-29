#!/bin/bash

git clone git@github.com:freqtrade/freqtrade.git tmp 
cd tmp
git checkout stable 
cd ..
cp -r tmp/* .

./setup.sh --install 

#rm -rf tmp 