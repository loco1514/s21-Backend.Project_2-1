# s21-Backend.Project_2-1

## ShopAPI — краткое ТЗ

### Цель

Реализовать **RESTful API** для магазина бытовой техники.

### Стек

- HTTP/REST
- PostgreSQL
- Flask (Python)
- Документация — **OpenAPI 3.0** (Swagger UI)

**Базовый префикс роутов:** `/api/v1/...`
**Swagger:** `http://localhost:{PORT}/swagger/index.html`

---

### Сущности БД (PostgreSQL)

Использовать подходящие типы. Для уникальных идентификаторов — `UUID`.

- **client**`id, client_name, client_surname, birthday, gender, registration_date, address_id`
- **product**`id, name, category, price, available_stock, last_update_date, supplier_id, image_id UUID`
- **supplier**`id, name, address_id, phone_number`
- **images**`id UUID, image bytea`
- **address**
  `id, country, city, street`

Допускается добавление вспомогательных сущностей/связей. Реляционная модель, нормальные формы.

---

### CRUD-функциональность (общее)

Реализовать стандартные HTTP-методы: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.

#### Клиенты

- `POST /clients` — добавление клиента (JSON)
- `DELETE /clients/{id}` — удаление
- `GET /clients/search?name=&surname=` — выборка по имени и фамилии
- `GET /clients?limit=&offset=` — все клиенты (с пагинацией)
- `PATCH`/`PUT /clients/{id}/address` — смена адреса (JSON)

#### Товары

- `POST /products` — добавление товара (JSON)
- `PATCH /products/{id}/decrease` — уменьшение остатка
- `GET /products/{id}` — получить товар
- `GET /products` — список доступных товаров
- `DELETE /products/{id}` — удалить товар

#### Поставщики

- `POST /suppliers` — добавление (JSON)
- `PATCH`/`PUT /suppliers/{id}/address` — смена адреса (JSON)
- `DELETE /suppliers/{id}` — удаление
- `GET /suppliers` — список
- `GET /suppliers/{id}` — получить по id

#### Изображения

- `POST /images` — загрузка изображения (byte array) + productId
- `PUT`/`PATCH /images/{id}` — замена изображения (новые байты)
- `DELETE /images/{id}` — удаление
- `GET /products/{id}/image` — изображение товара
- `GET /images/{id}` — изображение по id
  **Ответ:** `Content-Type: application/octet-stream`, инициировать скачивание

---

### Валидация и ошибки

- Невалидные данные во входном теле → **400 Bad Request** с сообщением
- Поиск/обновление по несуществующему `id` → **404 Not Found** с сообщением
- Пустые выборки → пустой массив (не ошибка)

---

### Архитектура и требования к коду

- **RESTful-дизайн** эндпоинтов и семантика методов
- **PostgreSQL** как постоянное хранилище
- **Repository** — слой доступа к данным, поверх — сервисы
- **DAO/DTO** — DAO для работы с БД, DTO для коммуникации API
- **Мапперы** для преобразования между моделями БД и DTO
- **Swagger/OpenAPI** — полное покрытие методов, примеры объектов, комментарии для генерации
