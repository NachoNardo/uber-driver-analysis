import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from app.ui.main_view import MainView


def main():
    app = QApplication(sys.argv)

    base_dir = Path(__file__).resolve().parent
    icon_path = base_dir / "utils" / "imgs" / "logo.png"

    app.setWindowIcon(QIcon(str(icon_path)))

    window = MainView()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
