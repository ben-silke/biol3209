import pandas as p
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns

os.chdir('../')
# print(os.listdir())
genemark_files = [
    f'results/genemark_last/{f}' for f in os.listdir('results/genemark_last')]
# print(files)
# files
genemark_results = []
# print('NC_000913' in files)
# files = ['NC_000913']

for file in genemark_files:

    with open(file) as f:
        # print(file=='NC_000913')
        rows = csv.reader(f)
        for row in rows:
            # row = rows[i]
            if len(row) > 1:
                if row[0] == 'correct':
                    # print(row)
                    try:
                        genemark_results.append(int(row[1])/int(row[3]))
                    except:
                        print(row)

                    # break

                # if file == 'NC_000913':
                    # print(row)
genemark_arr = np.array(genemark_results)
genemark_arr.mean()


genemark_data = genemark_arr
print(genemark_arr.mean())


prodigal_files = [
    f'results/prodigal_last/{f}' for f in os.listdir('results/prodigal_last')]
# print(files)
# files
prodigal_results = []
# print('NC_000913' in files)
# files = ['NC_000913']

for file in prodigal_files:

    with open(file) as f:
        # print(file=='NC_000913')
        rows = csv.reader(f)
        # there is an ERROR with the reported number of correct
        correct = 0
        total = 0

        for row in rows:
            # print(row)
            if len(row) > 4:
                if row[4] == 'True':
                    correct = correct + 1
                    total = total + 1

                if row[4] == "No match found":
                    total = total + 1

        if correct and total:
            prodigal_results.append(correct/total)


prodigal_array = np.array(prodigal_results)
prodigal_array.mean()

print(prodigal_array.mean())


d = {
    'Program': ['Genemark2S' for i in range(len(genemark_results))] + ['Prodigal' for i in range(len(prodigal_results))],
    'data': genemark_results + prodigal_results
}
df = p.DataFrame(data=d)


fig = sns.histplot(data=df, hue="Program", x='data', element="poly")

fig.set(
    xlabel='Proportion of matches of gene last base coordinates'
)

# plt.text(0.04, 3, r'$\mu=0.020531$')
fig.text(0.75, 15, r' $\hat \mu _{genemark2s}=$'+str(round(genemark_arr.mean(), 3)))
fig.text(0.75, 16, r' $\hat \mu_{prodigal}=$'+str(round(prodigal_array.mean(), 3)))

# fig.annotate(r'$\it{E. coli}$', xy=(0.9, 2), xytext=(
#     0.8, 20), arrowprops=dict(facecolor='blue', arrowstyle='->'))

# fig.annotate('Better', xy=(0.8, 30), xytext=(
#     0.6, 30), arrowprops=dict(facecolor='green', arrowstyle='->'))

# print(dir(fig))
print(fig)
plot = fig.get_figure()
plot.savefig('last_base_accuracy.png')
# plt.sav
