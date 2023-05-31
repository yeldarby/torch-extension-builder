#!/bin/bash

# Replace with your base directory path
base_directory="/path/to/runners"

# Clear the working directories of all runners
for dir in $base_directory/runner*
do
    rm -rf "$dir"/*
done
