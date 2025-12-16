#!/bin/bash

cd ./src/c/game_core
make clean
make MESSAGE="Hello" TARGET=hello
make clean
make MESSAGE="Hi" TARGET=hi
make clean