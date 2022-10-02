import wx
import os
from ObjectListView import ObjectListView, ColumnDefn
from MyLib import Parse


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

        menubar.Append(fileMenu, '&Файл')
        menubar.Append(edit, '&Правка')
        menubar.Append(view, '&Вид')

        # кнопки в панель меню Файл
        open_btn = wx.MenuItem(fileMenu, wx.ID_OPEN, 'Открыть')
        create_btn = wx.MenuItem(fileMenu, wx.ID_FILE, 'Создать')
        save_btn = wx.MenuItem(fileMenu, wx.ID_SAVE, 'Сохранить')
        exit_btn = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Выход', 'Выход из приложения')

        fileMenu.Append(open_btn)
        fileMenu.Append(create_btn)
        fileMenu.Append(save_btn)
        fileMenu.Append(exit_btn)

        self.SetMenuBar(menubar)

        # события кнопок
        self.Bind(wx.EVT_MENU, self.OnOpen, open_btn)
        # self.Bind(wx.EVT_MENU, self. , create_btn)
        self.Bind(wx.EVT_MENU, self.onSave, save_btn)
        self.Bind(wx.EVT_MENU, self.onQuit, exit_btn)

        # виджеты

        self.dataOlv = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.SetColumns(
            [
                ColumnDefn("id", "left", 50, "Id"),
                ColumnDefn("source_text", "left", 350, "Source text"),
                ColumnDefn("translation_text", "left", 350, "translation text"),
                ColumnDefn("marker", "left", 50, "marker")
            ]

        )

        source_text = wx.TextCtrl(panel, value="Исходный текст", size=(850, 100), style=wx.TE_MULTILINE |
                                                                                        wx.TE_READONLY)
        translate_text = wx.TextCtrl(panel, value="Перевод", size=(850, 100), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # размещение виджетов

        box_for_table = wx.BoxSizer(wx.HORIZONTAL)
        box_for_table.Add(self.dataOlv, proportion=1)
        vbox.Add(box_for_table, flag=wx.EXPAND | wx.BOTTOM, border=10,)

        box_for_srctext = wx.BoxSizer(wx.HORIZONTAL)
        box_for_srctext.Add(source_text, proportion=1)
        vbox.Add(box_for_srctext, flag=wx.EXPAND |wx.BOTTOM, border=10)

        box_for_trctext = wx.BoxSizer(wx.HORIZONTAL)
        box_for_trctext.Add(translate_text, proportion=1)
        vbox.Add(box_for_trctext, flag=wx.EXPAND)

    def onQuit(self, event):
        self.Close()

    def OnOpen(self, event,):
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open file", wildcard="All files|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r', encoding='utf-8') as file:
                    Parse(file)
            except IOError:
                wx.LogError("Cannot open file '%s'.")

    def onSave(self, event):
        print('save sucsesfull')

app = wx.App()
frame = MyFrame(None, 'translate')
frame.SetSize(800, 700)
frame.Center()
frame.Show()
app.MainLoop()
