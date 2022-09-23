from cogent3.parse.fasta import MinimalFastaParser

class ProdigalResultParser:

    def __init__(self, file) -> None:
        self.parser = MinimalFastaParser(file)

    def run(self):
        genes = []
        for p in self.parser:
            print(f'{p}')
            genes.append(p)
        
        return genes
