#!/bin/bash
make
echo "compilation done.\n"
#python3 manyusers.py
>>>>>>> 4dc17a09ec240aeabf4221bc2e460a93ba46fe01
echo "Location script done.\n"
./cff_flow < ./costs_data > result.txt
echo "Flow done.\n"
python3 send_to_server.py
echo "Sent results to server."
