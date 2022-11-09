import matplotlib.pyplot as plt
import seaborn as sns
import csv
import os
os.chdir('../')
os.listdir()

file = 'results/prodigal_overall.csv'

results = []

with open(file) as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            val = int(row[1])/int(row[2])
            results.append(val)
        except:
            print(f'fail {row=}')
            # print(row)

# print(results)
import numpy as np
