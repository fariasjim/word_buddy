"""
WordBuddy - A PyQt5 borderless, draggable, centered window.

This module creates a custom QWidget window with the following features:
- Frameless (no title bar or borders)
- Black background
- Starts centered on the screen
- Can be moved by clicking and dragging anywhere on the window

Usage:
    Run this file directly to launch the WordBuddy window.
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import sys


class WordBuddy(QtWidgets.QWidget):
    """
    Main application window for WordBuddy.

    Features:
    - Frameless window
    - Black background
    - Centered on screen at startup
    - Moveable by dragging with left mouse button
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("WordBuddy")
        self.resize(600, 400)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Borderless window
        self.setStyleSheet("background-color: black;")
        self._offset = None
        self.center_window()

    def center_window(self):
        """
        Centers the window on the primary screen.
        """
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)

    def mousePressEvent(self, event):
        """
        Records the mouse position when the left button is pressed.
        Enables window dragging.
        """
        if event.button() == QtCore.Qt.LeftButton:
            self._offset = event.pos()

    def mouseMoveEvent(self, event):
        """
        Moves the window as the mouse is dragged with the left button held.
        """
        if self._offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self._offset)

    def mouseReleaseEvent(self, event):
        """
        Resets the drag offset when the mouse button is released.
        """
        self._offset = None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WordBuddy()
    window.show()
    sys.exit(app.exec_())