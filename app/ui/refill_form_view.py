from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDoubleSpinBox,
    QPushButton,
    QHBoxLayout,
    QLayout
)
from PyQt6.QtCore import Qt


class RefillFormView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Refill")
        self.resize(400, 200)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        form_layout = QFormLayout()

        self.id_input = QLineEdit()
        self.id_input.setDisabled(True)

        self.value_input = QDoubleSpinBox()
        self.value_input.setDecimals(2)
        self.value_input.setMaximum(9999999.99)

        self.liters_input = QDoubleSpinBox()
        self.liters_input.setDecimals(3)
        self.liters_input.setMaximum(999999.999)

        self.current_distance_traveled_input = QDoubleSpinBox()
        self.current_distance_traveled_input.setDecimals(2)
        self.current_distance_traveled_input.setMaximum(9999999.99)

        form_layout.addRow("ID", self.id_input)
        form_layout.addRow("Value", self.value_input)
        form_layout.addRow("Liters", self.liters_input)
        form_layout.addRow("Current Distance Traveled", self.current_distance_traveled_input)

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
