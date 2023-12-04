from cogent3.parse import genbank as cogent


class GenbankParser:
    files = []
    file = None

    handlers = cogent.handlers

    default_handler = cogent.generic_adaptor

    recs = []

    def __init__(self, file=None, files=[]) -> None:
        if files:
            self.files = files
        if file:
            self.file = file

        self.handlers["FEATURES"] = (self.feature_table_adaptor,)

        # Can maybe make this function better

    def parser(self, file=None):
        if self.file:
            file = self.file

        p = cogent.GbFinder(file)
        print(f"{p=}")

        for recs in cogent.GbFinder(file):
            for rec in recs:
                curr = {}
                bad_record = False
                for field in cogent.indent_splitter(rec):
                    print(f"{field=}")
                    first_word = field[0].split(None, 1)[0]
                    handler = self.handlers.get(first_word, self.default_handler)
                    print(f"{handler=}")
                    try:
                        handler(field, curr)
                    except Exception:
                        bad_record = True
                        break
                if not bad_record:
                    # print(curr)
                    yield curr

    def minimal_cogent_parser(self, open_file=None):
        if self.file:
            open_file = self.file

        if not open_file:
            raise ValueError("No file provided")

        return cogent.MinimalGenbankParser(open_file)

    def rich_cogent_parser(
        self,
        open_file=None,
        info_excludes=None,
        moltype=None,
        skip_contigs=False,
        add_annotation=None,
    ):
        if self.file:
            open_file = self.file

        if not open_file:
            raise ValueError("No file provided")
        return cogent.RichGenbankParser(
            open_file,
            info_excludes=info_excludes,
            moltype=moltype,
            skip_contigs=skip_contigs,
            add_annotation=add_annotation,
        )

    def feature_table_adaptor(self, lines, curr):
        if "features" not in curr:
            curr["features"] = []
        curr["features"].extend(self.parse_feature_table(lines))

    def parse_feature_table(self, lines):
        """Simple parser for feature table. Assumes starts with FEATURES line."""
        if not lines:
            return []
        if lines[0].startswith("FEATURES"):
            lines = lines[1:]
        return [self.parse_feature(f) for f in self.indent_splitter(lines)]

    def parse_feature(self, lines):
        """Parses a feature. Doesn't handle subfeatures.

        Returns dict containing:
        'type': source, gene, CDS, etc.
        'location': unparsed location string
        ...then, key-value pairs for each annotation,
            e.g. '/gene="MNBH"' -> {'gene':['MNBH']} (i.e. quotes stripped)
        All relations are assumed 'to many', and order will be preserved.
        """
        print(f"{lines=}")
        type_, data = cogent.block_consolidator(lines)
        result = {"type": type_}
        location = []
        found_feature = False
        for curr_line_idx, line in enumerate(data):
            if line.lstrip().startswith("/"):
                found_feature = True
                break
            else:
                location.append(line)
        result["raw_location"] = location
        try:
            result["location"] = cogent.parse_location_line(
                cogent.location_line_tokenizer(location)
            )
        except (TypeError, ValueError):
            result["location"] = None
        if not found_feature:
            return result
        fci = cogent.feature_component_iterator
        for feature_component in fci(data[curr_line_idx:]):
            first = feature_component[0].lstrip()[1:]  # remove leading space, '/'
            try:
                label, first_line = first.split("=", 1)
            except ValueError:  # sometimes not delimited by =
                label, first_line = first, ""
            # chop off leading quote if appropriate
            first_line = first_line.removeprefix('"')
            remainder = [first_line] + feature_component[1:]
            # chop off trailing quote, if appropriate
            last_line = remainder[-1].rstrip()
            if last_line.endswith('"'):
                remainder[-1] = last_line[:-1]
            if label in cogent._join_with_empty:
                curr_data = "".join(map(cogent.strip, remainder))
            elif label in cogent._leave_as_lines:
                curr_data = remainder
            else:
                curr_data = " ".join(map(cogent.strip, remainder))
            if label.lower() == "type":
                # some source features have /type=...
                label = "type_field"
            if label not in result:
                result[label.lower()] = []

            result[label.lower()].append(curr_data)
        return result
