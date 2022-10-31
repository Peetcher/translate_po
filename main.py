import wx
from ObjectListView import ObjectListView, ColumnDefn
from MyLib import parse
from data import data
from Translate import *
from configparser import ConfigParser
import datetime
from loguru import logger

logger.add("report.log", format="{time} {level} {message}", level="DEBUG", rotation="20KB", compression="zip")

config = ConfigParser()
config.read("config.ini")


class SettingsDialog(wx.Dialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent, title="Настройки", size=(500, 300))

        vertical_box = wx.BoxSizer(wx.VERTICAL)
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_box_user = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_box_email = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_box2 = wx.BoxSizer(wx.HORIZONTAL)
        panel = wx.Panel(self)
        panel.SetSizer(vertical_box)

        api_label_api = wx.StaticText(panel, label="API-ключ:")
        if config["user"]["api_key"] is None:
            config["user"]["api_key"] = "вставьте ключ"
        else:
            self.user_input_api = wx.TextCtrl(panel, wx.ID_ANY, value=config["user"]["api_key"])

        api_label_user = wx.StaticText(panel, label="Пользователь:")

        self.user_input_user = wx.TextCtrl(panel, wx.ID_ANY, value="")

        if data.get_pofile() is None:
            self.user_input_user.SetValue("")
        else:
            self.user_input_user.SetValue(data.get_pofile().metadata['Last-Translator'])

        api_label_email = wx.StaticText(panel, label="Email:")

        self.user_input_email = wx.TextCtrl(panel, wx.ID_ANY, value="")
        if data.get_pofile() is None:
            self.user_input_email.SetValue("")
        else:
            self.user_input_email.SetValue(data.get_pofile().metadata['Report-Msgid-Bugs-To'])

        horizontal_box.Add(api_label_api, flag=wx.RIGHT, border=10)
        horizontal_box.Add(self.user_input_api, proportion=1)
        vertical_box.Add(horizontal_box, flag=wx.EXPAND | wx.ALL, border=10)

        horizontal_box_user.Add(api_label_user, flag=wx.RIGHT, border=10)
        horizontal_box_user.Add(self.user_input_user, proportion=1)
        vertical_box.Add(horizontal_box_user, flag=wx.EXPAND | wx.ALL, border=10)

        horizontal_box_email.Add(api_label_email, flag=wx.RIGHT, border=10)
        horizontal_box_email.Add(self.user_input_email, proportion=1)
        vertical_box.Add(horizontal_box_email, flag=wx.EXPAND | wx.ALL, border=10)

        ok_button = wx.Button(panel, wx.ID_OK, label="ок")
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label="отмена")

        horizontal_box2.Add(ok_button, flag=wx.LEFT, border=10)
        horizontal_box2.Add(cancel_button, flag=wx.LEFT, border=10)
        vertical_box.Add(horizontal_box2, flag=wx.ALIGN_RIGHT | wx.BOTTOM | wx.RIGHT | wx.TOP, border=10)
        self.user_input_api.GetValue()


class TranslateDialog(wx.Dialog):
    def __init__(self, parent, title):
        super(TranslateDialog, self).__init__(parent, title="Параметры перевода")

        vertical_box = wx.BoxSizer(wx.VERTICAL)
        horizontal_box1 = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_box2 = wx.BoxSizer(wx.HORIZONTAL)

        values = ["Всё", "Только выделенное", "Только непереведённое", "Непереведённое и выделенное"]
        self.radiobox = wx.RadioBox(self, label="Параметры перевода", size=(500, 400), choices=values,
                                    style=wx.RA_SPECIFY_ROWS)
        translate_button = wx.Button(self, wx.ID_OK, label="Перевести")
        cancel_button = wx.Button(self, wx.ID_CANCEL, label="Отмена")

        self.radiobox.Bind(wx.EVT_RADIOBOX, self.radiobox_event)

        horizontal_box1.Add(self.radiobox)
        horizontal_box2.Add(translate_button, flag=wx.ALL, border=10)
        horizontal_box2.Add(cancel_button, flag=wx.ALL, border=10)

        vertical_box.Add(horizontal_box1, proportion=1)
        vertical_box.Add(horizontal_box2, flag=wx.ALIGN_RIGHT)
        self.SetSizer(vertical_box)

    def radiobox_event(self, event):
        data.set_radiobox_selection(self.radiobox.GetSelection())


