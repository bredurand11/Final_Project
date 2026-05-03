from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from lab1logic import Logic

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Logic()
    window.show()
    sys.exit(app.exec())