#!/bin/bash
make
echo "compilation done.\n"
python3 manyusers.py
echo "Location script done.\n"
./cff_flow < ./costs_data
