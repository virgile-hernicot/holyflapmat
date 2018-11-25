#!/bin/bash
make
echo "compilation done.\n"
python3 manyusers.py
echo "Location script done.\n"
./cff_flow < ./costs_data > result.txt
echo "Flow done.\n"
python3 send_to_server.py
echo "Sent results to server."
python3 persist_available_spots.py
echo "Available parking spots persisted."