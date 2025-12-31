#!/bin/bash

cd ./src/c/game_core
make clean
make MESSAGE="Test" TARGET=test
make clean
# make MESSAGE="Hi" TARGET=hi
# make clean