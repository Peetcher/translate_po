import polib
from data import data

class Note(object):
    def __init__(self, id, source_text, translate_text, commentary):
        self.id = id
        self.source_text = source_text
        self.translate_text = translate_text
        self.commentary = commentary


def to_note_list(pofile):
    notes = []
    for index, entry in enumerate(pofile):
        notes.append(Note(index, entry.msgid, entry.msgstr, entry.occurrences))
    data.set_notes(notes)


def parse(file):
    po = polib.pofile(file.replace("\\", "/"), encoding="utf-8")
    to_note_list(po)
    data.set_pofile(po)
    return po
    # for line in file:
    #    line = line.strip()
    #    if not line or line.startswith('#'):
    #        if not line:
    #            commentary.append([])
    #        else:
    #            commentary[-1].append(line)
    #        continue
    #    if line.startswith('msgid'):
    #        if line.startswith('msgid ""'):
    #            pairs.append([[], None])
    #        elif line.startswith('msgid_plural'):
    #            pairs[-1].append([line.strip('msgid_plural')])
    #        else:
    #            pairs.append([[line.strip('msgid')], []])
    #    elif line.startswith('msgstr'):
    #        if line.startswith('msgstr ""'):
    #            pairs[-1][1] = []
    #        else:
    #            if pairs[-1][1] is None:
    #                pairs[-1][1] = []
    #            pairs[-1][1].append(line.strip('msgstr'))
    #    elif pairs[-1][1] is None:
    #        pairs[-1][0].append(line)
    #    else:
    #        pairs[-1][1].append(line)
    # return pairs
