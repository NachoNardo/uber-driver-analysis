from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QPushButton,
    QHBoxLayout
)


class RefillView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Refills")
        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Value",
            "Liters",
            "Current Distance Traveled"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

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
