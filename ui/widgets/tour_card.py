from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton


class TourCard(QFrame):
    def __init__(self, tour, open_callback):
        super().__init__()
        self.tour = tour
        self.open_callback = open_callback
        self.setObjectName("tourCard")
        self.setMinimumHeight(360)
        self.setMaximumWidth(360)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(12)

        self.image_label = QLabel()
        self.image_label.setMinimumHeight(180)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background: #dbe8f5; border-radius: 14px;")

        self.title_label = QLabel(self.tour["tour_name"])
        self.title_label.setObjectName("tourTitle")
        self.title_label.setWordWrap(True)

        self.meta_label = QLabel(
            f'{self.tour["country_name"]} • {self.tour["rest_type_name"]}\n{self.tour["start_date"]} — {self.tour["end_date"]}'
        )
        self.meta_label.setObjectName("tourMeta")
        self.meta_label.setWordWrap(True)

        self.price_label = QLabel(f'{self.tour["price"]} грн')
        self.price_label.setObjectName("tourPrice")

        self.open_button = QPushButton("Відкрити")
        self.open_button.clicked.connect(lambda: self.open_callback(self.tour["id_tour"]))

        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.meta_label)
        self.main_layout.addWidget(self.price_label)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.open_button)

        self.setLayout(self.main_layout)

        self.set_tour_image()

    def set_tour_image(self):
        image_path = self.tour.get("image_path")

        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(
                    pixmap.scaled(
                        320,
                        180,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )
                return

        self.image_label.setText(self.tour["country_name"])
        self.image_label.setStyleSheet(
            "background: #dbe8f5; border-radius: 14px; color: #297FD5; font-size: 20px; font-weight: 700;"
        )