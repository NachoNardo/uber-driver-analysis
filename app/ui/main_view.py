import sys
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton
)
from PyQt6.QtCore import Qt


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UberAnalysis")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.travels_button = QPushButton("Travels")
        self.refills_button = QPushButton("Refills")
        self.analysis_button = QPushButton("Analysis")

        for button in (
            self.travels_button,
            self.refills_button,
            self.analysis_button,
        ):
            button.setMinimumHeight(40)
            button.setMinimumWidth(200)

        layout.addWidget(self.travels_button)
        layout.addWidget(self.refills_button)
        layout.addWidget(self.analysis_button)

        central_widget.setLayout(layout)

        self.adjustSize()
        self.setFixedSize(self.size())
