from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFrame, QComboBox, QPushButton,
    QMessageBox, QHBoxLayout, QGridLayout, QScrollArea, QWidget
)

from database.client_repository import get_clients
from database.bus_repository import get_tour_bus_info, get_bus_seats_by_tour
from database.application_repository import get_occupied_seat_ids, create_application
from ui.widgets.seat_button import SeatButton


class CreateApplicationDialog(QDialog):
    def __init__(self, tour_id):
        super().__init__()
        self.tour_id = tour_id
        self.selected_seat_id = None
        self.selected_button = None
        self.seat_buttons = []

        self.setWindowTitle("Записати клієнта на тур")
        self.resize(760, 680)
        self.setMinimumSize(620, 480)

        self.tour = get_tour_bus_info(self.tour_id)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

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

        self.title_label = QLabel("Запис клієнта на тур")
        self.title_label.setObjectName("bannerTitle")

        self.subtitle_label = QLabel(self.get_subtitle_text())
        self.subtitle_label.setObjectName("bannerSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.subtitle_label)
        self.header_card.setLayout(self.header_layout)

        self.client_card = QFrame()
        self.client_card.setObjectName("contentCard")
        self.client_layout = QVBoxLayout()
        self.client_layout.setContentsMargins(20, 20, 20, 20)
        self.client_layout.setSpacing(12)

        self.client_title = QLabel("1. Оберіть клієнта")
        self.client_title.setObjectName("sectionTitle")

        self.client_combo = QComboBox()
        self.load_clients()

        self.client_layout.addWidget(self.client_title)
        self.client_layout.addWidget(self.client_combo)
        self.client_card.setLayout(self.client_layout)

        self.seats_card = QFrame()
        self.seats_card.setObjectName("contentCard")
        self.seats_layout = QVBoxLayout()
        self.seats_layout.setContentsMargins(20, 20, 20, 20)
        self.seats_layout.setSpacing(14)

        self.seats_title = QLabel("2. Оберіть місце в автобусі")
        self.seats_title.setObjectName("sectionTitle")

        self.seats_hint = QLabel("Зелені місця — вільні, червоні — зайняті, синє — обране")
        self.seats_hint.setObjectName("smallMuted")

        self.seats_grid = QGridLayout()
        self.seats_grid.setSpacing(10)

        self.seats_layout.addWidget(self.seats_title)
        self.seats_layout.addWidget(self.seats_hint)
        self.seats_layout.addLayout(self.seats_grid)
        self.seats_card.setLayout(self.seats_layout)

        self.buttons_row = QHBoxLayout()
        self.buttons_row.setSpacing(12)

        self.cancel_button = QPushButton("Скасувати")
        self.cancel_button.setObjectName("secondary")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton("Створити заявку")
        self.save_button.setObjectName("success")
        self.save_button.clicked.connect(self.save_application)

        self.buttons_row.addStretch()
        self.buttons_row.addWidget(self.cancel_button)
        self.buttons_row.addWidget(self.save_button)

        self.scroll_layout.addWidget(self.header_card)
        self.scroll_layout.addWidget(self.client_card)
        self.scroll_layout.addWidget(self.seats_card)
        self.scroll_layout.addLayout(self.buttons_row)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.main_layout.addWidget(self.scroll_area)
        self.setLayout(self.main_layout)

        self.load_seats()

    def get_subtitle_text(self):
        if not self.tour:
            return "Тур не знайдено"

        bus_text = self.tour["bus_number"] if self.tour["bus_number"] else "автобус не призначено"

        return f'{self.tour["tour_name"]} • автобус: {bus_text} • вартість: {self.tour["price"]} грн'

    def load_clients(self):
        clients = get_clients()

        self.client_combo.clear()

        for client in clients:
            self.client_combo.addItem(
                f'{client["full_name"]} • {client["phone"]} • {client["email"]}',
                client["id_client"]
            )

    def load_seats(self):
        if not self.tour or not self.tour["bus_id"]:
            label = QLabel("Для цього туру не призначено автобус")
            label.setObjectName("smallMuted")
            self.seats_grid.addWidget(label, 0, 0)
            self.save_button.setEnabled(False)
            return

        seats = get_bus_seats_by_tour(self.tour_id)
        occupied_ids = get_occupied_seat_ids(self.tour_id)

        if not seats:
            label = QLabel("Для автобуса не створені місця")
            label.setObjectName("smallMuted")
            self.seats_grid.addWidget(label, 0, 0)
            self.save_button.setEnabled(False)
            return

        columns = 4
        row = 0
        col = 0

        for seat in seats:
            is_occupied = seat["id_bus_seat"] in occupied_ids
            button = SeatButton(
                seat["id_bus_seat"],
                seat["seat_number"],
                is_occupied
            )

            if not is_occupied:
                button.clicked.connect(lambda checked=False, btn=button: self.select_seat(btn))

            self.seat_buttons.append(button)
            self.seats_grid.addWidget(button, row, col)

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def select_seat(self, button):
        if self.selected_button:
            self.selected_button.set_free()

        self.selected_button = button
        self.selected_seat_id = button.seat_id
        button.set_selected()

    def save_application(self):
        client_id = self.client_combo.currentData()

        if not client_id:
            QMessageBox.warning(self, "Помилка", "Оберіть клієнта")
            return

        if not self.selected_seat_id:
            QMessageBox.warning(self, "Помилка", "Оберіть місце в автобусі")
            return

        try:
            create_application({
                "client_id": client_id,
                "tour_id": self.tour_id,
                "bus_seat_id": self.selected_seat_id,
                "total_price": self.tour["price"],
                "status": "Створена"
            })

            QMessageBox.information(self, "Успіх", "Заявку успішно створено")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Помилка", str(e))