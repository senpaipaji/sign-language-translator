import sys
from PyQt5 import uic  
from PyQt5.QtWidgets import QApplication,QWidget

class MyForm(QWidget):  # Create a class for your form
    def __init__(self):
        super().__init__()
        uic.loadUi("form.ui", self)  # Load the UI file into this class

        # Your application logic and event handling will go here

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create a QApplication instance
    window = MyForm()  # Create an instance of your form class
    window.show()  # Display the window
    sys.exit(app.exec_())  # Start the Qt event loop    