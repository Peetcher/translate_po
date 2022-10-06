import wx
from ObjectListView import ObjectListView, ColumnDefn
from MyLib import parse, to_note_list
from data import data
from Translate import translate
import json


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        # панель-меню
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        edit = wx.Menu()
        view = wx.Menu()
        translate = wx.Menu()

        # добавление кнопок на панель окна
        menubar.Append(fileMenu, '&Файл')
        menubar.Append(edit, '&Правка')
        menubar.Append(view, '&Вид')
        menubar.Append(translate, '&Перевод')

        # кнопки для панели File
        open_btn = wx.MenuItem(fileMenu, wx.ID_OPEN, 'Открыть')
        create_btn = wx.MenuItem(fileMenu, wx.ID_FILE, 'Создать')
        save_btn = wx.MenuItem(fileMenu, wx.ID_SAVE, 'Сохранить')
        exit_btn = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Выход', 'Выход из приложения')

        # кнопки для панели translate
        translate_btn = wx.MenuItem(translate, wx.ID_ANY, 'Перевести')

        # добавление кнопок в File
        fileMenu.Append(open_btn)
        fileMenu.Append(create_btn)
        fileMenu.Append(save_btn)
        fileMenu.Append(exit_btn)

        # добавление кнопок в Translate
        translate.Append(translate_btn)

        self.SetMenuBar(menubar)

        # события кнопок
        self.Bind(wx.EVT_MENU, self.OnOpen, open_btn)
        # self.Bind(wx.EVT_MENU, self. , create_btn)
        self.Bind(wx.EVT_MENU, self.onSave, save_btn)
        self.Bind(wx.EVT_MENU, self.onQuit, exit_btn)
        self.Bind(wx.EVT_MENU, self.onTranslate, translate_btn)

        # виджеты

        self.dataOlv = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        self.dataOlv.SetColumns(
            [
                ColumnDefn("Id", "left", 50, "id"),
                ColumnDefn("Source_text", "left", 350, "source_text"),
                ColumnDefn("Translation_text", "left", 350, "translate_text"),
                ColumnDefn("Comments", "left", 100, "commentary")
            ]

        )

        # текстовые поля для отображение элментов

        source_text = wx.TextCtrl(panel, value="Исходный текст", size=(850, 100),
                                  style=wx.TE_MULTILINE | wx.TE_READONLY)
        translate_text = wx.TextCtrl(panel, value="Перевод", size=(850, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # размещение виджетов
        vbox.Add(self.dataOlv, proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=10)


        box_for_srctext = wx.BoxSizer(wx.HORIZONTAL)
        box_for_srctext.Add(source_text, proportion=1)
        vbox.Add(box_for_srctext, flag=wx.EXPAND | wx.BOTTOM, border=10)

        box_for_trctext = wx.BoxSizer(wx.HORIZONTAL)
        box_for_trctext.Add(translate_text, proportion=1)
        vbox.Add(box_for_trctext, flag=wx.EXPAND)

    # функции событий

    def onQuit(self, event):
        self.Close()

    def OnOpen(self, event):
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open file", wildcard="All files|*.po",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf-8') as file:
                    parse(file.name)
                    self.dataOlv.SetObjects(data.get_notes())
            except IOError:
                wx.LogError("Cannot open file '%s'.")

    def onSave(self, event):
        pass

    def onTranslate(self, event):
        po = data.get_pofile()
        for item in po:
            request_result = json.loads(translate(item.msgid))
            item.msgstr = request_result["translated_text"]
        data.set_pofile(po)
        to_note_list(po)
        self.dataOlv.SetObjects(data.get_notes())


app = wx.App()
frame = MyFrame(None, 'translate')
frame.SetSize(800, 700)
frame.Center()
frame.Show()
app.MainLoop()