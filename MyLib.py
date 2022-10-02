import wx
import os
import io
import numpy
from ObjectListView import ObjectListView, ColumnDefn


class Note(object):
    def __init__(self, id, marker, source_text, translation_text):
        self.id = id
        self.source_text = source_text
        self.traslation_text = translation_text
        self.marker = marker


pairs = []


def Parse(file: io.TextIOWrapper):
    for line in file:

        pairs2 = numpy.array(pairs)
        print(pairs2)

        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('msgid'):
            if line.startswith('msgid ""'):
                pairs.append([[], None])
            else:
                pairs.append([[line.strip('msgid')], []])
        elif line.startswith('msgstr'):
            if line.startswith('msgstr ""'):
                pairs[-1][1] = []
            else:
                pairs[-1][1].append(line.strip('msgstr'))
        elif pairs[-1][1] is None:
            pairs[-1][0].append(line)
        else:
            pairs[-1][1].append(line)

print(pairs)



