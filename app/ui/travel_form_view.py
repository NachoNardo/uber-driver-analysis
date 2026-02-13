from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QSpinBox,
    QDateTimeEdit,
    QPushButton,
    QHBoxLayout
)
from PyQt6.QtCore import QDateTime


class TravelFormView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Travel")
        self.setMinimumSize(600, 600)

        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.id_input.setDisabled(True)

        self.total_value_input = QDoubleSpinBox()
        self.total_value_input.setDecimals(2)
        self.total_value_input.setMaximum(9999999.99)

        self.street_start_input = QLineEdit()
        self.neiborghood_start_input = QLineEdit()

        self.street_end_input = QLineEdit()
        self.neiborghood_end_input = QLineEdit()

        self.distance_start_input = QDoubleSpinBox()
        self.distance_start_input.setDecimals(2)
        self.distance_start_input.setMaximum(999999.99)

        self.distance_travel_input = QDoubleSpinBox()
        self.distance_travel_input.setDecimals(2)
        self.distance_travel_input.setMaximum(999999.99)

        self.time_start_input = QDateTimeEdit()
        self.time_start_input.setCalendarPopup(True)
        self.time_start_input.setDateTime(QDateTime.currentDateTime())

        self.time_reach_input = QDateTimeEdit()
        self.time_reach_input.setCalendarPopup(True)
        self.time_reach_input.setDateTime(QDateTime.currentDateTime())

        self.time_end_input = QDateTimeEdit()
        self.time_end_input.setCalendarPopup(True)
        self.time_end_input.setDateTime(QDateTime.currentDateTime())

        self.time_total_input = QSpinBox()
        self.time_total_input.setMaximum(999999)

        form_layout.addRow("ID", self.id_input)
        form_layout.addRow("Total Value", self.total_value_input)
        form_layout.addRow("Street Start", self.street_start_input)
        form_layout.addRow("Neighborhood Start", self.neiborghood_start_input)
        form_layout.addRow("Street End", self.street_end_input)
        form_layout.addRow("Neighborhood End", self.neiborghood_end_input)
        form_layout.addRow("Distance Start", self.distance_start_input)
        form_layout.addRow("Distance Travel", self.distance_travel_input)
        form_layout.addRow("Time Start", self.time_start_input)
        form_layout.addRow("Time Reach", self.time_reach_input)
        form_layout.addRow("Time End", self.time_end_input)
        form_layout.addRow("Time Total", self.time_total_input)

        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.delete_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.adjustSize()
        self.setFixedSize(self.size())
