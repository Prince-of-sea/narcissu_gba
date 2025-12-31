#!/bin/bash

cd ./src/c/game_core
export PATH=$PATH:/opt/devkitpro/devkitARM/bin
make clean
make MESSAGE="Test" TARGET=test
# make clean
# make MESSAGE="Hi" TARGET=hi
# make clean