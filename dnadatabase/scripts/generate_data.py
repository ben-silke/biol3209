import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django
django.setup()
import csv
print(os.listdir())
os.chdir('../')
print(os.listdir())

folder = 'data/summary_stats'

from gene.models import CDS

# counts_file = folder+'/counts_stats.csv'
# with open(counts_file, 'w') as f:
#     writer = csv.writer(f)

#     headers = ['gene_name', 'counts']
#     writer.writerow(headers)

#     for name in set(Gene.objects.values_list('name')):
#         name = name[0]
#         count = Gene.objects.filter(name=name).count()
#         writer.writerow([name, count])

# counts = []
# with open(counts_file) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         count = row[1]
#         print(count)
#         print(type(count))
#         try:
#             count = int(row[1])
#             print(type(count))
#             if count > 1:
#                 counts.append(row)
#         except:
#             counts.append(row)

# print(counts)

# high_counts_file = folder+'/high_counts_stats.csv'
# with open(high_counts_file, 'w') as f:
#     writer = csv.writer(f)
#     for row in counts:
#         writer.writerow(row)



# for gene in CDS.objects.all():
#     name = gene.name
#     print(name)
    # name = name.replace('[','').replace(']','').replace("\'","")
    # print(name)
    # gene.name = name
    # gene.save()
