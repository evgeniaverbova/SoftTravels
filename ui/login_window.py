from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFrame, QHBoxLayout, QSizePolicy
from services.auth import authenticate_user
from ui.main_window import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("loginPage")
        self.setWindowTitle("Soft Travels")
        self.resize(980, 620)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(24)

        self.left_panel = QFrame()
        self.left_panel.setObjectName("topBanner")
        self.left_panel.setMinimumWidth(420)

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(36, 36, 36, 36)
        self.left_layout.setSpacing(18)

        self.left_title = QLabel("Soft Travels")
        self.left_title.setObjectName("bannerTitle")

        self.left_subtitle = QLabel("Система управління туристичною компанією")
        self.left_subtitle.setObjectName("bannerSubtitle")
        self.left_subtitle.setWordWrap(True)

        self.left_text_1 = QLabel("• Керування турами та бронюваннями")
        self.left_text_1.setObjectName("bannerSubtitle")

        self.left_text_2 = QLabel("• Робота з клієнтами в одному середовищі")
        self.left_text_2.setObjectName("bannerSubtitle")

        self.left_text_3 = QLabel("• Створення заявок та перегляд актуальних даних")
        self.left_text_3.setObjectName("bannerSubtitle")
        self.left_text_3.setWordWrap(True)

        self.left_layout.addWidget(self.left_title)
        self.left_layout.addWidget(self.left_subtitle)
        self.left_layout.addSpacing(20)
        self.left_layout.addWidget(self.left_text_1)
        self.left_layout.addWidget(self.left_text_2)
        self.left_layout.addWidget(self.left_text_3)
        self.left_layout.addStretch()

        self.left_panel.setLayout(self.left_layout)

        self.right_panel = QFrame()
        self.right_panel.setObjectName("loginCard")
        self.right_panel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(44, 44, 44, 44)
        self.right_layout.setSpacing(16)

        self.brand_title = QLabel("Вхід до системи")
        self.brand_title.setObjectName("brandTitle")

        self.brand_subtitle = QLabel("Увійдіть як користувач системи")
        self.brand_subtitle.setObjectName("brandSubtitle")
        self.brand_subtitle.setWordWrap(True)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Логін")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Увійти")
        self.login_button.setMinimumHeight(50)
        self.login_button.clicked.connect(self.handle_login)

        self.demo_label = QLabel("Тестовий вхід: admin / 1234")
        self.demo_label.setObjectName("smallMuted")
        self.demo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.right_layout.addStretch()
        self.right_layout.addWidget(self.brand_title)
        self.right_layout.addWidget(self.brand_subtitle)
        self.right_layout.addSpacing(10)
        self.right_layout.addWidget(self.username_input)
        self.right_layout.addWidget(self.password_input)
        self.right_layout.addSpacing(8)
        self.right_layout.addWidget(self.login_button)
        self.right_layout.addWidget(self.demo_label)
        self.right_layout.addStretch()

        self.right_panel.setLayout(self.right_layout)

        self.main_layout.addWidget(self.left_panel, 5)
        self.main_layout.addWidget(self.right_panel, 6)

        self.setLayout(self.main_layout)

        self.main_window = None

    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Заповніть усі поля")
            return

        user = authenticate_user(username, password)

        if user:
            self.main_window = MainWindow(user)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Помилка", "Невірний логін або пароль")