class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vbox)

        '''панель----------------------------------------------------------------------------------------------------'''

        # панель-меню
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        view = wx.Menu()
        translate = wx.Menu()
        about = wx.Menu()

        # добавление кнопок на панель окна
        menubar.Append(fileMenu, '&Файл')
        menubar.Append(view, '&Вид')
        menubar.Append(translate, '&Перевод')
        menubar.Append(about, '&Справка')

        # кнопки для панели File
        open_btn = wx.MenuItem(fileMenu, wx.ID_OPEN, 'Открыть')
        save_btn = wx.MenuItem(fileMenu, wx.ID_SAVE, 'Сохранить как')
        setting_btn = wx.MenuItem(fileMenu, wx.ID_SETUP, 'Настройки')
        exit_btn = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Выход', 'Выход из приложения')

        # кнопки для панели translate
        translate_btn = wx.MenuItem(translate, wx.ID_ANY, 'Параметры перевода')

        # кнопки для справка
        about_file_btn = wx.MenuItem(about, wx.ID_ABOUT, "Справка о файле")
        about_program_btn = wx.MenuItem(about, wx.ID_ANY, "Справка о программе")

        # добавление кнопок в view
        self.status = view.Append(wx.ID_VIEW_DETAILS, "показать выделение", kind=wx.ITEM_CHECK)
        self.sort_by_translate = view.Append(wx.ID_ANY, "сортировать по переводу")
        self.sort_by_source = view.Append(wx.ID_ANY, "сортировать по исходному тексту")

        # добавление кнопок в File
        fileMenu.Append(open_btn)
        fileMenu.Append(save_btn)
        fileMenu.AppendSeparator()
        fileMenu.Append(setting_btn)
        fileMenu.AppendSeparator()
        fileMenu.Append(exit_btn)

        # добавление кнопок в Translate
        translate.Append(translate_btn)

        # добавление кнопок в about
        about.Append(about_file_btn)
        about.Append(about_program_btn)

        self.SetMenuBar(menubar)

        '''dataObjectListview----------------------------------------------------------------------------------------'''

        self.dataOlv = ObjectListView(panel, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_NONE
        self.dataOlv.useExpansionColumn = True
        self.dataOlv.SetEmptyListMsg("Файл не выбран")

        # cтолбцы

        self.id_column = ColumnDefn("Id", "left", 50, "id")
        self.source_column = ColumnDefn("Исходный текст", "left", 350, "source_text", isSpaceFilling=True)
        self.translate_column = ColumnDefn("Переведенный текст", "left", 350, "translate_text", isSpaceFilling=True)
        self.comments_column = ColumnDefn("Комментарии", "left", 100, "commentary")

        self.dataOlv.SetColumns(
            [
                self.id_column,
                self.source_column,
                self.translate_column,
                self.comments_column

            ]

        )
        '''Labels----------------------------------------------------------------------------------------------------'''

        self.source_text_label = wx.StaticText(panel, label="Исходный текст")
        self.translate_text_label = wx.StaticText(panel, label="Перевод")
        self.commentary_label = wx.StaticText(panel, label="Комментарии")

        '''текстовые поля для отображение элментов-------------------------------------------------------------------'''

        self.source_text = wx.TextCtrl(panel, value="", size=(850, 100), style=wx.TE_MULTILINE)
        self.translate_text = wx.TextCtrl(panel, value="", size=(850, 100), style=wx.TE_MULTILINE)
        self.comments = wx.TextCtrl(panel, value="", size=(300, 200), style=wx.TE_MULTILINE | wx.TE_READONLY)

        '''Перевод Выбрать-------------------------------------------------------------------------------------------'''
        values = ["Всё", "Только выделенное", "Только непереведённое", "Непереведённое и выделенное"]
        self.radiobox = wx.RadioBox(panel, label="Параметры перевода", choices=values, majorDimension=4,
                                    style=wx.RA_SPECIFY_COLS)
        translate_button = wx.Button(panel, wx.ID_ANY, label="Перевести")
        self.select_button = wx.Button(panel, wx.ID_ANY, label="Выбрать")

        '''Status bar------------------------------------------------------------------------------------------------'''

        self.statusbar = self.CreateStatusBar(style=wx.STB_DEFAULT_STYLE)

        '''размещение виджетов---------------------------------------------------------------------------------------'''
        vbox.Add(self.dataOlv, proportion=1, flag=wx.EXPAND | wx.BOTTOM, border=5)

        box_for_top_labels = wx.BoxSizer(wx.HORIZONTAL)
        box_for_top_labels.Add(self.source_text_label, wx.EXPAND)
        box_for_top_labels.Add(self.commentary_label)

        vbox.Add(box_for_top_labels, flag=wx.EXPAND | wx.RIGHT | wx.LEFT, border=5)

        box_for_text = wx.BoxSizer(wx.VERTICAL)
        # box_for_text.Add(self.source_text_label, flag=wx.EXPAND | wx.ALL, border=3)
        box_for_text.Add(self.source_text)
        box_for_text.Add(self.translate_text_label, flag=wx.TOP | wx.BOTTOM | wx.LEFT, border=5)
        box_for_text.Add(self.translate_text)

        box_for_all_text = wx.BoxSizer(wx.HORIZONTAL)
        box_for_all_text.Add(box_for_text, flag=wx.RIGHT, border=5)
        box_for_all_text.Add(self.comments, proportion=1, flag=wx.EXPAND)

        vbox.Add(box_for_all_text, flag=wx.EXPAND)

        box_for_radiobox = wx.BoxSizer(wx.HORIZONTAL)
        box_for_radiobox.Add(self.radiobox)
        box_for_radiobox.Add(translate_button, flag=wx.TOP | wx.LEFT, border=15)
        box_for_radiobox.Add(self.select_button, flag=wx.TOP | wx.LEFT, border=15)
        vbox.Add(box_for_radiobox, flag=wx.ALL, border=5)

        '''События---------------------------------------------------------------------------------------------------'''

        self.Bind(wx.EVT_MENU, self.on_open, open_btn)
        self.Bind(wx.EVT_MENU, self.on_save, save_btn)
        self.Bind(wx.EVT_MENU, self.on_quit, exit_btn)
        self.Bind(wx.EVT_MENU, self.on_translate_menu, translate_btn)
        self.Bind(wx.EVT_BUTTON, self.on_translate, translate_button)
        self.Bind(wx.EVT_MENU, self.on_chekbox_view, id=wx.ID_VIEW_DETAILS)
        self.Bind(wx.EVT_BUTTON, self.on_chekbox_view, self.select_button)
        self.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.click_handler, self.dataOlv)
        self.Bind(wx.EVT_TEXT, self.change_text, self.source_text)
        self.Bind(wx.EVT_TEXT, self.change_text, self.translate_text)
        self.Bind(wx.EVT_MENU, self.on_sort_translate, self.sort_by_translate)
        self.Bind(wx.EVT_MENU, self.on_sort_source, self.sort_by_source)
        self.Bind(wx.EVT_MENU, self.on_settings, setting_btn)
        self.Bind(wx.EVT_MENU, self.on_about, about_file_btn)
        self.Bind(wx.EVT_MENU, self.on_about_program, about_program_btn)
        self.radiobox.Bind(wx.EVT_RADIOBOX, self.radiobox_event)

    '''Обработчики событий-------------------------------------------------------------------------------------------'''

    def radiobox_event(self, event):
        data.set_radiobox_selection(self.radiobox.GetSelection())

    def on_about_program(self, event):
        wx.MessageBox(f"translatepo beta version", caption="Информация о программе", style=wx.OK)

    def on_about(self, event):
        if data.get_pofile() is None:
            wx.MessageBox("Файл не выбран")
        else:
            meta = data.get_pofile().metadata
            header = data.get_pofile().header
            wx.MessageBox(f" {header} {meta}", caption="Информация о файле", style=wx.OK)

    def on_settings(self, event):
        with SettingsDialog(self) as dialog:
            result = dialog.ShowModal()
            if result == wx.ID_OK:
                config["user"]["api_key"] = dialog.user_input_api.GetValue()
                config["user"]["translator"] = dialog.user_input_user.GetValue()
                config["user"]["email"] = dialog.user_input_email.GetValue()
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            else:
                return

    def on_sort_source(self, event):
        self.dataOlv.SortBy(1)

    def on_sort_translate(self, event):
        self.dataOlv.SortBy(2)

    def change_text(self, event):
        if data.get_pofile() is None:
            return
        id = self.dataOlv.GetSelectedObject().id
        po = data.get_pofile()
        if event.GetEventObject() is self.source_text:
            if po[id].msgid == self.source_text.Value:
                return
            po[id].msgid = self.source_text.Value
            refresh(po, self.dataOlv, self.statusbar)
            self.dataOlv.SelectObject(data.get_notes()[id])
        else:
            if po[id].msgstr == self.translate_text.Value:
                return
            po[id].msgstr = self.translate_text.Value
            refresh(po, self.dataOlv, self.statusbar)
            self.dataOlv.SelectObject(data.get_notes()[id])

    def click_handler(self, event):
        try:
            id = self.dataOlv.GetSelectedObject().id
            po = data.get_pofile()
            self.source_text.SetValue(po[id].msgid)
            self.translate_text.SetValue(po[id].msgstr)
            self.comments.SetValue(str(self.dataOlv.GetSelectedObject().commentary))
        except AttributeError:
            pass

    def on_quit(self, event):
        self.Close()

    def on_open(self, event):
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
                    self.statusbar.SetStatusText(f'переведено {data.get_pofile().percent_translated()} %')
            except IOError:
                wx.LogError("Cannot open file '%s'.")
                logger.error("error opening file")

    def on_save(self, event):
        if data.get_pofile() is None:
            wx.MessageBox('файл не выбран')
            return
        else:
            filedialog = wx.FileDialog(
                self, message="Save file as ...",
                defaultDir=".",
                defaultFile="newfile", wildcard="*.*", style=wx.FD_SAVE
            )
            if filedialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = filedialog.GetPath()
            po = data.get_pofile()
            po.metadata['Report-Msgid-Bugs-To'] = config["user"]["email"]
            po.metadata['Last-Translator'] = config["user"]["translator"]
            po.metadata['PO-Revision-Date'] = datetime.datetime.now()
            data.set_pofile(po)
            data.get_pofile().save(f"{pathname}.po")
            data.get_pofile().save_as_mofile(f'{pathname}.mo')

            logger.info("Save successfully!")

    def on_translate_menu(self, event):
        with TranslateDialog(self, title="Параметры") as dialog:
            res = dialog.ShowModal()
            if res == wx.ID_OK:
                self.on_translate(self)

    def on_chekbox_view(self, event):
        if event.Id == 5042:
            if self.status.IsChecked():
                self.dataOlv.InstallCheckStateColumn(self.id_column)
                self.dataOlv.SetObjects(data.get_notes())
            else:
                self.dataOlv.InstallCheckStateColumn(None)
                self.dataOlv.SetObjects(data.get_notes())
        else:
            self.dataOlv.InstallCheckStateColumn(self.id_column)
            self.dataOlv.SetObjects(data.get_notes())

    @logger.catch
    def on_translate(self, event):
        if data.get_pofile() is None:
            wx.MessageBox('файл не выбран')
            return
        else:
            try:
                if data.get_radiobox_selection() == 0:
                    translate_all(data.get_pofile(), self.dataOlv, self)  # перевод всего
                elif data.get_radiobox_selection() == 1:
                    translate_selected(data.get_pofile(), self.dataOlv, self)  # перевод только выделенных
                elif data.get_radiobox_selection() == 2:
                    translate_untranslated(data.get_pofile(), self.dataOlv, self)  # только непереведённых
                elif data.get_radiobox_selection() == 3:
                    translate_selected_and_untrans(data.get_pofile(), self.dataOlv, self)  # непереведённых и выделенных
            except KeyError:
                error = json.loads(data.get_response_error())["message"]
                logger.error(f"ошибка API :{error}")
                wx.MessageBox(f"ошибка API :{error}")


app = wx.App()
frame = MyFrame(None, 'translate')
frame.SetSize(1300, 800)
frame.Center()
frame.Show()
app.MainLoop()
