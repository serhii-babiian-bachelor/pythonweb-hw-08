# Contacts API — FastAPI + PostgreSQL

REST API для управління контактами, створений з використанням FastAPI, SQLAlchemy та PostgreSQL.

## Функціонал

- Створення нового контакту
- Отримання списку всіх контактів
- Отримання контакту за ID
- Оновлення контакту
- Видалення контакту
- Пошук контактів за:
  - ім’ям
  - прізвищем
  - email
- Отримання контактів з днями народження на найближчі 7 днів
- Swagger/OpenAPI документація

---

# Технології

- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn

---

# Структура проєкту

```bash
pythonweb-hw-08/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│
├── requirements.txt
├── .gitignore
├── README.md

Встановлення та запуск
1. Клонувати репозиторій
git clone https://github.com/YOUR_USERNAME/UMT-pythonweb-hw-08.git
2. Перейти в папку проєкту
cd UMT-pythonweb-hw-08
3. Створити та активувати віртуальне середовище
Mac/Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate
4. Встановити залежності
pip install -r requirements.txt
Налаштування PostgreSQL
Створити базу даних
CREATE DATABASE contacts_api;
Вказати дані підключення

У файлі database.py:

DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/contacts_api"
Запуск проєкту
uvicorn app.main:app --reload
Swagger документація

Після запуску доступно:

Swagger UI
http://127.0.0.1:8000/docs
ReDoc
http://127.0.0.1:8000/redoc
API Endpoints
Method	Endpoint	Description
POST	/contacts/	Create contact
GET	/contacts/	Get all contacts
GET	/contacts/{contact_id}	Get contact by ID
PUT	/contacts/{contact_id}	Update contact
DELETE	/contacts/{contact_id}	Delete contact
GET	/search/	Search contacts
GET	/birthdays/	Upcoming birthdays
Приклад JSON для створення контакту
{
  "first_name": "Serhii",
  "last_name": "Babiian",
  "email": "serhii@test.com",
  "phone": "123456789",
  "birthday": "1999-05-15",
  "additional_data": "QA Engineer"
}
Автор

Serhii Babiian

QA Engineer | Python Backend Developer
