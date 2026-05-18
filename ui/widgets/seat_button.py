from PyQt6.QtWidgets import QPushButton


class SeatButton(QPushButton):
    def __init__(self, seat_id, seat_number, is_occupied=False):
        super().__init__(str(seat_number))
        self.seat_id = seat_id
        self.seat_number = seat_number
        self.is_occupied = is_occupied
        self.setFixedSize(48, 48)

        if self.is_occupied:
            self.set_occupied()
        else:
            self.set_free()

    def set_free(self):
        self.setEnabled(True)
        self.setStyleSheet("""
            QPushButton {
                background-color: #e8f7ef;
                color: #176b42;
                border: 1px solid #8fd3b0;
                border-radius: 10px;
                font-weight: 700;
            }
            QPushButton:hover {
                background-color: #d5f0e2;
            }
        """)

    def set_selected(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #297FD5;
                color: white;
                border: 2px solid #242852;
                border-radius: 10px;
                font-weight: 700;
            }
        """)

    def set_occupied(self):
        self.setEnabled(False)
        self.setStyleSheet("""
            QPushButton {
                background-color: #f4d7d7;
                color: #9b1c1c;
                border: 1px solid #e7a0a0;
                border-radius: 10px;
                font-weight: 700;
            }
        """)