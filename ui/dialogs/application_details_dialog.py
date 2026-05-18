from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QFrame,
    QMessageBox, QHBoxLayout, QScrollArea, QWidget
)

from database.application_repository import get_application_by_id, update_application_status
from services.pdf_service import generate_contract_pdf
from services.email_service import send_contract_email


class ApplicationDetailsDialog(QDialog):
    def __init__(self, application_id):
        super().__init__()
        self.application_id = application_id
        self.application_data = None
        self.pdf_path = None

        self.setWindowTitle("Перегляд заявки")
        self.resize(760, 680)
        self.setMinimumSize(620, 480)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(24, 24, 24, 24)
        self.scroll_layout.setSpacing(18)

        self.header_card = QFrame()
        self.header_card.setObjectName("topBanner")
        self.header_layout = QVBoxLayout()
        self.header_layout.setContentsMargins(24, 24, 24, 24)
        self.header_layout.setSpacing(8)

        self.title_label = QLabel("Заявка")
        self.title_label.setObjectName("bannerTitle")

        self.subtitle_label = QLabel("Детальна інформація")
        self.subtitle_label.setObjectName("bannerSubtitle")

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.subtitle_label)
        self.header_card.setLayout(self.header_layout)

        self.info_card = QFrame()
        self.info_card.setObjectName("contentCard")
        self.info_layout = QVBoxLayout()
        self.info_layout.setContentsMargins(24, 24, 24, 24)
        self.info_layout.setSpacing(12)
        self.info_card.setLayout(self.info_layout)

        self.buttons_row = QHBoxLayout()
        self.buttons_row.setSpacing(12)

        self.generate_pdf_button = QPushButton("Згенерувати PDF")
        self.generate_pdf_button.clicked.connect(self.generate_pdf)

        self.send_email_button = QPushButton("Надіслати PDF на пошту")
        self.send_email_button.setObjectName("success")
        self.send_email_button.clicked.connect(self.send_email)

        self.close_button = QPushButton("Закрити")
        self.close_button.setObjectName("secondary")
        self.close_button.clicked.connect(self.close)

        self.buttons_row.addStretch()
        self.buttons_row.addWidget(self.generate_pdf_button)
        self.buttons_row.addWidget(self.send_email_button)
        self.buttons_row.addWidget(self.close_button)

        self.scroll_layout.addWidget(self.header_card)
        self.scroll_layout.addWidget(self.info_card)
        self.scroll_layout.addLayout(self.buttons_row)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        self.load_application()

    def add_info_row(self, title, value):
        row = QFrame()
        row.setObjectName("statCard")
        row_layout = QVBoxLayout()
        row_layout.setContentsMargins(16, 14, 16, 14)
        row_layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("smallMuted")

        value_label = QLabel(str(value))
        value_label.setWordWrap(True)
        value_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #242852; background: transparent;")

        row_layout.addWidget(title_label)
        row_layout.addWidget(value_label)
        row.setLayout(row_layout)

        self.info_layout.addWidget(row)

    def load_application(self):
        self.application_data = get_application_by_id(self.application_id)

        if not self.application_data:
            QMessageBox.critical(self, "Помилка", "Заявку не знайдено")
            self.close()
            return

        self.title_label.setText(f"Заявка №{self.application_data['id_application']}")
        self.subtitle_label.setText(f"{self.application_data['full_name']} • {self.application_data['tour_name']}")

        self.add_info_row("Клієнт", self.application_data["full_name"])
        self.add_info_row("Телефон", self.application_data["phone"])
        self.add_info_row("Email", self.application_data["email"])
        self.add_info_row("Тур", self.application_data["tour_name"])
        self.add_info_row("Країна", self.application_data["country_name"])
        self.add_info_row("Дати", f"{self.application_data['start_date']} — {self.application_data['end_date']}")
        self.add_info_row("Автобус", self.application_data["bus_number"] if self.application_data["bus_number"] else "Не призначено")
        self.add_info_row("Місце", self.application_data["seat_number"] if self.application_data["seat_number"] else "Не обрано")
        self.add_info_row("Сума", f"{self.application_data['total_price']} грн")
        self.add_info_row("Статус", self.application_data["status"])
        self.add_info_row("Дата створення", self.application_data["created_at"])

    def generate_pdf(self):
        try:
            self.pdf_path = generate_contract_pdf(self.application_data)
            QMessageBox.information(self, "Успіх", f"PDF створено:\n{self.pdf_path}")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))

    def send_email(self):
        try:
            if not self.pdf_path:
                self.pdf_path = generate_contract_pdf(self.application_data)

            send_contract_email(
                self.application_data["email"],
                f"Договір Soft Travels №{self.application_data['id_application']}",
                "Доброго дня! У вкладенні знаходиться PDF-договір за вашим туристичним бронюванням.",
                self.pdf_path
            )

            update_application_status(self.application_id, "PDF надіслано")
            QMessageBox.information(self, "Успіх", "PDF-договір надіслано клієнту на пошту")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))