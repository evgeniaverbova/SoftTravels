from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QFormLayout, QLineEdit,
    QComboBox, QDateEdit, QDoubleSpinBox, QPushButton, QFileDialog,
    QMessageBox, QHBoxLayout, QScrollArea, QWidget
)

from database.reference_repository import (
    get_countries,
    get_rest_types,
    get_meal_types,
    get_hotel_levels,
    get_package_types,
    get_buses
)
from database.tour_repository import create_tour
from services.image_service import save_image_to_assets


class AddTourDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Додати тур")
        self.resize(650, 620)
        self.setMinimumSize(520, 420)
        self.image_source_path = None

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(24, 24, 24, 24)
        self.scroll_layout.setSpacing(18)

        self.header = QLabel("Створення нового туру")
        self.header.setObjectName("sectionTitle")

        self.form_card = QFrame()
        self.form_card.setObjectName("contentCard")

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(24, 24, 24, 24)
        self.form_layout.setSpacing(14)

        self.tour_name_input = QLineEdit()

        self.country_combo = QComboBox()
        self.rest_type_combo = QComboBox()
        self.meal_type_combo = QComboBox()
        self.hotel_level_combo = QComboBox()
        self.package_type_combo = QComboBox()
        self.bus_combo = QComboBox()

        self.start_date_input = QDateEdit()
        self.start_date_input.setCalendarPopup(True)
        self.start_date_input.setDate(QDate.currentDate())

        self.end_date_input = QDateEdit()
        self.end_date_input.setCalendarPopup(True)
        self.end_date_input.setDate(QDate.currentDate().addDays(7))

        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(10000000)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" грн")

        self.image_path_label = QLabel("Зображення не вибрано")
        self.image_path_label.setObjectName("smallMuted")
        self.image_path_label.setWordWrap(True)

        self.choose_image_button = QPushButton("Обрати зображення")
        self.choose_image_button.setObjectName("secondary")
        self.choose_image_button.clicked.connect(self.choose_image)

        self.form_layout.addRow("Назва туру", self.tour_name_input)
        self.form_layout.addRow("Країна", self.country_combo)
        self.form_layout.addRow("Тип відпочинку", self.rest_type_combo)
        self.form_layout.addRow("Тип харчування", self.meal_type_combo)
        self.form_layout.addRow("Рівень готелю", self.hotel_level_combo)
        self.form_layout.addRow("Пакет", self.package_type_combo)
        self.form_layout.addRow("Автобус", self.bus_combo)
        self.form_layout.addRow("Дата початку", self.start_date_input)
        self.form_layout.addRow("Дата завершення", self.end_date_input)
        self.form_layout.addRow("Ціна", self.price_input)
        self.form_layout.addRow("Файл зображення", self.image_path_label)
        self.form_layout.addRow("", self.choose_image_button)

        self.form_card.setLayout(self.form_layout)

        self.buttons_row = QHBoxLayout()
        self.buttons_row.setSpacing(12)

        self.cancel_button = QPushButton("Скасувати")
        self.cancel_button.setObjectName("secondary")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Зберегти тур")
        self.save_button.setObjectName("success")
        self.save_button.clicked.connect(self.save_tour)

        self.buttons_row.addStretch()
        self.buttons_row.addWidget(self.cancel_button)
        self.buttons_row.addWidget(self.save_button)

        self.scroll_layout.addWidget(self.header)
        self.scroll_layout.addWidget(self.form_card)
        self.scroll_layout.addLayout(self.buttons_row)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        self.load_reference_data()

    def load_reference_data(self):
        for item_id, item_name in get_countries():
            self.country_combo.addItem(item_name, item_id)

        for item_id, item_name in get_rest_types():
            self.rest_type_combo.addItem(item_name, item_id)

        for item_id, item_name in get_meal_types():
            self.meal_type_combo.addItem(item_name, item_id)

        for item_id, item_name in get_hotel_levels():
            self.hotel_level_combo.addItem(item_name, item_id)

        for item_id, item_name in get_package_types():
            self.package_type_combo.addItem(item_name, item_id)

        self.bus_combo.addItem("Без автобуса", None)
        for item_id, item_name in get_buses():
            self.bus_combo.addItem(item_name, item_id)

    def choose_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Оберіть зображення туру",
            "",
            "Images (*.png *.jpg *.jpeg *.webp)"
        )

        if file_path:
            self.image_source_path = file_path
            self.image_path_label.setText(file_path)

    def save_tour(self):
        tour_name = self.tour_name_input.text().strip()
        start_date = self.start_date_input.date().toString("yyyy-MM-dd")
        end_date = self.end_date_input.date().toString("yyyy-MM-dd")
        price = self.price_input.value()

        if not tour_name:
            QMessageBox.warning(self, "Помилка", "Вкажіть назву туру")
            return

        if self.end_date_input.date() < self.start_date_input.date():
            QMessageBox.warning(self, "Помилка", "Дата завершення не може бути раніше дати початку")
            return

        image_path = save_image_to_assets(self.image_source_path)

        create_tour({
            "tour_name": tour_name,
            "country_id": self.country_combo.currentData(),
            "rest_type_id": self.rest_type_combo.currentData(),
            "meal_type_id": self.meal_type_combo.currentData(),
            "hotel_level_id": self.hotel_level_combo.currentData(),
            "package_type_id": self.package_type_combo.currentData(),
            "start_date": start_date,
            "end_date": end_date,
            "price": price,
            "bus_id": self.bus_combo.currentData(),
            "image_path": image_path
        })

        QMessageBox.information(self, "Успіх", "Тур успішно додано")
        self.accept()