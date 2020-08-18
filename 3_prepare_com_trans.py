from pathlib import Path
import re
import polib


class Po:
    def __init__(self):
        self.par_marker = '\n\n\n'
        self.trans_pattern = r'(.*?\n\t.*)\n'
        self.trans_delimiter = '\n\t'
        self.file = polib.POFile()
        self.file.metadata = {
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

    def _create_entry(self, msgid, msgstr="", msgctxt=None, comment=None, tcomment=None):
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
            msgctxt=msgctxt,
            comment=comment,
            tcomment=tcomment
        )
        self.file.append(entry)

    def write_to_file(self, filename):
        self.file.save(filename)

    def dump_to_entries(self, dump, origin):
        for num, par in enumerate(dump.strip().split(self.par_marker)):
            pairs = re.split(self.trans_pattern, par)
            pairs = [p for p in pairs if p]
            source = []
            comment = []
            for pair in pairs:
                s, c = pair.split(self.trans_delimiter)
                source.append(s)
                comment.append(c)
            source = ' '.join(source)
            comment = ' '.join(comment)
            self._create_entry(msgid=source, msgctxt=f'line {num + 1}, {origin}', tcomment=comment)

    def txt_to_po(self, filename):
        filename = Path(filename)
        lines = filename.read_text(encoding='utf-8')
        self.dump_to_entries(lines, filename.name)

        outfile = Path(out_folder) / (filename.stem + ".po")
        self.write_to_file(outfile)


if __name__ == '__main__':
    in_folder = 'fr_com/source/txt'
    out_folder = 'fr_com/source/po'
    for file in Path(in_folder).glob('*.txt'):
        po = Po()
        po.txt_to_po(file)
