# hotel-api
## API для управления бронированием отеля

### Hotel Booking API

#### Описание проекта
API для управления номерами отеля, категориями номеров, удобствами и бронированиями. Проект реализован на Django REST Framework с поддержкой массовых операций, фильтрации, кеширования и JWT-аутентификации.

#### Функционал
- **Управление категориями номеров**: создание, редактирование, фильтрация по названию.
- **Управление номерами**: указание номера комнаты, привязка к категории, отметка о статусе уборки, множественные удобства (ManyToMany).
- **Удобства**: создание списка удобств (Wi-Fi, кондиционер и т.д.).
- **Бронирования**: гости могут бронировать номера с указанием дат заезда и выезда.
- **Массовые операции**: создание, обновление и удаление пачками (списком).
- **Кеширование**: GET-запросы детального просмотра кешируются на 15 минут.
- **JWT-аутентификация**: защита эндпоинтов с помощью токенов.

#### Эндпоинты

##### Основные ресурсы

**Аутентификация**
- `POST /api/token/` — получение access и refresh токенов (требует username и password)
- `POST /api/token/refresh/` — обновление access токена

**Категории номеров (RoomCategories)**
- `GET /api/v1/categories/` — список категорий (фильтрация по name)
- `POST /api/v1/categories/` — создание одной или списка категорий
- `GET /api/v1/categories/{id}/` — получение категории (кешируется)
- `PUT /api/v1/categories/{id}/` — полное обновление
- `PATCH /api/v1/categories/{id}/` — частичное обновление
- `DELETE /api/v1/categories/{id}/` — удаление одной категории
- `DELETE /api/v1/categories/?ids=1,2,3` — массовое удаление

**Номера (Rooms)**
- `GET /api/v1/rooms/` — список номеров (фильтрация по category_id, room_number)
- `POST /api/v1/rooms/` — создание номера (требует category_id)
- `GET /api/v1/rooms/{id}/` — получение номера с вложенной категорией и удобствами (кешируется)
- `PUT /api/v1/rooms/{id}/` — полное обновление
- `PATCH /api/v1/rooms/{id}/` — частичное обновление
- `DELETE /api/v1/rooms/{id}/` — удаление номера
- `DELETE /api/v1/rooms/?ids=1,2,3` — массовое удаление

**Удобства (Amenities)**
- `GET /api/v1/amenities/` — список удобств
- `POST /api/v1/amenities/` — создание одного или списка удобств
- `GET /api/v1/amenities/{id}/` — получение удобства (кешируется)
- `PUT /api/v1/amenities/{id}/` — полное обновление
- `PATCH /api/v1/amenities/{id}/` — частичное обновление
- `DELETE /api/v1/amenities/{id}/` — удаление удобства
- `DELETE /api/v1/amenities/?ids=1,2,3` — массовое удаление

**Бронирования (Bookings)**
- `GET /api/v1/bookings/` — список бронирований (фильтрация по room_id, guest_name)
- `POST /api/v1/bookings/` — создание бронирования (требует room_id, check_in_date, check_out_date)
- `GET /api/v1/bookings/{id}/` — получение бронирования (кешируется)
- `PUT /api/v1/bookings/{id}/` — полное обновление
- `PATCH /api/v1/bookings/{id}/` — частичное обновление
- `DELETE /api/v1/bookings/{id}/` — удаление бронирования
- `DELETE /api/v1/bookings/?ids=1,2,3` — массовое удаление

#### Документация API

Интерактивная документация доступна по адресу:
- **Swagger UI**: `/api/schema/swagger-ui/`
- **OpenAPI схема**: `/api/schema/`

#### Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать: `venv\Scripts\activate`
4. Установить зависимости: `pip install -r requirements.txt`
5. Применить миграции: `python manage.py migrate`
6. Создать суперпользователя: `python manage.py createsuperuser`
7. Запустить сервер: `python manage.py runserver 8000`

#### Технологии

- Python 3.x
- Django 5.x
- Django REST Framework
- Microsoft SQL Server (via `mssql-django`)
- drf-spectacular (Swagger)
- drf-extensions (для кеширования)
- djangorestframework-simplejwt (JWT-аутентификация)

#### Автор

Svetlana