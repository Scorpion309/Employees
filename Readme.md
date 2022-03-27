## Запуск проекта

- Установите и запустите docker.
- Скачайте проект из репозитория.
- Создайте файл .env и скопируйте в него содержимое файла .env.sample.
- В папке с файлом docker-compose.yml выполните команду:

    ```bash
    docker-compose up --build -d
    ```

- Выполните миграции базы данных, с помощью команды:

    ```bash
    docker-compose exec application python3 manage.py migrate --noinput
    ```
- Если получите следующую ошибку:

  ```
  django.db.utils.OperationalError: FATAL:  database "django_db" does not exist
  ```
- Остановите контейнер командой:

    ```bash
    docker-compose down -v
    ```
- Затем заново создайте образы, запустите контейнеры и примените миграции.

- Далее выполните создание супер пользователя, с помощью команды:

    ```bash
    docker-compose exec application python3 manage.py createsuperuser
    ```
- Запуск проекта осуществляется командой:

  ```bash
    docker-compose up
  ```

- Для проверки запуска проекта зайдите на страницу <http://localhost/admin/>.

Для загрузки данных в проект необходимо выполнить следующие действия:
