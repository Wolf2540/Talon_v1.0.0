import sys
import curses
import npyscreen
from npyscreen import npysThemeManagers as ThemeManagers
import os

class EmuTheme(ThemeManagers.ThemeManager):
    default_colors = {
        'DEFAULT'     : 'CYAN_BLACK',
        'FORMDEFAULT' : 'WHITE_BLACK',
        'NO_EDIT'     : 'BLUE_BLACK',
        'STANDOUT'    : 'CYAN_BLACK',
        'CURSOR'      : 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL'       : 'YELLOW_BLACK',
        'LABELBOLD'   : 'WHITE_BLACK',
        'CONTROL'     : 'WHITE_BLACK',
        'WARNING'     : 'RED_BLACK',
        'CRITICAL'    : 'BLACK_RED',
        'GOOD'        : 'YELLOW_BLACK',
        'GOODHL'      : 'YELLOW_BLACK',
        'VERYGOOD'    : 'BLACK_GREEN',
        'CAUTION'     : 'YELLOW_BLACK',
        'CAUTIONHL'   : 'BLACK_YELLOW',
    }

class TextEditorApp(npyscreen.NPSAppManaged):
    def __init__(self, filename=None):
        self.filename = filename
        self.temp_content = ""  # Shared attribute to store content
        super(TextEditorApp, self).__init__()

    def onStart(self):
        npyscreen.setTheme(EmuTheme)
        name = self.filename if self.filename else "Untitled"
        self.addForm('MAIN', MainForm, name=name, filename=self.filename)
        self.addFormClass('SAVEAS', SaveAsPopup)


class MainForm(npyscreen.ActionForm):
    def create(self):
        self.filename = self.parentApp.filename
        self.editor = self.add(npyscreen.MultiLineEdit, name="Content:", max_height=None)

        # Load file contents if a valid filename is provided
        if self.filename and os.path.isfile(self.filename):
            with open(self.filename, 'r') as file:
                self.editor.value = file.read()

    def on_ok(self):
        if not self.filename:
            self.parentApp.temp_content = self.editor.value  # Store editor content in shared attribute
            self.parentApp.switchForm('SAVEAS')
        else:
            with open(self.filename, 'w') as file:
                file.write(self.editor.value)
            npyscreen.notify_confirm("File saved successfully", title="Success")

    def on_cancel(self):
        self.parentApp.setNextForm(None)


class SaveAsPopup(npyscreen.ActionPopup):
    def create(self):
        self.filename = self.add(npyscreen.TitleText, name="Enter filename:")

    def on_ok(self):
        filename = self.filename.value
        if filename:
            with open(filename, 'w') as file:
                file.write(self.parentApp.temp_content)  # Write the shared content to the file
            npyscreen.notify_confirm("File saved successfully", title="Success")
            main_form = self.parentApp.getForm('MAIN')
            main_form.filename = filename
            main_form.name = filename
            self.parentApp.switchForm('MAIN')
        else:
            npyscreen.notify_confirm("Filename not provided", title="Error")

    def on_cancel(self):
        self.parentApp.switchForm('MAIN')

def run(arg):
    app = TextEditorApp(filename=arg)
    app.run()

if __name__ == "__main__":
    try:
        filename = input("Emu v1 >> \\filename$-").strip()
        if filename.lower() in ["quit", "q"]: sys.exit(0)
        app = TextEditorApp(filename=filename)
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)
