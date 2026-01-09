#!/bin/bash

cd ./src/c/game_core
export PATH=$PATH:/opt/devkitpro/devkitARM/bin
make clean
make
# make clean