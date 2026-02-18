from decimal import Decimal

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from sqlalchemy.orm import sessionmaker

from app.db.session import engine
from app.service.refill_service import RefillService
from app.ui.refill_form_view import RefillFormView


class RefillView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Refills")
        self.setMinimumSize(600, 400)

        session_factory = sessionmaker(bind=engine)
        self.session = session_factory()
        self.service = RefillService(self.session)

        self.form_view = None
        self.refills = []
        self._is_closing = False

        main_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels([
            "Value",
            "Liters",
            "Current Distance Traveled",
        ])
        self.table.horizontalHeader().setStretchLastSection(True)

        buttons_layout = QHBoxLayout()

        self.new_button = QPushButton("New")
        self.edit_button = QPushButton("Edit")
        self.cancel_button = QPushButton("Cancel")

        self.new_button.clicked.connect(self.open_new_form)
        self.edit_button.clicked.connect(self.open_edit_form)
        self.cancel_button.clicked.connect(self.close)

        buttons_layout.addWidget(self.new_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.cancel_button)

        main_layout.addWidget(self.table)
        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self._load_table()

    def _get_or_create_form(self):
        if self.form_view is None:
            self.form_view = RefillFormView()
            self.form_view.setAttribute(
                Qt.WidgetAttribute.WA_DeleteOnClose, True
            )
            self.form_view.save_button.clicked.connect(self.save_form)
            self.form_view.delete_button.clicked.connect(self.delete_form_entity)
            self.form_view.cancel_button.clicked.connect(self.form_view.close)
            self.form_view.destroyed.connect(self._on_form_closed)

        return self.form_view

    def _load_table(self):
        self.refills = sorted(
            self.service.get_all(),
            key=lambda refill: refill.id,
            reverse=True,
        )

        self.table.setRowCount(len(self.refills))

        for row, refill in enumerate(self.refills):
            self.table.setItem(row, 0, QTableWidgetItem(f"{refill.value:.2f}"))
            self.table.setItem(row, 1, QTableWidgetItem(f"{refill.liters:.3f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{refill.current_distance_traveled:.2f}"))

    def open_new_form(self):
        form = self._get_or_create_form()
        self._clear_form(form)
        self.hide()
        form.show()
        form.raise_()
        form.activateWindow()

    def open_edit_form(self):
        row = self.table.currentRow()

        if row < 0 or row >= len(self.refills):
            QMessageBox.warning(self, "Edit Refill", "Select a refill row first.")
            return

        refill = self.refills[row]
        form = self._get_or_create_form()
        self._fill_form(form, refill)
        self.hide()
        form.show()
        form.raise_()
        form.activateWindow()

    def _on_form_closed(self, _=None):
        self.form_view = None

        if self._is_closing:
            return

        self._load_table()
        self.show()
        self.raise_()
        self.activateWindow()

    def _clear_form(self, form: RefillFormView):
        form.id_input.setText("")
        form.value_input.setValue(0.0)
        form.liters_input.setValue(0.0)
        form.current_distance_traveled_input.setValue(0.0)
        form.delete_button.setEnabled(False)

    def _fill_form(self, form: RefillFormView, refill):
        form.id_input.setText(str(refill.id))
        form.value_input.setValue(float(refill.value))
        form.liters_input.setValue(float(refill.liters))
        form.current_distance_traveled_input.setValue(float(refill.current_distance_traveled))
        form.delete_button.setEnabled(True)

    def save_form(self):
        form = self._get_or_create_form()
        refill_id = form.id_input.text().strip()

        payload = {
            "value": Decimal(str(form.value_input.value())),
            "liters": form.liters_input.value(),
            "current_distance_traveled": form.current_distance_traveled_input.value(),
        }

        if refill_id:
            self.service.update(int(refill_id), **payload)
        else:
            created = self.service.create(**payload)
            form.id_input.setText(str(created.id))
            form.delete_button.setEnabled(True)

        form.close()

    def delete_form_entity(self):
        form = self._get_or_create_form()
        refill_id = form.id_input.text().strip()

        if not refill_id:
            return

        self.service.delete(int(refill_id))
        form.close()

    def closeEvent(self, event):
        self._is_closing = True

        if self.form_view is not None:
            self.form_view.close()

        self.session.close()
        super().closeEvent(event)
