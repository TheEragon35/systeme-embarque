
from main_window import *
from popup import Ui_Form
import sys
from PySide2.QtWidgets import QApplication, QMainWindow

class Listener(QMainWindow):

    def __init__(self):
        super(Listener, self).__init__()
        print("hello")
        self.main_window = Ui_UselessWindow()
        self.main_window.setupUi(self)


        self.catButton.connect(self.catPopUp())

    def catPopUp(self):
        print("ehllo")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Listener()
    # app.run()

    sys.exit(app.exec())

    