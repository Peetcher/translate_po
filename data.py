class Data:
    def __init__(self):
        self.__notes = []
        self.__pofile = None
        self.__radiobox_selection = 0
        self.__response_error = None

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

    def get_response_error(self):
        return self.response_error

    def set_response_error(self, someinfo):
        self.response_error = someinfo


data = Data()




