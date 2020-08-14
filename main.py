# Copper Text Editor, ver. 0.9
import sys, os
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow, QApplication

ver = "0.9"

# Main application class
class MainWindow(QMainWindow):

    # Initialization function
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load .ui file from root directory
        uic.loadUi('MainWindow.ui', self)

        # Disable rich text
        self.textEdit.setAcceptRichText(False)

        # Create variable to hold path of opened or saved file
        self.filename = ""

        self.title_update()

        # Connect signals with actions
        self.actionNew.triggered.connect(self.new)
        self.actionOpen.triggered.connect(self.open)
        self.actionMenuOpen.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save)
        self.actionMenuSave.triggered.connect(self.save)
        self.actionMenuSave_as.triggered.connect(self.save_as)
        self.actionMenuAbout_Qt.triggered.connect(self.about_qt)
        self.actionMenuAbout.triggered.connect(self.about)
        self.actionCopy.triggered.connect(self.copy)
        self.actionMenuCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionMenuPaste.triggered.connect(self.paste)
        self.actionCut.triggered.connect(self.cut)
        self.actionMenuCut.triggered.connect(self.cut)
        self.actionMenuQuit.triggered.connect(self.quit)
        self.actionToggleWrap.triggered.connect(self.wrap_toggle)

    # Displays About Qt dialog
    def about_qt(self):
        QMessageBox.aboutQt(None, "")

    # Displays custom About dialog
    def about(self):
        # Checks Python version and converts it to list
        pyver = sys.version
        pyver = pyver.split()
        # Setup dialog
        abt = QMessageBox(self)
        abt.setWindowTitle("About")
        abt.setText("Copper Text Editor")
        abt.setInformativeText(f"A simple, lightweight text editor for Windows, Mac and Linux. \n \nVersion: {ver} \nPython: {str(pyver[0])}")
        abt.setDetailedText("Credits: \nSome icons by Yusuke Kamiyamane. Licensed under a Creative Commons Attribution 3.0 License. \nhttps://creativecommons.org/licenses/by/3.0/")
        abt.setIcon(QMessageBox.Information)
        abt.exec_()

    def quit(self):
        sys.exit()

    def open(self):
        # Open file explorer dialog
        self.filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);;All files (*.*)")
        # Try to read data from opened document
        try:
            with open(self.filename, newline='', encoding='utf8') as f:
                self.textEdit.setText(f.read())
                self.title_update()
        # if exception, show error message
        except Exception as e:
            print(str(e))

    def new(self):
        # If file wasn't saved and New button pressed, displays warning dialog with Yes, Save and Cancel buttons
        if not self.filename:
            wrn = QMessageBox(self)
            wrn.setWindowTitle("Save warning")
            wrn.setText("This file has not been saved yet. Do you want to create a new file anyway?")
            wrn.setIcon(QMessageBox.Warning)
            wrn.setStandardButtons(QMessageBox.Yes | QMessageBox.Save | QMessageBox.Cancel)
            msg = wrn.exec_()
            if msg == QMessageBox.Yes:
                self.filename = ""
                self.textEdit.clear()
                self.title_update()
            elif msg == QMessageBox.Save:
                self.save_as()
            elif msg == QMessageBox.Cancel:
                return
        # else clear filename and textEdit
        else:
            self.filename = ""
            self.textEdit.clear()

    def save(self):
        # If file wasn't saved and Save button pressed, call function save_as()
        if not self.filename:
            self.save_as()
        # else try to save changes to opened file
        try:
            with open(self.filename, "w", encoding='utf8') as f:
                f.write(self.textEdit.toPlainText())
        except:
            return

    def save_as(self):
        # Open file explorer dialog
        self.filename, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);;All files (*.*)")
        # Try to save changes
        try:
            with open(self.filename, "w", encoding='utf8') as f:
                f.write(self.textEdit.toPlainText())
                self.statusbar.showMessage(f"File saved in: {self.filename}")
                self.title_update()
        # if exception, show error message
        except Exception as e:
            print(str(e))

    def title_update(self):
        filetext = (os.path.basename(self.filename) if self.filename else "Untitled")
        self.setWindowTitle(f"{filetext} - Copper Text Editor")

    def copy(self):
        self.textEdit.copy()

    def paste(self):
        self.textEdit.paste()

    def cut(self): 
        self.textEdit.cut()
    
    def wrap_toggle(self):
        self.textEdit.setLineWrapMode(1 if self.textEdit.lineWrapMode() == 0 else 0)


# Load functions and initialize app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())