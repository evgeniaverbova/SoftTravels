from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView

from database.client_repository import get_clients
from ui.dialogs.add_client_dialog import AddClientDialog


class ClientsPage(QWidget):
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

        self.title_label = QLabel("База клієнтів")
        self.title_label.setObjectName("sectionTitle")

        self.subtitle_label = QLabel("Перегляд і додавання клієнтів")
        self.subtitle_label.setObjectName("smallMuted")

        self.header_text_layout.addWidget(self.title_label)
        self.header_text_layout.addWidget(self.subtitle_label)

        self.add_client_button = QPushButton("Додати клієнта")
        self.add_client_button.setObjectName("success")
        self.add_client_button.clicked.connect(self.open_add_client_dialog)

        self.refresh_button = QPushButton("Оновити")
        self.refresh_button.setObjectName("secondary")
        self.refresh_button.clicked.connect(self.load_clients)

        self.header_layout.addLayout(self.header_text_layout)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.add_client_button)
        self.header_layout.addWidget(self.refresh_button)

        self.header_card.setLayout(self.header_layout)

        self.table_card = QFrame()
        self.table_card.setObjectName("contentCard")

        self.table_layout = QVBoxLayout()
        self.table_layout.setContentsMargins(20, 20, 20, 20)
        self.table_layout.setSpacing(12)

        self.clients_table = QTableWidget()
        self.clients_table.setColumnCount(4)
        self.clients_table.setHorizontalHeaderLabels([
            "ID",
            "ПІБ",
            "Телефон",
            "Email"
        ])
        self.clients_table.verticalHeader().setVisible(False)
        self.clients_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.clients_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.clients_table.setAlternatingRowColors(True)
        self.clients_table.setShowGrid(False)

        header = self.clients_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table_layout.addWidget(self.clients_table)
        self.table_card.setLayout(self.table_layout)

        self.main_layout.addWidget(self.header_card)
        self.main_layout.addWidget(self.table_card)

        self.setLayout(self.main_layout)

        self.load_clients()

    def load_clients(self):
        clients = get_clients()
        self.clients_table.setRowCount(len(clients))

        for i, client in enumerate(clients):
            self.clients_table.setItem(i, 0, QTableWidgetItem(str(client["id_client"])))
            self.clients_table.setItem(i, 1, QTableWidgetItem(client["full_name"]))
            self.clients_table.setItem(i, 2, QTableWidgetItem(client["phone"]))
            self.clients_table.setItem(i, 3, QTableWidgetItem(client["email"]))

            for j in range(4):
                item = self.clients_table.item(i, j)
                if j == 1 or j == 3:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.clients_table.resizeRowsToContents()

    def open_add_client_dialog(self):
        dialog = AddClientDialog()
        if dialog.exec():
            self.load_clients()