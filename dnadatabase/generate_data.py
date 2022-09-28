import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dnadatabase.settings")
import django


django.setup()
import csv


print(os.listdir())
os.chdir('../')
print(os.listdir())

folder = 'data/summary_stats'

from gene.models import CDS, CdsDatabaseReference, Gene


# counts_file = folder+'/cds_counts_stats.csv'
# with open(counts_file, 'w') as f:
#     writer = csv.writer(f)

#     headers = ['gene_name', 'counts']
#     writer.writerow(headers)

#     for name in set(CDS.objects.values_list('name')):
#         name = name[0]
#         count = CDS.objects.filter(name=name).count()
#         writer.writerow([name, count])

# counts = []
# with open(counts_file) as f:
#     reader = csv.reader(f)
#     for row in reader:
#         count = row[1]
#         try:
#             count = int(row[1])
#             if count > 1:
#                 counts.append(row)
#         except:
#             counts.append(row)

# print(counts)

# high_counts_file = folder+'/high_cds_counts_stats.csv'
# with open(high_counts_file, 'w') as f:
#     writer = csv.writer(f)
#     for row in counts:
#         writer.writerow(row)

# file = folder+'/database_references.csv'
# with open(file, 'w') as f:
#     rows = []
#     field_names = set()
#     for gene in Gene.objects.all():
#         row = {
#             'name': gene.name
#         }
#         for ref in gene.database_set:
#             row[ref.database.name] = ref.db_xref
#             field_names.add(ref.database.name)
#         if gene.cds:
#             for ref in gene.cds.database_set:
#                 row[ref.database.name] = ref.db_xref
#                 field_names.add(ref.database.name)

#         if len(row) > 1:
#             rows.append(row)

#     print(field_names)
#     print([name for name in field_names])
#     print(['name'] + [name for name in field_names])

#     field_names = ['name'] + [name for name in field_names]
#     print(field_names)
#     writer = csv.DictWriter(f, fieldnames=field_names)
#     print(field_names)
#     writer.writeheader()
#     writer.writerows(rows)


# for gene in Gene.objects.all():
#     print(gene.name)
#     name = gene.name.replace("[","").replace("]","").replace("\'","")
#     print(f'{name=}')
#     gene.name = name
#     gene.save()

# for gene in CDS.objects.all():
#     print(gene.name)
#     name = gene.name.replace("[","").replace("]","").replace("\'","")
#     print(f'{name=}')
#     gene.name = name
#     gene.save()

ls = []
counts_file = folder+'/cds_kegg_links.csv'
with open(counts_file, 'w') as f:
    writer = csv.writer(f)
    for i, ref in enumerate(CdsDatabaseReference.objects.filter(database__name='UniProtKB/Swiss-Prot')):
        cds = ref.cds
        output = cds.kegg_link()
        row = [cds.name]
        if output:
            if cds.kegg_id:
                row.append(cds.kegg_id)
            row.append(output)
        ls.append(row)
        print(f'{i}- {cds.name}')
        writer.writerow(row)
