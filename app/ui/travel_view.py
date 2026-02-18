from decimal import Decimal

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import QDateTime, Qt
from sqlalchemy.orm import sessionmaker

from app.db.session import engine
from app.service.travel_service import TravelService
from app.ui.travel_form_view import TravelFormView


class TravelView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Travels")
        self.resize(1200, 500)

        session_factory = sessionmaker(bind=engine)
        self.session = session_factory()
        self.service = TravelService(self.session)

        self.form_view = None
        self.travels = []
        self._is_closing = False

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
            "Time Total",
        ])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        self.table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)

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
            self.form_view = TravelFormView()
            self.form_view.setAttribute(
                Qt.WidgetAttribute.WA_DeleteOnClose, True
            )
            self.form_view.save_button.clicked.connect(self.save_form)
            self.form_view.delete_button.clicked.connect(self.delete_form_entity)
            self.form_view.cancel_button.clicked.connect(self.form_view.close)
            self.form_view.destroyed.connect(self._on_form_closed)

        return self.form_view

    def _load_table(self):
        self.travels = sorted(
            self.service.get_all(),
            key=lambda travel: (travel.time_end, travel.id),
            reverse=True,
        )

        self.table.setRowCount(len(self.travels))

        for row, travel in enumerate(self.travels):
            self.table.setItem(row, 0, QTableWidgetItem(f"{travel.total_value:.2f}"))
            self.table.setItem(row, 1, QTableWidgetItem(travel.street_start))
            self.table.setItem(row, 2, QTableWidgetItem(travel.neiborghood_start))
            self.table.setItem(row, 3, QTableWidgetItem(travel.street_end))
            self.table.setItem(row, 4, QTableWidgetItem(travel.neiborghood_end))
            self.table.setItem(row, 5, QTableWidgetItem(f"{travel.distance_start:.2f}"))
            self.table.setItem(row, 6, QTableWidgetItem(f"{travel.distance_travel:.2f}"))
            self.table.setItem(row, 7, QTableWidgetItem(travel.time_start.strftime("%Y-%m-%d %H:%M:%S")))
            self.table.setItem(row, 8, QTableWidgetItem(travel.time_reach.strftime("%Y-%m-%d %H:%M:%S")))
            self.table.setItem(row, 9, QTableWidgetItem(travel.time_end.strftime("%Y-%m-%d %H:%M:%S")))
            self.table.setItem(row, 10, QTableWidgetItem(str(travel.time_total)))

    def open_new_form(self):
        form = self._get_or_create_form()
        self._clear_form(form)
        self.hide()
        form.show()
        form.raise_()
        form.activateWindow()

    def open_edit_form(self):
        row = self.table.currentRow()

        if row < 0 or row >= len(self.travels):
            QMessageBox.warning(self, "Edit Travel", "Select a travel row first.")
            return

        travel = self.travels[row]
        form = self._get_or_create_form()
        self._fill_form(form, travel)
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

    def _clear_form(self, form: TravelFormView):
        form.id_input.setText("")
        form.total_value_input.setValue(0.0)
        form.street_start_input.setText("")
        form.neiborghood_start_input.setText("")
        form.street_end_input.setText("")
        form.neiborghood_end_input.setText("")
        form.distance_start_input.setValue(0.0)
        form.distance_travel_input.setValue(0.0)
        form.time_start_input.setDateTime(QDateTime.currentDateTime())
        form.time_reach_input.setDateTime(QDateTime.currentDateTime())
        form.time_end_input.setDateTime(QDateTime.currentDateTime())
        form.time_total_input.setValue(0)
        form.delete_button.setEnabled(False)

    def _fill_form(self, form: TravelFormView, travel):
        form.id_input.setText(str(travel.id))
        form.total_value_input.setValue(float(travel.total_value))
        form.street_start_input.setText(travel.street_start)
        form.neiborghood_start_input.setText(travel.neiborghood_start)
        form.street_end_input.setText(travel.street_end)
        form.neiborghood_end_input.setText(travel.neiborghood_end)
        form.distance_start_input.setValue(float(travel.distance_start))
        form.distance_travel_input.setValue(float(travel.distance_travel))
        form.time_start_input.setDateTime(travel.time_start)
        form.time_reach_input.setDateTime(travel.time_reach)
        form.time_end_input.setDateTime(travel.time_end)
        form.time_total_input.setValue(int(travel.time_total))
        form.delete_button.setEnabled(True)

    def save_form(self):
        form = self._get_or_create_form()
        travel_id = form.id_input.text().strip()

        payload = {
            "total_value": Decimal(str(form.total_value_input.value())),
            "street_start": form.street_start_input.text(),
            "neiborghood_start": form.neiborghood_start_input.text(),
            "street_end": form.street_end_input.text(),
            "neiborghood_end": form.neiborghood_end_input.text(),
            "distance_start": form.distance_start_input.value(),
            "distance_travel": form.distance_travel_input.value(),
            "time_start": form.time_start_input.dateTime().toPyDateTime(),
            "time_reach": form.time_reach_input.dateTime().toPyDateTime(),
            "time_end": form.time_end_input.dateTime().toPyDateTime(),
            "time_total": form.time_total_input.value(),
        }

        if travel_id:
            self.service.update(int(travel_id), **payload)
        else:
            created = self.service.create(**payload)
            form.id_input.setText(str(created.id))
            form.delete_button.setEnabled(True)

        form.close()

    def delete_form_entity(self):
        form = self._get_or_create_form()
        travel_id = form.id_input.text().strip()

        if not travel_id:
            return

        self.service.delete(int(travel_id))
        form.close()

    def closeEvent(self, event):
        self._is_closing = True

        if self.form_view is not None:
            self.form_view.close()

        self.session.close()
        super().closeEvent(event)
