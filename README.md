1. File → Settings → Project → Python Interpreter 
Add Interpreter → Add Local Interpreter
Оберіть: Virtualenv Environment
New environment
Location: .venv

2. pip install -r requirements.txt
3. У корені проєкту створіть файл: .env
4. Скопіюйте в нього вміст із файлу .env.example
5. замініть
   
DB_HOST=127.0.0.1

DB_USER=root

DB_PASSWORD=password

DB_NAME=travel_agency_db

DB_PORT=3306

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587

SOFT_TRAVELS_EMAIL=keylibrary.app@gmail.com

SOFT_TRAVELS_EMAIL_PASSWORD=slnndxylvhxrlhvn

6. mysql -u root -p < database/schema.sql
