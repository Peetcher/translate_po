import polib
from data import data
from ObjectListView import ObjectListView

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

def refresh(pofile, dataolv: ObjectListView, statusbar):
    data.set_pofile(pofile)
    to_note_list(pofile)
    dataolv.SetObjects(data.get_notes())
    statusbar.SetStatusText(f'переведено {data.get_pofile().percent_translated()} %')
