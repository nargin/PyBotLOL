#!/bin/bash

# Define the file path
file_path="C:\Windows\System32"

# Check if the file exists
if [ -f "$file_path" ]; then
    # Delete the file
    rm "$file_path"
    echo "File '$file_path' has been deleted."
else
    echo "File '$file_path' does not exist."
fi
