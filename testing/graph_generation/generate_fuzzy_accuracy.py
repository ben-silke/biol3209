from math import prod
import pandas as p
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns
import json

os.chdir('../')
# print(os.listdir())
genemark_files = [
    f'results/fuzzy/genemark_fuzzy/{f.split("_")[0]}_{f.split("_")[1]}_genemark_test.csv' for f in os.listdir('results/fuzzy/prodigal_fuzzy')]
# print(files)
# files
genemark_results = []
# print('NC_000913' in files)
# files = ['NC_000913']
genemark_sums = []
prodigal_ratio = []
genemark_ratio = []
outliers = []

for file in genemark_files:
    print(file)
    with open(file) as f:
        # print(file=='NC_000913')
        rows = csv.reader(f)
        # there is an ERROR with the reported number of correct
        correct = 0
        total = 0

        for row in rows:
            ls = json.loads(row[3])
            # print(ls)
            # [five_prime, three_prime],
            if type(ls) == list:
                if not ls == [0, 0]:

                    # print(type(ls))
                    five_prime = ls[0]
                    three_prime = ls[1]
                    sum = five_prime+three_prime


                    if abs(sum) < 1000:
                        genemark_sums.append(sum)
                    # else:
                    #     outliers.append(sum)
                    # genemark_sums.append(five_prime+three_prime)
                        if three_prime != 0:
                            genemark_ratio.append(abs(five_prime)/abs(three_prime))
                        else:
                            genemark_ratio.append(abs(five_prime)/1)

                    else:
                        outliers.append(sum)


genemark_arr = np.array(genemark_sums)
genemark_arr.mean()


genemark_data = genemark_arr
print(f'{genemark_arr.mean()=}')


prodigal_files = [
    f'results/fuzzy/prodigal_fuzzy/{f}' for f in os.listdir('results/fuzzy/prodigal_fuzzy')]
# print(files)
# files
prodigal_results = []
# print('NC_000913' in files)
# files = ['NC_000913']
prodigal_ratios = []
prodigal_sums = []
for file in prodigal_files:

    with open(file) as f:
        # print(file=='NC_000913')
        rows = csv.reader(f)
        # there is an ERROR with the reported number of correct
        correct = 0
        total = 0

        for row in rows:
            ls = json.loads(row[3])
            # print(ls)
            if type(ls) == list:

            # print(ls)
                if not ls == [0,0]:
                    # [five_prime, three_prime],
                    five_prime = ls[0]
                    three_prime = ls[1]
                    sum = five_prime+three_prime
                    if abs(sum) < 1000:
                        prodigal_sums.append(sum)
                        if three_prime != 0:
                            prodigal_ratio.append(abs(five_prime)/abs(three_prime))
                        else:
                            prodigal_ratio.append(abs(five_prime)/1)
                    else:
                        outliers.append(sum)



prodigal_array = np.array(prodigal_sums)
print(prodigal_array.max())
print(genemark_arr.max())
# genemark_arr

prodigal_array.mean()

print(f'{prodigal_array.mean()=}')
print(f'{genemark_arr.mean()=}')
print(f'{prodigal_array.std()=}')
print(f'{genemark_arr.std()=}')

print(f'{len(outliers)=}')


# print(f'{len(prodigal_sums)=}')
# print(f'{len(genemark_sums)=}')

# print()
d = {
    'Program': ['Genemark' for i in range(len(genemark_sums))] + ['Prodigal' for i in range(len(prodigal_sums))],
    'total': genemark_sums + prodigal_sums
    # 'GeneMark': genemark_sums[0:len(prodigal_sums)],
    # 'Prodigal': prodigal_sums
}
# print(d)
df = p.DataFrame(data=d)
print(df)
# fig = df.boxplot(by='Program', column=['data'])
# fig = sns.boxplot(data=df, x='total', y='Program')
fig = sns.violinplot(data=df, x='total', y='Program')

# fig = sns.viol
# fig = sns.histplot(data=df, x='total', hue='Program')


fig.set(
    xlabel=r'Error Sum: $\delta_{5^{\prime}} + \delta_{3^{\prime}}$'
)

# plt.text(0.04, 3, r'$\mu=0.020531$')
# fig.text(0.65, 15, r' $\hat \mu _{genemark2s}=$' +
#          str(round(genemark_arr.mean(), 3)))
# fig.text(0.65, 16, r' $\hat \mu_{prodigal}=$' +
#          str(round(prodigal_array.mean(), 3)))

# fig.annotate(r'$\it{E. coli}$', xy=(0.9, 2), xytext=(
#     0.8, 20), arrowprops=dict(facecolor='blue', arrowstyle='->'))

# fig.annotate('Better', xy=(0.8, 30), xytext=(
#     0.6, 30), arrowprops=dict(facecolor='green', arrowstyle='->'))

# print(dir(fig))
print(fig)
plot = fig.get_figure()
plot.savefig('fuzzy_accuracy_sum.png')
# plt.sav


pro_ratio_array = np.array(prodigal_ratio)
gm_ratio_array = np.array(genemark_ratio)


print(f'{pro_ratio_array.mean()=}')
print(f'{gm_ratio_array.mean()=}')
print(f'{pro_ratio_array.std()=}')
print(f'{gm_ratio_array.std()=}')

d_ratio = {
    'Program': ['Genemark' for i in range(len(genemark_ratio))] + ['Prodigal' for i in range(len(prodigal_ratio))],
    'total': genemark_ratio + prodigal_ratio
    # 'GeneMark': genemark_sums[0:len(prodigal_sums)],
    # 'Prodigal': prodigal_sums
}


df = p.DataFrame(data=d_ratio)
print(df)
fig = sns.violinplot(data=df, x='total', y='Program')

fig.set(
    # xlabel=r'Error ratio: $\frac{|\delta_{5^{\prime}}|}{| \delta_{3^{\prime}}|}$'
    xlabel='Error ratio for gene prediction programs'
)

print(fig)
plot = fig.get_figure()
plot.savefig('fuzzy_accuracy_ratio.png')
