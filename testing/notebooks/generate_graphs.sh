#!/bin/bash


# just enter all python scripts and it will urn

python3 generate_prodigal_accuracy.py
python3 generate_genemark_time_results.py
python3 generate_prodigal_time.py
python3 generate_genemark_acc_results.py


python3 generate_both_results.py
python3 generate_both_time.py
