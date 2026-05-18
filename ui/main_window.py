from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout,
    QGridLayout, QScrollArea, QComboBox, QStackedWidget
)

from database.reference_repository import (
    get_countries,
    get_rest_types,
    get_meal_types,
    get_hotel_levels,
    get_package_types
)
from database.stats_repository import get_dashboard_stats
from database.tour_repository import get_tours, get_tour_by_id
from ui.widgets.tour_card import TourCard
from ui.dialogs.add_tour_dialog import AddTourDialog
from ui.dialogs.create_application_dialog import CreateApplicationDialog
from ui.pages.clients_page import ClientsPage
from ui.pages.applications_page import ApplicationsPage


class MainWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.current_tour_id = None

        self.setObjectName("mainPage")
        self.setWindowTitle("Soft Travels")
        self.resize(1280, 820)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(0)

        self.outer_scroll = QScrollArea()
        self.outer_scroll.setWidgetResizable(True)

        self.outer_content = QWidget()
        self.outer_content_layout = QVBoxLayout()
        self.outer_content_layout.setContentsMargins(8, 8, 8, 8)
        self.outer_content_layout.setSpacing(18)

        self.banner = QFrame()
        self.banner.setObjectName("topBanner")

        self.banner_layout = QHBoxLayout()
        self.banner_layout.setContentsMargins(28, 24, 28, 24)
        self.banner_layout.setSpacing(20)

        self.banner_text_layout = QVBoxLayout()
        self.banner_text_layout.setSpacing(6)

        self.banner_title = QLabel("Soft Travels")
        self.banner_title.setObjectName("bannerTitle")

        self.banner_subtitle = QLabel(
            f'Вітаємо, {self.user["full_name"]}. Роль: {self.user["role_name"]}. Панель керування турами та клієнтами.'
        )
        self.banner_subtitle.setObjectName("bannerSubtitle")
        self.banner_subtitle.setWordWrap(True)

        self.banner_text_layout.addWidget(self.banner_title)
        self.banner_text_layout.addWidget(self.banner_subtitle)

        self.banner_buttons_layout = QHBoxLayout()
        self.banner_buttons_layout.setSpacing(12)

        self.tours_button = QPushButton("Тури")
        self.tours_button.setObjectName("secondary")
        self.tours_button.setMinimumHeight(48)
        self.tours_button.clicked.connect(self.show_tours_page)

        self.clients_button = QPushButton("Клієнти")
        self.clients_button.setObjectName("secondary")
        self.clients_button.setMinimumHeight(48)
        self.clients_button.clicked.connect(self.show_clients_page)

        self.applications_button = QPushButton("Заявки")
        self.applications_button.setObjectName("secondary")
        self.applications_button.setMinimumHeight(48)
        self.applications_button.clicked.connect(self.show_applications_page)

        self.add_tour_button = QPushButton("Додати тур")
        self.add_tour_button.setObjectName("success")
        self.add_tour_button.setMinimumHeight(48)
        self.add_tour_button.clicked.connect(self.open_add_tour_dialog)

        self.refresh_button = QPushButton("Оновити дані")
        self.refresh_button.setMinimumHeight(48)
        self.refresh_button.clicked.connect(self.refresh_all)

        self.banner_buttons_layout.addWidget(self.tours_button)
        self.banner_buttons_layout.addWidget(self.clients_button)
        self.banner_buttons_layout.addWidget(self.applications_button)
        self.banner_buttons_layout.addWidget(self.add_tour_button)
        self.banner_buttons_layout.addWidget(self.refresh_button)

        self.banner_layout.addLayout(self.banner_text_layout)
        self.banner_layout.addStretch()
        self.banner_layout.addLayout(self.banner_buttons_layout)

        self.banner.setLayout(self.banner_layout)

        self.stats_layout = QGridLayout()
        self.stats_layout.setSpacing(16)

        self.stat_card_1 = self.create_stat_card("Усього турів", "0")
        self.stat_card_2 = self.create_stat_card("Клієнтів", "0")
        self.stat_card_3 = self.create_stat_card("Заявок", "0")

        self.stats_layout.addWidget(self.stat_card_1["frame"], 0, 0)
        self.stats_layout.addWidget(self.stat_card_2["frame"], 0, 1)
        self.stats_layout.addWidget(self.stat_card_3["frame"], 0, 2)

        self.stacked = QStackedWidget()

        self.list_page = self.build_list_page()
        self.details_page = self.build_details_page()
        self.clients_page = ClientsPage()
        self.applications_page = ApplicationsPage()

        self.stacked.addWidget(self.list_page)
        self.stacked.addWidget(self.details_page)
        self.stacked.addWidget(self.clients_page)
        self.stacked.addWidget(self.applications_page)

        self.outer_content_layout.addWidget(self.banner)
        self.outer_content_layout.addLayout(self.stats_layout)
        self.outer_content_layout.addWidget(self.stacked)

        self.outer_content.setLayout(self.outer_content_layout)
        self.outer_scroll.setWidget(self.outer_content)

        self.main_layout.addWidget(self.outer_scroll)
        self.setLayout(self.main_layout)

        self.load_filter_data()
        self.refresh_all()

    def build_list_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        self.filters_card = QFrame()
        self.filters_card.setObjectName("contentCard")
        self.filters_layout = QVBoxLayout()
        self.filters_layout.setContentsMargins(20, 20, 20, 20)
        self.filters_layout.setSpacing(14)

        self.filters_title = QLabel("Фільтрація турів")
        self.filters_title.setObjectName("sectionTitle")

        self.filters_subtitle = QLabel("Оберіть параметри для швидкого пошуку")
        self.filters_subtitle.setObjectName("smallMuted")

        self.filters_row_1 = QHBoxLayout()
        self.filters_row_1.setSpacing(12)

        self.country_combo = QComboBox()
        self.country_combo.addItem("Усі країни", None)

        self.rest_type_combo = QComboBox()
        self.rest_type_combo.addItem("Усі типи відпочинку", None)

        self.meal_type_combo = QComboBox()
        self.meal_type_combo.addItem("Усі типи харчування", None)

        self.filters_row_1.addWidget(self.country_combo)
        self.filters_row_1.addWidget(self.rest_type_combo)
        self.filters_row_1.addWidget(self.meal_type_combo)

        self.filters_row_2 = QHBoxLayout()
        self.filters_row_2.setSpacing(12)

        self.hotel_level_combo = QComboBox()
        self.hotel_level_combo.addItem("Усі рівні готелів", None)

        self.package_type_combo = QComboBox()
        self.package_type_combo.addItem("Усі пакети", None)

        self.apply_filters_button = QPushButton("Застосувати фільтри")
        self.apply_filters_button.clicked.connect(self.load_tours)

        self.reset_filters_button = QPushButton("Скинути")
        self.reset_filters_button.setObjectName("secondary")
        self.reset_filters_button.clicked.connect(self.reset_filters)

        self.filters_row_2.addWidget(self.hotel_level_combo)
        self.filters_row_2.addWidget(self.package_type_combo)
        self.filters_row_2.addWidget(self.apply_filters_button)
        self.filters_row_2.addWidget(self.reset_filters_button)

        self.filters_layout.addWidget(self.filters_title)
        self.filters_layout.addWidget(self.filters_subtitle)
        self.filters_layout.addLayout(self.filters_row_1)
        self.filters_layout.addLayout(self.filters_row_2)

        self.filters_card.setLayout(self.filters_layout)

        self.content_card = QFrame()
        self.content_card.setObjectName("contentCard")

        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(14)

        self.section_title = QLabel("Доступні тури")
        self.section_title.setObjectName("sectionTitle")

        self.section_subtitle = QLabel("Оберіть тур і відкрийте повну інформацію")
        self.section_subtitle.setObjectName("smallMuted")

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout()
        self.cards_layout.setSpacing(18)
        self.cards_layout.setContentsMargins(4, 4, 4, 4)
        self.cards_container.setLayout(self.cards_layout)

        self.content_layout.addWidget(self.section_title)
        self.content_layout.addWidget(self.section_subtitle)
        self.content_layout.addWidget(self.cards_container)

        self.content_card.setLayout(self.content_layout)

        layout.addWidget(self.filters_card)
        layout.addWidget(self.content_card)

        page.setLayout(layout)
        return page

    def build_details_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        self.details_header = QFrame()
        self.details_header.setObjectName("topBanner")
        self.details_header_layout = QHBoxLayout()
        self.details_header_layout.setContentsMargins(24, 24, 24, 24)
        self.details_header_layout.setSpacing(16)

        self.details_title_wrap = QVBoxLayout()
        self.details_title_wrap.setSpacing(6)

        self.details_title = QLabel("Тур")
        self.details_title.setObjectName("bannerTitle")

        self.details_subtitle = QLabel("Повна інформація")
        self.details_subtitle.setObjectName("bannerSubtitle")
        self.details_subtitle.setWordWrap(True)

        self.details_title_wrap.addWidget(self.details_title)
        self.details_title_wrap.addWidget(self.details_subtitle)

        self.book_button = QPushButton("Записати клієнта")
        self.book_button.setObjectName("success")
        self.book_button.clicked.connect(self.open_create_application_dialog)

        self.back_button = QPushButton("Назад")
        self.back_button.setObjectName("secondary")
        self.back_button.clicked.connect(self.show_tours_page)

        self.details_header_layout.addLayout(self.details_title_wrap)
        self.details_header_layout.addStretch()
        self.details_header_layout.addWidget(self.book_button)
        self.details_header_layout.addWidget(self.back_button)

        self.details_header.setLayout(self.details_header_layout)

        self.details_image_card = QFrame()
        self.details_image_card.setObjectName("contentCard")
        self.details_image_card_layout = QVBoxLayout()
        self.details_image_card_layout.setContentsMargins(16, 16, 16, 16)

        self.details_image_label = QLabel()
        self.details_image_label.setMinimumHeight(320)
        self.details_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.details_image_label.setStyleSheet("background: #dbe8f5; border-radius: 14px;")

        self.details_image_card_layout.addWidget(self.details_image_label)
        self.details_image_card.setLayout(self.details_image_card_layout)

        self.details_info_card = QFrame()
        self.details_info_card.setObjectName("contentCard")
        self.details_info_layout = QVBoxLayout()
        self.details_info_layout.setContentsMargins(24, 24, 24, 24)
        self.details_info_layout.setSpacing(14)
        self.details_info_card.setLayout(self.details_info_layout)

        layout.addWidget(self.details_header)
        layout.addWidget(self.details_image_card)
        layout.addWidget(self.details_info_card)

        page.setLayout(layout)
        return page

    def create_stat_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("statCard")

        layout = QVBoxLayout()
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        number_label = QLabel(value)
        number_label.setObjectName("statNumber")

        text_label = QLabel(title)
        text_label.setObjectName("statText")

        layout.addWidget(number_label)
        layout.addWidget(text_label)
        frame.setLayout(layout)

        return {
            "frame": frame,
            "number": number_label,
            "text": text_label
        }

    def create_detail_row(self, title, value):
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

        return row

    def clear_cards(self):
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def clear_detail_rows(self):
        while self.details_info_layout.count():
            item = self.details_info_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def load_filter_data(self):
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

    def reset_filters(self):
        self.country_combo.setCurrentIndex(0)
        self.rest_type_combo.setCurrentIndex(0)
        self.meal_type_combo.setCurrentIndex(0)
        self.hotel_level_combo.setCurrentIndex(0)
        self.package_type_combo.setCurrentIndex(0)
        self.load_tours()

    def get_filter_values(self):
        return {
            "country_id": self.country_combo.currentData(),
            "rest_type_id": self.rest_type_combo.currentData(),
            "meal_type_id": self.meal_type_combo.currentData(),
            "hotel_level_id": self.hotel_level_combo.currentData(),
            "package_type_id": self.package_type_combo.currentData()
        }

    def refresh_all(self):
        self.load_stats()
        self.load_tours()
        self.clients_page.load_clients()
        self.applications_page.load_applications()

    def load_stats(self):
        stats = get_dashboard_stats()
        self.stat_card_1["number"].setText(str(stats["tours_count"]))
        self.stat_card_2["number"].setText(str(stats["clients_count"]))
        self.stat_card_3["number"].setText(str(stats["applications_count"]))

    def load_tours(self):
        tours = get_tours(self.get_filter_values())

        self.clear_cards()

        columns = 3
        row = 0
        col = 0

        for tour in tours:
            card = TourCard(tour, self.show_tour_details)
            self.cards_layout.addWidget(card, row, col)

            col += 1
            if col >= columns:
                col = 0
                row += 1

        while col != 0 and col < columns:
            spacer = QWidget()
            spacer.setStyleSheet("background: transparent;")
            self.cards_layout.addWidget(spacer, row, col)
            col += 1

    def set_details_image(self, image_path, fallback_text):
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.details_image_label.setPixmap(
                    pixmap.scaled(
                        1000,
                        320,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                return

        self.details_image_label.setText(fallback_text)
        self.details_image_label.setStyleSheet(
            "background: #dbe8f5; border-radius: 14px; color: #297FD5; font-size: 24px; font-weight: 700;"
        )

    def show_tour_details(self, tour_id):
        self.current_tour_id = tour_id
        tour = get_tour_by_id(tour_id)

        if not tour:
            return

        self.details_title.setText(tour["tour_name"])
        self.details_subtitle.setText(f'{tour["country_name"]} • {tour["rest_type_name"]}')
        self.set_details_image(tour["image_path"], tour["country_name"])

        self.clear_detail_rows()
        self.details_info_layout.addWidget(self.create_detail_row("Назва туру", tour["tour_name"]))
        self.details_info_layout.addWidget(self.create_detail_row("Країна", tour["country_name"]))
        self.details_info_layout.addWidget(self.create_detail_row("Тип відпочинку", tour["rest_type_name"]))
        self.details_info_layout.addWidget(self.create_detail_row("Тип харчування", tour["meal_type_name"]))
        self.details_info_layout.addWidget(self.create_detail_row("Рівень готелю", tour["hotel_level_name"]))
        self.details_info_layout.addWidget(self.create_detail_row("Пакет", tour["package_type_name"]))
        self.details_info_layout.addWidget(self.create_detail_row("Дата початку", tour["start_date"]))
        self.details_info_layout.addWidget(self.create_detail_row("Дата завершення", tour["end_date"]))
        self.details_info_layout.addWidget(self.create_detail_row("Вартість", f'{tour["price"]} грн'))
        self.details_info_layout.addWidget(
            self.create_detail_row("Автобус", tour["bus_number"] if tour["bus_number"] else "Не призначено")
        )
        self.details_info_layout.addStretch()

        self.stacked.setCurrentWidget(self.details_page)
        self.outer_scroll.verticalScrollBar().setValue(0)

    def show_tours_page(self):
        self.stacked.setCurrentWidget(self.list_page)
        self.outer_scroll.verticalScrollBar().setValue(0)

    def show_clients_page(self):
        self.clients_page.load_clients()
        self.stacked.setCurrentWidget(self.clients_page)
        self.outer_scroll.verticalScrollBar().setValue(0)

    def show_applications_page(self):
        self.applications_page.load_applications()
        self.stacked.setCurrentWidget(self.applications_page)
        self.outer_scroll.verticalScrollBar().setValue(0)

    def open_add_tour_dialog(self):
        dialog = AddTourDialog()
        if dialog.exec():
            self.refresh_all()
            self.show_tours_page()

    def open_create_application_dialog(self):
        if not self.current_tour_id:
            return

        dialog = CreateApplicationDialog(self.current_tour_id)
        if dialog.exec():
            self.refresh_all()
            self.show_applications_page()