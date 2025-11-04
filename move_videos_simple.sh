#!/bin/bash
# Simple script to move MP4 files from examples to videos directory

mkdir -p videos && mv examples/*.mp4 videos/ 2>/dev/null && echo "MP4 files moved to videos/" || echo "No MP4 files found in examples/"
