from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QFormLayout,
    QLineEdit, QPushButton, QMessageBox, QHBoxLayout
)

from database.client_repository import create_client


class AddClientDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Додати клієнта")
        self.resize(560, 420)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(24, 24, 24, 24)
        self.main_layout.setSpacing(18)

        self.header = QLabel("Створення нового клієнта")
        self.header.setObjectName("sectionTitle")

        self.form_card = QFrame()
        self.form_card.setObjectName("contentCard")

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(24, 24, 24, 24)
        self.form_layout.setSpacing(14)

        self.full_name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()

        self.form_layout.addRow("ПІБ", self.full_name_input)
        self.form_layout.addRow("Телефон", self.phone_input)
        self.form_layout.addRow("Email", self.email_input)
        self.form_layout.addRow("Пароль", self.password_input)

        self.form_card.setLayout(self.form_layout)

        self.buttons_row = QHBoxLayout()
        self.buttons_row.setSpacing(12)

        self.cancel_button = QPushButton("Скасувати")
        self.cancel_button.setObjectName("secondary")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Зберегти клієнта")
        self.save_button.setObjectName("success")
        self.save_button.clicked.connect(self.save_client)

        self.buttons_row.addStretch()
        self.buttons_row.addWidget(self.cancel_button)
        self.buttons_row.addWidget(self.save_button)

        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_card)
        self.main_layout.addLayout(self.buttons_row)

        self.setLayout(self.main_layout)

    def save_client(self):
        full_name = self.full_name_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not full_name or not phone or not email or not password:
            QMessageBox.warning(self, "Помилка", "Заповніть усі поля")
            return

        try:
            create_client({
                "full_name": full_name,
                "phone": phone,
                "email": email,
                "password_hash": password
            })
            QMessageBox.information(self, "Успіх", "Клієнта успішно додано")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))