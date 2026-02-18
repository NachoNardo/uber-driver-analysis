from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

# from app.ui.analisys_view import AnalisysView
from app.ui.refill_view import RefillView
from app.ui.travel_view import TravelView


class MainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("UberAnalysis")

        self.travels_view = None
        self.refills_view = None
        # self.analisys_view = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        self.travels_button = QPushButton("Travels")
        self.refills_button = QPushButton("Refills")
        # self.analysis_button = QPushButton("Analysis")

        for button in (
            self.travels_button,
            self.refills_button,
            # self.analysis_button,
        ):
            button.setMinimumHeight(40)
            button.setMinimumWidth(200)

        self.travels_button.clicked.connect(self.open_travels_view)
        self.refills_button.clicked.connect(self.open_refills_view)
        # self.analysis_button.clicked.connect(self.open_analisys_view)

        layout.addWidget(self.travels_button)
        layout.addWidget(self.refills_button)
        # layout.addWidget(self.analysis_button)

        central_widget.setLayout(layout)

        self.adjustSize()
        self.setFixedSize(self.size())

    def open_travels_view(self):
        if self.travels_view is None:
            self.travels_view = TravelView()
            self.travels_view.setAttribute(
                Qt.WidgetAttribute.WA_DeleteOnClose, True
            )
            self.travels_view.destroyed.connect(self._on_travels_view_closed)

        self.hide()
        self.travels_view.show()
        self.travels_view.raise_()
        self.travels_view.activateWindow()

    def open_refills_view(self):
        if self.refills_view is None:
            self.refills_view = RefillView()
            self.refills_view.setAttribute(
                Qt.WidgetAttribute.WA_DeleteOnClose, True
            )
            self.refills_view.destroyed.connect(self._on_refills_view_closed)

        self.hide()
        self.refills_view.show()
        self.refills_view.raise_()
        self.refills_view.activateWindow()

    def _on_travels_view_closed(self, _=None):
        self.travels_view = None
        self.show()
        self.raise_()
        self.activateWindow()

    def _on_refills_view_closed(self, _=None):
        self.refills_view = None
        self.show()
        self.raise_()
        self.activateWindow()

    # def open_analisys_view(self):
    #     if self.analisys_view is None:
    #         self.analisys_view = AnalisysView()

    #     self.analisys_view.show()
    #     self.analisys_view.raise_()
    #     self.analisys_view.activateWindow()
