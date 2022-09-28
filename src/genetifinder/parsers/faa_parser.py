from cogent3.parse.fasta import MinimalFastaParser


class ProdigalResultParser:
    def __init__(self, open_file) -> None:
        self.parser = MinimalFastaParser(open_file)

    def run(self):
        genes = []
        for p in self.parser:
            content = p
            metadata = content[0].split(";")
            core_info = metadata[0].split("#")

            data = {
                "sequence": content[1],
                "name": core_info[0].strip(),
                "start": core_info[1].strip(),
                "end": core_info[2].strip(),
            }
            for property in metadata[2:]:
                property = property.split("=")
                data[property[0]] = property[1]
            genes.append(data)
        return genes


class GeneMarkS2ResultParser:
    def __init__(self, open_file) -> None:
        self.parser = MinimalFastaParser(open_file)
