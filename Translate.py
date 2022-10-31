from MyLib import refresh
import json
from configparser import ConfigParser
import grequests
from loguru import logger
config = ConfigParser()
config.read("config.ini")
from data import data

logger.add("report.log", format="{time} {level} {message}", level="DEBUG", rotation="20KB", compression="zip")

def translate(array):
    config.read("config.ini")
    url = "https://translo.p.rapidapi.com/api/v3/translate"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": config['user']['api_key'],
        "X-RapidAPI-Host": "translo.p.rapidapi.com"
    }
    response = (grequests.request("POST", url, data=payload, headers=headers) for payload in array)

    resp = grequests.map(response)

    data.set_response_error(resp[0].text)

    return resp

def translate_part(entries_trans, po, dataOlv):
    for index, item in enumerate(entries_trans):
        if item is None:
            entries_trans[index] = "Error API"
            continue
        entries_trans[index] = (json.loads(item.text))["translated_text"]



def translate_all(po, dataOlv):
    entries = []
    for item in po:
        temp = item.msgid.replace("’", " ")
        entries.append(f"from=en&to=ru&text={temp}")
    entries_trans = translate(entries)

    translate_part(entries_trans, po, dataOlv)

    for index, item in enumerate(po):
        item.msgstr = entries_trans[index]
    refresh(po, dataOlv)


def translate_selected(po, dataOlv):
    entries = []
    cheked_objects = dataOlv.GetCheckedObjects()
    for item in cheked_objects:
        temp = po[item.id].msgid.replace("’", " ")
        entries.append(f"from=en&to=ru&text={temp}")
    entries_trans = translate(entries)

    translate_part(entries_trans, po, dataOlv)

    for index, item in enumerate(cheked_objects):
        po[item.id].msgstr = entries_trans[index]
    refresh(po, dataOlv)


def translate_untranslated(po, dataOlv):
    entries = []
    for index, item in enumerate(po.untranslated_entries()):
        temp = item.msgid.replace("’", " ")
        entries.append(f"from=en&to=ru&text={temp}")
    entries_trans = translate(entries)

    translate_part(entries_trans, po, dataOlv)

    for index, item in enumerate(po.untranslated_entries()):
        item.msgstr = entries_trans[index]
    refresh(po, dataOlv)


def translate_selected_and_untrans(po, dataOlv):
    entries = []
    id = []
    cheked_objects = dataOlv.GetCheckedObjects()
    for item in cheked_objects:
        if po[item.id] in po.untranslated_entries():
            continue
        else:
            temp = po[item.id].msgid.replace("’", " ")
            entries.append(f"from=en&to=ru&text={temp}")
            id.append(item.id)
    entries_trans = translate(entries)
    translate_part(entries_trans, po, dataOlv)
    for index, item in enumerate(id):
        po[item].msgstr = entries_trans[index]
    refresh(po, dataOlv)


    translate_untranslated(po, dataOlv)
