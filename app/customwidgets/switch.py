from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect, pyqtProperty, Qt
from PyQt5.QtGui import QColor, QPainter

class Switch(QCheckBox):
    def __init__(self, parent=None):
        super(Switch, self).__init__(parent)
        self.setFixedSize(60, 35)

        self._offset = 0

        self._animation = QPropertyAnimation(self, b"offset", self)
        self._animation.setEasingCurve(QEasingCurve.InOutSine)
        self._animation.setDuration(100)

        self.stateChanged.connect(self.start_transition)

        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("QCheckBox::indicator { width: 0; height: 0; }")

    def start_transition(self, state):
        if state:
            self._animation.setStartValue(self._offset)
            self._animation.setEndValue(25)
        else:
            self._animation.setStartValue(self._offset)
            self._animation.setEndValue(0)
        self._animation.start()

    def getOffset(self):
        return self._offset

    def setOffset(self, value):
        self._offset = value
        self.update()

    offset = pyqtProperty(int, getOffset, setOffset)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        margin = 5
        switch_width = 50
        switch_height = 25

        if self.isChecked():
            p.setBrush(QColor(0, 200, 0))
        else:
            p.setBrush(QColor(150, 150, 150))
        p.setPen(Qt.NoPen)
        background_rect = QRect(margin, margin, switch_width, switch_height)
        p.drawRoundedRect(background_rect, switch_height / 2, switch_height / 2)

        p.setBrush(QColor(255, 255, 255))
        handle_rect = QRect(margin + self._offset, margin, switch_height, switch_height)
        p.drawEllipse(handle_rect)

    def mousePressEvent(self, event):
        self.toggle()
        super(Switch, self).mousePressEvent(event)
