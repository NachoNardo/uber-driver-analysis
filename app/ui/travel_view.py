from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QPushButton,
    QHBoxLayout,
    QHeaderView
)


class TravelView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Travels")
        self.resize(1200, 500)

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "Total Value",
            "Street Start",
            "Neighborhood Start",
            "Street End",
            "Neighborhood End",
            "Distance Start",
            "Distance Travel",
            "Time Start",
            "Time Reach",
            "Time End",
            "Time Total"
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        self.table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)

        buttons_layout = QHBoxLayout()

        self.new_button = QPushButton("New")
        self.edit_button = QPushButton("Edit")
        self.cancel_button = QPushButton("Cancel")

        buttons_layout.addWidget(self.new_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addWidget(self.table)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.adjustSize()
        self.setFixedSize(self.size())
