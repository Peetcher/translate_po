class Data:
    def __init__(self):
        self.__notes = []
        self.__pofile = None
        self.__radiobox_selection = 0

    def get_notes(self):
        return self.__notes

    def set_notes(self, someinfo):
        self.__notes = someinfo

    def get_pofile(self):
        return self.__pofile

    def set_pofile(self, someinfo):
        self.__pofile = someinfo

    def get_radiobox_selection(self):
        return self.__radiobox_selection

    def set_radiobox_selection(self, someinfo):
        self.__radiobox_selection = someinfo


data = Data()




