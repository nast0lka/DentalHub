# DentalHub

Система управления стоматологической клиникой на базе FastAPI.

---

## Содержание

- [Обзор](#обзор)
- [Технологии](#технологии)
- [Архитектура](#архитектура)
- [Быстрый старт](#быстрый-старт)
- [Конфигурация](#конфигурация)
- [API](#api)
- [Структура проекта](#структура-проекта)

---

## Обзор

DentalHub — веб-приложение для автоматизации работы стоматологической клиники. Система охватывает полный цикл взаимодействия с пациентом: от регистрации и записи на приём до управления врачами, услугами и специализациями.

**Основной функционал:**

- Управление записями на приём (создание, редактирование, отмена)
- Каталог врачей с информацией о специализациях
- Прайс-лист услуг клиники
- Регистрация и аутентификация пользователей с подтверждением по email
- Административная панель для управления данными
- REST API для внешних интеграций
- Асинхронная отправка email через Celery + Redis

---

## Технологии

| Компонент | Технология |
|---|---|
| Web-фреймворк | FastAPI |
| ORM | SQLAlchemy (async) |
| База данных | PostgreSQL 17 |
| Миграции | Alembic |
| Валидация | Pydantic v2 |
| Админ-панель | SQLAdmin |
| Очередь задач | Celery |
| Брокер сообщений | Redis |
| Шаблонизатор | Jinja2 |
| Контейнеризация | Docker / Docker Compose |

---

## Архитектура

Приложение разворачивается в четырёх Docker-контейнерах:

```
┌─────────────┐     ┌─────────────┐
│   web        │     │   celery    │
│  FastAPI     │     │   worker    │
│  :8000       │     │             │
└──────┬───────┘     └──────┬──────┘
       │                    │
       ▼                    ▼
┌─────────────┐     ┌─────────────┐
│  database   │     │    redis    │
│ PostgreSQL  │     │   :6379     │
│  :5432      │     │             │
└─────────────┘     └─────────────┘
```

- **web** — FastAPI приложение, обрабатывает HTTP запросы
- **database** — PostgreSQL, основное хранилище данных
- **redis** — брокер сообщений для Celery
- **celery** — воркер для асинхронных задач (отправка email)

---

## Быстрый старт

### Требования

- Docker Desktop 4.0+
- Docker Compose v2

### Установка

**1. Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/dentalhub.git
cd dentalhub
```

**2. Создайте файл `.env`** на основе примера ниже и заполните своими значениями.

**3. Запустите контейнеры:**
```bash
docker-compose up --build
```

**4. Приложение доступно по адресам:**

| Сервис | URL |
|---|---|
| Веб-интерфейс | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Админ-панель | http://localhost:8000/admin |

---

## Конфигурация

Создайте файл `.env` в корне проекта:

```dotenv
# База данных
DB_HOST=database
DB_PORT=5432
DB_USER=postgres
DB_PASS=your_password
DB_NAME=dentalhub

# JWT
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0

# SMTP (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

> **Важно:** для отправки почты через Gmail необходимо использовать [пароль приложения](https://myaccount.google.com/apppasswords), а не пароль аккаунта. Двухфакторная аутентификация должна быть включена.

### Docker Compose

Сервисы и их зависимости:

```yaml
web       depends_on → database (healthy)
celery    depends_on → database (healthy), redis (healthy)
```

Все сервисы имеют `healthcheck` — приложение и воркер стартуют только после того, как БД и Redis готовы принимать соединения.

**Управление контейнерами:**

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Пересборка после изменений
docker-compose up --build

# Логи конкретного сервиса
docker-compose logs -f web
docker-compose logs -f celery
```

---

## API

Полная документация доступна в Swagger UI после запуска приложения: `http://localhost:8000/docs`

Основные группы эндпоинтов:

| Префикс | Описание |
|---|---|
| `/auth` | Регистрация, вход, подтверждение email |
| `/appointments` | Управление записями на приём |
| `/doctors` | Информация о врачах |
| `/services` | Каталог услуг и прайс-лист |
| `/admin` | Административная панель |

---

## Структура проекта

```
dentalhub/
├── app/
│   ├── main.py              # Точка входа FastAPI
│   ├── config.py            # Настройки приложения
│   ├── database.py          # Подключение к БД
│   ├── users/               # Аутентификация и пользователи
│   ├── appointments/        # Записи на приём
│   ├── doctors/             # Врачи и специализации
│   ├── services/            # Услуги клиники
│   ├── tasks/               # Celery задачи
│   │   ├── celery.py        # Конфигурация Celery
│   │   ├── tasks.py         # Определение задач
│   │   └── email_templates.py
│   ├── pages/               # Роутеры для HTML страниц
│   ├── templates/           # Jinja2 шаблоны
│   └── static/              # Статические файлы
├── migrations/              # Alembic миграции
├── docker-compose.yaml
├── Dockerfile
├── .env
└── requirements.txt
```