import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def register_font():
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont("Arial", font_path))
        return "Arial"
    return "Helvetica"


def generate_contract_pdf(application_data):
    output_dir = os.path.join(os.getcwd(), "generated", "contracts")
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"contract_application_{application_data['id_application']}.pdf"
    file_path = os.path.join(output_dir, file_name)

    font_name = register_font()

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 60

    c.setFont(font_name, 18)
    c.drawString(50, y, "ДОГОВІР НА ТУРИСТИЧНЕ ОБСЛУГОВУВАННЯ")

    y -= 40
    c.setFont(font_name, 11)
    c.drawString(50, y, f"Номер заявки: {application_data['id_application']}")
    y -= 22
    c.drawString(50, y, f"Дата створення: {application_data['created_at']}")
    y -= 22
    c.drawString(50, y, f"Статус: {application_data['status']}")

    y -= 40
    c.setFont(font_name, 14)
    c.drawString(50, y, "Дані клієнта")

    y -= 28
    c.setFont(font_name, 11)
    c.drawString(50, y, f"ПІБ: {application_data['full_name']}")
    y -= 22
    c.drawString(50, y, f"Телефон: {application_data['phone']}")
    y -= 22
    c.drawString(50, y, f"Email: {application_data['email']}")

    y -= 40
    c.setFont(font_name, 14)
    c.drawString(50, y, "Дані туру")

    y -= 28
    c.setFont(font_name, 11)
    c.drawString(50, y, f"Назва туру: {application_data['tour_name']}")
    y -= 22
    c.drawString(50, y, f"Країна: {application_data['country_name']}")
    y -= 22
    c.drawString(50, y, f"Тип відпочинку: {application_data['rest_type_name']}")
    y -= 22
    c.drawString(50, y, f"Тип харчування: {application_data['meal_type_name']}")
    y -= 22
    c.drawString(50, y, f"Рівень готелю: {application_data['hotel_level_name']}")
    y -= 22
    c.drawString(50, y, f"Пакет: {application_data['package_type_name']}")
    y -= 22
    c.drawString(50, y, f"Дата початку: {application_data['start_date']}")
    y -= 22
    c.drawString(50, y, f"Дата завершення: {application_data['end_date']}")

    y -= 40
    c.setFont(font_name, 14)
    c.drawString(50, y, "Транспорт")

    y -= 28
    c.setFont(font_name, 11)
    c.drawString(50, y, f"Автобус: {application_data['bus_number'] if application_data['bus_number'] else 'Не призначено'}")
    y -= 22
    c.drawString(50, y, f"Місце: {application_data['seat_number'] if application_data['seat_number'] else 'Не обрано'}")

    y -= 40
    c.setFont(font_name, 14)
    c.drawString(50, y, "Оплата")

    y -= 28
    c.setFont(font_name, 11)
    c.drawString(50, y, f"Вартість туру: {application_data['total_price']} грн")

    y -= 60
    c.drawString(50, y, "Підпис менеджера: ____________________")
    c.drawString(330, y, "Підпис клієнта: ____________________")

    c.save()

    return file_path