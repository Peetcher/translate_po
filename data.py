class Data:
    def __init__(self):
        self.__msg_pairs = []
        self.__notes = []
        self.__pofile = None

    def get_msgpairs(self):
        return self.__msg_pairs

    def set_msgpairs(self, someinfo):
        self.__msg_pairs = someinfo

    def get_notes(self):
        return self.__notes

    def set_notes(self, someinfo):
        self.__notes = someinfo

    def get_pofile(self):
        return self.__pofile

    def set_pofile(self, someinfo):
        self.__pofile = someinfo


data = Data()


