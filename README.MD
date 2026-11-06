## Запуск всего проекта через Docker Compose

Docker Compose позволяет запустить Backend, Frontend и PostgreSQL одной командой.

### 1. Требования

Убедись, что установлены и запущены:

- Git
- Docker Desktop

### 2. Клонирование проекта

```powershell
git clone <REPOSITORY_URL>
cd todo-app
```

### 3. Настройка переменных окружения

Создай файл `.env` в корневой директории проекта на основе `.env.example`.

Пример конфигурации:

```env
app_name="Todo App"
database_url=postgresql+psycopg://todo_user:todo_pass@todo-postgres:5432/todo_db
database_user=todo_user
database_pass=todo_pass
```

### 4. Запуск сервисов

Из корневой директории проекта, где находится `docker-compose.yml`, выполни:

```powershell
docker compose up -d --build
```

Docker Compose автоматически:
- Соберёт Docker-образы Backend и Frontend.
- Создаст контейнеры.
- Создаст общую Docker-сеть.
- Запустит PostgreSQL.
- Запустит Backend и Frontend.

### 5. Проверка состояния сервисов

```powershell
docker compose ps
```

Просмотр логов всех сервисов:

```powershell
docker compose logs -f
```

Просмотр логов конкретного сервиса:

```powershell
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f db-postgres
```

### 6. Остановка сервисов

Остановить и удалить контейнеры и созданную Compose сеть:

```powershell
docker compose down
```

Данные PostgreSQL сохраняются в Docker volume, если он настроен в `docker-compose.yml`.

### 7. Повторный запуск

Если контейнеры уже созданы, повторный запуск выполняется командой:

```powershell
docker compose up -d
```

Если Dockerfile или зависимости изменились, используй:

```powershell
docker compose up -d --build
```