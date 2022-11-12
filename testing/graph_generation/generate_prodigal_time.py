import seaborn as sns
import numpy as np
import csv
import os
os.chdir('../')
os.listdir()
import matplotlib.pyplot as plt

folders = [f'{d}' for d in os.listdir('data/output/prodigal')]
# folders
prefix = 'data/output/prodigal/'
print(os.listdir())
time = []
for folder in folders:
    file = f'{prefix}{folder}/{folder}.strace.txt'
    try:
        # print(fi)
        with open(file) as f:
            # print(f'YAY {file}')
            rows = csv.reader(f)
            for row in rows:
                # print(row)
                # print('total' in row)
                # # print(type(row))
                if 'total' in row[0]:
                    # print(row)
                    row = row[0].split(' ')
                    # print(row[4])
                    time.append(float(row[4]))
                # print(row)
    except Exception as e:
        print(e, file)

arr = np.array(time)
arr.mean()


prodigal_data = arr


figure = sns.histplot(
    data=prodigal_data,
    # xlabel="exact_matches_per_sequence",
    bins=50,
    element="poly",
    # y='Sequence Counts'
)

# figure.set_axis_labels('')
figure.set(
    xlabel='Runtime (seconds)'
)
print(f'{arr.mean()=}')
figure.text(0.1, 200, r'$\hat \mu=$'+str(round(arr.mean(), 4)))



# print(dir(fig))
# print(fig)
plot = figure.get_figure()
plot.savefig('prodigal_runtime.png')
# plt.sav
