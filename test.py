from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QFontDatabase

app = QApplication([])

# Get a list of available font families
font_families = QFontDatabase().families()

# Create a widget to display text
widget = QWidget()
layout = QVBoxLayout(widget)

# Output "Hello" using each font
for font_family in font_families:
    label = QLabel(f"Hello - {font_family}", widget)

    # Set the font for the label
    font = label.font()
    font.setFamily(font_family)
    font.setPointSize(14)  # Set your desired font size
    label.setFont(font)

    layout.addWidget(label)

widget.show()
app.exec_()
