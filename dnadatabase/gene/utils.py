import gff3_parser

from cogent3.parse.fasta import MinimalFastaParser


class ProdigalResultParser:

    def __init__(self, open_file) -> None:
        self.parser = MinimalFastaParser(open_file)

    def run(self):
        genes = []
        for p in self.parser:
            content = p
            metadata = content[0].split(';')
            core_info = metadata[0].split('#')

            data = {
                'sequence': content[1],
                'name': core_info[0].strip(),
                'start': core_info[1].strip(),
                'end': core_info[2].strip(),
            }
            for property in metadata[2:]:
                property = property.split('=')
                data[property[0]] = property[1]
            genes.append(data)
        return genes


class GffParser:

    metadata = []
    genes = []
    def __init__(self, open_file) -> None:
        self.open_file = open_file

    # TODO: maybe make this read a line at once; seems excessive to make the absolutely optimised
    # However; at the moment this requires reading everything twice; plus a third when it is used

    def run(self):
        self.lines = self.open_file.readlines()
        i=0
        for line in self.lines:
            i += 1
            if line[0] == '#':
                self.metadata.append(line)
            else:
                print(line)
                data = line.split('\t')
                print(data)
                print(len(data))
                if len(data) > 5:
                    gene = {
                        'locus': data[0],
                        'method': data[1],
                        'type': data[2],
                        'start': int(data[3]),
                        'end': int(data[4]),
                    }
                # Get the last element
                other_data = data[-1].split(';')
                for entry in other_data:
                    content = entry.strip().split(' ')
                    if len(content) == 2:
                        value = content[1].replace('"','')
                        gene[content[0]] = value
                self.genes.append(gene)

        return self.genes
