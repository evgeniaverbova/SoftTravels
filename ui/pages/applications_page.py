from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
)

from database.application_repository import get_applications
from ui.dialogs.application_details_dialog import ApplicationDetailsDialog


class ApplicationsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(18)

        self.header_card = QFrame()
        self.header_card.setObjectName("contentCard")

        self.header_layout = QHBoxLayout()
        self.header_layout.setContentsMargins(20, 20, 20, 20)
        self.header_layout.setSpacing(12)

        self.header_text_layout = QVBoxLayout()
        self.header_text_layout.setSpacing(6)

        self.title_label = QLabel("Заявки")
        self.title_label.setObjectName("sectionTitle")

        self.subtitle_label = QLabel("Перегляд бронювань, договорів і статусів")
        self.subtitle_label.setObjectName("smallMuted")

        self.header_text_layout.addWidget(self.title_label)
        self.header_text_layout.addWidget(self.subtitle_label)

        self.refresh_button = QPushButton("Оновити")
        self.refresh_button.setObjectName("secondary")
        self.refresh_button.clicked.connect(self.load_applications)

        self.open_button = QPushButton("Відкрити заявку")
        self.open_button.setObjectName("success")
        self.open_button.clicked.connect(self.open_selected_application)

        self.header_layout.addLayout(self.header_text_layout)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.open_button)
        self.header_layout.addWidget(self.refresh_button)

        self.header_card.setLayout(self.header_layout)

        self.table_card = QFrame()
        self.table_card.setObjectName("contentCard")

        self.table_layout = QVBoxLayout()
        self.table_layout.setContentsMargins(20, 20, 20, 20)
        self.table_layout.setSpacing(12)

        self.applications_table = QTableWidget()
        self.applications_table.setColumnCount(8)
        self.applications_table.setHorizontalHeaderLabels([
            "ID",
            "Клієнт",
            "Телефон",
            "Email",
            "Тур",
            "Місце",
            "Сума",
            "Статус"
        ])
        self.applications_table.verticalHeader().setVisible(False)
        self.applications_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.applications_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.applications_table.setAlternatingRowColors(True)
        self.applications_table.setShowGrid(False)

        header = self.applications_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)

        self.applications_table.cellDoubleClicked.connect(self.open_selected_application)

        self.table_layout.addWidget(self.applications_table)
        self.table_card.setLayout(self.table_layout)

        self.main_layout.addWidget(self.header_card)
        self.main_layout.addWidget(self.table_card)

        self.setLayout(self.main_layout)

        self.load_applications()

    def load_applications(self):
        applications = get_applications()
        self.applications_table.setRowCount(len(applications))

        for i, application in enumerate(applications):
            values = [
                application["id_application"],
                application["full_name"],
                application["phone"],
                application["email"],
                application["tour_name"],
                application["seat_number"] if application["seat_number"] else "-",
                application["total_price"],
                application["status"]
            ]

            for j, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                if j in [1, 3, 4]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.applications_table.setItem(i, j, item)

        self.applications_table.resizeRowsToContents()

    def get_selected_application_id(self):
        selected_row = self.applications_table.currentRow()

        if selected_row < 0:
            return None

        item = self.applications_table.item(selected_row, 0)

        if not item:
            return None

        return int(item.text())

    def open_selected_application(self):
        application_id = self.get_selected_application_id()

        if not application_id:
            return

        dialog = ApplicationDetailsDialog(application_id)
        dialog.exec()
        self.load_applications()