import sys
from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #eef3f8;
            color: #242852;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QWidget#loginPage {
            background-color: #eef3f8;
        }

        QWidget#mainPage {
            background-color: #eef3f8;
        }

        QFrame#loginCard {
            background-color: #ffffff;
            border: 1px solid #d9e3ee;
            border-radius: 24px;
        }

        QFrame#topBanner {
            background-color: #242852;
            border-radius: 24px;
        }

        QFrame#contentCard {
            background-color: #ffffff;
            border: 1px solid #d9e3ee;
            border-radius: 20px;
        }

        QLabel#brandTitle {
            font-size: 34px;
            font-weight: 700;
            color: #242852;
            background: transparent;
        }

        QLabel#brandSubtitle {
            font-size: 15px;
            color: #7F8FA9;
            background: transparent;
        }

        QLabel#bannerTitle {
            font-size: 30px;
            font-weight: 700;
            color: white;
            background: transparent;
        }

        QLabel#bannerSubtitle {
            font-size: 14px;
            color: #d9e3ee;
            background: transparent;
        }

        QLabel#sectionTitle {
            font-size: 20px;
            font-weight: 700;
            color: #242852;
            background: transparent;
        }

        QLabel#smallMuted {
            font-size: 13px;
            color: #7F8FA9;
            background: transparent;
        }

        QLabel#statNumber {
            font-size: 24px;
            font-weight: 700;
            color: #242852;
            background: transparent;
        }

        QLabel#statText {
            font-size: 13px;
            color: #7F8FA9;
            background: transparent;
        }

        QFrame#statCard {
            background-color: #f8fbfe;
            border: 1px solid #d9e3ee;
            border-radius: 16px;
        }

        QFrame#tourCard {
            background-color: #ffffff;
            border: 1px solid #d9e3ee;
            border-radius: 18px;
        }

        QLabel#tourTitle {
            font-size: 18px;
            font-weight: 700;
            color: #242852;
            background: transparent;
        }

        QLabel#tourMeta {
            font-size: 13px;
            color: #7F8FA9;
            background: transparent;
        }

        QLabel#tourPrice {
            font-size: 20px;
            font-weight: 700;
            color: #297FD5;
            background: transparent;
        }

        QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox {
            background-color: #f8fafc;
            border: 1px solid #c7d3e2;
            border-radius: 14px;
            padding: 12px 14px;
            font-size: 14px;
            color: #242852;
        }

        QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus {
            border: 2px solid #297FD5;
            background-color: #ffffff;
        }

        QComboBox::drop-down, QDateEdit::drop-down, QDoubleSpinBox::drop-down {
            border: none;
            width: 28px;
        }

        QComboBox QAbstractItemView {
            background-color: #ffffff;
            border: 1px solid #c7d3e2;
            selection-background-color: #d9ebfb;
            selection-color: #242852;
        }

        QPushButton {
            background-color: #297FD5;
            color: white;
            border: none;
            border-radius: 14px;
            padding: 12px 18px;
            font-weight: 600;
        }

        QPushButton:hover {
            background-color: #629DD1;
        }

        QPushButton:pressed {
            background-color: #242852;
        }

        QPushButton#secondary {
            background-color: #ffffff;
            color: #242852;
            border: 1px solid #c7d3e2;
        }

        QPushButton#secondary:hover {
            background-color: #f4f8fc;
        }

        QPushButton#success {
            background-color: #1f8f5f;
            color: white;
        }

        QPushButton#success:hover {
            background-color: #27a06d;
        }

        QScrollArea {
            border: none;
            background: transparent;
        }

        QScrollBar:vertical {
            background: #edf2f7;
            width: 10px;
            margin: 2px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical {
            background: #7F8FA9;
            min-height: 30px;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background: #629DD1;
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
    """)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()