import sys
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import *
import os
 


class MyStream(object):
    def write(self, text):
        # Add text to a QTextEdit...

sys.stdout = MyStream()




class EmittingStream(QtCore.QObject):
	textWritten = QtCore.pyqtSignal(str)
	def write(self, text):
		self.textWritten.emit(str(text))

class MainWindow():
	def __init__(self, parent=None, **kwargs):
		# ...

		# Install the custom output stream
		sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)

	def __del__(self):
		# Restore sys.stdout
		sys.stdout = sys.__stdout__

	def normalOutputWritten(self, text):
		"""Append text to the QTextEdit."""
		# Maybe QTextEdit.append() works as well, but this is how I do it:
		cursor = self.textEdit.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.textEdit.setTextCursor(cursor)
		self.textEdit.ensureCursorVisible()

# create our window
app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle('MAP-HEVC')
 
# Create textbox
textbox = QLineEdit(w)
textbox.move(20, 20)
textbox.resize(280,40)
 
# Set window size. 
w.resize(320, 150)
 
# Create a button in the window
button = QPushButton('Run', w)
button.move(20,80)

sys.stdout = EmittingStream();

# Create the actions 
@pyqtSlot()
def on_click():
	os.system("python teste.py")
# connect the signals to the slots
button.clicked.connect(on_click)



# Show the window and run the app
w.show()
app.exec_()



