import wx
import os
import io
from ObjectListView import ObjectListView, ColumnDefn

class Note(object):
    def __init__(self,id , marker, source_text, translation_text):
        self.id = id
        self.source_text = source_text
        self.traslation_text = translation_text
        self.marker = marker

def Parse(file : io.TextIOWrapper):
    text = ""
    for lines in file:
        if lines.startswith("msgid"):
            text += f" {lines.strip()}"
        elif lines.startswith("msgstr"):
            text += f" {lines.strip()}"
        else:
            text += lines.strip()
    text.split()

    sourcetxt = []

    for index, word in enumerate(text):
        if word = "msgid":





